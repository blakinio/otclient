#!/usr/bin/env python3
"""Fail-closed inspection of the already manifest-owned Track-A X11 window.

This helper never selects a replacement window. It revalidates the supplied XID
against the exact client PID through XRes, reports X11 geometry/topology, and
summarizes same-PID viewable descendants without changing focus, size, parent,
map state, or any X11 resource.
"""
from __future__ import annotations

import argparse
import ctypes
import importlib.util
import os
from collections import Counter
from ctypes import POINTER, byref, c_char_p, c_int, c_uint, c_ulong, c_void_p
from pathlib import Path
import sys


MAX_WINDOWS = 256
MAX_DEPTH = 8


class UiWindowError(RuntimeError):
    pass


def load_owner(path: Path):
    if not path.is_file():
        raise UiWindowError("owner_helper_missing")
    spec = importlib.util.spec_from_file_location("track_a_xres_owner_exact_ui", path)
    if spec is None or spec.loader is None:
        raise UiWindowError("owner_import_failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def inspect_exact(
    *,
    display: str,
    pid: int,
    xid: int,
    toolroot: Path,
    owner_helper: Path,
    wire_helper: Path,
) -> dict[str, object]:
    if pid <= 1:
        raise UiWindowError("pid_out_of_bounds")
    if xid <= 0 or xid > 0xFFFFFFFF:
        raise UiWindowError("xid_out_of_bounds")
    try:
        os.kill(pid, 0)
    except ProcessLookupError as exc:
        raise UiWindowError("exact_client_exited") from exc

    owner = load_owner(owner_helper)
    wire = owner._load_wire(wire_helper)
    libx11 = owner._choose_library(toolroot, "libX11.so.6")
    libxcb = owner._choose_library(toolroot, "libxcb.so.1")

    x11 = ctypes.CDLL(str(libx11))
    x11.XOpenDisplay.argtypes = [c_char_p]
    x11.XOpenDisplay.restype = c_void_p
    x11.XDefaultRootWindow.argtypes = [c_void_p]
    x11.XDefaultRootWindow.restype = c_ulong
    x11.XQueryTree.argtypes = [
        c_void_p,
        c_ulong,
        POINTER(c_ulong),
        POINTER(c_ulong),
        POINTER(POINTER(c_ulong)),
        POINTER(c_uint),
    ]
    x11.XQueryTree.restype = c_int
    x11.XGetWindowAttributes.argtypes = [c_void_p, c_ulong, POINTER(owner.XAttr)]
    x11.XGetWindowAttributes.restype = c_int
    x11.XFree.argtypes = [c_void_p]
    x11.XFree.restype = c_int
    x11.XCloseDisplay.argtypes = [c_void_p]
    x11.XCloseDisplay.restype = c_int

    dpy = x11.XOpenDisplay(display.encode())
    if not dpy:
        raise UiWindowError("XOpenDisplay_failed")

    def attrs(window: int):
        value = owner.XAttr()
        if not x11.XGetWindowAttributes(dpy, c_ulong(window), byref(value)):
            raise UiWindowError(f"XGetWindowAttributes_failed:{window}")
        return value

    def children_of(window: int) -> tuple[int, int, list[int]]:
        root_ret = c_ulong()
        parent_ret = c_ulong()
        children = POINTER(c_ulong)()
        count = c_uint()
        if not x11.XQueryTree(
            dpy,
            c_ulong(window),
            byref(root_ret),
            byref(parent_ret),
            byref(children),
            byref(count),
        ):
            raise UiWindowError(f"XQueryTree_failed:{window}")
        try:
            values = [int(children[i]) for i in range(int(count.value))]
        finally:
            if children:
                x11.XFree(children)
        return int(root_ret.value), int(parent_ret.value), values

    try:
        root = int(x11.XDefaultRootWindow(dpy))
        target = attrs(xid)
        query_root, parent, direct_children = children_of(xid)
        if query_root != root or int(target.root) != root:
            raise UiWindowError("root_identity_mismatch")
        if int(target.map_state) != owner.VIEWABLE:
            raise UiWindowError("manifest_window_not_viewable")
        root_attr = attrs(root)
        parent_attr = attrs(parent) if parent else None

        descendants: list[tuple[int, int, int, int]] = []
        seen = {xid}

        def walk(window: int, depth: int) -> None:
            if depth > MAX_DEPTH or len(seen) >= MAX_WINDOWS:
                return
            _r, _p, kids = children_of(window)
            for child in kids:
                if child in seen or len(seen) >= MAX_WINDOWS:
                    continue
                seen.add(child)
                a = attrs(child)
                descendants.append((child, int(a.width), int(a.height), int(a.map_state)))
                walk(child, depth + 1)

        walk(xid, 1)
    finally:
        x11.XCloseDisplay(dpy)

    with owner.RawXRes(display, libxcb, wire) as xres:
        target_pid = xres.local_pid(xid)
        if target_pid != pid:
            raise UiWindowError(f"manifest_xres_pid:{target_pid}!={pid}")
        same_pid_viewable: list[tuple[int, int, int]] = []
        for child, width, height, map_state in descendants:
            if map_state != owner.VIEWABLE:
                continue
            try:
                child_pid = xres.local_pid(child)
            except Exception:
                continue
            if child_pid == pid:
                same_pid_viewable.append((child, width, height))

    histogram = Counter((width, height) for _child, width, height in same_pid_viewable)
    geometry_histogram = ",".join(
        f"{width}x{height}:{count}"
        for (width, height), count in sorted(histogram.items())
    ) or "NONE"
    unique_1020 = sum(1 for _child, width, height in same_pid_viewable if (width, height) == (1020, 650))

    return {
        "xid": xid,
        "width": int(target.width),
        "height": int(target.height),
        "border": int(target.border_width),
        "depth": int(target.depth),
        "map_state": int(target.map_state),
        "root": root,
        "root_width": int(root_attr.width),
        "root_height": int(root_attr.height),
        "parent": parent,
        "parent_is_root": parent == root,
        "parent_width": int(parent_attr.width) if parent_attr is not None else 0,
        "parent_height": int(parent_attr.height) if parent_attr is not None else 0,
        "direct_child_count": len(direct_children),
        "descendant_count": len(descendants),
        "same_pid_viewable_descendant_count": len(same_pid_viewable),
        "same_pid_viewable_geometry_histogram": geometry_histogram,
        "same_pid_viewable_1020x650_count": unique_1020,
    }


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--display", required=True)
    p.add_argument("--pid", required=True, type=int)
    p.add_argument("--xid", required=True, type=int)
    p.add_argument("--toolroot", required=True, type=Path)
    p.add_argument("--owner-helper", required=True, type=Path)
    p.add_argument("--wire-helper", required=True, type=Path)
    return p


