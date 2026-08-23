from __future__ import annotations

import http.client
import json
import subprocess
import tempfile
from pathlib import Path

from tools.tibia_re_control_center.control_api import ControlApiServer
from tools.tibia_re_control_center.control_cli import (
    ControlApiClient,
    ControlClientError,
)

ROOT = Path(__file__).resolve().parents[3]
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


def raw(server: ControlApiServer, path: str, *, host: str | None = None, nonce: str | None = None, origin: str | None = None) -> tuple[int, dict]:
    connection = http.client.HTTPConnection("127.0.0.1", server.port, timeout=5)
    headers = {"Host": host or server.authority}
    if nonce is not None:
        headers["X-Tibia-RE-Control-Nonce"] = nonce
    if origin is not None:
        headers["Origin"] = origin
    connection.request("GET", path, headers=headers)
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
            if raw(first, "/v1/status")[0] != 401:
                raise SystemExit("missing nonce was admitted")
            if raw(first, "/v1/status", nonce=nonce, host="evil.invalid")[0] != 421:
                raise SystemExit("bad Host was admitted")
            if raw(first, "/v1/status", nonce=nonce, origin="https://evil.invalid")[0] != 403:
                raise SystemExit("cross-origin browser request was admitted")
            scenario = client.get("/v1/scenarios")["items"][0]["scenario"]
            first.domain.inject_test_crash_once("after_domain")
            try:
                client.post("/v1/experiments/one-step", {"scenario": scenario}, request_id="audit-lost-response")
            except ControlClientError as exc:
                if exc.status != 503:
                    raise
            else:
                raise SystemExit("crash injection unexpectedly returned success")
            if len(first.domain.adapter.physical_effects) != 1:
                raise SystemExit("crash-window effect cardinality contradiction")
            replay = client.post("/v1/experiments/one-step", {"scenario": scenario}, request_id="audit-lost-response")
            if len(first.domain.adapter.physical_effects) != 1:
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
            for path in first.domain.store.control_dir.glob("control-center.sqlite3*"):
                if nonce.encode("ascii") in path.read_bytes():
                    raise SystemExit("nonce leaked to persistent database")
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
            stale_status, _ = raw(second, "/v1/status", nonce=nonce)
            if stale_status != 401:
                raise SystemExit("stale nonce survived backend restart")
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