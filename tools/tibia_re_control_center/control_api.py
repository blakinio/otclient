from __future__ import annotations

import argparse
import hmac
import json
import os
import re
import secrets
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit

from .canonical import jcs_dumps
from .control_domain import ControlDomainError, ControlDomainService, DomainReply
from .control_ui import render_control_ui
from .model import SimulatedCrash, ValidationError
from .native_login_socket import lifecycle_from_environment

MAX_BODY_BYTES = 262_144
MAX_HEADER_BYTES = 32_768
MAX_PAGE = 1_000
MAX_CONCURRENT_REQUESTS = 64
MAX_REJECTION_DRAIN_BYTES = 65_536
REQUEST_TIMEOUT_SECONDS = 5.0
DEFAULT_PAGE = 100
REQUEST_ID_HEADER = "X-Tibia-RE-Request-Id"
NONCE_HEADER = "X-Tibia-RE-Control-Nonce"
_RUN_CONTROL_RE = re.compile(r"^/v1/runs/([^/]+)/(pause|resume|abort)$")
_RUN_ARTIFACT_RE = re.compile(r"^/v1/runs/([^/]+)/artifacts$")
_RUN_RE = re.compile(r"^/v1/runs/([^/]+)$")
_ACTION_RE = re.compile(r"^/v1/actions/([^/]+)$")


def _allowed_methods(path: str) -> frozenset[str]:
    methods: set[str] = set()
    if path == "/":
        methods.add("GET")
    if path in {
        "/v1/status",
        "/v1/capabilities",
        "/v1/scenarios",
        "/v1/runs",
        "/v1/events",
        "/v1/agent/session",
        "/v1/agent/events",
        "/v1/agent/result",
        "/v1/native-login/status",
    } or _RUN_ARTIFACT_RE.fullmatch(path) or _RUN_RE.fullmatch(path) or _ACTION_RE.fullmatch(path):
        methods.add("GET")
    if path in {
        "/v1/runs",
        "/v1/experiments/one-step",
        "/v1/stop-all",
        "/v1/reset-stop",
        "/v1/agent/tasks",
        "/v1/agent/chat",
        "/v1/agent/control",
        "/v1/native-login/start",
    } or _RUN_CONTROL_RE.fullmatch(path):
        methods.add("POST")
    return frozenset(methods)


