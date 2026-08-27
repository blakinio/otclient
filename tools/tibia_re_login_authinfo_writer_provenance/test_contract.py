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

print('CURRENT_GAME_LOGIN_AUTHINFO_WRITER_CONTRACT=PASS')
