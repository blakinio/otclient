from __future__ import annotations

import http.client
import json
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tools.tibia_re_control_center.control_api import ControlApiServer
from tools.tibia_re_control_center.control_cli import (
    ControlApiClient,
    ControlClientError,
)
from tools.tibia_re_control_center.model import AdapterKind
from tools.tibia_re_control_center.persistent_store import (
    RequestLedgerRecord,
    SQLitePersistentStore,
)
from tools.tibia_re_control_center.scenario import validate_scenario


def http_call(
    server: ControlApiServer,
    method: str,
    path: str,
    *,
    body: object | bytes | str | None = None,
    nonce: str | None | object = ...,
    host: str | None = None,
    origin: str | None = None,
    headers: dict[str, str] | None = None,
    request_id: str | None = None,
) -> tuple[int, dict[str, str], bytes]:
    connection = http.client.HTTPConnection(server.host, server.port, timeout=5)
    request_headers = dict(headers or {})
    request_headers["Host"] = host or server.authority
    if nonce is ...:
        request_headers["X-Tibia-RE-Control-Nonce"] = server.nonce
    elif nonce is not None:
        request_headers["X-Tibia-RE-Control-Nonce"] = str(nonce)
    if origin is not None:
        request_headers["Origin"] = origin
    if request_id is not None:
        request_headers["X-Tibia-RE-Request-Id"] = request_id
    payload: bytes | None
    if isinstance(body, bytes):
        payload = body
        request_headers.setdefault("Content-Type", "application/json")
    elif isinstance(body, str):
        payload = body.encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    elif body is not None:
        payload = json.dumps(body, separators=(",", ":")).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")
    else:
        payload = None
    connection.request(method, path, body=payload, headers=request_headers)
    response = connection.getresponse()
    raw = response.read()
    result_headers = {key.lower(): value for key, value in response.getheaders()}
    status = response.status
    connection.close()
    return status, result_headers, raw


def decode(raw: bytes) -> dict:
    return json.loads(raw.decode("utf-8"))


class PackageBTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.server = ControlApiServer(self.root).start()
        self.client = ControlApiClient(self.root)

    def tearDown(self) -> None:
        if self.server is not None:
            self.server.close()
        self.temp.cleanup()

    def scenario(self) -> dict:
        return self.client.get("/v1/scenarios")["items"][0]["scenario"]

    def experiment(self, request_id: str = "test-exp", scenario: dict | None = None) -> dict:
        return self.client.post(
            "/v1/experiments/one-step",
            {"scenario": scenario or self.scenario()},
            request_id=request_id,
        )

    def restart(self, *, clean: bool = True) -> None:
        old = self.server
        if clean:
            old.close()
        else:
            old._httpd.shutdown()
            if old._thread is not None:
                old._thread.join(timeout=5)
            old._httpd.server_close()
            old.domain.store.close()
            old.nonce_file.unlink(missing_ok=True)
            old._closed = True
        self.server = ControlApiServer(self.root).start()
        self.client = ControlApiClient(self.root)

    def test_01_exact_ipv4_loopback_bind_only(self):
        self.assertEqual("127.0.0.1", self.server.host)
        for host in ("0.0.0.0", "::1", "localhost"):
            with self.subTest(host=host), self.assertRaises(ValueError):
                ControlApiServer(self.root / host.replace(":", "_"), host=host)

    def test_02_nonce_is_fresh_256_bit_private_file_material(self):
        first = self.server.nonce
        self.assertEqual(64, len(first))
        int(first, 16)
        self.assertEqual(first, self.server.nonce_file.read_text(encoding="utf-8").strip())
        self.restart(clean=True)
        self.assertNotEqual(first, self.server.nonce)

    def test_03_every_v1_route_requires_nonce_before_routing(self):
        for path in ("/v1/status", "/v1/capabilities", "/v1/scenarios", "/v1/runs", "/v1/events", "/v1/not-real"):
            status, _, raw = http_call(self.server, "GET", path, nonce=None)
            self.assertEqual(401, status, path)
            self.assertEqual("CONTROL_AUTH_REQUIRED", decode(raw)["code"])

    def test_04_stale_nonce_rejected_after_restart(self):
        stale = self.server.nonce
        self.restart(clean=True)
        status, _, raw = http_call(self.server, "GET", "/v1/status", nonce=stale)
        self.assertEqual(401, status)
        self.assertEqual("CONTROL_AUTH_REQUIRED", decode(raw)["code"])

    def test_05_nonce_not_in_runtime_metadata_or_persistent_database(self):
        nonce = self.server.nonce
        self.experiment("nonce-scan")
        runtime = self.server.runtime_file.read_text(encoding="utf-8")
        self.assertNotIn(nonce, runtime)
        self.server.domain.store.flush_safety_state()
        for path in self.server.domain.store.control_dir.glob("control-center.sqlite3*"):
            self.assertNotIn(nonce.encode("ascii"), path.read_bytes())

    def test_06_host_allowlist_rejects_unknown_authority(self):
        status, _, raw = http_call(self.server, "GET", "/v1/status", host="evil.invalid")
        self.assertEqual(421, status)
        self.assertEqual("CONTROL_HOST_REJECTED", decode(raw)["code"])

    def test_07_origin_is_exact_same_origin_when_present(self):
        good, _, _ = http_call(self.server, "GET", "/v1/status", origin=self.server.origin)
        bad, _, raw = http_call(self.server, "GET", "/v1/status", origin="https://evil.invalid")
        null, _, _ = http_call(self.server, "GET", "/v1/status", origin="null")
        self.assertEqual(200, good)
        self.assertEqual(403, bad)
        self.assertEqual("CONTROL_ORIGIN_REJECTED", decode(raw)["code"])
        self.assertEqual(403, null)

    def test_08_no_cors_or_cookie_ambient_authentication_headers(self):
        status, headers, _ = http_call(self.server, "GET", "/v1/status")
        self.assertEqual(200, status)
        self.assertNotIn("access-control-allow-origin", headers)
        self.assertNotIn("set-cookie", headers)
        self.assertEqual("no-store", headers.get("cache-control"))

    def test_09_cli_can_omit_origin_but_still_uses_nonce(self):
        self.assertEqual("NONE", self.client.get("/v1/status")["official_client_access"])
        bad = ControlApiClient(self.root)
        bad.nonce = "0" * 64
        with self.assertRaises(ControlClientError) as ctx:
            bad.get("/v1/status")
        self.assertEqual(401, ctx.exception.status)

    def test_10_oversized_body_is_rejected_before_json_parse(self):
        raw = b"{" + b" " * 262_144 + b"}"
        status, _, body = http_call(self.server, "POST", "/v1/stop-all", body=raw, request_id="big-body")
        self.assertEqual(413, status)
        self.assertEqual("CONTROL_BODY_TOO_LARGE", decode(body)["code"])

    def test_11_oversized_headers_are_rejected(self):
        status, _, raw = http_call(self.server, "GET", "/v1/status", headers={"X-Padding": "x" * 33_000})
        self.assertEqual(431, status)
        self.assertEqual("CONTROL_HEADERS_TOO_LARGE", decode(raw)["code"])

    def test_12_duplicate_json_keys_are_rejected(self):
        status, _, raw = http_call(self.server, "POST", "/v1/stop-all", body='{"x":1,"x":2}', request_id="dupe-json")
        self.assertEqual(400, status)
        self.assertEqual("CONTROL_BODY_DUPLICATE_KEY", decode(raw)["code"])

    def test_13_same_request_id_same_body_returns_same_resource_once(self):
        first = self.experiment("idem-same")
        second = self.experiment("idem-same")
        self.assertEqual(first, second)
        self.assertEqual(1, len(self.server.domain.adapter.physical_effects))
        record = self.server.domain.store.load_request("idem-same")
        self.assertEqual("COMPLETED", record.status)
        self.assertEqual(first["resource_id"], record.resource_id)

    def test_14_same_request_id_different_normalized_body_conflicts(self):
        first_scenario = self.scenario()
        self.experiment("idem-conflict", first_scenario)
        changed = json.loads(json.dumps(first_scenario))
        changed["name"] = "different semantic request"
        with self.assertRaises(ControlClientError) as ctx:
            self.experiment("idem-conflict", changed)
        self.assertEqual(409, ctx.exception.status)
        self.assertEqual("CONTROL_IDEMPOTENCY_CONFLICT", ctx.exception.payload["code"])
        self.assertEqual(1, len(self.server.domain.adapter.physical_effects))

    def test_15_failed_logical_request_replays_same_failure(self):
        with self.assertRaises(ControlClientError) as first:
            self.client.post("/v1/runs/not-active/pause", {}, request_id="failed-replay")
        with self.assertRaises(ControlClientError) as second:
            self.client.post("/v1/runs/not-active/pause", {}, request_id="failed-replay")
        self.assertEqual(first.exception.status, second.exception.status)
        self.assertEqual(first.exception.payload, second.exception.payload)
        self.assertEqual("FAILED", self.server.domain.store.load_request("failed-replay").status)

    def test_16_crash_after_accepted_before_domain_reuses_reserved_resource(self):
        self.server.domain.inject_test_crash_once("after_accept")
        with self.assertRaises(ControlClientError) as interrupted:
            self.experiment("crash-after-accept")
        self.assertEqual(503, interrupted.exception.status)
        accepted = self.server.domain.store.load_request("crash-after-accept")
        self.assertEqual("ACCEPTED", accepted.status)
        result = self.experiment("crash-after-accept")
        self.assertEqual(accepted.resource_id, result["resource_id"])
        self.assertEqual(1, len(self.server.domain.adapter.physical_effects))

    def test_17_completed_domain_lost_response_replays_without_second_effect(self):
        self.server.domain.inject_test_crash_once("after_domain")
        with self.assertRaises(ControlClientError) as interrupted:
            self.experiment("crash-after-domain")
        self.assertEqual(503, interrupted.exception.status)
        accepted = self.server.domain.store.load_request("crash-after-domain")
        self.assertEqual("ACCEPTED", accepted.status)
        self.assertEqual(1, len(self.server.domain.adapter.physical_effects))
        result = self.experiment("crash-after-domain")
        self.assertEqual(accepted.resource_id, result["resource_id"])
        self.assertEqual(1, len(self.server.domain.adapter.physical_effects))

    def test_18_completed_request_replays_across_clean_backend_restart(self):
        result = self.experiment("restart-replay")
        resource_id = result["resource_id"]
        self.restart(clean=True)
        replay = self.experiment("restart-replay")
        self.assertEqual(resource_id, replay["resource_id"])
        self.assertEqual(result, replay)
        self.assertEqual([], self.server.domain.adapter.physical_effects)

    def test_19_stop_and_reset_use_reserved_transition_identity(self):
        stop = self.client.post("/v1/stop-all", {}, request_id="stop-identity")
        stop_record = self.server.domain.store.load_request("stop-identity")
        self.assertEqual(stop_record.resource_id, stop["transition_id"])
        reset = self.client.post("/v1/reset-stop", {}, request_id="reset-identity")
        reset_record = self.server.domain.store.load_request("reset-identity")
        self.assertEqual(reset_record.resource_id, reset["transition_id"])
        self.assertGreater(reset["control_generation"], stop["control_generation"])

    def test_20_delayed_old_stop_replay_does_not_relatch_after_reset(self):
        old = self.client.post("/v1/stop-all", {}, request_id="old-stop")
        self.client.post("/v1/reset-stop", {}, request_id="new-reset")
        replay = self.client.post("/v1/stop-all", {}, request_id="old-stop")
        self.assertEqual(old, replay)
        self.assertFalse(self.client.get("/v1/status")["control"]["stop_latched"])

    def test_21_delayed_old_reset_replay_does_not_clear_newer_stop(self):
        self.client.post("/v1/stop-all", {}, request_id="stop-before-reset")
        old_reset = self.client.post("/v1/reset-stop", {}, request_id="old-reset")
        self.client.post("/v1/stop-all", {}, request_id="newer-stop")
        replay = self.client.post("/v1/reset-stop", {}, request_id="old-reset")
        self.assertEqual(old_reset, replay)
        self.assertTrue(self.client.get("/v1/status")["control"]["stop_latched"])

    def test_22_clean_shutdown_flushes_and_clears_active_backend_marker(self):
        nonce_path = self.server.nonce_file
        store_path = self.root
        self.assertTrue(self.server.close())
        self.server = None
        self.assertFalse(nonce_path.exists())
        store = SQLitePersistentStore(store_path)
        try:
            self.assertIsNone(store.load_control_state().active_backend_epoch)
            self.assertGreaterEqual(store.safety_flush_count, 0)
        finally:
            store.close()

    def test_23_failed_clean_shutdown_forces_recovery_required_on_next_backend(self):
        self.server.domain.store.inject_fault("safety_flush")
        self.assertFalse(self.server.close())
        self.server = ControlApiServer(self.root).start()
        self.client = ControlApiClient(self.root)
        status = self.client.get("/v1/status")
        self.assertTrue(status["control"]["recovery_required"])
        self.assertFalse(self.server.domain.coordinator.mutation_admission_allowed())

    def test_24_restart_preserves_run_activation_action_and_budget_truth(self):
        result = self.experiment("persist-run")
        run_id = result["run_id"]
        action_id = next(iter(result["actions"]))
        activation = self.server.domain.store.load_run_activation(run_id)
        budget = self.server.domain.store.load_budget(run_id)
        action = self.server.domain.store.load_action(action_id)
        self.restart(clean=True)
        self.assertEqual(activation, self.server.domain.store.load_run_activation(run_id))
        self.assertEqual(budget.deadline_monotonic_ns, self.server.domain.store.load_budget(run_id).deadline_monotonic_ns)
        self.assertEqual(action.lifecycle_state, self.server.domain.store.load_action(action_id).lifecycle_state)

    def test_25_incomplete_mutation_run_is_not_auto_resumed_after_unclean_restart(self):
        normalized = self.server.domain.normalize_post_body("ONE_STEP_EXPERIMENT", {"scenario": self.scenario()})
        request_id = "incomplete-restart"
        resource_id = "experiment-incomplete-restart"
        request_hash = self.server.domain._request_hash("/v1/experiments/one-step", normalized)
        self.server.domain.store.accept_request(RequestLedgerRecord(request_id, request_hash, self.server.domain.backend_epoch, "ONE_STEP_EXPERIMENT", resource_id, "ACCEPTED"))
        self.server.domain.store.ensure_resource(resource_id, request_id, "ONE_STEP_EXPERIMENT", normalized)
        scenario = validate_scenario(normalized["scenario"])
        self.server.domain.coordinator.start_run(resource_id, scenario.side_effect_budget, mutation_capable=True)
        self.restart(clean=False)
        with self.assertRaises(ControlClientError) as ctx:
            self.experiment(request_id)
        self.assertEqual(409, ctx.exception.status)
        self.assertEqual("CONTROL_RUN_RECOVERY_REQUIRED", ctx.exception.payload["code"])
        self.assertEqual([], self.server.domain.adapter.physical_effects)

    def test_26_bounded_event_polling_reports_backpressure_for_stale_cursor(self):
        events = [{"kind": "SYSTEM", "payload": {"index": index}} for index in range(4100)]
        self.server.domain.store.append_events("synthetic", events)
        with self.assertRaises(ControlClientError) as ctx:
            self.client.get("/v1/events?cursor=1&limit=10")
        self.assertEqual(409, ctx.exception.status)
        self.assertEqual("CONTROL_EVENT_BACKPRESSURE", ctx.exception.payload["code"])
        with self.assertRaises(ControlClientError):
            self.client.get("/v1/events?limit=1001")

    def test_27_raw_debug_and_unknown_mutation_routes_are_absent(self):
        for path in ("/v1/raw", "/v1/debug", "/v1/raw-actions", "/v1/debug-actions", "/v1/adapters/official"):
            status, _, raw = http_call(self.server, "GET", path)
            self.assertEqual(404, status, path)
            self.assertEqual("CONTROL_ROUTE_NOT_FOUND", decode(raw)["code"])
        status, _, raw = http_call(self.server, "DELETE", "/v1/status")
        self.assertEqual(405, status)
        self.assertEqual("CONTROL_METHOD_NOT_ALLOWED", decode(raw)["code"])
        status, _, raw = http_call(self.server, "DELETE", "/v1/not-real")
        self.assertEqual(404, status)
        self.assertEqual("CONTROL_ROUTE_NOT_FOUND", decode(raw)["code"])
        status, _, raw = http_call(self.server, "GET", "/v1/stop-all")
        self.assertEqual(405, status)
        self.assertEqual("CONTROL_METHOD_NOT_ALLOWED", decode(raw)["code"])
        status, _, raw = http_call(self.server, "POST", "/v1/status")
        self.assertEqual(405, status)
        self.assertEqual("CONTROL_METHOD_NOT_ALLOWED", decode(raw)["code"])
        status, _, raw = http_call(self.server, "OPTIONS", "/v1/not-real")
        self.assertEqual(404, status)
        self.assertEqual("CONTROL_ROUTE_NOT_FOUND", decode(raw)["code"])

    def test_28_browser_bootstrap_is_no_store_csp_self_contained_and_truthful(self):
        status, headers, raw = http_call(self.server, "GET", "/", nonce=None)
        page = raw.decode("utf-8")
        self.assertEqual(200, status)
        self.assertEqual("no-store", headers.get("cache-control"))
        self.assertIn("frame-ancestors 'none'", headers.get("content-security-policy", ""))
        for tab in ("Main", "Runtime", "Movement", "Healing", "Spells", "Consumables", "Combat", "Targeting", "Inventory", "Containers", "Equipment", "Chat", "Conditions", "Scenarios", "Recorder", "Network", "Experiments", "Compare", "Logger"):
            self.assertIn(f'>{tab}<', page)
        for truth in ("NONE", "UNSUPPORTED", "NOT_PROVEN", "UNKNOWN"):
            self.assertIn(truth, page)
        self.assertNotIn("localStorage", page)
        self.assertNotIn("sessionStorage", page)

    def test_29_browser_style_same_origin_request_and_cli_share_same_domain_state(self):
        status, _, raw = http_call(self.server, "GET", "/v1/status", origin=self.server.origin)
        browser_status = decode(raw)
        cli_status = self.client.get("/v1/status")
        self.assertEqual(200, status)
        self.assertEqual(browser_status, cli_status)
        self.assertEqual(browser_status["backend"]["epoch"], self.server.domain.backend_epoch)

    def test_30_mutation_capability_is_fake_only_and_not_locally_grantable(self):
        status = self.client.get("/v1/status")
        self.assertEqual(AdapterKind.FAKE_TEST.value, status["runtime"]["adapter_kind"])
        self.assertEqual("FAKE_TEST_ONLY", status["authority"]["scope"])
        self.assertFalse(status["authority"]["locally_grantable"])
        self.assertEqual("UNSUPPORTED", status["authority"]["official_mutation_authority"])
        self.assertEqual("NONE", status["official_client_access"])

    def test_31_corrupt_missing_request_ledger_cannot_silently_reexecute(self):
        self.experiment("ledger-corrupt")
        effects = len(self.server.domain.adapter.physical_effects)
        with self.server.domain.store._lock:
            self.server.domain.store._db.execute("DELETE FROM requests WHERE request_id=?", ("ledger-corrupt",))
        with self.assertRaises(ControlClientError) as ctx:
            self.experiment("ledger-corrupt")
        self.assertEqual(409, ctx.exception.status)
        self.assertEqual("REQUEST_LEDGER_CONTRADICTION", ctx.exception.payload["code"])
        self.assertEqual(effects, len(self.server.domain.adapter.physical_effects))

    def test_32_run_action_event_artifact_views_are_persistent_and_bounded(self):
        result = self.experiment("views")
        run_id = result["run_id"]
        action_id = next(iter(result["actions"]))
        run = self.client.get(f"/v1/runs/{run_id}")
        action = self.client.get(f"/v1/actions/{action_id}")
        events = self.client.get("/v1/events?limit=100")
        self.assertTrue(run["artifacts"])
        self.assertEqual(run_id, action["run_id"])
        self.assertTrue(events["items"])
        self.assertEqual("BOUNDED_POLLING", events["delivery"])

    def test_33_nonce_is_not_admitted_to_control_api_url(self):
        for path in (
            f"/v1/status?control_nonce={self.server.nonce}",
            f"/v1/status?opaque={self.server.nonce}",
        ):
            with self.subTest(path=path.split("=", 1)[0]):
                status, _, raw = http_call(self.server, "GET", path)
                self.assertEqual(400, status)
                self.assertEqual("CONTROL_NONCE_IN_URL", decode(raw)["code"])

    def test_34_package_b_domain_has_no_official_adapter_or_runtime_bridge(self):
        source = (Path("tools/tibia_re_control_center/control_domain.py").read_text(encoding="utf-8") + Path("tools/tibia_re_control_center/control_api.py").read_text(encoding="utf-8"))
        self.assertNotIn("tibia_runtime_bridge", source)
        self.assertNotIn("surveyor_provider", source)
        self.assertNotIn("OFFICIAL_TIBIA", source)

    def test_35_concurrent_duplicate_posts_share_one_result_and_effect(self):
        scenario = self.scenario()
        barrier = threading.Barrier(12)

        def worker() -> dict:
            barrier.wait(timeout=5)
            return self.client.post(
                "/v1/experiments/one-step",
                {"scenario": scenario},
                request_id="concurrent-same",
            )

        with ThreadPoolExecutor(max_workers=12) as pool:
            results = [future.result(timeout=10) for future in [pool.submit(worker) for _ in range(12)]]
        self.assertTrue(all(result == results[0] for result in results))
        self.assertEqual(1, len(self.server.domain.adapter.physical_effects))
        self.assertEqual(results[0]["resource_id"], self.server.domain.store.load_request("concurrent-same").resource_id)

    def test_36_concurrent_conflicting_request_id_executes_exactly_one_body(self):
        first = self.scenario()
        second = json.loads(json.dumps(first))
        second["name"] = "concurrent conflicting scenario"
        barrier = threading.Barrier(2)

        def worker(scenario: dict) -> tuple[str, int | str]:
            barrier.wait(timeout=5)
            try:
                result = self.client.post(
                    "/v1/experiments/one-step",
                    {"scenario": scenario},
                    request_id="concurrent-conflict",
                )
                return "ok", result["resource_id"]
            except ControlClientError as exc:
                return "error", exc.status

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = [future.result(timeout=10) for future in (pool.submit(worker, first), pool.submit(worker, second))]
        self.assertEqual(["error", "ok"], sorted(kind for kind, _ in outcomes))
        self.assertIn(("error", 409), outcomes)
        self.assertEqual(1, len(self.server.domain.adapter.physical_effects))

    def test_37_stop_racing_precommit_mutation_prevents_fake_effect(self):
        entered = threading.Event()
        release = threading.Event()

        def block_before_commit() -> None:
            entered.set()
            if not release.wait(timeout=5):
                raise RuntimeError("test gate timed out")

        self.server.domain.adapter.before_commit_hook = block_before_commit
        with ThreadPoolExecutor(max_workers=2) as pool:
            mutation = pool.submit(self.experiment, "stop-race-mutation")
            self.assertTrue(entered.wait(timeout=5))
            stop = pool.submit(self.client.post, "/v1/stop-all", {}, request_id="stop-race-control")
            stop_result = stop.result(timeout=5)
            release.set()
            mutation_result = mutation.result(timeout=5)
        self.server.domain.adapter.before_commit_hook = None
        self.assertTrue(stop_result["stop_latched"])
        self.assertEqual([], self.server.domain.adapter.physical_effects)
        self.assertTrue(all(action["dispatch_state"] == "NOT_DISPATCHED" for action in mutation_result["actions"].values()))

    def test_38_concurrent_stop_reset_linearizes_to_highest_generation(self):
        for iteration in range(64):
            barrier = threading.Barrier(2)

            def transition(
                path: str, request_id: str, sync_barrier: threading.Barrier = barrier
            ) -> tuple[str, dict]:
                sync_barrier.wait(timeout=5)
                try:
                    return "ok", self.client.post(path, {}, request_id=request_id)
                except ControlClientError as exc:
                    return "error", {"status": exc.status, "code": exc.payload.get("code")}

            with ThreadPoolExecutor(max_workers=2) as pool:
                outcomes = [
                    future.result(timeout=10)
                    for future in (
                        pool.submit(transition, "/v1/stop-all", f"concurrent-stop-{iteration}"),
                        pool.submit(transition, "/v1/reset-stop", f"concurrent-reset-{iteration}"),
                    )
                ]
            successful = [payload for kind, payload in outcomes if kind == "ok"]
            self.assertTrue(successful)
            highest = max(successful, key=lambda payload: payload["control_generation"])
            current = self.client.get("/v1/status")["control"]
            self.assertEqual(highest["control_generation"], current["control_generation"])
            self.assertEqual(highest["stop_latched"], current["stop_latched"])
            for kind, payload in outcomes:
                if kind == "error":
                    self.assertEqual({"status": 409, "code": "CONTROL_RESET_REFUSED"}, payload)
            if current["stop_latched"]:
                cleanup = self.client.post(
                    "/v1/reset-stop", {}, request_id=f"concurrent-cleanup-{iteration}"
                )
                self.assertFalse(cleanup["stop_latched"])

    def test_39_runtime_monotonic_clock_survives_backend_object_restart(self):
        first = self.server.domain.clock.now_ns()
        time.sleep(0.05)
        second = self.server.domain.clock.now_ns()
        self.assertGreater(second, first)
        self.restart(clean=True)
        third = self.server.domain.clock.now_ns()
        self.assertGreaterEqual(third, second)



if __name__ == "__main__":
    unittest.main()