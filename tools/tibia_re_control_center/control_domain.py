from __future__ import annotations

import copy
import hashlib
import threading
import time
import uuid
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass, fields, replace
from enum import Enum
from typing import Any

from .artifact import ArtifactStore
from .agent_protocol import AgentProvenance, OwnerControlCommand, TaskEnvelope
from .agent_session import AgentSessionCoordinator
from .canonical import sha256_jcs
from .engine import ScenarioEngine
from .execution import MutationCoordinator
from .fake import FakeAdapter, ManualClock
from .model import (
    ActionLedgerRecord,
    AdapterKind,
    ControlState,
    DurabilityError,
    DurabilityTimeout,
    PrivacyError,
    SimulatedCrash,
    ValidationError,
    validate_opaque_id,
)
from .persistent_store import (
    RequestLedgerRecord,
    SQLitePersistentStore,
    _ensure_persistable,
)
from .recorder import Recorder, ensure_no_secret_material
from .scenario import ACTION_KINDS, ValidatedScenario, validate_scenario


@dataclass(frozen=True)
class DomainReply:
    code: int
    body: dict[str, Any]
    request_status: str = "COMPLETED"
    result_status: str | None = None
    result_ref: str | None = None


class ControlDomainError(Exception):
    def __init__(self, code: str, safe_message: str, *, http_status: int = 400, retryable: bool = False):
        super().__init__(safe_message)
        self.code = code
        self.safe_message = safe_message
        self.http_status = http_status
        self.retryable = retryable


