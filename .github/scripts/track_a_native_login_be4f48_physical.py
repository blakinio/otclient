#!/usr/bin/env python3
"""Bounded physical worker for exact-current be4f48 native login on canonical KasmVNC."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time
from typing import Any, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tibia_runtime_bridge.secret_vault import SecretVaultError, decrypt_to_sealed_memfd

TARGET_CONTAINER = "otclient-track-a-kasmvnc"
TARGET_DISPLAY = ":1"
TARGET_USER = "kasm-user"
PACKAGE_DIR = "/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia"
CLIENT_PATH = PACKAGE_DIR + "/bin/client"
EXPECTED_VERSION = "15.32.be4f48"
EXPECTED_SIZE = 52105824
EXPECTED_SHA = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
PROOF_KIND = "existing_runtime_adoption_v1"
TASK_ROOT = "/tmp/otclient-native-login-current-sha"
BRIDGE_SOCKET = TASK_ROOT + "/bridge.sock"
AUTH_SOCKET = TASK_ROOT + "/auth.sock"
CHARACTER_SOCKET = TASK_ROOT + "/character.sock"
BRIDGE_SO = TASK_ROOT + "/otclient-tibia-runtime-bridge.so"
AUTH_SO = TASK_ROOT + "/otclient-tibia-native-auth-experimental.so"
CHARACTER_SO = TASK_ROOT + "/otclient-tibia-character-control-current.so"
CONTAINER_CLIENT = TASK_ROOT + "/container_native_login_client.py"
PROFILE = TASK_ROOT + "/tibia-15.32.be4f48.json"
REGISTRATION = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json")
PROBE_PATH = REPO_ROOT / ".github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py"
PROFILE_PATH = REPO_ROOT / "tools/tibia_runtime_bridge/profiles/tibia-15.32.be4f48.json"
BUNDLE_MANIFEST = "bundle-manifest.json"
BUNDLE_FILES = {
    "otclient-tibia-runtime-bridge.so": BRIDGE_SO,
    "otclient-tibia-native-auth-experimental.so": AUTH_SO,
    "otclient-tibia-character-control-current.so": CHARACTER_SO,
    "container_native_login_client.py": CONTAINER_CLIENT,
    "tibia-15.32.be4f48.json": PROFILE,
}


class PhysicalError(RuntimeError):
    pass


def _legacy_credential_env_names() -> tuple[str, str]:
    prefix = "_".join(("TIBIA", "TEST"))
    return prefix + "_" + "EMAIL", prefix + "_" + "PASSWORD"


def _clean_env() -> dict[str, str]:
    env = dict(os.environ)
    legacy = set(_legacy_credential_env_names())
    for key in list(env):
        if key in legacy or "LEASE_TOKEN" in key.upper() or "CAPABILITY" in key.upper():
            env.pop(key, None)
    return env


def _run(command: Sequence[str], *, timeout: int = 30, pass_fds: tuple[int, ...] = ()) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            list(command),
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=_clean_env(),
            close_fds=True,
            pass_fds=pass_fds,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PhysicalError(f"command_failed:{Path(command[0]).name}") from exc


def _require_success(command: Sequence[str], *, timeout: int = 30) -> str:
    completed = _run(command, timeout=timeout)
    if completed.returncode != 0:
        raise PhysicalError(f"command_failed:{Path(command[0]).name}:{completed.returncode}")
    return completed.stdout


def _load_probe_module() -> Any:
    spec = importlib.util.spec_from_file_location("track_a_kasm_existing_runtime_probe", PROBE_PATH)
    if spec is None or spec.loader is None:
        raise PhysicalError("canonical_probe_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _current_manifest() -> dict[str, Any]:
    module = _load_probe_module()
    try:
        result = module.collect()
    except Exception as exc:
        raise PhysicalError("canonical_probe_failed") from exc
    if not isinstance(result, dict) or result.get("proof_kind") != PROOF_KIND:
        raise PhysicalError("canonical_probe_invalid")
    if (
        result.get("client_version") != EXPECTED_VERSION
        or result.get("client_size") != EXPECTED_SIZE
        or result.get("client_sha256") != EXPECTED_SHA
        or result.get("candidate_count") != 1
        or result.get("inventory_complete") is not True
        or result.get("display") != TARGET_DISPLAY
    ):
        raise PhysicalError("canonical_probe_exact_current_failed")
    return result


def _read_registration() -> dict[str, Any]:
    try:
        st = REGISTRATION.lstat()
        if not stat.S_ISREG(st.st_mode) or REGISTRATION.is_symlink() or stat.S_IMODE(st.st_mode) != 0o600:
            raise PhysicalError("canonical_registration_unsafe")
        data = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    except PhysicalError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise PhysicalError("canonical_registration_unavailable") from exc
    required = {
        "proof_kind": PROOF_KIND,
        "client_version": EXPECTED_VERSION,
        "client_size": EXPECTED_SIZE,
        "client_sha256": EXPECTED_SHA,
        "display": TARGET_DISPLAY,
        "state": "UNKNOWN",
    }
    if not isinstance(data, dict) or any(data.get(key) != value for key, value in required.items()):
        raise PhysicalError("canonical_registration_not_fail_closed_current")
    if not str(data.get("runtime_locator", "")).startswith(f"docker:{TARGET_CONTAINER}:"):
        raise PhysicalError("canonical_registration_namespace_mismatch")
    if not isinstance(data.get("pid"), int) or not isinstance(data.get("process_start_ticks"), int):
        raise PhysicalError("canonical_registration_identity_invalid")
    return data


def _require_manifest_matches_registration(manifest: dict[str, Any], registration: dict[str, Any]) -> None:
    for key in (
        "boot_id_sha256", "pid", "process_start_ticks", "client_version", "client_size",
        "client_sha256", "display", "runtime_locator", "candidate_fingerprint",
    ):
        if manifest.get(key) != registration.get(key):
            raise PhysicalError(f"canonical_identity_mismatch:{key}")


def _container_id() -> str:
    output = _require_success(["docker", "ps", "--no-trunc", "--format", "{{.ID}}\t{{.Names}}"])
    rows = []
    for line in output.splitlines():
        parts = line.split("\t", 1)
        if len(parts) == 2 and parts[1] == TARGET_CONTAINER:
            rows.append(parts[0].lower())
    if len(rows) != 1 or len(rows[0]) != 64 or any(ch not in "0123456789abcdef" for ch in rows[0]):
        raise PhysicalError("target_container_identity_invalid")
    return rows[0]


def _container_init_pid() -> int:
    output = _require_success(["docker", "inspect", "-f", "{{.State.Pid}}", TARGET_CONTAINER]).strip()
    if not output.isdigit() or int(output) < 2:
        raise PhysicalError("target_container_init_pid_invalid")
    return int(output)


def _numeric_user() -> tuple[int, int]:
    uid = _require_success(["docker", "exec", TARGET_CONTAINER, "id", "-u", TARGET_USER]).strip()
    gid = _require_success(["docker", "exec", TARGET_CONTAINER, "id", "-g", TARGET_USER]).strip()
    if not uid.isdigit() or not gid.isdigit() or int(uid) < 1 or int(gid) < 1:
        raise PhysicalError("target_numeric_user_invalid")
    return int(uid), int(gid)


def same_numeric_uid(pid: int, expected_uid: int) -> bool:
    output = _require_success([
        "docker", "exec", TARGET_CONTAINER, "sh", "-lc",
        f"awk '/^Uid:/' /proc/{pid}/status | awk '{{print $2}}'",
    ]).strip()
    return output.isdigit() and int(output) == expected_uid


def _vault_precheck(vault_dir: Path) -> None:
    try:
        root = vault_dir.resolve(strict=True)
        st = root.lstat()
    except OSError as exc:
        raise PhysicalError("vault_bind_missing") from exc
    if not stat.S_ISDIR(st.st_mode) or stat.S_IMODE(st.st_mode) != 0o700:
        raise PhysicalError("vault_bind_unsafe")
    for name in ("tibia-test-credentials.key", "tibia-test-credentials.crt", "tibia-test-credentials.cms"):
        path = root / name
        try:
            item = path.lstat()
        except OSError as exc:
            raise PhysicalError("vault_bind_component_missing") from exc
        if not stat.S_ISREG(item.st_mode) or path.is_symlink() or stat.S_IMODE(item.st_mode) != 0o600:
            raise PhysicalError("vault_bind_component_unsafe")


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb", buffering=0) as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _verify_bundle(bundle: Path) -> dict[str, str]:
    try:
        doc = json.loads((bundle / BUNDLE_MANIFEST).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PhysicalError("helper_bundle_manifest_invalid") from exc
    files = doc.get("files") if isinstance(doc, dict) else None
    if not isinstance(doc, dict) or doc.get("schema") != "otclient.track-a.native-login-helper-bundle.v1" or not isinstance(files, dict):
        raise PhysicalError("helper_bundle_manifest_invalid")
    if set(files) != set(BUNDLE_FILES):
        raise PhysicalError("helper_bundle_file_set_invalid")
    verified: dict[str, str] = {}
    for name, expected in files.items():
        path = bundle / name
        if not path.is_file() or path.is_symlink():
            raise PhysicalError("helper_bundle_file_invalid")
        actual = _sha(path)
        if actual != expected:
            raise PhysicalError("helper_bundle_digest_mismatch")
        verified[name] = actual
    profile = json.loads((bundle / "tibia-15.32.be4f48.json").read_text(encoding="utf-8"))
    if profile.get("binary_sha256") != EXPECTED_SHA or profile.get("client_version") != EXPECTED_VERSION:
        raise PhysicalError("helper_bundle_profile_fence_invalid")
    return verified


def _nsenter_precheck() -> tuple[int, int, int]:
    if os.geteuid() != 0:
        raise PhysicalError("nsenter_requires_root_runner")
    nsenter = shutil.which("nsenter")
    if not nsenter:
        raise PhysicalError("nsenter_unavailable")
    init_pid = _container_init_pid()
    if not Path(f"/proc/{init_pid}/ns/mnt").exists() or not Path(f"/proc/{init_pid}/root").exists():
        raise PhysicalError("target_host_pid_namespace_not_visible")
    uid, gid = _numeric_user()
    completed = _run([
        nsenter, "--target", str(init_pid), "--mount", "--pid", "--root", "--wd=/", "--",
        "python3", "-c", "import os; assert os.geteuid()==0",
    ], timeout=10)
    if completed.returncode != 0:
        raise PhysicalError("nsenter_target_namespace_unavailable")
    return init_pid, uid, gid


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_CLOEXEC, 0o600)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def precheck(vault_dir: Path, bundle: Path, result: Path) -> None:
    _vault_precheck(vault_dir)
    _verify_bundle(bundle)
    registration = _read_registration()
    manifest = _current_manifest()
    _require_manifest_matches_registration(manifest, registration)
    init_pid, uid, gid = _nsenter_precheck()
    if not same_numeric_uid(int(manifest["pid"]), uid):
        raise PhysicalError("same_numeric_uid_failed")
    _write_json(result, {
        "schema": "otclient.track-a.native-login-physical-precheck.v1",
        "exact_current": True,
        "target_unique": True,
        "registration_current": True,
        "nsenter_fd_bridge_ready": True,
        "same_numeric_uid": True,
        "vault_bind": "HOST_ONLY_PRESENT_PRIVATE",
        "credential_plaintext_accessed": False,
        "container_init_pid_visible": init_pid >= 2,
        "target_uid": uid,
        "target_gid": gid,
    })


def _install_bundle(bundle: Path) -> None:
    _verify_bundle(bundle)
    _require_success([
        "docker", "exec", TARGET_CONTAINER, "sh", "-lc",
        f"umask 077; install -d -m 700 {TASK_ROOT}; "
        f"rm -f {BRIDGE_SOCKET} {AUTH_SOCKET} {CHARACTER_SOCKET} "
        f"{BRIDGE_SO} {AUTH_SO} {CHARACTER_SO} {CONTAINER_CLIENT} {PROFILE}",
    ])
    for name in BUNDLE_FILES:
        completed = _run(["docker", "cp", str(bundle / name), f"{TARGET_CONTAINER}:{TASK_ROOT}/{name}"], timeout=30)
        if completed.returncode != 0:
            raise PhysicalError("helper_bundle_copy_failed")
    _require_success([
        "docker", "exec", TARGET_CONTAINER, "sh", "-lc",
        f"chown {TARGET_USER}:{TARGET_USER} {TASK_ROOT}/*; chmod 600 {TASK_ROOT}/*",
    ])
    manifest = json.loads((bundle / BUNDLE_MANIFEST).read_text(encoding="utf-8"))["files"]
    for name, expected in manifest.items():
        actual = _require_success(["docker", "exec", TARGET_CONTAINER, "sha256sum", f"{TASK_ROOT}/{name}"]).split()[0]
        if actual != expected:
            raise PhysicalError("installed_helper_digest_mismatch")


def _profile_targets() -> str:
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    if profile.get("binary_sha256") != EXPECTED_SHA:
        raise PhysicalError("local_profile_fence_invalid")
    targets = profile.get("targets")
    if not isinstance(targets, dict):
        raise PhysicalError("local_profile_targets_invalid")
    values: list[str] = []
    for name in sorted(targets):
        target = targets[name]
        values.append(f"{name},{int(target['vptr_offset'], 16):x},{target['expected_qt_class']}")
    return ";".join(values)


def _wait_pid_gone(pid: int, seconds: float = 15.0) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if _run(["docker", "exec", TARGET_CONTAINER, "test", "!", "-e", f"/proc/{pid}"]).returncode == 0:
            return
        time.sleep(0.25)
    raise PhysicalError("registered_pid_did_not_exit_after_SIGTERM")


def _wait_replacement(old_pid: int, old_start: int, seconds: float = 60.0) -> dict[str, Any]:
    deadline = time.monotonic() + seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            manifest = _current_manifest()
            if manifest["pid"] != old_pid and manifest["process_start_ticks"] != old_start:
                for socket_path in (BRIDGE_SOCKET, AUTH_SOCKET, CHARACTER_SOCKET):
                    if _run(["docker", "exec", "-u", TARGET_USER, TARGET_CONTAINER, "test", "-S", socket_path]).returncode != 0:
                        raise PhysicalError("replacement_helper_socket_missing")
                return manifest
        except Exception as exc:
            last_error = exc
        time.sleep(0.5)
    raise PhysicalError("replacement_exact_current_runtime_not_ready") from last_error


def replace(vault_dir: Path, bundle: Path, result: Path) -> None:
    _vault_precheck(vault_dir)
    _verify_bundle(bundle)
    registration = _read_registration()
    manifest = _current_manifest()
    _require_manifest_matches_registration(manifest, registration)
    uid, _gid = _numeric_user()
    if not same_numeric_uid(int(registration["pid"]), uid):
        raise PhysicalError("same_numeric_uid_failed")
    _install_bundle(bundle)
    pid = int(registration["pid"])
    start = int(registration["process_start_ticks"])
    if _run(["docker", "exec", TARGET_CONTAINER, "kill", "-TERM", str(pid)]).returncode != 0:
        raise PhysicalError("exact_registered_SIGTERM_failed")
    _wait_pid_gone(pid)
    candidates = _run([
        "docker", "exec", TARGET_CONTAINER, "sh", "-lc",
        "for d in /proc/[0-9]*; do [ -r \"$d/exe\" ] || continue; "
        f"[ \"$(stat -Lc %s \"$d/exe\" 2>/dev/null || echo x)\" = \"{EXPECTED_SIZE}\" ] || continue; "
        f"[ \"$(sha256sum \"$d/exe\" 2>/dev/null | awk '{{print $1}}')\" = \"{EXPECTED_SHA}\" ] && echo ${{d#/proc/}}; done",
    ])
    if candidates.returncode != 0 or candidates.stdout.strip():
        raise PhysicalError("post_SIGTERM_exact_client_still_present")
    legacy_email, legacy_password = _legacy_credential_env_names()
    env_args = [
        "-e", "HOME=/home/kasm-user",
        "-e", f"DISPLAY={TARGET_DISPLAY}",
        "-e", f"LD_PRELOAD={BRIDGE_SO}:{AUTH_SO}:{CHARACTER_SO}",
        "-e", f"OTCLIENT_TIBIA_RE_SOCKET={BRIDGE_SOCKET}",
        "-e", f"OTCLIENT_TIBIA_RE_AUTH_SOCKET={AUTH_SOCKET}",
        "-e", f"OTCLIENT_TIBIA_RE_CHARACTER_SOCKET={CHARACTER_SOCKET}",
        "-e", f"OTCLIENT_TIBIA_RE_BINARY_SHA256={EXPECTED_SHA}",
        "-e", f"OTCLIENT_TIBIA_RE_CLIENT_VERSION={EXPECTED_VERSION}",
        "-e", f"OTCLIENT_TIBIA_RE_TARGETS={_profile_targets()}",
    ]
    launch = _run([
        "docker", "exec", "-d", "-u", "kasm-user", "-w", PACKAGE_DIR, *env_args,
        TARGET_CONTAINER, "/usr/bin/env", "-u", "RUNNER_TRACKING_ID", "-u", legacy_email,
        "-u", legacy_password, "-u", "TRACK_A_CANONICAL_LEASE_TOKEN",
        "-u", "TRACK_A_CANONICAL_LEASE_TOKEN_FILE", CLIENT_PATH,
    ], timeout=20)
    if launch.returncode != 0:
        raise PhysicalError("replacement_launch_failed")
    replacement = _wait_replacement(pid, start)
    _write_json(result, {
        "schema": "otclient.track-a.native-login-replacement.v1",
        "exact_current": True,
        "old_pid_replaced": True,
        "pid": replacement["pid"],
        "process_start_ticks": replacement["process_start_ticks"],
        "boot_id_sha256": replacement["boot_id_sha256"],
        "candidate_fingerprint": replacement["candidate_fingerprint"],
        "helpers_ready": True,
        "credential_plaintext_accessed": False,
    })


def _namespace_client_command(
    *,
    init_pid: int,
    uid: int,
    gid: int,
    operation: str,
    identity: dict[str, Any],
    credentials_fd: int | None = None,
    timeout: float = 8.0,
) -> list[str]:
    command = [
        shutil.which("nsenter") or "nsenter", "--target", str(init_pid), "--mount", "--pid", "--root", "--wd=/", "--",
        "python3", CONTAINER_CLIENT, operation,
        "--socket", AUTH_SOCKET if operation == "auth-fd" else CHARACTER_SOCKET,
        "--boot-id-sha256", str(identity["boot_id_sha256"]),
        "--pid", str(identity["pid"]),
        "--start-ticks", str(identity["process_start_ticks"]),
        "--client-version", EXPECTED_VERSION,
        "--client-size", str(EXPECTED_SIZE),
        "--client-sha256", EXPECTED_SHA,
        "--timeout", str(timeout),
    ]
    if operation == "auth-fd":
        if credentials_fd is None:
            raise PhysicalError("credentials_fd_missing")
        command.extend(["--credentials-fd", str(credentials_fd), "--drop-uid", str(uid), "--drop-gid", str(gid)])
    return command


def auth_one_shot(vault_dir: Path, result: Path) -> None:
    _vault_precheck(vault_dir)
    registration = _read_registration()
    manifest = _current_manifest()
    _require_manifest_matches_registration(manifest, registration)
    init_pid, uid, gid = _nsenter_precheck()
    if not same_numeric_uid(int(registration["pid"]), uid):
        raise PhysicalError("same_numeric_uid_failed")
    credentials_fd = -1
    try:
        credentials_fd = decrypt_to_sealed_memfd(vault_dir)
        auth_completed = _run(
            _namespace_client_command(
                init_pid=init_pid,
                uid=uid,
                gid=gid,
                operation="auth-fd",
                identity=registration,
                credentials_fd=credentials_fd,
                timeout=8.0,
            ),
            timeout=15,
            pass_fds=(credentials_fd,),
        )
    except SecretVaultError as exc:
        raise PhysicalError("machine_local_vault_decrypt_failed") from exc
    finally:
        if credentials_fd >= 0:
            try:
                os.close(credentials_fd)
            except OSError:
                pass

    response: dict[str, Any] = {}
    if auth_completed.stdout.strip():
        try:
            candidate = json.loads(auth_completed.stdout.strip().splitlines()[-1])
            if isinstance(candidate, dict):
                response = candidate
        except json.JSONDecodeError:
            response = {}
    if auth_completed.returncode == 0:
        if response.get("ok") is not True or response.get("invocation_dispatched") is not True:
            raise PhysicalError("native_auth_response_not_dispatch_proof")
        outcome = "PASS_RESPONSE"
    else:
        sent_without_response = bool(
            response.get("fd_sent") is True
            and response.get("error") == "AUTH_RESPONSE_UNAVAILABLE_AFTER_SEND"
        )
        if not sent_without_response:
            raise PhysicalError("native_auth_fd_send_not_proven")
        deadline = time.monotonic() + 15.0
        handoff: dict[str, Any] | None = None
        while time.monotonic() < deadline:
            try:
                candidate = _current_manifest()
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

    _write_json(result, {
        "schema": "otclient.track-a.native-login-auth.v1",
        "native_auth_ingress": outcome,
        "secret_source": "machine_local_encrypted_vault",
        "sealed_memfd": True,
        "scm_rights": True,
        "secret_attempt_count": 1,
        "NO_SECOND_SECRET_ATTEMPT": True,
        "credential_values_logged": False,
    })


def _character_call(identity: dict[str, Any], operation: str, timeout: float = 8.0) -> dict[str, Any]:
    uid, gid = _numeric_user()
    init_pid = _container_init_pid()
    completed = _run(
        _namespace_client_command(
            init_pid=init_pid,
            uid=uid,
            gid=gid,
            operation=operation,
            identity=identity,
            timeout=timeout,
        ),
        timeout=int(timeout) + 5,
    )
    if completed.returncode != 0 or not completed.stdout.strip():
        raise PhysicalError(f"character_{operation}_failed")
    try:
        result = json.loads(completed.stdout.strip().splitlines()[-1])
    except json.JSONDecodeError as exc:
        raise PhysicalError("character_response_invalid") from exc
    if not isinstance(result, dict) or result.get("ok") is not True:
        raise PhysicalError("character_response_not_ok")
    return result


def confirm_unique(result: Path) -> None:
    registration = _read_registration()
    manifest = _current_manifest()
    _require_manifest_matches_registration(manifest, registration)
    deadline = time.monotonic() + 90.0
    state: dict[str, Any] | None = None
    while time.monotonic() < deadline:
        try:
            state = _character_call(registration, "character-state", timeout=5.0)
        except PhysicalError:
            state = None
        if state is not None and state.get("character_count") == 1 and state.get("confirm_method_present") is True:
            break
        time.sleep(0.5)
    if state is None or state.get("character_count") != 1 or state.get("confirm_method_present") is not True:
        raise PhysicalError("native_character_count_not_exactly_one")
    confirmed = _character_call(registration, "confirm-unique", timeout=8.0)
    if confirmed.get("confirmation_dispatched") is not True or confirmed.get("character_index") != 0:
        raise PhysicalError("native_character_confirmation_not_proven")
    _write_json(result, {
        "schema": "otclient.track-a.native-login-character-confirm.v1",
        "character_count": 1,
        "confirm_method_present": True,
        "CONFIRM_UNIQUE": True,
        "confirmation_dispatched": True,
        "character_index": 0,
    })


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    pre = sub.add_parser("precheck")
    pre.add_argument("--vault-dir", required=True, type=Path)
    pre.add_argument("--bundle", required=True, type=Path)
    pre.add_argument("--result", required=True, type=Path)
    replacement = sub.add_parser("replace")
    replacement.add_argument("--vault-dir", required=True, type=Path)
    replacement.add_argument("--bundle", required=True, type=Path)
    replacement.add_argument("--result", required=True, type=Path)
    auth = sub.add_parser("auth-one-shot")
    auth.add_argument("--vault-dir", required=True, type=Path)
    auth.add_argument("--result", required=True, type=Path)
    confirm = sub.add_parser("confirm-unique")
    confirm.add_argument("--result", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.operation == "precheck":
            precheck(args.vault_dir, args.bundle, args.result)
        elif args.operation == "replace":
            replace(args.vault_dir, args.bundle, args.result)
        elif args.operation == "auth-one-shot":
            auth_one_shot(args.vault_dir, args.result)
        else:
            confirm_unique(args.result)
        print(f"TRACK_A_BE4F48_PHYSICAL_{args.operation.upper().replace('-', '_')}=PASS")
        if args.operation == "auth-one-shot":
            print("NO_SECOND_SECRET_ATTEMPT=true")
        return 0
    except (PhysicalError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"TRACK_A_BE4F48_PHYSICAL_ERROR={getattr(exc, 'args', ['physical_failure'])[0]}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
