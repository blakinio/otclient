#!/usr/bin/env python3
"""Exact-current be4f48 native-login worker using the physically proven secret-ingress shape."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shlex
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


def _write_bundle_file_as_target(source: Path, target: str) -> None:
    command = [
        "docker", "exec", "-i", "-u", _base.TARGET_USER,
        _base.TARGET_CONTAINER,
        "sh", "-c", 'umask 077; cat > "$1"', "sh", target,
    ]
    try:
        with source.open("rb") as handle:
            completed = subprocess.run(
                command,
                check=False,
                stdin=handle,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30,
                env=_base._clean_env(),
                close_fds=True,
            )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PhysicalError("helper_install_stream_failed") from exc
    if completed.returncode != 0:
        raise PhysicalError("helper_install_stream_failed")


def _install_bundle_user_owned(bundle: Path) -> None:
    _base._verify_bundle(bundle)
    uid, gid = _base._numeric_user()
    if uid < 1 or gid < 1:
        raise PhysicalError("helper_install_identity_invalid")

    # The reset must not inherit the container image's default USER. The stale
    # task root may contain files created by prior Docker-side installs, so use
    # explicit container root only for deleting this exact bounded task path.
    root_uid = _docker_stage(
        ["docker", "exec", "-u", "0", _base.TARGET_CONTAINER, "id", "-u"],
        "helper_install_root_exec_unavailable",
    ).strip()
    if root_uid != "0":
        raise PhysicalError("helper_install_root_exec_unavailable")
    _docker_stage(
        ["docker", "exec", "-u", "0", _base.TARGET_CONTAINER, "rm", "-rf", _base.TASK_ROOT],
        "helper_install_reset_failed",
    )

    # From this point forward the helper runtime is owned and populated only by
    # the exact GUI user; no chown or docker cp ownership repair is permitted.
    _docker_stage(
        [
            "docker", "exec", "-u", _base.TARGET_USER, _base.TARGET_CONTAINER,
            "install", "-d", "-m", "700", _base.TASK_ROOT,
        ],
        "helper_install_prepare_failed",
    )

    root_identity = _docker_stage(
        [
            "docker", "exec", "-u", _base.TARGET_USER, _base.TARGET_CONTAINER,
            "stat", "-c", "%u:%g:%a", _base.TASK_ROOT,
        ],
        "helper_install_identity_invalid",
    ).strip()
    if root_identity != f"{uid}:{gid}:700":
        raise PhysicalError("helper_install_identity_invalid")

    for name, target in _base.BUNDLE_FILES.items():
        _write_bundle_file_as_target(bundle / name, target)
        _docker_stage(
            [
                "docker", "exec", "-u", _base.TARGET_USER, _base.TARGET_CONTAINER,
                "chmod", "600", target,
            ],
            "helper_install_stream_failed",
        )
        file_identity = _docker_stage(
            [
                "docker", "exec", "-u", _base.TARGET_USER, _base.TARGET_CONTAINER,
                "stat", "-c", "%u:%g:%a", target,
            ],
            "helper_install_identity_invalid",
        ).strip()
        if file_identity != f"{uid}:{gid}:600":
            raise PhysicalError("helper_install_identity_invalid")

    try:
        manifest = json.loads((bundle / _base.BUNDLE_MANIFEST).read_text(encoding="utf-8"))["files"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise PhysicalError("helper_bundle_manifest_invalid") from exc
    for name, expected in manifest.items():
        output = _docker_stage(
            [
                "docker", "exec", "-u", _base.TARGET_USER, _base.TARGET_CONTAINER,
                "sha256sum", _base.BUNDLE_FILES[name],
            ],
            "helper_install_digest_read_failed",
        )
        parts = output.split()
        if not parts or parts[0] != expected:
            raise PhysicalError("installed_helper_digest_mismatch")


def _launcher_env(*, instrumented: bool) -> list[str]:
    env_args = [
        "-e", "HOME=/home/kasm-user",
        "-e", f"DISPLAY={_base.TARGET_DISPLAY}",
        "-e", "XAUTHORITY=/home/kasm-user/.Xauthority",
        "-e", f"LD_LIBRARY_PATH={_base.PACKAGE_DIR}:{_base.PACKAGE_DIR}/lib",
    ]
    if instrumented:
        env_args.extend([
            "-e", f"LD_PRELOAD={_base.BRIDGE_SO}:{_base.AUTH_SO}:{_base.CHARACTER_SO}",
            "-e", f"OTCLIENT_TIBIA_RE_SOCKET={_base.BRIDGE_SOCKET}",
            "-e", f"OTCLIENT_TIBIA_RE_AUTH_SOCKET={_base.AUTH_SOCKET}",
            "-e", f"OTCLIENT_TIBIA_RE_CHARACTER_SOCKET={_base.CHARACTER_SOCKET}",
            "-e", f"OTCLIENT_TIBIA_RE_BINARY_SHA256={_base.EXPECTED_SHA}",
            "-e", f"OTCLIENT_TIBIA_RE_CLIENT_VERSION={_base.EXPECTED_VERSION}",
            "-e", f"OTCLIENT_TIBIA_RE_TARGETS={_base._profile_targets()}",
        ])
    return env_args


def _launch_exact_client(*, instrumented: bool) -> subprocess.CompletedProcess[str]:
    legacy_email, legacy_password = _base._legacy_credential_env_names()
    command = [
        "docker", "exec", "-d", "-u", _base.TARGET_USER, "-w", _base.PACKAGE_DIR,
        *_launcher_env(instrumented=instrumented),
        _base.TARGET_CONTAINER,
        "/usr/bin/env",
        "-u", "RUNNER_TRACKING_ID",
        "-u", legacy_email,
        "-u", legacy_password,
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN",
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN_FILE",
    ]
    if not instrumented:
        command.extend([
            "-u", "LD_PRELOAD",
            "-u", "OTCLIENT_TIBIA_RE_SOCKET",
            "-u", "OTCLIENT_TIBIA_RE_AUTH_SOCKET",
            "-u", "OTCLIENT_TIBIA_RE_CHARACTER_SOCKET",
            "-u", "OTCLIENT_TIBIA_RE_BINARY_SHA256",
            "-u", "OTCLIENT_TIBIA_RE_CLIENT_VERSION",
            "-u", "OTCLIENT_TIBIA_RE_TARGETS",
        ])
    launch_script = f"cd {shlex.quote(_base.PACKAGE_DIR)} && exec ./client"
    command.extend(["sh", "-lc", launch_script])
    return _base._run(command, timeout=20)


def _wait_exact_runtime(old_pid: int, old_start: int, *, seconds: float = 30.0) -> dict[str, Any]:
    deadline = time.monotonic() + seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            manifest = _base._current_manifest()
            if manifest.get("pid") != old_pid and manifest.get("process_start_ticks") != old_start:
                return manifest
        except Exception as exc:
            last_error = exc
        time.sleep(0.5)
    raise PhysicalError("replacement_rollback_runtime_not_ready") from last_error


def _stop_failed_replacement_if_present(old_pid: int, old_start: int, uid: int) -> None:
    try:
        manifest = _base._current_manifest()
    except PhysicalError:
        return
    pid = int(manifest.get("pid", -1))
    start = int(manifest.get("process_start_ticks", -1))
    if pid == old_pid or start == old_start:
        return
    if not _base.same_numeric_uid(pid, uid):
        raise PhysicalError("replacement_failed_candidate_uid_mismatch")
    stopped = _base._run([
        "docker", "exec", "-u", _base.TARGET_USER, _base.TARGET_CONTAINER,
        "kill", "-TERM", str(pid),
    ])
    if stopped.returncode != 0:
        raise PhysicalError("replacement_failed_candidate_SIGTERM_failed")
    _base._wait_pid_gone(pid)


def _rollback_exact_client(old_pid: int, old_start: int, uid: int, result: Path) -> None:
    _stop_failed_replacement_if_present(old_pid, old_start, uid)
    launch = _launch_exact_client(instrumented=False)
    if launch.returncode != 0:
        raise PhysicalError("replacement_rollback_launch_failed")
    rollback = _wait_exact_runtime(old_pid, old_start)
    if not _base.same_numeric_uid(int(rollback["pid"]), uid):
        raise PhysicalError("replacement_rollback_uid_mismatch")
    _base._write_json(result, {
        "schema": "otclient.track-a.native-login-replacement.v1",
        "exact_current": True,
        "instrumented_ready": False,
        "rollback_exact_current": True,
        "rollback_registration_recovery_required": True,
        "pid": rollback["pid"],
        "process_start_ticks": rollback["process_start_ticks"],
        "boot_id_sha256": rollback["boot_id_sha256"],
        "candidate_fingerprint": rollback["candidate_fingerprint"],
        "helpers_ready": False,
        "credential_plaintext_accessed": False,
        "secret_attempt_count": 0,
    })


def replace(vault_dir: Path, bundle: Path, result: Path) -> None:
    _base._vault_precheck(vault_dir)
    _base._verify_bundle(bundle)
    registration = _base._read_registration()
    manifest = _base._current_manifest()
    _base._require_manifest_matches_registration(manifest, registration)
    uid, _gid = _base._numeric_user()
    if not _base.same_numeric_uid(int(registration["pid"]), uid):
        raise PhysicalError("same_numeric_uid_failed")

    _install_bundle_user_owned(bundle)
    old_pid = int(registration["pid"])
    old_start = int(registration["process_start_ticks"])
    stopped = _base._run([
        "docker", "exec", "-u", _base.TARGET_USER, _base.TARGET_CONTAINER,
        "kill", "-TERM", str(old_pid),
    ])
    if stopped.returncode != 0:
        raise PhysicalError("exact_registered_SIGTERM_failed")
    _base._wait_pid_gone(old_pid)

    # Fail closed if another exact-current process appeared before replacement.
    try:
        unexpected = _base._current_manifest()
    except PhysicalError:
        unexpected = None
    if unexpected is not None:
        raise PhysicalError("post_SIGTERM_exact_client_still_present")

    launch = _launch_exact_client(instrumented=True)
    if launch.returncode != 0:
        _rollback_exact_client(old_pid, old_start, uid, result)
        raise PhysicalError("replacement_instrumented_launch_failed")

    try:
        replacement = _base._wait_replacement(old_pid, old_start)
    except PhysicalError as exc:
        _rollback_exact_client(old_pid, old_start, uid, result)
        raise PhysicalError("replacement_instrumented_runtime_not_ready_rollback_restored") from exc

    _base._write_json(result, {
        "schema": "otclient.track-a.native-login-replacement.v1",
        "exact_current": True,
        "instrumented_ready": True,
        "rollback_exact_current": False,
        "rollback_registration_recovery_required": False,
        "pid": replacement["pid"],
        "process_start_ticks": replacement["process_start_ticks"],
        "boot_id_sha256": replacement["boot_id_sha256"],
        "candidate_fingerprint": replacement["candidate_fingerprint"],
        "helpers_ready": True,
        "credential_plaintext_accessed": False,
        "secret_attempt_count": 0,
    })


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
    # Override only the corrected install/replacement/ingress seams. Character
    # confirmation remains the base implementation, preserving its recursion fix.
    _base.precheck = precheck
    _base._install_bundle = _install_bundle_user_owned
    _base.replace = replace
    _base.auth_one_shot = auth_one_shot
    return int(_base.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
