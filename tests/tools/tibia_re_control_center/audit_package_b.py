from __future__ import annotations

import http.client
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.tibia_re_control_center.control_api import ControlApiServer
from tools.tibia_re_control_center.control_cli import (
    ControlApiClient,
    ControlClientError,
)

ALLOWED_EXACT = {
    ".github/workflows/tibia-re-control-center-package-b.yml",
    "tools/tibia_re_control_center/__init__.py",
    "tests/tools/tibia_re_control_center/test_package_a.py",
    "tools/tibia_re_control_center/persistent_store.py",
    "tools/tibia_re_control_center/control_domain.py",
    "tools/tibia_re_control_center/control_api.py",
    "tools/tibia_re_control_center/control_cli.py",
    "tools/tibia_re_control_center/control_ui.py",
    "tests/tools/tibia_re_control_center/test_package_b.py",
    "tests/tools/tibia_re_control_center/audit_package_b.py",
    "tests/tools/tibia_re_control_center/e2e_package_b.py",
}
ALLOWED_PREFIXES = (
    "docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-b.md",
    "docs/agents/tasks/archive/OTC-20260823-tibia-re-control-center-package-b.md",
    "docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-b/",
)


def changed_paths() -> list[str]:
    base = subprocess.check_output(["git", "merge-base", "origin/main", "HEAD"], cwd=ROOT, text=True).strip()
    return subprocess.check_output(["git", "diff", "--name-only", f"{base}...HEAD"], cwd=ROOT, text=True).splitlines()


def raw(
    server: ControlApiServer,
    path: str,
    *,
    method: str = "GET",
    host: str | None = None,
    nonce: str | None = None,
    origin: str | None = None,
) -> tuple[int, dict]:
    connection = http.client.HTTPConnection("127.0.0.1", server.port, timeout=5)
    headers = {"Host": host or server.authority}
    if nonce is not None:
        headers["X-Tibia-RE-Control-Nonce"] = nonce
    if origin is not None:
        headers["Origin"] = origin
    connection.request(method, path, headers=headers)
    response = connection.getresponse()
    body = json.loads(response.read().decode("utf-8"))
    status = response.status
    connection.close()
    return status, body


