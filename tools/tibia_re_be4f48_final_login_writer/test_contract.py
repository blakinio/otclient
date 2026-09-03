#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYZER = ROOT / "writer_path.py"


def load_analyzer():
    assert ANALYZER.is_file(), "writer_path.py is missing: expected RED before client materialization"
    spec = importlib.util.spec_from_file_location("be4f48_final_login_writer", ANALYZER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_contract() -> None:
    mod = load_analyzer()
    assert mod.EXPECTED_VERSION == "15.32.be4f48"
    assert mod.EXPECTED_SIZE == 52105824
    assert mod.EXPECTED_SHA256 == "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
    assert mod.ADAPTER_FDE == (0xBD3050, 0xBD34DD)
    assert mod.QUEUE_VTABLE_AP == 0x30ED588
    assert mod.QUEUE_VSLOT_68 == 0xBD24A0
    assert mod.PACKET_PROCESSOR_VSLOT_68 == 0xF4ECA0
    assert mod.FINAL_FRAME_FDE == (0xF4EDD0, 0xF4EF15)
    assert mod.hx(0xBD24A0) == "0xbd24a0"
    assert mod.signed64(0xFFFFFFFFFFFFFFFF) == -1
    assert mod.signed64(0x10) == 0x10
    assert mod.is_plausible_offset_to_top(0)
    assert mod.is_plausible_offset_to_top(-0x20)
    assert not mod.is_plausible_offset_to_top(0x100000)
    assert (
        mod.parse_itanium_nested_name("N5tibia8protocol21TProtocolMessageQueueE")
        == "tibia::protocol::TProtocolMessageQueue"
    )
    assert mod.parse_itanium_nested_name("not-itanium") is None


if __name__ == "__main__":
    test_exact_contract()
    print("BE4F48_FINAL_LOGIN_WRITER_CONTRACT=PASS")
