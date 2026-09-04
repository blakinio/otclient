#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "next_relay_edge.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-next-relay-edge.yml")


def main() -> None:
    assert TARGET.exists(), "next_relay_edge.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    required = (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        'QUEUE_SIGNAL_NAME = "clientMessageReadyToProcess"',
        "QUEUE_SIGNAL_INDEX = 0xBF",
        "QUEUE_SIGNAL_BODY = 0xBD2190",
        "SELF_RELAY_CONNECTIMPL_CALLSITE = 0xBE2EEE",
        "CONNECTIMPL_FDE = (0xBE2A50, 0xBE3086)",
        "CONNECTIMPL_TARGET = 0x4D6800",
        "CONNECTIMPL_ABI_SRET = True",
        'PROMOTED_RECEIVER_IDENTITY = "tibia::protocol::TProtocolMessageQueue"',
        'PROMOTED_CONNECTION_ROLE = "SIGNAL_RELAY"',
        'PROMOTED_ARGV1_IDENTITY = "exact GameclientMessage shared pair"',
        "PROMOTED_QSLOT_FUNCTION_TARGET = 0xBD2190",
        "def enumerate_bounded_connect_candidates(",
        "def trace_connect_arguments(",
        "def classify_next_relay_edge(",
        "def analyze(",
        '"connection_return_storage_provenance"',
        '"sender_provenance"',
        '"signal_argument_provenance"',
        '"receiver_provenance"',
        '"method_argument_provenance"',
        '"slot_object_provenance"',
        '"next_unique_relay_edge"',
        '"next_endpoint_identity"',
        '"next_relay_identity_preserved"',
        '"queue_signal_writer_identity"',
        '"final_queue_writer_identified"',
        '"final_tcp_writer_identified"',
        '"final_writer_contract"',
        '"runtime_access": "none"',
        '"official_client_executed": False',
        '"track_b_pr_284_modified": False',
        '"FIRST_MISSING_BOUNDARY"',
    )
    for token in required:
        assert token in text, f"missing next-relay contract token: {token}"
    forbidden = (
        "whole_executable_scan",
        "global_connect_census",
        "global_qobject_census",
        "global_qslot_census",
        "global_socket_census",
        "global_writer_census",
        "def exec_refs(",
    )
    for token in forbidden:
        assert token not in text, f"forbidden broad-search marker present: {token}"
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "next_relay_edge.py" in workflow
    assert "Validate repository-only next relay contract" in workflow
    assert "Prepare exact public client package through WARP" in workflow
    print("BE4F48_QUEUE_SIGNAL_BF_NEXT_RELAY_EDGE_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
