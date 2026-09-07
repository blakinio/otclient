#!/usr/bin/env python3
"""Exact-current be4f48 native-login worker using the physically proven secret-ingress shape."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import sys
import time
from typing import Any, Sequence

_BASE_PATH = Path(__file__).with_name("track_a_native_login_be4f48_physical_base.py")
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

SECRET_INGRESS_NAME = "native_login_secret_ingress.py"


def _load_base() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_native_login_be4f48_physical_base", _BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("physical_base_worker_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_base = _load_base()
PhysicalError = _base.PhysicalError
SECRET_INGRESS = _base.TASK_ROOT + "/" + SECRET_INGRESS_NAME
_base.BUNDLE_FILES[SECRET_INGRESS_NAME] = SECRET_INGRESS


def _vault_frame(vault_dir: Path) -> bytearray:
    from tools.tibia_runtime_bridge import secret_vault

    frame = secret_vault._decrypt_frame(vault_dir)
    if not isinstance(frame, bytearray) or len(frame) < 10:
        raise PhysicalError("vault_credential_frame_invalid")
    return frame


def _split_frame(frame: bytearray) -> tuple[str, str]:
    header = struct.Struct("<II")
    try:
        email_len, password_len = header.unpack_from(frame)
    except struct.error as exc:
        raise PhysicalError("vault_credential_frame_invalid") from exc
    if not (1 <= email_len <= 1024 and 1 <= password_len <= 1024):
        raise PhysicalError("vault_credential_frame_invalid")
    if len(frame) != header.size + email_len + password_len:
        raise PhysicalError("vault_credential_frame_invalid")
    start = header.size
    try:
        email = bytes(frame[start : start + email_len]).decode("utf-8")
        password = bytes(frame[start + email_len :]).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PhysicalError("vault_credential_frame_invalid") from exc
    if not email or not password or "\0" in email or "\0" in password:
        raise PhysicalError("vault_credential_frame_invalid")
    return email, password


def _parse_ingress_stdout(stdout: str) -> dict[str, Any]:
    if len(stdout.encode("utf-8", "replace")) > 1_048_576:
        raise PhysicalError("native_auth_ingress_response_too_large")
    lines = [line for line in stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise PhysicalError("native_auth_ingress_response_invalid")
    try:
        response = json.loads(lines[0])
    except json.JSONDecodeError as exc:
        raise PhysicalError("native_auth_ingress_response_invalid") from exc
    allowed = {"ok", "command", "invocation_dispatched", "qmeta_method_id", "error", "fd_sent"}
    if not isinstance(response, dict) or not set(response).issubset(allowed) or not isinstance(response.get("ok"), bool):
        raise PhysicalError("native_auth_ingress_response_invalid")
    return response


def _run_proven_secret_ingress(vault_dir: Path, registration: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    frame = _vault_frame(vault_dir)
    email = password = ""
    env: dict[str, str] | None = None
    try:
        email, password = _split_frame(frame)
        env = _base._clean_env()
        env["TIBIA_TEST_EMAIL"] = email
        env["TIBIA_TEST_PASSWORD"] = password
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [
            "docker", "exec", "-i", "-u", _base.TARGET_USER,
            "-e", "TIBIA_TEST_EMAIL",
            "-e", "TIBIA_TEST_PASSWORD",
            "-e", "PYTHONDONTWRITEBYTECODE",
            _base.TARGET_CONTAINER,
            "python3", SECRET_INGRESS,
            "--socket", _base.AUTH_SOCKET,
            "--boot-id-sha256", str(registration["boot_id_sha256"]),
            "--pid", str(registration["pid"]),
            "--start-ticks", str(registration["process_start_ticks"]),
            "--client-version", _base.EXPECTED_VERSION,
            "--client-size", str(_base.EXPECTED_SIZE),
            "--client-sha256", _base.EXPECTED_SHA,
            "--timeout", "8.0",
        ]
        try:
            completed = subprocess.run(
                command,
                check=False,
                text=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=20,
                env=env,
                close_fds=True,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise PhysicalError("native_auth_secret_ingress_process_failed") from exc
        response = _parse_ingress_stdout(completed.stdout)
        return completed.returncode, response
    finally:
        for index in range(len(frame)):
            frame[index] = 0
        if env is not None:
            env.pop("TIBIA_TEST_EMAIL", None)
            env.pop("TIBIA_TEST_PASSWORD", None)
        email = ""
        password = ""


def precheck(vault_dir: Path, bundle: Path, result: Path) -> None:
    _base._vault_precheck(vault_dir)
    _base._verify_bundle(bundle)
    registration = _base._read_registration()
    manifest = _base._current_manifest()
    _base._require_manifest_matches_registration(manifest, registration)
    uid, gid = _base._numeric_user()
    if not _base.same_numeric_uid(int(manifest["pid"]), uid):
        raise PhysicalError("same_numeric_uid_failed")
    ingress = bundle / SECRET_INGRESS_NAME
    try:
        info = ingress.lstat()
    except OSError as exc:
        raise PhysicalError("secret_ingress_bundle_missing") from exc
    if not stat.S_ISREG(info.st_mode) or ingress.is_symlink():
        raise PhysicalError("secret_ingress_bundle_invalid")
    _base._write_json(result, {
        "schema": "otclient.track-a.native-login-physical-precheck.v1",
        "exact_current": True,
        "target_unique": True,
        "registration_current": True,
        "same_numeric_uid": True,
        "secret_ingress_ready": True,
        "vault_bind": "HOST_ONLY_PRESENT_PRIVATE",
        "credential_plaintext_accessed": False,
        "target_uid": uid,
        "target_gid": gid,
    })


def _docker_stage(command: Sequence[str], failure_code: str, *, timeout: int = 30) -> str:
    completed = _base._run(command, timeout=timeout)
    if completed.returncode != 0:
        raise PhysicalError(failure_code)
    return completed.stdout


def _install_bundle_numeric(bundle: Path) -> None:
    _base._verify_bundle(bundle)
    uid, gid = _base._numeric_user()
    if uid < 1 or gid < 1:
        raise PhysicalError("helper_install_numeric_identity_invalid")

    _docker_stage(
        ["docker", "exec", _base.TARGET_CONTAINER, "install", "-d", "-m", "700", _base.TASK_ROOT],
        "helper_install_prepare_failed",
    )

    cleanup_paths = list(dict.fromkeys((
        _base.BRIDGE_SOCKET,
        _base.AUTH_SOCKET,
        _base.CHARACTER_SOCKET,
        *_base.BUNDLE_FILES.values(),
    )))
    for target in cleanup_paths:
        _docker_stage(
            ["docker", "exec", _base.TARGET_CONTAINER, "rm", "-f", target],
            "helper_install_cleanup_failed",
        )

    for name, target in _base.BUNDLE_FILES.items():
        completed = _base._run(
            ["docker", "cp", str(bundle / name), f"{_base.TARGET_CONTAINER}:{target}"],
            timeout=30,
        )
        if completed.returncode != 0:
            raise PhysicalError("helper_bundle_copy_failed")

    owner = f"{uid}:{gid}"
    for target in _base.BUNDLE_FILES.values():
        _docker_stage(
            ["docker", "exec", _base.TARGET_CONTAINER, "chown", owner, target],
            "helper_install_permissions_failed",
        )
        _docker_stage(
            ["docker", "exec", _base.TARGET_CONTAINER, "chmod", "600", target],
            "helper_install_permissions_failed",
        )

    try:
        manifest = json.loads((bundle / _base.BUNDLE_MANIFEST).read_text(encoding="utf-8"))["files"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise PhysicalError("helper_bundle_manifest_invalid") from exc
    for name, expected in manifest.items():
        output = _docker_stage(
            ["docker", "exec", _base.TARGET_CONTAINER, "sha256sum", _base.BUNDLE_FILES[name]],
            "helper_install_digest_read_failed",
        )
        parts = output.split()
        if not parts or parts[0] != expected:
            raise PhysicalError("installed_helper_digest_mismatch")


def auth_one_shot(vault_dir: Path, result: Path) -> None:
    registration = _base._read_registration()
    manifest = _base._current_manifest()
    _base._require_manifest_matches_registration(manifest, registration)
    uid, _gid = _base._numeric_user()
    if not _base.same_numeric_uid(int(registration["pid"]), uid):
        raise PhysicalError("same_numeric_uid_failed")
    if _base._run([
        "docker", "exec", "-u", _base.TARGET_USER, _base.TARGET_CONTAINER,
        "test", "-S", _base.AUTH_SOCKET,
    ]).returncode != 0:
        raise PhysicalError("native_auth_socket_missing")

    rc, response = _run_proven_secret_ingress(vault_dir, registration)
    if rc == 0:
        if response.get("ok") is not True or response.get("invocation_dispatched") is not True:
            raise PhysicalError("native_auth_response_not_dispatch_proof")
        outcome = "PASS_RESPONSE"
    elif (
        rc == 79
        and response.get("fd_sent") is True
        and response.get("error") == "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND"
    ):
        deadline = time.monotonic() + 15.0
        handoff: dict[str, Any] | None = None
        while time.monotonic() < deadline:
            try:
                candidate = _base._current_manifest()
                if (
                    candidate.get("pid") != registration.get("pid")
                    and candidate.get("process_start_ticks") != registration.get("process_start_ticks")
                ):
                    handoff = candidate
                    break
            except PhysicalError:
                pass
            time.sleep(0.5)
        if handoff is None:
            raise PhysicalError("native_auth_one_shot_failed_without_proven_handoff")
        outcome = "PASS_WITH_PROCESS_HANDOFF"
    else:
        raise PhysicalError("native_auth_secret_ingress_failed")

    _base._write_json(result, {
        "schema": "otclient.track-a.native-login-auth.v1",
        "native_auth_ingress": outcome,
        "secret_source": "machine_local_encrypted_vault",
        "secret_ingress": "bounded_docker_exec",
        "sealed_memfd": True,
        "scm_rights": True,
        "secret_attempt_count": 1,
        "NO_SECOND_SECRET_ATTEMPT": True,
        "credential_values_logged": False,
    })


def main(argv: Sequence[str] | None = None) -> int:
    # Only corrected ingress/install seams are replaced. Base replace() and
    # confirm_unique() remain untouched, preserving the recursion regression fix.
    _base.precheck = precheck
    _base._install_bundle = _install_bundle_numeric
    _base.auth_one_shot = auth_one_shot
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
