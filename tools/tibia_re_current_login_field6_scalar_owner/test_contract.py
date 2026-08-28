#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
base = root / 'tools/tibia_re_current_login_field6_scalar_owner'
probe = base / 'probe.py'
qmeta_owner = base / 'qmeta_owner.py'
focused = base / 'focused_qmeta_owner.py'
runner = base / 'focused_qmeta_owner_runner.py'
warp = base / 'prepare_warp.sh'
workflow = root / '.github/workflows/tibia-official-client-re-current-login-field6-scalar-owner.yml'

assert probe.exists(), 'scalar-owner probe not implemented'
assert qmeta_owner.exists(), 'QMeta caller-owner discriminator not implemented'
assert focused.exists(), 'focused timeout-recovery owner discriminator not implemented'
assert runner.exists(), 'focused occurrence runner not implemented'
assert warp.exists(), 'bounded WARP bootstrap not implemented'
assert workflow.exists(), 'scalar-owner workflow missing'

text = probe.read_text(encoding='utf-8')
qmeta_text = qmeta_owner.read_text(encoding='utf-8')
focused_text = focused.read_text(encoding='utf-8')
runner_text = runner.read_text(encoding='utf-8')
warp_text = warp.read_text(encoding='utf-8')
workflow_text = workflow.read_text(encoding='utf-8')
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
for required in (
    'FOCUSED_TIMEOUT_RECOVERY',
    'VIABLE_CALLSITE_0XCEDDCB',
    'VIABLE_CALLER_FDE_0XCEDD90',
    'VIABLE_EDX_VALUE_1',
    'FRESH_EXACT_REASSERTION',
    'FOCUSED_QMETA_OWNER',
    'FOCUSED_OWNER_CONSTRUCTOR_BINDING',
    'NO_FULL_SCALAR_CENSUS',
    'FIELD6_VALUE_PROVEN',
    'FIELD6_VALUE_UNKNOWN',
    'NO_HEURISTIC_RANKING',
    'NO_SEMANTIC_GUESSING',
):
    assert required in focused_text, required
for forbidden in ('recover_vtables(', 'enumerate_slot_calls(', 'SCALAR_CALLSITE_CENSUS'):
    assert forbidden not in focused_text, forbidden
for required in ('def raw_occurrences(', 'core.Image.occurrences = raw_occurrences', 'focused.main()'):
    assert required in runner_text, required
focused_command = 'python3 tools/tibia_re_current_login_field6_scalar_owner/focused_qmeta_owner_runner.py --client'
probe_command = 'python3 tools/tibia_re_current_login_field6_scalar_owner/probe.py --client'
qmeta_command = 'python3 tools/tibia_re_current_login_field6_scalar_owner/qmeta_owner.py --client'
assert focused_command in workflow_text
assert probe_command not in workflow_text
assert qmeta_command not in workflow_text
assert 'WARP_PROFILE_ATTEMPTS=2' in warp_text
assert 'WARP_BOOTSTRAP_FALLBACK=PASS' in warp_text
assert '25346' in warp_text and '25347' in warp_text
assert 'rm -rf' not in warp_text
combined = (text + qmeta_text + focused_text + runner_text + warp_text).lower()
for forbidden in ('subprocess', 'ptrace', 'process_vm_readv'):
    assert forbidden not in combined, forbidden
print('CURRENT_LOGIN_FIELD6_SCALAR_OWNER_CONTRACT=PASS')
