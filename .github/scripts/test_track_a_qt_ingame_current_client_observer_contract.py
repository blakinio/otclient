#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

WORKFLOW = Path('.github/workflows/track-a-qt-ingame-live-correlation.yml').read_text(encoding='utf-8')
PROMOTION = json.loads(Path('docs/agents/evidence/OTC-20260828-current-gameserver-dispatch-envelope-promotion/result.json').read_text(encoding='utf-8'))
EXACT = PROMOTION['exact_client']


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


require(PROMOTION.get('decision') == 'PASS_BOUNDED', 'current exact-client promotion is not accepted')
require(EXACT.get('version') == '15.32.75d4a0', 'unexpected promoted client version')
require(f"EXPECTED_SIZE: '{EXACT['unpacked_size']}'" in WORKFLOW, 'workflow exact size is not current promoted size')
require(f"EXPECTED_SHA: {EXACT['unpacked_sha256']}" in WORKFLOW, 'workflow exact SHA is not current promoted SHA')
require('52109920' not in WORKFLOW, 'superseded client size remains in workflow')
require('ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8' not in WORKFLOW, 'superseded client SHA remains in workflow')
for marker in ('GAME_VPTR=', 'AUTH_VPTR=', 'PLAYER_VPTR=', "os.open(f'/proc/{pid}/mem'"):
    require(marker not in WORKFLOW, f'superseded memory-layout observer remains: {marker}')
require('LOGGER_READY=true' in WORKFLOW, 'observer does not expose logger-ready boundary')
require('START_TICKS_CHANGED' in WORKFLOW, 'observer does not continuously fence process start identity')
require('character_window_context' in WORKFLOW, 'observer does not retain boolean character-window context')
require('raw_title_retained' in WORKFLOW, 'observer does not explicitly forbid raw title retention')
require('PERSISTENT_VIEW_URL' in WORKFLOW, 'observer does not expose the persistent owner-manual view')
require('packet_payloads_retained' in WORKFLOW, 'observer does not state packet-payload retention boundary')
print('TRACK_A_QT_INGAME_CURRENT_CLIENT_OBSERVER_CONTRACT=PASS')
