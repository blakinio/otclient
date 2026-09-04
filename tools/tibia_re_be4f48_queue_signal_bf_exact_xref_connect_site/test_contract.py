#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "exact_xref_connect_site.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-exact-xref-connect-site.yml")


def main() -> None:
    assert TARGET.exists(), "exact_xref_connect_site.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    required = (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        'QUEUE_SIGNAL_NAME = "clientMessageReadyToProcess"',
        "QUEUE_SIGNAL_INDEX = 0xBF",
        "QUEUE_SIGNAL_BODY = 0xBD2190",
        "SIGNAL_BODY_FDE = (0xBD2190, 0xBD2495)",
        "ACTIVATE_CALLSITE = 0xBD22C2",
        "QMETAOBJECT_ACTIVATE = 0x4D7DC0",
        "SELF_RELAY_CONNECTIMPL_CALLSITE = 0xBE2EEE",
        "CONSUMED_CONSTRUCTOR_FDE = (0xBE2A50, 0xBE3086)",
        "CONNECTIMPL_TARGET = 0x4D6800",
        "CONNECTIMPL_ABI_SRET = True",
        'PROMOTED_RECEIVER_IDENTITY = "tibia::protocol::TProtocolMessageQueue"',
        'PROMOTED_ARGV1_IDENTITY = "exact GameclientMessage shared pair"',
        "def derive_queue_signal_identity(",
        "def exact_lea_refs(",
        "def exact_data_refs(",
        "def enumerate_exact_signal_references(",
        "def find_exact_signal_connect_candidates(",
        "def trace_connect_arguments(",
        "def classify_exact_signal_connect_site(",
        "def analyze(",
        '"derived_queue_static_metaobject"',
        '"exact_signal_references"',
        '"exact_signal_reference_count"',
        '"exact_signal_connect_candidate_count"',
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
        assert token in text, f"missing exact-xref contract token: {token}"

    forbidden = (
        "QUEUE_STATIC_METAOBJECT =",
        "whole_executable_connect_scan",
        "all_connectimpl_callers",
        "global_connect_census",
        "global_qobject_census",
        "global_qslot_census",
        "global_socket_census",
        "global_writer_census",
    )
    for token in forbidden:
        assert token not in text, f"forbidden broad/assumed marker present: {token}"

    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "exact_xref_connect_site.py" in workflow
    assert "Validate repository-only exact-signal xref contract" in workflow
    assert "Prepare exact public client package through WARP" in workflow
    assert "Materialize transient exact client and resolve exact-signal connect site" in workflow
    assert workflow.index("Validate repository-only exact-signal xref contract") < workflow.index("Prepare exact public client package through WARP")
    print("BE4F48_QUEUE_SIGNAL_BF_EXACT_XREF_CONNECT_SITE_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
