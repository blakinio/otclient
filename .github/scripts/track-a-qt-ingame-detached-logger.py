#!/usr/bin/env python3
import hashlib
import json
import os
import pathlib
import re
import shutil
import struct
import subprocess
import sys
import time

pid = int(sys.argv[1])
start_ticks = int(sys.argv[2])
expected_size = int(sys.argv[3])
expected_sha = sys.argv[4]
duration = int(sys.argv[5])
out_path = pathlib.Path(sys.argv[6])

GAME_VPTR = 0x30ADCE8
AUTH_VPTR = 0x30B5290
AUTH_OFF = 0x8D0
QPRIV_OFF = 0x8
QSTATE_OFF = 0xF0
QRUN = 2
PLAYER_VPTR = 0x30C2738
PRIMARY = (0x2F0, 0x2F4, 0x2F8)
MIRROR = (0x408, 0x40C, 0x410)
QT_SIZE = 394824
QT_SHA = "26f504ae723fa15c77e0c33a93a964a305c63577f2bed3f136c098b7b06921e8"

def ticks():
    raw = pathlib.Path(f"/proc/{pid}/stat").read_text(encoding="ascii")
    return int(raw[raw.rfind(")") + 2:].split()[19])

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def emit(event):
    event["epoch_ms"] = time.time_ns() // 1_000_000
    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")
        f.flush()

if ticks() != start_ticks:
    raise SystemExit("START_TICKS_MISMATCH")
exe = pathlib.Path(os.path.realpath(f"/proc/{pid}/exe"))
if exe.stat().st_size != expected_size or digest(exe) != expected_sha:
    raise SystemExit("EXACT_FENCE_MISMATCH")
qt = exe.parent / "lib" / "libQt6StateMachine.so.6"
if not qt.is_file() or qt.stat().st_size != QT_SIZE or digest(qt) != QT_SHA:
    raise SystemExit("QT_FENCE_MISMATCH")

regions = []
for line in pathlib.Path(f"/proc/{pid}/maps").read_text().splitlines():
    p = line.split(maxsplit=5)
    begin, end = (int(x, 16) for x in p[0].split("-"))
    regions.append((begin, end, p[1], int(p[2], 16), p[5] if len(p) == 6 else ""))
bases = [b - off for b, e, perms, off, path in regions if path == str(exe)]
if not bases:
    raise SystemExit("CLIENT_MAPPING_MISSING")
base = min(bases)
rw = [r for r in regions if r[2].startswith("rw") and 0 < r[1] - r[0] <= 768 * 1024 * 1024]
heap = [(b, e) for b, e, perms, off, path in regions if path == "[heap]" and perms.startswith("rw")]
if len(heap) != 1:
    raise SystemExit("HEAP_MAPPING_COUNT")

fd = os.open(f"/proc/{pid}/mem", os.O_RDONLY | os.O_CLOEXEC)

def scan_ranges(ranges, vptr, private_filter=False):
    pat = struct.pack("<Q", base + vptr)
    hits = []
    for begin, end in ranges:
        cur = begin
        tail = b""
        while cur < end:
            want = min(1024 * 1024, end - cur)
            try:
                data = os.pread(fd, want, cur)
            except OSError:
                cur += want
                tail = b""
                continue
            if not data:
                cur += want
                tail = b""
                continue
            merged = tail + data
            merged_base = cur - len(tail)
            pos = 0
            while True:
                idx = merged.find(pat, pos)
                if idx < 0:
                    break
                obj = merged_base + idx
                if obj % 8 == 0:
                    if not private_filter:
                        hits.append(obj)
                    else:
                        try:
                            private = struct.unpack("<Q", os.pread(fd, 8, obj + 8))[0]
                        except Exception:
                            private = 0
                        if any(b <= private < e for b, e, *_ in rw):
                            hits.append(obj)
                pos = idx + 1
            tail = merged[-7:]
            cur += len(data)
    return sorted(set(hits))

