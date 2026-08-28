#!/usr/bin/env python3
from pathlib import Path

root=Path(__file__).resolve().parents[2]
base=root/'tools/tibia_re_current_login_field6_config_type_flow'
probe=base/'probe.py'
warp=base/'prepare_warp.sh'
assert probe.exists(), 'config-type probe not implemented'
assert warp.exists(), 'bounded WARP bootstrap not implemented'
text=probe.read_text(encoding='utf-8')
warp_text=warp.read_text(encoding='utf-8')
compact=text.replace(' ','')
assert "'runtime_access':'none'" in compact
assert "'official_client_executed':False" in compact
for required in (
    '0x30b6700','0xe25620','0x7d15c0','0x7d1a8a','0x9c8','0x30',
    'CONFIG_TYPE_IDENTITY','CONFIG_TYPE_UNKNOWN','CONFIG_OWNED_METHOD_FLOW',
    'CONFIG_TYPE_CONSTRUCTOR_DIAGNOSTICS',
    'FIELD6_VALUE_UNKNOWN','NO_HEURISTIC_RANKING','NO_SEMANTIC_GUESSING',
):
    assert required.lower() in text.lower(), required
assert 'WARP_PROFILE_ATTEMPTS=2' in warp_text
assert 'WARP_BOOTSTRAP_FALLBACK=PASS' in warp_text
combined=(text+warp_text).lower()
for forbidden in ('subprocess','ptrace','process_vm_readv'):
    assert forbidden not in combined, forbidden
print('CURRENT_LOGIN_FIELD6_CONFIG_TYPE_FLOW_CONTRACT=PASS')
