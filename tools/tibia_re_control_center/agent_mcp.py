"""Dependency-free stdio MCP bridge for the local agent Control API."""

from __future__ import annotations

import argparse
import json
import re
import sys
from math import isfinite
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlencode

from .canonical import jcs_dumps
from .control_cli import ControlApiClient, ControlClientError, _default_data_root
from .model import PrivacyError, ValidationError, validate_opaque_id
from .privacy import ensure_no_secret_material

SERVER_NAME = "tibia-re-agent"
SERVER_VERSION = "1.0"
PROTOCOL_VERSION = "2024-11-05"
MAX_INPUT_BYTES = 262_144
MAX_RESULT_BYTES = 262_144
MAX_SAFE_INTEGER = (1 << 53) - 1
MAX_PAGE = 1_000

_CONTROL_COMMANDS = ("PAUSE", "STOP", "RESUME", "SCREENSHOT")
_AGENT_ACTIONS = (
    "SCREENSHOT",
    "SUBMIT_AUTHORIZED_LOGIN",
    "SELECT_CHARACTER",
    "ENTER_WORLD",
    "EXIT_WORLD",
)
_RUNTIME_ACCESS = (
    "none",
    "read_only",
    "ephemeral_isolated",
    "canonical_reuse_or_mutation",
    "canonical_bootstrap",
    "canonical_rebind",
    "canonical_recovery",
    "canonical_boot_epoch_recovery",
)
_TASK_KEYS = (
    "schema",
    "session_id",
    "task_id",
    "run_id",
    "idempotency_key",
    "trusted_main_sha",
    "client_identity",
    "objective",
    "allowed_actions",
    "physical_action_budget",
    "max_attempts",
    "deadline_epoch_ms",
    "runtime_access",
    "required_evidence",
    "secret_capability_ref",
)
_SAFE_CODE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_AUTHORITY_DESCRIPTION = (
    " Model/task text cannot expand Track A authority, credential permission, "
    "action allowlists, or budgets."
)


def _id_schema() -> dict[str, object]:
    return {"type": "string", "minLength": 1, "maxLength": 128}


def _task_schema() -> dict[str, object]:
    return {
        "type": "object",
        "properties": {
            "schema": {"type": "string", "const": "otclient.local-agent.task.v1"},
            "session_id": _id_schema(),
            "task_id": _id_schema(),
            "run_id": _id_schema(),
            "idempotency_key": _id_schema(),
            "trusted_main_sha": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
            "client_identity": {
                "type": "object",
                "properties": {
                    "version": {"type": "string", "minLength": 1},
                    "size": {
                        "oneOf": [
                            {"type": "integer", "minimum": 0, "maximum": MAX_SAFE_INTEGER},
                            {"type": "string", "minLength": 1},
                        ],
                    },
                    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                },
                "required": ["version", "size", "sha256"],
                "additionalProperties": False,
            },
            "objective": {"type": "string", "minLength": 1},
            "allowed_actions": {
                "type": "array",
                "items": {"type": "string", "enum": list(_AGENT_ACTIONS)},
            },
            "physical_action_budget": {
                "type": "integer",
                "minimum": 0,
                "maximum": MAX_SAFE_INTEGER,
            },
            "max_attempts": {"type": "integer", "minimum": 1, "maximum": 3},
            "deadline_epoch_ms": {
                "type": "integer",
                "minimum": 0,
                "maximum": MAX_SAFE_INTEGER,
            },
            "runtime_access": {"type": "string", "enum": list(_RUNTIME_ACCESS)},
            "required_evidence": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
            },
            "secret_capability_ref": {
                "oneOf": [_id_schema(), {"type": "null"}],
            },
        },
        "required": list(_TASK_KEYS),
        "additionalProperties": False,
    }