try:
    game_hits = scan_ranges(heap, GAME_VPTR)
    if len(game_hits) != 1:
        raise SystemExit("GAME_CLIENT_OBJECT_COUNT=" + str(len(game_hits)))
    game = game_hits[0]
    auth = struct.unpack("<Q", os.pread(fd, 8, game + AUTH_OFF))[0]
    if struct.unpack("<Q", os.pread(fd, 8, auth))[0] != base + AUTH_VPTR:
        raise SystemExit("AUTH_VPTR_MISMATCH")
    qpriv = struct.unpack("<Q", os.pread(fd, 8, auth + QPRIV_OFF))[0]
    player_hits = scan_ranges([(b, e) for b, e, *_ in rw], PLAYER_VPTR, True)
    if len(player_hits) != 1:
        raise SystemExit("PLAYER_OBJECT_COUNT=" + str(len(player_hits)))
    player = player_hits[0]

    def read_pos():
        primary = tuple(struct.unpack("<i", os.pread(fd, 4, player + off))[0] for off in PRIMARY)
        mirror = tuple(struct.unpack("<i", os.pread(fd, 4, player + off))[0] for off in MIRROR)
        valid = primary == mirror and 1 <= primary[0] <= 65535 and 1 <= primary[1] <= 65535 and 0 <= primary[2] <= 15
        return list(primary) if valid else None, primary == mirror

    ss = shutil.which("ss")
    rx_re = re.compile(r"bytes_received:(\d+)")
    tx_re = re.compile(r"bytes_acked:(\d+)")

    def network():
        if not ss:
            return {"source": "unavailable", "established": None, "tx_acked": None, "rx": None}
        try:
            cp = subprocess.run([ss, "-tinp"], text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=1)
        except (subprocess.TimeoutExpired, OSError):
            return {"source": "unavailable", "established": None, "tx_acked": None, "rx": None}
        lines = cp.stdout.splitlines()
        established = tx = rx = 0
        for i, line in enumerate(lines):
            if f"pid={pid}," not in line:
                continue
            if line.lstrip().startswith("ESTAB"):
                established += 1
            detail = lines[i + 1] if i + 1 < len(lines) else ""
            mt, mr = tx_re.search(detail), rx_re.search(detail)
            if mt:
                tx += int(mt.group(1))
            if mr:
                rx += int(mr.group(1))
        return {"source": "ss_tcp_info", "established": established, "tx_acked": tx, "rx": rx}

    def character_context():
        env = dict(os.environ)
        env["DISPLAY"] = ":1"
        try:
            cp = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "^Tibia"], text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=1, env=env)
            ids = [x for x in cp.stdout.split() if x.isdigit()]
            for xid in ids[:4]:
                title = subprocess.run(["xdotool", "getwindowname", xid], text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=1, env=env).stdout.strip()
                if title.startswith("Tibia - "):
                    return True
            return False
        except (subprocess.TimeoutExpired, OSError):
            return None

    out_path.write_text("", encoding="utf-8")
    emit({"event": "LOGGER_READY", "pid": pid, "start_ticks": start_ticks, "duration_seconds": duration, "credentials_retained": False, "packet_payloads_retained": False, "raw_window_titles_retained": False})
    started = time.monotonic()
    last = None
    while time.monotonic() - started < duration:
        if ticks() != start_ticks:
            raise SystemExit("START_TICKS_CHANGED")
        qraw = struct.unpack("<I", os.pread(fd, 4, qpriv + QSTATE_OFF))[0]
        pos, mirror_ok = read_pos()
        net = network()
        context = character_context()
        state = (qraw, tuple(pos) if pos else None, mirror_ok, net["established"], net["tx_acked"], net["rx"], context)
        if state != last:
            emit({"event": "STATE", "auth_qstate_raw": qraw, "auth_running": qraw == QRUN, "player_position": pos, "position_mirror_consistent": mirror_ok, "tcp": net, "character_context": context})
            last = state
        time.sleep(0.25)
    emit({"event": "LOGGER_DONE"})
finally:
    os.close(fd)
