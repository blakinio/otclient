from pathlib import Path

workflow = Path('.github/workflows/track-a-current-world-entered-anchor.yml')
script = Path('.github/scripts/track_a_current_world_entered_anchor.py')
test = Path('.github/scripts/test_track_a_current_world_entered_anchor.py')
durable = Path('.github/scripts/track_a_current_world_entered_durable_state.py')
durable_test = Path('.github/scripts/test_track_a_current_world_entered_durable_state.py')
task = Path('docs/agents/tasks/active/OTC-20260828-current-qt-world-correlation.md')
for path in (workflow, script, test, durable, durable_test, task):
    if not path.is_file():
        raise SystemExit(f'missing world-entered anchor surface: {path}')

w = workflow.read_text(encoding='utf-8')
s = script.read_text(encoding='utf-8')
d = durable.read_text(encoding='utf-8')
t = task.read_text(encoding='utf-8')
checks = {
    'github hosted': 'runs-on: ubuntu-24.04' in w,
    'official source': 'https://static.tibia.com/launcher/tibiaclient-linux-current/bin/client.lzma' in w,
    'packed fence': '075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f' in w,
    'unpacked fence': 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a' in w,
    'size fence': '52105824' in w,
    'warp binary pins': '2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c' in w and 'e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c' in w,
    'capstone': 'capstone' in w,
    'anchor invoked': 'track_a_current_world_entered_anchor.py' in w,
    'durable invoked': 'track_a_current_world_entered_durable_state.py' in w,
    'bounded json upload': 'world-entered-anchor.json' in w and 'world-entered-durable-state.json' in w,
    'no raw upload': 'client.lzma' not in w.split('uses: actions/upload-artifact', 1)[-1] and '/client/client' not in w.split('uses: actions/upload-artifact', 1)[-1],
    'no self hosted': 'runs-on: [otclient' not in w and 'runs-on: [self-hosted' not in w,
    'no runtime execution': 'docker exec' not in w and 'client_executed: true' not in w,
    'dynamic qmeta': 'recover_world_entered_anchor' in s and 'TARGET_CLASS' in s,
    'dynamic dispatch': 'recover_dispatch_case' in s and 'FULL_RANGE_DISPATCH_NOT_UNIQUE' in s,
    'activation boundary': 'recover_activation_boundary' in s and 'qmeta_activate_target_va' in s,
    'activation arguments': 'SIGNAL_INDEX_ARGUMENT_NOT_PROVEN' in s and 'STATIC_METAOBJECT_ARGUMENT_NOT_PROVEN' in s,
    'durable qmeta': 'recover_qmeta_class' in d and 'TGameSessionDisconnectReactionController' in d,
    'durable writes': 'extract_this_immediate_writes' in d and 'select_durable_field_candidate' in d,
    'writer case trace': 'writer_case_trace = extract_bounded_case_trace' in d,
    'display signal cases': 'game_window_display_signal_cases' in d and 'gameScreenNowDisplayed' in d and 'startScreenNowDisplayed' in d,
    'display signal emitters': 'game_window_display_signal_emitters' in d and 'scan_qmeta_signal_activation_sites' in d,
    'state literal decode': 'game_window_state_assignment_sources' in d and 'decode_static_qstring_source' in d,
    'state initializer xrefs': 'game_window_state_initializer_xrefs' in d and 'scan_rip_target_xrefs' in d,
    'durable fail closed': 'PROVEN_STATIC_SIMPLE_FIELD_CANDIDATE' in d and 'NOT_PROVEN' in d,
    'no historical address reuse': 'historical_address_reuse' in s and 'False' in s and 'historical_address_reuse' in d,
    'no ingame claim': 'in_game_claimed' in s and 'False' in s and 'in_game_claimed' in d,
    'task frontier': 'world_entered_exact_current_anchor: STATIC_QMETA_ACTIVATION_PROVEN_NOT_RUNTIME_VALIDATED' in t,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit('world-entered anchor contract failed: ' + ', '.join(failed))
print('TRACK_A_CURRENT_WORLD_ENTERED_ANCHOR_CONTRACT=PASS')
