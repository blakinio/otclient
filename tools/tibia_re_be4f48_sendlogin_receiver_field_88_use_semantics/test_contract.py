#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "receiver_field_use_semantics.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-sendlogin-receiver-field-88-use-semantics.yml")


def main() -> None:
    assert TARGET.exists(), "receiver_field_use_semantics.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        "CONNECTIMPL_CALLSITE = 0x7C6B9F",
        "RECEIVER_FIELD_OFFSET = 0x88",
        "ADAPTER_TARGET = 0xBD3050",
        "def resolve_receiver_argument(",
        "def classify_receiver_field_value_use(",
        "def find_unique_object_tied_type_edge(",
        "def analyze(",
        '"receiver_field_value_use"',
        '"receiver_field_value_use_proven"',
        '"sendlogin_receiver_provenance"',
        '"sendlogin_receiver_identity"',
        '"sendlogin_receiver_identity_proven"',
        '"complete_sender_receiver_pair_proven"',
        '"sendlogin_causal_binding_proven"',
        '"runtime_access"',
        '"official_service_e2e_count"',
        '"track_b_pr_284_modified"',
        '"FIRST_MISSING_BOUNDARY"',
        '"SENDLOGIN_RECEIVER_FIELD_USE_IDENTITY_PROVEN"',
        '"SOURCE_BLOCKER"',
    ):
        assert token in text, f"missing receiver-field-use contract token: {token}"

    forbidden = (
        "find_direct_callers",
        "trace_owner_initializer",
        "recover_in_fde_owner_identity",
        "OWNER_EDGE_CALLSITE",
        "OWNER_EDGE_CALLEE",
        "receiver_field_refs",
        "executable_ranges",
    )
    for token in forbidden:
        assert token not in text, f"consumed/global proof mode must not be reintroduced: {token}"

    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "receiver_field_use_semantics.py" in workflow, "workflow must execute receiver_field_use_semantics.py"
    assert "Validate repository-only receiver field-use contract" in workflow
    assert "Prepare exact public client package through WARP" in workflow
    assert workflow.index("Validate repository-only receiver field-use contract") < workflow.index("Prepare exact public client package through WARP")
    assert "RAW_CLIENT_RETAINED=false" in workflow
    print("BE4F48_SENDLOGIN_RECEIVER_FIELD_88_USE_SEMANTICS_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
