#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYZER = ROOT / "peer_owner.py"
PLT_DISCRIMINATOR = ROOT / "plt_discriminator.py"


def load_module(path: Path, name: str):
    assert path.is_file(), f"{path.name} is missing: expected repository-only RED before client materialization"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_exact_contract() -> None:
    mod = load_module(ANALYZER, "be4f48_sender_peer")
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


def test_bounded_symbol_role_contract() -> None:
    mod = load_module(PLT_DISCRIMINATOR, "be4f48_sender_peer_plt")
    assert mod.EXPECTED_VERSION == "15.32.be4f48"
    assert mod.EXPECTED_SIZE == 52105824
    assert mod.EXPECTED_SHA256 == "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"
    assert mod.PEER_TARGET == 0xD052A0
    assert mod.PEER_DIRECT_CALLEE == 0x4D7DC0
    assert mod.HELPER_TARGET == 0x4D8670
    assert mod.is_qmeta_activate_symbol("QMetaObject::activate(QObject*, int, void**)")
    assert not mod.is_qmeta_activate_symbol("operator new(unsigned long)")
    assert mod.is_qobject_connect_impl_symbol(
        "QObject::connectImpl(QObject const*, void**, QObject const*, void**, QtPrivate::QSlotObjectBase*, Qt::ConnectionType, int const*, QMetaObject const*)"
    )
    assert not mod.is_qobject_connect_impl_symbol("QMetaObject::activate(QObject*, int, void**)")


if __name__ == "__main__":
    test_exact_contract()
    test_bounded_symbol_role_contract()
    print("BE4F48_SENDLOGIN_SENDER_PEER_CONTRACT=PASS")
