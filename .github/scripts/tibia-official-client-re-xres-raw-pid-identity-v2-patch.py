#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

TASK_ID = 'OTC-20260817-track-a-xres-raw-pid-identity'
INHERITED_TASK_ID = 'OTC-20260816-track-a-canonical-runtime-e2e'


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'XRES_RAW_V2_PATCH_REFUSED={label}_COUNT:{count}')
    return text.replace(old, new, 1)


def patch(text: str) -> str:
    inherited = f"task='{INHERITED_TASK_ID}'"
    text = replace_once(text, inherited, f"task='{TASK_ID}'", 'TASK_OWNER')
    if INHERITED_TASK_ID in text:
        raise SystemExit('XRES_RAW_V2_PATCH_REFUSED=INHERITED_TASK_REMAINS')

    snapshot_anchor = 'PYALLX\n    : >"$out"'
    snapshot_block = r'''PYALLX
    if [[ "$label" == t35 ]]; then
      python3 - "$display" "$client_pid" "$label" "$root/xres-raw-$label.tsv" "$tool" "$GITHUB_WORKSPACE/.github/scripts/tibia-official-client-re-xres-wire.py" <<'PYXRES'
import ctypes
import importlib.util
import os
import pathlib
import socket
import struct
import sys
from ctypes import POINTER, Structure, byref, c_char_p, c_int, c_long, c_uint, c_uint8, c_uint16, c_uint32, c_ulong, c_void_p

display, client_pid_s, label, out_path, tool_s, helper_s = sys.argv[1:]
client_pid = int(client_pid_s)
tool = pathlib.Path(tool_s).resolve()
helper_path = pathlib.Path(helper_s).resolve()


def choose_library(name):
    candidates = [
        tool / 'usr/lib/x86_64-linux-gnu' / name,
        tool / 'lib/x86_64-linux-gnu' / name,
        pathlib.Path('/usr/lib/x86_64-linux-gnu') / name,
        pathlib.Path('/lib/x86_64-linux-gnu') / name,
    ]
    for candidate in candidates:
        try:
            if candidate.exists():
                real = candidate.resolve()
                if real.is_file():
                    if str(candidate).startswith(str(tool)) and tool not in real.parents:
                        continue
                    return real
        except OSError:
            continue
    return None


if not helper_path.is_file():
    raise SystemExit('XRES_RAW_V2_ERROR=promoted_helper_missing')
spec = importlib.util.spec_from_file_location('track_a_xres_wire_runtime_v2', helper_path)
if spec is None or spec.loader is None:
    raise SystemExit('XRES_RAW_V2_ERROR=promoted_helper_import_spec')
wire = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = wire
spec.loader.exec_module(wire)

libxcb_path = choose_library('libxcb.so.1')
libx11_path = choose_library('libX11.so.6')
if not libxcb_path or not libx11_path:
    raise SystemExit(f'XRES_RAW_V2_ERROR=transport_library_missing:libxcb={bool(libxcb_path)}:libX11={bool(libx11_path)}')

class XAttr(Structure):
    _fields_ = [
        ('x', c_int), ('y', c_int), ('width', c_int), ('height', c_int),
        ('border_width', c_int), ('depth', c_int), ('visual', c_void_p),
        ('root', c_ulong), ('win_class', c_int), ('bit_gravity', c_int),
        ('win_gravity', c_int), ('backing_store', c_int), ('backing_planes', c_ulong),
        ('backing_pixel', c_ulong), ('save_under', c_int), ('colormap', c_ulong),
        ('map_installed', c_int), ('map_state', c_int), ('all_event_masks', c_long),
        ('your_event_mask', c_long), ('do_not_propagate_mask', c_long),
        ('override_redirect', c_int), ('screen', c_void_p),
    ]

x11 = ctypes.CDLL(str(libx11_path))
x11.XOpenDisplay.argtypes = [c_char_p]
x11.XOpenDisplay.restype = c_void_p
x11.XDefaultRootWindow.argtypes = [c_void_p]
x11.XDefaultRootWindow.restype = c_ulong
x11.XQueryTree.argtypes = [c_void_p, c_ulong, POINTER(c_ulong), POINTER(c_ulong), POINTER(POINTER(c_ulong)), POINTER(c_uint)]
x11.XQueryTree.restype = c_int
x11.XGetWindowAttributes.argtypes = [c_void_p, c_ulong, POINTER(XAttr)]
x11.XGetWindowAttributes.restype = c_int
x11.XFree.argtypes = [c_void_p]
x11.XFree.restype = c_int
x11.XCloseDisplay.argtypes = [c_void_p]
x11.XCloseDisplay.restype = c_int

dpy = x11.XOpenDisplay(display.encode())
if not dpy:
    raise SystemExit('XRES_RAW_V2_ERROR=XOpenDisplay')
root = int(x11.XDefaultRootWindow(dpy))
rows = []
seen = {root}

def walk(parent, depth):
    if depth > 6 or len(rows) >= 120:
        return
    root_ret = c_ulong(); parent_ret = c_ulong(); children = POINTER(c_ulong)(); n = c_uint()
    if not x11.XQueryTree(dpy, c_ulong(parent), byref(root_ret), byref(parent_ret), byref(children), byref(n)):
        return
    try:
        for i in range(min(int(n.value), 120 - len(rows))):
            wid = int(children[i])
            if wid in seen:
                continue
            seen.add(wid)
            attr = XAttr()
            if x11.XGetWindowAttributes(dpy, c_ulong(wid), byref(attr)):
                rows.append((wid, int(attr.map_state), int(attr.width), int(attr.height)))
            walk(wid, depth + 1)
            if len(rows) >= 120:
                break
    finally:
        if children:
            x11.XFree(children)
walk(root, 1)
x11.XCloseDisplay(dpy)

candidates = [(wid, state, width, height) for wid, state, width, height in rows if state == 2 and width == 1920 and height == 1080]
print(f'XRES_RAW_V2_CANDIDATE_COUNT={label}:{len(candidates)}')
for wid, state, width, height in rows:
    print(f'XRES_RAW_V2_WINDOW={label}:xid=0x{wid:08x}:map={state}:geom={width}x{height}')

class Cookie(Structure):
    _fields_ = [('sequence', c_uint)]

class QueryExtensionReply(Structure):
    _fields_ = [
        ('response_type', c_uint8), ('pad0', c_uint8), ('sequence', c_uint16),
        ('length', c_uint32), ('present', c_uint8), ('major_opcode', c_uint8),
        ('first_event', c_uint8), ('first_error', c_uint8), ('pad1', c_uint8 * 20),
    ]

xcb = ctypes.CDLL(str(libxcb_path))
libc = ctypes.CDLL(None)
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
libc.free.argtypes = [c_void_p]

screen = c_int()
conn = xcb.xcb_connect(display.encode(), byref(screen))
if not conn or xcb.xcb_connection_has_error(conn):
    raise SystemExit('XRES_RAW_V2_ERROR=xcb_connect')
raw_sock = None
lines = []
try:
    ext_name = b'X-Resource'
    ext_cookie = xcb.xcb_query_extension(conn, len(ext_name), ext_name)
    ext_ptr = xcb.xcb_query_extension_reply(conn, ext_cookie, None)
    if not ext_ptr:
        raise SystemExit('XRES_RAW_V2_ERROR=query_extension_reply')
    try:
        ext = ctypes.cast(ext_ptr, POINTER(QueryExtensionReply)).contents
        if int(ext.response_type) != 1 or int(ext.present) != 1:
            raise SystemExit('XRES_RAW_V2_ERROR=xres_extension_absent')
        major_opcode = int(ext.major_opcode)
    finally:
        libc.free(ext_ptr)
    if major_opcode < 128:
        raise SystemExit('XRES_RAW_V2_ERROR=xres_major_opcode_range')
    if xcb.xcb_flush(conn) <= 0:
        raise SystemExit('XRES_RAW_V2_ERROR=xcb_flush')
    fd = xcb.xcb_get_file_descriptor(conn)
    if fd < 0:
        raise SystemExit('XRES_RAW_V2_ERROR=xcb_fd')
    raw_sock = socket.socket(fileno=os.dup(fd))
    raw_sock.settimeout(5.0)

    def recv_exact(count):
        out = bytearray()
        while len(out) < count:
            chunk = raw_sock.recv(count - len(out))
            if not chunk:
                raise RuntimeError('unexpected_eof')
            out.extend(chunk)
        return bytes(out)

    def recv_reply(expected_sequence):
        for _ in range(8):
            header = recv_exact(32)
            response_type = header[0] & 0x7f
            sequence = struct.unpack_from('<H', header, 2)[0]
            if response_type == 0:
                error_code = header[1]
                major = header[10]
                minor = struct.unpack_from('<H', header, 8)[0]
                raise RuntimeError(f'x11_error:{error_code}:major={major}:minor={minor}:seq={sequence}')
            if response_type != 1:
                continue
            if sequence != expected_sequence:
                raise RuntimeError(f'sequence:{sequence}!={expected_sequence}')
            length_words = struct.unpack_from('<I', header, 4)[0]
            if length_words > 1024:
                raise RuntimeError('reply_too_large')
            return header + recv_exact(length_words * 4)
        raise RuntimeError('reply_not_found')

    sequence = (int(ext_cookie.sequence) + 1) & 0xffff
    raw_sock.sendall(wire.encode_query_version(major_opcode, 'little'))
    version_bytes = recv_reply(sequence)
    print(f'XRES_RAW_V2_VERSION_REPLY_HEX={label}:{version_bytes.hex()}')
    version = wire.parse_query_version_reply(version_bytes, 'little', expected_sequence=sequence)
    wire.require_xres_1_2(version)
    print(f'XRES_RAW_V2_VERSION={label}:{version.server_major}.{version.server_minor}:major_opcode={major_opcode}:sequence={sequence}')

    for wid, _state, width, height in candidates:
        sequence = (sequence + 1) & 0xffff
        try:
            raw_sock.sendall(wire.encode_query_client_ids(major_opcode, wid, 'little'))
            reply_bytes = recv_reply(sequence)
            print(f'XRES_RAW_V2_REPLY_HEX={label}:xid=0x{wid:08x}:sequence={sequence}:hex={reply_bytes.hex()}')
            records = wire.parse_query_client_ids_reply(reply_bytes, 'little', expected_sequence=sequence)
            pid = wire.extract_local_client_pid(records, wid)
            match = pid == client_pid if pid is not None else False
            pid_text = str(pid) if pid is not None else 'unknown'
            print(f'XRES_RAW_V2_IDENTITY={label}:xid=0x{wid:08x}:geom={width}x{height}:pid={pid_text}:matches_exact_client={str(match).lower()}')
            lines.append(f'0x{wid:08x}\tVIEWABLE\t{width}x{height}\t{pid_text}\t{str(match).lower()}')
        except Exception as exc:
            msg = ''.join(ch if ch.isalnum() or ch in '._:-' else '?' for ch in str(exc))[:160]
            print(f'XRES_RAW_V2_CANDIDATE_ERROR={label}:xid=0x{wid:08x}:{type(exc).__name__}:{msg}')
            lines.append(f'0x{wid:08x}\tVIEWABLE\t{width}x{height}\terror\tfalse')
finally:
    if raw_sock is not None:
        raw_sock.close()
    xcb.xcb_disconnect(conn)

pathlib.Path(out_path).write_text('\n'.join(lines) + ('\n' if lines else ''), encoding='utf-8')
PYXRES
    fi
    : >"$out"'''
    text = replace_once(text, snapshot_anchor, snapshot_block, 'SNAPSHOT_T35_XRES_INSERT')

    final_anchor = 'echo "WINDOW_DIAG_CLASSIFICATION=$classification"'
    final_block = r'''xres_raw_t35="$root/xres-raw-t35.tsv"
xres_raw_classification=XRES_RAW_V2_IDENTITY_UNRESOLVED
if [[ -s "$xres_raw_t35" ]] && awk -F'\t' '$2=="VIEWABLE" && $3=="1920x1080" && $5=="true" {found=1} END{exit !found}' "$xres_raw_t35"; then
  xres_raw_classification=XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
elif [[ -s "$xres_raw_t35" ]] && awk -F'\t' '$2=="VIEWABLE" && $3=="1920x1080" && $4 ~ /^[0-9]+$/ && $5=="false" {found=1} END{exit !found}' "$xres_raw_t35"; then
  xres_raw_classification=XRES_PROVES_VIEWABLE_WINDOW_FOREIGN_TO_EXACT_CLIENT
fi
echo "XRES_RAW_V2_FINAL_CLASSIFICATION=$xres_raw_classification"
echo "XRES_RAW_V2_WIRE_HELPER_USED=true"
echo "WINDOW_DIAG_CLASSIFICATION=$classification"'''
    text = replace_once(text, final_anchor, final_block, 'FINAL_XRES_CLASSIFICATION')

    required = (
        f"task='{TASK_ID}'",
        '[[ "$label" == t35 ]]',
        'XRES_RAW_V2_REPLY_HEX=',
        'wire.parse_query_client_ids_reply',
        'wire.extract_local_client_pid',
        'XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT',
        'XRES_RAW_V2_WIRE_HELPER_USED=true',
        'WINDOW_DIAG_CLEANUP=COMPLETE',
    )
    for needle in required:
        if needle not in text:
            raise SystemExit(f'XRES_RAW_V2_PATCH_REFUSED=MISSING:{needle}')
    forbidden = (
        INHERITED_TASK_ID,
        'libxcb-res.so.0',
        'libXRes.so',
        'runtime-registration.json',
        'canonical-live-runtime',
    )
    present = [needle for needle in forbidden if needle in text]
    if present:
        raise SystemExit(f'XRES_RAW_V2_PATCH_REFUSED=FORBIDDEN:{present}')
    return text


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit('usage: xres-raw-pid-identity-v2-patch.py INPUT OUTPUT')
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    result = patch(src.read_text(encoding='utf-8'))
    dst.write_text(result, encoding='utf-8')
    print(f'XRES_RAW_V2_TASK_OWNER={TASK_ID}')
    print('XRES_RAW_V2_PATCH=PASS')
    print('XRES_RAW_V2_T35_ONLY=true')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
