#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
base = root / 'tools/tibia_re_current_login_field6_owner_pair_flow'
probe = base / 'probe.py'
warp = base / 'prepare_warp.sh'
assert probe.exists(), 'owner-pair probe not implemented'
assert warp.exists(), 'bounded WARP bootstrap not implemented'
text = probe.read_text(encoding='utf-8')
warp_text = warp.read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'",
    "'official_client_executed': False",
    "'process_memory_access': False",
    '0x30b6700', '0xe25620', '0x7d15c0', '0x7d1a8a', '0x9c0', '0x9c8',
    'OWNER_PAIR_CONSTRUCTOR_REASSERTION',
    'CONFIG_FIELD_0X30_REACHING_CONSTANTS',
    'OWNER_PAIR_DIRECT_FLOW',
    'OWNER_PAIR_DIRECT_FLOW_UNKNOWN',
    'FIELD6_VALUE_PROVEN',
    'FIELD6_VALUE_UNKNOWN',
    'NO_HEURISTIC_RANKING',
    'NO_SEMANTIC_GUESSING',
):
    assert required.lower() in text.lower(), required
assert 'WARP_PROFILE_ATTEMPTS=2' in warp_text
assert 'WARP_BOOTSTRAP_FALLBACK=PASS' in warp_text
combined=(text+warp_text).lower()
for forbidden in ('subprocess','ptrace','process_vm_readv'):
    assert forbidden not in combined, forbidden
print('CURRENT_LOGIN_FIELD6_OWNER_PAIR_FLOW_CONTRACT=PASS')
