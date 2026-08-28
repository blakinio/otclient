#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[2]
probe = root / 'tools/tibia_re_gameserver_dispatch_envelope/probe.py'
assert probe.exists(), 'dispatch-envelope probe not implemented'
src = probe.read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'",
    "'login_performed': False",
    "'secret_access': False",
    "'process_memory_access': False",
    "'raw_client_uploaded': False",
    'TARGET_DISPATCH_ID = 0x34',
    'resolve_dispatch_parser',
    'resolve_dispatch_case',
    'resolve_type_identity',
):
    assert required in src, required
for forbidden in ('TIBIA_TEST_EMAIL', 'TIBIA_TEST_PASSWORD', 'ptrace(', 'gdb ', 'subprocess.run([client', 'os.exec'):
    assert forbidden not in src, forbidden
print('CURRENT_GAMESERVER_DISPATCH_ENVELOPE_CONTRACT=PASS')
