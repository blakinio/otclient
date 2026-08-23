from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from .model import ValidationError

READY_KEYS = frozenset({"type", "action_hash", "fence_digest"})
RESULT_KEYS = frozenset({"type", "outcome", "reason_code", "evidence_refs"})
ALLOWED_OUTCOMES = frozenset({"confirmed", "ambiguous"})


def require_exact_record(value: Any, keys: frozenset[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValidationError(
            "TRACK_A_BRIDGE_PROTOCOL_INVALID",
            "unexpected guarded-dispatch record",
        )
    return value


def normalize_result(value: Any) -> dict[str, Any]:
    record = require_exact_record(value, RESULT_KEYS)
    if record["type"] != "result" or record["outcome"] not in ALLOWED_OUTCOMES:
        raise ValidationError(
            "TRACK_A_BRIDGE_PROTOCOL_INVALID",
            "invalid guarded-dispatch result",
        )
    reason = record["reason_code"]
    refs = record["evidence_refs"]
    if reason is not None and not isinstance(reason, str):
        raise ValidationError("TRACK_A_BRIDGE_PROTOCOL_INVALID", "invalid result reason")
    if not isinstance(refs, (tuple, list)) or not all(isinstance(ref, str) for ref in refs):
        raise ValidationError("TRACK_A_BRIDGE_PROTOCOL_INVALID", "invalid evidence refs")
    return {
        "type": "result",
        "outcome": record["outcome"],
        "reason_code": reason,
        "evidence_refs": tuple(refs),
    }


class CanonicalTrackAAuthorityBridge:
    def __init__(
        self,
        repository_root: Path,
        task_id: str,
        session_id: str,
        token_file: Path,
        probe_path: Path,
        worker_path: Path,
    ) -> None:
        self.repository_root = Path(repository_root).resolve()
        self.task_id = task_id
        self.session_id = session_id
        self.token_file = Path(token_file)
        self.probe_path = self._repository_path(probe_path)
        self.worker_path = self._repository_path(worker_path)
        self.transition_path = self._repository_path(
            self.repository_root
            / ".github/scripts/tibia-official-client-re-canonical-live-transition.py"
        )

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
            "--task-id",
            self.task_id,
            "--session-id",
            self.session_id,
            "--token-file",
            str(self.token_file),
            "--probe",
            str(self.probe_path),
            "--worker",
            str(self.worker_path),
            "--request-file",
            str(Path(request_file)),
        ]