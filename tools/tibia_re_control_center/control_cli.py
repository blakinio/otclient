from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .canonical import jcs_dumps


class ControlClientError(Exception):
    def __init__(self, status: int, payload: dict[str, Any]):
        super().__init__(str(payload.get("safe_message", "Control API request failed")))
        self.status = status
        self.payload = payload


def _default_data_root() -> Path:
    return Path.home() / ".otclient" / "tibia-re-control-center"


class ControlApiClient:
    """Thin HTTP-only Package B client. It has no adapter or coordinator imports."""

    def __init__(self, data_root: str | Path, *, timeout: float = 5.0) -> None:
        self.data_root = Path(data_root).expanduser().resolve()
        runtime_path = self.data_root / "control" / "control-runtime.json"
        nonce_path = self.data_root / "control" / "control.nonce"
        try:
            runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
            nonce = nonce_path.read_text(encoding="utf-8").strip()
        except (OSError, json.JSONDecodeError) as exc:
            raise ControlClientError(0, {"code": "CONTROL_RUNTIME_UNAVAILABLE", "safe_message": "Control API runtime metadata is unavailable"}) from exc
        if set(runtime) != {"schema_version", "host", "port", "origin", "backend_epoch", "nonce_transport", "official_client_access"}:
            raise ControlClientError(0, {"code": "CONTROL_RUNTIME_INVALID", "safe_message": "Control API runtime metadata is invalid"})
        port = runtime.get("port")
        expected_origin = f"http://127.0.0.1:{port}" if isinstance(port, int) and not isinstance(port, bool) else None
        if (
            runtime.get("schema_version") != 1
            or runtime.get("host") != "127.0.0.1"
            or runtime.get("origin") != expected_origin
            or runtime.get("nonce_transport") != "PRIVATE_FILE"
            or runtime.get("official_client_access") != "NONE"
        ):
            raise ControlClientError(0, {"code": "CONTROL_RUNTIME_INVALID", "safe_message": "Control API runtime metadata is outside the admitted contract"})
        if not isinstance(nonce, str) or len(nonce) != 64:
            raise ControlClientError(0, {"code": "CONTROL_NONCE_UNAVAILABLE", "safe_message": "Control API nonce file is invalid"})
        self.origin = str(runtime["origin"])
        self.nonce = nonce
        self.timeout = timeout

    def _request(self, path: str, *, method: str = "GET", body: dict[str, Any] | None = None, request_id: str | None = None) -> dict[str, Any]:
        if not path.startswith("/v1/"):
            raise ValueError("ControlApiClient accepts only /v1/ API paths")
        headers = {"X-Tibia-RE-Control-Nonce": self.nonce, "Accept": "application/json"}
        raw: bytes | None = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            raw = jcs_dumps(body).encode("utf-8")
        if request_id is not None:
            headers["X-Tibia-RE-Request-Id"] = request_id
        request = Request(self.origin + path, data=raw, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            try:
                payload = json.loads(exc.read().decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                payload = {"code": "CONTROL_INVALID_ERROR", "safe_message": "Control API returned an invalid error envelope"}
            raise ControlClientError(exc.code, payload) from exc
        except URLError as exc:
            raise ControlClientError(0, {"code": "CONTROL_CONNECT_FAILED", "safe_message": "Control API connection failed"}) from exc

    def get(self, path: str) -> dict[str, Any]:
        return self._request(path)

    def post(self, path: str, body: dict[str, Any], *, request_id: str) -> dict[str, Any]:
        return self._request(path, method="POST", body=body, request_id=request_id)


def _read_scenario(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ControlClientError(0, {"code": "CONTROL_SCENARIO_FILE_INVALID", "safe_message": "scenario file is unavailable or invalid JSON"}) from exc
    if not isinstance(value, dict):
        raise ControlClientError(0, {"code": "CONTROL_SCENARIO_FILE_INVALID", "safe_message": "scenario file must contain a JSON object"})
    return value


def _post_parser(subparsers: Any, name: str, help_text: str) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(name, help=help_text)
    parser.add_argument("--request-id", required=True)
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Thin CLI for TIBIA RE Control Center Package B")
    parser.add_argument("--data-dir", type=Path, default=_default_data_root())
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("capabilities")
    sub.add_parser("scenarios")
    runs = sub.add_parser("runs")
    runs.add_argument("--limit", type=int, default=100)
    detail = sub.add_parser("run")
    detail.add_argument("run_id")
    action = sub.add_parser("action")
    action.add_argument("action_id")
    events = sub.add_parser("events")
    events.add_argument("--limit", type=int, default=100)
    events.add_argument("--cursor", type=int, default=0)
    create = _post_parser(sub, "create-run", "validate and execute a fake-backed Scenario v1 run")
    create.add_argument("--scenario", type=Path, required=True)
    experiment = _post_parser(sub, "experiment", "execute one fake one-step experiment")
    experiment.add_argument("--scenario", type=Path)
    _post_parser(sub, "stop-all", "latch STOP")
    _post_parser(sub, "reset-stop", "reset STOP when safety state permits")
    for name in ("pause", "resume", "abort"):
        item = _post_parser(sub, name, f"{name} an active run")
        item.add_argument("run_id")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        client = ControlApiClient(args.data_dir)
        command = args.command
        if command == "status":
            result = client.get("/v1/status")
        elif command == "capabilities":
            result = client.get("/v1/capabilities")
        elif command == "scenarios":
            result = client.get("/v1/scenarios")
        elif command == "runs":
            result = client.get(f"/v1/runs?limit={args.limit}")
        elif command == "run":
            result = client.get(f"/v1/runs/{args.run_id}")
        elif command == "action":
            result = client.get(f"/v1/actions/{args.action_id}")
        elif command == "events":
            result = client.get(f"/v1/events?limit={args.limit}&cursor={args.cursor}")
        elif command == "create-run":
            result = client.post("/v1/runs", {"scenario": _read_scenario(args.scenario)}, request_id=args.request_id)
        elif command == "experiment":
            scenario = _read_scenario(args.scenario) if args.scenario else client.get("/v1/scenarios")["items"][0]["scenario"]
            result = client.post("/v1/experiments/one-step", {"scenario": scenario}, request_id=args.request_id)
        elif command == "stop-all":
            result = client.post("/v1/stop-all", {}, request_id=args.request_id)
        elif command == "reset-stop":
            result = client.post("/v1/reset-stop", {}, request_id=args.request_id)
        else:
            result = client.post(f"/v1/runs/{args.run_id}/{command}", {}, request_id=args.request_id)
        print(jcs_dumps(result))
        return 0
    except ControlClientError as exc:
        print(jcs_dumps(exc.payload))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())