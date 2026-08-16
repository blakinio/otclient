#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

SOURCE_BLOB = "1616edcc982be50ef2c95b8077160ec8fe9291fe"
TASK = "OTC-20260816-track-a-canonical-runtime-e2e"
EXACT_CLIENT_SHA = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
XVFB_SHA = "2c7f5a9534410fed5092d782a69ca7ffd9fce80e98b81ffe4944d703dd11d3b1"
SWRAST_SHA = "c28638b02783ebc96a78bb982fe59ad0d54230bc1faf53305af33edab29cd388"


def replace_once(script: str, old: str, new: str, label: str) -> str:
    count = script.count(old)
    if count != 1:
        raise SystemExit(f"POST_RHI_TRANSFORM_REFUSED={label}_COUNT:{count}")
    return script.replace(old, new, 1)


def extract_run_block(data: bytes) -> str:
    lines = data.decode().splitlines()
    marker = "      - name: Reproduce isolated startup and inventory task-owned windows"
    try:
        step = lines.index(marker)
    except ValueError:
        raise SystemExit("POST_RHI_TRANSFORM_REFUSED=SOURCE_STEP_MISSING")
    run_index = None
    for idx in range(step + 1, len(lines)):
        if lines[idx].strip() == "run: |":
            run_index = idx
            break
        if lines[idx].startswith("      - name:"):
            break
    if run_index is None:
        raise SystemExit("POST_RHI_TRANSFORM_REFUSED=SOURCE_RUN_BLOCK_MISSING")
    run_indent = len(lines[run_index]) - len(lines[run_index].lstrip(" "))
    content_indent = None
    block: list[str] = []
    for line in lines[run_index + 1 :]:
        if not line.strip():
            block.append("")
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent <= run_indent:
            break
        if content_indent is None:
            content_indent = indent
        if indent < content_indent:
            raise SystemExit("POST_RHI_TRANSFORM_REFUSED=INCONSISTENT_BLOCK_INDENT")
        block.append(line[content_indent:])
    return "\n".join(block) + "\n"