class RuntimeMonotonicClock(ManualClock):
    """Real monotonic clock with the Package A ManualClock interface."""

    def __init__(self) -> None:
        pass

    def now_ns(self) -> int:
        return time.monotonic_ns()

    def advance_ns(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("runtime monotonic clock cannot move backwards")
        if amount:
            time.sleep(amount / 1_000_000_000)
        return self.now_ns()

    def advance_ms(self, amount: int) -> int:
        return self.advance_ns(amount * 1_000_000)

    def advance_seconds(self, amount: float) -> int:
        if amount < 0:
            raise ValueError("runtime monotonic clock cannot move backwards")
        return self.advance_ns(int(amount * 1_000_000_000))


def _jsonable(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _jsonable(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(child) for child in value]
    return value


def _exact_keys(value: Any, required: set[str]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ControlDomainError("CONTROL_BODY_INVALID", "request body must be a JSON object")
    if set(value) != required:
        raise ControlDomainError("CONTROL_BODY_INVALID", "request body has missing or unknown fields")
    return dict(value)


def _error_body(code: str, message: str, request_id: str | None, resource_id: str | None, retryable: bool) -> dict[str, Any]:
    return {
        "code": code,
        "safe_message": message,
        "request_id": request_id,
        "resource_id": resource_id,
        "retryable": retryable,
    }


class ControlDomainService:
    """Single Package B semantic path. The only mutating adapter admitted here is FakeAdapter."""

    def __init__(self, data_root: str, *, backend_epoch: str | None = None, event_retention: int = 4096) -> None:
        self.clock = RuntimeMonotonicClock()
        self.adapter = FakeAdapter(self.clock, allow_mutation=True)
        for capability in ACTION_KINDS:
            self.adapter.add_capability(capability)
        if self.adapter.identity().adapter_kind is not AdapterKind.FAKE_TEST:
            raise RuntimeError("Package B admits only the explicit FAKE_TEST adapter")
        self.store = SQLitePersistentStore(data_root, event_retention=event_retention)
        self.coordinator = MutationCoordinator(self.adapter, self.store, self.clock, backend_epoch=backend_epoch)
        self.agent = AgentSessionCoordinator(self.store, self.coordinator)
        self._request_stripes = tuple(threading.RLock() for _ in range(64))
        self._test_faults: dict[str, int] = {}

    @property
    def backend_epoch(self) -> str:
        return self.coordinator.backend_epoch

    def inject_test_crash_once(self, point: str) -> None:
        if point not in {"after_accept", "after_domain"}:
            raise ValueError("unsupported Package B crash point")
        self._test_faults[point] = self._test_faults.get(point, 0) + 1

    def _maybe_crash(self, point: str) -> None:
        remaining = self._test_faults.get(point, 0)
        if remaining:
            if remaining == 1:
                self._test_faults.pop(point, None)
            else:
                self._test_faults[point] = remaining - 1
            raise SimulatedCrash(f"simulated Package B crash at {point}")

    def normalize_post_body(self, operation: str, body: Any) -> dict[str, Any]:
        if operation == "AGENT_TASK":
            if not isinstance(body, Mapping):
                raise ControlDomainError("CONTROL_BODY_INVALID", "request body must be a JSON object")
            try:
                parsed = TaskEnvelope.from_mapping(body)
                ensure_no_secret_material(asdict(parsed), key_path="agent_task")
            except PrivacyError as exc:
                raise ControlDomainError(
                    "CONTROL_PRIVACY_REJECTED",
                    "request violates the privacy boundary",
                ) from exc
            return _jsonable(asdict(parsed))
        if operation == "AGENT_CHAT":
            data = _exact_keys(body, {"session_id", "text"})
            validate_opaque_id(data["session_id"], field_name="session_id")
            if not isinstance(data["text"], str) or not data["text"].strip():
                raise ControlDomainError("CONTROL_BODY_INVALID", "chat text must be a non-empty string")
            try:
                ensure_no_secret_material(data["text"], key_path="agent_chat.text")
            except PrivacyError as exc:
                raise ControlDomainError(
                    "CONTROL_PRIVACY_REJECTED",
                    "request violates the privacy boundary",
                ) from exc
            return {"session_id": data["session_id"], "text": data["text"]}
        if operation == "AGENT_CONTROL":
            data = _exact_keys(body, {"session_id", "command"})
            validate_opaque_id(data["session_id"], field_name="session_id")
            try:
                command = OwnerControlCommand(data["command"])
            except (TypeError, ValueError) as exc:
                raise ControlDomainError(
                    "CONTROL_BODY_INVALID",
                    "agent control command is not admitted",
                ) from exc
            return {"session_id": data["session_id"], "command": command.value}
        if operation in {"CREATE_RUN", "ONE_STEP_EXPERIMENT"}:
            data = _exact_keys(body, {"scenario"})
            if not isinstance(data["scenario"], Mapping):
                raise ControlDomainError("CONTROL_SCENARIO_INVALID", "scenario must be a JSON object")
            scenario = validate_scenario(data["scenario"])
            if operation == "ONE_STEP_EXPERIMENT" and (len(scenario.steps) != 1 or scenario.steps[0].step_type != "action"):
                raise ControlDomainError("CONTROL_ONE_STEP_REQUIRED", "one-step experiment requires exactly one action step")
            return {"scenario": copy.deepcopy(dict(scenario.ast))}
        _exact_keys(body, set())
        return {}

    def _request_hash(self, canonical_path: str, normalized_body: Mapping[str, Any]) -> str:
        return sha256_jcs({
            "api_major": 1,
            "method": "POST",
            "canonical_path": canonical_path,
            "normalized_body": dict(normalized_body),
        })

    @staticmethod
    def _resource_prefix(operation: str) -> str:
        return {
            "CREATE_RUN": "run",
            "ONE_STEP_EXPERIMENT": "experiment",
            "STOP_ALL": "stop",
            "RESET_STOP": "reset",
            "PAUSE_RUN": "pause",
            "RESUME_RUN": "resume",
            "ABORT_RUN": "abort",
            "AGENT_TASK": "agent-task",
            "AGENT_CHAT": "agent-chat",
            "AGENT_CONTROL": "agent-control",
        }[operation]

    def _new_resource_id(self, operation: str) -> str:
        return f"{self._resource_prefix(operation)}-{uuid.uuid4().hex}"

    def process_post(
        self,
        *,
        canonical_path: str,
        operation: str,
        request_id: str,
        body: Any,
        handler: Callable[[str, str, dict[str, Any]], DomainReply],
    ) -> DomainReply:
        validate_opaque_id(request_id, field_name="request_id", max_bytes=128)
        stripe_index = hashlib.sha256(request_id.encode("utf-8")).digest()[0] % len(self._request_stripes)
        with self._request_stripes[stripe_index]:
            return self._process_post_locked(
                canonical_path=canonical_path,
                operation=operation,
                request_id=request_id,
                body=body,
                handler=handler,
            )

    def _process_post_locked(
        self,
        *,
        canonical_path: str,
        operation: str,
        request_id: str,
        body: Any,
        handler: Callable[[str, str, dict[str, Any]], DomainReply],
    ) -> DomainReply:
        validate_opaque_id(request_id, field_name="request_id", max_bytes=128)
        normalized = self.normalize_post_body(operation, body)
        _ensure_persistable(normalized, key_path="control_request")
        request_hash = self._request_hash(canonical_path, normalized)
        existing = self.store.load_request(request_id)
        if existing is not None:
            if existing.request_hash != request_hash:
                raise ControlDomainError(
                    "CONTROL_IDEMPOTENCY_CONFLICT",
                    "request id is already bound to a different normalized request",
                    http_status=409,
                )
            if existing.status in {"COMPLETED", "FAILED"}:
                if existing.response_code is None or existing.response_body is None:
                    raise ControlDomainError("REQUEST_LEDGER_CONTRADICTION", "terminal request is missing its durable response", http_status=500)
                return DomainReply(
                    existing.response_code,
                    copy.deepcopy(existing.response_body),
                    existing.status,
                    existing.result_status,
                    existing.result_ref,
                )
            resource_id = existing.resource_id
        else:
            resource_id = self._new_resource_id(operation)
            now = self.clock.now_ns()
            accepted = RequestLedgerRecord(
                request_id=request_id,
                request_hash=request_hash,
                backend_epoch_created=self.backend_epoch,
                operation=operation,
                resource_id=resource_id,
                status="ACCEPTED",
                created_monotonic_ns=now,
                updated_monotonic_ns=now,
            )
            existing = self.store.accept_request(accepted)
            if existing.request_hash != request_hash:
                raise ControlDomainError("CONTROL_IDEMPOTENCY_CONFLICT", "request id conflict", http_status=409)
            resource_id = existing.resource_id
        self._maybe_crash("after_accept")
        try:
            reply = handler(resource_id, request_id, normalized)
            self._maybe_crash("after_domain")
        except SimulatedCrash:
            raise
        except ControlDomainError as exc:
            reply = DomainReply(
                exc.http_status,
                _error_body(exc.code, exc.safe_message, request_id, resource_id, exc.retryable),
                "FAILED",
                "FAILED",
                resource_id,
            )
        except PrivacyError:
            reply = DomainReply(
                400,
                _error_body("CONTROL_PRIVACY_REJECTED", "request or result violates the privacy boundary", request_id, resource_id, False),
                "FAILED",
                "FAILED",
                resource_id,
            )
        except ValidationError as exc:
            status = 409 if exc.code in {
                "MUTATION_LOCALLY_BLOCKED", "RECOVERY_STATE_MISSING", "RECOVERY_STATE_CONTRADICTORY",
                "RUN_ACTIVATION_CONFLICT", "RUN_NOT_ACTIVE", "REFUSED_MUTATION_RUN_CONFLICT",
                "IDEMPOTENCY_CONFLICT",
            } else 400
            reply = DomainReply(
                status,
                _error_body(exc.code, exc.safe_message, request_id, resource_id, False),
                "FAILED",
                "FAILED",
                resource_id,
            )
        except (DurabilityError, DurabilityTimeout):
            reply = DomainReply(
                503,
                _error_body("CONTROL_DURABILITY_FAILURE", "required durable state could not be committed", request_id, resource_id, False),
                "FAILED",
                "FAILED",
                resource_id,
            )
        except Exception:  # noqa: BLE001 - boundary sanitizes all unexpected failures
            reply = DomainReply(
                500,
                _error_body("CONTROL_INTERNAL_ERROR", "internal control operation failed safely", request_id, resource_id, False),
                "FAILED",
                "FAILED",
                resource_id,
            )
        terminal = replace(
            existing,
            status=reply.request_status,
            result_status=reply.result_status,
            result_control_generation=self.coordinator.control_generation,
            result_ref=reply.result_ref,
            response_code=reply.code,
            response_body_hash=sha256_jcs(reply.body),
            response_body=copy.deepcopy(reply.body),
            updated_monotonic_ns=self.clock.now_ns(),
        )
        self.store.finish_request(terminal)
        return reply

    def status(self) -> dict[str, Any]:
        runtime = self.adapter.runtime_status()
        identity = self.adapter.identity()
        control = self.coordinator.control_state
        capabilities = self.adapter.capabilities()
        return {
            "api_version": 1,
            "backend": {"epoch": self.backend_epoch, "state": "READY" if self.coordinator.activation_error is None else "DEGRADED"},
            "control": _jsonable(asdict(control)),
            "runtime": {
                "state": runtime.runtime_state,
                "client_state": runtime.client_state,
                "adapter_kind": identity.adapter_kind.value,
                "adapter_generation": identity.adapter_generation,
                "official_runtime_state": "NOT_PROVEN",
            },
            "recorder": {"state": runtime.recorder_state},
            "authority": {
                "state": runtime.authority_state,
                "scope": "FAKE_TEST_ONLY",
                "locally_grantable": False,
                "official_mutation_authority": "UNSUPPORTED",
            },
            "capability": {
                "state": "SUPPORTED_FAKE_ONLY",
                "count": len(capabilities),
                "official_action_capabilities": "UNSUPPORTED",
            },
            "evidence": {
                "fake_fixture": "PROVEN_SYNTHETIC",
                "official_client": "NOT_PROVEN",
                "surveyor_package_c": "NOT_INTEGRATED",
            },
            "freshness": {"fake": runtime.freshness.value, "official": "UNKNOWN"},
            "session": {
                "fake_session_epoch": identity.session_epoch,
                "fake_runtime_instance_id": identity.runtime_instance_id,
                "official_session": "UNKNOWN",
            },
            "official_client_access": "NONE",
            "agent": self.agent.foundation_status(),
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "adapter_kind": "FAKE_TEST",
            "official_client": "UNSUPPORTED",
            "items": [_jsonable(asdict(item)) for item in self.adapter.capabilities()],
        }

    @staticmethod
    def builtin_scenario() -> dict[str, Any]:
        return {
            "schema_version": 1,
            "id": "package-b-fake-move-one",
            "name": "Package B fake one-step movement",
            "adapter_requirements": {"reads": [], "actions": ["move"]},
            "preconditions": [],
            "side_effect_budget": {
                "max_runtime_seconds": 10,
                "max_actions": 1,
                "max_movement_tiles": 1,
                "max_spells": 0,
                "max_consumables": 0,
                "max_items_moved": 0,
                "max_gold": 0,
                "max_tibia_coins": 0,
                "max_irreversible_changes": 0,
            },
            "capture_policy": {"state": True, "events": True, "screenshots": "NONE", "network": "NONE", "traces": "NONE"},
            "steps": [{"action": {"id": "move-one", "kind": "move", "parameters": {"direction": "NORTH", "tiles": 1}, "timeout_ms": 1000}}],
            "abort_conditions": [],
            "expected_result": [],
            "privacy_policy": {"secret_material": "REJECT", "private_chat": "OMIT", "identities": "OMIT", "screenshots": "SAFE_ONLY"},
        }

    def scenarios(self) -> dict[str, Any]:
        scenario = validate_scenario(self.builtin_scenario())
        return {"items": [{"id": scenario.scenario_id, "hash": scenario.scenario_hash, "scenario": copy.deepcopy(dict(scenario.ast))}]}

    def _resource_reply(self, resource: dict[str, Any]) -> DomainReply | None:
        if resource.get("result") is None:
            return None
        result = copy.deepcopy(resource["result"])
        code = 201 if resource.get("operation") in {"CREATE_RUN", "ONE_STEP_EXPERIMENT"} else 200
        return DomainReply(code, result, "COMPLETED", str(result.get("status", "UNKNOWN")), resource["resource_id"])

    def _recover_incomplete_run(self, resource_id: str, request_id: str, operation: str, normalized: dict[str, Any]) -> DomainReply | None:
        resource = self.store.get_resource(resource_id)
        if resource is None:
            self.store.ensure_resource(resource_id, request_id, operation, normalized)
            return None
        prior = self._resource_reply(resource)
        if prior is not None:
            return prior
        if self.store.load_run_activation(resource_id) is None:
            return None
        actions = [record for record in self.store.action_ledgers.values() if record.run_id == resource_id]
        possibly_dispatched = any(record.dispatch_state.value != "NOT_DISPATCHED" for record in actions)
        status = "AMBIGUOUS" if possibly_dispatched else "INCOMPLETE"
        result = {
            "resource_id": resource_id,
            "run_id": resource_id,
            "status": status,
            "reason_codes": ["RECOVERY_REQUIRED_NO_AUTO_RESUME"],
            "official_client_access": "NONE",
            "adapter_kind": "FAKE_TEST",
        }
        self.store.finish_resource(resource_id, "FAILED", result)
        return DomainReply(
            409,
            _error_body("CONTROL_RUN_RECOVERY_REQUIRED", "incomplete mutation-capable run is not auto-resumed after restart", request_id, resource_id, False) | {"run_status": status},
            "FAILED",
            status,
            resource_id,
        )

    def _event_obj(self, event: Any) -> dict[str, Any]:
        return {item.name: _jsonable(getattr(event, item.name)) for item in fields(event)}

    def _execute_scenario(self, resource_id: str, request_id: str, normalized: dict[str, Any], operation: str) -> DomainReply:
        recovered = self._recover_incomplete_run(resource_id, request_id, operation, normalized)
        if recovered is not None:
            return recovered
        scenario: ValidatedScenario = validate_scenario(normalized["scenario"])
        artifacts = ArtifactStore()
        identity = self.adapter.identity()
        recorder = Recorder(
            self.clock,
            backend_epoch=self.backend_epoch,
            adapter_id=identity.adapter_id,
            adapter_generation=identity.adapter_generation,
            control_generation=self.coordinator.control_generation,
        )
        engine = ScenarioEngine(adapter=self.adapter, coordinator=self.coordinator, artifacts=artifacts, recorder=recorder)
        result = engine.run(scenario, run_id=resource_id)
        action_projection = {
            action_id: {
                "lifecycle_state": action.lifecycle_state.value,
                "status": action.status.value,
                "dispatch_state": action.dispatch_state.value,
                "reason_code": action.reason_code,
            }
            for action_id, action in result.action_results.items()
        }
        payload = {
            "resource_id": resource_id,
            "run_id": resource_id,
            "scenario_id": scenario.scenario_id,
            "scenario_hash": scenario.scenario_hash,
            "status": result.status,
            "reason_codes": list(result.reason_codes),
            "assertions": dict(result.assertions),
            "actions": action_projection,
            "adapter_kind": "FAKE_TEST",
            "official_client_access": "NONE",
        }
        run_artifact = artifacts.runs[resource_id]
        if run_artifact.finalized:
            self.store.persist_artifacts(resource_id, run_artifact.finalized, run_artifact.final_hashes)
        self.store.append_events(resource_id, [self._event_obj(event) for event in recorder.events])
        self.store.finish_resource(resource_id, "COMPLETED", payload)
        return DomainReply(201, payload, "COMPLETED", result.status, resource_id)

    def create_run(self, resource_id: str, request_id: str, normalized: dict[str, Any]) -> DomainReply:
        return self._execute_scenario(resource_id, request_id, normalized, "CREATE_RUN")

    def one_step(self, resource_id: str, request_id: str, normalized: dict[str, Any]) -> DomainReply:
        return self._execute_scenario(resource_id, request_id, normalized, "ONE_STEP_EXPERIMENT")

    def _transition_payload(self, state: ControlState, resource_id: str) -> dict[str, Any]:
        return {
            "resource_id": resource_id,
            "transition_id": state.transition_id,
            "stop_latched": state.stop_latched,
            "recovery_required": state.recovery_required,
            "control_generation": state.control_generation,
            "reason_code": state.reason_code,
            "official_client_access": "NONE",
        }

    def stop_all(self, resource_id: str, request_id: str, normalized: dict[str, Any]) -> DomainReply:
        resource = self.store.ensure_resource(resource_id, request_id, "STOP_ALL", normalized)
        prior = self._resource_reply(resource)
        if prior is not None:
            return prior
        historical = self.store.load_control_transition(resource_id)
        if historical is None:
            if not self.coordinator.stop_all(transition_id=resource_id, reason_code="CONTROL_API_STOP_ALL"):
                raise ControlDomainError("CONTROL_STOP_DURABILITY_FAILED", "STOP could not be durably committed", http_status=503)
            historical = self.store.load_control_transition(resource_id)
        if historical is None:
            raise ControlDomainError("CONTROL_STATE_CONTRADICTION", "STOP transition history is missing", http_status=500)
        payload = self._transition_payload(historical, resource_id)
        self.store.finish_resource(resource_id, "COMPLETED", payload)
        return DomainReply(200, payload, "COMPLETED", "STOPPED", resource_id)

    def reset_stop(self, resource_id: str, request_id: str, normalized: dict[str, Any]) -> DomainReply:
        resource = self.store.ensure_resource(resource_id, request_id, "RESET_STOP", normalized)
        prior = self._resource_reply(resource)
        if prior is not None:
            return prior
        historical = self.store.load_control_transition(resource_id)
        if historical is None:
            if not self.coordinator.reset_stop(transition_id=resource_id, reason_code="CONTROL_API_RESET_STOP"):
                raise ControlDomainError("CONTROL_RESET_REFUSED", "STOP reset is refused while safety state is unresolved", http_status=409)
            historical = self.store.load_control_transition(resource_id)
        if historical is None:
            raise ControlDomainError("CONTROL_STATE_CONTRADICTION", "reset transition history is missing", http_status=500)
        payload = self._transition_payload(historical, resource_id)
        self.store.finish_resource(resource_id, "COMPLETED", payload)
        return DomainReply(200, payload, "COMPLETED", "RESET", resource_id)

    def run_control(self, resource_id: str, request_id: str, normalized: dict[str, Any], *, operation: str, run_id: str) -> DomainReply:
        validate_opaque_id(run_id, field_name="run_id")
        resource = self.store.ensure_resource(resource_id, request_id, operation, {"target_run_id": run_id})
        prior = self._resource_reply(resource)
        if prior is not None:
            return prior
        run = self.coordinator.runs.get(run_id)
        if run is None:
            raise ControlDomainError("CONTROL_RUN_NOT_ACTIVE", "run is not active in this backend", http_status=409)
        if operation == "PAUSE_RUN":
            self.coordinator.pause_run(run_id)
            state = "PAUSED"
        elif operation == "RESUME_RUN":
            if not self.coordinator.resume_run(run_id):
                raise ControlDomainError("CONTROL_RUN_RESUME_REFUSED", "run resume is refused by current safety state", http_status=409)
            state = "RUNNING"
        else:
            run.cancelled = True
            state = "ABORTED"
        payload = {"resource_id": resource_id, "run_id": run_id, "state": state, "official_client_access": "NONE"}
        self.store.finish_resource(resource_id, "COMPLETED", payload)
        return DomainReply(200, payload, "COMPLETED", state, resource_id)

    @staticmethod
    def _latest_agent_event(events: list[dict[str, Any]], kind: str) -> dict[str, Any] | None:
        return next((event for event in reversed(events) if event.get("kind") == kind), None)

    def _safe_agent_snapshot(self, session_id: str) -> dict[str, Any]:
        snapshot = _jsonable(self.agent.snapshot(session_id))
        events = snapshot.get("events")
        if not isinstance(events, list):
            events = []
        capture_event = self._latest_agent_event(events, "SCREENSHOT_RESULT")
        capture: dict[str, Any] = {
            "status": "UNAVAILABLE",
            "artifact_ref": None,
            "sha256": None,
            "secret_safe": True,
        }
        if capture_event is not None:
            payload = capture_event.get("payload")
            refs = capture_event.get("artifact_refs")
            if isinstance(payload, dict) and payload.get("secret_safe") is True:
                capture = {
                    "status": payload.get("status", "UNAVAILABLE"),
                    "artifact_ref": refs[0] if isinstance(refs, list) and refs else None,
                    "sha256": payload.get("sha256"),
                    "secret_safe": True,
                }
        action_event = next(
            (
                event for event in reversed(events)
                if event.get("kind") in {"ACTION_RESULT", "ACTION_REFUSED", "MODEL_ACTION_PROPOSED"}
            ),
            None,
        )
        snapshot["dashboard"] = {
            "latest_secret_safe_capture": capture,
            "visual": {
                "label": "UNKNOWN",
                "ocr": [],
                "visual_only": True,
                "structural_authority": False,
            },
            "runtime_evidence_class": "UNKNOWN",
            "reconciliation_state": "UNKNOWN",
            "latest_action": action_event,
            "provenance_timeline": events,
        }
        ensure_no_secret_material(snapshot, key_path="agent_response")
        return snapshot

    def agent_session(self, session_id: str) -> dict[str, Any]:
        validate_opaque_id(session_id, field_name="session_id")
        if self.store.load_agent_session(session_id) is None:
            raise ControlDomainError("CONTROL_AGENT_SESSION_NOT_FOUND", "agent session was not found", http_status=404)
        return self._safe_agent_snapshot(session_id)

    def agent_events(self, session_id: str, *, cursor: int, limit: int) -> dict[str, Any]:
        validate_opaque_id(session_id, field_name="session_id")
        if self.store.load_agent_session(session_id) is None:
            raise ControlDomainError("CONTROL_AGENT_SESSION_NOT_FOUND", "agent session was not found", http_status=404)
        retained, high_watermark = self.store.list_events(
            cursor=cursor,
            limit=self.store.event_retention,
        )
        items = [event for event in retained if event.get("session_id") == session_id][:limit]
        ensure_no_secret_material(items, key_path="agent_events_response")
        return {
            "session_id": session_id,
            "items": items,
            "cursor": cursor,
            "high_watermark": high_watermark,
            "delivery": "BOUNDED_POLLING",
        }

    def _agent_task_for_run(self, run_id: str) -> dict[str, object] | None:
        return self.store.load_agent_task_for_run(run_id)

    def agent_result(self, run_id: str) -> dict[str, Any]:
        validate_opaque_id(run_id, field_name="run_id")
        task = self._agent_task_for_run(run_id)
        if task is None:
            raise ControlDomainError("CONTROL_AGENT_RESULT_NOT_FOUND", "agent result was not found", http_status=404)
        result = task.get("result")
        if result is None:
            return {"run_id": run_id, "status": "PENDING", "result": None}
        if not isinstance(result, dict):
            raise ControlDomainError("CONTROL_AGENT_RESULT_INVALID", "agent result is invalid", http_status=500)
        ensure_no_secret_material(result, key_path="agent_result_response")
        return copy.deepcopy(result)

    def agent_submit_task(self, resource_id: str, request_id: str, normalized: dict[str, Any]) -> DomainReply:
        del request_id
        accepted = self.agent.submit_task(TaskEnvelope.from_mapping(normalized))
        envelope = accepted["envelope"]
        if not isinstance(envelope, dict):
            raise ControlDomainError("CONTROL_AGENT_TASK_INVALID", "accepted agent task is invalid", http_status=500)
        session_id = str(envelope["session_id"])
        run_id = str(envelope["run_id"])
        payload = {
            "resource_id": resource_id,
            "status": "ACCEPTED",
            "accepted_new": bool(accepted["accepted_new"]),
            "provenance": AgentProvenance.SUPERVISOR.value,
            "session": self._safe_agent_snapshot(session_id),
        }
        return DomainReply(201, payload, "COMPLETED", "ACCEPTED", run_id)

    def agent_chat(self, resource_id: str, request_id: str, normalized: dict[str, Any]) -> DomainReply:
        del request_id
        result = self.agent.record_message(
            normalized["session_id"],
            AgentProvenance.OWNER,
            normalized["text"],
        )
        session = result.get("session")
        payload = {
            "resource_id": resource_id,
            "status": result.get("status", "RECORDED"),
            "provenance": AgentProvenance.OWNER.value,
            "session": self._safe_agent_snapshot(normalized["session_id"]) if session is not None else None,
        }
        return DomainReply(200, payload, "COMPLETED", str(payload["status"]), normalized["session_id"])

    def agent_control(self, resource_id: str, request_id: str, normalized: dict[str, Any]) -> DomainReply:
        del request_id
        result = self.agent.owner_control(normalized["session_id"], normalized["command"])
        payload = {
            "resource_id": resource_id,
            "status": result.get("status", "UNKNOWN"),
            "provenance": AgentProvenance.OWNER.value,
            "session": self._safe_agent_snapshot(normalized["session_id"]),
        }
        return DomainReply(200, payload, "COMPLETED", str(payload["status"]), normalized["session_id"])

    def list_runs(self, *, offset: int = 0, limit: int = 100) -> dict[str, Any]:
        items = []
        for resource in self.store.list_run_resources(offset=offset, limit=limit):
            result = resource.get("result") or {}
            items.append({
                "run_id": resource.get("resource_id"),
                "operation": resource.get("operation"),
                "state": resource.get("state"),
                "status": result.get("status", "UNKNOWN"),
                "scenario_id": result.get("scenario_id") or (resource.get("body") or {}).get("scenario", {}).get("id"),
            })
        return {"items": items, "offset": offset, "limit": limit}

    def run_detail(self, run_id: str) -> dict[str, Any]:
        validate_opaque_id(run_id, field_name="run_id")
        resource = self.store.get_resource(run_id)
        if resource is None or resource.get("operation") not in {"CREATE_RUN", "ONE_STEP_EXPERIMENT"}:
            raise ControlDomainError("CONTROL_RUN_NOT_FOUND", "run was not found", http_status=404)
        return {
            "run_id": run_id,
            "operation": resource["operation"],
            "state": resource["state"],
            "result": resource["result"],
            "artifacts": self.store.list_artifacts(run_id),
        }

    def action_detail(self, action_id: str) -> dict[str, Any]:
        validate_opaque_id(action_id, field_name="action_id", max_bytes=192)
        record: ActionLedgerRecord | None = self.store.load_action(action_id)
        if record is None:
            raise ControlDomainError("CONTROL_ACTION_NOT_FOUND", "action was not found", http_status=404)
        return _jsonable(asdict(record))

    def events(self, *, cursor: int = 0, limit: int = 100) -> dict[str, Any]:
        items, high_watermark = self.store.list_events(cursor=cursor, limit=limit)
        return {"items": items, "cursor": cursor, "high_watermark": high_watermark, "delivery": "BOUNDED_POLLING"}

    def artifacts(self, run_id: str) -> dict[str, Any]:
        self.run_detail(run_id)
        return {"run_id": run_id, "items": self.store.list_artifacts(run_id)}

    def close(self) -> bool:
        clean = self.coordinator.clean_shutdown()
        self.store.close()
        return clean
