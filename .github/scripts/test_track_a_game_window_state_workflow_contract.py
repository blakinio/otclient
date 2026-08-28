#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / '.github/workflows/track-a-game-window-state-qualification.yml'
TASK = ROOT / 'docs/agents/tasks/active/OTC-20260828-game-window-state-qualification.md'
text = WORKFLOW.read_text(encoding='utf-8')
task_text = TASK.read_text(encoding='utf-8')

required = (
    'issue_comment:',
    'START_GAME_WINDOW_STATE_QUALIFICATION',
    'github.event.comment.user.login == github.repository_owner',
    'runs-on: [otclient, synology]',
    'persist-credentials: false',
    'RUNTIME_NAMESPACE: track-a-game-window-state-validation',
    "grep -Fqx 'runtime_access: none' \"$task\"",
    "grep -Fqx 'runtime_owner_task: NOT_APPLICABLE' \"$task\"",
    "grep -Fqx 'runtime_namespace: NOT_APPLICABLE' \"$task\"",
    "grep -Fqx 'canonical_registration: NOT_APPLICABLE' \"$task\"",
    "grep -Fqx 'gate_a: NOT_APPLICABLE' \"$task\"",
    "grep -Fqx 'generation_rebind: NOT_APPLICABLE' \"$task\"",
    "grep -Fqx 'gate_b: NOT_APPLICABLE' \"$task\"",
    "grep -Fqx 'target_uniqueness: NOT_APPLICABLE' \"$task\"",
    'REPOSITORY_CHECKPOINT_RUNTIME_ACCESS=none',
    "text != 'START_GAME_WINDOW_STATE_QUALIFICATION'",
    'runtime_locator',
    "docker ps --no-trunc --format '{{.ID}}'",
    'OFFICIAL_CLIENT_CANDIDATE_COUNT=1',
    'game-window-state-readonly-admission.json',
    "'runtime_access':'read_only'",
    "'runtime_owner_task':task",
    "'runtime_namespace':namespace",
    "'gate_a':'NOT_APPLICABLE'",
    "'generation_rebind':'NOT_APPLICABLE'",
    "'gate_b':'NOT_APPLICABLE'",
    "'target_uniqueness':'PROVEN'",
    "'mutation_authorized':False",
    'TRACK_A_RUNTIME_ACCESS=read_only',
    'TRACK_A_RUNTIME_OWNER_TASK=$TASK_ID',
    'TRACK_A_RUNTIME_NAMESPACE=$RUNTIME_NAMESPACE',
    'TRACK_A_TARGET_UNIQUENESS=PROVEN',
    'TRACK_A_MUTATION_AUTHORIZED=false',
    'READ_ONLY_ADMISSION_RECORD=PASS',
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

for needle in (
    'runtime_access: none',
    'runtime_owner_task: NOT_APPLICABLE',
    'runtime_namespace: NOT_APPLICABLE',
    'canonical_registration: NOT_APPLICABLE',
    'canonical_lease_generation: NOT_APPLICABLE',
    'registration_lease_generation: NOT_APPLICABLE',
    'gate_a: NOT_APPLICABLE',
    'generation_rebind: NOT_APPLICABLE',
    'gate_b: NOT_APPLICABLE',
    'bootstrap: NOT_APPLICABLE',
    'target_uniqueness: NOT_APPLICABLE',
    'mutation_authorized: false',
):
    assert needle in task_text, f'TASK_RUNTIME_NONE_CHECKPOINT_MISSING:{needle}'

for forbidden in (
    'GATE_A_REQUIRED=PASS',
    'GENERATION_REBIND_REQUIRED=PASS_OR_NOT_REQUIRED',
    'GATE_B_REQUIRED=PASS',
    "grep -Fqx 'target_uniqueness: PROVEN' \"$task\"",
    'START_GAME_WINDOW_STATE_QUALIFICATION container=',
    'xdotool', 'xprop', 'xwininfo', 'wmctrl', 'screenshot',
    'TIBIA_TEST_EMAIL', 'TIBIA_TEST_PASSWORD', 'docker cp', '/proc/$pid/environ',
):
    assert forbidden.lower() not in text.lower(), f'WORKFLOW_FORBIDDEN_SURFACE:{forbidden}'

assert text.count('semantic_promotion_performed') >= 1
assert text.count('in_game_claimed') >= 1
print('TRACK_A_GAME_WINDOW_STATE_WORKFLOW_CONTRACT=PASS')
