#!/usr/bin/env python3
"""Resolve one X11 window to an expected local PID through raw XRes 1.2.

The helper is deliberately read-only: it enumerates X11 resources and sends
X-Resource QueryVersion / QueryClientIds requests. It never mutates the client,
X11 state, process memory, input, login state, or gameplay state.
"""
from __future__ import annotations

import argparse
import ctypes
import importlib.util
import os
from pathlib import Path
import socket
import struct
import sys
import time
from ctypes import (
    POINTER,
    Structure,
    byref,
    c_char_p,
    c_int,
    c_long,
    c_uint,
    c_uint8,
    c_uint16,
    c_uint32,
    c_ulong,
    c_void_p,
)
from dataclasses import dataclass
from typing import Callable, Sequence

VIEWABLE = 2
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
MAX_WINDOWS = 256
MAX_DEPTH = 8


class WindowOwnerError(RuntimeError):
    """Fail-closed X11/XRes ownership resolution error."""


@dataclass(frozen=True)
class WindowCandidate:
    xid: int
    width: int
    height: int


def extract_one_spec_local_pid(records: Sequence[object], local_pid_mask: int) -> int | None:
    """Extract LocalClientPid from a one-spec QueryClientIds reply.

    XRes identifies the owning client in CLIENTIDVALUE.client. For a query made
    with a resource XID, Xorg can therefore return that client's resource base
    (for example 0x00c00000) instead of echoing the queried resource
    (0x00c00011). Association with the queried resource is carried by the
    one-spec QueryClientIds request/reply relation, not equality of those XIDs.
    """

    if not records:
        return None
    if len(records) != 1:
        raise WindowOwnerError("one-spec QueryClientIds returned multiple records")
    record = records[0]
    client = getattr(record, "client", None)
    mask = getattr(record, "mask", None)
    values = getattr(record, "values", None)
    if not isinstance(client, int) or client < 0 or client > 0xFFFFFFFF:
        raise WindowOwnerError("invalid XRes client resource base")
    if mask != local_pid_mask:
        raise WindowOwnerError("unexpected XRes client-id mask")
    if not isinstance(values, tuple) or len(values) != 1:
        raise WindowOwnerError("LocalClientPid must contain one CARD32")
    pid = values[0]
    if not isinstance(pid, int) or pid <= 0 or pid > 0xFFFFFFFF:
        raise WindowOwnerError("LocalClientPid must be positive")
    return pid


def select_owned_xid(
    candidates: Sequence[WindowCandidate],
    expected_pid: int,
    pid_for_xid: Callable[[int], int | None],
) -> int | None:
    """Return exactly one candidate owned by expected_pid, else fail closed."""

    matches: list[int] = []
    for candidate in candidates:
        pid = pid_for_xid(candidate.xid)
        if pid == expected_pid:
            matches.append(candidate.xid)
    if len(matches) > 1:
        raise WindowOwnerError("multiple viewable windows resolve to expected PID")
    return matches[0] if matches else None


def _load_wire(path: Path):
    if not path.is_file():
        raise WindowOwnerError("XRes wire helper missing")
    spec = importlib.util.spec_from_file_location("track_a_xres_wire_window_owner", path)
    if spec is None or spec.loader is None:
        raise WindowOwnerError("cannot import XRes wire helper")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _choose_library(toolroot: Path, name: str) -> Path:
    root = toolroot.resolve()
    candidates = (
        root / "usr/lib/x86_64-linux-gnu" / name,
        root / "lib/x86_64-linux-gnu" / name,
        Path("/usr/lib/x86_64-linux-gnu") / name,
        Path("/lib/x86_64-linux-gnu") / name,
    )
    for candidate in candidates:
        try:
            if not candidate.exists():
                continue
            real = candidate.resolve()
            if not real.is_file():
                continue
            if candidate.is_relative_to(root) and not real.is_relative_to(root):
                continue
            return real
        except OSError:
            continue
    raise WindowOwnerError(f"transport library unavailable: {name}")


class XAttr(Structure):
    _fields_ = [
        ("x", c_int),
        ("y", c_int),
        ("width", c_int),
        ("height", c_int),
        ("border_width", c_int),
        ("depth", c_int),
        ("visual", c_void_p),
        ("root", c_ulong),
        ("win_class", c_int),
        ("bit_gravity", c_int),
        ("win_gravity", c_int),
        ("backing_store", c_int),
        ("backing_planes", c_ulong),
        ("backing_pixel", c_ulong),
        ("save_under", c_int),
        ("colormap", c_ulong),
        ("map_installed", c_int),
        ("map_state", c_int),
        ("all_event_masks", c_long),
        ("your_event_mask", c_long),
        ("do_not_propagate_mask", c_long),
        ("override_redirect", c_int),
        ("screen", c_void_p),
    ]


