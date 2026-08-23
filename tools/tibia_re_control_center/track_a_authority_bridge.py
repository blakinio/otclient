from __future__ import annotations

import json
import os
import queue
import sys
import tempfile
import threading
import time
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .model import ActionRequest, ValidationError
from .official_adapter import GuardedExecutionOutcome, GuardedRuntimeView

READY_KEYS = frozenset({"type", "action_hash", "fence_digest"})
RESULT_KEYS = frozenset({"type", "outcome", "reason_code", "evidence_refs"})
ALLOWED_OUTCOMES = frozenset({"confirmed", "ambiguous"})
_PRIVATE_READY_PREFIX = "TRACK_A_GUARDED_DISPATCH_READY="
_PRIVATE_RESULT_PREFIX = "TRACK_A_GUARDED_DISPATCH_RESULT="
_PRIVATE_READY_KEYS = frozenset({"protocol", "status", "action_hash", "fence_digest"})
_PRIVATE_RESULT_KEYS = frozenset({"status", "effect_count", "action_hash", "reason_code"})


def _invalid(message: str) -> ValidationError:
    return ValidationError("TRACK_A_BRIDGE_PROTOCOL_INVALID", message)


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value.lower()
    )


def require_exact_record(value: Any, keys: frozenset[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != set(keys):
        raise _invalid("unexpected guarded-dispatch record")
    return value


def normalize_result(value: Any) -> dict[str, Any]:
    record = require_exact_record(value, RESULT_KEYS)
    if record["type"] != "result" or record["outcome"] not in ALLOWED_OUTCOMES:
        raise _invalid("invalid guarded-dispatch result")
    reason = record["reason_code"]
    refs = record["evidence_refs"]
    if reason is not None and not isinstance(reason, str):
        raise _invalid("invalid result reason")
    if not isinstance(refs, (tuple, list)) or not all(isinstance(ref, str) and ref for ref in refs):
        raise _invalid("invalid evidence refs")
    return {
        "type": "result",
        "outcome": record["outcome"],
        "reason_code": reason,
        "evidence_refs": tuple(refs),
    }


def _normalize_private_ready(payload: Any, action_hash: str) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) != set(_PRIVATE_READY_KEYS):
        raise _invalid("unexpected Track A READY record")
    if payload.get("protocol") != "track-a-guarded-dispatch-v1" or payload.get("status") != "READY":
        raise _invalid("invalid Track A READY record")
    if payload.get("action_hash") != action_hash or not _is_sha256(payload.get("fence_digest")):
        raise _invalid("Track A READY fence mismatch")
    return require_exact_record(
        {"type": "ready", "action_hash": action_hash, "fence_digest": payload["fence_digest"]},
        READY_KEYS,
    )


def _normalize_private_result(payload: Any, action_hash: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise _invalid("invalid Track A RESULT record")
    keys = set(payload)
    if not keys.issubset(_PRIVATE_RESULT_KEYS) or not {"status", "effect_count", "action_hash"}.issubset(keys):
        raise _invalid("unexpected Track A RESULT record")
    if payload.get("action_hash") != action_hash:
        raise _invalid("Track A RESULT action mismatch")
    effect_count = payload.get("effect_count")
    if isinstance(effect_count, bool) or effect_count not in (0, 1):
        raise _invalid("invalid Track A RESULT effect count")
    status = payload.get("status")
    reason = payload.get("reason_code")
    if reason is not None and not isinstance(reason, str):
        raise _invalid("invalid Track A RESULT reason")
    if status == "CONFIRMED" and effect_count == 1:
        outcome, normalized_reason = "confirmed", reason
    elif status == "AMBIGUOUS":
        outcome, normalized_reason = "ambiguous", reason or "TRACK_A_RESULT_AMBIGUOUS"
    elif status == "REFUSED":
        outcome, normalized_reason = "ambiguous", reason or "TRACK_A_REFUSED_AFTER_COMMIT"
    else:
        raise _invalid("invalid Track A RESULT status")
    return normalize_result({
        "type": "result",
        "outcome": outcome,
        "reason_code": normalized_reason,
        "evidence_refs": (f"track-a:guarded-dispatch:{action_hash}",),
    })


class _LineReader:
    def __init__(self, stream: Any):
        self._queue: queue.Queue[str | None] = queue.Queue()

        def pump() -> None:
            try:
                while True:
                    line = stream.readline()
                    if line == "":
                        break
                    self._queue.put(line)
            finally:
                self._queue.put(None)

        threading.Thread(target=pump, daemon=True).start()

    def read_prefixed(self, prefix: str, timeout_seconds: float) -> str:
        deadline = time.monotonic() + timeout_seconds
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(prefix)
            try:
                line = self._queue.get(timeout=remaining)
            except queue.Empty as exc:
                raise TimeoutError(prefix) from exc
            if line is None:
                raise EOFError(prefix)
            if line.startswith(prefix):
                return line[len(prefix):].rstrip("\n")


class _GuardedSession:
    def __init__(
        self,
        process: Any,
        reader: _LineReader,
        request: ActionRequest,
        ready: dict[str, Any],
        client_state_provider: Callable[[], str],
        result_timeout_seconds: float,
    ) -> None:
        self._process = process
        self._reader = reader
        self._request = request
        self._ready = ready
        self._client_state_provider = client_state_provider
        self._result_timeout_seconds = result_timeout_seconds
        self._decision: str | None = None
        self._closed = False

    def _client_state(self) -> str:
        try:
            value = self._client_state_provider()
        except Exception:  # noqa: BLE001 -- external state provider must fail closed
            return "UNKNOWN"
        return value if value in {"IN_GAME", "LOGIN_SCREEN", "CHARACTER_SELECTION", "UNKNOWN"} else "UNKNOWN"

    def current_view(self) -> GuardedRuntimeView:
        fence = self._request.dispatch_fence
        active = not self._closed and self._process.poll() is None
        return GuardedRuntimeView(
            adapter_generation=fence.expected_adapter_generation,
            runtime_instance_id=fence.expected_runtime_instance_id,
            session_epoch=fence.expected_session_epoch,
            client_state=self._client_state(),
            authority_current=active,
            target_unique=active,
            input_lock_held=active,
            fence_digest=self._ready["fence_digest"],
        )

    def _send(self, decision: str) -> None:
        if self._decision is not None:
            raise ValidationError(
                "TRACK_A_BRIDGE_DECISION_ALREADY_SENT",
                "guarded-dispatch decision is one-shot",
            )
        self._decision = decision
        try:
            self._process.stdin.write(decision + "\n")
            self._process.stdin.flush()
        except Exception as exc:
            raise ValidationError(
                "TRACK_A_BRIDGE_DECISION_FAILED",
                "guarded-dispatch decision channel failed",
            ) from exc

    def abort_if_uncommitted(self) -> None:
        if self._decision is None:
            try:
                self._send("ABORT")
            except ValidationError:
                pass

    def cross_once_and_reconcile(self, request: ActionRequest) -> GuardedExecutionOutcome:
        if request.action_request_hash != self._request.action_request_hash:
            raise ValidationError("TRACK_A_BRIDGE_ACTION_MISMATCH", "guarded action changed")
        self._send("COMMIT")
        try:
            raw = self._reader.read_prefixed(_PRIVATE_RESULT_PREFIX, self._result_timeout_seconds)
            payload = json.loads(raw)
            normalized = _normalize_private_result(payload, self._request.action_request_hash)
        except (TimeoutError, EOFError):
            return GuardedExecutionOutcome("ambiguous", "TRACK_A_RESULT_TIMEOUT", ())
        except (json.JSONDecodeError, ValidationError):
            return GuardedExecutionOutcome("ambiguous", "TRACK_A_RESULT_INVALID", ())
        return GuardedExecutionOutcome(
            normalized["outcome"],
            normalized["reason_code"],
            tuple(normalized["evidence_refs"]),
        )

    def close(self) -> None:
        self._closed = True


class CanonicalTrackAAuthorityBridge:
    def __init__(
        self,
        repository_root: Path,
        task_id: str,
        session_id: str,
        token_file: Path,
        probe_path: Path,
        worker_path: Path,
        *,
        client_state_provider: Callable[[], str] | None = None,
        ready_timeout_seconds: float = 10.0,
        result_timeout_seconds: float = 30.0,
        process_factory: Callable[..., Any] | None = None,
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.task_id = task_id
        self.session_id = session_id
        self.token_file = Path(token_file)
        self.probe_path = self._repository_path(probe_path)
        self.worker_path = self._repository_path(worker_path)
        self.transition_path = self._repository_path(
            self.repository_root / ".github/scripts/tibia-official-client-re-canonical-live-transition.py"
        )
        self._client_state_provider = client_state_provider or (lambda: "UNKNOWN")
        self._ready_timeout_seconds = ready_timeout_seconds
        self._result_timeout_seconds = result_timeout_seconds
        self._process_factory = process_factory
        self._active_sessions: set[_GuardedSession] = set()
        self._sessions_lock = threading.Lock()

    def _repository_path(self, path: Path) -> Path:
        resolved = Path(path).resolve()
        try:
            resolved.relative_to(self.repository_root)
        except ValueError as exc:
            raise ValidationError(
                "TRACK_A_BRIDGE_PATH_INVALID",
                "bridge helper path must be repository-owned",
            ) from exc
        return resolved

    def command_for_request_file(self, request_file: Path) -> list[str]:
        return [
            sys.executable,
            str(self.transition_path),
            "guarded-dispatch",
            "--task-id", self.task_id,
            "--session-id", self.session_id,
            "--token-file", str(self.token_file),
            "--probe", str(self.probe_path),
            "--worker", str(self.worker_path),
            "--request-file", str(Path(request_file)),
        ]

    def advisory_available(self, request: ActionRequest) -> bool:
        del request
        try:
            return bool(
                self._client_state_provider() == "IN_GAME"
                and self.transition_path.is_file()
                and self.probe_path.is_file()
                and self.worker_path.is_file()
                and self.token_file.is_file()
            )
        except OSError:
            return False

    @staticmethod
    def _json_semantic(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {str(key): CanonicalTrackAAuthorityBridge._json_semantic(child) for key, child in value.items()}
        if isinstance(value, (tuple, list)):
            return [CanonicalTrackAAuthorityBridge._json_semantic(child) for child in value]
        return value

    @staticmethod
    def _request_payload(request: ActionRequest) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "action_hash": request.action_request_hash,
            "kind": request.kind,
            "parameters": CanonicalTrackAAuthorityBridge._json_semantic(request.parameters),
        }

    def _start_process(self, request_file: Path) -> Any:
        if self._process_factory is None:
            raise ValidationError(
                "TRACK_A_BRIDGE_TRANSPORT_UNBOUND",
                "Track A guarded-dispatch transport is not bound",
            )
        return self._process_factory(self.command_for_request_file(request_file), self.repository_root)

    @contextmanager
    def guarded_dispatch(self, request: ActionRequest) -> Iterator[_GuardedSession]:
        if not _is_sha256(request.action_request_hash):
            raise ValidationError("TRACK_A_BRIDGE_ACTION_HASH_INVALID", "invalid action hash")
        fd, request_name = tempfile.mkstemp(prefix=".control-center-guarded-", suffix=".json")
        request_path = Path(request_name)
        process = None
        session = None
        try:
            if hasattr(os, "fchmod"):
                os.fchmod(fd, 0o600)
            payload = json.dumps(self._request_payload(request), sort_keys=True, separators=(",", ":")) + "\n"
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            fd = -1
            process = self._start_process(request_path)
            if process.stdin is None or process.stdout is None:
                raise ValidationError("TRACK_A_BRIDGE_PROCESS_INVALID", "transition pipes unavailable")
            reader = _LineReader(process.stdout)
            try:
                raw_ready = reader.read_prefixed(_PRIVATE_READY_PREFIX, self._ready_timeout_seconds)
                ready = _normalize_private_ready(json.loads(raw_ready), request.action_request_hash)
            except (TimeoutError, EOFError) as exc:
                raise ValidationError("TRACK_A_READY_TIMEOUT", "Track A READY unavailable") from exc
            except json.JSONDecodeError as exc:
                raise _invalid("invalid Track A READY JSON") from exc
            session = _GuardedSession(
                process,
                reader,
                request,
                ready,
                self._client_state_provider,
                self._result_timeout_seconds,
            )
            with self._sessions_lock:
                self._active_sessions.add(session)
            try:
                yield session
            finally:
                session.abort_if_uncommitted()
        finally:
            if session is not None:
                session.close()
                with self._sessions_lock:
                    self._active_sessions.discard(session)
            if fd >= 0:
                os.close(fd)
            request_path.unlink(missing_ok=True)
            if process is not None:
                try:
                    process.wait(timeout=0.2)
                except TimeoutError:
                    try:
                        process.terminate()
                    except OSError:
                        pass

    def emergency_stop(self, reason: str) -> None:
        del reason
        with self._sessions_lock:
            sessions = tuple(self._active_sessions)
        for session in sessions:
            session.abort_if_uncommitted()