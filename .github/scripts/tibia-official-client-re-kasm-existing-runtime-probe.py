#!/usr/bin/env python3
"""Read-only proof for adopting the single exact official client in Track A KasmVNC."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Callable, Sequence

TARGET_CONTAINER = "otclient-track-a-kasmvnc"
TARGET_DISPLAY = ":1"
VER = "15.32.75d4a0"
SIZE = 52105824
SHA = "d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a"
PROOF_KIND = "existing_runtime_adoption_v1"
WINDOW_RE = re.compile(r'^\s*(0x[0-9a-fA-F]+)\s+"(Tibia(?: - .+)?)":')
BRIDGE_SOCKET = "/tmp/otclient-native-login-current-sha/bridge.sock"
BRIDGE_TARGETS = ("player_protocol_handler", "gameserver_game_session", "worldmap_handler")
BRIDGE_SCRIPT = r"""
import json, socket, struct, sys
path = sys.argv[1]
expected_pid = int(sys.argv[2])
commands = ["PING"] + ["DISCOVER " + name for name in sys.argv[3:]]
rows = []
for command in commands:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(12)
    sock.connect(path)
    peer_pid, _, _ = struct.unpack("3i", sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i")))
    if peer_pid != expected_pid:
        raise RuntimeError(f"bridge_peer_pid_mismatch:{peer_pid}!={expected_pid}")
    sock.sendall((command + "\n").encode())
    data = b""
    while b"\n" not in data and len(data) < 65536:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    sock.close()
    rows.append(json.loads(data.decode()))
print(json.dumps(rows, sort_keys=True, separators=(",", ":")))
"""


class ProbeError(RuntimeError):
    pass


def run(command: Sequence[str]) -> str:
    completed = subprocess.run(
        list(command), check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15
    )
    if completed.returncode:
        raise ProbeError(f"command_failed:{command[0]}:{completed.returncode}")
    return completed.stdout


def docker_containers(runner: Callable[[Sequence[str]], str] = run) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in runner(["docker", "ps", "--format", "{{.ID}}\t{{.Names}}"] ).splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        if len(parts) != 2:
            raise ProbeError("docker_inventory_malformed")
        rows.append((parts[0].strip(), parts[1].strip()))
    if not rows:
        raise ProbeError("docker_inventory_empty")
    return rows


def candidate_rows(container_id: str, runner: Callable[[Sequence[str]], str] = run) -> list[dict[str, Any]]:
    shell = r'''set -eu
for d in /proc/[0-9]*; do
  [ -r "$d/stat" ] || continue
  pid=${d#/proc/}
  comm=$(cat "$d/comm" 2>/dev/null || true)
  exe=$(readlink -f "$d/exe" 2>/dev/null || true)
  if [ -z "$exe" ]; then
    case "$comm" in
      client|Tibia*) printf '%s\tUNREADABLE\tUNREADABLE\tUNREADABLE\tUNREADABLE\n' "$pid"; continue ;;
      *) continue ;;
    esac
  fi
  base=${exe##*/}
  case "$base:$exe" in
    client:*|*:*Tibia*) ;;
    *) continue ;;
  esac
  size=$(stat -Lc %s "$d/exe" 2>/dev/null || echo UNREADABLE)
  sha=$(sha256sum "$d/exe" 2>/dev/null | awk '{print $1}' || true)
  [ -n "$sha" ] || sha=UNREADABLE
  start=$(awk '{print $22}' "$d/stat" 2>/dev/null || echo UNREADABLE)
  printf '%s\t%s\t%s\t%s\t%s\n' "$pid" "$exe" "$size" "$sha" "$start"
done'''
    output = runner(["docker", "exec", container_id, "sh", "-lc", shell])
    rows: list[dict[str, Any]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 5:
            raise ProbeError("candidate_inventory_malformed")
        pid_s, exe, size_s, sha, start_s = parts
        if not (pid_s.isdigit() and size_s.isdigit() and start_s.isdigit()) or sha == "UNREADABLE":
            raise ProbeError("candidate_unverifiable")
        rows.append({"pid": int(pid_s), "exe": exe, "size": int(size_s), "sha256": sha, "start_ticks": int(start_s)})
    return rows


def target_runtime(container_id: str, pid: int, runner: Callable[[Sequence[str]], str] = run) -> dict[str, Any]:
    shell = f'''set -eu
pid={pid}
test -r /proc/$pid/stat
exe=$(readlink -f /proc/$pid/exe)
size=$(stat -Lc %s /proc/$pid/exe)
sha=$(sha256sum /proc/$pid/exe | awk '{{print $1}}')
start=$(awk '{{print $22}}' /proc/$pid/stat)
boot=$(sha256sum /proc/sys/kernel/random/boot_id | awk '{{print $1}}')
printf 'EXE=%s\nSIZE=%s\nSHA=%s\nSTART=%s\nBOOT=%s\n' "$exe" "$size" "$sha" "$start" "$boot"
'''
    values: dict[str, str] = {}
    for line in runner(["docker", "exec", container_id, "sh", "-lc", shell]).splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    required = {"EXE", "SIZE", "SHA", "START", "BOOT"}
    if not required.issubset(values) or not values["SIZE"].isdigit() or not values["START"].isdigit():
        raise ProbeError("target_identity_incomplete")
    return {
        "exe": values["EXE"], "size": int(values["SIZE"]), "sha256": values["SHA"],
        "start_ticks": int(values["START"]), "boot_id_sha256": values["BOOT"],
    }


def window_proof(container_id: str, pid: int, runner: Callable[[Sequence[str]], str] = run) -> str:
    prefix = ["docker", "exec", "-u", "kasm-user", "-e", f"DISPLAY={TARGET_DISPLAY}", container_id, "sh", "-lc"]
    tree = runner(prefix + ["xwininfo -root -tree"])
    title_candidates: list[tuple[str, str]] = []
    for line in tree.splitlines():
        match = WINDOW_RE.match(line)
        if match:
            title_candidates.append((match.group(1), match.group(2)))
    owned: list[tuple[str, str]] = []
    class_pid_mismatch = False
    for window_id, title in title_candidates:
        props = runner(prefix + [f"xprop -id {window_id} _NET_WM_PID WM_CLASS"])
        if '"client"' not in props or '"Tibia"' not in props:
            continue
        pid_match = re.search(r"_NET_WM_PID\(CARDINAL\) = (\d+)", props)
        if not pid_match:
            raise ProbeError("window_pid_missing")
        if int(pid_match.group(1)) != pid:
            class_pid_mismatch = True
            continue
        owned.append((window_id, title))
    if len(owned) != 1:
        if not owned and class_pid_mismatch:
            raise ProbeError("window_pid_mismatch")
        raise ProbeError(f"main_window_count:{len(owned)}")
    window_id, title = owned[0]
    title_hash = hashlib.sha256(title.encode()).hexdigest()
    return f"x11:{window_id}:pid:{pid}:class:client/Tibia:title_sha256:{title_hash}"


def structural_state(container_id: str, pid: int, runtime: dict[str, Any], runner: Callable[[Sequence[str]], str] = run) -> tuple[str, str]:
    present = runner(["docker", "exec", container_id, "sh", "-lc", f"if [ -S {BRIDGE_SOCKET} ]; then echo PRESENT; else echo ABSENT; fi"]).strip()
    if present == "ABSENT":
        return "UNKNOWN", "NO_STRUCTURAL_BRIDGE"
    if present != "PRESENT":
        raise ProbeError("bridge_presence_invalid")
    raw = runner(["docker", "exec", container_id, "python3", "-c", BRIDGE_SCRIPT, BRIDGE_SOCKET, str(pid), *BRIDGE_TARGETS])
    try:
        rows = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProbeError("bridge_result_invalid_json") from exc
    if not isinstance(rows, list) or len(rows) != 4:
        raise ProbeError("bridge_result_invalid_shape")
    ping = rows[0]
    if not isinstance(ping, dict) or ping.get("ok") is not True or ping.get("command") != "PING":
        raise ProbeError("bridge_ping_failed")
    expected = {
        "pid": pid, "process_start_ticks": runtime["start_ticks"], "client_size": runtime["size"],
        "client_sha256": runtime["sha256"],
    }
    for key, value in expected.items():
        if ping.get(key) != value:
            raise ProbeError(f"bridge_ping_{key}_mismatch")
    for target, row in zip(BRIDGE_TARGETS, rows[1:]):
        if not isinstance(row, dict) or row.get("ok") is not True or row.get("target") != target:
            raise ProbeError(f"bridge_{target}_failed")
        if row.get("scan_status") != "OK" or row.get("validated_hits") != 1:
            raise ProbeError(f"bridge_{target}_not_unique")
    # The three objects are lifecycle/structure evidence only. A 2026-08-20
    # login-screen observation still produced one validated hit for all three, so
    # their presence cannot independently establish active gameplay state.
    return "UNKNOWN", "BRIDGE_3_OF_3_SEMANTICS_UNPROVEN"


def collect(runner: Callable[[Sequence[str]], str] = run) -> dict[str, Any]:
    containers = docker_containers(runner)
    target = [(cid, name) for cid, name in containers if name == TARGET_CONTAINER]
    if len(target) != 1:
        raise ProbeError(f"target_container_count:{len(target)}")
    all_candidates: list[tuple[str, str, dict[str, Any]]] = []
    for cid, name in containers:
        for item in candidate_rows(cid, runner):
            path_hinted = "Tibia" in item["exe"] or item["exe"].endswith("/bin/client")
            exact = item["size"] == SIZE and item["sha256"] == SHA
            if path_hinted and not exact:
                raise ProbeError("conflicting_official_client_candidate")
            if path_hinted or exact:
                all_candidates.append((cid, name, item))
    if len(all_candidates) != 1:
        raise ProbeError(f"official_client_candidate_count:{len(all_candidates)}")
    cid, name, item = all_candidates[0]
    if name != TARGET_CONTAINER:
        raise ProbeError("exact_client_outside_target")
    runtime = target_runtime(cid, int(item["pid"]), runner)
    if runtime["size"] != SIZE or runtime["sha256"] != SHA:
        raise ProbeError("exact_client_fence_mismatch")
    window_identity = window_proof(cid, int(item["pid"]), runner)
    state, state_evidence = structural_state(cid, int(item["pid"]), runtime, runner)
    locator = f"docker:{name}:{cid}"
    candidate_fingerprint = hashlib.sha256(
        f"{locator}:{item['pid']}:{runtime['start_ticks']}:{runtime['size']}:{runtime['sha256']}".encode()
    ).hexdigest()
    return {
        "proof_kind": PROOF_KIND, "pid": int(item["pid"]), "display": TARGET_DISPLAY,
        "window_identity": window_identity, "remote_view_endpoint": "https://synology:6902/",
        "remote_view_mapping": "UNKNOWN", "state": state, "state_evidence": state_evidence,
        "boot_id_sha256": runtime["boot_id_sha256"],
        "process_start_ticks": runtime["start_ticks"], "client_version": VER, "client_size": runtime["size"],
        "client_sha256": runtime["sha256"], "runtime_locator": locator,
        "inventory_scope": "all_running_docker_containers", "inventory_complete": True,
        "candidate_count": 1, "candidate_fingerprint": candidate_fingerprint,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["probe"])
    parser.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = collect()
        args.output.write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n")
        args.output.chmod(0o600)
        print("TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS")
        return 0
    except (ProbeError, subprocess.TimeoutExpired, OSError) as exc:
        print(f"TRACK_A_KASM_EXISTING_RUNTIME_PROBE_ERROR={type(exc).__name__}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
