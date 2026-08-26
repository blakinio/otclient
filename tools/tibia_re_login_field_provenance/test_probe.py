#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('field_probe', HERE / 'probe.py')
if SPEC is None or SPEC.loader is None:
    raise SystemExit('cannot load probe module')
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


class FakeImage:
    def __init__(self, raw: bytes):
        self.raw = raw

    def mapped(self, va: int, size: int = 1) -> bool:
        return 0 <= va <= len(self.raw) - size

    def va_to_off(self, va: int) -> int:
        if not self.mapped(va):
            raise ValueError('unmapped')
        return va

    def off_to_va(self, off: int) -> int | None:
        return off if 0 <= off < len(self.raw) else None


assert probe.expected_mangled_full('tibia::authentication::TLoginProtocolMessageHandler') == (
    'N5tibia14authentication28TLoginProtocolMessageHandlerE'
)
assert probe.safe_cstring(FakeImage(b'abc\0tail'), 0) == 'abc'
assert probe.safe_cstring(FakeImage(b'a\0tail'), 0) is None
assert probe.safe_cstring(FakeImage(b'abc\x01\0'), 0) is None

hits = probe.static_keyword_strings(
    FakeImage(b'noise\0session-key-label\0character-name\0other\0'),
    ('session', 'character'),
)
assert list(hits.values()) == ['session-key-label', 'character-name']

source = (HERE / 'probe.py').read_text(encoding='utf-8')
for required in (
    "'runtime_access': 'none'",
    "'login_performed': False",
    "'secret_access': False",
    "'raw_client_uploaded': False",
    "'password_session_to_rsa_field_mapping': 'UNKNOWN'",
    "'user_facing_semantic_field_names': 'UNKNOWN'",
):
    assert required in source, required

print('CURRENT_GAME_LOGIN_FIELD_PROVENANCE_CONTRACT=PASS')
