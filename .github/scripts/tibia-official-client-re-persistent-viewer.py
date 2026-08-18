#!/usr/bin/env python3
"""Persistent noVNC presentation for the Track A canonical live runtime.

The viewer is a separate programme resource. It binds to immutable runtime
identity, not to a disposable controller session or lease generation.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import re
import secrets
import shutil
import signal
import socket
import stat
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Sequence

CANONICAL_STATE = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
REGISTRATION = CANONICAL_STATE / "runtime-registration.json"
VIEWER_STATE = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-viewer")
LEASE_PATH = Path(__file__).with_name("tibia-official-client-re-canonical-live-lease.py")
XRES_OWNER = Path(__file__).with_name("tibia-official-client-re-xres-window-owner.py")
XRES_WIRE = Path(__file__).with_name("tibia-official-client-re-xres-wire.py")
DEFAULT_RFB_PORT = 5901
DEFAULT_BACKEND_PORT = 6081
DEFAULT_PUBLIC_URL = "http://synology:6082/"
IDENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}$")
VIEWER_MARK = "OTCLIENT_TIBIA_RE_PERSISTENT_VIEWER=1"
TRACK_MARK = "OTCLIENT_TIBIA_RE_TRACK=official-client-re"


class ViewerError(RuntimeError):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


def _contract_override(path: Path, expected: Path, code: str) -> Path:
    if path != expected and os.environ.get("TRACK_A_PERSISTENT_VIEWER_CONTRACT_TEST") != "1":
        raise ViewerError(code)
    return path


def _load_lease():
    spec = importlib.util.spec_from_file_location("track_a_viewer_lease", LEASE_PATH)
    if spec is None or spec.loader is None:
        raise ViewerError("lease_module_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _identity(value: str, field: str) -> str:
    if not IDENT_RE.fullmatch(value):
        raise ViewerError("invalid_identity", f"invalid {field}")
    return value


def _safe_json(path: Path, *, required_mode: int = 0o600) -> dict[str, Any]:
    try:
        st = path.lstat()
    except FileNotFoundError as exc:
        raise ViewerError("state_missing") from exc
    if not stat.S_ISREG(st.st_mode) or path.is_symlink():
        raise ViewerError("state_file_unsafe")
    if stat.S_IMODE(st.st_mode) != required_mode:
        raise ViewerError("state_file_permissions")
    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        raise ViewerError("state_file_owner")
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ViewerError("state_invalid_json") from exc
    if not isinstance(data, dict):
        raise ViewerError("state_invalid_shape")
    return data


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    import tempfile

    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    payload = json.dumps(data, sort_keys=True, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        os.chmod(path, 0o600)
        dir_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        tmp.unlink(missing_ok=True)


def _boot_hash() -> str:
    raw = Path("/proc/sys/kernel/random/boot_id").read_text().strip().encode()
    return hashlib.sha256(raw).hexdigest()


def _proc_start(pid: int) -> int:
    try:
        raw = Path(f"/proc/{pid}/stat").read_text()
    except FileNotFoundError as exc:
        raise ViewerError("runtime_process_missing") from exc
    close = raw.rfind(")")
    fields = raw[close + 2 :].split()
    if close < 0 or len(fields) < 20:
        raise ViewerError("runtime_proc_stat_invalid")
    return int(fields[19])


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb", buffering=0) as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _runtime_binding(registration: dict[str, Any]) -> dict[str, Any]:
    required = (
        "runtime_id",
        "boot_id_sha256",
        "pid",
        "process_start_ticks",
        "client_size",
        "client_sha256",
        "display",
        "window_identity",
    )
    if any(key not in registration for key in required):
        raise ViewerError("registration_schema_invalid")
    pid = registration["pid"]
    if not isinstance(pid, int) or pid < 2:
        raise ViewerError("registration_pid_invalid")
    display = registration["display"]
    window = registration["window_identity"]
    if not isinstance(display, str) or not display.startswith(":"):
        raise ViewerError("registration_display_invalid")
    if not isinstance(window, str) or not re.fullmatch(r"x11-window:[1-9][0-9]*", window):
        raise ViewerError("registration_window_invalid")
    try:
        exe = Path(os.readlink(f"/proc/{pid}/exe"))
        st = exe.stat()
    except OSError as exc:
        raise ViewerError("runtime_exe_unreadable") from exc
    current = {
        "runtime_id": registration["runtime_id"],
        "boot_id_sha256": _boot_hash(),
        "pid": pid,
        "process_start_ticks": _proc_start(pid),
        "client_size": st.st_size,
        "client_sha256": _sha(exe),
        "display": display,
        "window_identity": window,
    }
    for key in ("boot_id_sha256", "process_start_ticks", "client_size", "client_sha256"):
        if current[key] != registration[key]:
            raise ViewerError(f"runtime_binding_{key}_mismatch")
    return current


def _resolve_toolroot(explicit: Path | None) -> Path:
    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(explicit)
    session_hint = CANONICAL_STATE / "session" / "toolroot"
    if session_hint.is_file():
        try:
            candidates.append(Path(session_hint.read_text().strip()))
        except OSError:
            pass
    candidates += [
        Path("/home/runner/_work/_otclient_tibia_re_state/toolroot"),
        Path("/work/_otclient_tibia_re_state/toolroot"),
    ]
    for candidate in candidates:
        try:
            real = candidate.resolve(strict=True)
        except OSError:
            continue
        if real.is_dir():
            return real
    raise ViewerError("toolroot_unavailable")


def _resolve_window(binding: dict[str, Any], toolroot: Path) -> int:
    completed = subprocess.run(
        [
            sys.executable,
            str(XRES_OWNER),
            "--display",
            str(binding["display"]),
            "--pid",
            str(binding["pid"]),
            "--toolroot",
            str(toolroot),
            "--wire-helper",
            str(XRES_WIRE),
            "--attempts",
            "8",
            "--delay",
            "0.25",
        ],
        text=True,
        capture_output=True,
        close_fds=True,
        check=False,
    )
    if completed.returncode:
        raise ViewerError("runtime_xres_window_unresolved")
    try:
        xid = int(completed.stdout.strip())
    except ValueError as exc:
        raise ViewerError("runtime_xres_window_invalid") from exc
    expected = int(str(binding["window_identity"]).split(":", 1)[1])
    if xid != expected:
        raise ViewerError("runtime_xres_window_mismatch")
    return xid


def _sanitized_env(extra: dict[str, str]) -> dict[str, str]:
    env = dict(os.environ)
    for key in list(env):
        upper = key.upper()
        if (
            upper.startswith("TIBIA_TEST_")
            or "LEASE_TOKEN" in upper
            or "CAPABILITY" in upper
            or key == "RUNNER_TRACKING_ID"
        ):
            env.pop(key, None)
    env.update(extra)
    return env


def _owned_process(pid: int, instance: str, role: str) -> bool:
    try:
        raw = Path(f"/proc/{pid}/environ").read_bytes().split(b"\0")
    except OSError:
        return False
    values = {item.decode("utf-8", errors="replace") for item in raw if item}
    return {
        TRACK_MARK,
        VIEWER_MARK,
        f"OTCLIENT_TIBIA_RE_VIEWER_INSTANCE={instance}",
        f"OTCLIENT_TIBIA_RE_VIEWER_ROLE={role}",
    }.issubset(values)


def _stop_owned(pid: int, instance: str, role: str) -> None:
    if pid < 2 or not _owned_process(pid, instance, role):
        raise ViewerError(f"viewer_{role}_ownership_failed")
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + 3
    while time.monotonic() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(0.1)
    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def _port_open(host: str, port: int, timeout: float = 0.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _wait_port(host: str, port: int, process: subprocess.Popen[Any], seconds: float = 8.0) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise ViewerError("viewer_process_exited")
        if _port_open(host, port):
            return
        time.sleep(0.1)
    raise ViewerError("viewer_listener_timeout")


def _rfb_banner(port: int) -> None:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=2) as conn:
            banner = conn.recv(12)
    except OSError as exc:
        raise ViewerError("viewer_rfb_unreachable") from exc
    if not banner.startswith(b"RFB "):
        raise ViewerError("viewer_rfb_banner_invalid")


def _http_json(url: str, instance: str) -> dict[str, Any]:
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query.append(("instance", instance))
    target = urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, parsed.path, urllib.parse.urlencode(query), parsed.fragment)
    )
    request = urllib.request.Request(
        target,
        headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            payload = response.read(64 * 1024)
    except (OSError, urllib.error.URLError) as exc:
        raise ViewerError("viewer_http_unreachable") from exc
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ViewerError("viewer_identity_invalid_json") from exc
    if not isinstance(data, dict):
        raise ViewerError("viewer_identity_invalid_shape")
    return data


def _websocket_upgrade(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "http" or not parsed.hostname:
        raise ViewerError("viewer_public_url_invalid")
    port = parsed.port or 80
    key = base64.b64encode(secrets.token_bytes(16)).decode()
    request = (
        f"GET /websockify HTTP/1.1\r\n"
        f"Host: {parsed.hostname}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    ).encode()
    try:
        with socket.create_connection((parsed.hostname, port), timeout=3) as conn:
            conn.sendall(request)
            response = conn.recv(4096)
    except OSError as exc:
        raise ViewerError("viewer_websocket_unreachable") from exc
    first = response.split(b"\r\n", 1)[0]
    if b" 101 " not in first:
        raise ViewerError("viewer_websocket_upgrade_failed")


def _viewer_identity(binding: dict[str, Any], instance: str, backend_port: int) -> dict[str, Any]:
    # Deliberately excludes controller session, lease generation and registration
    # generation. Viewer continuity is tied only to immutable runtime identity.
    return {
        "schema_version": 1,
        "viewer_instance_id": instance,
        "runtime_id": binding["runtime_id"],
        "boot_id_sha256": binding["boot_id_sha256"],
        "pid": binding["pid"],
        "process_start_ticks": binding["process_start_ticks"],
        "client_size": binding["client_size"],
        "client_sha256": binding["client_sha256"],
        "display": binding["display"],
        "window_identity": binding["window_identity"],
        "backend_port": backend_port,
    }


def _health(
    *,
    registration_path: Path,
    state_dir: Path,
    toolroot: Path | None,
    public_url: str | None = None,
) -> dict[str, Any]:
    registration = _safe_json(registration_path)
    binding = _runtime_binding(registration)
    resolved_toolroot = _resolve_toolroot(toolroot)
    _resolve_window(binding, resolved_toolroot)
    runtime_health = "PASS"

    try:
        state = _safe_json(state_dir / "viewer.json")
        instance = str(state["viewer_instance_id"])
        rfb_port = int(state["rfb_port"])
        backend_port = int(state["backend_port"])
        public = str(public_url or state["public_url"])
        expected = _viewer_identity(binding, instance, backend_port)
        if state.get("runtime_binding") != binding:
            raise ViewerError("viewer_runtime_binding_changed")
        x11vnc_pid = int(state["x11vnc_pid"])
        websockify_pid = int(state["websockify_pid"])
        if not _owned_process(x11vnc_pid, instance, "x11vnc"):
            raise ViewerError("viewer_x11vnc_not_owned")
        if not _owned_process(websockify_pid, instance, "websockify"):
            raise ViewerError("viewer_websockify_not_owned")
        _rfb_banner(rfb_port)
        local = _http_json(f"http://127.0.0.1:{backend_port}/viewer-identity.json", instance)
        if local != expected:
            raise ViewerError("viewer_local_identity_mismatch")
        _websocket_upgrade(f"http://127.0.0.1:{backend_port}/")
        remote = _http_json(
            urllib.parse.urljoin(public.rstrip("/") + "/", "viewer-identity.json"),
            instance,
        )
        if remote != expected:
            raise ViewerError("viewer_public_identity_mismatch")
        _websocket_upgrade(public)
        viewer_health = "PASS"
        reason = "none"
    except ViewerError as exc:
        viewer_health = f"FAIL_{exc.code.upper()}"
        reason = exc.code
        public = str(public_url or DEFAULT_PUBLIC_URL)

    return {
        "runtime_health": runtime_health,
        "viewer_health": viewer_health,
        "viewer_url": public,
        "viewer_reason": reason,
        "runtime_binding": binding,
    }


def _prepare_webroot(
    state_dir: Path,
    novnc_root: Path,
    binding: dict[str, Any],
    instance: str,
    backend_port: int,
) -> tuple[Path, dict[str, Any]]:
    if not novnc_root.is_dir():
        raise ViewerError("novnc_root_missing")
    webroot = state_dir / "web"
    shutil.rmtree(webroot, ignore_errors=True)
    shutil.copytree(novnc_root, webroot, symlinks=False)
    identity = _viewer_identity(binding, instance, backend_port)
    (webroot / "viewer-identity.json").write_text(json.dumps(identity, sort_keys=True) + "\n")
    (webroot / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>Track A Tibia viewer</title>'
        "<script>location.replace('/vnc.html?autoconnect=1&resize=scale&quality=6"
        "&compression=3&show_dot=true&path=websockify');</script>\n"
    )
    return webroot, identity


def _validated_authority(lease: Any, task_id: str, session_id: str, token_file: Path):
    manager = lease.LeaseManager(CANONICAL_STATE)
    token = lease._read_private_token(token_file)
    manager._prepare()
    return manager, token, lease.LeaseIdentity(task_id, session_id)


def start(args: argparse.Namespace) -> int:
    lease = _load_lease()
    task_id = _identity(args.task_id, "task-id")
    session_id = _identity(args.session_id, "session-id")
    state_dir = _contract_override(args.state_dir, VIEWER_STATE, "noncanonical_viewer_state_override")
    registration_path = _contract_override(
        args.registration, REGISTRATION, "noncanonical_registration_override"
    )
    toolroot = _resolve_toolroot(args.toolroot)
    x11vnc = args.x11vnc or (toolroot / "usr/bin/x11vnc")
    websockify = args.websockify or Path(shutil.which("websockify") or "")
    if not x11vnc.is_file() or not os.access(x11vnc, os.X_OK):
        raise ViewerError("x11vnc_unavailable")
    if not websockify.is_file() or not os.access(websockify, os.X_OK):
        raise ViewerError("websockify_unavailable")
    manager, token, identity = _validated_authority(lease, task_id, session_id, args.token_file)
    state_file = state_dir / "viewer.json"
    state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(state_dir, 0o700)

    with manager.locked():
        lease_state = manager._load_state_unlocked()
        manager._require_current_unlocked(lease_state, identity, token, lease._now_epoch(None))
        registration = _safe_json(registration_path)
        binding = _runtime_binding(registration)
        _resolve_window(binding, toolroot)

        if state_file.exists():
            existing = _safe_json(state_file)
            if existing.get("runtime_binding") == binding:
                current = _health(
                    registration_path=registration_path,
                    state_dir=state_dir,
                    toolroot=toolroot,
                    public_url=args.public_url,
                )
                if current["viewer_health"] == "PASS":
                    print("TRACK_A_RUNTIME_HEALTH=PASS")
                    print("TRACK_A_VIEWER_HEALTH=PASS")
                    print(f"TRACK_A_VIEWER_URL={current['viewer_url']}")
                    print("TRACK_A_VIEWER_START=IDEMPOTENT")
                    return 0
            instance = str(existing.get("viewer_instance_id") or "")
            for role, key in (("websockify", "websockify_pid"), ("x11vnc", "x11vnc_pid")):
                pid = int(existing.get(key) or 0)
                if pid >= 2 and Path(f"/proc/{pid}").exists():
                    _stop_owned(pid, instance, role)
            state_file.unlink(missing_ok=True)

        if _port_open("127.0.0.1", args.rfb_port):
            raise ViewerError("viewer_rfb_port_in_use")
        if _port_open("127.0.0.1", args.backend_port):
            raise ViewerError("viewer_backend_port_in_use")

        instance = secrets.token_hex(16)
        webroot, expected = _prepare_webroot(
            state_dir, args.novnc_root, binding, instance, args.backend_port
        )
        state = {
            "schema_version": 1,
            "viewer_instance_id": instance,
            "status": "starting",
            "runtime_binding": binding,
            "rfb_port": args.rfb_port,
            "backend_port": args.backend_port,
            "public_url": args.public_url,
            "x11vnc_pid": None,
            "websockify_pid": None,
            "started_at": int(time.time()),
            "source_task": task_id,
        }
        _atomic_json(state_file, state)

        common = {
            TRACK_MARK.split("=", 1)[0]: TRACK_MARK.split("=", 1)[1],
            VIEWER_MARK.split("=", 1)[0]: VIEWER_MARK.split("=", 1)[1],
            "OTCLIENT_TIBIA_RE_VIEWER_INSTANCE": instance,
            "OTCLIENT_TIBIA_RE_VIEWER_RUNTIME_PID": str(binding["pid"]),
        }
        log_dir = state_dir / "logs"
        log_dir.mkdir(mode=0o700, exist_ok=True)
        xlog = (log_dir / "x11vnc.log").open("ab", buffering=0)
        wlog = (log_dir / "websockify.log").open("ab", buffering=0)
        xproc: subprocess.Popen[Any] | None = None
        wproc: subprocess.Popen[Any] | None = None
        keep = False
        try:
            xenv = _sanitized_env(
                common
                | {
                    "DISPLAY": str(binding["display"]),
                    "OTCLIENT_TIBIA_RE_VIEWER_ROLE": "x11vnc",
                }
            )
            xproc = subprocess.Popen(
                [
                    str(x11vnc),
                    "-display",
                    str(binding["display"]),
                    "-rfbport",
                    str(args.rfb_port),
                    "-localhost",
                    "-forever",
                    "-shared",
                    "-viewonly",
                    "-nopw",
                    "-noxdamage",
                ],
                stdin=subprocess.DEVNULL,
                stdout=xlog,
                stderr=subprocess.STDOUT,
                env=xenv,
                close_fds=True,
                start_new_session=True,
            )
            state["x11vnc_pid"] = xproc.pid
            _atomic_json(state_file, state)
            _wait_port("127.0.0.1", args.rfb_port, xproc)
            _rfb_banner(args.rfb_port)

            wenv = _sanitized_env(
                common | {"OTCLIENT_TIBIA_RE_VIEWER_ROLE": "websockify"}
            )
            wproc = subprocess.Popen(
                [
                    str(websockify),
                    "--web",
                    str(webroot),
                    f"0.0.0.0:{args.backend_port}",
                    f"127.0.0.1:{args.rfb_port}",
                ],
                stdin=subprocess.DEVNULL,
                stdout=wlog,
                stderr=subprocess.STDOUT,
                env=wenv,
                close_fds=True,
                start_new_session=True,
            )
            state["websockify_pid"] = wproc.pid
            _atomic_json(state_file, state)
            _wait_port("127.0.0.1", args.backend_port, wproc)
            local = _http_json(
                f"http://127.0.0.1:{args.backend_port}/viewer-identity.json", instance
            )
            if local != expected:
                raise ViewerError("viewer_local_identity_mismatch")
            _websocket_upgrade(f"http://127.0.0.1:{args.backend_port}/")
            state["status"] = "local_ready"
            _atomic_json(state_file, state)
            keep = True
        finally:
            xlog.close()
            wlog.close()
            if not keep:
                for proc, role in ((wproc, "websockify"), (xproc, "x11vnc")):
                    if proc is not None and proc.poll() is None:
                        try:
                            _stop_owned(proc.pid, instance, role)
                        except ViewerError:
                            pass

        public_ok = False
        try:
            remote = _http_json(
                urllib.parse.urljoin(
                    args.public_url.rstrip("/") + "/", "viewer-identity.json"
                ),
                instance,
            )
            if remote != expected:
                raise ViewerError("viewer_public_identity_mismatch")
            _websocket_upgrade(args.public_url)
            public_ok = True
        except ViewerError:
            public_ok = False
        state["status"] = "ready_public" if public_ok else "local_ready"
        state["public_mapping"] = "PROVEN" if public_ok else "UNKNOWN"
        _atomic_json(state_file, state)

    print("TRACK_A_RUNTIME_HEALTH=PASS")
    if public_ok:
        print("TRACK_A_VIEWER_HEALTH=PASS")
        print(f"TRACK_A_VIEWER_URL={args.public_url}")
        print("TRACK_A_VIEWER_START=PASS")
        return 0
    print("TRACK_A_VIEWER_HEALTH=FAIL_PUBLIC_MAPPING")
    print(f"TRACK_A_VIEWER_URL={args.public_url}")
    print("TRACK_A_VIEWER_START=LOCAL_BACKEND_PERSISTED")
    return 3


def health(args: argparse.Namespace) -> int:
    state_dir = _contract_override(args.state_dir, VIEWER_STATE, "noncanonical_viewer_state_override")
    registration_path = _contract_override(
        args.registration, REGISTRATION, "noncanonical_registration_override"
    )
    try:
        result = _health(
            registration_path=registration_path,
            state_dir=state_dir,
            toolroot=args.toolroot,
            public_url=args.public_url,
        )
    except ViewerError as exc:
        print(f"TRACK_A_RUNTIME_HEALTH=FAIL_{exc.code.upper()}")
        print("TRACK_A_VIEWER_HEALTH=UNKNOWN")
        print(f"TRACK_A_VIEWER_URL={args.public_url or DEFAULT_PUBLIC_URL}")
        return 2
    print(f"TRACK_A_RUNTIME_HEALTH={result['runtime_health']}")
    print(f"TRACK_A_VIEWER_HEALTH={result['viewer_health']}")
    print(f"TRACK_A_VIEWER_URL={result['viewer_url']}")
    return 0 if result["viewer_health"] == "PASS" else 3


def stop(args: argparse.Namespace) -> int:
    lease = _load_lease()
    task_id = _identity(args.task_id, "task-id")
    session_id = _identity(args.session_id, "session-id")
    state_dir = _contract_override(args.state_dir, VIEWER_STATE, "noncanonical_viewer_state_override")
    manager, token, identity = _validated_authority(lease, task_id, session_id, args.token_file)
    with manager.locked():
        lease_state = manager._load_state_unlocked()
        manager._require_current_unlocked(lease_state, identity, token, lease._now_epoch(None))
        state = _safe_json(state_dir / "viewer.json")
        instance = str(state.get("viewer_instance_id") or "")
        for role, key in (("websockify", "websockify_pid"), ("x11vnc", "x11vnc_pid")):
            pid = int(state.get(key) or 0)
            if pid >= 2 and Path(f"/proc/{pid}").exists():
                _stop_owned(pid, instance, role)
        shutil.rmtree(state_dir, ignore_errors=True)
    print("TRACK_A_VIEWER_STOP=PASS")
    print("TRACK_A_CANONICAL_RUNTIME_PRESERVED=true")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="operation", required=True)

    start_p = sub.add_parser("start")
    start_p.add_argument("--task-id", required=True)
    start_p.add_argument("--session-id", required=True)
    start_p.add_argument("--token-file", required=True, type=Path)
    start_p.add_argument("--registration", type=Path, default=REGISTRATION)
    start_p.add_argument("--state-dir", type=Path, default=VIEWER_STATE)
    start_p.add_argument("--toolroot", type=Path)
    start_p.add_argument("--x11vnc", type=Path)
    start_p.add_argument("--websockify", type=Path)
    start_p.add_argument("--novnc-root", type=Path, default=Path("/usr/share/novnc"))
    start_p.add_argument("--rfb-port", type=int, default=DEFAULT_RFB_PORT)
    start_p.add_argument("--backend-port", type=int, default=DEFAULT_BACKEND_PORT)
    start_p.add_argument("--public-url", default=DEFAULT_PUBLIC_URL)

    health_p = sub.add_parser("health")
    health_p.add_argument("--registration", type=Path, default=REGISTRATION)
    health_p.add_argument("--state-dir", type=Path, default=VIEWER_STATE)
    health_p.add_argument("--toolroot", type=Path)
    health_p.add_argument("--public-url")

    stop_p = sub.add_parser("stop")
    stop_p.add_argument("--task-id", required=True)
    stop_p.add_argument("--session-id", required=True)
    stop_p.add_argument("--token-file", required=True, type=Path)
    stop_p.add_argument("--state-dir", type=Path, default=VIEWER_STATE)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return {"start": start, "health": health, "stop": stop}[args.operation](args)
    except Exception as exc:
        print(
            f"TRACK_A_PERSISTENT_VIEWER_ERROR={getattr(exc, 'code', 'viewer_failure')}",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