def _enumerate_candidates(display: str, libx11_path: Path) -> list[WindowCandidate]:
    x11 = ctypes.CDLL(str(libx11_path))
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
    x11.XGetWindowAttributes.argtypes = [c_void_p, c_ulong, POINTER(XAttr)]
    x11.XGetWindowAttributes.restype = c_int
    x11.XFree.argtypes = [c_void_p]
    x11.XFree.restype = c_int
    x11.XCloseDisplay.argtypes = [c_void_p]
    x11.XCloseDisplay.restype = c_int

    dpy = x11.XOpenDisplay(display.encode())
    if not dpy:
        raise WindowOwnerError("XOpenDisplay failed")
    root = int(x11.XDefaultRootWindow(dpy))
    seen = {root}
    candidates: list[WindowCandidate] = []
    visited = 0

    def walk(parent: int, depth: int) -> None:
        nonlocal visited
        if depth > MAX_DEPTH or visited >= MAX_WINDOWS:
            return
        root_ret = c_ulong()
        parent_ret = c_ulong()
        children = POINTER(c_ulong)()
        count = c_uint()
        if not x11.XQueryTree(
            dpy,
            c_ulong(parent),
            byref(root_ret),
            byref(parent_ret),
            byref(children),
            byref(count),
        ):
            raise WindowOwnerError("XQueryTree failed")
        try:
            for index in range(int(count.value)):
                if visited >= MAX_WINDOWS:
                    break
                xid = int(children[index])
                if xid in seen:
                    continue
                seen.add(xid)
                visited += 1
                attr = XAttr()
                if x11.XGetWindowAttributes(dpy, c_ulong(xid), byref(attr)):
                    if (
                        int(attr.map_state) == VIEWABLE
                        and int(attr.width) == TARGET_WIDTH
                        and int(attr.height) == TARGET_HEIGHT
                    ):
                        candidates.append(
                            WindowCandidate(xid, int(attr.width), int(attr.height))
                        )
                walk(xid, depth + 1)
        finally:
            if children:
                x11.XFree(children)

    try:
        walk(root, 1)
    finally:
        x11.XCloseDisplay(dpy)
    return candidates


class Cookie(Structure):
    _fields_ = [("sequence", c_uint)]


class QueryExtensionReply(Structure):
    _fields_ = [
        ("response_type", c_uint8),
        ("pad0", c_uint8),
        ("sequence", c_uint16),
        ("length", c_uint32),
        ("present", c_uint8),
        ("major_opcode", c_uint8),
        ("first_event", c_uint8),
        ("first_error", c_uint8),
        ("pad1", c_uint8 * 20),
    ]


