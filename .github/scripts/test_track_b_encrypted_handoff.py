#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
workflow_path = root / '.github/workflows/tibia-global-login-encrypted-handoff.yml'
main_workflow_path = root / '.github/workflows/tibia-global-login-lab.yml'
prepare_path = root / '.github/track-b-encrypted-handoff/prepare.sh'
emitter_path = root / '.github/track-b-encrypted-handoff/emit.sh'
cert_path = root / '.github/track-b-encrypted-handoff/recipient.pem'

for path in (workflow_path, main_workflow_path, prepare_path, emitter_path, cert_path):
    assert path.is_file(), f'missing: {path}'

workflow = workflow_path.read_text(encoding='utf-8')
main_workflow = main_workflow_path.read_text(encoding='utf-8')
prepare = prepare_path.read_text(encoding='utf-8')
emitter = emitter_path.read_text(encoding='utf-8')
cert = cert_path.read_text(encoding='utf-8')

prep_step = workflow.index('Prepare encrypted handoff runtime')
emit_step = workflow.index('Emit encrypted one-shot game handoff')
upload_step = workflow.index('Upload ciphertext only')
assert prep_step < emit_step < upload_step
assert 'TIBIA_TEST_EMAIL' not in workflow[prep_step:emit_step]
assert 'TIBIA_TEST_PASSWORD' not in workflow[prep_step:emit_step]
assert '.github/track-b-encrypted-handoff/**' in workflow
assert '.github/scripts/test_track_b_encrypted_handoff.py' in workflow
assert 'retention-days: 1' in workflow and 'handoff.cms' in workflow
assert '.github/track-b-encrypted-handoff' not in main_workflow

assert 'secrets.TIBIA_TEST_EMAIL' not in prepare
assert 'secrets.TIBIA_TEST_PASSWORD' not in prepare
assert 'credential environment reached pre-secret prepare' in prepare
assert 'openssl' in prepare
assert 'LAB_ENCRYPTED_HANDOFF_OPENSSL_READY=true' in prepare

assert 'set +x' in emitter
assert 'CERT=.github/track-b-encrypted-handoff/recipient.pem' in emitter
assert 'openssl cms -encrypt' in emitter
assert '-aes-256-cbc' in emitter
assert '/lab/secrets/login-response.json' in emitter
assert 'rm -f /lab/secrets/login-response.json /lab/secrets/login-handoff.json' in emitter
assert "! grep -a -q 'sessionKey' \"$OUT\"" in emitter
assert 'sessionKey' in emitter and 'characterName' in emitter and 'worldHost' in emitter

assert cert.startswith('-----BEGIN CERTIFICATE-----')
assert 'PRIVATE KEY' not in cert
assert 'TIBIA_TEST_EMAIL' not in cert and 'TIBIA_TEST_PASSWORD' not in cert

print('TRACK_B_ENCRYPTED_HANDOFF_CONTRACT=PASS')
