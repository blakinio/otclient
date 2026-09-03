#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / "peer_metaowner.py"


def main() -> None:
    assert TARGET.exists(), "peer_metaowner.py must exist"
    text = TARGET.read_text(encoding="utf-8")
    for token in (
        'EXPECTED_VERSION = "15.32.be4f48"',
        "EXPECTED_SIZE = 52105824",
        'EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"',
        "METAOBJECT_ANCHOR = 0x30B68A0",
        "SIGNAL_INDEX = 0",
        "PEER_TARGET = 0xD052A0",
        "ADAPTER_TARGET = 0xBD3050",
        "ADAPTER_REFERENCE_SITE = 0x7C6B34",
        "CONNECTION_OWNER_FDE = (0x7C6700, 0x7CC933)",
        '"runtime_access": "none"',
        '"track_b_pr_284_modified": False',
    ):
        assert token in text, f"missing contract token: {token}"
    print("BE4F48_SENDLOGIN_PEER_METAOWNER_REPOSITORY_CONTRACT=PASS")


if __name__ == "__main__":
    main()
