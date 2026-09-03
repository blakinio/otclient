#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYZER = ROOT / "drain_consumption.py"


def load_analyzer():
    assert ANALYZER.is_file(), "drain_consumption.py is missing: expected RED before client materialization"
    spec = importlib.util.spec_from_file_location("be4f48_queue_drain_consumption", ANALYZER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_exact_contract() -> None:
    mod = load_analyzer()
    assert mod.EXPECTED_VERSION == "15.32.be4f48"
    assert mod.EXPECTED_SIZE == 52105824
    assert mod.EXPECTED_SHA256 == "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
    assert mod.ADAPTER_FDE == (0xBD3050, 0xBD34DD)
    assert mod.QUEUE_VTABLE_AP == 0x30ED588
    assert mod.QUEUE_INSERT == 0xBD24A0
    assert mod.DRAIN_FDE == (0xBD2190, 0xBD2495)
    assert mod.hx(0xBD2190) == "0xbd2190"
    assert (
        mod.parse_itanium_nested_name("N5tibia8protocol21TProtocolMessageQueueE")
        == "tibia::protocol::TProtocolMessageQueue"
    )
    assert mod.parse_itanium_nested_name("not-itanium") is None


def test_identity_join_is_fail_closed() -> None:
    mod = load_analyzer()
    obj = frozenset({"object"})
    owner = frozenset({"owner"})
    pair = frozenset({"object", "owner"})
    unknown = frozenset()
    assert mod.join_identity(obj, obj) == obj
    assert mod.join_identity(pair, pair) == pair
    assert mod.join_identity(obj, owner) == unknown
    assert mod.join_identity(pair, obj) == unknown
    assert mod.join_identity(unknown, obj) == unknown


def test_terminal_classification_requires_causal_identity_and_crosscheck() -> None:
    mod = load_analyzer()

    blocked = mod.classify_terminal(
        serialized_identity_proven=True,
        causal_consumption=False,
        next_writer_candidate=None,
        next_writer_crosscheck=False,
        first_missing_boundary="owned queue callback 0xbd2190 -> causal consumption of exact queued GameclientMessage identity",
    )
    assert blocked["queued_gameclientmessage_causal_consumption"] is False
    assert blocked["next_unique_writer_edge"] == "UNKNOWN"
    assert blocked["final_queue_writer_identified"] is False
    assert blocked["final_tcp_writer_identified"] is False
    assert blocked["final_writer_contract"] == "UNKNOWN"
    assert blocked["terminal_result"] == "SOURCE_BLOCKER"

    no_crosscheck = mod.classify_terminal(
        serialized_identity_proven=True,
        causal_consumption=True,
        next_writer_candidate=0x123456,
        next_writer_crosscheck=False,
        first_missing_boundary="candidate writer edge -> independent ownership cross-check",
    )
    assert no_crosscheck["queued_gameclientmessage_causal_consumption"] is True
    assert no_crosscheck["next_unique_writer_edge"] == "UNKNOWN"
    assert no_crosscheck["final_queue_writer_identified"] is False
    assert no_crosscheck["terminal_result"] == "QUEUE_DRAIN_CONSUMPTION_PROVEN"

    proved = mod.classify_terminal(
        serialized_identity_proven=True,
        causal_consumption=True,
        next_writer_candidate=0x123456,
        next_writer_crosscheck=True,
        first_missing_boundary="none",
    )
    assert proved["queued_gameclientmessage_causal_consumption"] is True
    assert proved["next_unique_writer_edge"] == "0x123456"
    assert proved["final_queue_writer_identified"] is True
    assert proved["final_tcp_writer_identified"] is False
    assert proved["terminal_result"] == "FINAL_QUEUE_WRITER_PROVEN"


def main() -> int:
    test_exact_contract()
    test_identity_join_is_fail_closed()
    test_terminal_classification_requires_causal_identity_and_crosscheck()
    print("BE4F48_QUEUE_DRAIN_CONSUMPTION_CONTRACT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
