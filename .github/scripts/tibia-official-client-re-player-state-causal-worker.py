#!/usr/bin/env python3
"""One-shot causal player-position discriminator for an already-admitted Track A runtime.

This worker is repository infrastructure only. Runtime authority is supplied by the
canonical guarded-dispatch supervisor; the worker never acquires or expands it.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
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

# The canonical guarded-dispatch contract used by terminal PR #698 is 30 s.
# Keep the worker comfortably inside that outer supervisor deadline. All work is
# sliced from one monotonic absolute deadline; RESULT_WRITE_RESERVE_SECONDS is
# withheld from every effect/read/reconciliation wait and kept for durable result
# publication. The remaining 3 seconds belong to parent scheduling/return jitter.
OUTER_GUARDED_DISPATCH_TIMEOUT_SECONDS = 30.0
SUPERVISOR_RETURN_MARGIN_SECONDS = 3.0
WORKER_TOTAL_BUDGET_SECONDS = (
    OUTER_GUARDED_DISPATCH_TIMEOUT_SECONDS - SUPERVISOR_RETURN_MARGIN_SECONDS
)
RESULT_WRITE_RESERVE_SECONDS = 2.0
MIN_DURABLE_WRITE_START_SECONDS = 0.25
TOOL_READY_TIMEOUT_CAP_SECONDS = 10.0
READER_TIMEOUT_CAP_SECONDS = 20.0
DISPATCH_TIMEOUT_CAP_SECONDS = 10.0
RECONCILIATION_SLEEP_SECONDS = 0.15
POST_DISPATCH_CHECKPOINT_FILENAME = ".guarded-dispatch-post-dispatch.json"
POST_DISPATCH_CHECKPOINT_REASON = "POST_DISPATCH_RECONCILIATION_INCOMPLETE"


class WorkerRefusal(RuntimeError):
    pass


class WorkerDeadlineExceeded(TimeoutError):
    pass


@dataclass(frozen=True)
class Target:
    pid: int
    start_ticks: int
    container: str
    display: str
    window_id: str


class DeadlineBudget:
    """One monotonic absolute worker deadline with caller-selected reserve."""

    def __init__(self, deadline: float, *, clock: Callable[[], float] = time.monotonic) -> None:
        if not math.isfinite(deadline):
            raise ValueError("deadline must be finite")
        self.deadline = float(deadline)
        self._clock = clock

    @classmethod
    def start(cls, *, clock: Callable[[], float] = time.monotonic) -> "DeadlineBudget":
        return cls(clock() + WORKER_TOTAL_BUDGET_SECONDS, clock=clock)

    def remaining(self, *, reserve: float = 0.0) -> float:
        return max(0.0, self.deadline - self._clock() - max(0.0, reserve))

    def timeout(self, cap: float, *, reserve: float = 0.0) -> float:
        remaining = self.remaining(reserve=reserve)
        if remaining <= 0.0:
            raise WorkerDeadlineExceeded("worker deadline exhausted")
        return min(float(cap), remaining)

    def require(self, minimum: float = 0.0, *, reserve: float = 0.0) -> None:
        remaining = self.remaining(reserve=reserve)
        if remaining <= 0.0 or remaining < minimum:
            raise WorkerDeadlineExceeded("insufficient worker deadline budget")

    def sleep(self, seconds: float, *, reserve: float = 0.0) -> None:
        duration = min(max(0.0, seconds), self.remaining(reserve=reserve))
        if duration <= 0.0:
            raise WorkerDeadlineExceeded("worker deadline exhausted before sleep")
        time.sleep(duration)


def validate_request(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict) or set(data) != {"schema_version", "action_hash", "kind", "parameters"}:
        raise WorkerRefusal("REQUEST_INVALID")
    if data.get("schema_version") != 1 or data.get("kind") != "move":
        raise WorkerRefusal("REQUEST_INVALID")
    action_hash = data.get("action_hash")
    params = data.get("parameters")
    if not isinstance(action_hash, str) or not HEX64.fullmatch(action_hash):
        raise WorkerRefusal("REQUEST_INVALID")
    semantic_payload = {
        "schema_version": data["schema_version"],
        "kind": data["kind"],
        "parameters": data["parameters"],
    }
    expected_hash = hashlib.sha256(
        json.dumps(semantic_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
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
        and data.get("state") == "IN_GAME"
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


def _run(
    command: Sequence[str],
    budget: DeadlineBudget,
    *,
    timeout_cap: float,
) -> subprocess.CompletedProcess[str]:
    timeout = budget.timeout(timeout_cap, reserve=RESULT_WRITE_RESERVE_SECONDS)
    return subprocess.run(
        list(command),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def tool_ready(target: Target, budget: DeadlineBudget) -> bool:
    completed = _run(
        [
            "docker", "exec", "-u", "kasm-user", "-e", f"DISPLAY={target.display}", target.container,
            "sh", "-lc", "command -v xdotool >/dev/null 2>&1",
        ],
        budget,
        timeout_cap=TOOL_READY_TIMEOUT_CAP_SECONDS,
    )
    return completed.returncode == 0


def read_candidate(registration: Mapping[str, Any], budget: DeadlineBudget) -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    root_s = str(root)
    if root_s not in sys.path:
        sys.path.insert(0, root_s)
    from tools.tibia_re_surveyor.player_state import read_player_state

    def runner(args: list[str]) -> str:
        timeout = budget.timeout(READER_TIMEOUT_CAP_SECONDS, reserve=RESULT_WRITE_RESERVE_SECONDS)
        completed = subprocess.run(
            args,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        if completed.returncode:
            raise RuntimeError("reader command failed")
        return completed.stdout

    return read_player_state(
        pid=int(registration["pid"]),
        start_ticks=int(registration["process_start_ticks"]),
        runner=runner,
        container=CONTAINER,
    )


def dispatch(command: Sequence[str], budget: DeadlineBudget) -> int:
    # Deadline exhaustion can happen before subprocess creation. Preserve that as
    # a no-effect refusal instead of falsely claiming a possibly-dispatched input.
    try:
        return _run(command, budget, timeout_cap=DISPATCH_TIMEOUT_CAP_SECONDS).returncode
    except WorkerDeadlineExceeded:
        raise
    except subprocess.TimeoutExpired:
        # The child was created and may already have sent input before timing out.
        return 255
    except OSError as exc:
        # subprocess creation failed before a child/effect could be established.
        raise WorkerRefusal("INPUT_DISPATCH_NOT_STARTED") from exc


def _refused(action_hash: str, reason: str) -> dict[str, Any]:
    return {
        "status": "REFUSED",
        "effect_count": 0,
        "action_hash": action_hash,
        "reason_code": reason,
    }


def _ambiguous(action_hash: str, reason: str) -> dict[str, Any]:
    return {
        "status": "AMBIGUOUS",
        "effect_count": 1,
        "action_hash": action_hash,
        "reason_code": reason,
    }


def execute_once(
    request: Any,
    registration: Any,
    *,
    budget: DeadlineBudget,
    read_candidate_fn: Callable[[Mapping[str, Any], DeadlineBudget], Mapping[str, Any]] = read_candidate,
    tool_ready_fn: Callable[[Target, DeadlineBudget], bool] = tool_ready,
    dispatch_fn: Callable[[Sequence[str], DeadlineBudget], int] = dispatch,
    sleep_fn: Callable[[float], None] | None = None,
    reconciliation_attempts: int = 12,
    post_dispatch_checkpoint_fn: Callable[[Mapping[str, Any], DeadlineBudget], None] | None = None,
) -> dict[str, Any]:
    fallback_hash = request.get("action_hash", "0" * 64) if isinstance(request, dict) else "0" * 64
    try:
        req = validate_request(request)
        target = validate_registration(registration)
        budget.require(reserve=RESULT_WRITE_RESERVE_SECONDS)
        if not tool_ready_fn(target, budget):
            raise WorkerRefusal("INPUT_TOOL_UNAVAILABLE")
        baseline_budget_before = budget.remaining(reserve=RESULT_WRITE_RESERVE_SECONDS)
        before = validate_candidate(read_candidate_fn(registration, budget))
        baseline_read_seconds = max(
            0.0,
            baseline_budget_before - budget.remaining(reserve=RESULT_WRITE_RESERVE_SECONDS),
        )
    except WorkerDeadlineExceeded:
        return _refused(fallback_hash, "SEMANTIC_PRECONDITION_TIMEOUT")
    except (WorkerRefusal, OSError, RuntimeError, subprocess.TimeoutExpired):
        return _refused(fallback_hash, "SEMANTIC_PRECONDITION_FAILED")

    direction = req["parameters"]["direction"]
    command = dispatch_command(target, direction)
    # Exactly one dispatch attempt after the preconditions. Deadline/spawn failure
    # before child creation is effect_count=0; once the child starts, nonzero or
    # timeout is conservatively effect-ambiguous and is never retried.
    try:
        rc = dispatch_fn(command, budget)
    except WorkerDeadlineExceeded:
        return _refused(req["action_hash"], "INPUT_DISPATCH_DEADLINE_BEFORE_START")
    except WorkerRefusal:
        return _refused(req["action_hash"], "INPUT_DISPATCH_NOT_STARTED")
    except OSError:
        return _refused(req["action_hash"], "INPUT_DISPATCH_NOT_STARTED")
    if rc != 0:
        return _ambiguous(req["action_hash"], "INPUT_DISPATCH_UNCERTAIN")

    post_dispatch_checkpoint = _ambiguous(req["action_hash"], POST_DISPATCH_CHECKPOINT_REASON)
    if post_dispatch_checkpoint_fn is not None:
        try:
            post_dispatch_checkpoint_fn(post_dispatch_checkpoint, budget)
        except (OSError, WorkerDeadlineExceeded):
            return post_dispatch_checkpoint

    last = before
    for attempt in range(max(1, reconciliation_attempts)):
        try:
            budget.require(
                baseline_read_seconds,
                reserve=RESULT_WRITE_RESERVE_SECONDS,
            )
            if attempt:
                if sleep_fn is None:
                    budget.sleep(
                        RECONCILIATION_SLEEP_SECONDS,
                        reserve=RESULT_WRITE_RESERVE_SECONDS,
                    )
                else:
                    duration = min(
                        RECONCILIATION_SLEEP_SECONDS,
                        budget.remaining(reserve=RESULT_WRITE_RESERVE_SECONDS),
                    )
                    if duration <= 0.0:
                        raise WorkerDeadlineExceeded("reconciliation sleep budget exhausted")
                    sleep_fn(duration)
                    budget.require(reserve=RESULT_WRITE_RESERVE_SECONDS)
            after = validate_candidate(read_candidate_fn(registration, budget))
        except WorkerDeadlineExceeded:
            return _ambiguous(req["action_hash"], "RECONCILIATION_DEADLINE_EXHAUSTED")
        except (WorkerRefusal, OSError, RuntimeError, subprocess.TimeoutExpired):
            if budget.remaining(reserve=RESULT_WRITE_RESERVE_SECONDS) <= 0.0:
                return _ambiguous(req["action_hash"], "RECONCILIATION_DEADLINE_EXHAUSTED")
            continue
        last = after
        if delta_confirms(before, after, direction):
            return {"status": "CONFIRMED", "effect_count": 1, "action_hash": req["action_hash"]}
        if after != before:
            return _ambiguous(req["action_hash"], "UNEXPECTED_POSITION_DELTA")

    # Reconciliation may exhaust its configured attempt count before the time
    # budget. That is still a terminal ambiguity, never permission to dispatch again.
    _ = last
    return _ambiguous(req["action_hash"], "MOVE_DELTA_NOT_CONFIRMED")


def write_result(path: Path, result: Mapping[str, Any], budget: DeadlineBudget) -> None:
    allowed = {"status", "effect_count", "action_hash", "reason_code"}
    data = {key: value for key, value in result.items() if key in allowed}
    parent = path.parent
    budget.require(MIN_DURABLE_WRITE_START_SECONDS)
    fd, name = tempfile.mkstemp(prefix=".player-state-result-", dir=parent)
    replaced = False
    try:
        if hasattr(os, "fchmod"):
            os.fchmod(fd, 0o600)
        budget.require()
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            fd = -1
            json.dump(data, handle, sort_keys=True, separators=(",", ":"))
            handle.write("\n")
            handle.flush()
            budget.require()
            os.fsync(handle.fileno())
        budget.require()
        os.replace(name, path)
        replaced = True
        budget.require()
        dir_fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
        budget.require()
    finally:
        if fd >= 0:
            os.close(fd)
        if not replaced:
            try:
                os.unlink(name)
            except FileNotFoundError:
                pass


def main(argv: Sequence[str] | None = None) -> int:
    # Start the single worker deadline at process entry, before request or
    # registration reads. All subprocess/read/reconciliation/write work consumes
    # this same absolute monotonic budget.
    budget = DeadlineBudget.start()
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
    checkpoint_path = result_path.with_name(POST_DISPATCH_CHECKPOINT_FILENAME)
    try:
        checkpoint_path.unlink(missing_ok=True)
    except OSError:
        return 2

    def persist_post_dispatch_checkpoint(
        checkpoint: Mapping[str, Any],
        checkpoint_budget: DeadlineBudget,
    ) -> None:
        write_result(checkpoint_path, checkpoint, checkpoint_budget)

    result = execute_once(
        request,
        registration,
        budget=budget,
        post_dispatch_checkpoint_fn=persist_post_dispatch_checkpoint,
    )
    try:
        write_result(result_path, result, budget)
    except (OSError, WorkerDeadlineExceeded):
        # A result that was not proven durably written is not success. The parent
        # guarded-dispatch path already treats nonzero worker termination as failure.
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
