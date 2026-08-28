#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
base = root / 'tools/tibia_re_current_login_field6_scalar_owner'
probe = base / 'probe.py'
qmeta_owner = base / 'qmeta_owner.py'
warp = base / 'prepare_warp.sh'

assert probe.exists(), 'scalar-owner probe not implemented'
assert qmeta_owner.exists(), 'QMeta caller-owner discriminator not implemented'
assert warp.exists(), 'bounded WARP bootstrap not implemented'

text = probe.read_text(encoding='utf-8')
qmeta_text = qmeta_owner.read_text(encoding='utf-8')
warp_text = warp.read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'",
    "'official_client_executed': False",
    "'process_memory_access': False",
    'TLoginProtocolMessageHandler',
    'SCALAR_CALLSITE_CENSUS',
    'CALLER_FDE_RTTI_OWNERS',
    'PARENT_MEMBER_HANDLER_BINDING',
    'UNIQUE_STATIC_SCALAR',
    'FIELD6_VALUE_PROVEN',
    'FIELD6_VALUE_UNKNOWN',
    'NO_HEURISTIC_RANKING',
    'NO_SEMANTIC_GUESSING',
):
    assert required in text, required
for required in ('0x30b6700', '0xe25620', '0x60'):
    assert required in text.lower(), required
for required in (
    'QMETA_CALLER_OWNER',
    'TARGET_SCALAR_PARENT_THIS',
    'STATIC_METAOBJECT_TRIPLE',
    'METHOD_CASE_DIRECT_EDGE',
    'OWNER_QMETA_CLASS',
    'PARENT_MEMBER_HANDLER_BINDING',
    'FIELD6_VALUE_PROVEN',
    'FIELD6_VALUE_UNKNOWN',
    'NO_HEURISTIC_RANKING',
    'NO_SEMANTIC_GUESSING',
    "result['qmeta_caller_owner']",
):
    assert required in qmeta_text, required
assert 'WARP_PROFILE_ATTEMPTS=2' in warp_text
assert 'WARP_BOOTSTRAP_FALLBACK=PASS' in warp_text
assert '25346' in warp_text and '25347' in warp_text
assert 'rm -rf' not in warp_text
combined = (text + qmeta_text + warp_text).lower()
for forbidden in ('subprocess', 'ptrace', 'process_vm_readv'):
    assert forbidden not in combined, forbidden
print('CURRENT_LOGIN_FIELD6_SCALAR_OWNER_CONTRACT=PASS')
