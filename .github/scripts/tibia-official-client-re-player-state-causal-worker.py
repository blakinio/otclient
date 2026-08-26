#!/usr/bin/env python3
"""One-shot causal player-position discriminator for an already-admitted Track A runtime."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable, Mapping, Sequence

RID = "track-a-canonical-live"
VER = "15.32"
SIZE = 52109920
SHA = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"
CONTAINER = "otclient-track-a-kasmvnc"
DISPLAY = ":1"
PROOF_KIND = "existing_runtime_adoption_v1"
STATE_ROOT = Path("/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime")
REGISTRATION = STATE_ROOT / "runtime-registration.json"
DIRECTIONS = {"north": "Up", "east": "Right", "south": "Down", "west": "Left"}
WINDOW_RE = re.compile(
    r"^x11:(0x[0-9a-fA-F]+):pid:(\d+):class:client/Tibia:title_sha256:([0-9a-f]{64})$"
)
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


class WorkerRefusal(RuntimeError):
    pass


@dataclass(frozen=True)
class Target:
    pid: int
    start_ticks: int
    container: str
    display: str
    window_id: str


def validate_request(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or set(data) != {"schema_version", "action_hash", "kind", "parameters"}:
        raise WorkerRefusal("REQUEST_INVALID")
    if data.get("schema_version") != 1 or data.get("kind") != "move":
        raise WorkerRefusal("REQUEST_INVALID")
    action_hash = data.get("action_hash")
    params = data.get("parameters")
    if not isinstance(action_hash, str) or not HEX64.fullmatch(action_hash):
        raise WorkerRefusal("REQUEST_INVALID")
    semantic_payload = {"schema_version": data["schema_version"], "kind": data["kind"], "parameters": data["parameters"]}
    expected_hash = hashlib.sha256(json.dumps(semantic_payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if action_hash != expected_hash:
        raise WorkerRefusal("ACTION_HASH_MISMATCH")
    if not isinstance(params, dict) or set(params) != {"direction", "tiles"}:
        raise WorkerRefusal("REQUEST_INVALID")
    if params.get("direction") not in DIRECTIONS or params.get("tiles") != 1:
        raise WorkerRefusal("MOVE_NOT_ONE_CARDINAL_TILE")
    return data


def validate_registration(data: Any) -> Target:
    if not isinstance(data, dict):
        raise WorkerRefusal("REGISTRATION_INVALID")
    exact = (
        data.get("schema_version") == 1
        and data.get("runtime_id") == RID
        and data.get("client_version") == VER
        and data.get("client_size") == SIZE
        and data.get("client_sha256") == SHA
        and data.get("display") == DISPLAY
        and data.get("state") == "UNKNOWN"
        and data.get("proof_kind") == PROOF_KIND
    )
    pid = data.get("pid")
    start = data.get("process_start_ticks")
    locator = data.get("runtime_locator")
    window = data.get("window_identity")
    if not exact or isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
        raise WorkerRefusal("REGISTRATION_FENCE_MISMATCH")
    if isinstance(start, bool) or not isinstance(start, int) or start <= 0:
        raise WorkerRefusal("REGISTRATION_FENCE_MISMATCH")
    if not isinstance(locator, str):
        raise WorkerRefusal("REGISTRATION_LOCATOR_INVALID")
    parts = locator.split(":", 2)
    if len(parts) != 3 or parts[0] != "docker" or parts[1] != CONTAINER or not parts[2]:
        raise WorkerRefusal("REGISTRATION_LOCATOR_INVALID")
    if not isinstance(window, str) or (match := WINDOW_RE.fullmatch(window)) is None:
        raise WorkerRefusal("WINDOW_IDENTITY_INVALID")
    if int(match.group(2)) != pid:
        raise WorkerRefusal("WINDOW_PID_MISMATCH")
    return Target(pid=pid, start_ticks=start, container=parts[1], display=DISPLAY, window_id=match.group(1))


def validate_candidate(data: Any) -> tuple[int, int, int]:
    if not isinstance(data, Mapping):
        raise WorkerRefusal("PLAYER_STATE_UNAVAILABLE")
    if (
        data.get("state") != "AVAILABLE"
        or data.get("reader_id") != "player_state_typed_reader"
        or data.get("object_count") != 1
        or data.get("position_mirror_consistent") is not True
        or data.get("process_memory_access") != "read_only"
        or data.get("semantic_state") != "CANDIDATE_PENDING_CAUSAL_E2E"
        or data.get("semantic_promotion_allowed") is not False
    ):
        raise WorkerRefusal("PLAYER_STATE_PRECONDITION_FAILED")
    pos = data.get("position")
    if not isinstance(pos, Mapping) or set(pos) != {"x", "y", "z"}:
        raise WorkerRefusal("PLAYER_STATE_POSITION_INVALID")
    values = tuple(pos[key] for key in ("x", "y", "z"))
    if any(isinstance(v, bool) or not isinstance(v, int) for v in values):
        raise WorkerRefusal("PLAYER_STATE_POSITION_INVALID")
    x, y, z = values
    if not (1 <= x <= 65535 and 1 <= y <= 65535 and 0 <= z <= 15):
        raise WorkerRefusal("PLAYER_STATE_POSITION_INVALID")
    return x, y, z


def delta_confirms(before: tuple[int, int, int], after: tuple[int, int, int], direction: str) -> bool:
    expected = {
        "north": (before[0], before[1] - 1, before[2]),
        "east": (before[0] + 1, before[1], before[2]),
        "south": (before[0], before[1] + 1, before[2]),
        "west": (before[0] - 1, before[1], before[2]),
    }[direction]
    return after == expected


def dispatch_command(target: Target, direction: str) -> list[str]:
    return [
        "docker", "exec", "-u", "kasm-user", "-e", f"DISPLAY={target.display}", target.container,
        "xdotool", "key", "--window", str(int(target.window_id, 16)), DIRECTIONS[direction],
    ]


def _run(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(command), check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)


def tool_ready(target: Target) -> bool:
    completed = _run([
        "docker", "exec", "-u", "kasm-user", "-e", f"DISPLAY={target.display}", target.container,
        "sh", "-lc", "command -v xdotool >/dev/null 2>&1",
    ])
    return completed.returncode == 0


def read_candidate(registration: Mapping[str, Any]) -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    root_s = str(root)
    if root_s not in sys.path:
        sys.path.insert(0, root_s)
    from tools.tibia_re_surveyor.player_state import read_player_state

    def runner(args: list[str]) -> str:
        completed = subprocess.run(args, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        if completed.returncode:
            raise RuntimeError("reader command failed")
        return completed.stdout

    return read_player_state(
        pid=int(registration["pid"]),
        start_ticks=int(registration["process_start_ticks"]),
        runner=runner,
        container=CONTAINER,
    )


def dispatch(command: Sequence[str]) -> int:
    try:
        return _run(command).returncode
    except (OSError, subprocess.TimeoutExpired):
        return 255


def execute_once(
    request: Any,
    registration: Any,
    *,
    read_candidate: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    tool_ready: Callable[[Target], bool],
    dispatch: Callable[[Sequence[str]], int],
    sleep: Callable[[float], None],
    reconciliation_attempts: int = 12,
) -> dict[str, Any]:
    try:
        req = validate_request(request)
        target = validate_registration(registration)
        if not tool_ready(target):
            raise WorkerRefusal("INPUT_TOOL_UNAVAILABLE")
        before = validate_candidate(read_candidate(registration))
    except (WorkerRefusal, OSError, RuntimeError, subprocess.TimeoutExpired):
        return {
            "status": "REFUSED", "effect_count": 0,
            "action_hash": request.get("action_hash", "0" * 64) if isinstance(request, dict) else "0" * 64,
            "reason_code": "SEMANTIC_PRECONDITION_FAILED",
        }

    direction = req["parameters"]["direction"]
    command = dispatch_command(target, direction)
    rc = dispatch(command)
    if rc != 0:
        return {
            "status": "AMBIGUOUS", "effect_count": 1, "action_hash": req["action_hash"],
            "reason_code": "INPUT_DISPATCH_UNCERTAIN",
        }

    last = before
    for attempt in range(max(1, reconciliation_attempts)):
        if attempt:
            sleep(0.15)
        try:
            after = validate_candidate(read_candidate(registration))
        except (WorkerRefusal, OSError, RuntimeError, subprocess.TimeoutExpired):
            continue
        last = after
        if delta_confirms(before, after, direction):
            return {"status": "CONFIRMED", "effect_count": 1, "action_hash": req["action_hash"]}
        if after != before:
            return {
                "status": "AMBIGUOUS", "effect_count": 1, "action_hash": req["action_hash"],
                "reason_code": "UNEXPECTED_POSITION_DELTA",
            }
    return {
        "status": "AMBIGUOUS", "effect_count": 1, "action_hash": req["action_hash"],
        "reason_code": "MOVE_DELTA_NOT_CONFIRMED",
    }


def write_result(path: Path, result: Mapping[str, Any]) -> None:
    allowed = {"status", "effect_count", "action_hash", "reason_code"}
    data = {key: value for key, value in result.items() if key in allowed}
    parent = path.parent
    fd, name = tempfile.mkstemp(prefix=".player-state-result-", dir=parent)
    try:
        if hasattr(os, "fchmod"):
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        fd = -1
        os.replace(name, path)
    finally:
        if fd >= 0:
            os.close(fd)
        try:
            os.unlink(name)
        except FileNotFoundError:
            pass


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 3 or args[0] != "guarded-dispatch":
        return 2
    request_path = Path(args[1])
    result_path = Path(args[2])
    try:
        request = json.loads(request_path.read_text(encoding="utf-8"))
        registration = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 2
    result = execute_once(
        request, registration,
        read_candidate=read_candidate,
        tool_ready=tool_ready,
        dispatch=dispatch,
        sleep=time.sleep,
    )
    try:
        write_result(result_path, result)
    except OSError:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
