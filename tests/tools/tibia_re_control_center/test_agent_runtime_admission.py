import importlib
import re
import unittest

from tools.tibia_re_control_center.current_client_fence import current_client_fence
from tools.tibia_re_control_center.model import ValidationError

TASK_ID = "OTC-20260901-vision-p2-runtime-admission"
_CURRENT_CLIENT_FENCE = current_client_fence()
CURRENT_CLIENT_VERSION = _CURRENT_CLIENT_FENCE.version
CURRENT_CLIENT_SIZE = _CURRENT_CLIENT_FENCE.size
CURRENT_CLIENT_SHA256 = _CURRENT_CLIENT_FENCE.sha256


def _module():
    try:
        return importlib.import_module("tools.tibia_re_control_center.agent_runtime_admission")
    except ModuleNotFoundError:
        return None


def _exact_observation():
    return {
        "schema": "otclient.local-agent.runtime-observation.v1",
        "track_id": "official-client-re",
        "task_id": TASK_ID,
        "runtime_owner_task": TASK_ID,
        "runtime_namespace": "synology:kasm:otclient-track-a-kasmvnc:display-1",
        "observed_at_epoch_ms": 10_000,
        "locator": {
            "runner": "synology-otclient-01",
            "remote_device": "Synology",
            "container": "otclient-track-a-kasmvnc",
            "container_gui_user": "kasm-user",
            "display": ":1",
            "observer_endpoint": "https://synology:6902/",
            "host_reachable": True,
            "container_running": True,
            "display_reachable": True,
        },
        "process": {
            "boot_id_sha256": "b" * 64,
            "pid": 123,
            "process_start_ticks": 456,
            "exe_path": "/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client",
            "display": ":1",
            "client_version": CURRENT_CLIENT_VERSION,
            "client_size": CURRENT_CLIENT_SIZE,
            "client_sha256": CURRENT_CLIENT_SHA256,
        },
        "window": {
            "xid": 321,
            "pid": 123,
            "display": ":1",
            "ownership_proven": True,
        },
        "inventory": {
            "inventory_scope": "DECLARED_RUNTIME_NAMESPACE",
            "official_client_candidate_count": 1,
            "exact_client_candidate_count": 1,
            "mismatched_or_unverifiable_candidate_count": 0,
            "target_uniqueness": "PROVEN",
        },
        "safety": {
            "credentials_used": False,
            "gui_input_sent": False,
            "anti_idle_input_sent": False,
            "process_control_used": False,
            "process_memory_access_used": False,
            "network_payload_capture_used": False,
            "physical_action_count": 0,
        },
    }


