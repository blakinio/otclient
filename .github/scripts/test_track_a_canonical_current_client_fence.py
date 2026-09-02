#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CURRENT_VERSION = '15.32.be4f48'
CURRENT_SIZE = 52_105_824
CURRENT_SHA = '552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1'
PREVIOUS_VERSION = '15.32.75d4a0'
PREVIOUS_SHA = 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
LEGACY_SIZE = 52_109_920
LEGACY_SHA = 'ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8'
STALE_CURRENT_SENTENCE = (
    f'The current public native-Linux package is fenced exactly as `{PREVIOUS_VERSION} / '
    f'{CURRENT_SIZE} / {PREVIOUS_SHA}`.'
)

PROMOTION = ROOT / 'docs/agents/evidence/OTC-20260902-canonical-current-client-fence-be4f48/result.json'
WORKER = ROOT / '.github/scripts/tibia-official-client-re-canonical-live-session.sh'
TRANSITION = ROOT / '.github/scripts/tibia-official-client-re-canonical-live-transition.py'
ADOPTION = ROOT / '.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py'
BOOTSTRAP_WORKER = ROOT / '.github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py'
CONTROL_CENTER_ADMISSION = ROOT / 'tools/tibia_re_control_center/agent_runtime_admission.py'
TRACKS = ROOT / 'docs/agents/TIBIA_RESEARCH_TRACKS.md'
ADR = ROOT / 'docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md'
BOOTSTRAP = ROOT / 'docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md'
RUNTIME_ADMISSION = ROOT / 'docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md'
GOVERNANCE = ROOT / '.github/workflows/track-a-canonical-live-governance.yml'
KASM_BOOTSTRAP_WORKFLOW = ROOT / '.github/workflows/track-a-kasm-canonical-bootstrap.yml'
CHANGELOG = ROOT / 'docs/agents/CHANGELOG.md'


def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def assert_python_constants(text: str, label: str) -> None:
    expected = (
        (r"^VER\s*=\s*['\"]([^'\"]+)['\"]", CURRENT_VERSION),
        (r'^SIZE\s*=\s*([0-9_]+)', str(CURRENT_SIZE)),
        (r"^SHA\s*=\s*['\"]([0-9a-f]+)['\"]", CURRENT_SHA),
    )
    for pattern, value in expected:
        match = re.search(pattern, text, flags=re.MULTILINE)
        assert match is not None, f'{label}: missing {pattern}'
        actual = match.group(1).replace('_', '')
        assert actual == value.replace('_', ''), f'{label}: {actual} != {value}'


def assert_current_governance_fence(text: str, label: str) -> None:
    assert CURRENT_VERSION in text, f'{label}: current build version missing'
    assert str(CURRENT_SIZE) in text.replace('_', ''), f'{label}: current client size missing'
    assert CURRENT_SHA in text, f'{label}: current client SHA missing'
    assert STALE_CURRENT_SENTENCE not in text, f'{label}: previous build still described as current'


def main() -> None:
    promoted = json.loads(read(PROMOTION))
    exact = promoted['exact_client']
    assert exact['version'] == CURRENT_VERSION
    assert exact['size'] == CURRENT_SIZE
    assert exact['sha256'] == CURRENT_SHA
    assert promoted['decision'] == 'PASS_EXACT_OFFICIAL_LAUNCHER_CURRENT_BUILD_PROVEN'

    assert_current_governance_fence(read(RUNTIME_ADMISSION), 'runtime admission contract')
    assert_current_governance_fence(read(CONTROL_CENTER_ADMISSION), 'Control Center runtime admission')

    worker = read(WORKER)
    assert re.search(rf'^SIZE={CURRENT_SIZE}$', worker, flags=re.MULTILINE), 'canonical session worker: stale client size'
    assert re.search(rf'^SHA={CURRENT_SHA}$', worker, flags=re.MULTILINE), 'canonical session worker: stale client SHA'
    assert LEGACY_SHA not in worker, 'canonical session worker: legacy SHA remains authoritative'

    for label, path in (
        ('canonical transition', TRANSITION),
        ('existing-runtime adoption probe', ADOPTION),
        ('Kasm bootstrap worker', BOOTSTRAP_WORKER),
    ):
        assert_python_constants(read(path), label)

    for label, path in (
        ('Track A research contract', TRACKS),
        ('canonical runtime ADR', ADR),
        ('canonical bootstrap contract', BOOTSTRAP),
    ):
        assert_current_governance_fence(read(path), label)

    governance = read(GOVERNANCE)
    assert f"fence = '{CURRENT_SHA}'" in governance, 'canonical-live governance: stale exact-fence audit'

    kasm_workflow = read(KASM_BOOTSTRAP_WORKFLOW)
    assert f'EXPECTED_VERSION: {CURRENT_VERSION}' in kasm_workflow, 'Kasm bootstrap workflow: stale version'
    assert f'EXPECTED_SHA: {CURRENT_SHA}' in kasm_workflow, 'Kasm bootstrap workflow: stale SHA'

    changelog = read(CHANGELOG)
    assert f'Track A canonical exact-client fence advances to `{CURRENT_VERSION}`' in changelog, 'changelog: current canonical fence entry missing'

    print('TRACK_A_CANONICAL_CURRENT_CLIENT_FENCE=PASS')


if __name__ == '__main__':
    main()