def main() -> int:
    unexpected = [path for path in changed_paths() if path not in ALLOWED_EXACT and not any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES)]
    if unexpected:
        raise SystemExit("Package B changed paths outside its declared ownership boundary")
    production = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in (
        "tools/tibia_re_control_center/control_domain.py",
        "tools/tibia_re_control_center/control_api.py",
        "tools/tibia_re_control_center/control_cli.py",
        "tools/tibia_re_control_center/control_ui.py",
        "tools/tibia_re_control_center/persistent_store.py",
    ))
    for forbidden in ("tibia_runtime_bridge", "surveyor_provider", "OfficialTibia", "official_adapter"):
        if forbidden in production:
            raise SystemExit("Package B production path acquired forbidden runtime/provider coupling")
    cli_source = (ROOT / "tools/tibia_re_control_center/control_cli.py").read_text(encoding="utf-8")
    if any(token in cli_source for token in ("FakeAdapter", "MutationCoordinator", "ScenarioEngine")):
        raise SystemExit("CLI bypasses the Control API domain path")
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        try:
            ControlApiServer(root / "bad", host="0.0.0.0")
        except ValueError:
            pass
        else:
            raise SystemExit("non-loopback bind was admitted")
        first = ControlApiServer(root).start()
        nonce = first.nonce
        try:
            client = ControlApiClient(root)
            status = client.get("/v1/status")
            if status["official_client_access"] != "NONE" or status["runtime"]["adapter_kind"] != "FAKE_TEST":
                raise SystemExit("truthfulness or fake-only boundary contradiction")
            missing_status, missing_body = raw(first, "/v1/status")
            if missing_status != 401 or missing_body.get("code") != "CONTROL_AUTH_REQUIRED":
                raise SystemExit("missing nonce did not produce contract-defined CONTROL_AUTH_REQUIRED")
            if raw(first, "/v1/status", nonce=nonce, host="evil.invalid")[0] != 421:
                raise SystemExit("bad Host was admitted")
            if raw(first, "/v1/status", nonce=nonce, origin="https://evil.invalid")[0] != 403:
                raise SystemExit("cross-origin browser request was admitted")
            nonce_url_status, nonce_url_body = raw(first, f"/v1/status?opaque={nonce}", nonce=nonce)
            if nonce_url_status != 400 or nonce_url_body.get("code") != "CONTROL_NONCE_IN_URL":
                raise SystemExit("literal control nonce was admitted in arbitrary URL data")
            unknown_status, unknown_body = raw(first, "/v1/not-real", nonce=nonce)
            if unknown_status != 404 or unknown_body.get("code") != "CONTROL_ROUTE_NOT_FOUND":
                raise SystemExit("unknown route did not produce contract-defined 404")
            wrong_method_status, wrong_method_body = raw(first, "/v1/status", method="DELETE", nonce=nonce)
            if wrong_method_status != 405 or wrong_method_body.get("code") != "CONTROL_METHOD_NOT_ALLOWED":
                raise SystemExit("known route accepted or misclassified an unsupported method")
            unknown_method_status, unknown_method_body = raw(first, "/v1/not-real", method="DELETE", nonce=nonce)
            if unknown_method_status != 404 or unknown_method_body.get("code") != "CONTROL_ROUTE_NOT_FOUND":
                raise SystemExit("unknown route was incorrectly classified as method-not-allowed")
            post_only_status, post_only_body = raw(first, "/v1/stop-all", nonce=nonce)
            if post_only_status != 405 or post_only_body.get("code") != "CONTROL_METHOD_NOT_ALLOWED":
                raise SystemExit("GET on a known POST-only route was not rejected as method-not-allowed")
            scenario = client.get("/v1/scenarios")["items"][0]["scenario"]
            conflict = json.loads(json.dumps(scenario))
            conflict["name"] = "audit idempotency conflict"
            client.post("/v1/experiments/one-step", {"scenario": scenario}, request_id="audit-idempotency")
            try:
                client.post("/v1/experiments/one-step", {"scenario": conflict}, request_id="audit-idempotency")
            except ControlClientError as exc:
                if exc.status != 409 or exc.payload.get("code") != "CONTROL_IDEMPOTENCY_CONFLICT":
                    raise SystemExit("idempotency conflict did not use the contract-defined error") from exc
            else:
                raise SystemExit("same request ID with a different normalized body was admitted")
            effects_before_lost_response = len(first.domain.adapter.physical_effects)
            first.domain.inject_test_crash_once("after_domain")
            try:
                client.post("/v1/experiments/one-step", {"scenario": scenario}, request_id="audit-lost-response")
            except ControlClientError as exc:
                if exc.status != 503:
                    raise
            else:
                raise SystemExit("crash injection unexpectedly returned success")
            if len(first.domain.adapter.physical_effects) != effects_before_lost_response + 1:
                raise SystemExit("crash-window effect cardinality contradiction")
            replay = client.post("/v1/experiments/one-step", {"scenario": scenario}, request_id="audit-lost-response")
            if len(first.domain.adapter.physical_effects) != effects_before_lost_response + 1:
                raise SystemExit("lost response replay duplicated a fake effect")
            stop = client.post("/v1/stop-all", {}, request_id="audit-old-stop")
            client.post("/v1/reset-stop", {}, request_id="audit-reset")
            if client.post("/v1/stop-all", {}, request_id="audit-old-stop") != stop:
                raise SystemExit("old STOP replay changed its durable result")
            if client.get("/v1/status")["control"]["stop_latched"]:
                raise SystemExit("old STOP replay relatched a newer reset state")
            first.domain.store.flush_safety_state()
            runtime_text = first.runtime_file.read_text(encoding="utf-8")
            if nonce in runtime_text:
                raise SystemExit("nonce leaked to runtime metadata")
            for path in root.rglob("*"):
                if path.is_file() and path != first.nonce_file and nonce.encode("ascii") in path.read_bytes():
                    raise SystemExit(f"nonce leaked outside the dedicated nonce file: {path.relative_to(root)}")
            resource_id = replay["resource_id"]
        finally:
            if not first.close():
                raise SystemExit("graceful shutdown audit failed")
        second = ControlApiServer(root).start()
        try:
            client = ControlApiClient(root)
            replay = client.post("/v1/experiments/one-step", {"scenario": scenario}, request_id="audit-lost-response")
            if replay["resource_id"] != resource_id or second.domain.adapter.physical_effects:
                raise SystemExit("restart replay duplicated or rebound the logical resource")
            stale_status, stale_body = raw(second, "/v1/status", nonce=nonce)
            if stale_status != 401 or stale_body.get("code") != "CONTROL_AUTH_REQUIRED":
                raise SystemExit("stale nonce did not produce contract-defined CONTROL_AUTH_REQUIRED")
        finally:
            if not second.close():
                raise SystemExit("second graceful shutdown audit failed")
    print("PACKAGE_B_AUDIT_BOUNDARY=PASS")
    print("PACKAGE_B_AUDIT_TRANSPORT=PASS")
    print("PACKAGE_B_AUDIT_IDEMPOTENCY=PASS")
    print("PACKAGE_B_AUDIT_RESTART=PASS")
    print("PACKAGE_B_AUDIT_PRIVACY=PASS")
    print("OFFICIAL_CLIENT_ACCESS=NONE")
    print("PACKAGE_B_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())