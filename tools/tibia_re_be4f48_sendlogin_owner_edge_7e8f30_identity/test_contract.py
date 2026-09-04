#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "edge_identity.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-sendlogin-owner-edge-7e8f30-identity.yml")


def main() -> None:
    assert TARGET.exists(), "edge_identity.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        "OWNER_EDGE_CALLSITE = 0x7C67B8",
        "OWNER_EDGE_CALLEE = 0x7E8F30",
        "RECEIVER_FIELD_OFFSET = 0x88",
        "def recover_callee_owner_identity(",
        "def follow_unique_internal_identity_edge(",
        "def analyze(",
        '"owner_edge_callsite"',
        '"owner_edge_callee"',
        '"owner_object_identity"',
        '"owner_object_identity_proven"',
        '"owner_identity_proof_classes"',
        '"sendlogin_receiver_provenance"',
        '"sendlogin_receiver_identity"',
        '"sendlogin_receiver_identity_proven"',
        '"complete_sender_receiver_pair_proven"',
        '"sendlogin_causal_binding_proven"',
        '"runtime_access"',
        '"track_b_pr_284_modified"',
        '"FIRST_MISSING_BOUNDARY"',
        '"SENDLOGIN_OWNER_EDGE_IDENTITY_PROVEN"',
        '"SOURCE_BLOCKER"',
    ):
        assert token in text, f"missing owner-edge contract token: {token}"

    forbidden = (
        "CONNECTION_OWNER_FDE",
        "CONNECTIMPL_CALLSITE",
        "find_direct_callers",
        "recover_in_fde_owner_identity",
        "follow_unique_identity_edge",
    )
    for token in forbidden:
        assert token not in text, f"consumed #884/#889 owner discovery must not be reintroduced: {token}"

    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "edge_identity.py" in workflow, "workflow must execute edge_identity.py"
    assert "Validate repository-only owner-edge identity contract" in workflow
    assert "Prepare exact public client package through WARP" in workflow
    assert workflow.index("Validate repository-only owner-edge identity contract") < workflow.index("Prepare exact public client package through WARP")
    print("BE4F48_SENDLOGIN_OWNER_EDGE_7E8F30_IDENTITY_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
