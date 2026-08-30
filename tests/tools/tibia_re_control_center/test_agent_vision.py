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
