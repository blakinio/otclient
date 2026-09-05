from __future__ import annotations

import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor

from tools.tibia_re_control_center.control_domain import ControlDomainService
from tools.tibia_re_control_center.native_login_lifecycle import (
    NativeLoginLifecycle,
    NativeLoginLifecycleError,
)


class _SyntheticLoginExecutor:
    def __init__(self) -> None:
        self.start_calls: list[str] = []
        self.stop_calls: list[str] = []
        self.stop_latch_observations: list[bool] = []
        self.stop_latched_probe = lambda: False

    def status(self) -> dict[str, object]:
        return {
            "state": "READY",
            "bound": True,
            "current": True,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_RUNTIME_READY",
        }

    def start(self, operation_id: str) -> dict[str, object]:
        self.start_calls.append(operation_id)
        return {
            "state": "STARTING",
            "bound": True,
            "current": True,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_START_ACCEPTED",
            "operation_id": operation_id,
        }

    def stop(self, operation_id: str) -> dict[str, object]:
        self.stop_calls.append(operation_id)
        self.stop_latch_observations.append(self.stop_latched_probe())
        return {
            "state": "STOPPED",
            "bound": True,
            "current": True,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_STOP_CONFIRMED",
            "operation_id": operation_id,
        }


class _FailingLoginExecutor(_SyntheticLoginExecutor):
    def __init__(self, *, physical_effect: bool) -> None:
        super().__init__()
        self.physical_effect = physical_effect

    def start(self, operation_id: str) -> dict[str, object]:
        self.start_calls.append(operation_id)
        raise NativeLoginLifecycleError(
            "NATIVE_LOGIN_SYNTHETIC_FAILURE",
            "synthetic native login failure",
            physical_effect=self.physical_effect,
        )


class _BlockingLoginExecutor(_SyntheticLoginExecutor):
    def __init__(self) -> None:
        super().__init__()
        self.start_entered = threading.Event()
        self.release_start = threading.Event()

    def start(self, operation_id: str) -> dict[str, object]:
        self.start_calls.append(operation_id)
        self.start_entered.set()
        if not self.release_start.wait(timeout=5):
            raise AssertionError("synthetic start release timed out")
        return {
            "state": "STARTING",
            "bound": True,
            "current": True,
            "physical_effect": False,
            "reason": "NATIVE_LOGIN_START_ACCEPTED",
            "operation_id": operation_id,
        }


