#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "owner_type.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-sendlogin-connection-owner-type.yml")


def main() -> None:
    assert TARGET.exists(), "owner_type.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        "CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)",
        "CONNECTIMPL_CALLSITE = 0x7C6B9F",
        "RECEIVER_FIELD_OFFSET = 0x88",
        "ADAPTER_TARGET = 0xBD3050",
        "def recover_in_fde_owner_identity(",
        "def follow_unique_identity_edge(",
        "def analyze(",
        '"connection_owner_entry_object"',
        '"connection_owner_identity"',
        '"connection_owner_identity_proven"',
        '"sendlogin_receiver_provenance"',
        '"sendlogin_receiver_identity"',
        '"sendlogin_receiver_identity_proven"',
        '"complete_sender_receiver_pair_proven"',
        '"sendlogin_causal_binding_proven"',
        '"runtime_access"',
        '"track_b_pr_284_modified"',
        '"FIRST_MISSING_BOUNDARY"',
    ):
        assert token in text, f"missing owner-type contract token: {token}"
    assert "find_direct_callers" not in text, "consumed #884 direct-caller discriminator must not be reintroduced"
    assert '"none"' in text, "owner-type analyzer must emit runtime_access=none"
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "owner_type.py" in workflow, "workflow must execute owner_type.py"
    assert "Validate repository-only connection owner-type contract" in workflow
    assert "Prepare exact public client package through WARP" in workflow
    print("BE4F48_SENDLOGIN_CONNECTION_OWNER_TYPE_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