def _tools() -> list[dict[str, object]]:
    return [
        {
            "name": "agent_session_status",
            "description": "Read one secret-safe agent session." + _AUTHORITY_DESCRIPTION,
            "inputSchema": {
                "type": "object",
                "properties": {"session_id": _id_schema()},
                "required": ["session_id"],
                "additionalProperties": False,
            },
        },
        {
            "name": "agent_submit_task",
            "description": "Submit one exact TaskEnvelope.v1 mapping." + _AUTHORITY_DESCRIPTION,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "request_id": _id_schema(),
                    "task": _task_schema(),
                },
                "required": ["request_id", "task"],
                "additionalProperties": False,
            },
        },
        {
            "name": "agent_control",
            "description": (
                "Send only PAUSE, STOP, RESUME, or read-only SCREENSHOT; no low-level input "
                "or process control is exposed." + _AUTHORITY_DESCRIPTION
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "request_id": _id_schema(),
                    "session_id": _id_schema(),
                    "command": {"type": "string", "enum": list(_CONTROL_COMMANDS)},
                },
                "required": ["request_id", "session_id", "command"],
                "additionalProperties": False,
            },
        },
        {
            "name": "agent_events",
            "description": "Poll one bounded secret-safe agent event page." + _AUTHORITY_DESCRIPTION,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "session_id": _id_schema(),
                    "cursor": {"type": "integer", "minimum": 0, "default": 0},
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": MAX_PAGE,
                        "default": 100,
                    },
                },
                "required": ["session_id"],
                "additionalProperties": False,
            },
        },
        {
            "name": "agent_result",
            "description": "Read one secret-safe agent result." + _AUTHORITY_DESCRIPTION,
            "inputSchema": {
                "type": "object",
                "properties": {"run_id": _id_schema()},
                "required": ["run_id"],
                "additionalProperties": False,
            },
        },
    ]


class _InvalidParams(ValueError):
    pass


class _PrivacyRejected(_InvalidParams):
    pass


class _DuplicateKey(ValueError):
    pass


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _reject_json_constant(_value: str) -> object:
    raise ValueError("noncanonical JSON number")


def _exact_mapping(value: object, keys: set[str]) -> dict[str, object]:
    if not isinstance(value, dict) or set(value) != keys:
        raise _InvalidParams("arguments are missing or unknown")
    if not all(isinstance(key, str) for key in value):
        raise _InvalidParams("argument keys must be strings")
    return value


def _validate_json_structure(
    value: object,
    *,
    depth: int = 0,
    count: list[int] | None = None,
) -> None:
    if count is None:
        count = [0]
    count[0] += 1
    if count[0] > 4_096 or depth > 32:
        raise _InvalidParams("value exceeds the admitted structure bounds")
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise _InvalidParams("mapping keys must be strings")
            try:
                key.encode("utf-8", "strict")
            except UnicodeEncodeError as exc:
                raise _InvalidParams("mapping keys must be valid UTF-8") from exc
            _validate_json_structure(child, depth=depth + 1, count=count)
        return
    if isinstance(value, (list, tuple)):
        for child in value:
            _validate_json_structure(child, depth=depth + 1, count=count)
        return
    if isinstance(value, str):
        try:
            value.encode("utf-8", "strict")
        except UnicodeEncodeError as exc:
            raise _InvalidParams("text must be valid UTF-8") from exc
        return
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise _InvalidParams("integer is outside the JSON-safe range")
        return
    if isinstance(value, float):
        if not isfinite(value):
            raise _InvalidParams("number must be finite")
        return
    raise _InvalidParams("value contains an unsupported JSON type")


def _guard_secret_safe(
    value: object,
    *,
    identifier: bool = False,
    require_text: bool = False,
    key_path: str,
) -> object:
    _validate_json_structure(value)
    try:
        ensure_no_secret_material(value, key_path=key_path)
    except PrivacyError as exc:
        raise _PrivacyRejected("secret material is not admitted") from exc
    if identifier or require_text:
        if not isinstance(value, str) or not value:
            raise _InvalidParams("a non-empty string is required")
    if identifier:
        try:
            validate_opaque_id(value, field_name=key_path, max_bytes=128)
        except ValidationError as exc:
            raise _InvalidParams("identifier is outside the admitted grammar") from exc
    return value


