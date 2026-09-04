#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "relay_receiver_type.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-relay-receiver-type.yml")


def main() -> None:
    assert TARGET.exists(), "relay_receiver_type.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        'QUEUE_SIGNAL_NAME = "clientMessageReadyToProcess"',
        "QUEUE_SIGNAL_INDEX = 0xBF",
        "CONNECTIMPL_FDE = (0xBE2A50, 0xBE3086)",
        "CONNECTIMPL_CALLSITE = 0xBE2EEE",
        'RECEIVER_PROVENANCE = "ENTRY_ARG:rdi"',
        "PROMOTED_RECEIVER_PROVENANCE = True",
        "QSLOT_FUNCTION_TARGET = 0xBD2190",
        "def resolve_receiver_type(",
        "def classify_connection_role(",
        "def trace_one_relay_edge(",
        "def analyze(",
        '"promoted_receiver_provenance_consumed"',
        '"queue_signal_receiver_identity"',
        '"queue_signal_receiver_identity_proven"',
        '"queue_signal_connection_role"',
        '"next_unique_relay_edge"',
        '"next_endpoint_identity"',
        '"final_queue_writer_identified"',
        '"final_tcp_writer_identified"',
        '"final_writer_contract"',
        '"runtime_access": "none"',
        '"official_client_executed": False',
        '"track_b_pr_284_modified": False',
        '"FIRST_MISSING_BOUNDARY"',
    ):
        assert token in text, f"missing relay-receiver contract token: {token}"
    for forbidden in (
        "def exec_refs(",
        "whole_executable_scan",
        "global_socket_census",
        "global_qobject_census",
    ):
        assert forbidden not in text, f"forbidden broad-search marker present: {forbidden}"
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "relay_receiver_type.py" in workflow, "workflow must execute relay_receiver_type.py"
    assert "Validate repository-only relay receiver contract" in workflow
    assert "Prepare exact public client package through WARP" in workflow
    print("BE4F48_QUEUE_SIGNAL_BF_RELAY_RECEIVER_TYPE_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
