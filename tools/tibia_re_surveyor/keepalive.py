from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
import time
from typing import List, Mapping, Optional, Tuple

from .runtime import CommandRunner, EXPECTED_CLIENT_SHA256, EXPECTED_CLIENT_SIZE

HEARTBEAT_PATH = "/tmp/otclient-track-a-last-activity"
GUI_LOCK_PATH = "/tmp/otclient-track-a-gui-input.lock"
DEFAULT_TRIGGER_SECONDS = 8 * 60
TARGET_MAX_INACTIVITY_SECONDS = 10 * 60


@dataclass(frozen=True)
class KeepaliveDecision:
    allowed: bool
    reasons: Tuple[str, ...]


def load_authority(path: Optional[Path]) -> Optional[dict]:
    if path is None:
        return None
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid keepalive authority input: {exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError("keepalive authority input must be a JSON object")
    return doc


def evaluate_authority(authority: Optional[Mapping[str, object]], snapshot: Mapping[str, object]) -> KeepaliveDecision:
    reasons: List[str] = []
    if authority is None:
        return KeepaliveDecision(False, ("NO_KEEPALIVE_AUTHORITY_INPUT",))
    required_pairs = {"runtime_access": "canonical_reuse_or_mutation", "gate_a": "PASS", "gate_b": "PASS", "target_uniqueness": "PROVEN", "whole_lifetime_supervisor": "PASS"}
    for key, expected in required_pairs.items():
        if authority.get(key) != expected:
            reasons.append(f"AUTHORITY_{key.upper()}_NOT_{expected}")
    if authority.get("generation_rebind") not in {"PASS", "NOT_APPLICABLE"}:
        reasons.append("AUTHORITY_GENERATION_REBIND_NOT_PASS")
    if authority.get("mutation_authorized") is not True:
        reasons.append("AUTHORITY_MUTATION_FALSE")
    if authority.get("gui_input_authorized") is not True:
        reasons.append("AUTHORITY_GUI_INPUT_FALSE")
    if snapshot.get("target_uniqueness") != "PROVEN":
        reasons.append("RUNTIME_TARGET_UNIQUENESS_NOT_PROVEN")
    fence = snapshot.get("exact_current_fence") or {}
    if not isinstance(fence, Mapping) or fence.get("match") is not True:
        reasons.append("RUNTIME_CURRENT_FENCE_NOT_MATCHED")
    control = snapshot.get("canonical_control") or {}
    if not isinstance(control, Mapping) or control.get("registration_present") is not True:
        reasons.append("CANONICAL_REGISTRATION_ABSENT")
        registration = None
    else:
        registration = control.get("registration")
    if not isinstance(control, Mapping) or control.get("lease_present") is not True:
        reasons.append("CANONICAL_LEASE_ABSENT")
        lease = None
    else:
        lease = control.get("lease")
    if isinstance(control, Mapping) and control.get("lease_expired") is not False:
        reasons.append("CANONICAL_LEASE_EXPIRED_OR_UNKNOWN")
    processes = snapshot.get("processes") or []
    process = processes[0] if isinstance(processes, list) and len(processes) == 1 else None
    if isinstance(registration, Mapping) and isinstance(process, Mapping):
        comparisons = {"pid": process.get("pid"), "process_start_ticks": process.get("process_start_ticks"), "client_size": process.get("client_size"), "client_sha256": process.get("client_sha256"), "display": snapshot.get("display")}
        for key, expected in comparisons.items():
            if registration.get(key) != expected:
                reasons.append(f"REGISTRATION_{key.upper()}_MISMATCH")
        if registration.get("client_size") != EXPECTED_CLIENT_SIZE or registration.get("client_sha256") != EXPECTED_CLIENT_SHA256:
            reasons.append("REGISTRATION_CURRENT_FENCE_MISMATCH")
        if registration.get("state") != "IN_GAME":
            reasons.append("REGISTRATION_STATE_NOT_IN_GAME")
    elif registration is not None:
        reasons.append("RUNTIME_PROCESS_IDENTITY_NOT_UNIQUE")
    if isinstance(registration, Mapping) and isinstance(lease, Mapping):
        if registration.get("lease_generation") != lease.get("generation"):
            reasons.append("LEASE_REGISTRATION_GENERATION_MISMATCH")
        owner = authority.get("runtime_owner_task")
        if not owner or lease.get("controller_task") != owner:
            reasons.append("LEASE_CONTROLLER_TASK_MISMATCH")
    return KeepaliveDecision(not reasons, tuple(sorted(set(reasons))))


class DockerKeepaliveTransport:
    def __init__(self, container: str, display: str, runner: Optional[CommandRunner] = None, now_fn=time.time, heartbeat_path: str = HEARTBEAT_PATH, lock_path: str = GUI_LOCK_PATH):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", container):
            raise ValueError("invalid container name")
        if not re.fullmatch(r":\d+", display):
            raise ValueError("invalid display")
        self.container = container
        self.display = display
        self.runner = runner or CommandRunner()
        self.now_fn = now_fn
        self.heartbeat_path = heartbeat_path
        self.lock_path = lock_path

    def heartbeat_age(self) -> Optional[int]:
        result = self.runner.run(["docker", "exec", self.container, "cat", self.heartbeat_path], timeout=5.0)
        if result.returncode != 0:
            return None
        try:
            last = int(result.stdout.strip())
        except ValueError:
            return None
        return max(0, int(self.now_fn()) - last)

    def rotate_once(self, *, pid: int, process_start_ticks: int, client_size: int, client_sha256: str, xid: int, trigger_seconds: int, modifier: str) -> str:
        if modifier not in {"ctrl", "shift", "alt"}:
            raise ValueError("turn modifier must be ctrl, shift or alt")
        if trigger_seconds <= 0 or trigger_seconds > TARGET_MAX_INACTIVITY_SECONDS:
            raise ValueError("invalid anti-idle trigger")
        if client_size != EXPECTED_CLIENT_SIZE or client_sha256 != EXPECTED_CLIENT_SHA256:
            return "KEEPALIVE_SKIPPED_IDENTITY_CHANGED"
        script = r'''
set -eu
lock=$1; heartbeat=$2; threshold=$3; pid=$4; start=$5; size=$6; sha=$7; xid=$8; modifier=$9
exec 9>"$lock"
if ! flock -n 9; then echo KEEPALIVE_SKIPPED_LOCKED; exit 0; fi
now=$(date +%s)
if [ -f "$heartbeat" ]; then
  old=$(cat "$heartbeat" 2>/dev/null || true)
  case "$old" in *[!0-9]*|'') old=0;; esac
  if [ "$old" -gt 0 ] && [ $((now-old)) -lt "$threshold" ]; then echo KEEPALIVE_SKIPPED_REFRESHED; exit 0; fi
fi
[ -r "/proc/$pid/stat" ] || { echo KEEPALIVE_SKIPPED_IDENTITY_CHANGED; exit 0; }
actual_start=$(awk '{print $22}' "/proc/$pid/stat")
[ "$actual_start" = "$start" ] || { echo KEEPALIVE_SKIPPED_IDENTITY_CHANGED; exit 0; }
actual_size=$(stat -Lc %s "/proc/$pid/exe")
[ "$actual_size" = "$size" ] || { echo KEEPALIVE_SKIPPED_IDENTITY_CHANGED; exit 0; }
actual_sha=$(sha256sum "/proc/$pid/exe" | awk '{print $1}')
[ "$actual_sha" = "$sha" ] || { echo KEEPALIVE_SKIPPED_IDENTITY_CHANGED; exit 0; }
actual_xpid=$(xprop -id "$xid" _NET_WM_PID 2>/dev/null | sed -n 's/.*= *\([0-9][0-9]*\).*/\1/p')
[ "$actual_xpid" = "$pid" ] || { echo KEEPALIVE_SKIPPED_WINDOW_CHANGED; exit 0; }
xdotool key --window "$xid" --clearmodifiers "${modifier}+Right" >/dev/null 2>&1 || { echo KEEPALIVE_FAILED_INPUT; exit 0; }
umask 077
tmp="${heartbeat}.tmp.$$"
printf '%s\n' "$now" > "$tmp"
mv -f "$tmp" "$heartbeat"
echo KEEPALIVE_ROTATION_SENT
'''
        args = ["docker", "exec", "-u", "kasm-user", "-e", f"DISPLAY={self.display}", self.container, "bash", "-lc", script, "surveyor-keepalive", self.lock_path, self.heartbeat_path, str(trigger_seconds), str(pid), str(process_start_ticks), str(client_size), client_sha256, str(xid), modifier]
        result = self.runner.run(args, timeout=20.0)
        if result.returncode != 0:
            return "KEEPALIVE_FAILED_TRANSPORT"
        marker = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
        allowed_markers = {"KEEPALIVE_SKIPPED_LOCKED", "KEEPALIVE_SKIPPED_REFRESHED", "KEEPALIVE_SKIPPED_IDENTITY_CHANGED", "KEEPALIVE_SKIPPED_WINDOW_CHANGED", "KEEPALIVE_FAILED_INPUT", "KEEPALIVE_ROTATION_SENT"}
        return marker if marker in allowed_markers else "KEEPALIVE_FAILED_TRANSPORT"


def run_keepalive_once(snapshot: Mapping[str, object], authority: Optional[Mapping[str, object]], transport: DockerKeepaliveTransport, *, trigger_seconds: int = DEFAULT_TRIGGER_SECONDS, modifier: str = "ctrl") -> dict:
    if trigger_seconds <= 0 or trigger_seconds > TARGET_MAX_INACTIVITY_SECONDS:
        raise ValueError("trigger must be within the ten-minute inactivity target")
    decision = evaluate_authority(authority, snapshot)
    age = transport.heartbeat_age()
    due = age is None or age >= trigger_seconds
    event = {"semantic_evidence": False, "trigger_seconds": trigger_seconds, "target_max_inactivity_seconds": TARGET_MAX_INACTIVITY_SECONDS, "heartbeat_age_seconds": age, "due": due, "authority_allowed": decision.allowed, "authority_reasons": list(decision.reasons)}
    if not due:
        event["result"] = "KEEPALIVE_NOT_DUE"
        return event
    if not decision.allowed:
        event["result"] = "KEEPALIVE_SKIPPED_UNAUTHORIZED"
        return event
    processes = snapshot.get("processes") or []
    windows = snapshot.get("visible_tibia_windows") or []
    if not isinstance(processes, list) or len(processes) != 1 or not isinstance(processes[0], Mapping):
        event["result"] = "KEEPALIVE_SKIPPED_IDENTITY_CHANGED"
        return event
    process = processes[0]
    xid = next((w.get("xid") for w in windows if isinstance(w, Mapping) and w.get("pid") == process.get("pid")), None)
    if not isinstance(xid, int):
        event["result"] = "KEEPALIVE_SKIPPED_WINDOW_CHANGED"
        return event
    event["result"] = transport.rotate_once(pid=int(process["pid"]), process_start_ticks=int(process["process_start_ticks"]), client_size=int(process["client_size"]), client_sha256=str(process["client_sha256"]), xid=xid, trigger_seconds=trigger_seconds, modifier=modifier)
    return event
