from __future__ import annotations

import ast
import unittest
from pathlib import Path

from tools.tibia_re_control_center.model import (
    ActionRequest,
    AdapterIdentity,
    AdapterKind,
    Authority,
    DispatchFence,
    EffectBound,
    Freshness,
    RuntimeStatus,
    ValidationError,
)
from tools.tibia_re_control_center.official_adapter_contract import (
    CURRENT_AUTHORITATIVE_RECONCILIATION_REQUIRED,
    NO_ACTION_CANDIDATE_READY,
    OFFICIAL_RUNTIME_NOT_ADMITTED,
    OfficialTibiaAdapterContract,
    first_slice_recommendation,
    official_action_readiness,
)
from tools.tibia_re_control_center.scenario import (
    ACTION_KINDS,
    action_request_hash,
    default_effect_bound,
    validate_action_parameters,
)


def official_identity(**overrides: object) -> AdapterIdentity:
    values: dict[str, object] = {
        "adapter_id": "official-prep",
        "adapter_kind": AdapterKind.OFFICIAL_TIBIA,
        "adapter_version": "prep-1",
        "adapter_generation": "static-prep-generation",
        "runtime_instance_id": None,
        "session_epoch": None,
    }
    values.update(overrides)
    return AdapterIdentity(**values)  # type: ignore[arg-type]


def move_request(*, effect_bound: EffectBound | None = None, kind: str = "move", parameters: dict | None = None) -> ActionRequest:
    params = parameters if parameters is not None else {"direction": "NORTH", "tiles": 1}
    if kind in ACTION_KINDS:
        normalized = validate_action_parameters(kind, params)
        bound = effect_bound or default_effect_bound(kind, normalized)
    else:
        normalized = params
        bound = effect_bound or EffectBound(max_actions=1)
    request_hash = action_request_hash(
        schema_version=1,
        run_id="d-prep-run",
        step_id="d-prep-step",
        attempt_index=0,
        kind=kind,
        parameters=normalized,
        timeout_ms=1000,
        required_capability=kind,
        required_authority=Authority.MUTATION,
    )
    return ActionRequest(
        action_id="d-prep-action",
        run_id="d-prep-run",
        step_id="d-prep-step",
        attempt_index=0,
        kind=kind,
        parameters=normalized,
        timeout_ms=1000,
        required_capability=kind,
        required_authority=Authority.MUTATION,
        dispatch_fence=DispatchFence(
            expected_backend_epoch="backend-prep",
            expected_control_generation=1,
            expected_adapter_generation="static-prep-generation",
            expected_runtime_instance_id=None,
            expected_session_epoch=None,
        ),
        effect_bound=bound,
        action_request_hash=request_hash,
    )


