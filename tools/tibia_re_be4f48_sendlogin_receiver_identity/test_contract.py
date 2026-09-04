#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "receiver_identity.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-sendlogin-receiver-identity.yml")


def main() -> None:
    assert TARGET.exists(), "receiver_identity.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        "CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)",
        "CONNECTIMPL_CALLSITE = 0x7C6B9F",
        "RECEIVER_FIELD_OFFSET = 0x88",
        "ADAPTER_TARGET = 0xBD3050",
        "CONNECTIMPL_HAS_HIDDEN_SRET = True",
        "def stack_deltas(",
        "def resolve_stack_slot(",
        "def resolve_receiver_argument(",
        '"runtime_access": "none"',
        '"track_b_pr_284_modified": False',
    ):
        assert token in text, f"missing receiver-identity contract token: {token}"
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "receiver_identity.py" in workflow, "workflow must execute receiver_identity.py"
    assert "Validate repository-only receiver identity contract" in workflow
    print("BE4F48_SENDLOGIN_RECEIVER_IDENTITY_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