def main() -> int:
    args = parser().parse_args()
    try:
        info = inspect_exact(
            display=args.display,
            pid=args.pid,
            xid=args.xid,
            toolroot=args.toolroot,
            owner_helper=args.owner_helper,
            wire_helper=args.wire_helper,
        )
    except Exception as exc:
        print(f"WORLDMAP_UI_EXACT_INSPECT_ERROR={type(exc).__name__}:{exc}", file=sys.stderr)
        return 44

    print(f"WORLDMAP_UI_EXACT_XID=x11-window:{info['xid']}")
    print(f"WORLDMAP_UI_EXACT_GEOMETRY={info['width']}x{info['height']}")
    print(f"WORLDMAP_UI_EXACT_BORDER_WIDTH={info['border']}")
    print(f"WORLDMAP_UI_EXACT_DEPTH={info['depth']}")
    print(f"WORLDMAP_UI_EXACT_MAP_STATE={info['map_state']}")
    print("WORLDMAP_UI_EXACT_XRES_PID_MATCH=PASS")
    print(f"WORLDMAP_UI_ROOT_GEOMETRY={info['root_width']}x{info['root_height']}")
    print("WORLDMAP_UI_PARENT_RELATION=" + ("DIRECT_ROOT_CHILD" if info['parent_is_root'] else "REPARENTED_OR_NESTED"))
    print(f"WORLDMAP_UI_PARENT_GEOMETRY={info['parent_width']}x{info['parent_height']}")
    print(f"WORLDMAP_UI_DIRECT_CHILD_COUNT={info['direct_child_count']}")
    print(f"WORLDMAP_UI_DESCENDANT_COUNT={info['descendant_count']}")
    print(f"WORLDMAP_UI_SAME_PID_VIEWABLE_DESCENDANT_COUNT={info['same_pid_viewable_descendant_count']}")
    print(f"WORLDMAP_UI_SAME_PID_VIEWABLE_DESCENDANT_GEOMETRIES={info['same_pid_viewable_geometry_histogram']}")
    print(f"WORLDMAP_UI_SAME_PID_VIEWABLE_1020X650_COUNT={info['same_pid_viewable_1020x650_count']}")
    print("WORLDMAP_UI_EXACT_INSPECT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
