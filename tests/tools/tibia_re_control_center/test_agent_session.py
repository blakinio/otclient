from __future__ import annotations

import tempfile
import threading
import unittest
from dataclasses import replace
from pathlib import Path

from tools.tibia_re_control_center.agent_protocol import (
    AgentProvenance,
    ClientIdentity,
    NamedAgentAction,
    OwnerControlCommand,
    ResultEnvelope,
    ResultStatus,
    TaskEnvelope,
)
from tools.tibia_re_control_center.agent_session import (
    AgentActionReceipt,
    AgentSessionCoordinator,
    CaptureReceipt,
    NullBoundedActionExecutor,
)
from tools.tibia_re_control_center.control_domain import ControlDomainService
from tools.tibia_re_control_center.execution import MutationCoordinator
from tools.tibia_re_control_center.fake import FakeAdapter, ManualClock
from tools.tibia_re_control_center.model import PrivacyError, ValidationError
from tools.tibia_re_control_center.persistent_store import SQLitePersistentStore


def task(**overrides) -> TaskEnvelope:
    values = {
        "schema": "otclient.local-agent.task.v1",
        "session_id": "session-1",
        "task_id": "task-1",
        "run_id": "run-1",
        "idempotency_key": "idem-1",
        "trusted_main_sha": "a" * 40,
        "client_identity": ClientIdentity("NOT_APPLICABLE", "NOT_APPLICABLE", "b" * 64),
        "objective": "bounded offline coordinator test",
        "allowed_actions": (NamedAgentAction.ENTER_WORLD, NamedAgentAction.SCREENSHOT),
        "physical_action_budget": 1,
        "max_attempts": 2,
        "deadline_epoch_ms": 4_000_000_000_000,
        "runtime_access": "none",
        "required_evidence": ("action",),
        "secret_capability_ref": None,
    }
    values.update(overrides)
    return TaskEnvelope(**values)


class FakeExecutor:
    def __init__(self, receipts=None, *, capture=None):
        self.receipts = list(receipts or [])
        self.capture = capture or CaptureReceipt("CAPTURED", "artifact-safe", "c" * 64, True)
        self.execute_calls = []
        self.screenshot_calls = []
        self.barrier = None

    def execute(self, request):
        self.execute_calls.append(request)
        if self.barrier is not None:
            self.barrier.wait(timeout=2)
        if self.receipts:
            value = self.receipts.pop(0)
            if isinstance(value, BaseException):
                raise value
            return value
        return AgentActionReceipt(request.action_id, "PERFORMED", True, True, 1, ("effect-safe",))

    def screenshot(self, session_id, run_id):
        self.screenshot_calls.append((session_id, run_id))
        return self.capture


class AgentSessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = SQLitePersistentStore(self.root)
        self.clock = ManualClock()
        self.adapter = FakeAdapter(self.clock, allow_mutation=True)
        self.control = MutationCoordinator(self.adapter, self.store, self.clock, backend_epoch="backend-test")
        self.executor = FakeExecutor()
        self.agent = AgentSessionCoordinator(self.store, self.control, self.executor)

    def tearDown(self):
        try:
            self.store.close()
        except Exception:
            pass
        self.temp.cleanup()

    def restart(self, *, clean=True, executor=None):
        if clean:
            self.control.clean_shutdown()
        self.store.close()
        self.store = SQLitePersistentStore(self.root)
        self.clock = ManualClock()
        self.adapter = FakeAdapter(self.clock, allow_mutation=True)
        self.control = MutationCoordinator(self.adapter, self.store, self.clock, backend_epoch="backend-restart")
        self.executor = executor or FakeExecutor()
        self.agent = AgentSessionCoordinator(self.store, self.control, self.executor)

    def submit(self, **overrides):
        return self.agent.submit_task(task(**overrides))

    def propose(self, action_id="action-1", **overrides):
        values = {
            "session_id": "session-1",
            "action_id": action_id,
            "action": NamedAgentAction.ENTER_WORLD,
            "provenance": AgentProvenance.SUPERVISOR,
            "expected_source_states": ("CHARACTER_SELECT",),
            "current_state": "CHARACTER_SELECT",
        }
        values.update(overrides)
        return self.agent.propose_named_action(**values)

    def test_exact_null_executor_receipts_have_zero_effect(self):
        null = NullBoundedActionExecutor()
        self.agent = AgentSessionCoordinator(self.store, self.control, null)
        self.submit()
        receipt = self.propose()
        self.assertEqual("REFUSED_EXECUTOR_UNBOUND", receipt.status)
        self.assertFalse(receipt.performed)
        self.assertTrue(receipt.outcome_known)
        self.assertEqual(0, receipt.low_level_event_count)
        capture = self.agent.owner_control("session-1", OwnerControlCommand.SCREENSHOT)
        self.assertEqual("UNAVAILABLE", capture["capture"]["status"])
        self.assertEqual(0, self.agent.snapshot("session-1")["physical_action_count"])

    def test_pause_and_stop_dominate_supervisor_and_model(self):
        self.submit()
        self.agent.owner_control("session-1", OwnerControlCommand.PAUSE)
        paused = self.propose("paused-action")
        self.assertEqual("REFUSED_OWNER_PAUSED", paused.status)
        model = self.propose("model-action", provenance=AgentProvenance.MODEL)
        self.assertEqual("REFUSED_OWNER_PAUSED", model.status)
        self.agent.owner_control("session-1", OwnerControlCommand.STOP)
        stopped = self.propose("stopped-action")
        self.assertEqual("REFUSED_SYSTEM_STOPPED", stopped.status)
        self.assertEqual([], self.executor.execute_calls)
        snapshot = self.agent.snapshot("session-1")
        self.assertEqual("run-1", snapshot["current_run_id"])
        self.assertTrue(snapshot["stop_latched"])
        self.assertGreaterEqual(len(snapshot["events"]), 4)

    def test_pause_and_stop_latches_reconstruct_directly_after_restart(self):
        self.submit()
        self.agent.owner_control("session-1", OwnerControlCommand.PAUSE)
        self.restart(clean=True)
        paused = self.agent.ensure_session("session-1")
        self.assertTrue(paused.pause_latched)
        self.assertEqual("PAUSED", paused.operational_state.value)

        self.agent.owner_control("session-1", OwnerControlCommand.STOP)
        self.restart(clean=True)
        stopped = self.agent.ensure_session("session-1")
        self.assertTrue(stopped.stop_latched)
        self.assertEqual("STOPPED", stopped.operational_state.value)

    def test_restart_never_auto_resumes_an_accepted_run(self):
        self.submit()
        self.restart(clean=True)
        replay = self.submit()
        self.assertFalse(replay["accepted_new"])
        self.assertEqual("PAUSED_AUTHORITY", self.agent.snapshot("session-1")["operational_state"])
        self.assertEqual("REFUSED_AUTHORITY_RECONCILIATION_REQUIRED", self.propose().status)

    def test_resume_refuses_global_stop_recovery_and_in_memory_blocks(self):
        self.submit()
        self.agent.owner_control("session-1", OwnerControlCommand.PAUSE)
        self.control.control_state = replace(self.control.control_state, stop_latched=True)
        refused = self.agent.owner_control("session-1", OwnerControlCommand.RESUME)
        self.assertEqual("REFUSED_GLOBAL_STOP_LATCHED", refused["status"])
        self.assertTrue(self.agent.snapshot("session-1")["pause_latched"])

        self.control.control_state = replace(self.control.control_state, stop_latched=False, recovery_required=True)
        self.assertEqual("REFUSED_GLOBAL_RECOVERY_REQUIRED", self.agent.owner_control("session-1", "RESUME")["status"])
        self.control.control_state = replace(self.control.control_state, recovery_required=False)
        self.control.in_memory_stop = True
        self.assertEqual("REFUSED_GLOBAL_MUTATION_DISABLED", self.agent.owner_control("session-1", "RESUME")["status"])

    def test_resume_never_resets_global_stop(self):
        self.submit()
        self.agent.owner_control("session-1", OwnerControlCommand.STOP)
        generation = self.control.control_generation
        self.assertEqual("REFUSED_GLOBAL_STOP_LATCHED", self.agent.owner_control("session-1", "RESUME")["status"])
        self.assertTrue(self.control.control_state.stop_latched)
        self.assertEqual(generation, self.control.control_generation)

    def test_owner_token_parsing_precedes_message_and_non_owner_cannot_control(self):
        self.submit()
        result = self.agent.record_message("session-1", AgentProvenance.OWNER, "  PAUSE  ")
        self.assertEqual("PAUSED", result["status"])
        before = self.agent.snapshot("session-1")["last_event_seq"]
        result = self.agent.record_message("session-1", AgentProvenance.MODEL, "STOP")
        self.assertEqual("RECORDED", result["status"])
        snapshot = self.agent.snapshot("session-1")
        self.assertFalse(snapshot["stop_latched"])
        self.assertGreater(snapshot["last_event_seq"], before)
        self.assertNotIn("STOP", str(snapshot["events"][-1].get("payload", {})))

    def test_raw_secret_message_is_rejected_without_persistence(self):
        self.agent.ensure_session("session-1")
        before = self.agent.snapshot("session-1")["last_event_seq"]
        with self.assertRaises(PrivacyError):
            self.agent.record_message("session-1", AgentProvenance.OWNER, "PASSWORD=hunter2")
        self.assertEqual(before, self.agent.snapshot("session-1")["last_event_seq"])

    def test_runtime_and_free_form_action_surfaces_are_rejected(self):
        with self.assertRaises(PrivacyError):
            self.submit(objective="PASSWORD=hunter2")
        self.assertIsNone(self.store.load_agent_session("session-1"))
        with self.assertRaises(ValidationError) as raised:
            self.submit(runtime_access="read_only")
        self.assertEqual("RUNTIME_ACCESS_UNAVAILABLE", raised.exception.code)
        self.assertIsNone(self.store.load_agent_task("idem-1"))
        self.submit()
        with self.assertRaises(ValidationError) as raised:
            self.agent.propose_named_action(
                "session-1", "action-raw", "CLICK", provenance=AgentProvenance.SUPERVISOR,
            )
        self.assertEqual("INVALID_NAMED_ACTION", raised.exception.code)

    def test_task_canonical_idempotency_and_concurrent_duplicate_race(self):
        barrier = threading.Barrier(3)
        replies = []

        def worker():
            barrier.wait(timeout=2)
            replies.append(self.submit())

        threads = [threading.Thread(target=worker) for _ in range(2)]
        for thread in threads:
            thread.start()
        barrier.wait(timeout=2)
        for thread in threads:
            thread.join(timeout=2)
        self.assertEqual([False, True], sorted(reply["accepted_new"] for reply in replies))
        events = self.agent.snapshot("session-1")["events"]
        self.assertEqual(1, sum(event.get("kind") == "TASK_ACCEPTED" for event in events))

    def test_concurrent_duplicate_action_executes_once(self):
        self.submit()
        replies = []
        barrier = threading.Barrier(3)

        def worker():
            barrier.wait(timeout=2)
            replies.append(self.propose("same-action"))

        threads = [threading.Thread(target=worker) for _ in range(2)]
        for thread in threads:
            thread.start()
        barrier.wait(timeout=2)
        for thread in threads:
            thread.join(timeout=2)
        self.assertEqual(2, len(replies))
        self.assertEqual(1, len(self.executor.execute_calls))
        self.assertEqual(replies[0], replies[1])
        self.assertEqual(1, self.agent.snapshot("session-1")["physical_action_count"])

    def test_disallowed_action_budget_deadline_and_attempt_exhaustion(self):
        self.submit(allowed_actions=(NamedAgentAction.SCREENSHOT,))
        self.assertEqual("REFUSED_ACTION_NOT_ALLOWED", self.propose().status)

        other = task(session_id="session-2", run_id="run-2", task_id="task-2", idempotency_key="idem-2", physical_action_budget=0)
        self.agent.submit_task(other)
        self.assertEqual("REFUSED_BUDGET_EXHAUSTED", self.propose(session_id="session-2", action_id="budget-action").status)

        expired = task(session_id="session-3", run_id="run-3", task_id="task-3", idempotency_key="idem-3", deadline_epoch_ms=0)
        self.agent.submit_task(expired)
        self.assertEqual("REFUSED_DEADLINE_EXPIRED", self.propose(session_id="session-3", action_id="deadline-action").status)

        limited = task(session_id="session-4", run_id="run-4", task_id="task-4", idempotency_key="idem-4", physical_action_budget=3, max_attempts=1)
        self.agent.submit_task(limited)
        self.propose(session_id="session-4", action_id="attempt-one")
        self.assertEqual("REFUSED_ATTEMPTS_EXHAUSTED", self.propose(session_id="session-4", action_id="attempt-two").status)

    def test_screenshot_while_paused_and_stopped_is_read_only_budget_free(self):
        self.submit()
        self.agent.owner_control("session-1", "PAUSE")
        paused = self.agent.owner_control("session-1", "SCREENSHOT")
        self.assertEqual("CAPTURED", paused["capture"]["status"])
        self.agent.owner_control("session-1", "STOP")
        stopped = self.agent.owner_control("session-1", "SCREENSHOT")
        self.assertEqual("CAPTURED", stopped["capture"]["status"])
        snapshot = self.agent.snapshot("session-1")
        self.assertEqual(0, snapshot["physical_action_count"])
        self.assertEqual(1, snapshot["physical_action_budget"])
        self.assertEqual(2, len(self.executor.screenshot_calls))

    def test_pre_effect_executor_exception_is_known_not_performed_and_retry_is_bounded(self):
        self.executor.receipts = [RuntimeError("pre-effect"), AgentActionReceipt("action-2", "PERFORMED", True, True, 1, ())]
        self.submit()
        first = self.propose("action-1")
        self.assertEqual("NOT_PERFORMED", first.status)
        self.assertFalse(first.performed)
        self.assertTrue(first.outcome_known)
        self.assertEqual(0, self.agent.snapshot("session-1")["physical_action_count"])
        self.assertEqual(first, self.propose("action-1"))
        second = self.propose("action-2")
        self.assertTrue(second.performed)
        self.assertEqual(2, len(self.executor.execute_calls))

    def test_performed_unknown_latches_identity_and_forces_inconclusive(self):
        self.executor.receipts = [AgentActionReceipt("action-1", "WORKER_LOST", True, False, 1, ("effect-unknown",))]
        self.submit()
        receipt = self.propose("action-1")
        self.assertEqual("PERFORMED_UNKNOWN", receipt.status)
        self.assertEqual(receipt, self.propose("action-1"))
        self.assertEqual(1, len(self.executor.execute_calls))
        snapshot = self.agent.snapshot("session-1")
        self.assertEqual("INCONCLUSIVE", snapshot["run_status"])
        self.assertEqual(1, snapshot["physical_action_count"])
        result = self.agent.complete_run(
            "session-1", status=ResultStatus.PASS, final_state="UNKNOWN",
            evidence_manifest_sha256="d" * 64, unresolved_conflicts=(),
        )
        self.assertEqual(ResultStatus.INCONCLUSIVE, result.status)
        self.assertIn("PERFORMED_UNKNOWN", result.unresolved_conflicts)

    def test_invalid_executor_receipt_fails_closed_as_performed_unknown(self):
        self.executor.receipts = [AgentActionReceipt("wrong-id", "PERFORMED", True, True, 2, ())]
        self.submit()
        receipt = self.propose("action-1")
        self.assertEqual("PERFORMED_UNKNOWN", receipt.status)
        self.assertTrue(receipt.performed)
        self.assertFalse(receipt.outcome_known)

    def test_task_result_restart_identity_and_first_write_idempotency(self):
        self.submit()
        result = self.agent.complete_run(
            "session-1", status="PASS", final_state="LOGIN_SCREEN",
            evidence_manifest_sha256="d" * 64, unresolved_conflicts=(),
        )
        same = self.agent.complete_run("session-1", result=result)
        self.assertEqual(result, same)
        with self.assertRaises(ValidationError):
            self.agent.complete_run("session-1", result=replace(result, status=ResultStatus.FAIL))
        self.restart(clean=True)
        replay = self.submit()
        self.assertEqual("PASS", replay["result"]["status"])
        self.assertEqual("PASS", self.agent.snapshot("session-1")["result"]["status"])

    def test_control_domain_status_is_additive_and_default_has_no_runtime_authority(self):
        with tempfile.TemporaryDirectory() as root:
            service = ControlDomainService(root, backend_epoch="service-test")
            try:
                status = service.status()
                self.assertEqual("FAKE_TEST", status["runtime"]["adapter_kind"])
                self.assertEqual("NONE", status["official_client_access"])
                self.assertEqual("none", status["agent"]["runtime_access"])
                self.assertEqual("NONE", status["agent"]["mutation_authority"])
                self.assertEqual(0, status["agent"]["physical_action_budget"])
                self.assertEqual(0, status["agent"]["physical_action_count"])
                self.assertIsInstance(service.agent.executor, NullBoundedActionExecutor)
            finally:
                service.close()


if __name__ == "__main__":
    unittest.main()
