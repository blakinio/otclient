from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from typing import Any, ClassVar

from .artifact import ArtifactStore
from .execution import MutationCoordinator
from .fake import FakeAdapter
from .model import (
    ActionRequest,
    ActionResult,
    ActionStatus,
    AdapterIdentity,
    Authority,
    DispatchFence,
    negotiate_major,
)
from .recorder import Recorder
from .scenario import (
    PredicateOutcome,
    ValidatedScenario,
    action_request_hash,
    evaluate_predicate,
    resolve_unknown_policy,
    validate_abort_condition,
    validate_predicate,
)


@dataclass(frozen=True)
class EngineRunResult:
    run_id: str
    status: str
    action_results: Mapping[str, ActionResult]
    assertions: Mapping[str, bool]
    reason_codes: tuple[str, ...] = ()
    artifact_result: Mapping[str, Any] = field(default_factory=dict)


class ScenarioEngine:
    """Deterministic Package A scenario executor over the semantic fake adapter."""

    REQUIRED_MAJORS: ClassVar[dict[str, int]] = {
        "adapter": 1,
        "execution": 1,
        "scenario": 1,
        "artifact": 1,
    }

    def __init__(
        self,
        *,
        adapter: FakeAdapter,
        coordinator: MutationCoordinator,
        artifacts: ArtifactStore,
        recorder: Recorder,
        supported_contracts: Mapping[str, list[int]] | None = None,
    ) -> None:
        self.adapter = adapter
        self.coordinator = coordinator
        self.artifacts = artifacts
        self.recorder = recorder
        self.supported_contracts = dict(supported_contracts or {
            "adapter": [1],
            "execution": [1],
            "scenario": [1],
            "artifact": [1],
        })

    def negotiate_contracts(self) -> None:
        for name, required in self.REQUIRED_MAJORS.items():
            negotiate_major(required, self.supported_contracts.get(name, []), contract_name=name)

    @staticmethod
    def _snapshot_mapping(snapshot: Any) -> dict[str, Any]:
        return {
            "client_state": snapshot.client_state,
            "player": dict(snapshot.player),
            "conditions": snapshot.conditions,
            "action_state": snapshot.action_state,
            "target": snapshot.target,
            "inventory": snapshot.inventory,
            "containers": snapshot.containers,
            "battle_list": snapshot.battle_list,
            "source_quality": dict(snapshot.source_quality),
        }

    @staticmethod
    def _identity_mapping(identity: AdapterIdentity) -> dict[str, Any]:
        data = asdict(identity)
        data["adapter_kind"] = identity.adapter_kind.value
        return data

    def _budget_summary(self, run_id: str) -> dict[str, Any]:
        run = self.coordinator.runs[run_id]
        return {
            "runtime": {
                "limit_seconds": run.budget.limit_seconds,
                "started_monotonic_ns": run.budget.started_monotonic_ns,
                "deadline_monotonic_ns": run.budget.deadline_monotonic_ns,
                "expired": run.budget.expired,
            },
            "effect_dimensions": {
                name: {
                    "limit": dimension.limit,
                    "reserved": dimension.reserved,
                    "at_risk": dimension.at_risk,
                    "committed": dimension.committed,
                    "uncertain": dimension.uncertain,
                }
                for name, dimension in run.budget.dimensions.items()
            },
        }

    def _action_request(self, run_id: str, step: Any, attempt_index: int = 1) -> ActionRequest:
        identity = self.adapter.identity()
        kind = str(step.body["kind"])
        parameters = dict(step.body["parameters"])
        capability = kind
        effect_bound = self.adapter.effect_bound(kind, parameters)
        request_hash = action_request_hash(
            schema_version=1,
            run_id=run_id,
            step_id=step.step_id,
            attempt_index=attempt_index,
            kind=kind,
            parameters=parameters,
            timeout_ms=int(step.body["timeout_ms"]),
            required_capability=capability,
            required_authority=Authority.MUTATION,
        )
        return ActionRequest(
            action_id=f"{run_id}:{step.step_id}:attempt-{attempt_index}",
            run_id=run_id,
            step_id=step.step_id,
            attempt_index=attempt_index,
            kind=kind,
            parameters=parameters,
            timeout_ms=int(step.body["timeout_ms"]),
            required_capability=capability,
            required_authority=Authority.MUTATION,
            dispatch_fence=DispatchFence(
                expected_backend_epoch=self.coordinator.backend_epoch,
                expected_control_generation=self.coordinator.control_generation,
                expected_adapter_generation=identity.adapter_generation,
                expected_runtime_instance_id=identity.runtime_instance_id,
                expected_session_epoch=identity.session_epoch,
            ),
            effect_bound=effect_bound,
            action_request_hash=request_hash,
        )

    def _abort_reason(self, scenario: ValidatedScenario, snapshot: Mapping[str, Any]) -> str | None:
        for raw in scenario.ast["abort_conditions"]:
            condition, _ = validate_abort_condition(raw)
            outcome = evaluate_predicate(condition.condition, snapshot)
            if outcome != PredicateOutcome.FALSE:
                return condition.reason_code
        return None

    def run(self, scenario: ValidatedScenario, *, run_id: str) -> EngineRunResult:
        self.negotiate_contracts()
        run = self.coordinator.start_run(
            run_id,
            scenario.side_effect_budget,
            mutation_capable=scenario.mutation_capable,
        )
        identity = self.adapter.identity()
        self.artifacts.create_run(
            run_id=run_id,
            scenario_id=scenario.scenario_id,
            scenario_hash=scenario.scenario_hash,
            scenario_ast=scenario.ast,
            adapter_identity=self._identity_mapping(identity),
            backend_epoch=self.coordinator.backend_epoch,
            initial_control_generation=self.coordinator.control_generation,
            started_monotonic_ns=run.budget.started_monotonic_ns,
            privacy_policy=scenario.ast["privacy_policy"],
        )
        action_results: dict[str, ActionResult] = {}
        assertions: dict[str, bool] = {}
        reason_codes: list[str] = []
        last_snapshot: Mapping[str, Any] | None = None
        status = "PASS"
        try:
            current = self._snapshot_mapping(self.adapter.snapshot())
            for raw in scenario.ast["preconditions"]:
                predicate, _ = validate_predicate(raw, safety_context=True)
                if resolve_unknown_policy(evaluate_predicate(predicate, current), predicate.unknown_policy) is not True:
                    status = "REFUSED"
                    reason_codes.append("PRECONDITION_FAILED")
                    break
            if status == "PASS":
                for step in scenario.steps:
                    current = self._snapshot_mapping(self.adapter.snapshot())
                    abort_reason = self._abort_reason(scenario, current)
                    if abort_reason is not None:
                        status = "CANCELLED"
                        reason_codes.append(abort_reason)
                        break
                    if step.step_type in {"snapshot", "checkpoint"}:
                        last_snapshot = current
                        self.recorder.record_event(
                            kind="SNAPSHOT",
                            payload={"snapshot_id": self.adapter.snapshot().snapshot_id},
                            run_id=run_id,
                            step_id=step.step_id,
                        )
                    elif step.step_type == "assert":
                        predicate, _ = validate_predicate(step.body["condition"])
                        passed = resolve_unknown_policy(
                            evaluate_predicate(predicate, current, checkpoint=last_snapshot),
                            predicate.unknown_policy,
                        ) is True
                        assertions[step.step_id] = passed
                        if not passed:
                            status = "FAIL"
                            reason_codes.append("ASSERTION_FAILED")
                            break
                    elif step.step_type == "wait":
                        predicate, _ = validate_predicate(step.body["condition"])
                        checkpoint = last_snapshot

                        def ready(
                            bound_predicate=predicate,
                            bound_checkpoint=checkpoint,
                        ) -> bool:
                            observed = self._snapshot_mapping(self.adapter.snapshot())
                            return resolve_unknown_policy(
                                evaluate_predicate(
                                    bound_predicate,
                                    observed,
                                    checkpoint=bound_checkpoint,
                                ),
                                bound_predicate.unknown_policy,
                            ) is True

                        wait_result = self.coordinator.wait_until(
                            run_id,
                            ready,
                            timeout_ms=int(step.body["timeout_ms"]),
                        )
                        if wait_result != "READY":
                            status = "TIMEOUT" if wait_result == "TIMEOUT" else "CANCELLED"
                            reason_codes.append(f"WAIT_{wait_result}")
                            break
                    elif step.step_type == "action":
                        request = self._action_request(run_id, step)
                        result = self.coordinator.execute_action(request)
                        action_results[request.action_id] = result
                        self.recorder.set_terminal_result(request.action_id, result.lifecycle_state.value)
                        self.recorder.record_event(
                            kind="ACTION",
                            payload={
                                "action_id": request.action_id,
                                "lifecycle_state": result.lifecycle_state.value,
                                "dispatch_state": result.dispatch_state.value,
                            },
                            run_id=run_id,
                            step_id=step.step_id,
                            stimulus_id=request.action_id,
                        )
                        if result.status != ActionStatus.PASS:
                            status = result.status.value
                            reason_codes.append(result.reason_code or result.status.value)
                            break
            if status == "PASS":
                current = self._snapshot_mapping(self.adapter.snapshot())
                for index, raw in enumerate(scenario.ast["expected_result"], 1):
                    predicate, _ = validate_predicate(raw)
                    passed = resolve_unknown_policy(
                        evaluate_predicate(predicate, current, checkpoint=last_snapshot),
                        predicate.unknown_policy,
                    ) is True
                    assertions[f"expected-{index}"] = passed
                    if not passed:
                        status = "FAIL"
                        reason_codes.append("EXPECTED_RESULT_FAILED")
                        break
            artifact_result = self.artifacts.finalize(
                run_id,
                recorder=self.recorder,
                action_results=action_results,
                requested_status=status,
                final_control_generation=self.coordinator.control_generation,
                budget_summary=self._budget_summary(run_id),
                assertions=assertions,
                safety_actions=self.coordinator.store.action_ledgers,
            )
            return EngineRunResult(
                run_id,
                str(artifact_result["status"]),
                action_results,
                assertions,
                tuple(reason_codes),
                artifact_result,
            )
        except Exception:
            self.artifacts.mark_crash(run_id)
            raise
        finally:
            self.coordinator.finish_run(run_id)
