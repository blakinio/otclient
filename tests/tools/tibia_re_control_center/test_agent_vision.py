from contextlib import ExitStack
import hashlib
import inspect
import os
import stat
from functools import partial
from pathlib import Path
import tempfile
import threading
import traceback
import unittest
from unittest.mock import patch

from tools.tibia_re_control_center.agent_protocol import AgentVisualState
from tools.tibia_re_control_center.agent_vision import (
    AgentVisionSensor,
    ModelSlotScheduler,
    ModelSlotUnavailable,
    QWEN_NUM_CTX,
    QWEN_NUM_PREDICT,
    QWEN_TEMPERATURE,
    QWEN_VISION_DIGEST,
    QWEN_VISION_MODEL,
    QWEN_VISION_PROFILE_ID,
    SecretSafeCapture,
)
from tools.tibia_re_vision.evidence import UnsafeInputError
from tools.tibia_re_vision.ollama import run_ollama_trial


_REAL_FDOPEN = os.fdopen
_REAL_OS_CLOSE = os.close
_REAL_PATH_READ_BYTES = Path.read_bytes


def _visual_evidence(capture, *, screen_class="LOGIN_SCREEN"):
    return {
        "schema_version": 1,
        "capture": {
            "evidence_ref": capture.evidence_ref,
            "sha256": capture.sha256,
            "source_monotonic_ns": capture.source_monotonic_ns,
        },
        "model": {"model_profile_id": QWEN_VISION_PROFILE_ID},
        "observation": {
            "screen_class": screen_class,
            "visible_text": ["ACCOUNT LOGIN"],
            "ui_objects": [],
            "appeared": [],
            "disappeared": [],
            "changed": [],
        },
        "quality": {
            "schema_valid": True,
            "visual_only": True,
            "structural_authority": False,
            "unknown_fields": [],
        },
    }


def _infer(scheduler, model=QWEN_VISION_MODEL):
    return scheduler.infer(
        model=model,
        expected_digest=QWEN_VISION_DIGEST,
        image_path=Path("unused"),
        evidence_ref="capture:test",
        capture_sha256="a" * 64,
        model_profile_id=QWEN_VISION_PROFILE_ID,
        source_monotonic_ns=42,
        keep_alive="0s",
        num_ctx=QWEN_NUM_CTX,
        num_predict=QWEN_NUM_PREDICT,
    )


def _capture_exception(test_case, exception_type, call):
    try:
        call()
    except exception_type as error:
        return error
    test_case.fail(f"{exception_type.__name__} not raised")


def _assert_sanitized_exception(test_case, error, code, forbidden):
    test_case.assertEqual(code, str(error))
    test_case.assertIsNone(error.__cause__)
    test_case.assertIsNone(error.__context__)
    graph = []
    pending = [error]
    seen = set()
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        graph.append(str(current))
        if current.__cause__ is not None:
            pending.append(current.__cause__)
        if current.__context__ is not None:
            pending.append(current.__context__)
    rendered = "".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )
    outward = "\n".join(graph + [rendered])
    for sentinel in forbidden:
        test_case.assertNotIn(sentinel, outward)


class _FailingBinaryHandle:
    def __init__(self, descriptor, operation, sentinel):
        self._handle = _REAL_FDOPEN(descriptor, "wb")
        self._operation = operation
        self._sentinel = sentinel

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    def close(self):
        self._handle.close()
        if self._operation == "close":
            raise OSError(self._sentinel)

    def write(self, bytes_):
        if self._operation == "write":
            raise OSError(self._sentinel)
        return self._handle.write(bytes_)

    def flush(self):
        if self._operation == "flush":
            raise OSError(self._sentinel)
        return self._handle.flush()

    def fileno(self):
        return self._handle.fileno()


class _FailingTemporaryDirectory:
    def __init__(self, path, sentinel, calls=None):
        self.name = str(path)
        self._sentinel = sentinel
        self._calls = calls

    def __enter__(self):
        return self.name

    def __exit__(self, exc_type, exc, tb):
        self.cleanup()
        return False

    def cleanup(self):
        if self._calls is not None:
            self._calls.append(self.name)
        raise OSError(f"{self._sentinel}:{self.name}")


class _ExplodingEqualityList(list):
    def __eq__(self, other):
        raise TypeError("SECONDARY_EQUALITY_SENTINEL")

    def __ne__(self, other):
        raise TypeError("SECONDARY_EQUALITY_SENTINEL")


class _ExplodingIterationList(list):
    def __iter__(self):
        raise AttributeError("SECONDARY_ITERATION_SENTINEL")


class _ExplodingString(str):
    def __bool__(self):
        raise TypeError("SECONDARY_STRING_SENTINEL")

    def __eq__(self, other):
        raise TypeError("SECONDARY_STRING_SENTINEL")


class _ProgrammingRuntimeError(RuntimeError):
    pass


