#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / '.github/workflows/track-a-game-window-state-qualification.yml'
text = WORKFLOW.read_text(encoding='utf-8')

required = (
    'issue_comment:',
    'START_GAME_WINDOW_STATE_QUALIFICATION',
    'github.event.comment.user.login == github.repository_owner',
    'runs-on: [otclient, synology]',
    'runtime_access: read_only',
    'mutation_authorized: false',
    'login_allowed: false',
    'character_selection_allowed: false',
    'gameplay_allowed: false',
    'gui_input_authorized: false',
    'process_control_authorized: false',
    'physical_action_budget: 0',
    'python3 .github/scripts/test_track_a_canonical_current_client_fence.py',
    'EXPECTED_SIZE: 52105824',
    'EXPECTED_SHA: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a',
    'docker exec -i "$CONTAINER" python3 -',
    'track_a_current_world_entered_anchor.py',
    'track_a_current_world_entered_durable_state.py',
    'track_a_game_window_state_qualification.py',
    'duration-seconds 1800',
    'heartbeat-seconds 5',
    'in_game_claimed',
    'semantic_promotion_performed',
    'actions/upload-artifact@',
    'retention-days: 3',
)
for needle in required:
    assert needle in text, f'WORKFLOW_CONTRACT_MISSING:{needle}'

for forbidden in (
    'xdotool', 'xprop', 'xwininfo', 'wmctrl', 'screenshot', 'credential',
    'TIBIA_TEST_EMAIL', 'TIBIA_TEST_PASSWORD', 'docker cp', '/proc/$pid/environ',
):
    assert forbidden.lower() not in text.lower(), f'WORKFLOW_FORBIDDEN_SURFACE:{forbidden}'

assert text.count('semantic_promotion_performed') >= 1
assert text.count('in_game_claimed') >= 1
print('TRACK_A_GAME_WINDOW_STATE_WORKFLOW_CONTRACT=PASS')