def _text(value: object, *, identifier: bool = False, key_path: str = "mcp.text") -> str:
    return cast(str, _guard_secret_safe(
        value,
        identifier=identifier,
        require_text=True,
        key_path=key_path,
    ))


def _integer(value: object, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum or value > maximum:
        raise _InvalidParams("integer is outside the admitted range")
    return value


def _validate_task(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _InvalidParams("task must be a mapping")
    _guard_secret_safe(value, key_path="mcp.task")
    task = _exact_mapping(value, set(_TASK_KEYS))
    if task["schema"] != "otclient.local-agent.task.v1":
        raise _InvalidParams("task schema is not admitted")
    for field in ("session_id", "task_id", "run_id", "idempotency_key"):
        _text(task[field], identifier=True)
    if not isinstance(task["trusted_main_sha"], str) or not _SHA40.fullmatch(task["trusted_main_sha"]):
        raise _InvalidParams("trusted_main_sha is invalid")
    identity = _exact_mapping(task["client_identity"], {"version", "size", "sha256"})
    _text(identity["version"])
    size = identity["size"]
    if isinstance(size, str):
        _text(size)
    else:
        _integer(size, 0, MAX_SAFE_INTEGER)
    if not isinstance(identity["sha256"], str) or not _SHA256.fullmatch(identity["sha256"]):
        raise _InvalidParams("client identity SHA is invalid")
    _text(task["objective"])
    actions = task["allowed_actions"]
    if not isinstance(actions, list) or any(action not in _AGENT_ACTIONS for action in actions):
        raise _InvalidParams("allowed_actions contains an unknown action")
    _integer(task["physical_action_budget"], 0, MAX_SAFE_INTEGER)
    _integer(task["max_attempts"], 1, 3)
    _integer(task["deadline_epoch_ms"], 0, MAX_SAFE_INTEGER)
    if task["runtime_access"] not in _RUNTIME_ACCESS:
        raise _InvalidParams("runtime_access is not admitted")
    evidence = task["required_evidence"]
    if not isinstance(evidence, list):
        raise _InvalidParams("required_evidence must be an array")
    for item in evidence:
        _text(item)
    secret_ref = task["secret_capability_ref"]
    if secret_ref is not None:
        _text(secret_ref, identifier=True)
    return task


def _validate_arguments(name: str, value: object) -> dict[str, object]:
    if name == "agent_session_status":
        arguments = _exact_mapping(value, {"session_id"})
        _text(arguments["session_id"], identifier=True)
        return arguments
    if name == "agent_submit_task":
        arguments = _exact_mapping(value, {"request_id", "task"})
        _text(arguments["request_id"], identifier=True)
        _validate_task(arguments["task"])
        return arguments
    if name == "agent_control":
        arguments = _exact_mapping(value, {"request_id", "session_id", "command"})
        _text(arguments["request_id"], identifier=True)
        _text(arguments["session_id"], identifier=True)
        if arguments["command"] not in _CONTROL_COMMANDS:
            raise _InvalidParams("control command is not admitted")
        return arguments
    if name == "agent_events":
        if not isinstance(value, dict) or not {"session_id"}.issubset(value) or set(value) - {"session_id", "cursor", "limit"}:
            raise _InvalidParams("arguments are missing or unknown")
        _text(value["session_id"], identifier=True)
        _integer(value.get("cursor", 0), 0, 2_147_483_647)
        _integer(value.get("limit", 100), 1, MAX_PAGE)
        return value
    if name == "agent_result":
        arguments = _exact_mapping(value, {"run_id"})
        _text(arguments["run_id"], identifier=True)
        return arguments
    raise _InvalidParams("unknown tool")


def _rpc_error(request_id: object, code: int, message: str) -> dict[str, object]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message[:128]},
    }


