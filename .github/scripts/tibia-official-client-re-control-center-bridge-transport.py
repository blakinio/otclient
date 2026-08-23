#!/usr/bin/env python3
"""External Track A process transport for Control Center guarded dispatch."""
from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any


class TransportError(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class TransitionProcess:
    def __init__(self, process: Any):
        self._process = process
        self.stdin = process.stdin
        self.stdout = process.stdout

    def poll(self):
        return self._process.poll()

    def wait(self, timeout=None):
        try:
            return self._process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError("track_a_transport_wait_timeout") from exc

    def terminate(self):
        return self._process.terminate()


def _owned_path(root: Path, raw: str) -> Path:
    path = Path(raw).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise TransportError("track_a_transport_command_invalid") from exc
    return path


def _validate_command(command: Sequence[str], cwd: Path) -> list[str]:
    if not isinstance(command, (list, tuple)) or len(command) != 15:
        raise TransportError("track_a_transport_command_invalid")
    if not all(isinstance(value, str) and value for value in command):
        raise TransportError("track_a_transport_command_invalid")
    argv = list(command)
    root = Path(cwd).resolve()
    expected_transition = (root / ".github/scripts/tibia-official-client-re-canonical-live-transition.py").resolve()
    if Path(argv[0]).resolve() != Path(sys.executable).resolve():
        raise TransportError("track_a_transport_command_invalid")
    if _owned_path(root, argv[1]) != expected_transition or argv[2] != "guarded-dispatch":
        raise TransportError("track_a_transport_command_invalid")
    flags = ("--task-id", "--session-id", "--token-file", "--probe", "--worker", "--request-file")
    if tuple(argv[index] for index in (3, 5, 7, 9, 11, 13)) != flags:
        raise TransportError("track_a_transport_command_invalid")
    for index in (10, 12):
        _owned_path(root, argv[index])
    return argv


def start_transition_process(command: Sequence[str], cwd: Path) -> TransitionProcess:
    root = Path(cwd).resolve()
    argv = _validate_command(command, root)
    process = subprocess.Popen(
        argv,
        cwd=root,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        close_fds=True,
        shell=False,
    )
    if process.stdin is None or process.stdout is None:
        try:
            process.terminate()
        except OSError:
            pass
        raise TransportError("track_a_transport_pipe_unavailable")
    return TransitionProcess(process)