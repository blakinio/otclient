#!/usr/bin/env python3
from pathlib import Path


def main() -> int:
    text = Path(__file__).with_name('probe.py').read_text(encoding='utf-8')
    required = [
        'tibiaclient-linux-current/package.json',
        'GameclientMessageLogin', 'LoginRSAEncryptedBlock', 'GameclientMessageEnterWorld',
        'expected_mangled_rtti', 'required_generated_offsets', 'generated_vtable_slots', 'slot_snapshots',
        'TLoginProtocolMessageHandler', 'TAuthenticationAndEncryptionInfo',
        'recover_exact_named_vtable', 'producer_reference_intersection',
        'login_handler_owner_slots', 'producer_candidates',
        "current_generated_method_slots': 'DISCOVERY_ONLY'",
        "runtime_access': 'none'", "raw_client_uploaded': False",
    ]
    for token in required:
        assert token in text, token
    forbidden = [
        '15.32.df7b29',
        'e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe',
        '0xe1abe0', '0x2f63240', '0x30c84a0', '0x30c8428',
        "generated_slot(vt, '0x20')", "generated_slot(vt, '0x40')", "generated_slot(vt, '0x60')",
    ]
    for token in forbidden:
        assert token not in text, token
    print('CURRENT_GAME_LOGIN_SCHEMA_CONTRACT=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