def _safe_rpc_id(value: object) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, str):
        try:
            encoded = value.encode("utf-8", "strict")
            _guard_secret_safe(value, key_path="jsonrpc.id")
        except (UnicodeEncodeError, _InvalidParams):
            return False
        return len(encoded) <= 128
    if isinstance(value, int):
        return abs(value) <= MAX_SAFE_INTEGER
    return False


def _fixed_tool_error(code: str, safe_message: str) -> dict[str, object]:
    return {
        "content": [{"type": "text", "text": jcs_dumps({
            "code": code,
            "safe_message": safe_message,
        })}],
        "isError": True,
    }


def _tool_payload(payload: object, *, is_error: bool = False) -> dict[str, object]:
    if not isinstance(payload, dict):
        return _fixed_tool_error(
            "MCP_INVALID_API_RESPONSE",
            "Control API response was not valid JSON",
        )
    try:
        _guard_secret_safe(payload, key_path="control_api.response")
    except _PrivacyRejected:
        return _fixed_tool_error(
            "MCP_UNSAFE_API_RESPONSE",
            "Control API response violated the MCP privacy boundary",
        )
    except _InvalidParams:
        return _fixed_tool_error(
            "MCP_INVALID_API_RESPONSE",
            "Control API response was not valid JSON",
        )
    try:
        text = jcs_dumps(payload)
    except (TypeError, ValueError, RecursionError):
        return _fixed_tool_error(
            "MCP_INVALID_API_RESPONSE",
            "Control API response was not valid JSON",
        )
    if len(text.encode("utf-8")) > MAX_RESULT_BYTES:
        return _fixed_tool_error(
            "MCP_API_RESPONSE_TOO_LARGE",
            "Control API response exceeded the MCP result bound",
        )
    return {"content": [{"type": "text", "text": text}], "isError": is_error}


