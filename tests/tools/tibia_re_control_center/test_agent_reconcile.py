"""Deterministic, authority-neutral visual/runtime reconciliation tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
import unittest

from tools.tibia_re_control_center import agent_reconcile as reconcile_module
from tools.tibia_re_control_center.agent_reconcile import (
    ReconciledState,
    RuntimeEvidenceClass,
    RuntimeObservation,
    reconcile_state,
)
from tools.tibia_re_control_center.agent_vision import VisionObservation
from tools.tibia_re_control_center.agent_vision import QWEN_VISION_PROFILE_ID


class _StringSubclass(str):
    pass


class _TupleSubclass(tuple):
    pass


def _visual(
    screen_class: object = "WORLD_VISUAL",
    *,
    visible_text: object = (),
    confidence: object = None,
    evidence_ref: object = "capture:fixture",
    capture_sha256: object = "a" * 64,
    model_profile_id: object = QWEN_VISION_PROFILE_ID,
    visual_only: object = True,
    structural_authority: object = False,
) -> VisionObservation:
    return VisionObservation(
        screen_class=screen_class,  # type: ignore[arg-type]
        visible_text=visible_text,  # type: ignore[arg-type]
        confidence=confidence,  # type: ignore[arg-type]
        model_profile_id=model_profile_id,  # type: ignore[arg-type]
        evidence_ref=evidence_ref,  # type: ignore[arg-type]
        capture_sha256=capture_sha256,  # type: ignore[arg-type]
        visual_only=visual_only,  # type: ignore[arg-type]
        structural_authority=structural_authority,  # type: ignore[arg-type]
    )


def _runtime(
    state: object = "UNKNOWN",
    evidence_class: object = RuntimeEvidenceClass.UNKNOWN,
    evidence_refs: object = (),
) -> RuntimeObservation:
    return RuntimeObservation(  # type: ignore[arg-type]
        state=state,
        evidence_class=evidence_class,
        evidence_refs=evidence_refs,
    )


def _trusted_context(
    runtime: RuntimeObservation,
    *,
    current_session_id: str = "session-current",
    current_run_id: str = "run-current",
    current_runtime_id: str = "track-a-runtime",
    current_runtime_instance_id: str = "instance-current",
    evidence_session_id: str = "session-current",
    evidence_run_id: str = "run-current",
    evidence_runtime_id: str = "track-a-runtime",
    evidence_runtime_instance_id: str = "instance-current",
    producer_id: str = "reviewed-producer",
    producer_contract_id: str = "runtime-state-v1",
    reviewed_producer_id: str = "reviewed-producer",
    reviewed_contract_id: str = "runtime-state-v1",
    observed_monotonic_ns: int = 950,
    current_monotonic_ns: int = 1_000,
    max_age_ns: int = 100,
) -> reconcile_module._ResolverStateSnapshot:
    """Build fake resolver-owned state; it is not authority by itself."""
    return reconcile_module._ResolverStateSnapshot(
        current_session_id=current_session_id,
        current_run_id=current_run_id,
        current_runtime_id=current_runtime_id,
        current_runtime_instance_id=current_runtime_instance_id,
        current_monotonic_ns=current_monotonic_ns,
        max_age_ns=max_age_ns,
        reviewed_producers=(
            reconcile_module._ReviewedProducerContract(
                producer_id=reviewed_producer_id,
                contract_id=reviewed_contract_id,
            ),
        ),
        runtime_evidence=reconcile_module._RuntimeEvidenceRecord(
            observation=runtime,
            session_id=evidence_session_id,
            run_id=evidence_run_id,
            runtime_id=evidence_runtime_id,
            runtime_instance_id=evidence_runtime_instance_id,
            producer_id=producer_id,
            producer_contract_id=producer_contract_id,
            observed_monotonic_ns=observed_monotonic_ns,
        ),
    )


class _FakeControlCenterRuntimeResolver:
    """Fake injected only at the trusted Control Center composition seam."""

    def __init__(self, context: reconcile_module._ResolverStateSnapshot) -> None:
        self.__context = context

    def resolve_current_reviewed(
        self,
        runtime: RuntimeObservation,
    ) -> RuntimeObservation | None:
        if reconcile_module._resolver_state_matches_runtime(runtime, self.__context):
            return self.__context.runtime_evidence.observation
        return None


def _trusted_reconcile(
    visual: VisionObservation,
    runtime: RuntimeObservation,
    context: reconcile_module._ResolverStateSnapshot,
):
    resolver = _FakeControlCenterRuntimeResolver(context)
    reconciler = reconcile_module._compose_trusted_reconciler(resolver)
    return reconciler.reconcile_state(visual, runtime)


class ReconciliationTests(unittest.TestCase):
    def test_caller_constructed_fact_bundle_cannot_self_grant_authority(self):
        cases = (
            ("WORLD_VISUAL", "IN_GAME"),
            ("WORLD_EXIT_VISUAL", "WORLD_EXIT"),
            ("LOGIN_SCREEN", "IN_GAME"),
        )

        for visual_state, runtime_state in cases:
            with self.subTest(visual_state=visual_state, runtime_state=runtime_state):
                runtime = _runtime(
                    runtime_state,
                    RuntimeEvidenceClass.REVIEWED_CAUSAL,
                    ("runtime:self-selected",),
                )
                caller_minted_context = _trusted_context(runtime)

                with self.assertRaises(TypeError):
                    reconcile_state(
                        _visual(visual_state),
                        runtime,
                        trusted_context=caller_minted_context,  # type: ignore[call-arg]
                    )

                default_result = reconcile_state(_visual(visual_state), runtime)
                self.assertIs(default_result.state, ReconciledState.UNKNOWN)

    def test_resolver_binding_requires_trusted_composition_seam(self):
        runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:composition",),
        )
        resolver = _FakeControlCenterRuntimeResolver(_trusted_context(runtime))

        with self.assertRaises(TypeError):
            reconcile_module._ResolverBoundReconciler(
                resolver,
                _issuance_key=object(),
            )

        reconciler = reconcile_module._compose_trusted_reconciler(resolver)
        with self.assertRaises(AttributeError):
            reconciler.resolver = resolver

    def test_bare_reviewed_runtime_observation_cannot_self_promote(self):
        runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("opaque-ref-cannot-confer-authority",),
        )

        result = reconcile_state(_visual("WORLD_VISUAL"), runtime)

        self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_forged_runtime_observation_does_not_match_trusted_evidence(self):
        trusted_runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:trusted",),
        )
        forged_runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:forged",),
        )
        context = _trusted_context(trusted_runtime)
        self.assertIsNotNone(context, "trusted reconciliation context API is missing")

        result = _trusted_reconcile(
            _visual("WORLD_VISUAL"),
            forged_runtime,
            context,
        )

        self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_stale_reviewed_runtime_evidence_is_inconclusive(self):
        runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:stale",),
        )
        context = _trusted_context(runtime, observed_monotonic_ns=899)
        self.assertIsNotNone(context, "trusted reconciliation context API is missing")

        result = _trusted_reconcile(
            _visual("WORLD_VISUAL"),
            runtime,
            context,
        )

        self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_freshness_window_is_closed_and_malformed_time_fails_closed(self):
        runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:freshness",),
        )
        valid_boundary = _trusted_context(runtime, observed_monotonic_ns=900)
        invalid_contexts = (
            _trusted_context(runtime, observed_monotonic_ns=1_001),
            _trusted_context(runtime, current_monotonic_ns=True),
            _trusted_context(runtime, max_age_ns=-1),
            replace(valid_boundary, reviewed_producers=()),
        )

        boundary_result = _trusted_reconcile(
            _visual("WORLD_VISUAL"),
            runtime,
            valid_boundary,
        )
        self.assertIs(boundary_result.state, ReconciledState.WORLD_CONFIRMED)

        for context in invalid_contexts:
            with self.subTest(context=context):
                result = _trusted_reconcile(
                    _visual("WORLD_VISUAL"),
                    runtime,
                    context,
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_wrong_session_or_run_reviewed_runtime_evidence_is_inconclusive(self):
        runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:wrong-run",),
        )
        cases = (
            ("wrong session", {"evidence_session_id": "session-other"}),
            ("wrong run", {"evidence_run_id": "run-other"}),
        )

        for name, overrides in cases:
            with self.subTest(name=name):
                context = _trusted_context(runtime, **overrides)
                self.assertIsNotNone(context, "trusted reconciliation context API is missing")
                result = _trusted_reconcile(
                    _visual("WORLD_VISUAL"),
                    runtime,
                    context,
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_wrong_runtime_identity_or_instance_is_inconclusive(self):
        runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:wrong-identity",),
        )
        cases = (
            ("wrong runtime", {"evidence_runtime_id": "runtime-other"}),
            ("wrong instance", {"evidence_runtime_instance_id": "instance-other"}),
        )

        for name, overrides in cases:
            with self.subTest(name=name):
                context = _trusted_context(runtime, **overrides)
                self.assertIsNotNone(context, "trusted reconciliation context API is missing")
                result = _trusted_reconcile(
                    _visual("WORLD_VISUAL"),
                    runtime,
                    context,
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_unknown_producer_or_contract_is_inconclusive(self):
        runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:unknown-producer",),
        )
        cases = (
            ("unknown producer", {"producer_id": "producer-other"}),
            ("unknown contract", {"producer_contract_id": "runtime-state-v2"}),
        )

        for name, overrides in cases:
            with self.subTest(name=name):
                context = _trusted_context(runtime, **overrides)
                self.assertIsNotNone(context, "trusted reconciliation context API is missing")
                result = _trusted_reconcile(
                    _visual("WORLD_VISUAL"),
                    runtime,
                    context,
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_valid_current_reviewed_evidence_enables_finite_promotions_and_conflict(self):
        cases = (
            (
                "world confirmed",
                "WORLD_VISUAL",
                "IN_GAME",
                "runtime:world",
                ReconciledState.WORLD_CONFIRMED,
            ),
            (
                "world exit",
                "WORLD_EXIT_VISUAL",
                "WORLD_EXIT",
                "runtime:exit",
                ReconciledState.WORLD_EXIT,
            ),
            (
                "trusted conflict",
                "LOGIN_SCREEN",
                "IN_GAME",
                "runtime:conflict",
                ReconciledState.CONFLICT,
            ),
        )

        for name, visual_state, runtime_state, runtime_ref, expected in cases:
            with self.subTest(name=name):
                runtime = _runtime(
                    runtime_state,
                    RuntimeEvidenceClass.REVIEWED_CAUSAL,
                    (runtime_ref,),
                )
                context = _trusted_context(runtime)
                self.assertIsNotNone(context, "trusted reconciliation context API is missing")
                result = _trusted_reconcile(
                    _visual(visual_state, evidence_ref="capture:current"),
                    runtime,
                    context,
                )
                self.assertIs(result.state, expected)
                self.assertEqual(result.visual_evidence_refs, ("capture:current",))
                self.assertEqual(result.runtime_evidence_refs, (runtime_ref,))

    def test_untrusted_runtime_disagreement_cannot_create_conflict(self):
        result = reconcile_state(
            _visual("LOGIN_SCREEN"),
            _runtime(
                "IN_GAME",
                RuntimeEvidenceClass.REVIEWED_CAUSAL,
                ("runtime:untrusted-conflict",),
            ),
        )

        self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_plan_example_visual_in_game_never_confirms_without_reviewed_runtime(self):
        visual = VisionObservation(
            screen_class="IN_GAME_VISUAL",
            visible_text=(),
            confidence=None,
            model_profile_id="test-profile",
            evidence_ref="fixture",
            capture_sha256="a" * 64,
        )

        result = reconcile_state(
            visual=visual,
            runtime=RuntimeObservation("UNKNOWN", RuntimeEvidenceClass.UNKNOWN, ()),
        )

        self.assertIsNot(result.state, ReconciledState.WORLD_CONFIRMED)
        self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_reconciliation_matrix_is_exact_and_case_sensitive(self):
        cases = (
            ("normalized visual world plus reviewed runtime", "WORLD_VISUAL", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.WORLD_CONFIRMED),
            ("Task 5 raw visual world is normalized", "IN_GAME_VISUAL", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.WORLD_CONFIRMED),
            ("reviewed runtime can establish world with an unknown visual", "UNKNOWN", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.WORLD_CONFIRMED),
            ("structural runtime cannot confirm", "WORLD_VISUAL", "IN_GAME", RuntimeEvidenceClass.STRUCTURAL_ONLY, ("runtime:structural",), ReconciledState.UNKNOWN),
            ("unknown runtime cannot confirm", "WORLD_VISUAL", "IN_GAME", RuntimeEvidenceClass.UNKNOWN, ("runtime:unknown",), ReconciledState.UNKNOWN),
            ("unknown runtime state cannot confirm", "WORLD_VISUAL", "UNKNOWN", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:unknown",), ReconciledState.UNKNOWN),
            ("lowercase runtime state is rejected", "WORLD_VISUAL", "in_game", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.UNKNOWN),
            ("runtime whitespace is rejected", "WORLD_VISUAL", " IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.UNKNOWN),
            ("login visual conflicts with reviewed world", "LOGIN_SCREEN", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.CONFLICT),
            ("character visual conflicts with reviewed world", "CHARACTER_SELECT", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.CONFLICT),
            ("login remains visual-only without runtime evidence", "LOGIN_SCREEN", "UNKNOWN", RuntimeEvidenceClass.UNKNOWN, (), ReconciledState.LOGIN_SCREEN),
            ("character remains visual-only without runtime evidence", "CHARACTER_SELECT", "UNKNOWN", RuntimeEvidenceClass.UNKNOWN, (), ReconciledState.CHARACTER_SELECT),
            ("error visual never corroborates runtime world", "ERROR_SCREEN", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.UNKNOWN),
            ("world exit needs reviewed causal runtime", "WORLD_EXIT_VISUAL", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:exit",), ReconciledState.WORLD_EXIT),
            ("Task 5 raw world exit is normalized", "WORLD_EXIT", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:exit",), ReconciledState.WORLD_EXIT),
            ("visual exit alone is inconclusive", "WORLD_EXIT_VISUAL", "UNKNOWN", RuntimeEvidenceClass.UNKNOWN, (), ReconciledState.UNKNOWN),
            ("structural exit cannot confirm", "WORLD_EXIT_VISUAL", "WORLD_EXIT", RuntimeEvidenceClass.STRUCTURAL_ONLY, ("runtime:exit",), ReconciledState.UNKNOWN),
            ("reviewed exit conflicts with world visual", "WORLD_VISUAL", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:exit",), ReconciledState.CONFLICT),
            ("reviewed exit conflicts with login", "LOGIN_SCREEN", "WORLD_EXIT", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:exit",), ReconciledState.CONFLICT),
            ("lowercase visual state is rejected", "world_visual", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.UNKNOWN),
            ("visual whitespace is rejected", " WORLD_VISUAL", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.UNKNOWN),
            ("unknown visual state is rejected", "SOMETHING_ELSE", "IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",), ReconciledState.UNKNOWN),
            ("explicit stale runtime state is inconclusive", "WORLD_VISUAL", "STALE", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:stale",), ReconciledState.UNKNOWN),
        )

        for name, visual_state, runtime_state, evidence_class, refs, expected in cases:
            with self.subTest(name=name):
                runtime = _runtime(runtime_state, evidence_class, refs)
                context = (
                    _trusted_context(runtime)
                    if evidence_class is RuntimeEvidenceClass.REVIEWED_CAUSAL
                    else None
                )
                result = (
                    _trusted_reconcile(
                        _visual(visual_state),
                        runtime,
                        context,
                    )
                    if context is not None
                    else reconcile_state(_visual(visual_state), runtime)
                )
                self.assertIs(result.state, expected)

    def test_full_runtime_evidence_matrix_never_promotes_without_reviewed_causal_in_game(self):
        visual_states = (
            "UNKNOWN",
            "LOGIN_SCREEN",
            "CHARACTER_SELECT",
            "WORLD_VISUAL",
            "WORLD_EXIT_VISUAL",
            "ERROR_SCREEN",
        )
        runtime_states = ("UNKNOWN", "IN_GAME", "WORLD_EXIT")
        classes = tuple(RuntimeEvidenceClass)

        for visual_state in visual_states:
            for runtime_state in runtime_states:
                for evidence_class in classes:
                    with self.subTest(
                        visual_state=visual_state,
                        runtime_state=runtime_state,
                        evidence_class=evidence_class,
                    ):
                        runtime = _runtime(
                            runtime_state,
                            evidence_class,
                            ("runtime:matrix",),
                        )
                        context = (
                            _trusted_context(runtime)
                            if evidence_class is RuntimeEvidenceClass.REVIEWED_CAUSAL
                            else None
                        )
                        result = (
                            _trusted_reconcile(
                                _visual(visual_state),
                                runtime,
                                context,
                            )
                            if context is not None
                            else reconcile_state(_visual(visual_state), runtime)
                        )
                        if result.state is ReconciledState.WORLD_CONFIRMED:
                            self.assertEqual(runtime_state, "IN_GAME")
                            self.assertIs(evidence_class, RuntimeEvidenceClass.REVIEWED_CAUSAL)
                            self.assertIn(visual_state, {"UNKNOWN", "WORLD_VISUAL"})
                        if runtime_state != "IN_GAME" or evidence_class is not RuntimeEvidenceClass.REVIEWED_CAUSAL:
                            self.assertIsNot(result.state, ReconciledState.WORLD_CONFIRMED)

    def test_missing_or_invalid_evidence_fails_closed_without_echoing_values(self):
        secret = "SENTINEL_UNTRUSTED_RECONCILIATION_REF"
        cases = (
            ("missing visual ref", _visual(evidence_ref=""), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))),
            ("invalid visual ref", _visual(evidence_ref=f"../{secret}"), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))),
            ("invalid visual digest", _visual(capture_sha256="A" * 64), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))),
            ("missing runtime refs", _visual(), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ())),
            ("invalid runtime ref", _visual(), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, (f"../{secret}",))),
            ("runtime refs must be a tuple", _visual(), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ["runtime:world"])),
            ("runtime class must be exact", _visual(), _runtime("IN_GAME", "REVIEWED_CAUSAL", ("runtime:world",))),
            ("visual must remain visual only", _visual(visual_only=False), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))),
            ("visual structural authority is rejected", _visual(structural_authority=True), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))),
            ("invalid profile ref", _visual(model_profile_id=f"../{secret}"), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))),
        )

        for name, visual, runtime in cases:
            with self.subTest(name=name):
                result = _trusted_reconcile(
                    visual,
                    runtime,
                    _trusted_context(runtime),
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)
                self.assertNotIn(secret, repr(result))

    def test_secret_shaped_provenance_is_dropped_without_an_outward_leak(self):
        sentinel = "OPENAI_API_KEY=sentinel_reconciliation_secret"
        cases = (
            ("visual ref", _visual(evidence_ref=sentinel), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))),
            ("runtime ref", _visual(), _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, (sentinel,))),
        )

        for name, visual, runtime in cases:
            with self.subTest(name=name):
                result = _trusted_reconcile(
                    visual,
                    runtime,
                    _trusted_context(runtime),
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)
                self.assertEqual(result.visual_evidence_refs, ())
                self.assertEqual(result.runtime_evidence_refs, ())
                self.assertNotIn(sentinel, repr(result))
                self.assertNotIn(sentinel, str(result))

    def test_complete_task5_visual_contract_is_required_before_all_table_rules(self):
        oversized_text = "x" * 4097
        cases = (
            ("mutable visible text", {"visible_text": ["safe"]}),
            ("tuple subclass visible text", {"visible_text": _TupleSubclass(("safe",))}),
            ("string subclass visible text", {"visible_text": (_StringSubclass("safe"),)}),
            ("surrogate visible text", {"visible_text": ("bad\ud800",)}),
            ("too many visible strings", {"visible_text": tuple("safe" for _ in range(257))}),
            ("oversized visible string", {"visible_text": (oversized_text,)}),
            ("nan confidence", {"confidence": float("nan")}),
            ("infinite confidence", {"confidence": float("inf")}),
            ("confidence below range", {"confidence": -0.01}),
            ("confidence above range", {"confidence": 1.01}),
            ("integer confidence", {"confidence": 1}),
            ("unreviewed profile", {"model_profile_id": "ollama:unreviewed@sha256:" + "b" * 64}),
            ("profile string subclass", {"model_profile_id": _StringSubclass(QWEN_VISION_PROFILE_ID)}),
            ("capture string subclass", {"capture_sha256": _StringSubclass("a" * 64)}),
            ("evidence ref string subclass", {"evidence_ref": _StringSubclass("capture:fixture")}),
        )

        for name, kwargs in cases:
            with self.subTest(name=name):
                runtime = _runtime(
                    "IN_GAME",
                    RuntimeEvidenceClass.REVIEWED_CAUSAL,
                    ("runtime:world",),
                )
                result = _trusted_reconcile(
                    _visual("WORLD_VISUAL", **kwargs),
                    runtime,
                    _trusted_context(runtime),
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)
                self.assertEqual(result.visual_evidence_refs, ())
                self.assertEqual(result.runtime_evidence_refs, ())

    def test_admitted_task5_confidence_forms_remain_reconcilable(self):
        for confidence in (None, 0.0, 0.5, 1.0):
            with self.subTest(confidence=confidence):
                runtime = _runtime(
                    "IN_GAME",
                    RuntimeEvidenceClass.REVIEWED_CAUSAL,
                    ("runtime:world",),
                )
                result = _trusted_reconcile(
                    _visual("WORLD_VISUAL", confidence=confidence),
                    runtime,
                    _trusted_context(runtime),
                )
                self.assertIs(result.state, ReconciledState.WORLD_CONFIRMED)

    def test_malformed_visual_never_emits_visual_state_without_runtime_evidence(self):
        for screen_class in ("LOGIN_SCREEN", "CHARACTER_SELECT", "WORLD_VISUAL"):
            with self.subTest(screen_class=screen_class):
                result = reconcile_state(
                    _visual(screen_class, visible_text=["mutable"]),
                    _runtime("UNKNOWN", RuntimeEvidenceClass.UNKNOWN, ()),
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)
                self.assertEqual(result.visual_evidence_refs, ())
                self.assertEqual(result.runtime_evidence_refs, ())

    def test_result_retains_immutable_visual_and_runtime_provenance(self):
        runtime = _runtime(
            "IN_GAME",
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
            ("runtime:one", "runtime:two"),
        )
        result = _trusted_reconcile(
            _visual(evidence_ref="capture:one"),
            runtime,
            _trusted_context(runtime),
        )

        self.assertIs(result.state, ReconciledState.WORLD_CONFIRMED)
        self.assertEqual(result.visual_evidence_refs, ("capture:one",))
        self.assertEqual(result.runtime_evidence_refs, ("runtime:one", "runtime:two"))
        with self.assertRaises(FrozenInstanceError):
            result.state = ReconciledState.UNKNOWN  # type: ignore[misc]
        with self.assertRaises(AttributeError):
            result.runtime_evidence_refs.append("runtime:three")  # type: ignore[attr-defined]

    def test_observation_contract_is_frozen(self):
        runtime = _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))
        self.assertEqual(
            tuple(field.name for field in fields(RuntimeObservation)),
            ("state", "evidence_class", "evidence_refs"),
        )
        with self.assertRaises(FrozenInstanceError):
            runtime.state = "UNKNOWN"  # type: ignore[misc]

    def test_resolver_state_records_are_immutable_but_not_issuance(self):
        runtime = _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",))
        context = _trusted_context(runtime)
        with self.assertRaises(FrozenInstanceError):
            context.current_run_id = "run-forged"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            context.runtime_evidence.observed_monotonic_ns = 1_000  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            context.reviewed_producers[0].contract_id = "forged"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
