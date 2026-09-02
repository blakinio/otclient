from __future__ import annotations

import ast
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.tibia_re_control_center.control_cli import ControlClientError

TASK = {
    "schema": "otclient.local-agent.task.v1",
    "session_id": "session-1",
    "task_id": "task-1",
    "run_id": "run-1",
    "idempotency_key": "idem-1",
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

PUNCTUATED_SECRET_ASSIGNMENTS = (
    "control.nonce=SENTINEL_PUNCTUATED_SECRET",
    "api.key=SENTINEL_PUNCTUATED_SECRET",
    "private.key=SENTINEL_PUNCTUATED_SECRET",
    "control:nonce=SENTINEL_PUNCTUATED_SECRET",
    "api:key=SENTINEL_PUNCTUATED_SECRET",
    "private:key=SENTINEL_PUNCTUATED_SECRET",
    "control/nonce=SENTINEL_PUNCTUATED_SECRET",
    "api/key=SENTINEL_PUNCTUATED_SECRET",
    "private/key=SENTINEL_PUNCTUATED_SECRET",
    "control.::/nonce=SENTINEL_PUNCTUATED_SECRET",
    "api/.:key=SENTINEL_PUNCTUATED_SECRET",
    "private:_./key=SENTINEL_PUNCTUATED_SECRET",
)

UNICODE_COMPAT_SECRET_ASSIGNMENTS = (
    "ＡＰＩ．ＫＥＹ＝S3cr3t42",
    "api.key＝S3cr3t42",
    "control.nonce：S3cr3t42",
    "ＣＯＮＴＲＯＬ／ＮＯＮＣＥ＝S3cr3t42",
    "ＰＲＩＶＡＴＥ：ＫＥＹ＝S3cr3t42",
    "𝐀𝐏𝐈.𝐊𝐄𝐘=S3cr3t42",
    "ⓐⓟⓘ﹒ⓚⓔⓨ﹦S3cr3t42",
)


class FakeControlApiClient:
    def __init__(self) -> None:
        self.calls: list[tuple[object, ...]] = []
        self.response: object = {"status": "OK"}
        self.error: BaseException | None = None

    def get(self, path: str) -> object:
        self.calls.append(("GET", path))
        if self.error is not None:
            raise self.error
        return self.response

    def post(self, path: str, body: dict[str, object], *, request_id: str) -> object:
        self.calls.append(("POST", path, body, request_id))
        if self.error is not None:
            raise self.error
        return self.response


def rpc(method: str, params: object | None = None, request_id: object = 1) -> dict[str, object]:
    request: dict[str, object] = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        request["params"] = params
    return request


def call(name: str, arguments: dict[str, object], request_id: object = 1) -> dict[str, object]:
    return rpc("tools/call", {"name": name, "arguments": arguments}, request_id)


class AgentMcpTests(unittest.TestCase):
    def setUp(self) -> None:
        from tools.tibia_re_control_center import agent_mcp

        self.agent_mcp = agent_mcp
        self.client = FakeControlApiClient()
        self.server = agent_mcp.AgentMcpServer(self.client)

    def assert_tool_payload(self, response: dict[str, object], expected: dict[str, object]) -> None:
        self.assertEqual("2.0", response["jsonrpc"])
        result = response["result"]
        self.assertIsInstance(result, dict)
        self.assertFalse(result["isError"])
        self.assertEqual(1, len(result["content"]))
        self.assertEqual("text", result["content"][0]["type"])
        self.assertEqual(expected, json.loads(result["content"][0]["text"]))

    def test_initialize_negotiates_exact_server_and_protocol(self) -> None:
        response = self.server.handle(rpc("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1"},
        }))

        self.assertEqual({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "tibia-re-agent", "version": "1.0"},
            },
        }, response)
        self.assertEqual([], self.client.calls)

    def test_tools_list_has_exact_five_names_schemas_and_authority_descriptions(self) -> None:
        response = self.server.handle(rpc("tools/list", {}))

        tools = response["result"]["tools"]
        self.assertEqual([
            "agent_session_status",
            "agent_submit_task",
            "agent_control",
            "agent_events",
            "agent_result",
        ], [tool["name"] for tool in tools])
        by_name = {tool["name"]: tool for tool in tools}
        self.assertEqual({
            "type": "object",
            "properties": {"session_id": {"type": "string", "minLength": 1, "maxLength": 128}},
            "required": ["session_id"],
            "additionalProperties": False,
        }, by_name["agent_session_status"]["inputSchema"])
        self.assertEqual({
            "type": "object",
            "properties": {
                "request_id": {"type": "string", "minLength": 1, "maxLength": 128},
                "session_id": {"type": "string", "minLength": 1, "maxLength": 128},
                "command": {"type": "string", "enum": ["PAUSE", "STOP", "RESUME", "SCREENSHOT"]},
            },
            "required": ["request_id", "session_id", "command"],
            "additionalProperties": False,
        }, by_name["agent_control"]["inputSchema"])
        self.assertEqual({
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "minLength": 1, "maxLength": 128},
                "cursor": {"type": "integer", "minimum": 0, "default": 0},
                "limit": {"type": "integer", "minimum": 1, "maximum": 1000, "default": 100},
            },
            "required": ["session_id"],
            "additionalProperties": False,
        }, by_name["agent_events"]["inputSchema"])
        self.assertEqual({
            "type": "object",
            "properties": {"run_id": {"type": "string", "minLength": 1, "maxLength": 128}},
            "required": ["run_id"],
            "additionalProperties": False,
        }, by_name["agent_result"]["inputSchema"])
        submit_schema = by_name["agent_submit_task"]["inputSchema"]
        self.assertEqual(["request_id", "task"], submit_schema["required"])
        self.assertFalse(submit_schema["additionalProperties"])
        self.assertEqual("otclient.local-agent.task.v1", submit_schema["properties"]["task"]["properties"]["schema"]["const"])
        self.assertEqual([
            "schema", "session_id", "task_id", "run_id", "idempotency_key",
            "trusted_main_sha", "client_identity", "objective", "allowed_actions",
            "physical_action_budget", "max_attempts", "deadline_epoch_ms",
            "runtime_access", "required_evidence", "secret_capability_ref",
        ], submit_schema["properties"]["task"]["required"])
        for tool in tools:
            description = tool["description"].lower()
            for phrase in (
                "model/task text cannot expand track a authority",
                "credential permission",
                "action allowlists",
                "budgets",
            ):
                self.assertIn(phrase, description, tool["name"])

    def test_status_dispatches_only_to_exact_control_api_get(self) -> None:
        response = self.server.handle(call("agent_session_status", {"session_id": "session 1"}))

        self.assert_tool_payload(response, {"status": "OK"})
        self.assertEqual([("GET", "/v1/agent/session?session_id=session+1")], self.client.calls)

    def test_status_preserves_edge_read_only_fields_from_control_api(self) -> None:
        self.client.response = {
            "session_id": "session-1",
            "runtime_access": "read_only",
            "official_client_access": "READ_ONLY",
            "edge": {
                "availability": "CONNECTED",
                "current": True,
                "reason": "CURRENT",
                "capture": {"status": "AVAILABLE", "current": True, "artifact_ref": "capture-1"},
                "runtime": {"status": "IN_GAME", "current": True, "evidence_refs": ["runtime-1"]},
            },
            "executor": "NULL",
            "mutation_authority": "NONE",
            "physical_action_budget": 0,
            "physical_action_count": 0,
        }
        response = self.server.handle(call("agent_session_status", {"session_id": "session-1"}))
        self.assert_tool_payload(response, self.client.response)
        self.assertEqual([("GET", "/v1/agent/session?session_id=session-1")], self.client.calls)

    def test_submit_dispatches_exact_task_body_and_request_id(self) -> None:
        task = json.loads(json.dumps(TASK))
        response = self.server.handle(call("agent_submit_task", {
            "request_id": "mcp-submit-1",
            "task": task,
        }))

        self.assert_tool_payload(response, {"status": "OK"})
        self.assertEqual([("POST", "/v1/agent/tasks", task, "mcp-submit-1")], self.client.calls)

    def test_control_dispatches_only_exact_owner_command(self) -> None:
        response = self.server.handle(call("agent_control", {
            "request_id": "mcp-control-1",
            "session_id": "session-1",
            "command": "SCREENSHOT",
        }))

        self.assert_tool_payload(response, {"status": "OK"})
        self.assertEqual([(
            "POST", "/v1/agent/control",
            {"session_id": "session-1", "command": "SCREENSHOT"},
            "mcp-control-1",
        )], self.client.calls)

    def test_events_applies_defaults_and_dispatches_exact_bounded_query(self) -> None:
        default_response = self.server.handle(call("agent_events", {"session_id": "session-1"}, 1))
        explicit_response = self.server.handle(call("agent_events", {
            "session_id": "session-1", "cursor": 7, "limit": 12,
        }, 2))

        self.assert_tool_payload(default_response, {"status": "OK"})
        self.assert_tool_payload(explicit_response, {"status": "OK"})
        self.assertEqual([
            ("GET", "/v1/agent/events?session_id=session-1&cursor=0&limit=100"),
            ("GET", "/v1/agent/events?session_id=session-1&cursor=7&limit=12"),
        ], self.client.calls)

    def test_result_dispatches_only_to_exact_control_api_get(self) -> None:
        response = self.server.handle(call("agent_result", {"run_id": "run/unsafe"}))

        self.assertEqual(-32602, response["error"]["code"])
        self.assertEqual([], self.client.calls)
        response = self.server.handle(call("agent_result", {"run_id": "run-1"}, 2))
        self.assert_tool_payload(response, {"status": "OK"})
        self.assertEqual([("GET", "/v1/agent/result?run_id=run-1")], self.client.calls)

    def test_unknown_tool_and_unknown_method_fail_safely(self) -> None:
        unknown_tool = self.server.handle(call("not_a_tool", {"password": "do-not-echo"}))
        unknown_method = self.server.handle(rpc("resources/read", {"uri": "secret://do-not-echo"}, 2))

        for response, code in ((unknown_tool, -32602), (unknown_method, -32601)):
            encoded = json.dumps(response)
            self.assertEqual(code, response["error"]["code"])
            self.assertLess(len(encoded), 1024)
            self.assertNotIn("do-not-echo", encoded)
        self.assertEqual([], self.client.calls)

    def test_malformed_json_rpc_requests_fail_safely_without_echo(self) -> None:
        cases = (
            [],
            {"jsonrpc": "1.0", "id": 1, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": {"secret": "do-not-echo"}, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 1, "method": 7},
            {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "unknown": "do-not-echo"},
        )
        for request in cases:
            with self.subTest(request=request):
                response = self.server.handle(request)
                encoded = json.dumps(response)
                self.assertIn(response["error"]["code"], {-32600, -32602})
                self.assertLess(len(encoded), 1024)
                self.assertNotIn("do-not-echo", encoded)
        self.assertEqual([], self.client.calls)

    def test_stdio_parse_errors_and_oversized_lines_are_bounded_and_server_continues(self) -> None:
        incoming = io.StringIO(
            "{not-json do-not-echo}\n"
            + ("x" * (self.agent_mcp.MAX_INPUT_BYTES + 1))
            + "\n"
            + json.dumps(rpc("tools/list", {}, 3))
            + "\n"
        )
        outgoing = io.StringIO()

        self.server.serve(incoming, outgoing)

        responses = [json.loads(line) for line in outgoing.getvalue().splitlines()]
        self.assertEqual([-32700, -32700], [item["error"]["code"] for item in responses[:2]])
        self.assertEqual(3, responses[2]["id"])
        self.assertLess(max(len(json.dumps(item)) for item in responses[:2]), 1024)
        self.assertNotIn("do-not-echo", outgoing.getvalue())

    def test_stdio_rejects_duplicate_keys_and_noncanonical_numbers_without_crashing(self) -> None:
        incoming = io.StringIO(
            '{"jsonrpc":"2.0","id":1,"method":"tools/list","method":"tools/call"}\n'
            '{"jsonrpc":"2.0","id":NaN,"method":"tools/list","params":{}}\n'
            + json.dumps(rpc("ping", {}, 3))
            + "\n"
        )
        outgoing = io.StringIO()

        self.server.serve(incoming, outgoing)

        responses = [json.loads(line) for line in outgoing.getvalue().splitlines()]
        self.assertEqual([-32700, -32700], [response["error"]["code"] for response in responses[:2]])
        self.assertEqual({"jsonrpc": "2.0", "id": 3, "result": {}}, responses[2])
        self.assertEqual([], self.client.calls)

    def test_json_rpc_ids_reject_null_secret_aliases_and_non_integer_numbers_without_dispatch(self) -> None:
        sentinel = "SENTINEL_RPC_SECRET"
        cases = (
            None,
            f"secret={sentinel}",
            f"CrEdEnTiAl:{sentinel}",
            f"CONTROL-NONCE={sentinel}",
            f"api_key={sentinel}",
            f"Authorization: Bearer {sentinel}12345678",
            f"PRIVATE-KEY={sentinel}",
            "x" * 129,
            9_007_199_254_740_992,
            1.5,
            float("nan"),
            float("inf"),
        )
        for request_id in cases:
            with self.subTest(request_id=repr(request_id)):
                response = self.server.handle(call(
                    "agent_result", {"run_id": "run-1"}, request_id,
                ))
                encoded = json.dumps(response)
                self.assertEqual(-32600, response["error"]["code"])
                self.assertIsNone(response["id"])
                self.assertLess(len(encoded), 1024)
                self.assertNotIn(sentinel, encoded)
        self.assertEqual([], self.client.calls)

    def test_valid_string_and_json_safe_integer_rpc_ids_remain_admitted(self) -> None:
        for request_id in ("rpc-safe-1", -9_007_199_254_740_991, 0, 9_007_199_254_740_991):
            with self.subTest(request_id=request_id):
                response = self.server.handle(rpc("ping", {}, request_id))
                self.assertEqual({"jsonrpc": "2.0", "id": request_id, "result": {}}, response)
        self.assertEqual([], self.client.calls)

    def test_punctuated_secret_assignments_in_rpc_ids_reject_with_null_id_without_dispatch(self) -> None:
        for request_id in PUNCTUATED_SECRET_ASSIGNMENTS:
            with self.subTest(request_id=request_id):
                response = self.server.handle(call(
                    "agent_result", {"run_id": "run-1"}, request_id,
                ))
                encoded = json.dumps(response)
                self.assertIn("error", response)
                self.assertEqual(-32600, response["error"]["code"])
                self.assertIsNone(response["id"])
                self.assertNotIn("SENTINEL_PUNCTUATED_SECRET", encoded)
        self.assertEqual([], self.client.calls)

    def test_unicode_compat_secret_assignments_in_rpc_ids_reject_with_null_id_without_dispatch(self) -> None:
        for request_id in UNICODE_COMPAT_SECRET_ASSIGNMENTS:
            with self.subTest(request_id=request_id):
                response = self.server.handle(call(
                    "agent_result", {"run_id": "run-1"}, request_id,
                ))
                encoded = json.dumps(response, ensure_ascii=False)
                self.assertIn("error", response)
                self.assertEqual(-32600, response["error"]["code"])
                self.assertIsNone(response["id"])
                self.assertNotIn("S3cr3t42", encoded)
        self.assertEqual([], self.client.calls)

    def test_secret_shaped_task_keys_and_values_are_rejected_before_api_call(self) -> None:
        cases: list[dict[str, object]] = []
        for key in ("password", "api_token", "credential", "authorization", "private_key"):
            task = json.loads(json.dumps(TASK))
            task["client_identity"][key] = "raw-secret"
            cases.append(task)
        for objective in ("password=hunter2", "Bearer abcdefghijklmnop", "api_token: raw-secret"):
            task = json.loads(json.dumps(TASK))
            task["objective"] = objective
            cases.append(task)

        for index, task in enumerate(cases):
            with self.subTest(index=index):
                response = self.server.handle(call("agent_submit_task", {
                    "request_id": f"secret-{index}", "task": task,
                }, index))
                encoded = json.dumps(response)
                self.assertEqual(-32602, response["error"]["code"])
                self.assertNotIn("raw-secret", encoded)
                self.assertNotIn("hunter2", encoded)
                self.assertNotIn("abcdefghijklmnop", encoded)
        self.assertEqual([], self.client.calls)

    def test_all_outer_ids_and_nested_task_text_use_the_control_privacy_vocabulary(self) -> None:
        cases: list[tuple[str, dict[str, object], str]] = [
            (
                "agent_session_status",
                {"session_id": "CrEdEnTiAl=SENTINEL_SESSION"},
                "SENTINEL_SESSION",
            ),
            (
                "agent_control",
                {
                    "request_id": "control_nonce=SENTINEL_REQUEST",
                    "session_id": "session-1",
                    "command": "PAUSE",
                },
                "SENTINEL_REQUEST",
            ),
            (
                "agent_control",
                {
                    "request_id": "request-1",
                    "session_id": "Authorization: Bearer SENTINEL_SESSION_BEARER",
                    "command": "PAUSE",
                },
                "SENTINEL_SESSION_BEARER",
            ),
            (
                "agent_events",
                {"session_id": "API-KEY=SENTINEL_EVENTS"},
                "SENTINEL_EVENTS",
            ),
            (
                "agent_result",
                {"run_id": "private-key=SENTINEL_RUN"},
                "SENTINEL_RUN",
            ),
        ]
        task_text_cases = (
            ("objective", "api_key=SENTINEL_OBJECTIVE"),
            ("session_id", "credential=SENTINEL_TASK_SESSION"),
            ("task_id", "SeCrEt=SENTINEL_TASK_ID"),
            ("run_id", "CONTROL-NONCE=SENTINEL_TASK_RUN"),
            ("idempotency_key", "AUTHORIZATION=SENTINEL_TASK_IDEMPOTENCY"),
        )
        for field, value in task_text_cases:
            task = json.loads(json.dumps(TASK))
            task[field] = value
            cases.append((
                "agent_submit_task",
                {"request_id": "submit-safe", "task": task},
                "SENTINEL" + value.split("SENTINEL", 1)[1],
            ))
        nested_task = json.loads(json.dumps(TASK))
        nested_task["client_identity"]["version"] = "PRIVATE-KEY=SENTINEL_NESTED"
        cases.append((
            "agent_submit_task",
            {"request_id": "submit-nested", "task": nested_task},
            "SENTINEL_NESTED",
        ))

        for index, (name, arguments, sentinel) in enumerate(cases):
            with self.subTest(index=index, name=name):
                response = self.server.handle(call(name, arguments, index + 1))
                encoded = json.dumps(response)
                self.assertEqual(-32602, response["error"]["code"])
                self.assertNotIn(sentinel, encoded)
        self.assertEqual([], self.client.calls)

    def test_punctuated_secret_assignments_in_every_outer_id_reject_before_dispatch(self) -> None:
        for assignment in PUNCTUATED_SECRET_ASSIGNMENTS:
            requests = (
                call("agent_control", {
                    "request_id": assignment,
                    "session_id": "session-1",
                    "command": "PAUSE",
                }),
                call("agent_session_status", {"session_id": assignment}),
                call("agent_result", {"run_id": assignment}),
            )
            for boundary, request in zip(("request_id", "session_id", "run_id"), requests):
                with self.subTest(boundary=boundary, assignment=assignment):
                    response = self.server.handle(request)
                    encoded = json.dumps(response)
                    self.assertIn("error", response)
                    self.assertEqual(-32602, response["error"]["code"])
                    self.assertNotIn("SENTINEL_PUNCTUATED_SECRET", encoded)
        self.assertEqual([], self.client.calls)

    def test_unicode_compat_secret_assignments_in_every_outer_id_reject_before_dispatch(self) -> None:
        for assignment in UNICODE_COMPAT_SECRET_ASSIGNMENTS:
            task = json.loads(json.dumps(TASK))
            requests = (
                call("agent_submit_task", {"request_id": assignment, "task": task}),
                call("agent_control", {
                    "request_id": assignment,
                    "session_id": "session-1",
                    "command": "PAUSE",
                }),
                call("agent_session_status", {"session_id": assignment}),
                call("agent_control", {
                    "request_id": "request-1",
                    "session_id": assignment,
                    "command": "PAUSE",
                }),
                call("agent_events", {"session_id": assignment}),
                call("agent_result", {"run_id": assignment}),
            )
            boundaries = (
                "submit.request_id",
                "control.request_id",
                "status.session_id",
                "control.session_id",
                "events.session_id",
                "result.run_id",
            )
            for boundary, request in zip(boundaries, requests):
                with self.subTest(boundary=boundary, assignment=assignment):
                    response = self.server.handle(request)
                    encoded = json.dumps(response, ensure_ascii=False)
                    self.assertIn("error", response)
                    self.assertEqual(-32602, response["error"]["code"])
                    self.assertNotIn("S3cr3t42", encoded)
        self.assertEqual([], self.client.calls)

    def test_punctuated_secret_assignments_in_scalar_and_nested_task_text_reject_before_dispatch(self) -> None:
        for assignment in PUNCTUATED_SECRET_ASSIGNMENTS:
            scalar_task = json.loads(json.dumps(TASK))
            scalar_task["objective"] = assignment
            nested_task = json.loads(json.dumps(TASK))
            nested_task["client_identity"]["version"] = assignment
            for boundary, task in (("scalar", scalar_task), ("nested", nested_task)):
                with self.subTest(boundary=boundary, assignment=assignment):
                    response = self.server.handle(call("agent_submit_task", {
                        "request_id": "punctuated-task", "task": task,
                    }))
                    encoded = json.dumps(response)
                    self.assertIn("error", response)
                    self.assertEqual(-32602, response["error"]["code"])
                    self.assertNotIn("SENTINEL_PUNCTUATED_SECRET", encoded)
        self.assertEqual([], self.client.calls)

    def test_unicode_compat_secret_assignments_in_scalar_and_nested_task_text_reject_before_dispatch(self) -> None:
        for assignment in UNICODE_COMPAT_SECRET_ASSIGNMENTS:
            scalar_task = json.loads(json.dumps(TASK))
            scalar_task["objective"] = assignment
            nested_task = json.loads(json.dumps(TASK))
            nested_task["client_identity"]["version"] = assignment
            for boundary, task in (("scalar", scalar_task), ("nested", nested_task)):
                with self.subTest(boundary=boundary, assignment=assignment):
                    response = self.server.handle(call("agent_submit_task", {
                        "request_id": "unicode-task", "task": task,
                    }))
                    encoded = json.dumps(response, ensure_ascii=False)
                    self.assertIn("error", response)
                    self.assertEqual(-32602, response["error"]["code"])
                    self.assertNotIn("S3cr3t42", encoded)
        self.assertEqual([], self.client.calls)

    def test_opaque_secret_capability_ref_is_not_resolved_or_rejected(self) -> None:
        task = json.loads(json.dumps(TASK))
        task["secret_capability_ref"] = "opaque-capability-1"

        response = self.server.handle(call("agent_submit_task", {
            "request_id": "opaque-ref", "task": task,
        }))

        self.assert_tool_payload(response, {"status": "OK"})
        self.assertEqual([("POST", "/v1/agent/tasks", task, "opaque-ref")], self.client.calls)

        self.client.calls.clear()
        task["secret_capability_ref"] = "credential=SENTINEL_CAPABILITY_REF"
        rejected = self.server.handle(call("agent_submit_task", {
            "request_id": "opaque-ref-secret", "task": task,
        }))
        self.assertEqual(-32602, rejected["error"]["code"])
        self.assertNotIn("SENTINEL_CAPABILITY_REF", json.dumps(rejected))
        self.assertEqual([], self.client.calls)

    def test_control_cannot_express_click_type_shell_or_process_commands(self) -> None:
        for command in ("CLICK", "TYPE", "SHELL", "PROCESS", "click", "PAUSE "):
            with self.subTest(command=command):
                response = self.server.handle(call("agent_control", {
                    "request_id": "bad-control",
                    "session_id": "session-1",
                    "command": command,
                }))
                self.assertEqual(-32602, response["error"]["code"])
        self.assertEqual([], self.client.calls)

    def test_unknown_arguments_wrong_types_and_out_of_range_pages_fail_before_api(self) -> None:
        cases = (
            call("agent_session_status", {"session_id": "session-1", "extra": True}),
            call("agent_session_status", {"session_id": 7}),
            call("agent_control", {"request_id": "r", "session_id": "s"}),
            call("agent_events", {"session_id": "s", "cursor": -1}),
            call("agent_events", {"session_id": "s", "limit": 0}),
            call("agent_events", {"session_id": "s", "limit": 1001}),
            call("agent_result", {"run_id": ""}),
        )
        for request in cases:
            with self.subTest(request=request):
                response = self.server.handle(request)
                self.assertEqual(-32602, response["error"]["code"])
        self.assertEqual([], self.client.calls)

    def test_control_api_errors_are_bounded_and_never_forward_raw_payload_secrets(self) -> None:
        self.client.error = ControlClientError(503, {
            "code": "CONTROL_CONNECT_FAILED",
            "safe_message": "token=raw-api-secret " + ("x" * 20_000),
            "nonce": "raw-nonce-secret",
        })

        response = self.server.handle(call("agent_result", {"run_id": "run-1"}))

        encoded = json.dumps(response)
        self.assertEqual("2.0", response["jsonrpc"])
        self.assertTrue(response["result"]["isError"])
        payload = json.loads(response["result"]["content"][0]["text"])
        self.assertEqual({
            "code": "CONTROL_CONNECT_FAILED",
            "safe_message": "Control API request failed safely",
            "status": 503,
        }, payload)
        self.assertLess(len(encoded), 1024)
        self.assertNotIn("raw-api-secret", encoded)
        self.assertNotIn("raw-nonce-secret", encoded)

    def test_unexpected_client_errors_are_fixed_bounded_tool_errors(self) -> None:
        self.client.error = RuntimeError("password=do-not-echo")

        response = self.server.handle(call("agent_session_status", {"session_id": "session-1"}))

        encoded = json.dumps(response)
        self.assertTrue(response["result"]["isError"])
        self.assertLess(len(encoded), 1024)
        self.assertNotIn("do-not-echo", encoded)
        self.assertEqual("MCP_INTERNAL_ERROR", json.loads(response["result"]["content"][0]["text"])["code"])

    def test_secret_bearing_success_payloads_become_one_fixed_safe_tool_error(self) -> None:
        sentinel = "SENTINEL_API_SUCCESS_SECRET"
        cases = (
            {"status": "OK", "nested": {"control_nonce": sentinel}},
            {"status": "OK", "items": [{"note": f"Api-Key={sentinel}"}]},
            {"status": "OK", "nested": [{"Authorization": f"Bearer {sentinel}12345678"}]},
            {"status": "OK", "private-key": sentinel},
        )
        expected = {
            "code": "MCP_UNSAFE_API_RESPONSE",
            "safe_message": "Control API response violated the MCP privacy boundary",
        }
        for payload in cases:
            with self.subTest(payload=payload):
                self.client.response = payload
                response = self.server.handle(call("agent_result", {"run_id": "run-1"}))
                encoded = json.dumps(response)
                self.assertTrue(response["result"]["isError"])
                self.assertEqual(expected, json.loads(response["result"]["content"][0]["text"]))
                self.assertLess(len(encoded), 1024)
                self.assertNotIn(sentinel, encoded)

    def test_punctuated_secret_assignments_in_scalar_and_nested_api_success_are_fixed_safe_errors(self) -> None:
        expected = {
            "code": "MCP_UNSAFE_API_RESPONSE",
            "safe_message": "Control API response violated the MCP privacy boundary",
        }
        for assignment in PUNCTUATED_SECRET_ASSIGNMENTS:
            payloads = (
                {"status": "OK", "note": assignment},
                {"status": "OK", "items": [{"note": assignment}]},
            )
            for boundary, payload in zip(("scalar", "nested"), payloads):
                with self.subTest(boundary=boundary, assignment=assignment):
                    self.client.response = payload
                    response = self.server.handle(call("agent_result", {"run_id": "run-1"}))
                    encoded = json.dumps(response)
                    self.assertTrue(response["result"]["isError"])
                    self.assertEqual(expected, json.loads(response["result"]["content"][0]["text"]))
                    self.assertLess(len(encoded), 1024)
                    self.assertNotIn("SENTINEL_PUNCTUATED_SECRET", encoded)

    def test_unicode_compat_secret_assignments_in_scalar_and_nested_api_success_are_fixed_safe_errors(self) -> None:
        expected = {
            "code": "MCP_UNSAFE_API_RESPONSE",
            "safe_message": "Control API response violated the MCP privacy boundary",
        }
        for assignment in UNICODE_COMPAT_SECRET_ASSIGNMENTS:
            payloads = (
                {"status": "OK", "note": assignment},
                {"status": "OK", "items": [{"note": assignment}]},
                {"status": "OK", "ＡＰＩ．ＫＥＹ": "S3cr3t42"},
                {"status": "OK", "nested": [{"control．nonce": "S3cr3t42"}]},
            )
            for boundary, payload in zip(("scalar", "nested", "key", "nested-key"), payloads):
                with self.subTest(boundary=boundary, assignment=assignment):
                    self.client.response = payload
                    response = self.server.handle(call("agent_result", {"run_id": "run-1"}))
                    encoded = json.dumps(response, ensure_ascii=False)
                    self.assertTrue(response["result"]["isError"])
                    self.assertEqual(expected, json.loads(response["result"]["content"][0]["text"]))
                    self.assertLess(len(encoded), 1024)
                    self.assertNotIn("S3cr3t42", encoded)

    def test_safe_non_ascii_text_and_capability_ref_are_admitted_without_normalization_mutation(self) -> None:
        safe_rpc_id = "请求.安全/路径:一"
        self.assertEqual(
            {"jsonrpc": "2.0", "id": safe_rpc_id, "result": {}},
            self.server.handle(rpc("ping", {}, safe_rpc_id)),
        )

        status = self.server.handle(call(
            "agent_session_status", {"session_id": "会话.安全:一"}, 2,
        ))
        self.assert_tool_payload(status, {"status": "OK"})

        task = json.loads(json.dumps(TASK))
        task["objective"] = "检查 资料．安全/路径：一"
        task["client_identity"]["version"] = "版本．安全：一"
        task["secret_capability_ref"] = "能力．引用：一"
        submitted = self.server.handle(call("agent_submit_task", {
            "request_id": "请求.安全:一", "task": task,
        }, 3))
        self.assert_tool_payload(submitted, {"status": "OK"})

        safe_response = {
            "status": "OK",
            "note": "资料．安全/路径：一",
            "nested": [{"ref": "能力．引用：一"}],
        }
        self.client.response = json.loads(json.dumps(safe_response))
        result = self.server.handle(call("agent_result", {"run_id": "运行.安全:一"}, 4))
        self.assert_tool_payload(result, safe_response)
        self.assertEqual([
            ("GET", "/v1/agent/session?session_id=%E4%BC%9A%E8%AF%9D.%E5%AE%89%E5%85%A8%3A%E4%B8%80"),
            ("POST", "/v1/agent/tasks", task, "请求.安全:一"),
            ("GET", "/v1/agent/result?run_id=%E8%BF%90%E8%A1%8C.%E5%AE%89%E5%85%A8%3A%E4%B8%80"),
        ], self.client.calls)

    def test_safe_dotted_slashed_and_colon_text_is_not_a_privacy_false_positive(self) -> None:
        safe_rpc_id = "rpc.safe/path:1"
        self.assertEqual(
            {"jsonrpc": "2.0", "id": safe_rpc_id, "result": {}},
            self.server.handle(rpc("ping", {}, safe_rpc_id)),
        )

        status = self.server.handle(call(
            "agent_session_status", {"session_id": "session.safe:1"}, 2,
        ))
        self.assert_tool_payload(status, {"status": "OK"})

        task = json.loads(json.dumps(TASK))
        task["objective"] = "inspect fixture.safe/path:revision-1"
        task["client_identity"]["version"] = "fixture.safe/path:revision-1"
        task["secret_capability_ref"] = "opaque.capability:1"
        submitted = self.server.handle(call("agent_submit_task", {
            "request_id": "request.safe:1", "task": task,
        }, 3))
        self.assert_tool_payload(submitted, {"status": "OK"})

        safe_response = {
            "status": "OK",
            "note": "fixture.safe/path:revision-1",
            "nested": [{"ref": "opaque.capability:1"}],
        }
        self.client.response = json.loads(json.dumps(safe_response))
        result = self.server.handle(call("agent_result", {"run_id": "run.safe:1"}, 4))
        self.assert_tool_payload(result, safe_response)
        self.assertEqual([
            ("GET", "/v1/agent/session?session_id=session.safe%3A1"),
            ("POST", "/v1/agent/tasks", task, "request.safe:1"),
            ("GET", "/v1/agent/result?run_id=run.safe%3A1"),
        ], self.client.calls)

    def test_success_payload_type_and_size_are_guarded_before_output(self) -> None:
        cases = (
            (["not", "a", "mapping"], "MCP_INVALID_API_RESPONSE"),
            ({"not_json": object()}, "MCP_INVALID_API_RESPONSE"),
            ({"large": "x" * (self.agent_mcp.MAX_RESULT_BYTES + 1)}, "MCP_API_RESPONSE_TOO_LARGE"),
        )
        for payload, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                self.client.response = payload
                response = self.server.handle(call("agent_result", {"run_id": "run-1"}))
                self.assertTrue(response["result"]["isError"])
                result = json.loads(response["result"]["content"][0]["text"])
                self.assertEqual(expected_code, result["code"])
                self.assertLess(len(json.dumps(response)), 1024)

    def test_notifications_have_no_response_and_ping_stays_offline(self) -> None:
        initialized = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}

        self.assertIsNone(self.server.handle(initialized))
        self.assertEqual({"jsonrpc": "2.0", "id": 2, "result": {}}, self.server.handle(rpc("ping", {}, 2)))
        self.assertEqual([], self.client.calls)

    def test_self_test_is_deterministic_and_constructs_no_control_client(self) -> None:
        output = io.StringIO()
        errors = io.StringIO()

        with (
            patch.object(self.agent_mcp, "ControlApiClient", side_effect=AssertionError("API contact")),
            patch("pathlib.Path.read_text", side_effect=AssertionError("filesystem contact")),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            first = self.agent_mcp.main(["--self-test"])
            second = self.agent_mcp.main(["--self-test"])

        self.assertEqual(0, first)
        self.assertEqual(0, second)
        self.assertEqual(output.getvalue().splitlines()[0], output.getvalue().splitlines()[1])
        self.assertEqual({"ok": True, "protocolVersion": "2024-11-05", "server": "tibia-re-agent", "tools": 5}, json.loads(output.getvalue().splitlines()[0]))
        self.assertEqual("", errors.getvalue())

    def test_module_imports_and_calls_are_statically_isolated(self) -> None:
        source_path = Path(self.agent_mcp.__file__)
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        forbidden_modules = {
            "subprocess", "docker", "ollama", "official_adapter",
            "track_a_authority_bridge", "persistent_store", "store",
        }
        imported: set[str] = set()
        called_names: set[str] = set()
        called_attributes: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.add(node.module or "")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    called_names.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    called_attributes.add(node.func.attr)

        for module in imported:
            self.assertFalse(any(part in module.lower() for part in forbidden_modules), module)
        for name in ("open", "exec", "eval", "compile", "__import__"):
            self.assertNotIn(name, called_names)
        for attribute in ("read_text", "write_text", "unlink", "mkdir", "system", "popen"):
            self.assertNotIn(attribute, called_attributes)


if __name__ == "__main__":
    unittest.main()
