#!/usr/bin/env python3
"""Fail-closed raw-XRes probe for an already registered Track A runtime.

This is the canonical reuse/Gate-B probe used after bootstrap. It replaces the
non-authoritative xdotool --pid window lookup with raw XRes LocalClientPid
ownership while retaining process-group, role, secret and listener checks.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import socket
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

BASE = Path("/home/runner/_work/_otclient_tibia_re_state")
STATE = BASE / "canonical-live-runtime"
SESSION = STATE / "session"
XRES_OWNER = Path(__file__).with_name("tibia-official-client-re-xres-window-owner.py")
XRES_WIRE = Path(__file__).with_name("tibia-official-client-re-xres-wire.py")
TRACK_MARK = "OTCLIENT_TIBIA_RE_TRACK=official-client-re"
RUNTIME_MARK = "OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1"
ROLE_MARK = "OTCLIENT_TIBIA_RE_ROLE="
SECRET_PREFIXES = (
    "TIBIA_TEST_",
    "TRACK_A_CANONICAL_LEASE_TOKEN",
    "TRACK_A_CANONICAL_LEASE_TOKEN_FILE",
)


class ProbeError(RuntimeError):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


def _safe_text(path: Path) -> str:
    try:
        st = path.lstat()
    except FileNotFoundError as exc:
        raise ProbeError("session_state_missing", str(path)) from exc
    if not stat.S_ISREG(st.st_mode) or path.is_symlink():
        raise ProbeError("session_state_unsafe", str(path))
    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        raise ProbeError("session_state_owner", str(path))
    try:
        return path.read_text().strip()
    except OSError as exc:
        raise ProbeError("session_state_unreadable", str(path)) from exc


def _positive_int(path: Path) -> int:
    raw = _safe_text(path)
    if not re.fullmatch(r"[1-9][0-9]*", raw):
        raise ProbeError("session_integer_invalid", str(path))
    return int(raw)


def _proc_fields(pid: int) -> list[str]:
    try:
        raw = Path(f"/proc/{pid}/stat").read_text()
    except FileNotFoundError as exc:
        raise ProbeError("tracked_process_missing", str(pid)) from exc
    close = raw.rfind(")")
    fields = raw[close + 2 :].split()
    if close < 0 or len(fields) < 20:
        raise ProbeError("proc_stat_invalid", str(pid))
    if fields[0] == "Z":
        raise ProbeError("tracked_process_zombie", str(pid))
    return fields


def _pgrp(pid: int) -> int:
    return int(_proc_fields(pid)[2])


def _proc_env(pid: int) -> set[str]:
    try:
        raw = Path(f"/proc/{pid}/environ").read_bytes().split(b"\0")
    except OSError as exc:
        raise ProbeError("tracked_environment_unreadable", str(pid)) from exc
    return {item.decode("utf-8", errors="replace") for item in raw if item}


def _proc_exe(pid: int) -> Path:
    try:
        return Path(os.readlink(f"/proc/{pid}/exe")).resolve(strict=True)
    except OSError as exc:
        raise ProbeError("tracked_executable_unreadable", str(pid)) from exc


def _require_role(pid: int, role: str, pgid: int, expected_exe: Path | None = None) -> None:
    if _pgrp(pid) != pgid:
        raise ProbeError("tracked_process_wrong_group", role)
    env = _proc_env(pid)
    required = {TRACK_MARK, RUNTIME_MARK, ROLE_MARK + role}
    if not required.issubset(env):
        raise ProbeError("tracked_process_ownership_failed", role)
    for item in env:
        key = item.split("=", 1)[0].upper()
        if any(key.startswith(prefix) for prefix in SECRET_PREFIXES) or "CAPABILITY" in key:
            raise ProbeError("tracked_process_secret_env_leak", role)
    if expected_exe is not None:
        try:
            expected = expected_exe.resolve(strict=True)
        except OSError as exc:
            raise ProbeError("expected_executable_unavailable", role) from exc
        if _proc_exe(pid) != expected:
            raise ProbeError("tracked_executable_mismatch", role)


def _listener_inodes(port: int) -> set[str]:
    wanted = f"{port:04X}"
    result: set[str] = set()
    for name in ("tcp", "tcp6"):
        path = Path("/proc/net") / name
        if not path.exists():
            continue
        try:
            rows = path.read_text().splitlines()[1:]
        except OSError as exc:
            raise ProbeError("listener_inventory_unreadable") from exc
        for row in rows:
            fields = row.split()
            if len(fields) < 10:
                continue
            if fields[1].rsplit(":", 1)[-1].upper() == wanted and fields[3] == "0A":
                result.add(fields[9])
    return result


def _process_socket_inodes(pid: int) -> set[str]:
    result: set[str] = set()
    try:
        entries = list(Path(f"/proc/{pid}/fd").iterdir())
    except OSError as exc:
        raise ProbeError("listener_owner_fd_unreadable", str(pid)) from exc
    for entry in entries:
        try:
            target = os.readlink(entry)
        except OSError:
            continue
        match = re.fullmatch(r"socket:\[([0-9]+)\]", target)
        if match:
            result.add(match.group(1))
    return result


def _require_listener(pid: int, port: int, role: str) -> None:
    listeners = _listener_inodes(port)
    if not listeners:
        raise ProbeError("listener_missing", role)
    if not listeners.intersection(_process_socket_inodes(pid)):
        raise ProbeError("listener_owner_mismatch", role)


def _rfb_banner(port: int) -> None:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=2) as conn:
            banner = conn.recv(12)
    except OSError as exc:
        raise ProbeError("vnc_rfb_unreachable") from exc
    if not banner.startswith(b"RFB "):
        raise ProbeError("vnc_rfb_banner_invalid")


def _toolroot() -> Path:
    raw = _safe_text(SESSION / "toolroot")
    path = Path(raw)
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise ProbeError("toolroot_unavailable") from exc
    if not resolved.is_dir() or path.is_symlink():
        raise ProbeError("toolroot_unsafe")
    return resolved


def _within(root: Path, path: Path) -> Path:
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise ProbeError("tool_executable_outside_toolroot", str(path)) from exc
    return resolved


def _display() -> tuple[str, int]:
    display = _safe_text(SESSION / "display")
    match = re.fullmatch(r":([1-9][0-9]*)", display)
    if not match:
        raise ProbeError("display_invalid")
    number = int(match.group(1))
    socket_path = Path(f"/tmp/.X11-unix/X{number}")
    if not socket_path.exists():
        raise ProbeError("display_socket_missing")
    return display, number


def _raw_xres_window(display: str, pid: int, toolroot: Path) -> int:
    completed = subprocess.run(
        [
            sys.executable,
            str(XRES_OWNER),
            "--display",
            display,
            "--pid",
            str(pid),
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
        env={
            key: value
            for key, value in os.environ.items()
            if not key.upper().startswith("TIBIA_TEST_")
            and "LEASE_TOKEN" not in key.upper()
            and "CAPABILITY" not in key.upper()
        },
    )
    if completed.returncode:
        raise ProbeError("raw_xres_window_unresolved")
    try:
        xid = int(completed.stdout.strip())
    except ValueError as exc:
        raise ProbeError("raw_xres_window_invalid") from exc
    if xid < 1:
        raise ProbeError("raw_xres_window_invalid")
    return xid


def probe(output: Path) -> dict[str, Any]:
    if os.environ.get("RUNNER_NAME") != "synology-otclient-01":
        raise ProbeError("wrong_runner")
    if os.environ.get("GITHUB_REPOSITORY") != "blakinio/otclient":
        raise ProbeError("wrong_repository")
    if not SESSION.is_dir():
        raise ProbeError("session_missing")

    pgid = _positive_int(SESSION / "bootstrap-pgid")
    roles = {
        "client": _positive_int(SESSION / "client.pid"),
        "xvfb": _positive_int(SESSION / "xvfb.pid"),
        "vnc": _positive_int(SESSION / "vnc.pid"),
        "wireproxy": _positive_int(SESSION / "wireproxy.pid"),
    }
    if len(set(roles.values())) != 4:
        raise ProbeError("tracked_pid_not_unique")

    toolroot = _toolroot()
    expected = {
        "xvfb": _within(toolroot, toolroot / "usr/bin/Xvfb"),
        "vnc": _within(toolroot, toolroot / "usr/bin/x11vnc"),
        "wireproxy": Path(_safe_text(SESSION / "wireproxy-bin")),
    }
    for role, pid in roles.items():
        _require_role(pid, role, pgid, expected.get(role))

    display, _ = _display()
    vnc_port = _positive_int(SESSION / "vnc-port")
    warp_port = _positive_int(SESSION / "warp-port")
    if not 1 <= vnc_port <= 65535 or not 1 <= warp_port <= 65535:
        raise ProbeError("listener_port_invalid")
    _require_listener(roles["vnc"], vnc_port, "vnc")
    _require_listener(roles["wireproxy"], warp_port, "wireproxy")
    _rfb_banner(vnc_port)

    xid = _raw_xres_window(display, roles["client"], toolroot)
    data = {
        "pid": roles["client"],
        "process_group_id": pgid,
        "tracked_processes": roles,
        "display": display,
        "window_identity": f"x11-window:{xid}",
        "remote_view_endpoint": f"127.0.0.1:{vnc_port}",
        "remote_view_mapping": "PROVEN",
        "state": "UNKNOWN",
    }
    output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    output.write_text(json.dumps(data, sort_keys=True) + "\n")
    os.chmod(output, 0o600)
    return data


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="operation", required=True)
    probe_parser = sub.add_parser("probe")
    probe_parser.add_argument("output", type=Path)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        probe(args.output)
    except Exception as exc:
        print(
            f"TRACK_A_CANONICAL_XRES_PROBE_ERROR={getattr(exc, 'code', 'probe_failure')}",
            file=sys.stderr,
        )
        return 2
    print("TRACK_A_CANONICAL_XRES_PROBE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
