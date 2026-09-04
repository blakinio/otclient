#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "qslot_identity.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-qslot-identity.yml")


def main() -> None:
    assert TARGET.exists(), "qslot_identity.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        "QUEUE_SIGNAL_INDEX = 0xBF",
        "QUEUE_SIGNAL_BODY = 0xBD2190",
        "CONNECTIMPL_FDE = (0xBE2A50, 0xBE3086)",
        "CONNECTIMPL_CALLSITE = 0xBE2EEE",
        "QSLOT_PRODUCER_CALLSITE = 0xBE2EB1",
        "QSLOT_CONSTRUCTION_WINDOW = (0xBE2E80, 0xBE2EEE)",
        "QSLOT_IMPL_STORE_SITE = 0xBE2EBF",
        'QSLOT_IMPL_REGISTER = "r13"',
        "def resolve_qslot_producer(",
        "def resolve_qslot_construction_window(",
        "def trace_qslot_impl_register(",
        "def resolve_qslot_function(",
        "def trace_one_writer_edge(",
        "def analyze(",
        '"qslot_object_producer"',
        '"qslot_construction_window"',
        '"qslot_impl_register_provenance"',
        '"qslot_function_target"',
        '"qslot_identity_proven"',
        '"queue_signal_writer_identity"',
        '"next_unique_writer_edge"',
        '"final_queue_writer_identified"',
        '"final_tcp_writer_identified"',
        '"final_writer_contract"',
        '"runtime_access": "none"',
        '"track_b_pr_284_modified": False',
        '"FIRST_MISSING_BOUNDARY"',
    ):
        assert token in text, f"missing qslot-identity contract token: {token}"
    assert "def exec_refs(" not in text, "global whole-executable reference census is forbidden"
    assert "for sec in img.sections" not in text or "whole_executable_scan" not in text, "global executable scan marker is forbidden"
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "qslot_identity.py" in workflow, "workflow must execute qslot_identity.py"
    assert "Validate repository-only QSlot identity contract" in workflow
    assert "Prepare exact public client package through WARP" in workflow
    print("BE4F48_QUEUE_SIGNAL_BF_QSLOT_IDENTITY_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
