#!/usr/bin/env python3
"""Resolve the exact 1020x650 Tibia UI window through XRes LocalClientPid.

This helper is a UI-control locator only. The task's 1920x1080 XRes-owned window
remains the runtime identity fence. The returned 1020x650 XID is independently
required to resolve to the same exact client PID before fixed UI geometry may be
used. No _NET_WM_PID or xdotool PID lookup is treated as ownership evidence.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import sys
import time


TARGET_WIDTH = 1020
TARGET_HEIGHT = 650


class UiWindowError(RuntimeError):
    pass


def load_owner(path: Path):
    if not path.is_file():
        raise UiWindowError("owner helper missing")
    spec = importlib.util.spec_from_file_location("track_a_xres_owner_for_ui", path)
    if spec is None or spec.loader is None:
        raise UiWindowError("cannot import owner helper")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def resolve_ui_window(
    *,
    display: str,
    pid: int,
    toolroot: Path,
    owner_helper: Path,
    wire_helper: Path,
    attempts: int,
    delay: float,
) -> int:
    if pid <= 1:
        raise UiWindowError("pid must be greater than one")
    if attempts <= 0 or attempts > 240:
        raise UiWindowError("attempt count outside bounds")
    if delay < 0 or delay > 5:
        raise UiWindowError("delay outside bounds")

    owner = load_owner(owner_helper)
    owner.TARGET_WIDTH = TARGET_WIDTH
    owner.TARGET_HEIGHT = TARGET_HEIGHT
    wire = owner._load_wire(wire_helper)
    libx11 = owner._choose_library(toolroot, "libX11.so.6")
    libxcb = owner._choose_library(toolroot, "libxcb.so.1")
    last_error: Exception | None = None

    for attempt in range(attempts):
        try:
            os.kill(pid, 0)
        except ProcessLookupError as exc:
            raise UiWindowError("exact client process exited") from exc
        try:
            candidates = owner._enumerate_candidates(display, libx11)
            if candidates:
                with owner.RawXRes(display, libxcb, wire) as xres:
                    xid = owner.select_owned_xid(candidates, pid, xres.local_pid)
                if xid is not None:
                    return int(xid)
                last_error = UiWindowError("1020x650 candidates exist but none belong to exact PID")
            else:
                last_error = UiWindowError("no viewable 1020x650 candidate")
        except Exception as exc:  # fail closed after bounded retries
            last_error = exc
        if attempt + 1 < attempts:
            time.sleep(delay)

    raise UiWindowError(f"XRes UI-window ownership unresolved: {last_error}")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--display", required=True)
    p.add_argument("--pid", required=True, type=int)
    p.add_argument("--toolroot", required=True, type=Path)
    p.add_argument("--owner-helper", required=True, type=Path)
    p.add_argument("--wire-helper", required=True, type=Path)
    p.add_argument("--attempts", type=int, default=40)
    p.add_argument("--delay", type=float, default=0.25)
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        xid = resolve_ui_window(
            display=args.display,
            pid=args.pid,
            toolroot=args.toolroot,
            owner_helper=args.owner_helper,
            wire_helper=args.wire_helper,
            attempts=args.attempts,
            delay=args.delay,
        )
    except UiWindowError as exc:
        print(f"WORLDMAP_XRES_UI_WINDOW_ERROR={exc}", file=sys.stderr)
        return 1
    print(xid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
