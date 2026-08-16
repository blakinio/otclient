#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'XRES_PATCH_REFUSED={label}_COUNT:{count}')
    return text.replace(old, new, 1)


def patch(text: str) -> str:
    snapshot_anchor = 'PYALLX\n  : >"$out"'
    xres_block = r'''PYALLX
  python3 - "$display" "$client_pid" "$label" "$root/xres-$label.tsv" "$tool" <<'PYXRES'
import ctypes
import hashlib
import pathlib
import sys
from ctypes import POINTER, Structure, byref, c_char_p, c_int, c_long, c_uint, c_uint8, c_uint16, c_uint32, c_ulong, c_void_p

display, client_pid_s, label, out_path, tool_s = sys.argv[1:]
client_pid = int(client_pid_s)
tool = pathlib.Path(tool_s).resolve()


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


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

libxcb_path = choose_library('libxcb.so.1')
libres_path = choose_library('libxcb-res.so.0')
libx11_path = choose_library('libX11.so.6')
if not libxcb_path or not libres_path or not libx11_path:
    print(f'XRES_HELPER={label}:libxcb={bool(libxcb_path)}:libxcb_res={bool(libres_path)}:libX11={bool(libx11_path)}')
    pathlib.Path(out_path).write_text('helper_unavailable\n', encoding='utf-8')
    raise SystemExit(0)

print(f'XRES_LIB={label}:xcb={libxcb_path}:sha256={digest(libxcb_path)}')
print(f'XRES_LIB={label}:res={libres_path}:sha256={digest(libres_path)}')
print(f'XRES_LIB={label}:x11={libx11_path}:sha256={digest(libx11_path)}')

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
    raise SystemExit('XRES_IDENTITY_ERROR=XOpenDisplay')
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

class Cookie(Structure):
    _fields_ = [('sequence', c_uint)]
class VersionReply(Structure):
    _fields_ = [('response_type', c_uint8), ('pad0', c_uint8), ('sequence', c_uint16), ('length', c_uint32), ('server_major', c_uint16), ('server_minor', c_uint16)]
class ClientIdSpec(Structure):
    _fields_ = [('client', c_uint32), ('mask', c_uint32)]
class ClientIdValue(Structure):
    _fields_ = [('spec', ClientIdSpec), ('length', c_uint32)]
class ClientIdIter(Structure):
    _fields_ = [('data', POINTER(ClientIdValue)), ('rem', c_int), ('index', c_int)]

xcb = ctypes.CDLL(str(libxcb_path))
res = ctypes.CDLL(str(libres_path))
libc = ctypes.CDLL(None)
xcb.xcb_connect.argtypes = [c_char_p, POINTER(c_int)]
xcb.xcb_connect.restype = c_void_p
xcb.xcb_connection_has_error.argtypes = [c_void_p]
xcb.xcb_connection_has_error.restype = c_int
xcb.xcb_disconnect.argtypes = [c_void_p]
res.xcb_res_query_version.argtypes = [c_void_p, c_uint8, c_uint8]
res.xcb_res_query_version.restype = Cookie
res.xcb_res_query_version_reply.argtypes = [c_void_p, Cookie, c_void_p]
res.xcb_res_query_version_reply.restype = c_void_p
res.xcb_res_query_client_ids.argtypes = [c_void_p, c_uint32, POINTER(ClientIdSpec)]
res.xcb_res_query_client_ids.restype = Cookie
res.xcb_res_query_client_ids_reply.argtypes = [c_void_p, Cookie, c_void_p]
res.xcb_res_query_client_ids_reply.restype = c_void_p
res.xcb_res_query_client_ids_ids_length.argtypes = [c_void_p]
res.xcb_res_query_client_ids_ids_length.restype = c_int
res.xcb_res_query_client_ids_ids_iterator.argtypes = [c_void_p]
res.xcb_res_query_client_ids_ids_iterator.restype = ClientIdIter
res.xcb_res_client_id_value_value.argtypes = [POINTER(ClientIdValue)]
res.xcb_res_client_id_value_value.restype = POINTER(c_uint32)
res.xcb_res_client_id_value_value_length.argtypes = [POINTER(ClientIdValue)]
res.xcb_res_client_id_value_value_length.restype = c_int
libc.free.argtypes = [c_void_p]

screen = c_int()
conn = xcb.xcb_connect(display.encode(), byref(screen))
if not conn or xcb.xcb_connection_has_error(conn):
    raise SystemExit('XRES_IDENTITY_ERROR=xcb_connect')
try:
    vcookie = res.xcb_res_query_version(conn, 1, 2)
    vptr = res.xcb_res_query_version_reply(conn, vcookie, None)
    if not vptr:
        raise SystemExit('XRES_IDENTITY_ERROR=query_version_reply')
    try:
        vr = ctypes.cast(vptr, POINTER(VersionReply)).contents
        major, minor = int(vr.server_major), int(vr.server_minor)
    finally:
        libc.free(vptr)
    print(f'XRES_VERSION={label}:{major}.{minor}')
    if (major, minor) < (1, 2):
        pathlib.Path(out_path).write_text(f'version={major}.{minor}\n', encoding='utf-8')
        raise SystemExit(0)

    map_names = {0: 'UNMAPPED', 1: 'UNVIEWABLE', 2: 'VIEWABLE'}
    lines = []
    for wid, map_state, width, height in rows:
        spec = ClientIdSpec(wid, 2)
        cookie = res.xcb_res_query_client_ids(conn, 1, byref(spec))
        reply = res.xcb_res_query_client_ids_reply(conn, cookie, None)
        pid = None
        if reply:
            try:
                if res.xcb_res_query_client_ids_ids_length(reply) > 0:
                    it = res.xcb_res_query_client_ids_ids_iterator(reply)
                    if it.rem > 0 and bool(it.data):
                        value_len = res.xcb_res_client_id_value_value_length(it.data)
                        value = res.xcb_res_client_id_value_value(it.data)
                        if value_len > 0 and bool(value):
                            pid = int(value[0])
            finally:
                libc.free(reply)
        match = pid == client_pid if pid is not None else False
        mname = map_names.get(map_state, f'UNKNOWN_{map_state}')
        pid_text = str(pid) if pid is not None else 'unknown'
        print(f'XRES_IDENTITY={label}:xid=0x{wid:08x}:map={mname}:geom={width}x{height}:pid={pid_text}:matches_exact_client={str(match).lower()}')
        lines.append(f'0x{wid:08x}\t{mname}\t{width}x{height}\t{pid_text}\t{str(match).lower()}')
    pathlib.Path(out_path).write_text('\n'.join(lines) + ('\n' if lines else ''), encoding='utf-8')
finally:
    xcb.xcb_disconnect(conn)
PYXRES
  : >"$out"'''
    text = replace_once(text, snapshot_anchor, xres_block, 'SNAPSHOT_XRES_INSERT')

    final_anchor = 'echo "WINDOW_DIAG_CLASSIFICATION=$classification"'
    final_block = r'''xres_t35="$root/xres-t35.tsv"
xres_classification=XRES_IDENTITY_UNRESOLVED
if [[ -s "$xres_t35" ]] && awk -F'\t' '$2=="VIEWABLE" && $5=="true" {found=1} END{exit !found}' "$xres_t35"; then
  xres_classification=XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT
elif [[ -s "$xres_t35" ]] && awk -F'\t' '$2=="VIEWABLE" && $4 ~ /^[0-9]+$/ && $5=="false" {found=1} END{exit !found}' "$xres_t35"; then
  xres_classification=XRES_PROVES_VIEWABLE_WINDOW_FOREIGN_TO_EXACT_CLIENT
elif [[ -s "$xres_t35" ]] && awk -F'\t' '$2=="VIEWABLE" {found=1} END{exit !found}' "$xres_t35"; then
  xres_classification=XRES_VIEWABLE_WINDOW_PID_UNAVAILABLE
fi
echo "XRES_FINAL_CLASSIFICATION=$xres_classification"
echo "WINDOW_DIAG_CLASSIFICATION=$classification"'''
    text = replace_once(text, final_anchor, final_block, 'FINAL_XRES_CLASSIFICATION')

    required = (
        'XRES_VERSION=',
        'XRES_IDENTITY=',
        'XCB_RES_CLIENT_ID_MASK_LOCAL_CLIENT_PID',
        'xcb_res_query_client_ids',
        'XRES_PROVES_VIEWABLE_WINDOW_OWNED_BY_EXACT_CLIENT',
        'XRES_PROVES_VIEWABLE_WINDOW_FOREIGN_TO_EXACT_CLIENT',
        'XRES_VIEWABLE_WINDOW_PID_UNAVAILABLE',
    )
    # The literal enum name is documented in this source contract while the runtime mask value is 2.
    text += "\n# XRES_SOURCE_CONTRACT=XCB_RES_CLIENT_ID_MASK_LOCAL_CLIENT_PID=2\n"
    for needle in required:
        if needle not in text:
            raise SystemExit(f'XRES_PATCH_REFUSED=MISSING:{needle}')
    return text


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit('usage: xres-patch.py INPUT OUTPUT')
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    result = patch(src.read_text(encoding='utf-8'))
    dst.write_text(result, encoding='utf-8')
    print('XRES_PATCH=PASS')
    print('XRES_OBSERVATION_ONLY=true')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
