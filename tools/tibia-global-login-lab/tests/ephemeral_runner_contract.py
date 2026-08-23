#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parents[3]
workflow = (root / '.github/workflows/tibia-global-login-lab.yml').read_text(encoding='utf-8')
prepare = (root / 'tools/tibia-global-login-lab/scripts/prepare-ephemeral-runtime.sh').read_text(encoding='utf-8')
clear_pid = (root / 'tools/tibia-global-login-lab/scripts/clear-stale-wireproxy-pid.sh').read_text(encoding='utf-8')

probe = workflow.index('  probe:')
build = workflow.index('      - name: Download exact native Linux binary', probe)
prep = workflow.index('      - name: Prepare ephemeral GitHub-hosted lab runtime', probe)
bootstrap = workflow.index('      - name: Verify and bootstrap isolated lab', probe)
clear_before_http = workflow.index('      - name: Clear stale WARP PID before HTTP container recreation', probe)
http = workflow.index('      - name: Verify redacted HTTP login transport', probe)
clear_before_world = workflow.index('      - name: Clear stale WARP PID before world-entry container recreation', probe)
world = workflow.index('      - name: Run controlled login and world-entry probe', probe)

assert 'runs-on: ubuntu-24.04' in workflow[probe:build]
assert "LAB_EPHEMERAL_HOSTED: '1'" in workflow[probe:build]
assert build < prep < bootstrap < clear_before_http < http < clear_before_world < world
assert workflow.count('bash tools/tibia-global-login-lab/scripts/clear-stale-wireproxy-pid.sh') == 2
assert 'cancel-in-progress: true' in workflow
assert 'TIBIA_TEST_EMAIL' not in workflow[prep:bootstrap]
assert 'TIBIA_TEST_PASSWORD' not in workflow[prep:bootstrap]

assert 'TIBIA_TEST_EMAIL' not in prepare
assert 'TIBIA_TEST_PASSWORD' not in prepare
assert 'wgcf" register --accept-tos' in prepare
assert '2ff97f2201972ce582a424455d50a3719a380eef0cd1f3144f7779348e122a2c' in prepare
assert 'e88c1d090740373fc606c1bafd81d9a5eadc642cce5667616e20e9d7a444f51c' in prepare
assert 'LAB_EPHEMERAL_WARP_CHANGED_EGRESS_VERIFIED=true' in prepare
assert 'docker commit "$CONTAINER" "$RUNTIME_IMAGE"' in prepare
assert 'RUNNER=github-hosted-ephemeral' in prepare

assert 'wireproxy.pid' in clear_pid
assert 'rm -f' in clear_pid
assert 'kill ' not in clear_pid
assert 'LAB_WIREPROXY_CROSS_CONTAINER_PID_CLEARED=true' in clear_pid

print('EPHEMERAL_RUNNER_CONTRACT=PASS')
