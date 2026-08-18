#!/usr/bin/env python3
"""Supported authority-aware entry point for the Track A persistent viewer."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
TRANSITION = SCRIPT_DIR / "tibia-official-client-re-canonical-live-transition.py"
XRES_PROBE = SCRIPT_DIR / "tibia-official-client-re-canonical-live-xres-probe.py"
VIEWER = SCRIPT_DIR / "tibia-official-client-re-persistent-viewer.py"


class ControllerError(RuntimeError):
    def __init__(self, code: str, message: str = "") -> None:
        super().__init__(message or code)
        self.code = code


def _run(command: list[str]) -> int:
    completed = subprocess.run(command, close_fds=True, check=False)
    return completed.returncode


def _gate_b(task_id: str, session_id: str, token_file: Path) -> None:
    rc = _run(
        [
            sys.executable,
            str(TRANSITION),
            "gate-b",
            "--task-id",
            task_id,
            "--session-id",
            session_id,
            "--token-file",
            str(token_file),
            "--probe",
            str(XRES_PROBE),
        ]
    )
    if rc:
        raise ControllerError("gate_b_failed")


def start(args: argparse.Namespace) -> int:
    # Gate B is deliberately completed before the low-level presentation
    # primitive is allowed to create persistent observer processes.
    _gate_b(args.task_id, args.session_id, args.token_file)
    command = [
        sys.executable,
        str(VIEWER),
        "start",
        "--task-id",
        args.task_id,
        "--session-id",
        args.session_id,
        "--token-file",
        str(args.token_file),
        "--rfb-port",
        str(args.rfb_port),
        "--backend-port",
        str(args.backend_port),
        "--public-url",
        args.public_url,
    ]
    if args.toolroot is not None:
        command += ["--toolroot", str(args.toolroot)]
    if args.x11vnc is not None:
        command += ["--x11vnc", str(args.x11vnc)]
    if args.websockify is not None:
        command += ["--websockify", str(args.websockify)]
    if args.novnc_root is not None:
        command += ["--novnc-root", str(args.novnc_root)]
    return _run(command)


def health(args: argparse.Namespace) -> int:
    command = [sys.executable, str(VIEWER), "health"]
    if args.toolroot is not None:
        command += ["--toolroot", str(args.toolroot)]
    if args.public_url is not None:
        command += ["--public-url", args.public_url]
    return _run(command)


def stop(args: argparse.Namespace) -> int:
    # Stop is cleanup of the separately marked viewer processes. The low-level
    # implementation still requires the current canonical lease under lock, but
    # does not require a healthy client merely to remove its own observer.
    return _run(
        [
            sys.executable,
            str(VIEWER),
            "stop",
            "--task-id",
            args.task_id,
            "--session-id",
            args.session_id,
            "--token-file",
            str(args.token_file),
        ]
    )


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="operation", required=True)

    start_p = sub.add_parser("start")
    start_p.add_argument("--task-id", required=True)
    start_p.add_argument("--session-id", required=True)
    start_p.add_argument("--token-file", required=True, type=Path)
    start_p.add_argument("--toolroot", type=Path)
    start_p.add_argument("--x11vnc", type=Path)
    start_p.add_argument("--websockify", type=Path)
    start_p.add_argument("--novnc-root", type=Path)
    start_p.add_argument("--rfb-port", type=int, default=5901)
    start_p.add_argument("--backend-port", type=int, default=6081)
    start_p.add_argument("--public-url", default="http://synology:6082/")

    health_p = sub.add_parser("health")
    health_p.add_argument("--toolroot", type=Path)
    health_p.add_argument("--public-url")

    stop_p = sub.add_parser("stop")
    stop_p.add_argument("--task-id", required=True)
    stop_p.add_argument("--session-id", required=True)
    stop_p.add_argument("--token-file", required=True, type=Path)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return {"start": start, "health": health, "stop": stop}[args.operation](args)
    except Exception as exc:
        print(
            f"TRACK_A_PERSISTENT_VIEWER_CONTROLLER_ERROR={getattr(exc, 'code', 'controller_failure')}",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
