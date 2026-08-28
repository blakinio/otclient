#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
probe = root / 'tools/tibia_re_current_game_login_pre_success_outbound/probe.py'
qmeta_runner = root / 'tools/tibia_re_current_game_login_pre_success_outbound/qmeta_runner.py'
auth_graph = root / 'tools/tibia_re_current_game_login_pre_success_outbound/auth_graph.py'
handler_owner = root / 'tools/tibia_re_current_game_login_pre_success_outbound/handler_owner.py'
handler_connections = root / 'tools/tibia_re_current_game_login_pre_success_outbound/handler_connections.py'
assert probe.exists(), 'pre-success outbound probe not implemented'
assert qmeta_runner.exists(), 'qmeta class-root regression runner not implemented'
assert auth_graph.exists(), 'auth start-game causal graph not implemented'
assert handler_owner.exists(), 'handler owner-field census not implemented'
assert handler_connections.exists(), 'handler connection thunk graph not implemented'
text = probe.read_text(encoding='utf-8')
runner = qmeta_runner.read_text(encoding='utf-8')
graph = auth_graph.read_text(encoding='utf-8')
owner = handler_owner.read_text(encoding='utf-8')
connections = handler_connections.read_text(encoding='utf-8')
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
assert 'FIELD6_SOURCE_CONTEXT' in runner
assert 'NESTED_SOURCE_CONTEXTS' in runner
assert 'FIELD6_BACKWARD_SOURCE' in runner
assert 'CFG_REACHING_DEFINITION' in runner
assert 'NEAREST_STATIC_REGISTER_DEFINITION' not in runner
assert 'LOGIN_PRODUCER_CALLSITE_CONTEXTS' in runner
assert 'VIRTUAL_SLOT_0X60_CENSUS' in runner
assert 'AUTH_START_GAMESERVER_LOGIN_GRAPH' in graph
assert 'TAuthenticationProcessController' in graph
assert 'onStartGameServerLoginStateEntered' in graph
assert "result['auth_start_gameserver_login_graph']" in graph
assert 'HANDLER_OWNER_FIELD_REF_CENSUS' in owner
assert '0x9c0' in owner
assert "result['handler_owner_field_refs']" in owner
assert 'HANDLER_CONNECTION_THUNK_GRAPH' in connections
assert '0x7d15c0' in connections
assert "result['handler_connection_thunk_graph']" in connections
assert "'field6_source_context'" in runner
assert "'field6_backward_source'" in runner
assert "'nested_source_contexts'" in runner
assert "'producer_callsite_contexts'" in runner
assert "'virtual_slot_0x60_callsites'" in runner
combined = text + runner + graph + owner + connections
assert 'subprocess' not in combined
assert 'ptrace' not in combined.lower()
assert 'process_vm_readv' not in combined.lower()
print('CURRENT_GAME_LOGIN_PRE_SUCCESS_OUTBOUND_CONTRACT=PASS')