class NativeLoginControlTests(unittest.TestCase):
    @staticmethod
    def _post(domain: ControlDomainService, *, path: str, operation: str, request_id: str, handler):
        return domain.process_post(
            canonical_path=path,
            operation=operation,
            request_id=request_id,
            body={},
            handler=handler,
        )

    @classmethod
    def _start(cls, domain: ControlDomainService, request_id: str):
        return cls._post(
            domain,
            path="/v1/native-login/start",
            operation="NATIVE_LOGIN_START",
            request_id=request_id,
            handler=domain.native_login_start,
        )

    @classmethod
    def _stop(cls, domain: ControlDomainService, request_id: str):
        return cls._post(
            domain,
            path="/v1/stop-all",
            operation="STOP_ALL",
            request_id=request_id,
            handler=domain.stop_all,
        )

    @classmethod
    def _reset(cls, domain: ControlDomainService, request_id: str):
        return cls._post(
            domain,
            path="/v1/reset-stop",
            operation="RESET_STOP",
            request_id=request_id,
            handler=domain.reset_stop,
        )

    def test_native_login_start_uses_durable_resource_identity_and_replays_once(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            lifecycle = NativeLoginLifecycle(executor=executor)
            domain = ControlDomainService(root, native_login_lifecycle=lifecycle)
            try:
                first = self._start(domain, "native-login-request-1")
                second = self._start(domain, "native-login-request-1")
                self.assertEqual(202, first.code)
                self.assertEqual(first.body, second.body)
                operation_id = first.body["operation_id"]
                self.assertTrue(operation_id.startswith("native-login-"))
                self.assertEqual(executor.start_calls, [operation_id])
                self.assertEqual("STARTING", first.body["state"])
                self.assertFalse(first.body["physical_effect"])
            finally:
                domain.close()

    def test_distinct_second_start_is_rejected_before_executor(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            try:
                first = self._start(domain, "native-login-singleton-first")
                second = self._start(domain, "native-login-singleton-second")
                self.assertEqual(202, first.code)
                self.assertEqual(409, second.code)
                self.assertEqual("NATIVE_LOGIN_ALREADY_ACTIVE", second.body["code"])
                self.assertEqual([first.body["operation_id"]], executor.start_calls)
            finally:
                domain.close()

    def test_active_native_login_claim_survives_control_center_restart(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            first_executor = _SyntheticLoginExecutor()
            first_domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=first_executor),
            )
            first = self._start(first_domain, "native-login-before-restart")
            self.assertEqual(202, first.code)
            self.assertEqual([first.body["operation_id"]], first_executor.start_calls)
            self.assertTrue(first_domain.close())

            second_executor = _SyntheticLoginExecutor()
            second_domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=second_executor),
            )
            try:
                rejected = self._start(second_domain, "native-login-after-restart")
                self.assertEqual(409, rejected.code)
                self.assertEqual("NATIVE_LOGIN_ALREADY_ACTIVE", rejected.body["code"])
                self.assertEqual([], second_executor.start_calls)
            finally:
                second_domain.close()

    def test_concurrent_distinct_starts_claim_exactly_one_native_session(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            barrier = threading.Barrier(3)

            def invoke(request_id: str):
                barrier.wait(timeout=5)
                return self._start(domain, request_id)

            try:
                with ThreadPoolExecutor(max_workers=2) as pool:
                    first_future = pool.submit(invoke, "native-login-concurrent-a")
                    second_future = pool.submit(invoke, "native-login-concurrent-b")
                    barrier.wait(timeout=5)
                    replies = [first_future.result(timeout=5), second_future.result(timeout=5)]
                self.assertEqual([202, 409], sorted(reply.code for reply in replies))
                rejected = next(reply for reply in replies if reply.code == 409)
                accepted = next(reply for reply in replies if reply.code == 202)
                self.assertEqual("NATIVE_LOGIN_ALREADY_ACTIVE", rejected.body["code"])
                self.assertEqual([accepted.body["operation_id"]], executor.start_calls)
            finally:
                domain.close()

    def test_stop_is_durable_before_native_cancel_and_replay_does_not_cancel_twice(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            executor.stop_latched_probe = lambda: domain.coordinator.control_state.stop_latched
            try:
                started = self._start(domain, "native-login-before-stop")
                self.assertEqual(202, started.code)

                first = self._stop(domain, "native-login-stop-1")
                replay = self._stop(domain, "native-login-stop-1")
                self.assertEqual(200, first.code)
                self.assertEqual(first.body, replay.body)
                self.assertTrue(first.body["stop_latched"])
                self.assertEqual([first.body["resource_id"]], executor.stop_calls)
                self.assertEqual([True], executor.stop_latch_observations)
            finally:
                domain.close()

    def test_native_login_start_after_stop_fails_before_executor(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            try:
                stopped = self._stop(domain, "stop-before-native-login")
                self.assertEqual(200, stopped.code)
                self.assertTrue(domain.coordinator.control_state.stop_latched)

                rejected = self._start(domain, "native-login-after-stop")
                self.assertEqual(409, rejected.code)
                self.assertEqual("NATIVE_LOGIN_STOP_LATCHED", rejected.body["code"])
                self.assertEqual([], executor.start_calls)
            finally:
                domain.close()

    def test_pre_effect_failure_releases_claim_for_a_fresh_start(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            failing = _FailingLoginExecutor(physical_effect=False)
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=failing),
            )
            try:
                failed = self._start(domain, "native-login-preeffect-failure")
                self.assertEqual(409, failed.code)
                self.assertEqual("NATIVE_LOGIN_SYNTHETIC_FAILURE", failed.body["code"])

                succeeding = _SyntheticLoginExecutor()
                domain.native_login_lifecycle = NativeLoginLifecycle(executor=succeeding)
                retried = self._start(domain, "native-login-after-preeffect-failure")
                self.assertEqual(202, retried.code)
                self.assertEqual([retried.body["operation_id"]], succeeding.start_calls)
            finally:
                domain.close()

    def test_physical_effect_failure_retains_claim_across_restart(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            failing = _FailingLoginExecutor(physical_effect=True)
            first_domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=failing),
            )
            failed = self._start(first_domain, "native-login-physical-failure")
            self.assertEqual(409, failed.code)
            self.assertEqual("NATIVE_LOGIN_SYNTHETIC_FAILURE", failed.body["code"])
            self.assertTrue(first_domain.close())

            succeeding = _SyntheticLoginExecutor()
            second_domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=succeeding),
            )
            try:
                rejected = self._start(second_domain, "native-login-after-physical-failure")
                self.assertEqual(409, rejected.code)
                self.assertEqual("NATIVE_LOGIN_ALREADY_ACTIVE", rejected.body["code"])
                self.assertEqual([], succeeding.start_calls)
            finally:
                second_domain.close()

    def test_stop_reset_releases_claim_and_allows_one_fresh_start(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _SyntheticLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            try:
                first = self._start(domain, "native-login-before-stop-reset")
                self.assertEqual(202, first.code)
                stopped = self._stop(domain, "native-login-stop-reset-stop")
                self.assertEqual(200, stopped.code)
                self.assertTrue(stopped.body["stop_latched"])
                reset = self._reset(domain, "native-login-stop-reset-reset")
                self.assertEqual(200, reset.code)
                self.assertFalse(reset.body["stop_latched"])
                second = self._start(domain, "native-login-after-stop-reset")
                self.assertEqual(202, second.code)
                self.assertEqual(2, len(executor.start_calls))
                self.assertEqual(second.body["operation_id"], executor.start_calls[-1])
            finally:
                domain.close()

    def test_inflight_start_and_stop_are_linearized_by_stop_operation_lock(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            executor = _BlockingLoginExecutor()
            domain = ControlDomainService(
                root,
                native_login_lifecycle=NativeLoginLifecycle(executor=executor),
            )
            executor.stop_latched_probe = lambda: domain.coordinator.control_state.stop_latched
            start_reply: list[object] = []
            stop_reply: list[object] = []

            def invoke_start() -> None:
                start_reply.append(self._start(domain, "native-login-race-start"))

            def invoke_stop() -> None:
                stop_reply.append(self._stop(domain, "native-login-race-stop"))

            try:
                start_thread = threading.Thread(target=invoke_start)
                start_thread.start()
                self.assertTrue(executor.start_entered.wait(timeout=5))

                stop_thread = threading.Thread(target=invoke_stop)
                stop_thread.start()
                self.assertFalse(domain.coordinator.control_state.stop_latched)

                executor.release_start.set()
                start_thread.join(timeout=5)
                stop_thread.join(timeout=5)
                self.assertFalse(start_thread.is_alive())
                self.assertFalse(stop_thread.is_alive())
                self.assertEqual(202, start_reply[0].code)
                self.assertEqual(200, stop_reply[0].code)
                self.assertTrue(domain.coordinator.control_state.stop_latched)
                self.assertEqual([True], executor.stop_latch_observations)
                self.assertEqual([stop_reply[0].body["resource_id"]], executor.stop_calls)
            finally:
                executor.release_start.set()
                domain.close()


if __name__ == "__main__":
    unittest.main()
