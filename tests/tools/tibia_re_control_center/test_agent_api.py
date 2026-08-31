from __future__ import annotations

import json
import io
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from tools.tibia_re_control_center.agent_session import CaptureReceipt, NullBoundedActionExecutor
from tools.tibia_re_control_center.control_api import ControlApiServer, MAX_PAGE
from tools.tibia_re_control_center.control_cli import build_parser, main as cli_main

from tests.tools.tibia_re_control_center.test_package_b import decode, http_call


def task_envelope(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema": "otclient.local-agent.task.v1",
        "session_id": "agent-session-1",
        "task_id": "agent-task-1",
        "run_id": "agent-run-1",
        "idempotency_key": "agent-idem-1",
        "trusted_main_sha": "a" * 40,
        "client_identity": {
            "version": "NOT_APPLICABLE",
            "size": "NOT_APPLICABLE",
            "sha256": "b" * 64,
        },
        "objective": "observe the offline fixture",
        "allowed_actions": ["SCREENSHOT"],
        "physical_action_budget": 0,
        "max_attempts": 1,
        "deadline_epoch_ms": 4_000_000_000_000,
        "runtime_access": "none",
        "required_evidence": ["secret-safe screenshot"],
        "secret_capability_ref": None,
    }
    value.update(overrides)
    return value


class CountingCaptureExecutor(NullBoundedActionExecutor):
    def __init__(self) -> None:
        self.screenshot_calls: list[tuple[str, str]] = []

    def screenshot(self, session_id: str, run_id: str) -> CaptureReceipt:
        self.screenshot_calls.append((session_id, run_id))
        return CaptureReceipt("CAPTURED", "capture-safe", "c" * 64, True)


class AgentApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.server = ControlApiServer(self.root).start()

    def tearDown(self) -> None:
        self.server.close()
        self.temp.cleanup()

    def restart(self, *, executor: object | None = None) -> None:
        old = self.server
        old.close()
        self.server = ControlApiServer(self.root).start()
        if executor is not None:
            self.server.domain.agent.executor = executor

    def post(
        self,
        path: str,
        body: object,
        request_id: str,
        **transport: object,
    ) -> tuple[int, dict[str, str], dict[str, object]]:
        status, headers, raw = http_call(
            self.server,
            "POST",
            path,
            body=body,
            request_id=request_id,
            **transport,
        )
        return status, headers, decode(raw)

    def get(self, path: str, **transport: object) -> tuple[int, dict[str, str], dict[str, object]]:
        status, headers, raw = http_call(self.server, "GET", path, **transport)
        return status, headers, decode(raw)

    def submit(self, request_id: str = "agent-submit-1", **overrides: object) -> dict[str, object]:
        status, _, payload = self.post("/v1/agent/tasks", task_envelope(**overrides), request_id)
        self.assertEqual(201, status, payload)
        return payload

    def test_all_six_routes_exist_and_nonce_is_checked_before_routing(self) -> None:
        requests = (
            ("GET", "/v1/agent/session?session_id=agent-session-1", None),
            ("GET", "/v1/agent/events?session_id=agent-session-1&cursor=0&limit=10", None),
            ("GET", "/v1/agent/result?run_id=agent-run-1", None),
            ("POST", "/v1/agent/tasks", task_envelope()),
            ("POST", "/v1/agent/chat", {"session_id": "agent-session-1", "text": "hello"}),
            ("POST", "/v1/agent/control", {"session_id": "agent-session-1", "command": "PAUSE"}),
        )
        for method, path, body in requests:
            with self.subTest(method=method, path=path):
                status, _, raw = http_call(
                    self.server,
                    method,
                    path,
                    body=body,
                    request_id="nonce-boundary" if method == "POST" else None,
                    nonce=None,
                )
                self.assertEqual(401, status)
                self.assertEqual("CONTROL_AUTH_REQUIRED", decode(raw)["code"])

    def test_agent_get_queries_are_exact_required_and_bounded(self) -> None:
        self.submit()
        cases = (
            "/v1/agent/session",
            "/v1/agent/session?session_id=agent-session-1&unknown=1",
            "/v1/agent/session?session_id=agent-session-1&session_id=again",
            "/v1/agent/events?cursor=0&limit=1",
            "/v1/agent/events?session_id=agent-session-1&cursor=0",
            "/v1/agent/events?session_id=agent-session-1&limit=1",
            "/v1/agent/events?session_id=agent-session-1&cursor=0&limit=1&unknown=1",
            "/v1/agent/events?session_id=agent-session-1&cursor=-1&limit=1",
            "/v1/agent/events?session_id=agent-session-1&cursor=0&limit=0",
            f"/v1/agent/events?session_id=agent-session-1&cursor=0&limit={MAX_PAGE + 1}",
            "/v1/agent/result",
            "/v1/agent/result?run_id=agent-run-1&unknown=1",
        )
        for path in cases:
            with self.subTest(path=path):
                status, _, payload = self.get(path)
                self.assertEqual(400, status, payload)
                self.assertEqual("CONTROL_QUERY_INVALID", payload["code"])

    def test_task_route_accepts_exact_envelope_and_request_ledger_replays_once(self) -> None:
        first = self.submit("agent-task-replay")
        second = self.submit("agent-task-replay")
        self.assertEqual(first, second)
        self.assertEqual("ACCEPTED", first["status"])
        self.assertTrue(first["accepted_new"])
        self.assertEqual("SUPERVISOR", first["provenance"])
        self.assertEqual("none", first["session"]["runtime_access"])
        self.assertEqual("NONE", first["session"]["mutation_authority"])
        self.assertEqual(0, first["session"]["physical_action_count"])
        self.assertEqual("COMPLETED", self.server.domain.store.load_request("agent-task-replay").status)
        accepted = [
            event for event in first["session"]["events"]
            if event.get("kind") == "TASK_ACCEPTED"
        ]
        self.assertEqual(1, len(accepted))
        self.assertEqual("SUPERVISOR", accepted[0]["provenance"])

    def test_task_lost_response_reuses_resource_across_restart_without_duplicate_acceptance(self) -> None:
        for point in ("after_accept", "after_domain"):
            with self.subTest(point=point):
                suffix = point.replace("_", "-")
                body = task_envelope(
                    session_id=f"task-lost-{suffix}",
                    task_id=f"task-lost-{suffix}",
                    run_id=f"run-lost-{suffix}",
                    idempotency_key=f"idem-lost-{suffix}",
                )
                request_id = f"request-task-lost-{suffix}"
                self.server.domain.inject_test_crash_once(point)
                status, _, interrupted = self.post("/v1/agent/tasks", body, request_id)
                self.assertEqual(503, status, interrupted)
                accepted = self.server.domain.store.load_request(request_id)
                self.assertEqual("ACCEPTED", accepted.status)
                durable_result = None
                if point == "after_domain":
                    resource = self.server.domain.store.get_resource(accepted.resource_id)
                    self.assertIsNotNone(resource)
                    durable_result = resource["result"]
                    self.assertIsNotNone(durable_result)
                self.restart()
                replay_status, _, replay = self.post("/v1/agent/tasks", body, request_id)
                self.assertEqual(201, replay_status, replay)
                if durable_result is not None:
                    self.assertEqual(durable_result, replay)
                self.assertEqual(accepted.resource_id, replay["resource_id"])
                session = self.server.domain.agent.snapshot(str(body["session_id"]))
                self.assertEqual(1, sum(
                    event.get("kind") == "TASK_ACCEPTED"
                    for event in session["events"]
                ))

    def test_same_request_id_with_different_envelope_conflicts_without_second_task(self) -> None:
        self.submit("agent-task-conflict")
        status, _, payload = self.post(
            "/v1/agent/tasks",
            task_envelope(objective="different offline objective"),
            "agent-task-conflict",
        )
        self.assertEqual(409, status)
        self.assertEqual("CONTROL_IDEMPOTENCY_CONFLICT", payload["code"])
        session = self.server.domain.agent.snapshot("agent-session-1")
        self.assertEqual(1, len([event for event in session["events"] if event.get("kind") == "TASK_ACCEPTED"]))

    def test_different_request_id_cannot_rebind_task_idempotency_key(self) -> None:
        self.submit("agent-task-first-request")
        status, _, payload = self.post(
            "/v1/agent/tasks",
            task_envelope(objective="conflicting task-level request"),
            "agent-task-second-request",
        )
        self.assertEqual(409, status, payload)
        self.assertEqual("IDEMPOTENCY_CONFLICT", payload["code"])
        session = self.server.domain.agent.snapshot("agent-session-1")
        self.assertEqual(1, len([event for event in session["events"] if event.get("kind") == "TASK_ACCEPTED"]))

    def test_task_body_is_exact_and_grants_no_runtime_or_physical_authority(self) -> None:
        for body in (
            {"task": task_envelope()},
            task_envelope(extra="unknown"),
            task_envelope(runtime_access="read_only"),
        ):
            with self.subTest(body=body):
                status, _, payload = self.post("/v1/agent/tasks", body, f"bad-task-{len(json.dumps(body))}")
                self.assertEqual(400, status, payload)
        self.assertEqual([], self.server.domain.adapter.physical_effects)

    def test_pause_resume_and_stop_delegate_to_authoritative_owner_control(self) -> None:
        self.submit()
        before = self.server.domain.coordinator.control_state
        status, _, paused = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "PAUSE"},
            "agent-pause",
        )
        self.assertEqual(200, status, paused)
        self.assertEqual("PAUSED", paused["status"])
        self.assertTrue(paused["session"]["pause_latched"])
        after_pause = self.server.domain.coordinator.control_state
        self.assertEqual(before.stop_latched, after_pause.stop_latched)
        self.assertEqual(before.recovery_required, after_pause.recovery_required)

        status, _, resumed = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "RESUME"},
            "agent-resume",
        )
        self.assertEqual(200, status, resumed)
        self.assertEqual("PAUSED_AUTHORITY", resumed["status"])
        self.assertFalse(resumed["session"]["pause_latched"])

        status, _, stopped = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "STOP"},
            "agent-stop",
        )
        self.assertEqual(200, status, stopped)
        self.assertEqual("STOPPED", stopped["status"])
        self.assertTrue(stopped["session"]["stop_latched"])
        self.assertTrue(self.server.domain.coordinator.control_state.stop_latched)
        self.assertEqual("OWNER", [event for event in stopped["session"]["events"] if event.get("kind") == "OWNER_STOP"][-1]["provenance"])

        generation = self.server.domain.coordinator.control_generation
        status, _, resumed_from_stop = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "RESUME"},
            "agent-resume-stopped",
        )
        self.assertEqual(200, status, resumed_from_stop)
        self.assertEqual("IDLE", resumed_from_stop["status"])
        self.assertFalse(resumed_from_stop["session"]["stop_latched"])
        self.assertFalse(resumed_from_stop["session"]["pause_latched"])
        self.assertFalse(self.server.domain.coordinator.control_state.stop_latched)
        self.assertEqual(generation + 1, self.server.domain.coordinator.control_generation)
        self.assertEqual("NONE", resumed_from_stop["session"]["mutation_authority"])

    def test_chat_lost_response_reuses_resource_across_restart_without_duplicate_owner_event(self) -> None:
        for point in ("after_accept", "after_domain"):
            with self.subTest(point=point):
                suffix = point.replace("_", "-")
                session_id = f"chat-lost-{suffix}"
                self.submit(
                    f"submit-chat-lost-{suffix}",
                    session_id=session_id,
                    task_id=f"task-chat-lost-{suffix}",
                    run_id=f"run-chat-lost-{suffix}",
                    idempotency_key=f"idem-chat-lost-{suffix}",
                )
                request_id = f"request-chat-lost-{suffix}"
                body = {"session_id": session_id, "text": "bounded owner replay note"}
                self.server.domain.inject_test_crash_once(point)
                status, _, interrupted = self.post("/v1/agent/chat", body, request_id)
                self.assertEqual(503, status, interrupted)
                accepted = self.server.domain.store.load_request(request_id)
                durable_result = None
                if point == "after_domain":
                    resource = self.server.domain.store.get_resource(accepted.resource_id)
                    self.assertIsNotNone(resource)
                    durable_result = resource["result"]
                    self.assertIsNotNone(durable_result)
                self.restart()
                replay_status, _, replay = self.post("/v1/agent/chat", body, request_id)
                self.assertEqual(200, replay_status, replay)
                if durable_result is not None:
                    self.assertEqual(durable_result, replay)
                self.assertEqual(accepted.resource_id, replay["resource_id"])
                session = self.server.domain.agent.snapshot(session_id)
                matching = [
                    event for event in session["events"]
                    if event.get("kind") == "MESSAGE_RECORDED"
                    and event.get("payload", {}).get("message_sha256")
                ]
                self.assertEqual(1, len(matching))

    def test_control_lost_response_reuses_resource_without_duplicate_capture_stop_or_reset(self) -> None:
        capture_executor = CountingCaptureExecutor()
        self.server.domain.agent.executor = capture_executor
        self.submit()
        for point in ("after_accept", "after_domain"):
            with self.subTest(command="SCREENSHOT", point=point):
                request_id = f"screenshot-lost-{point}"
                self.server.domain.inject_test_crash_once(point)
                status, _, interrupted = self.post(
                    "/v1/agent/control",
                    {"session_id": "agent-session-1", "command": "SCREENSHOT"},
                    request_id,
                )
                self.assertEqual(503, status, interrupted)
                accepted = self.server.domain.store.load_request(request_id)
                durable_result = None
                if point == "after_domain":
                    resource = self.server.domain.store.get_resource(accepted.resource_id)
                    self.assertIsNotNone(resource)
                    durable_result = resource["result"]
                    self.assertIsNotNone(durable_result)
                calls_before_replay = len(capture_executor.screenshot_calls)
                self.restart(executor=capture_executor)
                replay_status, _, replay = self.post(
                    "/v1/agent/control",
                    {"session_id": "agent-session-1", "command": "SCREENSHOT"},
                    request_id,
                )
                self.assertEqual(200, replay_status, replay)
                if durable_result is not None:
                    self.assertEqual(durable_result, replay)
                    self.assertEqual(calls_before_replay, len(capture_executor.screenshot_calls))
                self.assertEqual(accepted.resource_id, replay["resource_id"])
        session = self.server.domain.agent.snapshot("agent-session-1")
        self.assertEqual(2, sum(event.get("kind") == "SCREENSHOT_RESULT" for event in session["events"]))

        self.server.domain.inject_test_crash_once("after_domain")
        stop_status, _, stop_interrupted = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "STOP"},
            "stop-lost-response",
        )
        self.assertEqual(503, stop_status, stop_interrupted)
        stopped_generation = self.server.domain.coordinator.control_generation
        stop_record = self.server.domain.store.load_request("stop-lost-response")
        stop_resource = self.server.domain.store.get_resource(stop_record.resource_id)
        self.assertIsNotNone(stop_resource["result"])
        self.restart(executor=capture_executor)
        replay_status, _, replay_stop = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "STOP"},
            "stop-lost-response",
        )
        self.assertEqual(200, replay_status, replay_stop)
        self.assertEqual(stop_resource["result"], replay_stop)
        stop_transition = self.server.domain.store.load_control_transition(stop_record.resource_id)
        self.assertEqual(stopped_generation, stop_transition.control_generation)
        self.assertEqual("AGENT_OWNER_STOP", stop_transition.reason_code)
        self.assertEqual(1, sum(
            '"reason_code":"AGENT_OWNER_STOP"' in row[0]
            for row in self.server.domain.store._fetchall("SELECT body FROM control_history")
        ))
        self.assertEqual(1, sum(
            event.get("kind") == "OWNER_STOP"
            for event in self.server.domain.agent.snapshot("agent-session-1")["events"]
        ))

        self.server.domain.inject_test_crash_once("after_domain")
        resume_status, _, resume_interrupted = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "RESUME"},
            "resume-lost-response",
        )
        self.assertEqual(503, resume_status, resume_interrupted)
        resumed_generation = self.server.domain.coordinator.control_generation
        resume_record = self.server.domain.store.load_request("resume-lost-response")
        resume_resource = self.server.domain.store.get_resource(resume_record.resource_id)
        self.assertIsNotNone(resume_resource["result"])
        self.restart(executor=capture_executor)
        replay_status, _, replay_resume = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "RESUME"},
            "resume-lost-response",
        )
        self.assertEqual(200, replay_status, replay_resume)
        self.assertEqual(resume_resource["result"], replay_resume)
        resume_transition = self.server.domain.store.load_control_transition(resume_record.resource_id)
        self.assertEqual(resumed_generation, resume_transition.control_generation)
        self.assertEqual("AGENT_OWNER_RESUME", resume_transition.reason_code)
        self.assertEqual(1, sum(
            '"reason_code":"AGENT_OWNER_RESUME"' in row[0]
            for row in self.server.domain.store._fetchall("SELECT body FROM control_history")
        ))
        self.assertEqual(1, sum(
            event.get("kind") == "OWNER_RESUME"
            for event in self.server.domain.agent.snapshot("agent-session-1")["events"]
        ))

    def test_concurrent_agent_post_replays_share_one_domain_result(self) -> None:
        capture_executor = CountingCaptureExecutor()
        self.server.domain.agent.executor = capture_executor

        cases = (
            (
                "/v1/agent/tasks",
                task_envelope(
                    session_id="concurrent-task-session",
                    task_id="concurrent-task",
                    run_id="concurrent-task-run",
                    idempotency_key="concurrent-task-idem",
                ),
                "concurrent-agent-task",
                "concurrent-task-session",
                "TASK_ACCEPTED",
            ),
            (
                "/v1/agent/chat",
                {"session_id": "agent-session-1", "text": "one concurrent owner message"},
                "concurrent-agent-chat",
                "agent-session-1",
                "MESSAGE_RECORDED",
            ),
            (
                "/v1/agent/control",
                {"session_id": "agent-session-1", "command": "SCREENSHOT"},
                "concurrent-agent-control",
                "agent-session-1",
                "SCREENSHOT_RESULT",
            ),
        )
        self.submit()
        for path, body, request_id, session_id, event_kind in cases:
            with self.subTest(path=path):
                before = sum(
                    event.get("kind") == event_kind
                    for event in self.server.domain.agent.snapshot(session_id)["events"]
                ) if self.server.domain.store.load_agent_session(session_id) is not None else 0
                barrier = threading.Barrier(8)

                def invoke() -> tuple[int, dict[str, object]]:
                    barrier.wait(timeout=5)
                    status, _, payload = self.post(path, body, request_id)
                    return status, payload

                with ThreadPoolExecutor(max_workers=8) as pool:
                    results = [future.result(timeout=10) for future in [pool.submit(invoke) for _ in range(8)]]
                self.assertTrue(all(result == results[0] for result in results))
                self.assertIn(results[0][0], {200, 201})
                events = self.server.domain.agent.snapshot(session_id)["events"]
                self.assertEqual(before + 1, sum(event.get("kind") == event_kind for event in events))
        self.assertEqual(1, len(capture_executor.screenshot_calls))

    def test_screenshot_is_read_only_and_zero_budget(self) -> None:
        self.submit()
        before_effects = list(self.server.domain.adapter.physical_effects)
        status, _, payload = self.post(
            "/v1/agent/control",
            {"session_id": "agent-session-1", "command": "SCREENSHOT"},
            "agent-screenshot",
        )
        self.assertEqual(200, status, payload)
        self.assertEqual("UNAVAILABLE", payload["status"])
        self.assertEqual(0, payload["session"]["physical_action_count"])
        self.assertEqual(0, payload["session"]["physical_action_budget"])
        self.assertEqual(before_effects, self.server.domain.adapter.physical_effects)
        event = [event for event in payload["session"]["events"] if event.get("kind") == "SCREENSHOT_RESULT"][-1]
        self.assertFalse(event["payload"]["physical_effect"])

    def test_owner_chat_records_hash_only_and_rejects_secret_before_persistence(self) -> None:
        self.submit()
        status, _, recorded = self.post(
            "/v1/agent/chat",
            {"session_id": "agent-session-1", "text": "Please observe the login fixture"},
            "agent-chat-safe",
        )
        self.assertEqual(200, status, recorded)
        event = [event for event in recorded["session"]["events"] if event.get("kind") == "MESSAGE_RECORDED"][-1]
        self.assertEqual("OWNER", event["provenance"])
        self.assertNotIn("text", event["payload"])
        self.assertEqual(64, len(event["payload"]["message_sha256"]))
        before = recorded["session"]["last_event_seq"]
        replay_status, _, replayed = self.post(
            "/v1/agent/chat",
            {"session_id": "agent-session-1", "text": "Please observe the login fixture"},
            "agent-chat-safe",
        )
        self.assertEqual(200, replay_status)
        self.assertEqual(recorded, replayed)
        self.assertEqual(before, replayed["session"]["last_event_seq"])

        status, _, rejected = self.post(
            "/v1/agent/chat",
            {"session_id": "agent-session-1", "text": "PASSWORD=hunter2"},
            "agent-chat-secret",
        )
        self.assertEqual(400, status, rejected)
        self.assertEqual("CONTROL_PRIVACY_REJECTED", rejected["code"])
        self.assertIsNone(self.server.domain.store.load_request("agent-chat-secret"))
        after = self.server.domain.agent.snapshot("agent-session-1")
        self.assertEqual(before, after["last_event_seq"])
        self.assertNotIn("hunter2", json.dumps(after))

    def test_post_body_shapes_commands_and_transport_boundaries_are_preserved(self) -> None:
        self.submit()
        cases = (
            ("/v1/agent/chat", {"session_id": "agent-session-1"}),
            ("/v1/agent/chat", {"session_id": "agent-session-1", "text": "ok", "unknown": 1}),
            ("/v1/agent/control", {"session_id": "agent-session-1"}),
            ("/v1/agent/control", {"session_id": "agent-session-1", "command": "CLICK"}),
        )
        for index, (path, body) in enumerate(cases):
            with self.subTest(path=path, body=body):
                status, _, payload = self.post(path, body, f"agent-body-{index}")
                self.assertEqual(400, status, payload)
        status, headers, payload = self.post(
            "/v1/agent/chat",
            {"session_id": "agent-session-1", "text": "same origin"},
            "agent-origin-bad",
            origin="https://evil.invalid",
        )
        self.assertEqual(403, status, payload)
        self.assertNotIn("access-control-allow-origin", headers)
        self.assertNotIn("set-cookie", headers)

    def test_session_events_and_result_views_are_safe_and_exact(self) -> None:
        self.submit()
        self.post(
            "/v1/agent/chat",
            {"session_id": "agent-session-1", "text": "bounded owner note"},
            "agent-chat-view",
        )
        status, _, session = self.get("/v1/agent/session?session_id=agent-session-1")
        self.assertEqual(200, status, session)
        self.assertEqual("agent-session-1", session["session_id"])
        status, _, events = self.get(
            "/v1/agent/events?session_id=agent-session-1&cursor=0&limit=10"
        )
        self.assertEqual(200, status, events)
        self.assertTrue(events["items"])
        self.assertTrue(all(event["session_id"] == "agent-session-1" for event in events["items"]))
        self.assertEqual("BOUNDED_POLLING", events["delivery"])

        self.server.domain.agent.complete_run(
            "agent-session-1",
            status="PASS",
            final_state="LOGIN_SCREEN",
            evidence_manifest_sha256="c" * 64,
        )
        status, _, result = self.get("/v1/agent/result?run_id=agent-run-1")
        self.assertEqual(200, status, result)
        self.assertEqual("agent-run-1", result["run_id"])
        self.assertEqual("PASS", result["status"])
        self.server.close()
        self.server = ControlApiServer(self.root).start()
        restart_status, _, restart_result = self.get("/v1/agent/result?run_id=agent-run-1")
        self.assertEqual(200, restart_status, restart_result)
        self.assertEqual(result, restart_result)
        serialized = json.dumps({"session": session, "events": events, "result": result})
        for forbidden in (self.server.nonce, "secret_capability_ref", "PASSWORD=", "hunter2"):
            self.assertNotIn(forbidden, serialized)

    def test_task_response_omits_opaque_secret_reference_and_rejects_secret_text_pre_ledger(self) -> None:
        accepted = self.submit(
            "agent-task-secret-ref",
            session_id="agent-session-ref",
            task_id="agent-task-ref",
            run_id="agent-run-ref",
            idempotency_key="agent-idem-ref",
            secret_capability_ref="opaque-capability-ref",
        )
        self.assertNotIn("secret_capability_ref", json.dumps(accepted))
        status, _, payload = self.post(
            "/v1/agent/tasks",
            task_envelope(
                session_id="agent-session-secret",
                task_id="agent-task-secret",
                run_id="agent-run-secret",
                idempotency_key="agent-idem-secret",
                objective="PASSWORD=hunter2",
            ),
            "agent-task-secret-text",
        )
        self.assertEqual(400, status, payload)
        self.assertEqual("CONTROL_PRIVACY_REJECTED", payload["code"])
        self.assertIsNone(self.server.domain.store.load_request("agent-task-secret-text"))

    def test_cli_exact_agent_commands_have_no_credential_arguments(self) -> None:
        parser = build_parser()
        accepted = (
            ["agent-status", "--session", "session-1"],
            ["agent-task", "--file", "task.json", "--request-id", "request-1"],
            ["agent-chat", "--session", "session-1", "--text", "hello", "--request-id", "request-2"],
            ["agent-control", "--session", "session-1", "--command", "PAUSE", "--request-id", "request-3"],
            ["agent-events", "--session", "session-1", "--cursor", "0", "--limit", "10"],
            ["agent-result", "--run", "run-1"],
        )
        for argv in accepted:
            with self.subTest(argv=argv):
                self.assertIsNotNone(parser.parse_args(argv))
        for option in ("--password", "--credential", "--token", "--api-key", "--secret"):
            with self.subTest(option=option), self.assertRaises(SystemExit):
                with redirect_stderr(io.StringIO()):
                    parser.parse_args(["agent-chat", "--session", "session-1", "--text", "hello", "--request-id", "r", option, "value"])

    def test_all_six_agent_cli_commands_execute_against_live_server(self) -> None:
        task_path = self.root / "agent-task.json"
        task_path.write_text(json.dumps(task_envelope()), encoding="utf-8")
        commands = (
            ["agent-task", "--file", str(task_path), "--request-id", "cli-agent-task"],
            ["agent-status", "--session", "agent-session-1"],
            ["agent-chat", "--session", "agent-session-1", "--text", "owner cli note", "--request-id", "cli-agent-chat"],
            ["agent-control", "--session", "agent-session-1", "--command", "PAUSE", "--request-id", "cli-agent-control"],
            ["agent-events", "--session", "agent-session-1", "--cursor", "0", "--limit", "20"],
            ["agent-result", "--run", "agent-run-1"],
        )
        outputs: list[dict[str, object]] = []
        for command in commands:
            with self.subTest(command=command[0]):
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    exit_code = cli_main(["--data-dir", str(self.root), *command])
                self.assertEqual(0, exit_code, stdout.getvalue())
                outputs.append(json.loads(stdout.getvalue()))
        self.assertEqual("ACCEPTED", outputs[0]["status"])
        self.assertEqual("agent-session-1", outputs[1]["session_id"])
        self.assertEqual("RECORDED", outputs[2]["status"])
        self.assertEqual("PAUSED", outputs[3]["status"])
        self.assertTrue(outputs[4]["items"])
        self.assertEqual("PENDING", outputs[5]["status"])

    def test_ui_adds_safe_agent_dashboard_and_preserves_top_level_stop_all(self) -> None:
        status, _, raw = http_call(self.server, "GET", "/", nonce=None)
        page = raw.decode("utf-8")
        self.assertEqual(200, status)
        for required in (
            ">Agent<", "Session heartbeat", "Task / run / main SHA", "Secret-safe capture",
            "Visual-only label / OCR", "Runtime evidence class", "Reconciliation state",
            "Action status / budget", "Provenance timeline", "Owner chat",
            "PAUSE", "STOP", "RESUME", "SCREENSHOT", "STOP ALL",
        ):
            self.assertIn(required, page)
        self.assertNotIn('type="password"', page.lower())
        self.assertNotIn('name="credential"', page.lower())
        self.assertNotIn("raw ocr", page.lower())


if __name__ == "__main__":
    unittest.main()
