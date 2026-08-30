"""Deterministic, authority-neutral visual/runtime reconciliation tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
import unittest

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


class ReconciliationTests(unittest.TestCase):
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
                result = reconcile_state(_visual(visual_state), _runtime(runtime_state, evidence_class, refs))
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
                        result = reconcile_state(
                            _visual(visual_state),
                            _runtime(runtime_state, evidence_class, ("runtime:matrix",)),
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
                result = reconcile_state(visual, runtime)
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
                result = reconcile_state(visual, runtime)
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
                result = reconcile_state(
                    _visual("WORLD_VISUAL", **kwargs),
                    _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",)),
                )
                self.assertIs(result.state, ReconciledState.UNKNOWN)
                self.assertEqual(result.visual_evidence_refs, ())
                self.assertEqual(result.runtime_evidence_refs, ())

    def test_admitted_task5_confidence_forms_remain_reconcilable(self):
        for confidence in (None, 0.0, 0.5, 1.0):
            with self.subTest(confidence=confidence):
                result = reconcile_state(
                    _visual("WORLD_VISUAL", confidence=confidence),
                    _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:world",)),
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
        result = reconcile_state(
            _visual(evidence_ref="capture:one"),
            _runtime("IN_GAME", RuntimeEvidenceClass.REVIEWED_CAUSAL, ("runtime:one", "runtime:two")),
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
        with self.assertRaises(FrozenInstanceError):
            runtime.state = "UNKNOWN"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
