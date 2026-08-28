#!/usr/bin/env python3
from pathlib import Path

workflow = Path('.github/workflows/track-a-current-qt-world-snapshot.yml')
script = Path('.github/scripts/track_a_current_qt_world_snapshot.py')
task = Path('docs/agents/tasks/active/OTC-20260828-current-qt-world-correlation.md')
for path in (workflow, script, task):
    if not path.is_file():
        raise SystemExit(f'missing required snapshot surface: {path}')
w = workflow.read_text(encoding='utf-8')
s = script.read_text(encoding='utf-8')
t = task.read_text(encoding='utf-8')
checks = {
    'owner command': "github.event.comment.body == 'ONE_SHOT_QT_WORLD_SNAPSHOT'" in w,
    'owner actor': "github.actor == 'blakinio'" in w,
    'self hosted': 'runs-on: [otclient, synology]' in w,
    'current size': "EXPECTED_SIZE: '52105824'" in w,
    'current sha': 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a' in w,
    'registration gate': 'REGISTRATION_ABSENT' in w,
    'no gameplay': 'GAMEPLAY_ACTIONS=false' in w,
    'read only memory': "os.O_RDONLY | os.O_CLOEXEC" in s,
    'bounded member scan': 'AUTH_MEMBER_SCAN_LIMIT = 0x1200' in s,
    'qt state fence': 'KNOWN_QT_STATE_MACHINE_SHA256' in s,
    'qt family mapping': '"libQt6StateMachine": "libQt6StateMachine.so"' in s,
    'precise vptr count': 'heap_vptr_hit_count' in s,
    'no raw title': '"raw_window_title_retained": False' in s,
    'no secrets': '"credentials_retained": False' in s and '"session_secrets_retained": False' in s,
    'no payload': '"packet_payloads_retained": False' in s,
    'no ingame claim': '"in_game_claimed": False' in s,
    'live task mode guard': 'LIVE_TASK_RUNTIME_ACCESS_REQUIRED=read_only' in w and 'LIVE_TASK_MUTATION_AUTHORIZED_REQUIRED=false' in w,
    'task current static phase allowed': ('runtime_access: none' in t or 'runtime_access: read_only' in t),
    'task no mutation': 'mutation_authorized: false' in t,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit('snapshot contract failed: ' + ', '.join(failed))
print('TRACK_A_CURRENT_QT_WORLD_SNAPSHOT_CONTRACT=PASS')
