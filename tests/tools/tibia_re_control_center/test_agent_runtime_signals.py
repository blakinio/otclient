"""Trusted runtime-signal ingestion and provenance tests."""

from __future__ import annotations

import unittest
from dataclasses import fields

from tools.tibia_re_control_center import agent_reconcile as reconcile_module
from tools.tibia_re_control_center.agent_reconcile import (
    ReconciledState,
    RuntimeEvidenceClass,
)
from tools.tibia_re_control_center.agent_runtime_signals import (
    ReviewedRuntimeSignalContract,
    ReviewedRuntimeSignalRule,
    RuntimeSignalBinding,
    RuntimeSignalResolver,
    RuntimeSignalSample,
)
from tools.tibia_re_control_center.agent_vision import (
    QWEN_VISION_PROFILE_ID,
    VisionObservation,
)


class _StringSubclass(str):
    pass


def _binding(**overrides: str) -> RuntimeSignalBinding:
    values = {
        "session_id": "session-current",
        "run_id": "run-current",
        "runtime_id": "runtime-current",
        "runtime_instance_id": "instance-current",
        "runtime_binding_sha256": "b" * 64,
    }
    values.update(overrides)
    return RuntimeSignalBinding(**values)


def _contract(
    *,
    producer_id: str = "fixture-causal-producer",
    contract_id: str = "fixture-causal-v1",
    source_state: str = "WORLD_ENTERED",
    runtime_state: str = "IN_GAME",
    evidence_class: RuntimeEvidenceClass = RuntimeEvidenceClass.REVIEWED_CAUSAL,
) -> ReviewedRuntimeSignalContract:
    return ReviewedRuntimeSignalContract(
        producer_id=producer_id,
        contract_id=contract_id,
        rules=(
            ReviewedRuntimeSignalRule(
                source_state=source_state,
                runtime_state=runtime_state,
                evidence_class=evidence_class,
            ),
        ),
    )


def _resolver(
    *,
    binding: RuntimeSignalBinding | None = None,
    monotonic_ns=lambda: 1_000,
    max_age_ns: int = 100,
    contracts: tuple[ReviewedRuntimeSignalContract, ...] | None = None,
) -> RuntimeSignalResolver:
    return RuntimeSignalResolver(
        current_binding=binding or _binding(),
        reviewed_contracts=contracts or (_contract(),),
        monotonic_ns=monotonic_ns,
        max_age_ns=max_age_ns,
        clock_domain_id="clock:control-center",
    )


def _sample(
    *,
    binding: RuntimeSignalBinding | None = None,
    observed_monotonic_ns: int = 950,
    source_state: str = "WORLD_ENTERED",
    evidence_refs: tuple[str, ...] = ("producer:evidence-current",),
) -> RuntimeSignalSample:
    return RuntimeSignalSample(
        binding=binding or _binding(),
        clock_domain_id="clock:control-center",
        observed_monotonic_ns=observed_monotonic_ns,
        source_state=source_state,
        evidence_refs=evidence_refs,
    )


def _visual(screen_class: str = "WORLD_VISUAL") -> VisionObservation:
    return VisionObservation(
        screen_class=screen_class,
        visible_text=(),
        confidence=None,
        model_profile_id=QWEN_VISION_PROFILE_ID,
        evidence_ref="capture:fixture",
        capture_sha256="a" * 64,
        visual_only=True,
        structural_authority=False,
    )