class RuntimeAdmissionTests(unittest.TestCase):
    def test_exact_current_unique_read_only_target_is_admitted_with_typed_binding(self):
        module = _module()
        self.assertIsNotNone(module, "agent_runtime_admission module is not implemented")

        record = module.admit_read_only_runtime(
            _exact_observation(), now_epoch_ms=10_100, max_age_ms=1_000
        )

        self.assertEqual("otclient.local-agent.runtime-admission.v1", record.schema)
        self.assertEqual("read_only", record.runtime_access)
        self.assertEqual(TASK_ID, record.runtime_owner_task)
        self.assertEqual("PROVEN", record.target_uniqueness)
        self.assertFalse(record.mutation_authorized)
        self.assertEqual("NOT_APPLICABLE", record.gate_a)
        self.assertEqual("NOT_APPLICABLE", record.gate_b)
        self.assertRegex(record.runtime_binding_sha256, re.compile(r"^[0-9a-f]{64}$"))

        provenance = record.to_provenance()
        self.assertEqual("otclient.local-agent.runtime-provenance.v1", provenance["schema"])
        self.assertEqual(record.runtime_binding_sha256, provenance["runtime_binding_sha256"])
        self.assertEqual(CURRENT_CLIENT_SHA256, provenance["process"]["client_sha256"])
        self.assertEqual(321, provenance["window"]["xid"])
        self.assertEqual(0, provenance["safety"]["physical_action_count"])
        self.assertFalse(provenance["mutation_authorized"])


    def test_historical_or_mismatched_client_fence_is_refused(self):
        module = _module()
        observation = _exact_observation()
        observation["process"]["client_version"] = "15.32"
        observation["process"]["client_size"] = 52_109_920
        observation["process"]["client_sha256"] = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"

        with self.assertRaises(ValidationError) as caught:
            module.admit_read_only_runtime(
                observation, now_epoch_ms=10_100, max_age_ms=1_000
            )

        self.assertEqual("RUNTIME_FENCE_MISMATCH", caught.exception.code)
        self.assertNotIn(observation["process"]["client_sha256"], str(caught.exception))


    def test_non_unique_or_incomplete_candidate_inventory_is_refused(self):
        module = _module()
        mutations = (
            lambda inventory: inventory.__setitem__("target_uniqueness", "UNKNOWN"),
            lambda inventory: inventory.__setitem__("official_client_candidate_count", 2),
            lambda inventory: inventory.__setitem__("exact_client_candidate_count", 0),
            lambda inventory: inventory.__setitem__("mismatched_or_unverifiable_candidate_count", 1),
            lambda inventory: inventory.__setitem__("inventory_scope", "TARGET_CONTAINER_ONLY"),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                observation = _exact_observation()
                mutate(observation["inventory"])
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual("RUNTIME_TARGET_NOT_UNIQUE", caught.exception.code)


    def test_stale_or_future_observation_cannot_be_admitted(self):
        module = _module()
        cases = (
            (8_000, "RUNTIME_OBSERVATION_STALE"),
            (10_101, "RUNTIME_OBSERVATION_FUTURE"),
        )
        for observed_at, expected_code in cases:
            with self.subTest(observed_at=observed_at):
                observation = _exact_observation()
                observation["observed_at_epoch_ms"] = observed_at
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual(expected_code, caught.exception.code)


    def test_target_owned_by_another_task_is_refused(self):
        module = _module()
        observation = _exact_observation()
        observation["runtime_owner_task"] = "OTC-OTHER-TASK"

        with self.assertRaises(ValidationError) as caught:
            module.admit_read_only_runtime(
                observation, now_epoch_ms=10_100, max_age_ms=1_000
            )

        self.assertEqual("RUNTIME_OWNERSHIP_MISMATCH", caught.exception.code)


    def test_any_effect_or_forbidden_access_invalidates_read_only_admission(self):
        module = _module()
        mutations = (
            lambda safety: safety.__setitem__("credentials_used", True),
            lambda safety: safety.__setitem__("gui_input_sent", True),
            lambda safety: safety.__setitem__("anti_idle_input_sent", True),
            lambda safety: safety.__setitem__("process_control_used", True),
            lambda safety: safety.__setitem__("process_memory_access_used", True),
            lambda safety: safety.__setitem__("network_payload_capture_used", True),
            lambda safety: safety.__setitem__("physical_action_count", 1),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                observation = _exact_observation()
                mutate(observation["safety"])
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual("RUNTIME_READ_ONLY_VIOLATION", caught.exception.code)


    def test_unreachable_host_container_or_display_is_refused(self):
        module = _module()
        for field in ("host_reachable", "container_running", "display_reachable"):
            with self.subTest(field=field):
                observation = _exact_observation()
                observation["locator"][field] = False
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual("RUNTIME_LOCATOR_UNAVAILABLE", caught.exception.code)


    def test_inconsistent_process_display_or_window_identity_is_refused(self):
        module = _module()
        mutations = (
            lambda observation: observation["process"].__setitem__("pid", 0),
            lambda observation: observation["process"].__setitem__("process_start_ticks", 0),
            lambda observation: observation["process"].__setitem__("boot_id_sha256", "b" * 63),
            lambda observation: observation["process"].__setitem__("exe_path", "relative/client"),
            lambda observation: observation["process"].__setitem__("display", ":2"),
            lambda observation: observation["window"].__setitem__("xid", 0),
            lambda observation: observation["window"].__setitem__("pid", 999),
            lambda observation: observation["window"].__setitem__("display", ":2"),
            lambda observation: observation["window"].__setitem__("ownership_proven", False),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                observation = _exact_observation()
                mutate(observation)
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual("RUNTIME_IDENTITY_MISMATCH", caught.exception.code)


    def test_unknown_fields_cannot_enter_admission_or_provenance(self):
        module = _module()
        secret = "SENTINEL_SECRET_DO_NOT_RETAIN"
        mutations = (
            lambda observation: observation.__setitem__("unexpected", secret),
            lambda observation: observation["locator"].__setitem__("password", secret),
            lambda observation: observation["process"].__setitem__("session_token", secret),
            lambda observation: observation["window"].__setitem__("title", secret),
            lambda observation: observation["inventory"].__setitem__("raw_dump", secret),
            lambda observation: observation["safety"].__setitem__("credential_value", secret),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                observation = _exact_observation()
                mutate(observation)
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual("UNKNOWN_FIELD", caught.exception.code)
                self.assertNotIn(secret, str(caught.exception))


    def test_observation_schema_track_and_namespace_are_strict(self):
        module = _module()
        cases = (
            (lambda observation: observation.__setitem__("schema", "otclient.local-agent.runtime-observation.v0"), "INVALID_SCHEMA"),
            (lambda observation: observation.__setitem__("track_id", "otclient-global-login"), "INVALID_TRACK"),
            (lambda observation: observation.__setitem__("runtime_namespace", "UNKNOWN"), "INVALID_RUNTIME_NAMESPACE"),
            (lambda observation: observation.__setitem__("runtime_namespace", "NOT_APPLICABLE"), "INVALID_RUNTIME_NAMESPACE"),
            (lambda observation: observation.__setitem__("runtime_namespace", ""), "INVALID_RUNTIME_NAMESPACE"),
        )
        for mutate, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                observation = _exact_observation()
                mutate(observation)
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual(expected_code, caught.exception.code)


    def test_boolean_values_cannot_masquerade_as_runtime_counts(self):
        module = _module()
        mutations = (
            lambda observation: observation["inventory"].__setitem__("official_client_candidate_count", True),
            lambda observation: observation["inventory"].__setitem__("exact_client_candidate_count", True),
            lambda observation: observation["inventory"].__setitem__("mismatched_or_unverifiable_candidate_count", False),
            lambda observation: observation["safety"].__setitem__("physical_action_count", False),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                observation = _exact_observation()
                mutate(observation)
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual("INVALID_INTEGER", caught.exception.code)


    def test_admitted_snapshot_is_immutable_and_platform_explicit(self):
        module = _module()
        record = module.admit_read_only_runtime(
            _exact_observation(), now_epoch_ms=10_100, max_age_ms=1_000
        )

        self.assertTrue(hasattr(record, "runtime_platform"), "runtime platform is not explicit")
        self.assertEqual("official_native_linux_only", record.runtime_platform)
        with self.assertRaises(TypeError):
            record.process["pid"] = 999
        with self.assertRaises(TypeError):
            record.locator["display"] = ":99"
        provenance = record.to_provenance()
        self.assertEqual("official_native_linux_only", provenance["runtime_platform"])


    def test_admission_record_carries_complete_read_only_track_a_fields_and_inventory(self):
        module = _module()
        record = module.admit_read_only_runtime(
            _exact_observation(), now_epoch_ms=10_100, max_age_ms=1_000
        )

        for field in (
            "track_id",
            "canonical_registration",
            "canonical_lease_generation",
            "registration_lease_generation",
            "inventory",
        ):
            self.assertTrue(hasattr(record, field), f"missing Track A admission field: {field}")
        self.assertEqual("official-client-re", record.track_id)
        self.assertEqual("NOT_APPLICABLE", record.canonical_registration)
        self.assertEqual("NOT_APPLICABLE", record.canonical_lease_generation)
        self.assertEqual("NOT_APPLICABLE", record.registration_lease_generation)
        self.assertEqual(1, record.inventory["official_client_candidate_count"])
        self.assertEqual("PROVEN", record.inventory["target_uniqueness"])

        provenance = record.to_provenance()
        self.assertEqual("official-client-re", provenance["track_id"])
        self.assertEqual("NOT_APPLICABLE", provenance["canonical_registration"])
        self.assertEqual("NOT_APPLICABLE", provenance["canonical_lease_generation"])
        self.assertEqual("NOT_APPLICABLE", provenance["registration_lease_generation"])
        self.assertEqual("NOT_APPLICABLE", provenance["gate_a"])
        self.assertEqual("NOT_APPLICABLE", provenance["generation_rebind"])
        self.assertEqual("NOT_APPLICABLE", provenance["gate_b"])
        self.assertEqual("NOT_APPLICABLE", provenance["bootstrap"])
        self.assertEqual(1, provenance["inventory"]["exact_client_candidate_count"])


    def test_identifiers_and_observer_endpoint_are_safe_and_explicit(self):
        module = _module()
        secret = "SENTINEL_URL_PASSWORD"
        cases = (
            (lambda observation: (observation.__setitem__("task_id", ""), observation.__setitem__("runtime_owner_task", "")), "INVALID_IDENTIFIER"),
            (lambda observation: observation["locator"].__setitem__("runner", ""), "INVALID_IDENTIFIER"),
            (lambda observation: observation["locator"].__setitem__("remote_device", ""), "INVALID_IDENTIFIER"),
            (lambda observation: observation["locator"].__setitem__("container", ""), "INVALID_IDENTIFIER"),
            (lambda observation: observation["locator"].__setitem__("container_gui_user", ""), "INVALID_IDENTIFIER"),
            (lambda observation: observation["locator"].__setitem__("observer_endpoint", f"https://user:{secret}@synology:6902/"), "INVALID_OBSERVER_ENDPOINT"),
            (lambda observation: observation["locator"].__setitem__("observer_endpoint", "http://synology:6902/"), "INVALID_OBSERVER_ENDPOINT"),
            (lambda observation: observation["locator"].__setitem__("observer_endpoint", "https://synology:notaport/"), "INVALID_OBSERVER_ENDPOINT"),
            (lambda observation: observation["locator"].__setitem__("observer_endpoint", f"https://synology:6902/?token={secret}"), "INVALID_OBSERVER_ENDPOINT"),
        )
        for mutate, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                observation = _exact_observation()
                mutate(observation)
                with self.assertRaises(ValidationError) as caught:
                    module.admit_read_only_runtime(
                        observation, now_epoch_ms=10_100, max_age_ms=1_000
                    )
                self.assertEqual(expected_code, caught.exception.code)
                self.assertNotIn(secret, str(caught.exception))


if __name__ == "__main__":
    unittest.main()
