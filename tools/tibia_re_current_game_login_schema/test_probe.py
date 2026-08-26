#!/usr/bin/env python3
from pathlib import Path


def main() -> int:
    probe = Path(__file__).with_name('probe.py')
    assert probe.is_file(), 'probe.py missing'
    text = probe.read_text(encoding='utf-8')
    required = [
        'tibiaclient-linux-current/package.json',
        'GameclientMessageLogin',
        'LoginRSAEncryptedBlock',
        'GameclientMessageEnterWorld',
        'recover_vtable',
        'expected_mangled_rtti',
        "'tibia::protobuf::protocol::' + simple_name",
        "row['rtti_name'] == expected",
        'internal_serialize',
        'byte_size_long',
        'wire_fields',
        "runtime_access': 'none'",
        "raw_client_uploaded': False",
    ]
    for token in required:
        assert token in text, token
    forbidden = [
        '15.32.df7b29',
        'e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe',
        '0x30c84a0', '0x30c8428', '0x176dec0', '0x176db40',
    ]
    for token in forbidden:
        assert token not in text, token
    print('CURRENT_GAME_LOGIN_SCHEMA_CONTRACT=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