class RuntimeSignalTests(unittest.TestCase):
    def test_binding_requires_exact_runtime_admission_hash(self):
        try:
            binding = RuntimeSignalBinding(
                session_id="session-current",
                run_id="run-current",
                runtime_id="runtime-current",
                runtime_instance_id="instance-current",
                runtime_binding_sha256="b" * 64,
            )
        except TypeError as exc:
            self.fail(f"runtime admission binding hash missing: {exc}")
        self.assertEqual(binding.runtime_binding_sha256, "b" * 64)

    def test_current_reviewed_signal_is_bound_to_current_context(self):
        resolver = _resolver()
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )
        evidence = resolver.ingest(source, _sample())

        self.assertIsNotNone(evidence)
        self.assertEqual(evidence.observation.state, "IN_GAME")
        self.assertIs(
            evidence.observation.evidence_class,
            RuntimeEvidenceClass.REVIEWED_CAUSAL,
        )
        self.assertEqual(
            resolver.resolve_current_reviewed(evidence.observation),
            evidence.observation,
        )
        self.assertEqual(len(evidence.observation.evidence_refs), 1)
        self.assertTrue(evidence.observation.evidence_refs[0].startswith("runtime-signal:"))
        self.assertNotIn("producer:evidence-current", evidence.observation.evidence_refs)

    def test_runtime_signal_payload_has_no_semantic_or_provenance_authority_fields(self):
        self.assertEqual(
            tuple(field.name for field in fields(RuntimeSignalSample)),
            (
                "binding",
                "clock_domain_id",
                "observed_monotonic_ns",
                "source_state",
                "evidence_refs",
            ),
        )
        with self.assertRaises(TypeError):
            RuntimeSignalSample(
                binding=_binding(),
                clock_domain_id="clock:control-center",
                observed_monotonic_ns=950,
                source_state="WORLD_ENTERED",
                evidence_refs=("producer:evidence-current",),
                runtime_state="IN_GAME",  # type: ignore[call-arg]
            )

    def test_current_causal_resolver_composes_with_existing_reconciler(self):
        resolver = _resolver()
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )
        evidence = resolver.ingest(source, _sample())
        self.assertIsNotNone(evidence)
        reconciler = reconcile_module._compose_trusted_reconciler(resolver)

        result = reconciler.reconcile_state(_visual(), evidence.observation)

        self.assertIs(result.state, ReconciledState.WORLD_CONFIRMED)
        self.assertEqual(result.runtime_evidence_refs, evidence.observation.evidence_refs)

    def test_structural_runtime_signal_cannot_assert_semantic_world_state(self):
        for runtime_state in ("IN_GAME", "WORLD_EXIT"):
            contract = _contract(
                runtime_state=runtime_state,
                evidence_class=RuntimeEvidenceClass.STRUCTURAL_ONLY,
            )
            with self.subTest(runtime_state=runtime_state), self.assertRaises(ValueError):
                _resolver(contracts=(contract,))

    def test_structural_unknown_signal_stays_semantically_unknown(self):
        contract = _contract(
            runtime_state="UNKNOWN",
            evidence_class=RuntimeEvidenceClass.STRUCTURAL_ONLY,
        )
        resolver = _resolver(contracts=(contract,))
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )
        evidence = resolver.ingest(source, _sample())
        self.assertIsNotNone(evidence)
        reconciler = reconcile_module._compose_trusted_reconciler(resolver)

        result = reconciler.reconcile_state(_visual(), evidence.observation)

        self.assertEqual(evidence.observation.state, "UNKNOWN")
        self.assertIs(result.state, ReconciledState.UNKNOWN)

    def test_stale_signal_is_rejected_and_current_evidence_ages_out(self):
        clock = [1_000]
        resolver = _resolver(monotonic_ns=lambda: clock[0])
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )

        self.assertIsNone(
            resolver.ingest(source, _sample(observed_monotonic_ns=899))
        )
        evidence = resolver.ingest(source, _sample(observed_monotonic_ns=950))
        self.assertIsNotNone(evidence)
        clock[0] = 1_051
        self.assertIsNone(resolver.resolve_current_reviewed(evidence.observation))

    def test_foreign_session_run_runtime_or_instance_is_rejected(self):
        resolver = _resolver()
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )
        foreign_bindings = (
            _binding(session_id="session-other"),
            _binding(run_id="run-other"),
            _binding(runtime_id="runtime-other"),
            _binding(runtime_instance_id="instance-other"),
            _binding(runtime_binding_sha256="c" * 64),
        )

        for binding in foreign_bindings:
            with self.subTest(binding=binding):
                self.assertIsNone(resolver.ingest(source, _sample(binding=binding)))

    def test_reviewed_source_binding_requires_exact_safe_identifiers(self):
        resolver = _resolver()
        with self.assertRaises(ValueError):
            resolver.bind_reviewed_source(
                producer_id=_StringSubclass("fixture-causal-producer"),
                contract_id="fixture-causal-v1",
            )
        with self.assertRaises(ValueError):
            resolver.bind_reviewed_source(
                producer_id="fixture-causal-producer",
                contract_id=_StringSubclass("fixture-causal-v1"),
            )

    def test_reviewed_source_handle_is_resolver_owned(self):
        resolver = _resolver()
        other = _resolver()
        foreign_source = other.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )

        self.assertIsNone(resolver.ingest(foreign_source, _sample()))
        with self.assertRaises(ValueError):
            resolver.bind_reviewed_source(
                producer_id="unreviewed-producer",
                contract_id="unreviewed-v1",
            )

    def test_invalid_trusted_binding_is_rejected_at_composition(self):
        for field in (
            "session_id",
            "run_id",
            "runtime_id",
            "runtime_instance_id",
            "runtime_binding_sha256",
        ):
            with self.subTest(field=field), self.assertRaises(ValueError):
                _resolver(binding=_binding(**{field: ""}))

    def test_reviewed_contract_rules_are_unambiguous_and_semantic_bounded(self):
        duplicate_rule_contract = ReviewedRuntimeSignalContract(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
            rules=(
                ReviewedRuntimeSignalRule(
                    source_state="WORLD_ENTERED",
                    runtime_state="IN_GAME",
                    evidence_class=RuntimeEvidenceClass.REVIEWED_CAUSAL,
                ),
                ReviewedRuntimeSignalRule(
                    source_state="WORLD_ENTERED",
                    runtime_state="WORLD_EXIT",
                    evidence_class=RuntimeEvidenceClass.REVIEWED_CAUSAL,
                ),
            ),
        )
        invalid_runtime_state = _contract(runtime_state="WORLD_VISUAL")
        invalid_evidence_class = ReviewedRuntimeSignalContract(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
            rules=(
                ReviewedRuntimeSignalRule(
                    source_state="WORLD_ENTERED",
                    runtime_state="IN_GAME",
                    evidence_class="REVIEWED_CAUSAL",  # type: ignore[arg-type]
                ),
            ),
        )

        for contract in (
            duplicate_rule_contract,
            invalid_runtime_state,
            invalid_evidence_class,
        ):
            with self.subTest(contract=contract), self.assertRaises(ValueError):
                _resolver(contracts=(contract,))

    def test_source_evidence_reference_count_is_bounded(self):
        resolver = _resolver()
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )
        refs = tuple(f"producer:ref-{index}" for index in range(33))

        self.assertIsNone(resolver.ingest(source, _sample(evidence_refs=refs)))

    def test_secret_or_malformed_source_evidence_is_rejected_without_retention(self):
        resolver = _resolver()
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )
        cases = (
            _sample(evidence_refs=("OPENAI_API_KEY=sentinel_runtime_signal_secret",)),
            RuntimeSignalSample(
                binding=_binding(),
                clock_domain_id="clock:control-center",
                observed_monotonic_ns=950,
                source_state="WORLD_ENTERED",
                evidence_refs=["producer:not-a-tuple"],  # type: ignore[arg-type]
            ),
            _sample(evidence_refs=("../unsafe-ref",)),
        )

        for sample in cases:
            with self.subTest(sample=sample):
                result = resolver.ingest(source, sample)
                self.assertIsNone(result)
                self.assertNotIn("sentinel_runtime_signal_secret", repr(resolver))

    def test_reviewed_causal_signal_requires_source_provenance_reference(self):
        resolver = _resolver()
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )

        self.assertIsNone(resolver.ingest(source, _sample(evidence_refs=())))

    def test_freshness_requires_the_same_trusted_clock_domain(self):
        try:
            resolver = RuntimeSignalResolver(
                current_binding=_binding(),
                reviewed_contracts=(_contract(),),
                monotonic_ns=lambda: 1_000,
                max_age_ns=100,
                clock_domain_id="clock:control-center",
            )
            matching = RuntimeSignalSample(
                binding=_binding(),
                observed_monotonic_ns=950,
                source_state="WORLD_ENTERED",
                evidence_refs=("producer:matching-clock",),
                clock_domain_id="clock:control-center",
            )
            foreign = RuntimeSignalSample(
                binding=_binding(),
                observed_monotonic_ns=950,
                source_state="WORLD_ENTERED",
                evidence_refs=("producer:foreign-clock",),
                clock_domain_id="clock:runtime-edge",
            )
        except TypeError as exc:
            self.fail(f"runtime signal clock-domain binding missing: {exc}")
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )

        self.assertIsNotNone(resolver.ingest(source, matching))
        self.assertIsNone(resolver.ingest(source, foreign))

    def test_clock_failure_fails_closed_instead_of_promoting_runtime_state(self):
        def broken_clock():
            raise RuntimeError("clock unavailable")

        resolver = _resolver(monotonic_ns=broken_clock)
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )

        self.assertIsNone(resolver.ingest(source, _sample()))

    def test_programming_clock_failure_is_not_silently_downgraded(self):
        def broken_clock():
            raise AssertionError("programming defect")

        resolver = _resolver(monotonic_ns=broken_clock)
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )

        with self.assertRaises(AssertionError):
            resolver.ingest(source, _sample())

    def test_non_callable_clock_is_a_composition_type_error(self):
        with self.assertRaises(TypeError):
            RuntimeSignalResolver(
                current_binding=_binding(),
                reviewed_contracts=(_contract(),),
                monotonic_ns=object(),  # type: ignore[arg-type]
                max_age_ns=100,
                clock_domain_id="clock:control-center",
            )

    def test_newer_signal_supersedes_older_signal_from_same_reviewed_source(self):
        contract = ReviewedRuntimeSignalContract(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
            rules=(
                ReviewedRuntimeSignalRule(
                    source_state="WORLD_ENTERED",
                    runtime_state="IN_GAME",
                    evidence_class=RuntimeEvidenceClass.REVIEWED_CAUSAL,
                ),
                ReviewedRuntimeSignalRule(
                    source_state="WORLD_EXITED",
                    runtime_state="WORLD_EXIT",
                    evidence_class=RuntimeEvidenceClass.REVIEWED_CAUSAL,
                ),
            ),
        )
        resolver = _resolver(contracts=(contract,))
        source = resolver.bind_reviewed_source(
            producer_id="fixture-causal-producer",
            contract_id="fixture-causal-v1",
        )
        entered = resolver.ingest(
            source,
            _sample(observed_monotonic_ns=950, source_state="WORLD_ENTERED"),
        )
        exited = resolver.ingest(
            source,
            _sample(
                observed_monotonic_ns=960,
                source_state="WORLD_EXITED",
                evidence_refs=("producer:evidence-exit",),
            ),
        )

        self.assertIsNotNone(entered)
        self.assertIsNotNone(exited)
        self.assertIsNone(resolver.resolve_current_reviewed(entered.observation))
        self.assertEqual(
            resolver.resolve_current_reviewed(exited.observation),
            exited.observation,
        )
        self.assertIsNone(
            resolver.ingest(
                source,
                _sample(
                    observed_monotonic_ns=955,
                    source_state="WORLD_ENTERED",
                    evidence_refs=("producer:evidence-out-of-order",),
                ),
            )
        )

    def test_conflicting_current_causal_producers_fail_closed_as_ambiguous(self):
        entered_contract = _contract(
            producer_id="fixture-entered", contract_id="entered-v1"
        )
        exited_contract = _contract(
            producer_id="fixture-exited",
            contract_id="exited-v1",
            source_state="WORLD_EXITED",
            runtime_state="WORLD_EXIT",
        )
        resolver = _resolver(contracts=(entered_contract, exited_contract))
        entered_source = resolver.bind_reviewed_source(
            producer_id="fixture-entered", contract_id="entered-v1"
        )
        exited_source = resolver.bind_reviewed_source(
            producer_id="fixture-exited", contract_id="exited-v1"
        )
        entered = resolver.ingest(
            entered_source,
            _sample(evidence_refs=("producer:entered",)),
        )
        exited = resolver.ingest(
            exited_source,
            _sample(
                observed_monotonic_ns=960,
                source_state="WORLD_EXITED",
                evidence_refs=("producer:exited",),
            ),
        )

        self.assertIsNotNone(entered)
        self.assertIsNotNone(exited)
        self.assertIsNone(resolver.resolve_current_reviewed(entered.observation))
        self.assertIsNone(resolver.resolve_current_reviewed(exited.observation))


if __name__ == "__main__":
    unittest.main()