class ModelSlotSchedulerTests(unittest.TestCase):
    def _scheduler(self, resident, *, digest=QWEN_VISION_DIGEST, provider=None, unload=None):
        self.unloads = []
        self.inferences = []

        def ps():
            value = resident[0]
            if isinstance(value, BaseException):
                raise value
            return value

        def default_unload(model):
            self.unloads.append(model)
            resident[0] = []

        def default_provider(
            model,
            image_path,
            prompt,
            *,
            evidence_ref,
            capture_sha256,
            model_profile_id,
            source_monotonic_ns,
            keep_alive,
            num_ctx,
            num_predict,
        ):
            call = {
                "model": model,
                "image_path": image_path,
                "prompt": prompt,
                "evidence_ref": evidence_ref,
                "capture_sha256": capture_sha256,
                "model_profile_id": model_profile_id,
                "source_monotonic_ns": source_monotonic_ns,
                "keep_alive": keep_alive,
                "num_ctx": num_ctx,
                "num_predict": num_predict,
            }
            self.inferences.append(call)
            if provider:
                return provider(call)
            resident[0] = [model]
            return {"ok": True}

        digest_fn = digest if callable(digest) else lambda model: digest
        return ModelSlotScheduler(
            ps=ps,
            digest=digest_fn,
            infer=default_provider,
            unload=unload or default_unload,
        )

    def test_empty_slot_claims_only_after_exact_provider_load(self):
        resident = [[]]
        scheduler = self._scheduler(resident)
        self.assertEqual({"ok": True}, _infer(scheduler))
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))

    def test_model_slot_error_codes_are_allowlisted_and_value_free(self):
        code_secret = "SENTINEL_SECRET_UNAPPROVED_CODE"
        failure = _capture_exception(
            self,
            ValueError,
            lambda: ModelSlotUnavailable(code_secret),
        )
        _assert_sanitized_exception(
            self,
            failure,
            "model slot error code invalid",
            (code_secret,),
        )

    def test_zero_keep_alive_success_reconciles_empty(self):
        resident = [[]]
        scheduler = self._scheduler(resident, provider=lambda call: {"ok": True})
        _infer(scheduler)
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

    def test_digest_mismatch_and_exception_refuse_safely(self):
        resident = [[]]
        scheduler = self._scheduler(resident, digest="0" * 64)
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_DIGEST_MISMATCH"):
            _infer(scheduler)
        self.assertEqual([], self.inferences)
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

        resident = [[]]
        scheduler = self._scheduler(resident)
        _infer(scheduler)
        scheduler._digest = lambda model: (_ for _ in ()).throw(RuntimeError("digest"))
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_DIGEST_UNAVAILABLE"):
            _infer(scheduler, "other:exact")
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))
        self.assertEqual([QWEN_VISION_MODEL], resident[0])

    def test_foreign_multiple_and_unknown_residency_never_evict(self):
        cases = ((["foreign:model"], "DIFFERENT_RESIDENT_MODEL"),
                 ([QWEN_VISION_MODEL, "foreign:model"], "MULTIPLE_RESIDENT_MODELS"),
                 (None, "RESIDENCY_UNKNOWN"))
        for state, code in cases:
            with self.subTest(state=state):
                scheduler = self._scheduler([state])
                with self.assertRaisesRegex(ModelSlotUnavailable, code):
                    _infer(scheduler)
                self.assertEqual([], self.unloads)

    def test_exact_unowned_target_fails_closed(self):
        scheduler = self._scheduler([[QWEN_VISION_MODEL]])
        with self.assertRaisesRegex(ModelSlotUnavailable, "TARGET_NOT_OWNED"):
            _infer(scheduler)
        self.assertEqual([], self.unloads)

    def test_owned_target_reuse_and_verified_switch(self):
        resident = [[]]
        scheduler = self._scheduler(resident)
        _infer(scheduler)
        _infer(scheduler)
        _infer(scheduler, "other:exact")
        self.assertEqual([QWEN_VISION_MODEL], self.unloads)
        self.assertTrue(scheduler.owns("other:exact"))

    def test_failed_switch_provider_claims_neither_old_nor_new(self):
        resident = [[]]

        def provider(call):
            if call["model"] == QWEN_VISION_MODEL:
                resident[0] = [QWEN_VISION_MODEL]
                return {"ok": True}
            raise RuntimeError("failed before target load")

        scheduler = self._scheduler(resident, provider=provider)
        _infer(scheduler)
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_INFERENCE_FAILED"):
            _infer(scheduler, "other:exact")
        self.assertEqual([], resident[0])
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
        self.assertFalse(scheduler.owns("other:exact"))

    def test_failed_switch_unload_verification_preserves_old_ownership(self):
        resident = [[]]
        unloads = []
        scheduler = self._scheduler(resident, unload=lambda model: unloads.append(model))
        _infer(scheduler)
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_UNLOAD_NOT_VERIFIED"):
            _infer(scheduler, "other:exact")
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))
        self.assertEqual([QWEN_VISION_MODEL], unloads)

    def test_switch_unload_exception_preserves_resident_owner(self):
        resident = [[]]
        scheduler = self._scheduler(resident)
        _infer(scheduler)
        scheduler._unload = lambda model: (_ for _ in ()).throw(RuntimeError("unload"))
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_UNLOAD_FAILED"):
            _infer(scheduler, "other:exact")
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))
        self.assertEqual([QWEN_VISION_MODEL], resident[0])

    def test_provider_failure_before_load_never_claims_later_foreign_same_name(self):
        resident = [[]]
        unloads = []
        scheduler = self._scheduler(
            resident,
            provider=lambda call: (_ for _ in ()).throw(RuntimeError("before load")),
            unload=lambda model: unloads.append(model),
        )
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_INFERENCE_FAILED"):
            _infer(scheduler)
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
        resident[0] = [QWEN_VISION_MODEL]
        scheduler.release()
        self.assertEqual([], unloads)

    def test_provider_failure_after_load_is_owned_but_auto_empty_is_not(self):
        resident = [[]]

        def after_load(call):
            resident[0] = [call["model"]]
            raise RuntimeError("after load")

        scheduler = self._scheduler(resident, provider=after_load)
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_INFERENCE_FAILED"):
            _infer(scheduler)
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))
        scheduler.release()
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

        scheduler = self._scheduler([[]], provider=lambda call: (_ for _ in ()).throw(RuntimeError("auto empty")))
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_INFERENCE_FAILED"):
            _infer(scheduler)
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

    def test_provider_ambiguous_post_state_fails_closed_without_eviction(self):
        cases = ((["foreign:model"], "DIFFERENT_RESIDENT_MODEL"),
                 ([QWEN_VISION_MODEL, "foreign:model"], "MULTIPLE_RESIDENT_MODELS"),
                 (None, "RESIDENCY_UNKNOWN"))
        for state, code in cases:
            with self.subTest(state=state):
                resident = [[]]

                def provider(call, value=state):
                    resident[0] = value
                    return {"ok": True}

                scheduler = self._scheduler(resident, provider=provider)
                with self.assertRaisesRegex(ModelSlotUnavailable, code):
                    _infer(scheduler)
                self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
                self.assertEqual([], self.unloads)

    def test_provider_duration_serializes_different_models(self):
        resident = [[]]
        first_entered = threading.Event()
        first_exit = threading.Event()
        second_started = threading.Event()
        second_inspected = threading.Event()
        second_entered = threading.Event()
        events = []
        failures = []

        def ps():
            if threading.current_thread().name == "second":
                second_inspected.set()
            events.append(("ps", threading.current_thread().name))
            return resident[0]

        def provider(model, image_path, prompt, **kwargs):
            events.append(("enter", model))
            resident[0] = [model]
            if model == QWEN_VISION_MODEL:
                first_entered.set()
                if not first_exit.wait(2):
                    raise AssertionError("barrier timeout")
                events.append(("exit", model))
            else:
                second_entered.set()
            return {"ok": True}

        def unload(model):
            resident[0] = []

        scheduler = ModelSlotScheduler(
            ps=ps,
            digest=lambda model: QWEN_VISION_DIGEST,
            infer=provider,
            unload=unload,
        )
        one = threading.Thread(target=lambda: self._thread_call(failures, lambda: _infer(scheduler)), name="first")
        two = threading.Thread(
            target=lambda: (
                second_started.set(),
                self._thread_call(failures, lambda: _infer(scheduler, "other:exact")),
            ),
            name="second",
        )
        one.start()
        self.assertTrue(first_entered.wait(2))
        two.start()
        self.assertTrue(second_started.wait(2))
        self.assertFalse(second_inspected.wait(0.2))
        self.assertFalse(second_entered.is_set())
        first_exit.set()
        one.join(2)
        two.join(2)
        self.assertEqual([], failures)
        self.assertFalse(one.is_alive())
        self.assertFalse(two.is_alive())
        self.assertTrue(second_entered.is_set())
        self.assertLess(events.index(("exit", QWEN_VISION_MODEL)), events.index(("ps", "second")))

    def test_release_cannot_race_inference(self):
        resident = [[]]
        entered = threading.Event()
        provider_exit = threading.Event()
        release_started = threading.Event()
        release_inspected = threading.Event()
        unloaded = threading.Event()
        failures = []

        def ps():
            if threading.current_thread().name == "release":
                release_inspected.set()
            return resident[0]

        def provider(model, image_path, prompt, **kwargs):
            resident[0] = [model]
            entered.set()
            if not provider_exit.wait(2):
                raise AssertionError("barrier timeout")
            return {"ok": True}

        def unload(model):
            unloaded.set()
            resident[0] = []

        scheduler = ModelSlotScheduler(ps=ps, digest=lambda model: QWEN_VISION_DIGEST, infer=provider, unload=unload)
        one = threading.Thread(target=lambda: self._thread_call(failures, lambda: _infer(scheduler)), name="infer")
        two = threading.Thread(
            target=lambda: (release_started.set(), self._thread_call(failures, scheduler.release)),
            name="release",
        )
        one.start()
        self.assertTrue(entered.wait(2))
        two.start()
        self.assertTrue(release_started.wait(2))
        self.assertFalse(release_inspected.wait(0.2))
        self.assertFalse(unloaded.is_set())
        provider_exit.set()
        one.join(2)
        two.join(2)
        self.assertEqual([], failures)
        self.assertTrue(unloaded.is_set())
        self.assertEqual([], resident[0])

    def test_release_only_owned_and_failed_verification_preserves_owner(self):
        resident = [[]]
        scheduler = self._scheduler(resident)
        _infer(scheduler)
        scheduler.release()
        self.assertEqual([QWEN_VISION_MODEL], self.unloads)
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

        resident = [[]]
        unloads = []
        scheduler = self._scheduler(resident, unload=lambda model: unloads.append(model))
        _infer(scheduler)
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_UNLOAD_NOT_VERIFIED"):
            scheduler.release()
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))

    def test_release_never_unloads_foreign_replacement(self):
        resident = [[]]
        scheduler = self._scheduler(resident)
        _infer(scheduler)
        resident[0] = ["foreign:model"]
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_SLOT_NOT_OWNED"):
            scheduler.release()
        self.assertEqual([], self.unloads)

    def test_release_unload_exception_after_empty_effect_clears_ownership(self):
        resident = [[]]
        unloads = []

        def unload_then_raise(model):
            unloads.append(model)
            resident[0] = []
            raise RuntimeError("provider reported unload failure")

        scheduler = self._scheduler(resident, unload=unload_then_raise)
        _infer(scheduler)
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_UNLOAD_FAILED"):
            scheduler.release()
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

        resident[0] = [QWEN_VISION_MODEL]
        scheduler.release()
        self.assertEqual([QWEN_VISION_MODEL], unloads)

    def test_switch_loses_ownership_for_every_unverified_post_unload_state(self):
        self._assert_unload_loses_ownership(operation="switch", unload_raises=False)
        self._assert_unload_loses_ownership(operation="switch", unload_raises=True)

    def test_release_loses_ownership_for_every_unverified_post_unload_state(self):
        self._assert_unload_loses_ownership(operation="release", unload_raises=False)
        self._assert_unload_loses_ownership(operation="release", unload_raises=True)

    def test_release_unload_exception_with_exact_old_model_preserves_ownership(self):
        resident = [[]]
        unloads = []

        def unload_without_effect(model):
            unloads.append(model)
            raise RuntimeError("unload failed before effect")

        scheduler = self._scheduler(resident, unload=unload_without_effect)
        _infer(scheduler)
        with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_UNLOAD_FAILED"):
            scheduler.release()
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))
        self.assertEqual([QWEN_VISION_MODEL], resident[0])
        self.assertEqual([QWEN_VISION_MODEL], unloads)

    def test_unload_return_and_raise_failures_expose_only_fixed_codes(self):
        foreign_secret = "SENTINEL_SECRET_FOREIGN_MODEL"
        unload_secret = "SENTINEL_SECRET_UNLOAD_PROVIDER"
        ps_secret = "SENTINEL_SECRET_RESIDENCY_PROVIDER"

        resident = [[]]

        def unload_to_foreign(model):
            resident[0] = [foreign_secret]

        scheduler = self._scheduler(resident, unload=unload_to_foreign)
        _infer(scheduler)
        failure = _capture_exception(
            self,
            ModelSlotUnavailable,
            scheduler.release,
        )
        _assert_sanitized_exception(
            self,
            failure,
            "MODEL_UNLOAD_NOT_VERIFIED",
            (foreign_secret,),
        )
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

        resident = [[]]

        def unload_then_fail_unknown(model):
            resident[0] = RuntimeError(ps_secret)
            raise RuntimeError(unload_secret)

        scheduler = self._scheduler(resident, unload=unload_then_fail_unknown)
        _infer(scheduler)
        failure = _capture_exception(
            self,
            ModelSlotUnavailable,
            scheduler.release,
        )
        _assert_sanitized_exception(
            self,
            failure,
            "MODEL_UNLOAD_FAILED",
            (unload_secret, ps_secret),
        )
        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

    def test_digest_provider_exception_is_sanitized_and_preserves_old_owner(self):
        digest_secret = "SENTINEL_SECRET_DIGEST_PROVIDER"
        resident = [[]]
        scheduler = self._scheduler(resident)
        _infer(scheduler)
        scheduler._digest = lambda model: (_ for _ in ()).throw(RuntimeError(digest_secret))

        failure = _capture_exception(
            self,
            ModelSlotUnavailable,
            lambda: _infer(scheduler, "other:exact"),
        )

        _assert_sanitized_exception(
            self,
            failure,
            "MODEL_DIGEST_UNAVAILABLE",
            (digest_secret,),
        )
        self.assertTrue(scheduler.owns(QWEN_VISION_MODEL))

    def test_inference_provider_exception_normal_post_states_are_sanitized(self):
        provider_secret = "SENTINEL_SECRET_INFERENCE_PROVIDER"
        for post_state, owned in (([], False), ([QWEN_VISION_MODEL], True)):
            with self.subTest(post_state=post_state):
                resident = [[]]

                def provider(call, state=post_state):
                    resident[0] = state
                    raise RuntimeError(provider_secret)

                scheduler = self._scheduler(resident, provider=provider)
                failure = _capture_exception(
                    self,
                    ModelSlotUnavailable,
                    lambda: _infer(scheduler),
                )
                _assert_sanitized_exception(
                    self,
                    failure,
                    "MODEL_INFERENCE_FAILED",
                    (provider_secret,),
                )
                self.assertEqual(owned, scheduler.owns(QWEN_VISION_MODEL))

    def test_inference_exception_with_unsafe_post_state_keeps_safety_primary(self):
        provider_secret = "SENTINEL_SECRET_INFERENCE_FAILURE"
        foreign_secret = "SENTINEL_SECRET_POST_MODEL"
        ps_secret = "SENTINEL_SECRET_POST_RESIDENCY"
        cases = (
            ([foreign_secret], "DIFFERENT_RESIDENT_MODEL", (provider_secret, foreign_secret)),
            (RuntimeError(ps_secret), "RESIDENCY_UNKNOWN", (provider_secret, ps_secret)),
        )
        for post_state, expected_code, forbidden in cases:
            with self.subTest(expected_code=expected_code):
                resident = [[]]

                def provider(call, state=post_state):
                    resident[0] = state
                    raise RuntimeError(provider_secret)

                scheduler = self._scheduler(resident, provider=provider)
                failure = _capture_exception(
                    self,
                    ModelSlotUnavailable,
                    lambda: _infer(scheduler),
                )
                _assert_sanitized_exception(
                    self,
                    failure,
                    expected_code,
                    forbidden,
                )
                self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

    def test_inference_does_not_catch_process_control_exceptions(self):
        for control_error in (KeyboardInterrupt(), SystemExit()):
            with self.subTest(error_type=type(control_error).__name__):
                resident = [[]]

                def provider(call, error=control_error):
                    raise error

                scheduler = self._scheduler(resident, provider=provider)
                propagated = _capture_exception(
                    self,
                    type(control_error),
                    lambda: _infer(scheduler),
                )
                self.assertIs(control_error, propagated)
                self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))

    def test_started_provider_control_exceptions_reconcile_every_post_state(self):
        controls = (KeyboardInterrupt("interrupt"), SystemExit("exit"))
        post_states = (
            ("empty", [], False),
            ("exact", [QWEN_VISION_MODEL], True),
            ("foreign", ["foreign:model"], False),
        )
        for control_error in controls:
            for label, post_state, expected_owned in post_states:
                with self.subTest(error=type(control_error).__name__, post_state=label):
                    resident = [[]]
                    unloads = []
                    calls = []

                    def provider(call, state=post_state, error=control_error):
                        calls.append(call)
                        if len(calls) == 1:
                            resident[0] = [call["model"]]
                            return {"ok": True}
                        resident[0] = state
                        raise error

                    scheduler = self._scheduler(
                        resident,
                        provider=provider,
                        unload=lambda model: unloads.append(model),
                    )
                    _infer(scheduler)
                    propagated = _capture_exception(
                        self,
                        type(control_error),
                        lambda: _infer(scheduler),
                    )
                    self.assertIs(control_error, propagated)
                    self.assertEqual(expected_owned, scheduler.owns(QWEN_VISION_MODEL))
                    self.assertIsNone(scheduler._transition_thread)

                    if not expected_owned:
                        resident[0] = [QWEN_VISION_MODEL]
                        with self.assertRaisesRegex(ModelSlotUnavailable, "TARGET_NOT_OWNED"):
                            _infer(scheduler)
                        scheduler.release()
                        self.assertEqual([], unloads)

    def test_started_unload_control_exceptions_reconcile_every_post_state(self):
        controls = (KeyboardInterrupt("interrupt"), SystemExit("exit"))
        post_states = (
            ("empty", [], False),
            ("exact", [QWEN_VISION_MODEL], True),
            ("foreign", ["foreign:model"], False),
        )
        for control_error in controls:
            for label, post_state, expected_owned in post_states:
                with self.subTest(error=type(control_error).__name__, post_state=label):
                    resident = [[]]
                    unloads = []

                    def unload(model, state=post_state, error=control_error):
                        unloads.append(model)
                        resident[0] = state
                        raise error

                    scheduler = self._scheduler(resident, unload=unload)
                    _infer(scheduler)
                    propagated = _capture_exception(
                        self,
                        type(control_error),
                        scheduler.release,
                    )
                    self.assertIs(control_error, propagated)
                    self.assertEqual(expected_owned, scheduler.owns(QWEN_VISION_MODEL))
                    self.assertIsNone(scheduler._transition_thread)

                    if not expected_owned:
                        resident[0] = [QWEN_VISION_MODEL]
                        with self.assertRaisesRegex(ModelSlotUnavailable, "TARGET_NOT_OWNED"):
                            _infer(scheduler)
                        scheduler.release()
                        self.assertEqual([QWEN_VISION_MODEL], unloads)

    def test_programming_exceptions_at_ps_and_digest_propagate_unchanged(self):
        for error_type in (AssertionError, TypeError, AttributeError):
            for seam in ("ps", "digest"):
                with self.subTest(error=error_type.__name__, seam=seam):
                    resident = [[]]
                    scheduler = self._scheduler(resident)
                    programmer_error = error_type(f"{seam} programmer defect")
                    if seam == "ps":
                        scheduler._ps = lambda error=programmer_error: (_ for _ in ()).throw(error)
                    else:
                        scheduler._digest = lambda model, error=programmer_error: (_ for _ in ()).throw(error)

                    propagated = _capture_exception(
                        self,
                        error_type,
                        lambda: _infer(scheduler),
                    )
                    self.assertIs(programmer_error, propagated)
                    self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
                    self.assertIsNone(scheduler._transition_thread)

    def test_post_transition_ps_programming_errors_are_visible_and_clear_owner(self):
        for error_type in (AssertionError, TypeError, AttributeError):
            for transition in ("infer", "unload"):
                with self.subTest(error=error_type.__name__, transition=transition):
                    resident = [[]]
                    ps_error = error_type("post-transition ps programmer defect")

                    def provider(call, error=ps_error):
                        resident[0] = error
                        return {"ok": True}

                    def unload(model, error=ps_error):
                        resident[0] = error

                    scheduler = self._scheduler(
                        resident,
                        provider=provider if transition == "infer" else None,
                        unload=unload if transition == "unload" else None,
                    )
                    if transition == "unload":
                        _infer(scheduler)
                        call = scheduler.release
                    else:
                        call = lambda: _infer(scheduler)

                    propagated = _capture_exception(self, error_type, call)
                    self.assertIs(ps_error, propagated)
                    self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
                    self.assertIsNone(scheduler._transition_thread)

    def test_started_provider_programming_exceptions_reconcile_and_propagate(self):
        for error_type in (AssertionError, TypeError, AttributeError):
            for label, post_state, expected_owned in (
                ("empty", [], False),
                ("exact", [QWEN_VISION_MODEL], True),
                ("foreign", ["foreign:model"], False),
            ):
                with self.subTest(error=error_type.__name__, post_state=label):
                    resident = [[]]
                    calls = []
                    programmer_error = error_type("provider programmer defect")

                    def provider(call, state=post_state, error=programmer_error):
                        calls.append(call)
                        if len(calls) == 1:
                            resident[0] = [call["model"]]
                            return {"ok": True}
                        resident[0] = state
                        raise error

                    scheduler = self._scheduler(resident, provider=provider)
                    _infer(scheduler)
                    propagated = _capture_exception(
                        self,
                        error_type,
                        lambda: _infer(scheduler),
                    )
                    self.assertIs(programmer_error, propagated)
                    self.assertEqual(expected_owned, scheduler.owns(QWEN_VISION_MODEL))
                    self.assertIsNone(scheduler._transition_thread)

    def test_started_unload_programming_exceptions_reconcile_and_propagate(self):
        for error_type in (AssertionError, TypeError, AttributeError):
            for label, post_state, expected_owned in (
                ("empty", [], False),
                ("exact", [QWEN_VISION_MODEL], True),
                ("foreign", ["foreign:model"], False),
            ):
                with self.subTest(error=error_type.__name__, post_state=label):
                    resident = [[]]
                    programmer_error = error_type("unload programmer defect")

                    def unload(model, state=post_state, error=programmer_error):
                        resident[0] = state
                        raise error

                    scheduler = self._scheduler(resident, unload=unload)
                    _infer(scheduler)
                    propagated = _capture_exception(
                        self,
                        error_type,
                        scheduler.release,
                    )
                    self.assertIs(programmer_error, propagated)
                    self.assertEqual(expected_owned, scheduler.owns(QWEN_VISION_MODEL))
                    self.assertIsNone(scheduler._transition_thread)

    def test_explicit_operational_endpoint_errors_use_fixed_slot_codes(self):
        cases = (
            ("ps", "RESIDENCY_UNKNOWN"),
            ("digest", "MODEL_DIGEST_UNAVAILABLE"),
            ("infer", "MODEL_INFERENCE_FAILED"),
            ("unload", "MODEL_UNLOAD_FAILED"),
        )
        for error_type in (OSError, TimeoutError, RuntimeError, ValueError):
            for seam, expected_code in cases:
                with self.subTest(error=error_type.__name__, seam=seam):
                    resident = [[]]
                    sentinel = f"OPERATIONAL_SECRET_{error_type.__name__}_{seam}"
                    operational_error = error_type(sentinel)
                    scheduler = self._scheduler(resident)

                    if seam == "ps":
                        scheduler._ps = lambda error=operational_error: (_ for _ in ()).throw(error)
                        call = lambda: _infer(scheduler)
                    elif seam == "digest":
                        scheduler._digest = lambda model, error=operational_error: (_ for _ in ()).throw(error)
                        call = lambda: _infer(scheduler)
                    elif seam == "infer":
                        scheduler._infer = lambda *args, error=operational_error, **kwargs: (
                            (_ for _ in ()).throw(error)
                        )
                        call = lambda: _infer(scheduler)
                    else:
                        _infer(scheduler)
                        scheduler._unload = lambda model, error=operational_error: (
                            (_ for _ in ()).throw(error)
                        )
                        call = scheduler.release

                    failure = _capture_exception(self, ModelSlotUnavailable, call)
                    _assert_sanitized_exception(
                        self,
                        failure,
                        expected_code,
                        (sentinel,),
                    )

    def test_active_control_or_programming_error_survives_broken_reconciliation(self):
        for primary_error in (KeyboardInterrupt("primary"), SystemExit("primary"), TypeError("primary")):
            for seam in ("infer", "unload"):
                with self.subTest(primary=type(primary_error).__name__, seam=seam):
                    resident = [[]]
                    calls = []

                    def provider(call, error=primary_error):
                        calls.append(call)
                        if len(calls) == 1:
                            resident[0] = [call["model"]]
                            return {"ok": True}
                        resident[0] = AssertionError("secondary residency defect")
                        raise error

                    def unload(model, error=primary_error):
                        resident[0] = AssertionError("secondary residency defect")
                        raise error

                    scheduler = self._scheduler(resident, provider=provider, unload=unload)
                    _infer(scheduler)
                    propagated = _capture_exception(
                        self,
                        type(primary_error),
                        (lambda: _infer(scheduler)) if seam == "infer" else scheduler.release,
                    )
                    self.assertIs(primary_error, propagated)
                    _assert_sanitized_exception(
                        self,
                        propagated,
                        str(primary_error),
                        ("secondary residency defect",),
                    )
                    self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
                    self.assertIsNone(scheduler._transition_thread)

    def test_adversarial_residency_cannot_mask_an_active_transition_error(self):
        shape_factories = (
            ("equality", lambda: _ExplodingEqualityList([QWEN_VISION_MODEL])),
            ("iteration", lambda: _ExplodingIterationList([QWEN_VISION_MODEL])),
            ("string_subclass", lambda: [_ExplodingString(QWEN_VISION_MODEL)]),
        )
        primary_types = (KeyboardInterrupt, SystemExit, TypeError)
        secondary_sentinels = (
            "SECONDARY_EQUALITY_SENTINEL",
            "SECONDARY_ITERATION_SENTINEL",
            "SECONDARY_STRING_SENTINEL",
        )
        for transition in ("infer", "unload"):
            for shape_name, shape_factory in shape_factories:
                for primary_type in primary_types:
                    with self.subTest(
                        transition=transition,
                        shape=shape_name,
                        primary=primary_type.__name__,
                    ):
                        resident = [[]]
                        calls = []
                        unloads = []
                        primary_error = primary_type("PRIMARY_TRANSITION_SENTINEL")

                        def provider(call, error=primary_error):
                            calls.append(call)
                            if len(calls) == 1:
                                resident[0] = [call["model"]]
                                return {"ok": True}
                            resident[0] = shape_factory()
                            raise error

                        def unload(model, error=primary_error):
                            unloads.append(model)
                            resident[0] = shape_factory()
                            raise error

                        scheduler = self._scheduler(
                            resident,
                            provider=provider if transition == "infer" else None,
                            unload=(
                                unload
                                if transition == "unload"
                                else lambda model: unloads.append(model)
                            ),
                        )
                        _infer(scheduler)
                        propagated = _capture_exception(
                            self,
                            primary_type,
                            (lambda: _infer(scheduler))
                            if transition == "infer"
                            else scheduler.release,
                        )
                        self.assertIs(primary_error, propagated)
                        _assert_sanitized_exception(
                            self,
                            propagated,
                            "PRIMARY_TRANSITION_SENTINEL",
                            secondary_sentinels,
                        )
                        transition_code = (
                            ModelSlotScheduler.infer.__code__
                            if transition == "infer"
                            else ModelSlotScheduler._unload_owned_and_verify_empty.__code__
                        )
                        callback_code = (
                            provider.__code__
                            if transition == "infer"
                            else unload.__code__
                        )
                        traceback_codes = []
                        current_traceback = propagated.__traceback__
                        while current_traceback is not None:
                            traceback_codes.append(current_traceback.tb_frame.f_code)
                            current_traceback = current_traceback.tb_next
                        self.assertEqual(1, traceback_codes.count(transition_code))
                        self.assertIs(callback_code, traceback_codes[-1])
                        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
                        self.assertIsNone(scheduler._transition_thread)

                        resident[0] = [QWEN_VISION_MODEL]
                        with self.assertRaisesRegex(ModelSlotUnavailable, "TARGET_NOT_OWNED"):
                            _infer(scheduler)
                        scheduler.release()
                        self.assertEqual(
                            1 if transition == "unload" else 0,
                            len(unloads),
                        )

    def test_adversarial_residency_shapes_fail_closed_without_a_primary(self):
        shape_factories = (
            lambda: _ExplodingEqualityList([QWEN_VISION_MODEL]),
            lambda: _ExplodingIterationList([QWEN_VISION_MODEL]),
            lambda: [_ExplodingString(QWEN_VISION_MODEL)],
        )
        forbidden = (
            "SECONDARY_EQUALITY_SENTINEL",
            "SECONDARY_ITERATION_SENTINEL",
            "SECONDARY_STRING_SENTINEL",
        )
        for shape_factory in shape_factories:
            for transition in ("preflight", "infer", "unload"):
                with self.subTest(shape=shape_factory, transition=transition):
                    resident = [shape_factory() if transition == "preflight" else []]

                    def provider(call):
                        resident[0] = shape_factory()
                        return {"ok": True}

                    def unload(model):
                        resident[0] = shape_factory()

                    scheduler = self._scheduler(
                        resident,
                        provider=provider if transition == "infer" else None,
                        unload=unload if transition == "unload" else None,
                    )
                    if transition == "unload":
                        _infer(scheduler)
                        call = scheduler.release
                        expected_code = "MODEL_UNLOAD_NOT_VERIFIED"
                    else:
                        call = lambda: _infer(scheduler)
                        expected_code = "RESIDENCY_UNKNOWN"

                    failure = _capture_exception(self, ModelSlotUnavailable, call)
                    _assert_sanitized_exception(
                        self,
                        failure,
                        expected_code,
                        forbidden,
                    )
                    self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
                    self.assertIsNone(scheduler._transition_thread)

    def test_runtime_programming_subclasses_propagate_at_all_endpoint_seams(self):
        error_types = (
            NotImplementedError,
            RecursionError,
            _ProgrammingRuntimeError,
        )
        for error_type in error_types:
            for seam in ("ps", "digest", "infer", "unload"):
                with self.subTest(error=error_type.__name__, seam=seam):
                    resident = [[]]
                    unloads = []
                    programmer_error = error_type("RUNTIME_PROGRAMMING_SENTINEL")
                    scheduler = self._scheduler(
                        resident,
                        unload=lambda model: unloads.append(model),
                    )

                    if seam == "ps":
                        scheduler._ps = lambda error=programmer_error: (
                            (_ for _ in ()).throw(error)
                        )
                        call = lambda: _infer(scheduler)
                    elif seam == "digest":
                        scheduler._digest = lambda model, error=programmer_error: (
                            (_ for _ in ()).throw(error)
                        )
                        call = lambda: _infer(scheduler)
                    elif seam == "infer":
                        def fail_infer(*args, error=programmer_error, **kwargs):
                            resident[0] = []
                            raise error

                        scheduler._infer = fail_infer
                        call = lambda: _infer(scheduler)
                    else:
                        _infer(scheduler)

                        def fail_unload(model, error=programmer_error):
                            unloads.append(model)
                            resident[0] = []
                            raise error

                        scheduler._unload = fail_unload
                        call = scheduler.release

                    propagated = _capture_exception(self, error_type, call)
                    self.assertIs(programmer_error, propagated)
                    _assert_sanitized_exception(
                        self,
                        propagated,
                        "RUNTIME_PROGRAMMING_SENTINEL",
                        (),
                    )
                    self.assertIsNone(scheduler._transition_thread)

                    if seam in {"infer", "unload"}:
                        self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
                        resident[0] = [QWEN_VISION_MODEL]
                        with self.assertRaisesRegex(ModelSlotUnavailable, "TARGET_NOT_OWNED"):
                            _infer(scheduler)
                        scheduler.release()
                        self.assertEqual(1 if seam == "unload" else 0, len(unloads))

    def _assert_unload_loses_ownership(self, *, operation, unload_raises):
        post_states = (
            ("foreign", ["foreign:model"]),
            ("multiple", [QWEN_VISION_MODEL, "foreign:model"]),
            ("unknown", None),
            ("malformed", [""]),
        )
        expected_code = "MODEL_UNLOAD_FAILED" if unload_raises else "MODEL_UNLOAD_NOT_VERIFIED"
        for label, post_state in post_states:
            with self.subTest(operation=operation, unload_raises=unload_raises, post_state=label):
                resident = [[]]
                unloads = []

                def unload(model, state=post_state):
                    unloads.append(model)
                    resident[0] = state
                    if unload_raises:
                        raise RuntimeError("unload provider failed")

                scheduler = self._scheduler(resident, unload=unload)
                _infer(scheduler)
                with self.assertRaisesRegex(ModelSlotUnavailable, expected_code):
                    if operation == "switch":
                        _infer(scheduler, "other:exact")
                    else:
                        scheduler.release()

                self.assertFalse(scheduler.owns(QWEN_VISION_MODEL))
                resident[0] = [QWEN_VISION_MODEL]
                with self.assertRaisesRegex(ModelSlotUnavailable, "TARGET_NOT_OWNED"):
                    _infer(scheduler)
                scheduler.release()
                self.assertEqual([QWEN_VISION_MODEL], unloads)

    @staticmethod
    def _thread_call(failures, call):
        try:
            call()
        except BaseException as exc:
            failures.append(exc)


