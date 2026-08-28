#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
probe = root / 'tools/tibia_re_prelogin_outbound_sequence/probe.py'
assert probe.exists(), 'pre-login outbound sequence probe not implemented'
src = probe.read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'",
    "'login_performed': False",
    "'secret_access': False",
    "'process_memory_access': False",
    "'raw_client_uploaded': False",
    'TARGET_MESSAGE_TYPES',
    'resolve_game_connect_boundary',
    'resolve_send_login_boundary',
    'resolve_prelogin_outbound_sequence',
):
    assert required in src, required
for target in ('GameclientMessageClientDetails','GameclientMessageSetClientOptions','GameclientMessageEnterWorld','GameclientMessageSecondaryLogin','GameclientMessageLogin'):
    assert target in src, target
for forbidden in ('TIBIA_TEST_EMAIL','TIBIA_TEST_PASSWORD','ptrace(','gdb ','subprocess.run([client','os.exec'):
    assert forbidden not in src, forbidden
print('CURRENT_PRELOGIN_OUTBOUND_SEQUENCE_CONTRACT=PASS')