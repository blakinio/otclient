#!/usr/bin/env python3
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / '.github/workflows/track-a-kasm-canonical-bootstrap.yml'
TASK = ROOT / 'docs/agents/tasks/active/OTC-20260829-track-a-kasm-canonical-bootstrap.md'


def job_block(text: str, name: str) -> str:
    match = re.search(
        rf'(?ms)^  {re.escape(name)}:\s*\n(?P<body>.*?)(?=^  [A-Za-z0-9_.-]+:\s*\n|\Z)',
        text,
    )
    if not match:
        raise AssertionError(f'job missing: {name}')
    return match.group('body')


class Tests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text(encoding='utf-8')
        self.task = TASK.read_text(encoding='utf-8')

    def test_pr_and_owner_main_dispatch_are_separate_surfaces(self):
        self.assertIn('pull_request:', self.text)
        self.assertIn('workflow_dispatch:', self.text)
        contract = job_block(self.text, 'contract')
        live = job_block(self.text, 'live-bootstrap')
        self.assertIn("github.event_name == 'pull_request'", contract)
        self.assertIn('runs-on: ubuntu-24.04', contract)
        prefix = live.split('runs-on:', 1)[0]
        for required in (
            "github.event_name == 'workflow_dispatch'",
            'github.actor == github.repository_owner',
            "github.ref == 'refs/heads/main'",
            "inputs.authorization == 'INVALIDATE_PRIOR_BOOT_THEN_CREATE_NEW_KASM_CANONICAL_BOOTSTRAP'",
        ):
            self.assertIn(required, prefix)
        self.assertNotIn('pull_request', prefix)
        self.assertIn('runs-on: [otclient, synology]', live)

    def test_live_job_is_non_secret_and_attempt_one_before_process_control(self):
        live = job_block(self.text, 'live-bootstrap')
        for forbidden in ('${{ secrets.', 'TIBIA_TEST_EMAIL', 'TIBIA_TEST_PASSWORD'):
            self.assertNotIn(forbidden, self.text)
        self.assertNotIn('uses: actions/checkout', live)
        self.assertNotIn('github.token', live)
        self.assertIn('permissions: {}', live)
        self.assertIn('git clone', live)
        attempt = live.index('GITHUB_RUN_ATTEMPT')
        consumed = live.index('bootstrap-attempt-consumed.json')
        recovery_lease = live.index('RECOVERY_LEASE_ACQUIRE')
        invalidation = live.index('boot-epoch-registration-invalidate')
        bootstrap_lease = live.index('BOOTSTRAP_LEASE_ACQUIRE')
        launch = live.index('python3 "$transition" kasm-bootstrap')
        self.assertLess(attempt, consumed)
        self.assertLess(consumed, recovery_lease)
        self.assertLess(recovery_lease, invalidation)
        self.assertLess(invalidation, bootstrap_lease)
        self.assertLess(bootstrap_lease, launch)
        self.assertEqual(live.count('python3 "$transition" boot-epoch-registration-invalidate'), 1)
        self.assertEqual(live.count('python3 "$transition" kasm-bootstrap'), 1)
        self.assertNotIn('docker exec -d', live)
        self.assertNotIn('docker stop', live)
        self.assertNotIn('docker restart', live)
        self.assertNotIn('docker rm', live)

    def test_live_task_admission_is_exact_and_separate(self):
        live = job_block(self.text, 'live-bootstrap')
        self.assertIn('OTC-20260829-track-a-kasm-canonical-bootstrap-invalidation-live.md', live)
        recovery_required = (
            'runtime_access: canonical_recovery',
            'runtime_owner_task: OTC-20260829-track-a-kasm-canonical-bootstrap-invalidation-live',
            'runtime_namespace: canonical-live-runtime',
            'canonical_registration: PRESENT',
            'canonical_lease_generation: UNKNOWN',
            'gate_a: REQUIRED_NOT_PROVEN',
            'generation_rebind: NOT_APPLICABLE',
            'gate_b: NOT_APPLICABLE',
            'bootstrap: NOT_APPLICABLE',
            'target_uniqueness: UNKNOWN',
            'mutation_authorized: false',
            'recovery_mode: prior_boot_zero_client_invalidation_v1',
            'credentials_allowed: false',
            'login_allowed: false',
            'process_control_authorized: false',
            'physical_action_budget: 0',
        )
        for exact in recovery_required:
            key, value = exact.split(': ', 1)
            self.assertIn(f"'{key}': '{value}'", live)

        self.assertIn('OTC-20260829-track-a-kasm-canonical-bootstrap-live.md', live)
        bootstrap_required = (
            'runtime_access: canonical_bootstrap',
            'runtime_owner_task: OTC-20260829-track-a-kasm-canonical-bootstrap-live',
            'runtime_namespace: canonical-live-runtime',
            'canonical_registration: ABSENT',
            'canonical_lease_generation: UNKNOWN',
            'registration_lease_generation: NOT_APPLICABLE',
            'gate_a: REQUIRED_NOT_PROVEN',
            'generation_rebind: NOT_APPLICABLE',
            'gate_b: NOT_APPLICABLE',
            'bootstrap: PASS',
            'target_uniqueness: UNKNOWN',
            'mutation_authorized: true',
            'bootstrap_mode: create_new',
            'bootstrap_attempt_limit: 1',
            'credentials_allowed: false',
            'login_allowed: false',
            'relogin_allowed: false',
            'character_selection_allowed: false',
            'gameplay_allowed: false',
            'gui_input_authorized: false',
            'process_control_authorized: true',
            'physical_action_budget: 1',
            'physical_action_count: 0',
        )
        for exact in bootstrap_required:
            key, value = exact.split(': ', 1)
            self.assertIn(f"'{key}': '{value}'", live)
        self.assertIn('live_runtime_authorization_source', live)
        self.assertGreaterEqual(live.count('check_task('), 3)
        self.assertIn('validate_track_a_task', live)

    def test_implementation_task_remains_repository_only(self):
        frontmatter = self.task.split('---', 2)[1]
        for exact in (
            'runtime_access: none',
            'mutation_authorized: false',
            'credentials_allowed: false',
            'login_allowed: false',
            'gui_input_authorized: false',
            'process_control_authorized: false',
            'process_memory_access_allowed: false',
            'physical_action_budget: 0',
            'physical_action_count: 0',
        ):
            self.assertIn(exact, frontmatter)

    def test_hosted_contract_runs_focused_security_and_runtime_regressions(self):
        contract = job_block(self.text, 'contract')
        for required in (
            'test_tibia_official_client_re_kasm_bootstrap_worker.py',
            'test_tibia_official_client_re_canonical_live_transition.py',
            'test_tibia_official_client_re_kasm_existing_runtime_probe.py',
            'test_track_a_kasm_canonical_bootstrap_workflow.py',
            'test_track_a_agent_runtime_governance.py',
            'audit_track_a_selfhosted_pr_boundary.py',
            'git diff --check',
            'YAML_PARSE=PASS',
        ):
            self.assertIn(required, contract)

    def test_live_transaction_uses_merged_controller_not_inline_docker_launch(self):
        live = job_block(self.text, 'live-bootstrap')
        self.assertIn('tibia-official-client-re-canonical-live-transition.py', live)
        self.assertIn('tibia-official-client-re-kasm-bootstrap-worker.py', live)
        self.assertIn('tibia-official-client-re-kasm-existing-runtime-probe.py', live)
        self.assertIn('python3 "$transition" boot-epoch-registration-invalidate', live)
        self.assertIn('TRACK_A_KASM_CANONICAL_INVALIDATION_RELEASE=PASS', live)
        self.assertIn('python3 "$transition" kasm-bootstrap', live)
        self.assertIn('TRACK_A_KASM_CANONICAL_BOOTSTRAP_RELEASE=PASS', live)
        self.assertIn('TRACK_A_KASM_CANONICAL_INVALIDATION_REGISTRATION_ABSENT=PASS', live)
        self.assertIn('bootstrap_provenance', live)
        self.assertIn("'kasm_create_new_v1'", live)
        self.assertIn("'state') == 'UNKNOWN'", live)
        self.assertIn('PROCESS_MEMORY_OBSERVATION=false', live)
        self.assertIn('CREDENTIAL_ACCESS=false', live)


if __name__ == '__main__':
    unittest.main()
