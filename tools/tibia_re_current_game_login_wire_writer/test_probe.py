#!/usr/bin/env python3
from pathlib import Path


def main() -> int:
    text = Path(__file__).with_name('probe.py').read_text(encoding='utf-8')
    required = [
        "find_stringdata", "find_metadata", "find_qmeta_static_metacall", "recover_jump_table",
        "containing_fde", "function_control_transfers", "instruction_context", "rtti_vtable_candidates",
        "plt_symbol_addresses", "rip_refs", "direct_calls", "vtable_reference_contexts", "writer_slot_ref_fdes",
        "tibia::protocol::TProtocolMessageQueue", "sendLogin", "send_login_adapter", "adapter_fde",
        "adapter_indirect_calls", "adapter_indirect_contexts",
        "tibia::network::TGameserverTCPConnection", "tibia::network::TTCPConnection",
        "TProtocolClientMessageProcessor", "TGameserverNetworkPacketRawDataProcessor",
        "TGameserverDualConnection", "TGameserverNetworkPacketConnection",
        "TGameserverNetworkPacketProcessor", "TIODeviceWriter", "TProtocolWriter", "rtti_vtables",
        "QDataStream", "QTcpSocket", "QIODevice", "QBuffer",
        "final_writer_contract': 'UNKNOWN'", "LOGIN_PERFORMED=false", "SECRET_ACCESS=false",
        "RAW_CLIENT_UPLOADED=false",
    ]
    for token in required:
        assert token in text, token
    forbidden = [
        '15.32.df7b29', '15.32.bf29ac',
        'e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe',
        'ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8',
        '0xdf5fe0', '0xdf6be2', '0xbd36a0', '0xb46bd0', '0xf50090', '0x4dd250',
    ]
    for token in forbidden:
        assert token not in text, token

    assert "runtime_access': 'none'" in text
    assert "raw_client_uploaded': False" in text
    print('CURRENT_GAME_LOGIN_WIRE_PROBE_CONTRACT=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