def transform(data: bytes) -> str:
    actual_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if actual_blob != SOURCE_BLOB:
        raise SystemExit(f"POST_RHI_TRANSFORM_REFUSED=SOURCE_BLOB_MISMATCH:{actual_blob}")
    script = extract_run_block(data)

    script = replace_once(
        script,
        'local label="$1" out="$root/windows-$label.tsv" pids="$root/pids-$label.txt"',
        'local label="$1"\n  local out="$root/windows-$label.tsv"\n  local pids="$root/pids-$label.txt"',
        "SNAPSHOT_LOCAL",
    )
    script = replace_once(
        script,
        "task='OTC-20260816-track-a-client-window-ownership-discriminator'",
        f"task='{TASK}'",
        "TASK_ID",
    )
    script = replace_once(
        script,
        "'QT_XCB_GL_INTEGRATION': 'none',",
        "'QSG_INFO': '1',\n              'QT_DEBUG_PLUGINS': '1',",
        "GRAPHICS_ENV",
    )
    script = replace_once(
        script,
        "tool='/work/_otclient_tibia_re_state/toolroot'",
        "tool='/work/_otclient_tibia_re_state/toolroot'\n"
        'dri="$tool/usr/lib/x86_64-linux-gnu/dri"\n'
        'swrast="$dri/swrast_dri.so"\n'
        f"xvfb_support_sha='{XVFB_SHA}'\n"
        f"swrast_support_sha='{SWRAST_SHA}'",
        "DRI_VARIABLES",
    )

    support_anchor = (
        '[[ -d "$tool/usr/share/X11/xkb" && ! -L "$tool/usr/share/X11/xkb" ]] '
        "|| { echo 'WINDOW_DIAG_REFUSED=XKBROOT'; exit 46; }"
    )
    support_patch = support_anchor + r'''
[[ "$(sha256sum "$tool/usr/bin/Xvfb" | awk '{print $1}')" == "$xvfb_support_sha" ]] || { echo 'POST_RHI_REFUSED=XVFB_SHA'; exit 46; }
[[ -d "$dri" && ! -L "$dri" && "$(realpath -e "$dri")" == "$dri" ]] || { echo 'POST_RHI_REFUSED=DRI_ROOT'; exit 46; }
[[ -e "$swrast" ]] || { echo 'POST_RHI_REFUSED=SWRAST_MISSING'; exit 46; }
swrast_real="$(realpath -e "$swrast")" || { echo 'POST_RHI_REFUSED=SWRAST_REALPATH'; exit 46; }
case "$swrast_real" in "$dri"/*) ;; *) echo 'POST_RHI_REFUSED=SWRAST_ESCAPE'; exit 46 ;; esac
[[ -f "$swrast_real" ]] || { echo 'POST_RHI_REFUSED=SWRAST_NOT_FILE'; exit 46; }
[[ "$(sha256sum "$swrast" | awk '{print $1}')" == "$swrast_support_sha" ]] || { echo 'POST_RHI_REFUSED=SWRAST_SHA'; exit 46; }
[[ -e "$tool/usr/lib/x86_64-linux-gnu/libX11.so.6" ]] || { echo 'POST_RHI_REFUSED=LIBX11'; exit 46; }
echo 'POST_RHI_SUPPORT_FENCE=PASS'
echo "POST_RHI_DRI_PATH=$dri"
echo "POST_RHI_SWRAST_REAL=$swrast_real"'''
    script = replace_once(script, support_anchor, support_patch, "SUPPORT_ANCHOR")

    xkb_token = 'XKB_CONFIG_ROOT="$tool/usr/share/X11/xkb"'
    script = replace_once(
        script,
        xkb_token,
        'LIBGL_DRIVERS_PATH="$dri" XKB_CONFIG_ROOT="$tool/usr/share/X11/xkb"',
        "XVFB_DRI_ENV",
    )

    xvfb_anchor = "echo 'WINDOW_DIAG_XVFB=PASS'\n"
    x11_extension_probe = r'''echo 'WINDOW_DIAG_XVFB=PASS'
python3 - "$display_number" <<'PYXEXT'
import socket, struct, sys
n=int(sys.argv[1]); s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(3.0); s.connect(f'/tmp/.X11-unix/X{n}')
def rx(k):
    b=b''
    while len(b)<k:
        c=s.recv(k-len(b))
        if not c: raise SystemExit('POST_RHI_X11_ERROR=unexpected_eof')
        b+=c
    return b
s.sendall(struct.pack('<BBHHHHH',ord('l'),0,11,0,0,0,0)); h=rx(8); body=rx(struct.unpack_from('<H',h,6)[0]*4)
if h[0]!=1: raise SystemExit('POST_RHI_X11_ERROR=setup_failed')
s.sendall(struct.pack('<BBH',99,0,1)); r=rx(32); payload=rx(struct.unpack_from('<I',r,4)[0]*4)
names=[]; off=0
for _ in range(r[1]):
    ln=payload[off]; off+=1; names.append(payload[off:off+ln].decode('ascii','replace')); off+=ln
def q(name):
    raw=name.encode(); pad=(-len(raw))%4; length=(8+len(raw)+pad)//4
    s.sendall(struct.pack('<BBHHH',98,0,length,len(raw),0)+raw+b'\0'*pad); rep=rx(32); return bool(rep[8]),int(rep[9])
glx,go=q('GLX'); render,ro=q('RENDER')
print(f'POST_RHI_X11_EXTENSION_COUNT={len(names)}')
print(f'POST_RHI_X11_GLX_PRESENT={str(glx).lower()}')
print(f'POST_RHI_X11_GLX_MAJOR_OPCODE={go if glx else 0}')
print(f'POST_RHI_X11_RENDER_PRESENT={str(render).lower()}')
print(f'POST_RHI_X11_RENDER_MAJOR_OPCODE={ro if render else 0}')
s.close()
PYXEXT
'''
    script = replace_once(script, xvfb_anchor, x11_extension_probe, "X11_EXTENSION_ANCHOR")

    process_anchor = '    descendant_pids | sort -nu >"$pids"\n    while read -r pid; do'
    thread_patch = r'''    descendant_pids | sort -nu >"$pids"
    python3 - "$client_pid" "$label" <<'PYTHREADS'
import pathlib,re,sys
pid=sys.argv[1]; label=sys.argv[2]
root=pathlib.Path('/proc')/pid/'task'
threads=[]
if root.is_dir():
    for entry in sorted(root.iterdir(), key=lambda p: int(p.name) if p.name.isdigit() else 10**12):
        if not entry.name.isdigit(): continue
        try:
            stat=(entry/'stat').read_text(errors='replace').split()
            state=stat[2] if len(stat)>2 else 'unknown'
            comm=(entry/'comm').read_text(errors='replace').strip()
            wchan=(entry/'wchan').read_text(errors='replace').strip()
        except OSError:
            continue
        safe=lambda s: re.sub(r'[^A-Za-z0-9_+./:-]','?',s)[:120]
        threads.append((entry.name,state,safe(comm),safe(wchan)))
        if len(threads)>=64: break
print(f'POST_RHI_THREAD_COUNT={label}:{len(threads)}')
for tid,state,comm,wchan in threads:
    print(f'POST_RHI_THREAD={label}:tid={tid}:state={state}:comm={comm}:wchan={wchan}')
PYTHREADS
    while read -r pid; do'''
    script = replace_once(script, process_anchor, thread_patch, "THREAD_ANCHOR")

    allx_anchor = '    done <"$pids"\n    : >"$out"'
    allx_patch = r'''    done <"$pids"
    python3 - "$display" "$tool/usr/lib/x86_64-linux-gnu/libX11.so.6" "$tool/usr/bin/xdotool" "$pids" "$label" "$root/allx-$label.summary" <<'PYALLX'
import ctypes, os, pathlib, re, subprocess, sys
from ctypes import POINTER, Structure, byref, c_int, c_long, c_uint, c_ulong, c_void_p

display, libpath, xdotool, pids_path, label, summary_path = sys.argv[1:]
owned_pids=set()
try:
    owned_pids={int(x) for x in pathlib.Path(pids_path).read_text().split() if x.isdigit()}
except OSError:
    pass
lib=ctypes.CDLL(libpath)
lib.XOpenDisplay.argtypes=[ctypes.c_char_p]; lib.XOpenDisplay.restype=c_void_p
lib.XDefaultRootWindow.argtypes=[c_void_p]; lib.XDefaultRootWindow.restype=c_ulong
lib.XQueryTree.argtypes=[c_void_p,c_ulong,POINTER(c_ulong),POINTER(c_ulong),POINTER(POINTER(c_ulong)),POINTER(c_uint)]; lib.XQueryTree.restype=c_int
lib.XFree.argtypes=[c_void_p]; lib.XFree.restype=c_int
class Attr(Structure):
    _fields_=[('x',c_int),('y',c_int),('width',c_int),('height',c_int),('border_width',c_int),('depth',c_int),('visual',c_void_p),('root',c_ulong),('win_class',c_int),('bit_gravity',c_int),('win_gravity',c_int),('backing_store',c_int),('backing_planes',c_ulong),('backing_pixel',c_ulong),('save_under',c_int),('colormap',c_ulong),('map_installed',c_int),('map_state',c_int),('all_event_masks',c_long),('your_event_mask',c_long),('do_not_propagate_mask',c_long),('override_redirect',c_int),('screen',c_void_p)]
lib.XGetWindowAttributes.argtypes=[c_void_p,c_ulong,POINTER(Attr)]; lib.XGetWindowAttributes.restype=c_int

dpy=lib.XOpenDisplay(display.encode())
if not dpy: raise SystemExit('POST_RHI_ALLX_ERROR=XOpenDisplay')
root=lib.XDefaultRootWindow(dpy)
rows=[]; seen={int(root)}
def walk(parent, depth):
    if depth>6 or len(rows)>=120: return
    root_ret=c_ulong(); parent_ret=c_ulong(); children=POINTER(c_ulong)(); n=c_uint()
    if not lib.XQueryTree(dpy,c_ulong(parent),byref(root_ret),byref(parent_ret),byref(children),byref(n)):
        return
    try:
        for i in range(min(int(n.value),120-len(rows))):
            wid=int(children[i])
            if wid in seen: continue
            seen.add(wid); a=Attr()
            if lib.XGetWindowAttributes(dpy,c_ulong(wid),byref(a)):
                rows.append((wid,depth,a.map_state,a.x,a.y,a.width,a.height,a.override_redirect))
            walk(wid,depth+1)
            if len(rows)>=120: break
    finally:
        if children: lib.XFree(children)
walk(int(root),1)

env=dict(os.environ); env['DISPLAY']=display
def cmd(args):
    try:
        r=subprocess.run([xdotool,*args],env=env,text=True,capture_output=True,timeout=2,check=False)
        return r.stdout.strip() if r.returncode==0 else ''
    except Exception:
        return ''
def safe(text):
    text=re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}','<redacted-email>',text)
    text=re.sub(r'(?i)((?:password|token|authorization|cookie|session)[^=:\s]{0,20}[=:]\s*)\S+',r'\1<redacted>',text)
    text=''.join(ch if ch.isprintable() else '?' for ch in text).replace(':',';')
    return text[:140]
map_names={0:'UNMAPPED',1:'UNVIEWABLE',2:'VIEWABLE'}
counts={'total':len(rows),'viewable':0,'unviewable':0,'unmapped':0,'owned':0,'owned_viewable':0}
for wid,depth,map_state,x,y,w,h,override in rows:
    m=map_names.get(map_state,f'UNKNOWN_{map_state}')
    if map_state==2: counts['viewable']+=1
    elif map_state==1: counts['unviewable']+=1
    elif map_state==0: counts['unmapped']+=1
    ptxt=cmd(['getwindowpid',str(wid)])
    pid=int(ptxt) if ptxt.isdigit() else None
    owned=pid in owned_pids if pid is not None else False
    if owned:
        counts['owned']+=1
        if map_state==2: counts['owned_viewable']+=1
    title=safe(cmd(['getwindowname',str(wid)]))
    klass=safe(cmd(['getwindowclassname',str(wid)]))
    print(f'POST_RHI_X11_WINDOW={label}:id={wid}:depth={depth}:map={m}:pid={pid if pid is not None else "unknown"}:owned={str(owned).lower()}:override={override}:geom={w}x{h}+{x}+{y}:title={title}:class={klass}')
print('POST_RHI_X11_TREE_COUNTS='+label+':' + ':'.join(f'{k}={v}' for k,v in counts.items()))
pathlib.Path(summary_path).write_text('\n'.join(f'{k}={v}' for k,v in counts.items())+'\n')
PYALLX
    : >"$out"'''
    script = replace_once(script, allx_anchor, allx_patch, "ALL_X11_ANCHOR")

    old_filter = "chosen=lines[:40] + (['...<middle omitted>...'] if len(lines)>120 else []) + (lines[-80:] if len(lines)>40 else [])"
    broad_filter = "chosen=[line for line in lines if re.search(r'(?i)(QQml|QML|QtQuick|QQuick|QWindow|QPlatformWindow|window|scenegraph|QSG|QRhi|Vulkan|xcb|GLX|EGL|surface|swapchain|present|render|warning|error|failed|fatal|cannot|screen)', line)]"
    script = replace_once(script, old_filter, broad_filter, "LOG_FILTER")
    old_count = "print(f'WINDOW_DIAG_CLIENT_LOG_TOTAL_LINES={len(lines)}')"
    new_count = "print(f'POST_RHI_CLIENT_LOG_FILTER_MATCHES={seen}')\nprint(f'WINDOW_DIAG_CLIENT_LOG_TOTAL_LINES={len(lines)}')"
    script = replace_once(script, old_count, new_count, "LOG_COUNT")

    old_final = r'''final="$root/windows-t35.tsv"
if ! exact_client_alive; then
  classification=CLIENT_EXITED_WITHIN_35S
elif awk -F'\t' '$3=="true" && $4=="launched_pid" && $5=="Tibia" {found=1} END{exit !found}' "$final"; then
  classification=LAUNCHED_PID_TIBIA_WINDOW_FOUND
elif awk -F'\t' '$3=="true" && $4=="owned_descendant" {found=1} END{exit !found}' "$final"; then
  classification=OWNED_DESCENDANT_VISIBLE_WINDOW_FOUND
elif awk -F'\t' '$3=="true" {found=1} END{exit !found}' "$final"; then
  classification=LAUNCHED_RUNTIME_VISIBLE_WINDOW_DIFFERENT_TITLE_OR_CLASS
elif [[ -s "$final" ]]; then
  classification=VISIBLE_WINDOW_FOREIGN_TO_TASK_NAMESPACE
else
  classification=CLIENT_ALIVE_NO_VISIBLE_WINDOWS_ON_ISOLATED_DISPLAY
fi'''
    new_final = r'''final="$root/windows-t35.tsv"
summary="$root/allx-t35.summary"
total_nonroot="$(sed -n 's/^total=//p' "$summary" 2>/dev/null || true)"
viewable_nonroot="$(sed -n 's/^viewable=//p' "$summary" 2>/dev/null || true)"
owned_nonroot="$(sed -n 's/^owned=//p' "$summary" 2>/dev/null || true)"
owned_viewable="$(sed -n 's/^owned_viewable=//p' "$summary" 2>/dev/null || true)"
total_nonroot="${total_nonroot:-0}"; viewable_nonroot="${viewable_nonroot:-0}"; owned_nonroot="${owned_nonroot:-0}"; owned_viewable="${owned_viewable:-0}"
if ! exact_client_alive; then
  classification=CLIENT_EXITED_BEFORE_DISCRIMINATOR
elif (( owned_viewable > 0 )); then
  classification=TASK_OWNED_X11_WINDOW_VIEWABLE
elif (( owned_nonroot > 0 )); then
  classification=TASK_OWNED_X11_WINDOW_PRESENT_BUT_NOT_VIEWABLE
elif (( total_nonroot == 0 )); then
  classification=NO_NONROOT_X11_WINDOWS_CREATED
elif (( viewable_nonroot == 0 )); then
  classification=NONROOT_X11_WINDOWS_PRESENT_NONE_VIEWABLE
else
  classification=NONROOT_X11_WINDOWS_PRESENT_NONE_TASK_PID_BOUND
fi
printf 'POST_RHI_FINAL_COUNTS=total=%s:viewable=%s:owned=%s:owned_viewable=%s\n' "$total_nonroot" "$viewable_nonroot" "$owned_nonroot" "$owned_viewable"'''
    script = replace_once(script, old_final, new_final, "FINAL_CLASSIFICATION")

    client_start = script.index('python3 - "$root/client.pid"')
    client_end = script.index('client_pid="$(cat "$root/client.pid")"', client_start)
    client_launch = script[client_start:client_end]
    if "LIBGL_DRIVERS_PATH" in client_launch:
        raise SystemExit("POST_RHI_TRANSFORM_REFUSED=DRI_ENV_LEAK_TO_CLIENT")

    required = [
        f"task='{TASK}'",
        "'QT_QUICK_BACKEND': 'software'",
        "'QSG_INFO': '1'",
        "'QT_DEBUG_PLUGINS': '1'",
        'LIBGL_DRIVERS_PATH="$dri"',
        "POST_RHI_SUPPORT_FENCE=PASS",
        "POST_RHI_X11_GLX_PRESENT=",
        "POST_RHI_THREAD_COUNT=",
        "POST_RHI_X11_TREE_COUNTS=",
        "POST_RHI_CLIENT_LOG_FILTER_MATCHES=",
        "NO_NONROOT_X11_WINDOWS_CREATED",
        "TASK_OWNED_X11_WINDOW_PRESENT_BUT_NOT_VIEWABLE",
        "start_new_session=True",
        "descendant_pids()",
        'sha256sum "/proc/$client_pid/exe"',
        "WINDOW_DIAG_CLEANUP=COMPLETE",
        EXACT_CLIENT_SHA,
    ]
    for needle in required:
        if needle not in script:
            raise SystemExit(f"POST_RHI_TRANSFORM_REFUSED=MISSING_FENCE:{needle}")
    forbidden = [
        "'QT_XCB_GL_INTEGRATION': 'none'",
        "+extension GLX",
        "/proc/*/environ",
        "glob('/proc/*')",
        "runtime-registration.json",
        "canonical-live-runtime",
        "TIBIA_TEST_EMAIL=",
        "TIBIA_TEST_PASSWORD=",
        "QSG_RHI_BACKEND",
    ]
    for needle in forbidden:
        if needle in script:
            raise SystemExit(f"POST_RHI_TRANSFORM_REFUSED=FORBIDDEN_SOURCE_SHAPE:{needle}")
    return script


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: transform.py SOURCE OUTPUT")
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    script = transform(source.read_bytes())
    output.write_text(script, encoding="utf-8")
    print(f"POST_RHI_SOURCE_BLOB=PASS:{SOURCE_BLOB}")
    print("POST_RHI_TRANSFORM=PASS")
    print("POST_RHI_CANONICAL_STATE_ACCESS=NONE")
    print("POST_RHI_RUNTIME_ACCESS=EPHEMERAL_ISOLATED")
    print("POST_RHI_CLIENT_ENV=QT_QUICK_BACKEND_software,QSG_INFO_1,QT_DEBUG_PLUGINS_1")
    print("POST_RHI_XVFB_NEW_INPUT=LIBGL_DRIVERS_PATH_ONLY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
