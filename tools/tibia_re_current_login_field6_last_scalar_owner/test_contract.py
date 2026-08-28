#!/usr/bin/env python3
from pathlib import Path

root=Path(__file__).resolve().parents[2]
base=root/'tools/tibia_re_current_login_field6_last_scalar_owner'
probe=base/'probe.py'
warp=base/'prepare_warp.sh'
assert probe.exists(), 'last-scalar owner probe not implemented'
assert warp.exists(), 'bounded WARP bootstrap not implemented'
text=probe.read_text(encoding='utf-8')
warp_text=warp.read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'", "'official_client_executed': False",
    '0x16da340','0x16da7fc','0x16da705','0x16da70e','0x16da713','0x16da716',
    'LAST_SCALAR_EXACT_REASSERTION','LAST_SCALAR_QMETA_OWNER','LAST_SCALAR_MEMBER_BINDING',
    'TLoginProtocolMessageHandler','0x30b6700','0xe25620',
    'FIELD6_VALUE_PROVEN','FIELD6_VALUE_UNKNOWN','NO_HEURISTIC_RANKING','NO_SEMANTIC_GUESSING',
):
    assert required.lower() in text.lower(), required
assert 'WARP_PROFILE_ATTEMPTS=2' in warp_text
assert 'WARP_BOOTSTRAP_FALLBACK=PASS' in warp_text
combined=(text+warp_text).lower()
for forbidden in ('subprocess','ptrace','process_vm_readv'):
    assert forbidden not in combined, forbidden
print('CURRENT_LOGIN_FIELD6_LAST_SCALAR_OWNER_CONTRACT=PASS')
