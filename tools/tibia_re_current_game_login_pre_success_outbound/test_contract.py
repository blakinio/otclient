#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
probe = root / 'tools/tibia_re_current_game_login_pre_success_outbound/probe.py'
qmeta_runner = root / 'tools/tibia_re_current_game_login_pre_success_outbound/qmeta_runner.py'
auth_graph = root / 'tools/tibia_re_current_game_login_pre_success_outbound/auth_graph.py'
handler_owner = root / 'tools/tibia_re_current_game_login_pre_success_outbound/handler_owner.py'
handler_connections = root / 'tools/tibia_re_current_game_login_pre_success_outbound/handler_connections.py'
sendlogin_binding = root / 'tools/tibia_re_current_game_login_pre_success_outbound/sendlogin_binding.py'
workflow = root / '.github/workflows/tibia-official-client-re-current-game-login-pre-success-outbound.yml'
assert probe.exists(), 'pre-success outbound probe not implemented'
assert qmeta_runner.exists(), 'qmeta class-root regression runner not implemented'
assert auth_graph.exists(), 'auth start-game causal graph not implemented'
assert handler_owner.exists(), 'handler owner-field census not implemented'
assert handler_connections.exists(), 'handler connection thunk graph not implemented'
assert sendlogin_binding.exists(), 'sendLogin indirect binding discriminator not implemented'
assert workflow.exists(), 'pre-success outbound workflow missing'
text = probe.read_text(encoding='utf-8')
runner = qmeta_runner.read_text(encoding='utf-8')
graph = auth_graph.read_text(encoding='utf-8')
owner = handler_owner.read_text(encoding='utf-8')
connections = handler_connections.read_text(encoding='utf-8')
binding = sendlogin_binding.read_text(encoding='utf-8')
workflow_text = workflow.read_text(encoding='utf-8')
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
assert 'SENDLOGIN_ADAPTER_BINDING' in binding
assert 'sendlogin_adapter_binding' in binding
assert 'rip_refs' in binding
assert 'direct_call_refs' in binding
assert "EXPECTED_SHA256 = '552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1'" in binding
assert 'EXPECTED_SIZE = 52105824' in binding
assert "'field6_source_context'" in runner
assert "'field6_backward_source'" in runner
assert "'nested_source_contexts'" in runner
assert "'producer_callsite_contexts'" in runner
assert "'virtual_slot_0x60_callsites'" in runner
combined = text + runner + graph + owner + connections + binding
assert 'subprocess' not in combined
assert 'ptrace' not in combined.lower()
assert 'process_vm_readv' not in combined.lower()
assert "'VERSION':'15.32.be4f48'" in workflow_text
assert "'UNPACKED_SHA':'552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1'" in workflow_text
assert "'UNPACKED_SIZE':'52105824'" in workflow_text
assert "d['exact_client']['sha256']=='552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1'" in workflow_text
assert 'python3 tools/tibia_re_current_game_login_pre_success_outbound/sendlogin_binding.py --client' in workflow_text
assert "d['sendlogin_adapter_binding']['classification']=='SENDLOGIN_ADAPTER_BINDING'" in workflow_text
assert '15.32.75d4a0' not in workflow_text
assert 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a' not in workflow_text
print('CURRENT_GAME_LOGIN_PRE_SUCCESS_OUTBOUND_CONTRACT=PASS')
