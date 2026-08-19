from __future__ import annotations

import argparse
import ctypes
import fcntl
import os
from pathlib import Path
import resource
import struct
import subprocess
import sys

_MAX_FIELD_BYTES = 1024
_HEADER = struct.Struct("<II")
_KEY_NAME = "tibia-test-credentials.key"
_CERT_NAME = "tibia-test-credentials.crt"
_VAULT_NAME = "tibia-test-credentials.cms"


class SecretVaultError(RuntimeError):
    pass


def _harden_process() -> None:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(4, 0, 0, 0, 0) != 0:  # PR_SET_DUMPABLE
            raise OSError(ctypes.get_errno(), "prctl(PR_SET_DUMPABLE) failed")
    except (AttributeError, OSError):
        pass


def _run(args: list[str], *, data: bytes | bytearray | None = None) -> bytes:
    result = subprocess.run(
        args,
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise SecretVaultError(f"OpenSSL operation failed with status {result.returncode}")
    return result.stdout


def _paths(vault_dir: Path) -> tuple[Path, Path, Path]:
    root = vault_dir.resolve()
    return root / _KEY_NAME, root / _CERT_NAME, root / _VAULT_NAME


def ensure_identity(vault_dir: Path) -> tuple[Path, Path, Path]:
    vault_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(vault_dir, 0o700)
    key, cert, vault = _paths(vault_dir)
    if not key.exists():
        _run([
            "openssl", "genpkey", "-algorithm", "RSA",
            "-pkeyopt", "rsa_keygen_bits:4096", "-out", str(key),
        ])
        os.chmod(key, 0o600)
    if not cert.exists():
        _run([
            "openssl", "req", "-new", "-x509", "-sha256", "-days", "3650",
            "-key", str(key), "-out", str(cert),
            "-subj", "/CN=otclient-track-a-local-secret-vault",
        ])
        os.chmod(cert, 0o600)
    if key.stat().st_mode & 0o077:
        raise SecretVaultError("vault private key permissions are too broad")
    return key, cert, vault


def _credential_frame(email: str, password: str) -> bytearray:
    email_bytes = email.encode("utf-8")
    password_bytes = password.encode("utf-8")
    if not (1 <= len(email_bytes) <= _MAX_FIELD_BYTES):
        raise SecretVaultError("email length is outside the bounded credential frame")
    if not (1 <= len(password_bytes) <= _MAX_FIELD_BYTES):
        raise SecretVaultError("password length is outside the bounded credential frame")
    if b"\0" in email_bytes or b"\0" in password_bytes:
        raise SecretVaultError("NUL bytes are forbidden in credentials")
    return bytearray(_HEADER.pack(len(email_bytes), len(password_bytes)) + email_bytes + password_bytes)


def seed_from_environment(vault_dir: Path) -> None:
    _harden_process()
    email = os.environ.pop("TIBIA_TEST_EMAIL", "")
    password = os.environ.pop("TIBIA_TEST_PASSWORD", "")
    if not email or not password:
        raise SecretVaultError("required GitHub Actions Secrets are unavailable")
    key, cert, vault = ensure_identity(vault_dir)
    frame = _credential_frame(email, password)
    try:
        sealed = _run([
            "openssl", "cms", "-encrypt", "-binary", "-aes256",
            "-outform", "DER", str(cert),
        ], data=frame)
        tmp = vault.with_suffix(".cms.new")
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            os.write(fd, sealed)
            os.fsync(fd)
        finally:
            os.close(fd)
        os.replace(tmp, vault)
        os.chmod(vault, 0o600)
    finally:
        for index in range(len(frame)):
            frame[index] = 0
        del email, password, key


def _decrypt_frame(vault_dir: Path) -> bytearray:
    _harden_process()
    key, cert, vault = _paths(vault_dir)
    for path in (key, cert, vault):
        if not path.is_file():
            raise SecretVaultError(f"required vault component is missing: {path.name}")
    if key.stat().st_mode & 0o077:
        raise SecretVaultError("vault private key permissions are too broad")
    plaintext = bytearray(_run([
        "openssl", "cms", "-decrypt", "-binary", "-inform", "DER",
        "-in", str(vault), "-recip", str(cert), "-inkey", str(key),
    ]))
    if len(plaintext) < _HEADER.size + 2:
        raise SecretVaultError("decrypted credential frame is truncated")
    email_len, password_len = _HEADER.unpack_from(plaintext)
    if not (1 <= email_len <= _MAX_FIELD_BYTES and 1 <= password_len <= _MAX_FIELD_BYTES):
        raise SecretVaultError("decrypted credential lengths are invalid")
    if len(plaintext) != _HEADER.size + email_len + password_len:
        raise SecretVaultError("decrypted credential frame length mismatch")
    return plaintext


def decrypt_to_sealed_memfd(vault_dir: Path) -> int:
    frame = _decrypt_frame(vault_dir)
    flags = getattr(os, "MFD_CLOEXEC", 0) | getattr(os, "MFD_ALLOW_SEALING", 0)
    fd = os.memfd_create("tibia-native-auth-credentials", flags)
    try:
        os.write(fd, frame)
        os.lseek(fd, 0, os.SEEK_SET)
        required = fcntl.F_SEAL_SEAL | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_GROW | fcntl.F_SEAL_WRITE
        fcntl.fcntl(fd, fcntl.F_ADD_SEALS, required)
        return fd
    except Exception:
        os.close(fd)
        raise
    finally:
        for index in range(len(frame)):
            frame[index] = 0


def verify(vault_dir: Path) -> None:
    fd = decrypt_to_sealed_memfd(vault_dir)
    os.close(fd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Machine-local encrypted Tibia test credential vault")
    parser.add_argument("operation", choices=("seed", "verify"))
    parser.add_argument("--vault-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.operation == "seed":
        seed_from_environment(args.vault_dir)
        print("SECRET_VAULT_SEED=PASS")
    else:
        verify(args.vault_dir)
        print("SECRET_VAULT_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SecretVaultError as exc:
        print(f"secret vault error: {exc}", file=sys.stderr)
        raise SystemExit(2)