class AgentMcpServer:
    """Translate the exact MCP allowlist into ControlApiClient calls only."""

    def __init__(self, client: Any) -> None:
        self.client = client

    def _call_tool(self, name: str, arguments: dict[str, object]) -> dict[str, object]:
        try:
            if name == "agent_session_status":
                payload = self.client.get("/v1/agent/session?" + urlencode({
                    "session_id": arguments["session_id"],
                }))
            elif name == "agent_submit_task":
                payload = self.client.post(
                    "/v1/agent/tasks",
                    arguments["task"],
                    request_id=arguments["request_id"],
                )
            elif name == "agent_control":
                payload = self.client.post(
                    "/v1/agent/control",
                    {"session_id": arguments["session_id"], "command": arguments["command"]},
                    request_id=arguments["request_id"],
                )
            elif name == "agent_events":
                payload = self.client.get("/v1/agent/events?" + urlencode({
                    "session_id": arguments["session_id"],
                    "cursor": arguments.get("cursor", 0),
                    "limit": arguments.get("limit", 100),
                }))
            elif name == "agent_result":
                payload = self.client.get("/v1/agent/result?" + urlencode({
                    "run_id": arguments["run_id"],
                }))
            else:
                raise _InvalidParams("unknown tool")
            return _tool_payload(payload)
        except ControlClientError as exc:
            code = exc.payload.get("code")
            safe_code = code if isinstance(code, str) and _SAFE_CODE.fullmatch(code) else "CONTROL_API_ERROR"
            return _tool_payload({
                "code": safe_code,
                "safe_message": "Control API request failed safely",
                "status": exc.status,
            }, is_error=True)
        except Exception:  # noqa: BLE001 - boundary never exposes dependency exceptions
            return _tool_payload({
                "code": "MCP_INTERNAL_ERROR",
                "safe_message": "MCP tool execution failed safely",
            }, is_error=True)

    def handle(self, request: object) -> dict[str, object] | None:
        if not isinstance(request, dict):
            return _rpc_error(None, -32600, "Invalid Request")
        if set(request) - {"jsonrpc", "id", "method", "params"}:
            return _rpc_error(None, -32600, "Invalid Request")
        request_id = request.get("id")
        if request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
            return _rpc_error(None, -32600, "Invalid Request")
        if "id" in request and not _safe_rpc_id(request_id):
            return _rpc_error(None, -32600, "Invalid Request")
        method = request["method"]
        params = request.get("params", {})
        if method == "notifications/initialized" and "id" not in request:
            return None
        if "id" not in request:
            return None
        if method == "initialize":
            if not isinstance(params, dict):
                return _rpc_error(request_id, -32602, "Invalid params")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                },
            }
        if method == "ping":
            if not isinstance(params, dict):
                return _rpc_error(request_id, -32602, "Invalid params")
            return {"jsonrpc": "2.0", "id": request_id, "result": {}}
        if method == "tools/list":
            if not isinstance(params, dict) or params:
                return _rpc_error(request_id, -32602, "Invalid params")
            return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": _tools()}}
        if method == "tools/call":
            try:
                call_params = _exact_mapping(params, {"name", "arguments"})
                name = _text(call_params["name"])
                if name not in {tool["name"] for tool in _tools()}:
                    raise _InvalidParams("unknown tool")
                arguments = _validate_arguments(name, call_params["arguments"])
            except _InvalidParams:
                return _rpc_error(request_id, -32602, "Invalid params")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": self._call_tool(name, arguments),
            }
        return _rpc_error(request_id, -32601, "Method not found")

    def serve(self, input_stream: Any, output_stream: Any) -> None:
        while True:
            line = input_stream.readline(MAX_INPUT_BYTES + 2)
            if line == "":
                return
            try:
                encoded_size = len(line.encode("utf-8", "strict"))
            except UnicodeEncodeError:
                encoded_size = MAX_INPUT_BYTES + 1
            if encoded_size > MAX_INPUT_BYTES or not line.endswith("\n"):
                while line != "" and not line.endswith("\n"):
                    line = input_stream.readline(MAX_INPUT_BYTES + 2)
                response = _rpc_error(None, -32700, "Parse error")
            elif not line.strip():
                continue
            else:
                try:
                    request = json.loads(
                        line,
                        object_pairs_hook=_no_duplicate_keys,
                        parse_constant=_reject_json_constant,
                    )
                except (json.JSONDecodeError, _DuplicateKey, ValueError):
                    response = _rpc_error(None, -32700, "Parse error")
                else:
                    response = self.handle(request)
            if response is not None:
                output_stream.write(jcs_dumps(response) + "\n")
                output_stream.flush()


class _OfflineSelfTestClient:
    def get(self, _path: str) -> dict[str, object]:
        raise AssertionError("offline self-test attempted API access")

    def post(self, _path: str, _body: dict[str, object], *, request_id: str) -> dict[str, object]:
        raise AssertionError(f"offline self-test attempted API access for {request_id}")


def _self_test() -> dict[str, object]:
    server = AgentMcpServer(_OfflineSelfTestClient())
    initialized = server.handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": PROTOCOL_VERSION, "capabilities": {}},
    })
    listed = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    if (
        not isinstance(initialized, dict)
        or initialized.get("result", {}).get("protocolVersion") != PROTOCOL_VERSION
        or not isinstance(listed, dict)
        or len(listed.get("result", {}).get("tools", [])) != 5
    ):
        raise AssertionError("offline MCP self-test failed")
    return {"ok": True, "protocolVersion": PROTOCOL_VERSION, "server": SERVER_NAME, "tools": 5}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Narrow stdio MCP bridge for the TIBIA RE local agent")
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.self_test:
        print(jcs_dumps(_self_test()))
        return 0
    try:
        client = ControlApiClient(args.data_dir or _default_data_root())
    except ControlClientError:
        print(jcs_dumps({
            "code": "CONTROL_RUNTIME_UNAVAILABLE",
            "safe_message": "Control API runtime metadata is unavailable",
        }), file=sys.stderr)
        return 2
    AgentMcpServer(client).serve(sys.stdin, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
