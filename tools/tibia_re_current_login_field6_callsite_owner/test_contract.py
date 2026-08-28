#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
probe = root / 'tools/tibia_re_current_login_field6_callsite_owner/probe.py'
assert probe.exists(), 'field6 callsite owner probe not implemented'
text = probe.read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'",
    "'official_client_executed': False",
    "'process_memory_access': False",
    'TLoginProtocolMessageHandler',
    'FIELD6_CALLSITE_OWNER',
    'FIELD6_EDX_REACHING_VALUE',
):
    assert required in text, required
lower = text.lower()
for required in ('0x30b6700', '0xe25620', '0x60'):
    assert required in lower, required
for forbidden in ('subprocess', 'ptrace', 'process_vm_readv'):
    assert forbidden not in lower, forbidden
print('CURRENT_LOGIN_FIELD6_CALLSITE_OWNER_CONTRACT=PASS')
