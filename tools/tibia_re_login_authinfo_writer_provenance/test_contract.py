#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
workflow = root / '.github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml'
trace = root / 'tools/tibia_re_login_authinfo_writer_provenance/probe_trace.py'

assert workflow.is_file()
assert trace.is_file(), 'missing narrow backward trace probe'

wf = workflow.read_text(encoding='utf-8')
src = trace.read_text(encoding='utf-8')

for required in (
    'Track A current game-login AuthInfo writer provenance',
    'runs-on: ubuntu-24.04',
    '15.32.75d4a0',
    'probe_deep.py',
    'probe_owner.py',
    'probe_trace.py',
    'artifacts/current-game-login-authinfo-writer-provenance',
):
    assert required in wf, required

for required in (
    "'runtime_access': 'none'",
    "'login_performed': False",
    "'secret_access': False",
    "'raw_client_uploaded': False",
):
    assert required in src, required

# The hosted discriminator must disassemble the client only once. Deep/owner
# helpers are imported/reused by probe_trace, not executed as separate full scans.
assert 'python3 tools/tibia_re_login_authinfo_writer_provenance/probe_deep.py \\' not in wf
assert 'python3 tools/tibia_re_login_authinfo_writer_provenance/probe_owner.py \\' not in wf
for required in (
    'TGameClient',
    'auth_slot_sites',
    'devirtualized_owner_candidates',
    'caller_object_tgameclient_slot_match',
):
    assert required in src, required

for required in (
    'gameserver_session_vtable_refs',
    'auth_slot_ref_fdes',
    'receivedLoginChallengeMessage',
    'valid_qmeta_records',
):
    assert required in src, required

for required in (
    'sessionkey_literal_refs',
    'character_parser_literal_refs',
    'exact_qmeta_classes',
    'onConnectClientToGameserver',
    'loginSuccessful',
    'requestCharacterLogin',
):
    assert required in src, required

for required in (
    'schema_storage_targets',
    'schema_storage_runtime_refs',
    'raw_rip_refs',
):
    assert required in src, required

for required in (
    'semantic_edge_callers',
    'targeted_semantic_snapshots',
    'TProtocolMessageQueue',
    'receivedLoginChallengeMessage',
    'GameserverMessageLoginChallenge',
):
    assert required in src, required

for required in (
    'rsa_rtti_candidates',
    'rsa_slot_callers',
    'rsa_vtable_refs',
    'RSA_STATIC_DISCRIMINATOR',
):
    assert required in src, required

for required in (
    'login_adapter_helper_snapshots',
    'generated_serializer_callers',
    'generated_serializer_vtable_refs',
    'LOGIN_SPECIFIC_TRANSFORM_DISCRIMINATOR',
):
    assert required in src, required

for required in (
    'login_envelope_vtables',
    'login_envelope_serializer_snapshots',
    'LOGIN_ENVELOPE_DISCRIMINATOR',
):
    assert required in src, required

for required in (
    'gameclient_message_wire_snapshots',
    'GAMECLIENT_MESSAGE_WIRE_DISCRIMINATOR',
):
    assert required in src, required

for required in (
    'gameclient_payload_helper_snapshot',
    'GAMECLIENT_PAYLOAD_TAG_DISCRIMINATOR',
):
    assert required in src, required

print('CURRENT_GAME_LOGIN_AUTHINFO_WRITER_CONTRACT=PASS')
