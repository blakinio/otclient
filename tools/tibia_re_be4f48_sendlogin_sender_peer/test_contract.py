#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYZER = ROOT / "peer_owner.py"


def test_peer_owner_analyzer_exists() -> None:
    assert ANALYZER.is_file(), "peer_owner.py is missing: expected RED before client materialization"


if __name__ == "__main__":
    test_peer_owner_analyzer_exists()
    print("BE4F48_SENDLOGIN_SENDER_PEER_CONTRACT=PASS")
