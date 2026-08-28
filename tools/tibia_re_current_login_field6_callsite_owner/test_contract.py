#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
base = root / 'tools/tibia_re_current_login_field6_callsite_owner'
paths = {
    'probe': base / 'probe.py',
    'member': base / 'member_provenance.py',
    'focused': base / 'focused_member_provenance.py',
    'qmeta': base / 'handler_qmeta.py',
    'dependency': base / 'producer_dependency.py',
    'accessor': base / 'dependency_accessor.py',
    'queue': base / 'queue_sendlogin.py',
    'gameserver': base / 'gameserver_login_route.py',
    'warp': base / 'prepare_warp.sh',
}
for name, path in paths.items():
    assert path.exists(), f'{name} discriminator not implemented'
texts = {name: path.read_text(encoding='utf-8') for name, path in paths.items()}
text = texts['probe']
for required in ("'runtime_access': 'none'","'official_client_executed': False","'process_memory_access': False",'TLoginProtocolMessageHandler','FIELD6_CALLSITE_OWNER','FIELD6_EDX_REACHING_VALUE'):
    assert required in text, required
for required in ('0x30b6700','0xe25620','0x60'):
    assert required in text.lower(), required
for required in ('INTERPROCEDURAL_MEMBER_PROVENANCE','CALLER_FDE_RTTI_OWNERS','CONSTRUCTOR_MEMBER_BINDING','NO_HEURISTIC_RANKING'):
    assert required in texts['member'], required
for required in ('CALLSITE_FDE_SCOPE','VTABLE_RIP_CONSTRUCTOR_SCOPE','BINARY_SEARCH_FDE_LOOKUP','NO_HEURISTIC_RANKING',"result['interprocedural_member_provenance']"):
    assert required in texts['focused'], required
for required in ('HANDLER_QMETA_SIGNATURES','TLoginProtocolMessageHandler','PARAMETER_TYPES','PARAMETER_NAMES','NO_SEMANTIC_GUESSING',"result['handler_qmeta_signatures']"):
    assert required in texts['qmeta'], required
for required in ('PRODUCER_DEPENDENCY_GUARD','HANDLER_MEMBER_OFFSET_0X10','DEPENDENCY_VIRTUAL_SLOT_0X98','DEPENDENCY_TARGET_0XE195B0','RTTI_OWNER_RECOVERY','NO_SEMANTIC_GUESSING',"result['producer_dependency_guard']"):
    assert required in texts['dependency'], required
for required in ('DEPENDENCY_ACCESSOR_PROVENANCE','TAuthenticationAndEncryptionInfo','ACCESSOR_TARGET_0XE195B0','ACCESSOR_MEMBER_OFFSET','CONSTRUCTOR_WRITES','ALL_MEMBER_WRITES','NO_SEMANTIC_GUESSING',"result['dependency_accessor_provenance']"):
    assert required in texts['accessor'], required
for required in ('QUEUE_SENDLOGIN_PROVENANCE','TProtocolMessageQueue','sendLogin','PARAMETER_TYPES','PARAMETER_NAMES','SLOT_0X60_EDGE','FIELD6_EDX_REACHING_VALUE','NO_SEMANTIC_GUESSING',"result['queue_sendlogin_provenance']"):
    assert required in texts['queue'], required
for required in ('GAMESERVER_LOGIN_ROUTE_PROVENANCE','TAuthenticationProcessController','requestCharacterGameserverLogin','INTERPROCEDURAL_RDX_PROPAGATION','SLOT_0X60_EDGE','FIELD6_EDX_REACHING_VALUE','NO_SEMANTIC_GUESSING',"result['gameserver_login_route_provenance']"):
    assert required in texts['gameserver'], required
assert 'WARP_PROFILE_ATTEMPTS=2' in texts['warp']
assert 'WARP_BOOTSTRAP_FALLBACK=PASS' in texts['warp']
assert '25346' in texts['warp'] and '25347' in texts['warp']
assert 'rm -rf' not in texts['warp']
combined = ''.join(texts.values()).lower()
for forbidden in ('subprocess','ptrace','process_vm_readv'):
    assert forbidden not in combined, forbidden
print('CURRENT_LOGIN_FIELD6_CALLSITE_OWNER_CONTRACT=PASS')
