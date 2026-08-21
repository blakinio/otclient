from __future__ import annotations

import copy
import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from .canonical import jcs_dumps, sha256_bytes, sha256_jcs
from .model import (
    ActionLedgerRecord,
    ActionResult,
    ActionStatus,
    DispatchState,
    LifecycleState,
    RunArtifactState,
    ValidationError,
    validate_opaque_id,
)
from .recorder import (
    Recorder,
    ScreenshotDisposition,
    ScreenshotRecord,
    ensure_no_secret_material,
)


def _safe_relative_path(path: str) -> str:
    if not isinstance(path, str) or not path or path.startswith(("/", "\\")) or "\x00" in path:
        raise ValidationError("ARTIFACT_PATH_INVALID", "artifact path must be a relative logical path")
    normalized = path.replace("\\", "/")
    parts = normalized.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValidationError("ARTIFACT_PATH_INVALID", "artifact path traversal is forbidden")
    return "/".join(parts)


def _json_object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(
                "ARTIFACT_JSON_DUPLICATE_KEY",
                f"duplicate JSON key is forbidden: {key}",
            )
        result[key] = value
    return result


def _admit_public_artifact_bytes(logical: str, data: bytes, *, key_path: str) -> bytes:
    payload = bytes(data)
    try:
        decoded = payload.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValidationError(
            "ARTIFACT_PRIVACY_UNCLASSIFIED",
            "binary artifact requires a typed privacy-approved path",
        ) from exc
    if logical.endswith(".json"):
        try:
            structured = json.loads(decoded, object_pairs_hook=_json_object_without_duplicate_keys)
        except json.JSONDecodeError as exc:
            raise ValidationError(
                "ARTIFACT_STRUCTURED_INVALID",
                "JSON artifact must parse before privacy admission",
            ) from exc
        ensure_no_secret_material(structured, key_path=key_path)
    elif logical.endswith(".jsonl"):
        for line_number, line in enumerate(decoded.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                structured = json.loads(line, object_pairs_hook=_json_object_without_duplicate_keys)
            except json.JSONDecodeError as exc:
                raise ValidationError(
                    "ARTIFACT_STRUCTURED_INVALID",
                    f"JSONL artifact line {line_number} must parse before privacy admission",
                ) from exc
            ensure_no_secret_material(structured, key_path=f"{key_path}.{line_number}")
    else:
        ensure_no_secret_material(decoded, key_path=key_path)
    return payload


@dataclass
class RunArtifact:
    run_id: str
    scenario_id: str
    scenario_hash: str
    scenario_ast: Mapping[str, Any]
    adapter_identity: Mapping[str, Any]
    backend_epoch: str
    initial_control_generation: int
    started_monotonic_ns: int
    privacy_policy: Mapping[str, Any]
    state: RunArtifactState = RunArtifactState.ACTIVE
    stage: dict[str, bytes] = field(default_factory=dict)
    finalized: dict[str, bytes] = field(default_factory=dict)
    quarantine: dict[str, bytes] = field(default_factory=dict)
    supplements: dict[str, dict[str, bytes]] = field(default_factory=dict)
    final_result: Mapping[str, Any] | None = None
    final_hashes: dict[str, str] = field(default_factory=dict)


class ArtifactStore:
    """Deterministic Package A Artifact-v1 model; no filesystem or network I/O."""

    def __init__(self) -> None:
        self.runs: dict[str, RunArtifact] = {}
        self.fail_next_presentation_write = False

    def create_run(
        self,
        *,
        run_id: str,
        scenario_id: str,
        scenario_hash: str,
        scenario_ast: Mapping[str, Any],
        adapter_identity: Mapping[str, Any],
        backend_epoch: str,
        initial_control_generation: int,
        started_monotonic_ns: int,
        privacy_policy: Mapping[str, Any],
    ) -> RunArtifact:
        validate_opaque_id(run_id, field_name="run_id")
        scenario_ast_snapshot = copy.deepcopy(dict(scenario_ast))
        adapter_identity_snapshot = copy.deepcopy(dict(adapter_identity))
        privacy_policy_snapshot = copy.deepcopy(dict(privacy_policy))
        privacy_policy_for_scan = {
            f"policy_{key}": value for key, value in privacy_policy_snapshot.items()
        }
        ensure_no_secret_material(privacy_policy_for_scan, key_path="privacy_policy")
        if privacy_policy_snapshot != scenario_ast_snapshot.get("privacy_policy"):
            raise ValidationError(
                "PRIVACY_POLICY_CONTRADICTION",
                "privacy policy must match the validated scenario AST",
            )
        ensure_no_secret_material(
            {
                "run_id": run_id,
                "scenario_id": scenario_id,
                "adapter_identity": adapter_identity_snapshot,
                "backend_epoch": backend_epoch,
            },
            key_path="artifact_metadata",
        )
        privacy_scan_ast = {
            key: value for key, value in scenario_ast_snapshot.items() if key != "privacy_policy"
        }
        ensure_no_secret_material(privacy_scan_ast, key_path="scenario")
        if scenario_hash != sha256_jcs(scenario_ast_snapshot):
            raise ValidationError(
                "SCENARIO_HASH_CONTRADICTION",
                "scenario hash does not match canonical Scenario-v1 AST",
            )
        if run_id in self.runs:
            existing = self.runs[run_id]
            if existing.scenario_hash != scenario_hash:
                raise ValidationError(
                    "RUN_ARTIFACT_CONFLICT",
                    "run_id already exists with different scenario hash",
                )
            return existing
        run = RunArtifact(
            run_id=run_id,
            scenario_id=scenario_id,
            scenario_hash=scenario_hash,
            scenario_ast=scenario_ast_snapshot,
            adapter_identity=adapter_identity_snapshot,
            backend_epoch=backend_epoch,
            initial_control_generation=initial_control_generation,
            started_monotonic_ns=started_monotonic_ns,
            privacy_policy=privacy_policy_snapshot,
        )
        run.stage["scenario.json"] = jcs_dumps(scenario_ast_snapshot).encode("utf-8")
        self.runs[run_id] = run
        return run

    def _write_stage(
        self,
        run_id: str,
        path: str,
        data: bytes,
        *,
        privacy_approved: bool,
    ) -> None:
        run = self.runs[run_id]
        if run.state == RunArtifactState.FINALIZED:
            raise ValidationError("FINALIZED_IMMUTABLE", "finalized run artifacts are immutable")
        logical = _safe_relative_path(path)
        if not privacy_approved:
            data = _admit_public_artifact_bytes(
                logical, data, key_path=f"artifact_stage.{logical}"
            )
        if self.fail_next_presentation_write:
            self.fail_next_presentation_write = False
            run.state = RunArtifactState.INCOMPLETE
            raise OSError("simulated presentation write failure")
        run.stage[logical] = bytes(data)

    def write_stage(self, run_id: str, path: str, data: bytes) -> None:
        self._write_stage(run_id, path, data, privacy_approved=False)

    def store_screenshot(self, run_id: str, record: ScreenshotRecord) -> None:
        run = self.runs[run_id]
        if record.disposition == ScreenshotDisposition.SAFE and record.normal_artifact_bytes is not None:
            self._write_stage(
                run_id,
                f"screenshots/{record.screenshot_id}.bin",
                record.normal_artifact_bytes,
                privacy_approved=True,
            )
        elif record.disposition == ScreenshotDisposition.QUARANTINED and record.quarantine_bytes is not None:
            run.quarantine[record.screenshot_id] = record.quarantine_bytes

    def mark_crash(self, run_id: str) -> None:
        run = self.runs[run_id]
        if run.state != RunArtifactState.FINALIZED:
            run.state = RunArtifactState.INCOMPLETE

    def _events_jsonl(self, recorder: Recorder) -> bytes:
        lines: list[str] = []
        last = 0
        for event in recorder.events:
            if event.ingest_seq <= last:
                raise ValidationError("EVENT_SEQUENCE_INVALID", "event ingest_seq must strictly increase")
            last = event.ingest_seq
            payload = {
                "schema_version": event.schema_version,
                "event_id": event.event_id,
                "ingest_seq": event.ingest_seq,
                "ingested_monotonic_ns": event.ingested_monotonic_ns,
                "source_timestamp": event.source_timestamp,
                "source_clock_domain": event.source_clock_domain,
                "source_sequence": event.source_sequence,
                "source_sequence_scope": event.source_sequence_scope,
                "ordering_confidence": event.ordering_confidence.value,
                "late": event.late,
                "backend_epoch": event.backend_epoch,
                "control_generation": event.control_generation,
                "adapter_id": event.adapter_id,
                "adapter_generation": event.adapter_generation,
                "runtime_instance_id": event.runtime_instance_id,
                "session_epoch": event.session_epoch,
                "run_id": event.run_id,
                "experiment_id": event.experiment_id,
                "step_id": event.step_id,
                "stimulus_id": event.stimulus_id,
                "kind": event.kind,
                "sensitivity": event.sensitivity,
                "payload": dict(event.payload),
            }
            lines.append(jcs_dumps(payload))
        return (("\n".join(lines) + "\n") if lines else "").encode("utf-8")

    def finalize(
        self,
        run_id: str,
        *,
        recorder: Recorder,
        action_results: Mapping[str, ActionResult],
        requested_status: str,
        final_control_generation: int,
        budget_summary: Mapping[str, Any],
        assertions: Mapping[str, Any] | None = None,
        privacy_ok: bool = True,
        cleanup_ok: bool = True,
        safety_actions: Mapping[str, ActionLedgerRecord] | None = None,
        reason_codes: list[str] | tuple[str, ...] | None = None,
    ) -> Mapping[str, Any]:
        run = self.runs[run_id]
        if run.state == RunArtifactState.FINALIZED:
            if run.final_result is None:
                raise ValidationError("FINALIZATION_CONTRADICTION", "finalized run lacks result")
            return run.final_result
        prior_incomplete = run.state == RunArtifactState.INCOMPLETE
        if safety_actions is not None:
            self.validate_safety_precedence(action_results, safety_actions)
        run.state = RunArtifactState.CLOSING
        recorder.begin_closing()
        ambiguous = any(result.status == ActionStatus.AMBIGUOUS for result in action_results.values())
        if ambiguous:
            status = "AMBIGUOUS"
        elif prior_incomplete or not privacy_ok or not cleanup_ok:
            status = "INCOMPLETE"
        else:
            status = requested_status
        if status == "PASS" and (ambiguous or not privacy_ok or not cleanup_ok):
            status = "INCOMPLETE"
        try:
            run.stage["events.jsonl"] = self._events_jsonl(recorder)
            action_projection = {
                action_id: {
                    "lifecycle_state": result.lifecycle_state.value,
                    "status": result.status.value,
                    "dispatch_state": result.dispatch_state.value,
                    "reason_code": result.reason_code,
                }
                for action_id, result in action_results.items()
            }
            action_lines = [
                jcs_dumps({"action_id": action_id, **projection})
                for action_id, projection in sorted(action_projection.items())
            ]
            run.stage["actions.jsonl"] = (
                (("\n".join(action_lines) + "\n") if action_lines else "").encode("utf-8")
            )
            result = {
                "schema_version": 1,
                "run_id": run_id,
                "status": status,
                "first_failure_step_id": None,
                "reason_codes": [] if status == "PASS" else list(reason_codes or (status,)),
                "assertions": dict(assertions or {}),
                "action_outcomes": action_projection,
                "budget_outcome": dict(budget_summary),
                "recorder_outcome": {
                    "events": len(recorder.events),
                    "late_supplements": len(recorder.supplemental_events),
                },
                "privacy_outcome": {"ok": privacy_ok},
                "cleanup_outcome": {"ok": cleanup_ok},
                "evidence_refs": sorted(run.stage),
            }
            run.stage["result.json"] = jcs_dumps(result).encode("utf-8")
            hashes = {path: sha256_bytes(data) for path, data in sorted(run.stage.items())}
            manifest = {
                "schema_version": 1,
                "artifact_contract_major": 1,
                "run_id": run_id,
                "scenario_id": run.scenario_id,
                "scenario_hash": run.scenario_hash,
                "adapter_id": run.adapter_identity.get("adapter_id"),
                "adapter_kind": run.adapter_identity.get("adapter_kind"),
                "adapter_version": run.adapter_identity.get("adapter_version"),
                "adapter_generation_at_start": run.adapter_identity.get("adapter_generation"),
                "backend_epoch": run.backend_epoch,
                "initial_control_generation": run.initial_control_generation,
                "final_control_generation": final_control_generation,
                "runtime_instance_id_at_start": run.adapter_identity.get("runtime_instance_id"),
                "session_epoch_at_start": run.adapter_identity.get("session_epoch"),
                "state": "FINALIZED" if status != "INCOMPLETE" else "INCOMPLETE",
                "started_monotonic_ns": run.started_monotonic_ns,
                "finished_monotonic_ns": recorder.clock.now_ns(),
                "privacy_policy": dict(run.privacy_policy),
                "action_summary": action_projection,
                "budget_summary": dict(budget_summary),
                "event_summary": {"count": len(recorder.events)},
                "artifact_hashes": hashes,
                "supplements": sorted(run.supplements),
            }
            run.finalized = dict(run.stage)
            run.finalized["manifest.json"] = jcs_dumps(manifest).encode("utf-8")
            run.final_hashes = {path: sha256_bytes(data) for path, data in run.finalized.items()}
            run.final_result = result
            run.state = (
                RunArtifactState.FINALIZED if status != "INCOMPLETE" else RunArtifactState.INCOMPLETE
            )
            recorder.finalize()
            return result
        except Exception:
            run.state = RunArtifactState.INCOMPLETE
            raise

    def validate_safety_precedence(
        self,
        action_results: Mapping[str, ActionResult],
        safety_actions: Mapping[str, ActionLedgerRecord],
    ) -> None:
        for action_id, safety in safety_actions.items():
            result = action_results.get(action_id)
            if safety.dispatch_state != DispatchState.NOT_DISPATCHED and (
                result is None or result.dispatch_state == DispatchState.NOT_DISPATCHED
            ):
                raise ValidationError(
                    "SAFETY_PRESENTATION_CONTRADICTION",
                    "presentation cannot downgrade possible-dispatch safety truth",
                )
            if safety.lifecycle_state == LifecycleState.AMBIGUOUS and (
                result is None or result.status != ActionStatus.AMBIGUOUS
            ):
                raise ValidationError(
                    "SAFETY_PRESENTATION_CONTRADICTION",
                    "presentation cannot downgrade ambiguous action safety truth",
                )

    def validate_hashes(self, run_id: str) -> bool:
        run = self.runs[run_id]
        return all(
            sha256_bytes(run.finalized[path]) == digest
            for path, digest in run.final_hashes.items()
        )

    def validate_report_status(self, run_id: str, report_status: str) -> None:
        run = self.runs[run_id]
        if run.final_result is None:
            raise ValidationError("REPORT_WITHOUT_RESULT", "report cannot precede machine-readable result")
        if report_status != run.final_result["status"]:
            raise ValidationError("REPORT_RESULT_CONTRADICTION", "report contradicts machine-readable result")

    def add_supplement(self, run_id: str, supplement_id: str, files: Mapping[str, bytes]) -> None:
        run = self.runs[run_id]
        validate_opaque_id(supplement_id, field_name="supplement_id")
        if run.final_result is None:
            raise ValidationError(
                "SUPPLEMENT_BEFORE_FINALIZATION",
                "supplement requires an original final result",
            )
        if supplement_id in run.supplements:
            raise ValidationError("SUPPLEMENT_EXISTS", "supplement ID already exists")
        safe_files: dict[str, bytes] = {}
        for path, data in files.items():
            logical = _safe_relative_path(path)
            safe_files[logical] = _admit_public_artifact_bytes(
                logical,
                data,
                key_path=f"artifact_supplement.{supplement_id}.{logical}",
            )
        if "result.json" in safe_files or "manifest.json" in safe_files:
            raise ValidationError(
                "SUPPLEMENT_REWRITE_FORBIDDEN",
                "supplement cannot replace original result/manifest",
            )
        manifest = {
            "schema_version": 1,
            "supplement_id": supplement_id,
            "parent_run_id": run_id,
            "created_monotonic_ns": 0,
            "reason": "LATE_ADMITTED_EVIDENCE",
            "artifact_hashes": {
                path: sha256_bytes(data) for path, data in safe_files.items()
            },
            "evidence_refs": sorted(safe_files),
        }
        safe_files["supplement-manifest.json"] = jcs_dumps(manifest).encode("utf-8")
        run.supplements[supplement_id] = safe_files
