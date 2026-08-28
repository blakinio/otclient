#!/usr/bin/env python3
from pathlib import Path

workflow = Path('.github/workflows/track-a-qt-lifecycle-transition-logger.yml')
script = Path('.github/scripts/track_a_qt_lifecycle_transition_logger.py')
task = Path('docs/agents/tasks/active/OTC-20260828-current-qt-world-correlation.md')
for path in (workflow, script, task):
    if not path.is_file():
        raise SystemExit(f'missing lifecycle logger surface: {path}')
w = workflow.read_text(encoding='utf-8')
s = script.read_text(encoding='utf-8')
t = task.read_text(encoding='utf-8')

checks = {
    'owner command': "ONE_SHOT_QT_LIFECYCLE_TRANSITION" in w,
    'owner actor': "github.actor == 'blakinio'" in w,
    'current size': "EXPECTED_SIZE: '52105824'" in w,
    'current sha': 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a' in w,
    'registration gate': 'REGISTRATION_ABSENT' in w,
    'read only authority': 'PROCESS_MEMORY_ACCESS=read_only' in w,
    'no agent input': 'AGENT_GUI_INPUT=false' in w and 'GAMEPLAY_ACTIONS=false' in w,
    'auth controller': 'TAuthenticationProcessController' in s,
    'gameserver login controller': 'TGameserverLoginProcessController' in s,
    'character selection controller': 'TCharacterSelectionController' in s,
    'disconnect controller': 'TGameSessionDisconnectReactionController' in s,
    'qstate polling': 'qstate_candidates' in s and 'QSTATE_STATE_OFFSET' in s,
    'tcp metadata only': 'tcp_established_count' in s and '/proc/net/tcp' in s,
    'same process fence': 'START_TICKS_CHANGED' in s,
    'logger ready': 'LOGGER_READY' in s,
    'no socket endpoints': 'remote_address' not in s and 'remote_port' not in s,
    'no raw memory retention': 'heap_bytes_retained' in s,
    'no secrets': 'credentials_retained' in s and 'session_secrets_retained' in s,
    'no payload': 'packet_payloads_retained' in s,
    'no semantic promotion': 'semantic_promotion_performed' in s and 'in_game_claimed' in s,
    'task branch': 'branch: research/OTC-20260828-qt-lifecycle-transition-logger' in t,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit('lifecycle logger contract failed: ' + ', '.join(failed))
print('TRACK_A_QT_LIFECYCLE_TRANSITION_LOGGER_CONTRACT=PASS')