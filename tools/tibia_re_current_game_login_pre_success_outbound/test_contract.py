#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
probe = root / 'tools/tibia_re_current_game_login_pre_success_outbound/probe.py'
qmeta_runner = root / 'tools/tibia_re_current_game_login_pre_success_outbound/qmeta_runner.py'
assert probe.exists(), 'pre-success outbound probe not implemented'
assert qmeta_runner.exists(), 'qmeta class-root regression runner not implemented'
text = probe.read_text(encoding='utf-8')
runner = qmeta_runner.read_text(encoding='utf-8')
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
assert 'stringdata_bases_for_literal(img, class_name)' in runner
assert 'stringdata_bases_for_literal(img, seed)' not in runner
assert 'core.exact_qmeta_class = exact_qmeta_class' in runner
assert 'subprocess' not in text + runner
assert 'ptrace' not in (text + runner).lower()
assert 'process_vm_readv' not in (text + runner).lower()
print('CURRENT_GAME_LOGIN_PRE_SUCCESS_OUTBOUND_CONTRACT=PASS')
