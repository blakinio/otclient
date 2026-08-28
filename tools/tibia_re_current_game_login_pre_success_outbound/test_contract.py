#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
probe = root / 'tools/tibia_re_current_game_login_pre_success_outbound/probe.py'
assert probe.exists(), 'pre-success outbound probe not implemented'
text = probe.read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'",
    "'login_performed': False",
    "'secret_access': False",
    "'raw_client_uploaded': False",
    'GameclientMessageLogin',
    'LoginRSAEncryptedBlock',
    'field6',
    'sendLogin',
    'sendEnterWorld',
    'receivedLoginSuccessMessage',
    'PRIMARY_PRODUCER_FIELD_PRESENCE',
    'PRE_SUCCESS_SEND_SEQUENCE',
):
    assert required in text, required
assert 'subprocess' not in text
assert 'ptrace' not in text.lower()
assert 'process_vm_readv' not in text.lower()
print('CURRENT_GAME_LOGIN_PRE_SUCCESS_OUTBOUND_CONTRACT=PASS')