class PackageDPrepContractTests(unittest.TestCase):
    def test_action_matrix_covers_exact_current_scenario_v1_actions(self):
        rows = official_action_readiness()
        self.assertEqual(set(ACTION_KINDS), {row.action_kind for row in rows})
        self.assertEqual(len(ACTION_KINDS), len(rows))

    def test_action_matrix_does_not_invent_current_track_a_grades(self):
        rows = official_action_readiness()
        self.assertTrue(rows)
        for row in rows:
            with self.subTest(action=row.action_kind):
                self.assertEqual("UNKNOWN", row.current_read_gate)
                self.assertEqual("UNKNOWN", row.current_action_gate)
                self.assertFalse(row.recommended_for_first_real_slice)
                self.assertTrue(row.raw_transport_hidden)
                self.assertTrue(row.finite_effect_bound_available)
                self.assertEqual(
                    CURRENT_AUTHORITATIVE_RECONCILIATION_REQUIRED,
                    row.confirmation_source,
                )
                self.assertEqual("unknown", row.reference_ui_path_known)
                self.assertEqual("UNKNOWN", row.required_gui_input_lock)
                self.assertTrue(row.open_gaps)

    def test_no_first_slice_is_recommended_without_current_runtime_evidence(self):
        self.assertEqual(NO_ACTION_CANDIDATE_READY, first_slice_recommendation())
        self.assertFalse(any(row.recommended_for_first_real_slice for row in official_action_readiness()))

    def test_adapter_identity_is_typed_but_grants_no_capability(self):
        adapter = OfficialTibiaAdapterContract(official_identity())
        self.assertEqual(AdapterKind.OFFICIAL_TIBIA, adapter.identity().adapter_kind)
        capabilities = adapter.capabilities()
        self.assertEqual(set(ACTION_KINDS), {cap.capability_id for cap in capabilities})
        self.assertTrue(all(not cap.read_supported for cap in capabilities))
        self.assertTrue(all(not cap.action_supported for cap in capabilities))

    def test_non_official_identity_is_rejected(self):
        identity = AdapterIdentity(
            adapter_id="fake",
            adapter_kind=AdapterKind.FAKE_TEST,
            adapter_version="1",
            adapter_generation="fake-generation",
        )
        with self.assertRaises(ValidationError) as caught:
            OfficialTibiaAdapterContract(identity)
        self.assertEqual("OFFICIAL_ADAPTER_IDENTITY_REQUIRED", caught.exception.code)

    def test_runtime_status_is_closed_and_unknown(self):
        adapter = OfficialTibiaAdapterContract(
            official_identity(runtime_instance_id="diagnostic-runtime", session_epoch="diagnostic-session")
        )
        status = adapter.runtime_status()
        self.assertEqual("UNKNOWN", status.runtime_state)
        self.assertEqual("UNKNOWN", status.client_state)
        self.assertEqual("NOT_ADMITTED", status.authority_state)
        self.assertEqual(Freshness.UNKNOWN, status.freshness)
        self.assertIn(OFFICIAL_RUNTIME_NOT_ADMITTED, status.reasons)

    def test_semantic_mapping_exposes_no_raw_transport_or_runtime_handle(self):
        adapter = OfficialTibiaAdapterContract(official_identity())
        mapping = adapter.map_action(move_request())
        self.assertEqual("move", mapping.action_kind)
        self.assertEqual("move", mapping.required_capability)
        self.assertEqual(Authority.MUTATION, mapping.required_authority)
        self.assertEqual(default_effect_bound("move", {"direction": "NORTH", "tiles": 1}), mapping.effect_bound)
        self.assertTrue(mapping.raw_transport_hidden)
        self.assertEqual(CURRENT_AUTHORITATIVE_RECONCILIATION_REQUIRED, mapping.confirmation_source)
        exposed = vars(mapping)
        forbidden = {
            "key",
            "keys",
            "coordinate",
            "coordinates",
            "opcode",
            "address",
            "pointer",
            "pid",
            "process_id",
            "bridge_handle",
            "window",
            "display",
            "lease_token",
            "credential",
            "password",
            "session_secret",
        }
        self.assertTrue(forbidden.isdisjoint(exposed))
        self.assertNotIn("parameters", exposed)

    def test_mapping_revalidates_scenario_parameters_and_effect_bound(self):
        adapter = OfficialTibiaAdapterContract(official_identity())
        with self.assertRaises(ValidationError) as invalid_kind:
            adapter.map_action(move_request(kind="raw_key", parameters={"key": "W"}))
        self.assertEqual("UNSUPPORTED_ACTION_KIND", invalid_kind.exception.code)

        mismatched = move_request(effect_bound=EffectBound(max_actions=0))
        with self.assertRaises(ValidationError) as invalid_bound:
            adapter.map_action(mismatched)
        self.assertEqual("EFFECT_BOUND_MISMATCH", invalid_bound.exception.code)

    def test_optimistic_reported_status_cannot_enable_preflight(self):
        adapter = OfficialTibiaAdapterContract(official_identity())
        optimistic = RuntimeStatus(
            adapter_id="official-prep",
            adapter_generation="static-prep-generation",
            runtime_state="ONLINE",
            client_state="IN_GAME",
            authority_state="MUTATION_ALLOWED",
            freshness=Freshness.FRESH,
        )
        result = adapter.preflight(move_request(), observed_status=optimistic)
        self.assertFalse(result.admitted)
        self.assertEqual(OFFICIAL_RUNTIME_NOT_ADMITTED, result.reason_code)
        self.assertEqual("move", result.mapping.action_kind)

    def test_execute_refuses_deterministically_even_after_optimistic_preflight_input(self):
        adapter = OfficialTibiaAdapterContract(official_identity())
        request = move_request()
        optimistic = RuntimeStatus(
            adapter_id="official-prep",
            adapter_generation="static-prep-generation",
            runtime_state="ONLINE",
            client_state="IN_GAME",
            authority_state="MUTATION_ALLOWED",
            freshness=Freshness.FRESH,
        )
        self.assertFalse(adapter.preflight(request, observed_status=optimistic).admitted)
        with self.assertRaises(ValidationError) as caught:
            adapter.execute(request)
        self.assertEqual(OFFICIAL_RUNTIME_NOT_ADMITTED, caught.exception.code)

    def test_hard_disabled_skeleton_has_no_coordinator_physical_dispatch_surface(self):
        adapter = OfficialTibiaAdapterContract(official_identity())
        for name in (
            "cross_irreversible_boundary",
            "dispatch_guard",
            "await_authority",
            "emergency_stop",
            "capture_start",
            "capture_stop",
        ):
            self.assertFalse(hasattr(adapter, name), name)

    def test_source_import_graph_contains_no_runtime_or_raw_dispatch_dependency(self):
        path = Path("tools/tibia_re_control_center/official_adapter_contract.py")
        tree = ast.parse(path.read_text(encoding="utf-8"))
        modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
        forbidden_roots = {
            "subprocess",
            "socket",
            "ctypes",
            "docker",
            "pyautogui",
            "pynput",
            "tools.tibia_runtime_bridge",
            "tools.tibia_re_surveyor",
        }
        self.assertTrue(forbidden_roots.isdisjoint(modules), modules)


if __name__ == "__main__":
    unittest.main()
