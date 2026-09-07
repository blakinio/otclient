#!/usr/bin/env python3
from pathlib import Path

root=Path(__file__).resolve().parents[2]
base=root/'tools/tibia_re_current_login_field6_last_scalar_owner'
probe=base/'probe.py'
focused=base/'focused_probe.py'
warp=base/'prepare_warp.sh'
workflow=root/'.github/workflows/tibia-official-client-re-current-login-field6-last-scalar-owner.yml'
assert probe.exists(), 'last-scalar owner probe not implemented'
assert focused.exists(), 'focused timeout-recovery probe not implemented'
assert warp.exists(), 'bounded WARP bootstrap not implemented'
assert workflow.exists(), 'last-scalar workflow missing'
text=probe.read_text(encoding='utf-8')
focused_text=focused.read_text(encoding='utf-8')
warp_text=warp.read_text(encoding='utf-8')
workflow_text=workflow.read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'", "'official_client_executed': False",
    '0x16da340','0x16da7fc','0x16da705','0x16da70e','0x16da713','0x16da716',
    'LAST_SCALAR_EXACT_REASSERTION','LAST_SCALAR_QMETA_OWNER','LAST_SCALAR_MEMBER_BINDING',
    'TLoginProtocolMessageHandler','0x30b6700','0xe25620',
    'FIELD6_VALUE_PROVEN','FIELD6_VALUE_UNKNOWN','NO_HEURISTIC_RANKING','NO_SEMANTIC_GUESSING',
):
    assert required.lower() in text.lower(), required
for required in ('FOCUSED_TIMEOUT_RECOVERY','RAW_REL32_TARGET_PREFILTER','RAW_RIP_VTABLE_PREFILTER'):
    assert required in focused_text, required
focused_cmd='python3 tools/tibia_re_current_login_field6_last_scalar_owner/focused_probe.py --client'
slow_cmd='python3 tools/tibia_re_current_login_field6_last_scalar_owner/probe.py --client'
assert focused_cmd in workflow_text
assert slow_cmd not in workflow_text
assert 'WARP_PROFILE_ATTEMPTS=2' in warp_text
assert 'WARP_BOOTSTRAP_FALLBACK=PASS' in warp_text
combined=(text+focused_text+warp_text).lower()
for forbidden in ('subprocess','ptrace','process_vm_readv'):
    assert forbidden not in combined, forbidden
print('CURRENT_LOGIN_FIELD6_LAST_SCALAR_OWNER_CONTRACT=PASS')
