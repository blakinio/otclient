#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
base = root / 'tools/tibia_re_current_login_field6_callsite_owner'
probe = base / 'probe.py'
member = base / 'member_provenance.py'
focused = base / 'focused_member_provenance.py'
qmeta = base / 'handler_qmeta.py'
dependency = base / 'producer_dependency.py'
accessor = base / 'dependency_accessor.py'
warp = base / 'prepare_warp.sh'
for path, message in ((probe,'field6 callsite owner probe not implemented'),(member,'interprocedural member provenance not implemented'),(focused,'focused member provenance not implemented'),(qmeta,'handler QMeta discriminator not implemented'),(dependency,'producer dependency discriminator not implemented'),(accessor,'dependency accessor provenance not implemented'),(warp,'bounded WARP bootstrap fallback not implemented')):
    assert path.exists(), message
text = probe.read_text(encoding='utf-8')
member_text = member.read_text(encoding='utf-8')
focused_text = focused.read_text(encoding='utf-8')
qmeta_text = qmeta.read_text(encoding='utf-8')
dependency_text = dependency.read_text(encoding='utf-8')
accessor_text = accessor.read_text(encoding='utf-8')
warp_text = warp.read_text(encoding='utf-8')
for required in ("'runtime_access': 'none'","'official_client_executed': False","'process_memory_access': False",'TLoginProtocolMessageHandler','FIELD6_CALLSITE_OWNER','FIELD6_EDX_REACHING_VALUE'):
    assert required in text, required
for required in ('0x30b6700','0xe25620','0x60'):
    assert required in text.lower(), required
for required in ('INTERPROCEDURAL_MEMBER_PROVENANCE','CALLER_FDE_RTTI_OWNERS','CONSTRUCTOR_MEMBER_BINDING','NO_HEURISTIC_RANKING'):
    assert required in member_text, required
for required in ('CALLSITE_FDE_SCOPE','VTABLE_RIP_CONSTRUCTOR_SCOPE','BINARY_SEARCH_FDE_LOOKUP','NO_HEURISTIC_RANKING',"result['interprocedural_member_provenance']"):
    assert required in focused_text, required
for required in ('HANDLER_QMETA_SIGNATURES','TLoginProtocolMessageHandler','PARAMETER_TYPES','PARAMETER_NAMES','NO_SEMANTIC_GUESSING',"result['handler_qmeta_signatures']"):
    assert required in qmeta_text, required
for required in ('PRODUCER_DEPENDENCY_GUARD','HANDLER_MEMBER_OFFSET_0X10','DEPENDENCY_VIRTUAL_SLOT_0X98','DEPENDENCY_TARGET_0XE195B0','RTTI_OWNER_RECOVERY','NO_SEMANTIC_GUESSING',"result['producer_dependency_guard']"):
    assert required in dependency_text, required
for required in ('DEPENDENCY_ACCESSOR_PROVENANCE','TAuthenticationAndEncryptionInfo','ACCESSOR_TARGET_0XE195B0','ACCESSOR_MEMBER_OFFSET','CONSTRUCTOR_WRITES','ALL_MEMBER_WRITES','NO_SEMANTIC_GUESSING',"result['dependency_accessor_provenance']"):
    assert required in accessor_text, required
assert 'WARP_PROFILE_ATTEMPTS=2' in warp_text
assert 'WARP_BOOTSTRAP_FALLBACK=PASS' in warp_text
assert '25346' in warp_text and '25347' in warp_text
assert 'rm -rf' not in warp_text
combined = (text + member_text + focused_text + qmeta_text + dependency_text + accessor_text + warp_text).lower()
for forbidden in ('subprocess','ptrace','process_vm_readv'):
    assert forbidden not in combined, forbidden
print('CURRENT_LOGIN_FIELD6_CALLSITE_OWNER_CONTRACT=PASS')