class AgentVisionSensorTests(unittest.TestCase):
    def _capture(self, directory, *, body=b"safe frame", secret_safe=True, digest=None,
                 run_id="run-1", evidence_ref="capture:one", filename="frame.bin"):
        path = directory / filename
        path.write_bytes(body)
        return SecretSafeCapture(
            run_id=run_id,
            evidence_ref=evidence_ref,
            path=path,
            sha256=hashlib.sha256(body).hexdigest() if digest is None else digest,
            secret_safe=secret_safe,
            source_monotonic_ns=42,
        )

    def _sensor(self, provider, *, digest=None):
        resident = [[]]

        def infer(
            model,
            image_path,
            prompt,
            *,
            evidence_ref,
            capture_sha256,
            model_profile_id,
            source_monotonic_ns,
            keep_alive,
            num_ctx,
            num_predict,
        ):
            return provider({
                "model": model,
                "image_path": image_path,
                "prompt": prompt,
                "evidence_ref": evidence_ref,
                "capture_sha256": capture_sha256,
                "model_profile_id": model_profile_id,
                "source_monotonic_ns": source_monotonic_ns,
                "keep_alive": keep_alive,
                "num_ctx": num_ctx,
                "num_predict": num_predict,
            })

        return AgentVisionSensor(ModelSlotScheduler(
            ps=lambda: resident[0],
            digest=digest or (lambda model: QWEN_VISION_DIGEST),
            infer=infer,
            unload=lambda model: resident.__setitem__(0, []),
        ))

    def test_unsafe_empty_or_hash_mismatched_capture_refuses_before_provider(self):
        cases = ((b"safe", False, None, UnsafeInputError),
                 (b"", True, None, ValueError),
                 (b"safe", True, "0" * 64, ValueError))
        for body, secret_safe, digest, error in cases:
            calls = []
            with self.subTest(body=body), tempfile.TemporaryDirectory() as raw:
                capture = self._capture(Path(raw), body=body, secret_safe=secret_safe, digest=digest)
                sensor = self._sensor(lambda call: calls.append(call))
                with self.assertRaises(error):
                    sensor.observe(capture)
            self.assertEqual([], calls)

    def test_pinned_provider_args_have_no_temperature_or_custom_prompt(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            calls = []
            self._sensor(lambda call: calls.append(call) or _visual_evidence(capture)).observe(capture)
        self.assertEqual(QWEN_VISION_MODEL, calls[0]["model"])
        self.assertEqual("0s", calls[0]["keep_alive"])
        self.assertEqual(QWEN_NUM_CTX, calls[0]["num_ctx"])
        self.assertEqual(QWEN_NUM_PREDICT, calls[0]["num_predict"])
        self.assertEqual(QWEN_VISION_PROFILE_ID, calls[0]["model_profile_id"])
        self.assertNotIn("temperature", calls[0])
        self.assertEqual(0, QWEN_TEMPERATURE)
        self.assertNotIn("caller secret", calls[0]["prompt"])

    def test_constructor_has_no_free_form_prompt_channel(self):
        scheduler = ModelSlotScheduler(
            ps=lambda: [], digest=lambda model: QWEN_VISION_DIGEST,
            infer=lambda *args, **kwargs: None, unload=lambda model: None,
        )
        with self.assertRaises(TypeError):
            AgentVisionSensor(scheduler, prompt="caller secret")

    def test_endpoint_bound_stable_adapter_signature_is_directly_compatible_offline(self):
        endpoint_bound = partial(run_ollama_trial, "http://127.0.0.1:11434")
        signature = inspect.signature(endpoint_bound)
        signature.bind(
            QWEN_VISION_MODEL,
            Path("snapshot"),
            "static prompt",
            evidence_ref="capture:one",
            capture_sha256="a" * 64,
            model_profile_id=QWEN_VISION_PROFILE_ID,
            source_monotonic_ns=42,
            keep_alive="0s",
            num_ctx=QWEN_NUM_CTX,
            num_predict=QWEN_NUM_PREDICT,
        )

    def test_provider_uses_snapshot_if_original_is_mutated_replaced_or_unlinked(self):
        for action in ("mutate", "replace", "unlink"):
            with self.subTest(action=action), tempfile.TemporaryDirectory() as raw:
                directory = Path(raw)
                capture = self._capture(directory)
                consumed = []

                def provider(call):
                    if action == "mutate":
                        capture.path.write_bytes(b"changed")
                    elif action == "replace":
                        replacement = directory / "replacement"
                        replacement.write_bytes(b"replacement")
                        replacement.replace(capture.path)
                    else:
                        capture.path.unlink()
                    consumed.append(Path(call["image_path"]).read_bytes())
                    return _visual_evidence(capture)

                result = self._sensor(provider).observe(capture)
                self.assertEqual([b"safe frame"], consumed)
                self.assertEqual(capture.sha256, result.capture_sha256)

    def test_snapshot_tamper_is_rejected_and_retry_succeeds(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            calls = []

            def provider(call):
                calls.append(call)
                if len(calls) == 1:
                    snapshot = Path(call["image_path"])
                    snapshot.chmod(0o600)
                    snapshot.write_bytes(b"tampered")
                return _visual_evidence(capture)

            sensor = self._sensor(provider)
            with self.assertRaisesRegex(ValueError, "snapshot integrity"):
                sensor.observe(capture)
            result = sensor.observe(capture)
        self.assertEqual(capture.sha256, result.capture_sha256)
        self.assertEqual(2, len(calls))

    def test_capture_and_snapshot_os_errors_do_not_leak_paths_or_causes(self):
        capture_secret = "SENTINEL_SECRET_CAPTURE_PATH"
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(
                Path(raw),
                filename=f"{capture_secret}.bin",
            )
            capture.path.unlink()
            failure = _capture_exception(
                self,
                ValueError,
                lambda: self._sensor(lambda call: None).observe(capture),
            )
            _assert_sanitized_exception(
                self,
                failure,
                "capture bytes unavailable",
                (capture_secret, str(capture.path)),
            )

            capture = self._capture(Path(raw), filename="snapshot-source.bin")
            snapshot_parents = []

            def unlink_snapshot(call):
                snapshot = Path(call["image_path"])
                snapshot_parents.append(snapshot.parent)
                snapshot.unlink()
                return _visual_evidence(capture)

            failure = _capture_exception(
                self,
                ValueError,
                lambda: self._sensor(unlink_snapshot).observe(capture),
            )
            _assert_sanitized_exception(
                self,
                failure,
                "capture snapshot integrity invalid",
                ("capture.snapshot", "tibia-re-vision-"),
            )
            self.assertFalse(snapshot_parents[0].exists())

    def test_every_snapshot_filesystem_operation_is_fixed_sanitized_and_retryable(self):
        operations = (
            "temporary_parent",
            "exclusive_open",
            "fdopen",
            "descriptor_close",
            "write",
            "flush",
            "fsync",
            "close",
            "chmod",
            "lstat",
            "read_verify",
            "cleanup",
        )
        for operation in operations:
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as raw:
                directory = Path(raw)
                capture = self._capture(directory, filename=f"{operation}.bin")
                calls = []
                sensor = self._sensor(
                    lambda call: calls.append(call) or _visual_evidence(capture)
                )
                sentinel = f"SENTINEL_SECRET_SNAPSHOT_{operation.upper()}"
                generated_paths = []

                if operation == "temporary_parent":
                    failure_patch = patch(
                        "tools.tibia_re_control_center.agent_vision.tempfile.TemporaryDirectory",
                        side_effect=OSError(sentinel),
                    )
                elif operation == "exclusive_open":
                    def fail_open(path, *args, **kwargs):
                        generated_paths.append(str(path))
                        raise OSError(f"{sentinel}:{path}")

                    failure_patch = patch(
                        "tools.tibia_re_control_center.agent_vision.os.open",
                        side_effect=fail_open,
                    )
                elif operation == "fdopen":
                    failure_patch = patch(
                        "tools.tibia_re_control_center.agent_vision.os.fdopen",
                        side_effect=OSError(sentinel),
                    )
                elif operation == "descriptor_close":
                    def fail_descriptor_close(descriptor):
                        _REAL_OS_CLOSE(descriptor)
                        raise OSError(sentinel)

                    failure_patch = ExitStack()
                    failure_patch.enter_context(patch(
                        "tools.tibia_re_control_center.agent_vision.os.fdopen",
                        side_effect=OSError("FDOPEN_OPERATIONAL_SENTINEL"),
                    ))
                    failure_patch.enter_context(patch(
                        "tools.tibia_re_control_center.agent_vision.os.close",
                        side_effect=fail_descriptor_close,
                    ))
                elif operation in {"write", "flush", "close"}:
                    failure_patch = patch(
                        "tools.tibia_re_control_center.agent_vision.os.fdopen",
                        side_effect=lambda descriptor, mode, op=operation, value=sentinel: (
                            _FailingBinaryHandle(descriptor, op, value)
                        ),
                    )
                elif operation == "fsync":
                    failure_patch = patch(
                        "tools.tibia_re_control_center.agent_vision.os.fsync",
                        side_effect=OSError(sentinel),
                    )
                elif operation == "chmod":
                    failure_patch = patch.object(
                        Path,
                        "chmod",
                        side_effect=OSError(sentinel),
                    )
                elif operation == "lstat":
                    failure_patch = patch.object(
                        Path,
                        "lstat",
                        side_effect=OSError(sentinel),
                    )
                elif operation == "read_verify":
                    def fail_snapshot_read(path):
                        if path.name == "capture.snapshot":
                            raise OSError(f"{sentinel}:{path}")
                        return _REAL_PATH_READ_BYTES(path)

                    failure_patch = patch.object(Path, "read_bytes", new=fail_snapshot_read)
                else:
                    cleanup_parent = directory / "cleanup-parent"
                    cleanup_parent.mkdir()
                    failure_patch = patch(
                        "tools.tibia_re_control_center.agent_vision.tempfile.TemporaryDirectory",
                        return_value=_FailingTemporaryDirectory(cleanup_parent, sentinel),
                    )

                with failure_patch:
                    failure = _capture_exception(
                        self,
                        ValueError,
                        lambda: sensor.observe(capture),
                    )
                _assert_sanitized_exception(
                    self,
                    failure,
                    (
                        "capture snapshot integrity invalid"
                        if operation in {"lstat", "read_verify"}
                        else "capture snapshot filesystem failure"
                    ),
                    (
                        sentinel,
                        "FDOPEN_OPERATIONAL_SENTINEL",
                        "tibia-re-vision-",
                        *generated_paths,
                    ),
                )

                result = sensor.observe(capture)
                self.assertEqual(capture.sha256, result.capture_sha256)
                self.assertGreaterEqual(len(calls), 1)

    def test_snapshot_tamper_and_control_exception_preserves_control_and_retry(self):
        for control_error in (
            KeyboardInterrupt("INTERRUPT_SECRET_SENTINEL"),
            SystemExit("SYSTEM_EXIT_SECRET_SENTINEL"),
        ):
            with self.subTest(error=type(control_error).__name__), tempfile.TemporaryDirectory() as raw:
                capture = self._capture(Path(raw))
                calls = []

                def provider(call, error=control_error):
                    calls.append(call)
                    if len(calls) == 1:
                        snapshot = Path(call["image_path"])
                        snapshot.chmod(0o600)
                        snapshot.write_bytes(b"tampered")
                        raise error
                    return _visual_evidence(capture)

                sensor = self._sensor(provider)
                propagated = _capture_exception(
                    self,
                    type(control_error),
                    lambda: sensor.observe(capture),
                )
                self.assertIs(control_error, propagated)
                self.assertIsNone(propagated.__cause__)
                self.assertIsNone(propagated.__context__)
                result = sensor.observe(capture)
                self.assertEqual(capture.sha256, result.capture_sha256)
                self.assertEqual(2, len(calls))

    def test_tamper_and_cleanup_failure_never_replace_an_active_provider_error(self):
        active_errors = (
            KeyboardInterrupt("PRIMARY_INTERRUPT"),
            SystemExit("PRIMARY_EXIT"),
            TypeError("PRIMARY_PROGRAMMING"),
            RuntimeError("PRIMARY_OPERATIONAL"),
        )
        for active_error in active_errors:
            with self.subTest(error=type(active_error).__name__), tempfile.TemporaryDirectory() as raw:
                directory = Path(raw)
                capture = self._capture(directory)
                calls = []
                cleanup_calls = []
                cleanup_sentinel = "SENTINEL_SECRET_CLEANUP_DURING_PRIMARY"
                cleanup_parent = directory / "cleanup-primary"
                cleanup_parent.mkdir()

                def provider(call, error=active_error):
                    calls.append(call)
                    if len(calls) == 1:
                        snapshot = Path(call["image_path"])
                        snapshot.chmod(0o600)
                        snapshot.write_bytes(b"tampered")
                        raise error
                    return _visual_evidence(capture)

                sensor = self._sensor(provider)
                with patch(
                    "tools.tibia_re_control_center.agent_vision.tempfile.TemporaryDirectory",
                    return_value=_FailingTemporaryDirectory(
                        cleanup_parent,
                        cleanup_sentinel,
                        cleanup_calls,
                    ),
                ):
                    if isinstance(active_error, RuntimeError):
                        propagated = _capture_exception(
                            self,
                            ModelSlotUnavailable,
                            lambda: sensor.observe(capture),
                        )
                        expected_text = "MODEL_INFERENCE_FAILED"
                    else:
                        propagated = _capture_exception(
                            self,
                            type(active_error),
                            lambda: sensor.observe(capture),
                        )
                        self.assertIs(active_error, propagated)
                        expected_text = str(active_error)

                _assert_sanitized_exception(
                    self,
                    propagated,
                    expected_text,
                    (cleanup_sentinel, str(cleanup_parent)),
                )
                self.assertEqual([str(cleanup_parent)], cleanup_calls)
                result = sensor.observe(capture)
                self.assertEqual(capture.sha256, result.capture_sha256)
                self.assertEqual(2, len(calls))

    def test_strict_output_diagnostics_never_include_untrusted_values(self):
        output_secret = "SENTINEL_SECRET_MODEL_OUTPUT"
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            evidence = _visual_evidence(capture)
            evidence[output_secret] = {"raw": output_secret}
            failure = _capture_exception(
                self,
                ValueError,
                lambda: self._sensor(lambda call: evidence).observe(capture),
            )
        _assert_sanitized_exception(
            self,
            failure,
            "VisualEvidence invalid: payload keys invalid",
            (output_secret,),
        )

    def test_provider_digest_and_schema_failures_all_allow_exact_retry(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)

            capture = self._capture(directory, filename="provider.bin")
            provider_calls = []

            def flaky_provider(call):
                provider_calls.append(call)
                if len(provider_calls) == 1:
                    raise RuntimeError("transient provider")
                return _visual_evidence(capture)

            sensor = self._sensor(flaky_provider)
            with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_INFERENCE_FAILED"):
                sensor.observe(capture)
            sensor.observe(capture)
            self.assertEqual(2, len(provider_calls))

            capture = self._capture(directory, filename="digest.bin")
            digest_calls = []

            def flaky_digest(model):
                digest_calls.append(model)
                if len(digest_calls) == 1:
                    raise RuntimeError("transient digest")
                return QWEN_VISION_DIGEST

            provider_calls = []
            sensor = self._sensor(
                lambda call: provider_calls.append(call) or _visual_evidence(capture),
                digest=flaky_digest,
            )
            with self.assertRaisesRegex(ModelSlotUnavailable, "MODEL_DIGEST_UNAVAILABLE"):
                sensor.observe(capture)
            sensor.observe(capture)
            self.assertEqual(1, len(provider_calls))

            capture = self._capture(directory, filename="schema.bin")
            schema_calls = []

            def flaky_schema(call):
                schema_calls.append(call)
                evidence = _visual_evidence(capture)
                if len(schema_calls) == 1:
                    evidence["model"]["authority"] = "forbidden"
                return evidence

            sensor = self._sensor(flaky_schema)
            with self.assertRaisesRegex(ValueError, "VisualEvidence"):
                sensor.observe(capture)
            sensor.observe(capture)
            self.assertEqual(2, len(schema_calls))

    def test_visual_only_in_game_mapping_is_non_authoritative(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            observation = self._sensor(
                lambda call: _visual_evidence(capture, screen_class="IN_GAME_VISUAL")
            ).observe(capture)
        self.assertEqual(AgentVisualState.WORLD_VISUAL.value, observation.screen_class)
        self.assertTrue(observation.visual_only)
        self.assertFalse(observation.structural_authority)

    def test_successful_identity_binding_and_run_scoped_duplicates(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            first = self._capture(directory, filename="first")
            rebound = self._capture(directory, body=b"different", filename="rebound")
            duplicate = self._capture(directory, evidence_ref="capture:two", filename="duplicate")
            cross_run = self._capture(
                directory, run_id="run-2", evidence_ref="capture:two", filename="cross-run"
            )
            captures = [first, cross_run]
            calls = []

            def provider(call):
                evidence = _visual_evidence(captures[len(calls)])
                calls.append(call)
                return evidence

            sensor = self._sensor(provider)
            sensor.observe(first)
            with self.assertRaisesRegex(ValueError, "EVIDENCE_REF_SHA256_REBIND"):
                sensor.observe(rebound)
            with self.assertRaisesRegex(ValueError, "DUPLICATE_CAPTURE_SHA256"):
                sensor.observe(duplicate)
            result = sensor.observe(cross_run)
        self.assertEqual(cross_run.evidence_ref, result.evidence_ref)
        self.assertEqual(2, len(calls))

    def test_concurrent_duplicate_reserves_once_and_calls_provider_once(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            entered = threading.Event()
            provider_exit = threading.Event()
            calls = []
            results = []
            failures = []

            def provider(call):
                calls.append(call)
                entered.set()
                if not provider_exit.wait(2):
                    raise AssertionError("barrier timeout")
                return _visual_evidence(capture)

            sensor = self._sensor(provider)

            def observe():
                try:
                    results.append(sensor.observe(capture))
                except BaseException as exc:
                    failures.append(exc)

            one = threading.Thread(target=observe)
            two = threading.Thread(target=observe)
            one.start()
            self.assertTrue(entered.wait(2))
            two.start()
            two.join(2)
            self.assertFalse(two.is_alive())
            provider_exit.set()
            one.join(2)
        self.assertEqual(1, len(calls))
        self.assertEqual(1, len(results))
        self.assertEqual(1, len(failures))
        self.assertRegex(str(failures[0]), "DUPLICATE_CAPTURE_SHA256")

    def test_completed_duplicate_never_returns_stale_evidence(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            calls = []
            sensor = self._sensor(lambda call: calls.append(call) or _visual_evidence(capture))
            sensor.observe(capture)
            with self.assertRaisesRegex(ValueError, "DUPLICATE_CAPTURE_SHA256"):
                sensor.observe(capture)
        self.assertEqual(1, len(calls))

    def test_snapshot_metadata_policy_is_factored_for_posix_and_windows(self):
        regular = stat.S_IFREG
        cases = (
            (False, regular | 0o400, True),
            (False, regular | 0o444, True),
            (False, regular | 0o600, False),
            (False, regular | 0o200, False),
            (True, regular | 0o444, True),
            (True, regular | 0o400, True),
            (True, regular | 0o666, False),
            (True, regular | 0o644, False),
            (False, stat.S_IFLNK | 0o400, False),
            (True, stat.S_IFDIR | 0o444, False),
        )
        for windows, mode, expected in cases:
            with self.subTest(windows=windows, mode=oct(mode)):
                self.assertEqual(
                    expected,
                    AgentVisionSensor._snapshot_metadata_is_safe(
                        mode,
                        windows=windows,
                    ),
                )

    @unittest.skipUnless(os.name == "nt", "requires real Windows chmod semantics")
    def test_windows_snapshot_exact_path_read_tamper_and_cleanup(self):
        with tempfile.TemporaryDirectory() as raw:
            capture = self._capture(Path(raw))
            snapshot_parents = []
            consumed = []

            def provider(call):
                snapshot = Path(call["image_path"])
                snapshot_parents.append(snapshot.parent)
                consumed.append(snapshot.read_bytes())
                return _visual_evidence(capture)

            result = self._sensor(provider).observe(capture)
            self.assertEqual(capture.sha256, result.capture_sha256)
            self.assertEqual([b"safe frame"], consumed)
            self.assertFalse(snapshot_parents[0].exists())

            capture = self._capture(Path(raw), filename="tamper.bin")

            def tampering_provider(call):
                snapshot = Path(call["image_path"])
                snapshot_parents.append(snapshot.parent)
                snapshot.chmod(stat.S_IREAD | stat.S_IWRITE)
                snapshot.write_bytes(b"tampered")
                return _visual_evidence(capture)

            with self.assertRaisesRegex(ValueError, "snapshot integrity"):
                self._sensor(tampering_provider).observe(capture)
            self.assertFalse(snapshot_parents[1].exists())


if __name__ == "__main__":
    unittest.main()
