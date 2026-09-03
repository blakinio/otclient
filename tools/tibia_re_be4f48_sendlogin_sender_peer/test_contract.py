#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYZER = ROOT / "peer_owner.py"


def load_analyzer():
    assert ANALYZER.is_file(), "peer_owner.py is missing: expected RED before client materialization"
    spec = importlib.util.spec_from_file_location("be4f48_sender_peer", ANALYZER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_contract() -> None:
    mod = load_analyzer()
    assert mod.EXPECTED_VERSION == "15.32.be4f48"
    assert mod.EXPECTED_SIZE == 52105824
    assert mod.EXPECTED_SHA256 == "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
    assert mod.PEER_TARGET == 0xD052A0
    assert mod.HELPER_TARGET == 0x4D8670
    assert mod.ADAPTER_TARGET == 0xBD3050
    assert mod.CONNECTION_OWNER_FDE == (0x7C6700, 0x7CC933)
    assert mod.hx(0xD052A0) == "0xd052a0"
    assert mod.signed64(0xFFFFFFFFFFFFFFFF) == -1
    assert mod.signed64(0x10) == 0x10
    assert mod.is_plausible_offset_to_top(0)
    assert mod.is_plausible_offset_to_top(-0x20)
    assert not mod.is_plausible_offset_to_top(0x100000)


if __name__ == "__main__":
    test_exact_contract()
    print("BE4F48_SENDLOGIN_SENDER_PEER_CONTRACT=PASS")
