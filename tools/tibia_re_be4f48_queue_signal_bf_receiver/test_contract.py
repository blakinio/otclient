#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "signal_receiver.py"
WORKFLOW = Path(".github/workflows/tibia-official-client-re-be4f48-queue-signal-bf-receiver.yml")


def main() -> None:
    assert TARGET.exists(), "signal_receiver.py is missing: expected RED before client materialization"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        "QUEUE_STATIC_METAOBJECT = 0x30B73E0",
        "QUEUE_SIGNAL_INDEX = 0xBF",
        "DRAIN_CALLBACK = 0xBD2190",
        "QMETAOBJECT_ACTIVATE = 0x4D7DC0",
        '"runtime_access": "none"',
        '"track_b_pr_284_modified": False',
    ):
        assert token in text, f"missing queue-signal receiver contract token: {token}"
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "signal_receiver.py" in workflow, "workflow must execute signal_receiver.py"
    assert "Validate repository-only queue signal receiver contract" in workflow
    print("BE4F48_QUEUE_SIGNAL_BF_RECEIVER_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
