#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile

BASE_PATH = Path(__file__).with_name("track_a_agent_runtime_governance_base.py")
SPEC = importlib.util.spec_from_file_location("track_a_agent_runtime_governance_base", BASE_PATH)
if SPEC is None or SPEC.loader is None:
    raise SystemExit("Track A governance base validator unavailable")
_base = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _base
SPEC.loader.exec_module(_base)

# Preserve the promoted validator byte-for-byte and extend only the newly reviewed
# same-boot zero-client recovery submode. All other tasks use the original code.
_ORIGINAL_VALIDATE = _base.validate_track_a_task
SAME_BOOT_ZERO_CLIENT_INVALIDATION_MODE = "same_boot_zero_client_invalidation_v1"
SAME_BOOT_ZERO_CLIENT_CONTRACT = "TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1"

TRACK_A = _base.TRACK_A
CANONICAL_NAMESPACE = _base.CANONICAL_NAMESPACE
parse_frontmatter = _base.parse_frontmatter
fail_task = _base.fail_task
positive_generation = _base.positive_generation


def validate_track_a_task(path: Path) -> bool:
    values = parse_frontmatter(path)
    if (
        values.get("track_id") != TRACK_A
        or values.get("runtime_access") != "canonical_recovery"
        or values.get("recovery_mode") != SAME_BOOT_ZERO_CLIENT_INVALIDATION_MODE
    ):
        return bool(_ORIGINAL_VALIDATE(path))

    missing = [field for field in _base.ADMISSION_FIELDS if not values.get(field)]
    if missing:
        fail_task(path, f"missing admission fields {missing}")
    task_id = values.get("task_id")
    if not task_id or values.get("runtime_owner_task") != task_id:
        fail_task(path, "same-boot zero-client recovery owner must equal current task_id")
    if not _base.is_canonical_namespace(values.get("runtime_namespace", "")):
        fail_task(path, "same-boot zero-client recovery must use canonical namespace")
    if values.get("mutation_authorized") != "false":
        fail_task(path, "same-boot zero-client recovery is metadata-only")
    required = {
        "canonical_registration": "PRESENT",
        "generation_rebind": "NOT_APPLICABLE",
        "gate_b": "NOT_APPLICABLE",
        "bootstrap": "NOT_APPLICABLE",
        "target_uniqueness": "UNKNOWN",
        "same_boot_zero_client_contract": SAME_BOOT_ZERO_CLIENT_CONTRACT,
    }
    for field, expected in required.items():
        if values.get(field) != expected:
            fail_task(path, f"same-boot zero-client recovery requires {field}={expected}")
    if values.get("gate_a") not in {"REQUIRED_NOT_PROVEN", "PASS"}:
        fail_task(path, "same-boot zero-client recovery requires Gate A pending or PASS")

    registered = positive_generation(path, values, "registration_lease_generation")
    if values["gate_a"] == "REQUIRED_NOT_PROVEN":
        if values.get("canonical_lease_generation") != "UNKNOWN":
            fail_task(path, "pending same-boot zero-client recovery requires canonical_lease_generation=UNKNOWN")
    else:
        current = positive_generation(path, values, "canonical_lease_generation")
        if current <= registered:
            fail_task(path, "same-boot zero-client recovery requires a newer current controller generation")
    return True


# Patch the base module's global lookup so its existing audit_changed_tasks() and
# self-tests continue to run normally while recognizing the additive submode.
_base.validate_track_a_task = validate_track_a_task


def same_boot_zero_client_invalidation_mode_self_test() -> None:
    def task_text(**overrides: str) -> str:
        values = {
            "task_id": "OTC-TEST-SAME-BOOT-ZERO-CLIENT",
            "track_id": TRACK_A,
            "runtime_access": "canonical_recovery",
            "runtime_owner_task": "OTC-TEST-SAME-BOOT-ZERO-CLIENT",
            "runtime_namespace": CANONICAL_NAMESPACE,
            "canonical_registration": "PRESENT",
            "canonical_lease_generation": "UNKNOWN",
            "registration_lease_generation": "55",
            "gate_a": "REQUIRED_NOT_PROVEN",
            "generation_rebind": "NOT_APPLICABLE",
            "gate_b": "NOT_APPLICABLE",
            "bootstrap": "NOT_APPLICABLE",
            "target_uniqueness": "UNKNOWN",
            "mutation_authorized": "false",
            "recovery_mode": SAME_BOOT_ZERO_CLIENT_INVALIDATION_MODE,
            "same_boot_zero_client_contract": SAME_BOOT_ZERO_CLIENT_CONTRACT,
        }
        values.update(overrides)
        body = "\n".join(f"{key}: {value}" for key, value in values.items())
        return f"---\n{body}\n---\nfixture\n"

    def validate_fixture(**overrides: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "task.md"
            path.write_text(task_text(**overrides), encoding="utf-8")
            if not validate_track_a_task(path):
                raise SystemExit("same-boot zero-client fixture unexpectedly non-Track-A")

    validate_fixture()
    validate_fixture(canonical_lease_generation="56", gate_a="PASS")
    for label, overrides in (
        ("wrong-contract", {"same_boot_zero_client_contract": "WRONG"}),
        ("not-newer", {"canonical_lease_generation": "55", "gate_a": "PASS"}),
        ("singleton-claim", {"target_uniqueness": "PROVEN"}),
        ("mutation", {"mutation_authorized": "true"}),
        ("missing-registration", {"canonical_registration": "ABSENT"}),
    ):
        try:
            validate_fixture(**overrides)
        except SystemExit:
            continue
        raise SystemExit(f"same-boot zero-client self-test failed to reject {label}")

    contract = (_base.ROOT / "docs/agents/contracts/TRACK_A_SAME_BOOT_ZERO_CLIENT_INVALIDATION_V1.md").read_text(encoding="utf-8")
    for marker in (
        SAME_BOOT_ZERO_CLIENT_INVALIDATION_MODE,
        "metadata-only",
        "registration boot identity MUST equal current boot identity",
        "candidate_count == 0",
        "main_window_count == 0",
    ):
        if marker not in contract:
            raise SystemExit(f"same-boot zero-client contract missing marker: {marker}")


def main() -> int:
    same_boot_zero_client_invalidation_mode_self_test()
    return int(_base.main())


if __name__ == "__main__":
    raise SystemExit(main())
