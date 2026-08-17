#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

TASK_ID = "OTC-20260817-track-a-worldmap-mutation-physical-validation"
INHERITED_TASK_ID = "OTC-20260816-track-a-canonical-runtime-e2e"
PATCH_HELPER = ".github/scripts/tibia-official-client-re-worldmap-copy-patch.py"


class TransformRefused(RuntimeError):
    pass


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise TransformRefused(f"{label}_COUNT:{count}")
    return text.replace(old, new, 1)


def transform(text: str) -> str:
    text = replace_once(
        text,
        f"task='{INHERITED_TASK_ID}'",
        f"task='{TASK_ID}'",
        "TASK_OWNER",
    )
    if INHERITED_TASK_ID in text:
        raise TransformRefused("INHERITED_TASK_REMAINS")

    text = replace_once(
        text,
        "client_real=''",
        "client_real=''\nsupervisor_pid=''\npatched_sha=''",
        "SUPERVISOR_STATE",
    )
    text = replace_once(
        text,
        "cleanup_client_tree || true",
        'cleanup_client_tree || true\n  kill_owned "$supervisor_pid" observer || true',
        "SUPERVISOR_CLEANUP",
    )

    copied_fence = '''[[ "$(stat -c %s "$client")" == "$size" && "$(sha256sum "$client" | awk '{print $1}')" == "$sha" ]] || { echo 'WINDOW_DIAG_REFUSED=COPIED_CLIENT_FENCE'; exit 61; }'''
    patch_block = copied_fence + r'''
python3 "$GITHUB_WORKSPACE/.github/scripts/tibia-official-client-re-worldmap-copy-patch.py" \
  patch "$source_client" "$client" "$root/worldmap-patch-manifest.txt"
patched_sha="$(sed -n 's/^patched_sha256=//p' "$root/worldmap-patch-manifest.txt")"
patch_offset="$(sed -n 's/^file_offset=//p' "$root/worldmap-patch-manifest.txt")"
[[ "$patched_sha" =~ ^[0-9a-f]{64}$ && "$patched_sha" != "$sha" ]] || { echo 'WORLDMAP_REFUSED=PATCHED_SHA'; exit 61; }
[[ -n "$patch_offset" ]] || { echo 'WORLDMAP_REFUSED=PATCH_OFFSET'; exit 61; }
[[ "$(sha256sum "$source_client" | awk '{print $1}')" == "$sha" ]] || { echo 'WORLDMAP_REFUSED=SOURCE_CHANGED_AFTER_PATCH'; exit 61; }
echo "WORLDMAP_PATCHED_SHA256=$patched_sha"
echo "WORLDMAP_PATCH_FILE_OFFSET=$patch_offset"
echo 'WORLDMAP_PATCH_CANDIDATE=19,14'
echo 'WORLDMAP_PATCH_DIFF_BYTES=1' '''
    text = replace_once(text, copied_fence, patch_block, "COPY_PATCH_INSERT")

    launch_token = 'python3 - "$root/client.pid"'
    start = text.find(launch_token)
    if start < 0:
        raise TransformRefused("LAUNCH_START_MISSING")
    line_start = text.rfind("\n", 0, start) + 1
    end_token = 'client_pid="$(cat "$root/client.pid")"'
    end = text.find(end_token, start)
    if end < 0:
        raise TransformRefused("LAUNCH_END_MISSING")
    launch_prefix = text[line_start:start]
    if launch_prefix.strip():
        raise TransformRefused("LAUNCH_PREFIX_UNEXPECTED")

    supervisor = r'''env -u RUNNER_TRACKING_ID -u TIBIA_TEST_EMAIL -u TIBIA_TEST_PASSWORD \
  OTCLIENT_TIBIA_RE_DIAG_TASK="$task" OTCLIENT_TIBIA_RE_ROLE=observer \
  python3 - "$root/client.pid" "$root/client.log" "$root/memory.log" "$package" "$client" "$home" "$display" "$tool" "$preload" "$root/proxychains.conf" "$task" "$patched_sha" <<'PYWMSUP' \
  >"$root/supervisor.log" 2>&1 &
import os
import pathlib
import struct
import subprocess
import sys
import time

pidfile_s, logfile_s, memlog_s, cwd_s, client_s, home, display, tool, preload, proxyconf, task, patched_sha = sys.argv[1:]
pidfile = pathlib.Path(pidfile_s)
logfile = pathlib.Path(logfile_s)
memlog = pathlib.Path(memlog_s)
client_path = pathlib.Path(client_s).resolve()
package = pathlib.Path(cwd_s)
env = dict(os.environ)
for key in ('RUNNER_TRACKING_ID', 'TIBIA_TEST_EMAIL', 'TIBIA_TEST_PASSWORD'):
    env.pop(key, None)
env.update({
    'OTCLIENT_TIBIA_RE_DIAG_TASK': task,
    'OTCLIENT_TIBIA_RE_ROLE': 'client',
    'HOME': home,
    'DISPLAY': display,
    'PATH': f'{tool}/usr/bin:{tool}/usr/sbin:/usr/bin:/bin',
    'LD_LIBRARY_PATH': f'{package}/bin/lib:{tool}/usr/lib/x86_64-linux-gnu:{tool}/usr/lib/x86_64-linux-gnu/libproxy:{tool}/lib/x86_64-linux-gnu',
    'QT_QUICK_BACKEND': 'software',
    'QSG_INFO': '1',
    'QT_DEBUG_PLUGINS': '1',
    'XDG_DATA_DIRS': f'{tool}/usr/share:/usr/share',
    'FONTCONFIG_PATH': f'{tool}/etc/fonts',
    'FONTCONFIG_FILE': f'{tool}/etc/fonts/fonts.conf',
    'LD_PRELOAD': preload,
    'PROXYCHAINS_CONF_FILE': proxyconf,
})
with logfile.open('ab', buffering=0) as log:
    proc = subprocess.Popen(
        [str(client_path)], cwd=str(package), env=env, stdin=subprocess.DEVNULL,
        stdout=log, stderr=subprocess.STDOUT, start_new_session=True, close_fds=True,
    )
pidfile.write_text(str(proc.pid), encoding='ascii')

HANDLER_VPTR = 0x030871D8
STORAGE_VPTR = 0x0308CE70
VIEWPORT_VPTR = 0x0308C9A8
RENDER_VPTR = 0x02F6C258
PICKER_VPTR = 0x02F6B7C8
CAMERA_VPTR = 0x03083968


def log(line: str) -> None:
    with memlog.open('a', encoding='utf-8') as f:
        f.write(line + '\n')
        f.flush()


def elf_loads(path: pathlib.Path):
    with path.open('rb') as f:
        h = f.read(64)
        if len(h) != 64 or h[:4] != b'\x7fELF' or h[4] != 2 or h[5] != 1:
            raise RuntimeError('elf_shape')
        phoff = struct.unpack_from('<Q', h, 32)[0]
        entsz = struct.unpack_from('<H', h, 54)[0]
        num = struct.unpack_from('<H', h, 56)[0]
        out = []
        for i in range(num):
            f.seek(phoff + i * entsz)
            raw = f.read(56)
            if len(raw) != 56:
                raise RuntimeError('phdr_truncated')
            p_type, flags, off, va, _pa, filesz, memsz, align = struct.unpack('<IIQQQQQQ', raw)
            if p_type == 1:
                out.append((off, va, filesz, memsz, flags, align))
        return out


def parse_maps(pid: int):
    rows = []
    for line in pathlib.Path(f'/proc/{pid}/maps').read_text().splitlines():
        fields = line.split(None, 5)
        if len(fields) < 5:
            continue
        lo_s, hi_s = fields[0].split('-', 1)
        rows.append({
            'lo': int(lo_s, 16), 'hi': int(hi_s, 16), 'perms': fields[1],
            'offset': int(fields[2], 16), 'path': fields[5] if len(fields) > 5 else '',
        })
    return rows


def load_bias(pid: int, rows) -> int:
    page = os.sysconf('SC_PAGE_SIZE')
    real = str(client_path)
    loads = elf_loads(client_path)
    biases = []
    for row in rows:
        raw_path = row['path'].replace(' (deleted)', '')
        if not raw_path or raw_path.startswith('['):
            continue
        try:
            if os.path.realpath(raw_path) != real:
                continue
        except OSError:
            continue
        for off, va, _filesz, _memsz, _flags, _align in loads:
            off_page = off - (off % page)
            va_page = va - (va % page)
            if row['offset'] == off_page:
                biases.append(row['lo'] - va_page)
    if not biases or len(set(biases)) != 1:
        raise RuntimeError(f'load_bias:{sorted(set(biases))}')
    return biases[0]


def scan_vptr(memfd: int, rows, needle: int, max_matches: int = 24):
    target = struct.pack('<Q', needle)
    ranges = []
    total = 0
    for row in rows:
        if not row['perms'].startswith('rw'):
            continue
        path = row['path']
        if path and not path.startswith('['):
            continue
        size = row['hi'] - row['lo']
        if size <= 0 or size > 256 * 1024 * 1024:
            continue
        if total + size > 768 * 1024 * 1024:
            continue
        ranges.append((row['lo'], row['hi']))
        total += size
    matches = []
    chunk = 1024 * 1024
    for lo, hi in ranges:
        pos = lo
        carry = b''
        carry_addr = pos
        while pos < hi:
            n = min(chunk, hi - pos)
            try:
                data = os.pread(memfd, n, pos)
            except OSError:
                break
            blob = carry + data
            base = carry_addr if carry else pos
            search = 0
            while True:
                idx = blob.find(target, search)
                if idx < 0:
                    break
                addr = base + idx
                if addr % 8 == 0:
                    matches.append(addr)
                    if len(matches) >= max_matches:
                        return matches, len(ranges), total
                search = idx + 1
            carry = blob[-7:] if len(blob) >= 7 else blob
            carry_addr = pos + len(data) - len(carry)
            pos += len(data)
    return matches, len(ranges), total


def u32(memfd: int, addr: int):
    data = os.pread(memfd, 4, addr)
    return struct.unpack('<I', data)[0] if len(data) == 4 else None


def u64(memfd: int, addr: int):
    data = os.pread(memfd, 8, addr)
    return struct.unpack('<Q', data)[0] if len(data) == 8 else None


def snapshot(label: str) -> None:
    if proc.poll() is not None:
        log(f'WM_MEM_SNAPSHOT={label}:client_exited={proc.returncode}')
        return
    try:
        rows = parse_maps(proc.pid)
        bias = load_bias(proc.pid, rows)
        memfd = os.open(f'/proc/{proc.pid}/mem', os.O_RDONLY)
    except Exception as exc:
        log(f'WM_MEM_ACCESS_REFUSED={label}:{type(exc).__name__}:{str(exc)[:100]}')
        return
    try:
        targets = {
            'HANDLER': bias + HANDLER_VPTR,
            'STORAGE': bias + STORAGE_VPTR,
            'VIEWPORT': bias + VIEWPORT_VPTR,
            'RENDER': bias + RENDER_VPTR,
            'PICKER': bias + PICKER_VPTR,
            'CAMERA': bias + CAMERA_VPTR,
        }
        log(f'WM_MEM_SNAPSHOT={label}:pid={proc.pid}:load_bias=0x{bias:x}:patched_sha={patched_sha}')
        for kind, target in targets.items():
            matches, range_count, scan_bytes = scan_vptr(memfd, rows, target)
            log(f'WM_VPTR_COUNT={label}:{kind}:{len(matches)}:target=0x{target:x}:ranges={range_count}:bytes={scan_bytes}')
            for addr in matches:
                if kind == 'HANDLER':
                    x = u32(memfd, addr + 0xB0); y = u32(memfd, addr + 0xB4); sp = u64(memfd, addr + 0x10)
                    sv = u64(memfd, sp) if sp else None
                    sm = sv == targets['STORAGE'] if sv is not None else False
                    log(f'WM_HANDLER={label}:addr=0x{addr:x}:pair={x},{y}:member10=0x{(sp or 0):x}:member10_storage_vptr={str(sm).lower()}')
                elif kind == 'STORAGE':
                    x = u32(memfd, addr + 0x48); y = u32(memfd, addr + 0x4C)
                    log(f'WM_STORAGE={label}:addr=0x{addr:x}:pair={x},{y}')
                else:
                    log(f'WM_{kind}={label}:addr=0x{addr:x}')
    finally:
        os.close(memfd)

start = time.monotonic()
for target_s, label in ((1.0, 't01'), (5.0, 't05'), (15.0, 't15'), (35.0, 't35')):
    delay = target_s - (time.monotonic() - start)
    if delay > 0:
        time.sleep(delay)
    snapshot(label)
    if proc.poll() is not None:
        break
log('WM_MEM_DONE=1')
while proc.poll() is None:
    time.sleep(0.25)
PYWMSUP
supervisor_pid=$!
for _ in $(seq 1 80); do
  [[ -s "$root/client.pid" ]] && break
  kill -0 "$supervisor_pid" 2>/dev/null || { echo 'WORLDMAP_REFUSED=SUPERVISOR_EXITED_BEFORE_PID'; exit 66; }
  sleep .1
done
[[ -s "$root/client.pid" ]] || { echo 'WORLDMAP_REFUSED=CLIENT_PID_TIMEOUT'; exit 66; }
'''
    text = text[:line_start] + supervisor + text[end:]

    live_sha = '''[[ "$(sha256sum "/proc/$client_pid/exe" | awk '{print $1}')" == "$sha" ]] || { echo 'WINDOW_DIAG_REFUSED=LIVE_CLIENT_SHA'; exit 66; }'''
    live_patch_sha = '''[[ "$(sha256sum "/proc/$client_pid/exe" | awk '{print $1}')" == "$patched_sha" ]] || { echo 'WORLDMAP_REFUSED=LIVE_PATCHED_CLIENT_SHA'; exit 66; }
echo 'WORLDMAP_LIVE_PATCHED_PROCESS_FENCE=PASS' '''
    text = replace_once(text, live_sha, live_patch_sha, "LIVE_PATCHED_SHA")

    t35_anchor = "snapshot t35\n"
    t35_block = r'''snapshot t35
for _ in $(seq 1 80); do
  grep -Fxq 'WM_MEM_DONE=1' "$root/memory.log" 2>/dev/null && break
  sleep .25
done
if [[ -f "$root/memory.log" ]]; then
  echo '=== WORLDMAP_MEMORY_OBSERVER ==='
  cat "$root/memory.log"
fi
wm_structural=NO_HANDLER_CANARY_OBSERVED
if grep -Eq '^WM_HANDLER=.*:pair=19,14:' "$root/memory.log" 2>/dev/null; then
  wm_structural=HANDLER_CANARY_OBSERVED
  if grep -Eq '^WM_STORAGE=.*:pair=19,14$' "$root/memory.log" 2>/dev/null; then
    wm_structural=HANDLER_AND_STORAGE_CANARY_OBSERVED
  fi
fi
echo "WORLDMAP_STRUCTURAL_CLASSIFICATION=$wm_structural"
'''
    text = replace_once(text, t35_anchor, t35_block, "MEMORY_LOG_AFTER_T35")

    rm_anchor = 'rm -rf --one-file-system "$root" 2>/dev/null || true'
    rollback = r'''if [[ -n "${source_client:-}" && -f "$source_client" ]]; then
    current_source_sha="$(sha256sum "$source_client" 2>/dev/null | awk '{print $1}' || true)"
    if [[ "$current_source_sha" == "$sha" ]]; then
      echo 'WORLDMAP_ORIGINAL_SOURCE_REHASH=PASS'
    else
      echo "WORLDMAP_ORIGINAL_SOURCE_REHASH=FAIL:${current_source_sha:-missing}"
      rc=91
    fi
  fi
  rm -rf --one-file-system "$root" 2>/dev/null || true
  if [[ ! -e "$root" ]]; then echo 'WORLDMAP_PATCHED_COPY_REMOVED=PASS'; else echo 'WORLDMAP_PATCHED_COPY_REMOVED=FAIL'; rc=92; fi'''
    text = replace_once(text, rm_anchor, rollback, "ROLLBACK_REHASH")

    required = (
        f"task='{TASK_ID}'",
        PATCH_HELPER,
        "WORLDMAP_PATCH_CANDIDATE=19,14",
        "WORLDMAP_LIVE_PATCHED_PROCESS_FENCE=PASS",
        "WM_HANDLER=",
        "WM_STORAGE=",
        "WORLDMAP_STRUCTURAL_CLASSIFICATION=",
        "WORLDMAP_ORIGINAL_SOURCE_REHASH=PASS",
        "WORLDMAP_PATCHED_COPY_REMOVED=PASS",
        "WINDOW_DIAG_CLEANUP=COMPLETE",
    )
    missing = [x for x in required if x not in text]
    if missing:
        raise TransformRefused(f"MISSING:{missing}")
    forbidden = (
        INHERITED_TASK_ID,
        "runtime-registration.json",
        "canonical-live-runtime",
        "TIBIA_TEST_EMAIL=",
        "TIBIA_TEST_PASSWORD=",
        "+extension GLX",
        "QSG_RHI_BACKEND",
    )
    present = [x for x in forbidden if x in text]
    if present:
        raise TransformRefused(f"FORBIDDEN:{present}")
    return text


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: worldmap-mutation-transform.py INPUT OUTPUT")
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    try:
        result = transform(src.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_TRANSFORM_REFUSED={exc}")
        return 44
    dst.write_text(result, encoding="utf-8")
    print(f"WORLDMAP_TRANSFORM_TASK_OWNER={TASK_ID}")
    print("WORLDMAP_TRANSFORM=PASS")
    print("WORLDMAP_CANARY=19,14")
    print("WORLDMAP_PROCESS_MEMORY=READ_ONLY_TASK_PID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