class RawXRes:
    def __init__(self, display: str, libxcb_path: Path, wire) -> None:
        self.display = display
        self.wire = wire
        self.xcb = ctypes.CDLL(str(libxcb_path))
        self.libc = ctypes.CDLL(None)
        self.conn: int | None = None
        self.sock: socket.socket | None = None
        self.sequence = 0
        self.major_opcode = 0
        self.byte_order = sys.byteorder
        self._configure()

    def _configure(self) -> None:
        xcb = self.xcb
        xcb.xcb_connect.argtypes = [c_char_p, POINTER(c_int)]
        xcb.xcb_connect.restype = c_void_p
        xcb.xcb_connection_has_error.argtypes = [c_void_p]
        xcb.xcb_connection_has_error.restype = c_int
        xcb.xcb_disconnect.argtypes = [c_void_p]
        xcb.xcb_query_extension.argtypes = [c_void_p, c_uint16, c_char_p]
        xcb.xcb_query_extension.restype = Cookie
        xcb.xcb_query_extension_reply.argtypes = [c_void_p, Cookie, c_void_p]
        xcb.xcb_query_extension_reply.restype = c_void_p
        xcb.xcb_get_file_descriptor.argtypes = [c_void_p]
        xcb.xcb_get_file_descriptor.restype = c_int
        xcb.xcb_flush.argtypes = [c_void_p]
        xcb.xcb_flush.restype = c_int
        self.libc.free.argtypes = [c_void_p]

    def __enter__(self):
        screen = c_int()
        conn = self.xcb.xcb_connect(self.display.encode(), byref(screen))
        if not conn or self.xcb.xcb_connection_has_error(conn):
            raise WindowOwnerError("xcb_connect failed")
        self.conn = int(conn)
        ext_name = b"X-Resource"
        cookie = self.xcb.xcb_query_extension(conn, len(ext_name), ext_name)
        ext_ptr = self.xcb.xcb_query_extension_reply(conn, cookie, None)
        if not ext_ptr:
            raise WindowOwnerError("XRes QueryExtension failed")
        try:
            ext = ctypes.cast(ext_ptr, POINTER(QueryExtensionReply)).contents
            if int(ext.response_type) != 1 or int(ext.present) != 1:
                raise WindowOwnerError("XRes extension unavailable")
            self.major_opcode = int(ext.major_opcode)
        finally:
            self.libc.free(ext_ptr)
        if self.major_opcode < 128:
            raise WindowOwnerError("invalid XRes major opcode")
        if self.xcb.xcb_flush(conn) <= 0:
            raise WindowOwnerError("xcb_flush failed")
        fd = self.xcb.xcb_get_file_descriptor(conn)
        if fd < 0:
            raise WindowOwnerError("xcb file descriptor unavailable")
        self.sock = socket.socket(fileno=os.dup(fd))
        self.sock.settimeout(5.0)
        self.sequence = int(cookie.sequence) & 0xFFFF

        self.sequence = (self.sequence + 1) & 0xFFFF
        self.sock.sendall(
            self.wire.encode_query_version(self.major_opcode, self.byte_order)
        )
        version_bytes = self._recv_reply(self.sequence)
        version = self.wire.parse_query_version_reply(
            version_bytes, self.byte_order, expected_sequence=self.sequence
        )
        self.wire.require_xres_1_2(version)
        return self

    def __exit__(self, _type, _value, _traceback) -> None:
        if self.sock is not None:
            self.sock.close()
            self.sock = None
        if self.conn is not None:
            self.xcb.xcb_disconnect(c_void_p(self.conn))
            self.conn = None

    def _recv_exact(self, count: int) -> bytes:
        if self.sock is None:
            raise WindowOwnerError("raw XRes socket unavailable")
        data = bytearray()
        while len(data) < count:
            chunk = self.sock.recv(count - len(data))
            if not chunk:
                raise WindowOwnerError("unexpected X11 EOF")
            data.extend(chunk)
        return bytes(data)

    def _recv_reply(self, expected_sequence: int) -> bytes:
        prefix = "<" if self.byte_order == "little" else ">"
        for _ in range(8):
            header = self._recv_exact(32)
            response_type = header[0] & 0x7F
            sequence = struct.unpack_from(prefix + "H", header, 2)[0]
            if response_type == 0:
                raise WindowOwnerError(
                    f"X11 error code={header[1]} sequence={sequence}"
                )
            if response_type != 1:
                continue
            if sequence != expected_sequence:
                raise WindowOwnerError(
                    f"X11 sequence mismatch {sequence}!={expected_sequence}"
                )
            length_words = struct.unpack_from(prefix + "I", header, 4)[0]
            if length_words > 1024:
                raise WindowOwnerError("X11 reply exceeds cap")
            return header + self._recv_exact(length_words * 4)
        raise WindowOwnerError("X11 reply not found")

    def local_pid(self, xid: int) -> int | None:
        if self.sock is None:
            raise WindowOwnerError("raw XRes socket unavailable")
        self.sequence = (self.sequence + 1) & 0xFFFF
        self.sock.sendall(
            self.wire.encode_query_client_ids(
                self.major_opcode, xid, self.byte_order
            )
        )
        reply = self._recv_reply(self.sequence)
        records = self.wire.parse_query_client_ids_reply(
            reply, self.byte_order, expected_sequence=self.sequence
        )
        return extract_one_spec_local_pid(
            records, self.wire.XRES_CLIENT_ID_MASK_LOCAL_CLIENT_PID
        )


def resolve_window(
    display: str,
    expected_pid: int,
    toolroot: Path,
    wire_path: Path,
    attempts: int,
    delay: float,
) -> int:
    if expected_pid <= 1:
        raise WindowOwnerError("expected PID must be greater than one")
    if attempts <= 0 or attempts > 600:
        raise WindowOwnerError("attempt count outside bounds")
    if delay < 0 or delay > 10:
        raise WindowOwnerError("delay outside bounds")

    wire = _load_wire(wire_path)
    libx11 = _choose_library(toolroot, "libX11.so.6")
    libxcb = _choose_library(toolroot, "libxcb.so.1")
    last_error: Exception | None = None

    for attempt in range(attempts):
        try:
            os.kill(expected_pid, 0)
        except ProcessLookupError as exc:
            raise WindowOwnerError("expected client process exited") from exc
        candidates = _enumerate_candidates(display, libx11)
        if candidates:
            try:
                with RawXRes(display, libxcb, wire) as xres:
                    owned = select_owned_xid(
                        candidates, expected_pid, xres.local_pid
                    )
                if owned is not None:
                    return owned
                last_error = None
            except WindowOwnerError as exc:
                last_error = exc
        if attempt + 1 < attempts:
            time.sleep(delay)

    if last_error is not None:
        raise WindowOwnerError(f"XRes ownership unresolved: {last_error}") from last_error
    raise WindowOwnerError("no viewable 1920x1080 window owned by expected PID")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--display", required=True)
    result.add_argument("--pid", required=True, type=int)
    result.add_argument("--toolroot", required=True, type=Path)
    result.add_argument("--wire-helper", required=True, type=Path)
    result.add_argument("--attempts", type=int, default=120)
    result.add_argument("--delay", type=float, default=0.25)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        xid = resolve_window(
            args.display,
            args.pid,
            args.toolroot,
            args.wire_helper,
            args.attempts,
            args.delay,
        )
    except WindowOwnerError as exc:
        print(f"TRACK_A_XRES_WINDOW_OWNER_ERROR={exc}", file=sys.stderr)
        return 1
    print(xid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