class _DuplicateKey(ValueError):
    pass


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _write_private_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    try:
        os.chmod(temporary, 0o600)
    except OSError:
        pass
    os.replace(temporary, path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


class _ControlHttpServer(ThreadingHTTPServer):
    daemon_threads = False
    block_on_close = True
    allow_reuse_address = False
    request_queue_size = 32

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._request_slots = threading.BoundedSemaphore(MAX_CONCURRENT_REQUESTS)
        super().__init__(*args, **kwargs)

    def process_request(self, request: Any, client_address: Any) -> None:
        if not self._request_slots.acquire(blocking=False):
            try:
                payload = jcs_dumps({
                    "code": "CONTROL_SERVER_BUSY",
                    "safe_message": "Control API concurrent request limit reached",
                    "request_id": None,
                    "resource_id": None,
                    "retryable": True,
                }).encode("utf-8")
                response = (
                    b"HTTP/1.1 503 Service Unavailable\r\n"
                    b"Content-Type: application/json; charset=utf-8\r\n"
                    b"Cache-Control: no-store\r\n"
                    b"Connection: close\r\n"
                    + f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii")
                    + payload
                )
                request.sendall(response)
            finally:
                self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self._request_slots.release()
            raise

    def process_request_thread(self, request: Any, client_address: Any) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._request_slots.release()


class ControlRequestHandler(BaseHTTPRequestHandler):
    server_version = "TibiaREControl/1"
    sys_version = ""

    @property
    def control(self) -> ControlApiServer:
        return self.server.control  # type: ignore[attr-defined]

    def setup(self) -> None:
        super().setup()
        self.connection.settimeout(REQUEST_TIMEOUT_SECONDS)

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _headers_size(self) -> int:
        return sum(len(str(key).encode("utf-8")) + len(str(value).encode("utf-8")) + 4 for key, value in self.headers.items())

    def _send_json(self, status: int, payload: dict[str, Any], *, request_id: str | None = None) -> None:
        raw = jcs_dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Pragma", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        if request_id is not None:
            self.send_header("X-Tibia-RE-Request-Id", request_id)
        self.end_headers()
        self.wfile.write(raw)

    def _error(self, status: int, code: str, message: str, *, request_id: str | None = None, resource_id: str | None = None, retryable: bool = False) -> None:
        self._send_json(status, {
            "code": code,
            "safe_message": message,
            "request_id": request_id,
            "resource_id": resource_id,
            "retryable": retryable,
        }, request_id=request_id)

    def _single_header(self, name: str) -> str | None:
        values = self.headers.get_all(name) or []
        if len(values) != 1:
            return None
        return values[0]

    def _validate_transport(self, *, api: bool) -> bool:
        if self._headers_size() > MAX_HEADER_BYTES:
            self._error(HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE, "CONTROL_HEADERS_TOO_LARGE", "request headers exceed the admitted size")
            return False
        host = self._single_header("Host")
        if host != self.control.authority:
            self._error(HTTPStatus.MISDIRECTED_REQUEST, "CONTROL_HOST_REJECTED", "Host is not the bound Control API authority")
            return False
        split = urlsplit(self.path)
        query = parse_qs(split.query, keep_blank_values=True)
        decoded_target = unquote(self.path)
        if self.control.nonce in decoded_target or any(key.lower() in {"nonce", "control_nonce", "control-nonce"} for key in query):
            self._error(HTTPStatus.BAD_REQUEST, "CONTROL_NONCE_IN_URL", "control nonce is forbidden in URL data")
            return False
        if not api:
            return True
        nonce = self._single_header(NONCE_HEADER)
        if nonce is None or not hmac.compare_digest(nonce, self.control.nonce):
            self._error(HTTPStatus.UNAUTHORIZED, "CONTROL_AUTH_REQUIRED", "valid Control API nonce is required")
            return False
        origin_values = self.headers.get_all("Origin") or []
        if len(origin_values) > 1:
            self._error(HTTPStatus.FORBIDDEN, "CONTROL_ORIGIN_REJECTED", "multiple Origin headers are forbidden")
            return False
        if origin_values and origin_values[0] != self.control.origin:
            self._error(HTTPStatus.FORBIDDEN, "CONTROL_ORIGIN_REJECTED", "browser Origin is not the exact Control API origin")
            return False
        return True

    def _parsed_path(self) -> tuple[str, dict[str, list[str]]]:
        split = urlsplit(self.path)
        return split.path, parse_qs(split.query, keep_blank_values=True)

    @staticmethod
    def _bounded_int(query: dict[str, list[str]], key: str, default: int, maximum: int) -> int:
        values = query.get(key)
        if values is None:
            return default
        if len(values) != 1:
            raise ControlDomainError("CONTROL_QUERY_INVALID", f"query parameter {key} must occur once")
        try:
            value = int(values[0], 10)
        except ValueError as exc:
            raise ControlDomainError("CONTROL_QUERY_INVALID", f"query parameter {key} must be an integer") from exc
        if value < 0 or value > maximum:
            raise ControlDomainError("CONTROL_QUERY_INVALID", f"query parameter {key} is outside the admitted range")
        return value

    def _page(self, query: dict[str, list[str]], *, cursor: bool = False) -> tuple[int, int]:
        admitted = {"limit", "cursor" if cursor else "offset"}
        if set(query) - admitted:
            raise ControlDomainError("CONTROL_QUERY_INVALID", "unknown query parameter")
        limit = self._bounded_int(query, "limit", DEFAULT_PAGE, MAX_PAGE)
        if limit < 1:
            raise ControlDomainError("CONTROL_QUERY_INVALID", "limit must be at least 1")
        second = self._bounded_int(query, "cursor" if cursor else "offset", 0, 2_147_483_647)
        return limit, second

    @staticmethod
    def _required_query(query: dict[str, list[str]], required: set[str]) -> dict[str, str]:
        if set(query) != required:
            raise ControlDomainError(
                "CONTROL_QUERY_INVALID",
                "query parameters are missing or unknown",
            )
        result: dict[str, str] = {}
        for key in required:
            values = query[key]
            if len(values) != 1 or not values[0]:
                raise ControlDomainError(
                    "CONTROL_QUERY_INVALID",
                    f"query parameter {key} must occur once and be non-empty",
                )
            result[key] = values[0]
        return result

    def _read_body(self) -> Any:
        if self.headers.get("Transfer-Encoding") is not None:
            raise ControlDomainError("CONTROL_TRANSFER_ENCODING_REJECTED", "chunked or transformed request bodies are not admitted", http_status=400)
        values = self.headers.get_all("Content-Length") or []
        if len(values) != 1:
            raise ControlDomainError("CONTROL_CONTENT_LENGTH_REQUIRED", "exactly one Content-Length header is required", http_status=411)
        try:
            length = int(values[0], 10)
        except ValueError as exc:
            raise ControlDomainError("CONTROL_CONTENT_LENGTH_INVALID", "Content-Length is invalid") from exc
        if length < 0:
            raise ControlDomainError("CONTROL_CONTENT_LENGTH_INVALID", "Content-Length is invalid")
        if length > MAX_BODY_BYTES:
            overflow = length - MAX_BODY_BYTES
            if overflow <= MAX_REJECTION_DRAIN_BYTES:
                self.rfile.read(length)
            self.close_connection = True
            raise ControlDomainError("CONTROL_BODY_TOO_LARGE", "request body exceeds the admitted size", http_status=413)
        media_type = (self.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
        if media_type != "application/json":
            raise ControlDomainError("CONTROL_CONTENT_TYPE_REQUIRED", "POST requests require application/json", http_status=415)
        raw = self.rfile.read(length)
        if len(raw) != length:
            raise ControlDomainError("CONTROL_BODY_TRUNCATED", "request body was truncated")
        try:
            text = raw.decode("utf-8", "strict")
            return json.loads(text, object_pairs_hook=_no_duplicate_keys)
        except UnicodeDecodeError as exc:
            raise ControlDomainError("CONTROL_BODY_UTF8_REQUIRED", "request body must be valid UTF-8") from exc
        except _DuplicateKey as exc:
            raise ControlDomainError("CONTROL_BODY_DUPLICATE_KEY", "duplicate JSON keys are forbidden") from exc
        except json.JSONDecodeError as exc:
            raise ControlDomainError("CONTROL_BODY_JSON_INVALID", "request body must be valid JSON") from exc

    def _validate_method(self, method: str, path: str) -> bool:
        allowed = _allowed_methods(path)
        if not allowed:
            self._error(HTTPStatus.NOT_FOUND, "CONTROL_ROUTE_NOT_FOUND", "resource was not found")
            return False
        if method not in allowed:
            self._error(HTTPStatus.METHOD_NOT_ALLOWED, "CONTROL_METHOD_NOT_ALLOWED", "HTTP method is not admitted")
            return False
        return True

    def do_OPTIONS(self) -> None:
        path, _ = self._parsed_path()
        if not self._validate_transport(api=path.startswith("/v1/")):
            return
        self._validate_method("OPTIONS", path)

    def do_GET(self) -> None:
        path, query = self._parsed_path()
        if not self._validate_transport(api=path.startswith("/v1/")):
            return
        if not self._validate_method("GET", path):
            return
        if path == "/":
            if query:
                self._error(HTTPStatus.BAD_REQUEST, "CONTROL_QUERY_INVALID", "browser bootstrap URL does not accept query parameters")
                return
            csp_nonce = secrets.token_urlsafe(18)
            raw = render_control_ui(self.control.nonce, csp_nonce).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Pragma", "no-cache")
            self.send_header("Content-Security-Policy", f"default-src 'none'; script-src 'nonce-{csp_nonce}'; style-src 'nonce-{csp_nonce}'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(raw)
            return
        try:
            if path == "/v1/status":
                if query:
                    raise ControlDomainError("CONTROL_QUERY_INVALID", "status does not accept query parameters")
                payload = self.control.domain.status()
            elif path == "/v1/native-login/status":
                if query:
                    raise ControlDomainError("CONTROL_QUERY_INVALID", "native login status does not accept query parameters")
                payload = self.control.domain.native_login_lifecycle.status()
            elif path == "/v1/capabilities":
                if query:
                    raise ControlDomainError("CONTROL_QUERY_INVALID", "capabilities does not accept query parameters")
                payload = self.control.domain.capabilities()
            elif path == "/v1/scenarios":
                if query:
                    raise ControlDomainError("CONTROL_QUERY_INVALID", "scenarios does not accept query parameters")
                payload = self.control.domain.scenarios()
            elif path == "/v1/runs":
                limit, offset = self._page(query)
                payload = self.control.domain.list_runs(offset=offset, limit=limit)
            elif path == "/v1/events":
                limit, cursor = self._page(query, cursor=True)
                payload = self.control.domain.events(cursor=cursor, limit=limit)
            elif path == "/v1/agent/session":
                values = self._required_query(query, {"session_id"})
                payload = self.control.domain.agent_session(values["session_id"])
            elif path == "/v1/agent/events":
                values = self._required_query(query, {"session_id", "cursor", "limit"})
                numeric_query = {key: query[key] for key in ("cursor", "limit")}
                limit, cursor = self._page(numeric_query, cursor=True)
                payload = self.control.domain.agent_events(
                    values["session_id"],
                    cursor=cursor,
                    limit=limit,
                )
            elif path == "/v1/agent/result":
                values = self._required_query(query, {"run_id"})
                payload = self.control.domain.agent_result(values["run_id"])
            elif (match := _RUN_ARTIFACT_RE.fullmatch(path)) is not None:
                if query:
                    raise ControlDomainError("CONTROL_QUERY_INVALID", "artifact view does not accept query parameters")
                payload = self.control.domain.artifacts(unquote(match.group(1)))
            elif (match := _RUN_RE.fullmatch(path)) is not None:
                if query:
                    raise ControlDomainError("CONTROL_QUERY_INVALID", "run view does not accept query parameters")
                payload = self.control.domain.run_detail(unquote(match.group(1)))
            elif (match := _ACTION_RE.fullmatch(path)) is not None:
                if query:
                    raise ControlDomainError("CONTROL_QUERY_INVALID", "action view does not accept query parameters")
                payload = self.control.domain.action_detail(unquote(match.group(1)))
            else:
                raise ControlDomainError("CONTROL_ROUTE_NOT_FOUND", "resource was not found", http_status=404)
            self._send_json(HTTPStatus.OK, payload)
        except ControlDomainError as exc:
            self._error(exc.http_status, exc.code, exc.safe_message, retryable=exc.retryable)
        except ValidationError as exc:
            status = HTTPStatus.CONFLICT if exc.code == "CONTROL_EVENT_BACKPRESSURE" else HTTPStatus.BAD_REQUEST
            self._error(status, exc.code, exc.safe_message)
        except Exception:  # noqa: BLE001 - boundary sanitizes all unexpected failures
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "CONTROL_INTERNAL_ERROR", "read operation failed safely")

    def do_POST(self) -> None:
        path, query = self._parsed_path()
        if not self._validate_transport(api=path.startswith("/v1/")):
            return
        if not self._validate_method("POST", path):
            return
        if query:
            self._error(HTTPStatus.BAD_REQUEST, "CONTROL_QUERY_INVALID", "POST routes do not accept query parameters")
            return
        request_id = self._single_header(REQUEST_ID_HEADER)
        if request_id is None:
            self._error(HTTPStatus.BAD_REQUEST, "CONTROL_REQUEST_ID_REQUIRED", "exactly one request id header is required")
            return
        try:
            body = self._read_body()
            operation: str
            handler: Any
            if path == "/v1/runs":
                operation, handler = "CREATE_RUN", self.control.domain.create_run
            elif path == "/v1/experiments/one-step":
                operation, handler = "ONE_STEP_EXPERIMENT", self.control.domain.one_step
            elif path == "/v1/stop-all":
                operation, handler = "STOP_ALL", self.control.domain.stop_all
            elif path == "/v1/reset-stop":
                operation, handler = "RESET_STOP", self.control.domain.reset_stop
            elif path == "/v1/native-login/start":
                operation, handler = "NATIVE_LOGIN_START", self.control.domain.native_login_start
            elif path == "/v1/agent/tasks":
                operation, handler = "AGENT_TASK", self.control.domain.agent_submit_task
            elif path == "/v1/agent/chat":
                operation, handler = "AGENT_CHAT", self.control.domain.agent_chat
            elif path == "/v1/agent/control":
                operation, handler = "AGENT_CONTROL", self.control.domain.agent_control
            elif (match := _RUN_CONTROL_RE.fullmatch(path)) is not None:
                run_id = unquote(match.group(1))
                verb = match.group(2)
                operation = {"pause": "PAUSE_RUN", "resume": "RESUME_RUN", "abort": "ABORT_RUN"}[verb]
                handler = lambda resource_id, rid, normalized, op=operation, target=run_id: self.control.domain.run_control(resource_id, rid, normalized, operation=op, run_id=target)
            else:
                self._error(HTTPStatus.NOT_FOUND, "CONTROL_ROUTE_NOT_FOUND", "resource was not found", request_id=request_id)
                return
            reply: DomainReply = self.control.domain.process_post(
                canonical_path=path,
                operation=operation,
                request_id=request_id,
                body=body,
                handler=handler,
            )
            self._send_json(reply.code, reply.body, request_id=request_id)
        except ControlDomainError as exc:
            self._error(exc.http_status, exc.code, exc.safe_message, request_id=request_id, retryable=exc.retryable)
        except ValidationError as exc:
            status = HTTPStatus.CONFLICT if exc.code in {"REQUEST_LEDGER_CONTRADICTION", "IDEMPOTENCY_CONFLICT"} else HTTPStatus.BAD_REQUEST
            self._error(status, exc.code, exc.safe_message, request_id=request_id)
        except SimulatedCrash:
            self._error(HTTPStatus.SERVICE_UNAVAILABLE, "CONTROL_SIMULATED_CRASH", "simulated crash interrupted the response", request_id=request_id)
        except Exception:  # noqa: BLE001 - boundary sanitizes all unexpected failures
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "CONTROL_INTERNAL_ERROR", "request failed safely", request_id=request_id)

    def do_PUT(self) -> None:
        self._method_not_allowed()

    def do_DELETE(self) -> None:
        self._method_not_allowed()

    def do_PATCH(self) -> None:
        self._method_not_allowed()

    def _method_not_allowed(self) -> None:
        path, _ = self._parsed_path()
        if not self._validate_transport(api=path.startswith("/v1/")):
            return
        self._validate_method(self.command, path)


class ControlApiServer:
    def __init__(self, data_root: str | Path, *, host: str = "127.0.0.1", port: int = 0, domain: ControlDomainService | None = None) -> None:
        if host != "127.0.0.1":
            raise ValueError("Control API binds only exact IPv4 loopback 127.0.0.1")
        if isinstance(port, bool) or not isinstance(port, int) or port < 0 or port > 65535:
            raise ValueError("port must be in 0..65535")
        self.data_root = Path(data_root).expanduser().resolve()
        self.domain = domain or ControlDomainService(
            str(self.data_root),
            native_login_lifecycle=lifecycle_from_environment(),
        )
        self.nonce = secrets.token_bytes(32).hex()
        self._httpd = _ControlHttpServer((host, port), ControlRequestHandler)
        self._httpd.control = self  # type: ignore[attr-defined]
        bound_host, bound_port = self._httpd.server_address[:2]
        if bound_host != "127.0.0.1":
            self._httpd.server_close()
            raise RuntimeError("Control API escaped exact loopback binding")
        self.host = bound_host
        self.port = int(bound_port)
        self.authority = f"127.0.0.1:{self.port}"
        self.origin = f"http://{self.authority}"
        self.runtime_dir = self.data_root / "control"
        self.runtime_file = self.runtime_dir / "control-runtime.json"
        self.nonce_file = self.runtime_dir / "control.nonce"
        _write_private_text(self.nonce_file, self.nonce + "\n")
        _write_private_text(self.runtime_file, jcs_dumps({
            "schema_version": 1,
            "host": self.host,
            "port": self.port,
            "origin": self.origin,
            "backend_epoch": self.domain.backend_epoch,
            "nonce_transport": "PRIVATE_FILE",
            "official_client_access": "NONE",
        }) + "\n")
        self._thread: threading.Thread | None = None
        self._closed = False

    def start(self) -> ControlApiServer:
        if self._thread is not None:
            return self
        self._thread = threading.Thread(target=self._httpd.serve_forever, name="tibia-re-control-api", daemon=True)
        self._thread.start()
        return self

    def serve_forever(self) -> None:
        self._httpd.serve_forever()

    def close(self, *, shutdown_listener: bool = True) -> bool:
        if self._closed:
            return True
        if shutdown_listener and self._thread is not None:
            self._httpd.shutdown()
            self._thread.join(timeout=5)
        self._httpd.server_close()
        clean = self.domain.close()
        self.nonce = secrets.token_bytes(32).hex()
        try:
            self.nonce_file.unlink(missing_ok=True)
        finally:
            self._closed = True
        return clean


def _default_data_root() -> Path:
    return Path.home() / ".otclient" / "tibia-re-control-center"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="TIBIA RE Control Center Package B loopback backend")
    parser.add_argument("--data-dir", type=Path, default=_default_data_root())
    parser.add_argument("--port", type=int, default=0)
    args = parser.parse_args(argv)
    server = ControlApiServer(args.data_dir, port=args.port)
    print(f"CONTROL_API={server.origin}", flush=True)
    print(f"RUNTIME_FILE={server.runtime_file}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close(shutdown_listener=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
