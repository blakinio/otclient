#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name('tibia-official-client-re-canonical-live-transition.py')
WORKER = Path(__file__).with_name('tibia-official-client-re-canonical-live-session.sh')
KASM_WORKER = Path(__file__).with_name('tibia-official-client-re-kasm-bootstrap-worker.py')
KASM_PROBE = Path(__file__).with_name('tibia-official-client-re-kasm-existing-runtime-probe.py')
KASM_CONTAINER_ID = 'a' * 64


def load():
    spec = importlib.util.spec_from_file_location('transition_tested', SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Manager:
    generation = 1

    def __init__(self, _):
        pass

    def _load_state_unlocked(self):
        return {'generation': self.generation}

    def _require_current_unlocked(self, state, _identity, token, _now):
        if state['generation'] != self.generation or token != 'token':
            raise RuntimeError('not current')


class Lease:
    LeaseManager = Manager

    @staticmethod
    def LeaseIdentity(task, session):
        return task, session

    @staticmethod
    def _read_private_token(_):
        return 'token'

    @staticmethod
    def _now_epoch(_=None):
        return 100


class Guard:
    _supervisor_cancel_signal = None


class Popen:
    def __init__(self, command, **kwargs):
        self.pid = 777
        self.command = command
        self.kwargs = kwargs

    def wait(self, timeout=None):
        return 0


class Tests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.m.STATE = root
        self.m.REG = root / 'runtime-registration.json'
        request_file = root / 'guarded-request.json'
        request_file.write_text(json.dumps({
            'schema_version': 1,
            'action_hash': 'a' * 64,
        }))
        self.args = argparse.Namespace(
            task_id='OTC-TEST', session_id='s', token_file=root / 'tok',
            worker=WORKER, probe=WORKER, worker_timeout=2,
            request_file=request_file, input_lock_timeout=0.2,
        )
        self.identity = {
            'boot_id_sha256': 'b' * 64,
            'pid': 4242,
            'process_start_ticks': 123,
            'client_size': self.m.SIZE,
            'client_sha256': self.m.SHA,
        }
        self.manifest = {
            'pid': 4242,
            'process_group_id': 777,
            'tracked_processes': {
                'client': 4242, 'xvfb': 4243, 'vnc': 4244, 'wireproxy': 4245,
            },
            'display': ':104',
            'window_identity': 'x11-window:9',
            'remote_view_endpoint': '127.0.0.1:6091',
            'remote_view_mapping': 'PROVEN',
            'state': 'UNKNOWN',
        }
        self.guard = Guard()

    def tearDown(self):
        self.temp.cleanup()

    def registration(self, lease_generation=1, registration_generation=1):
        return {
            'schema_version': 1,
            'runtime_id': self.m.RID,
            'registration_generation': registration_generation,
            'lease_generation': lease_generation,
            'registered_at': 1,
            'boot_id_sha256': self.identity['boot_id_sha256'],
            'pid': 4242,
            'process_start_ticks': self.identity['process_start_ticks'],
            'client_version': self.m.VER,
            'client_size': self.m.SIZE,
            'client_sha256': self.m.SHA,
            'display': self.manifest['display'],
            'window_identity': self.manifest['window_identity'],
            'remote_view_endpoint': self.manifest['remote_view_endpoint'],
            'remote_view_mapping': self.manifest['remote_view_mapping'],
            'state': self.manifest['state'],
            'source_task': 'old',
            'source_run': 'old',
        }

    def write(self, data):
        self.m.STATE.mkdir(parents=True, exist_ok=True)
        self.m.REG.write_text(json.dumps(data))
        self.m.REG.chmod(0o600)

    def common(self):
        return (
            mock.patch.object(self.m, '_ident', return_value=dict(self.identity)),
            mock.patch.object(self.m, '_exact', return_value=None),
            mock.patch.object(self.m, '_lease', return_value=1),
            mock.patch.object(self.m, '_assert_group_tracked', return_value=None),
        )

    def test_bootstrap_stages_then_commits_and_uses_exact_worker_argv(self):
        sequence = iter(([], [4242], [4242], [4242]))
        p1, p2, p3, p4 = self.common()
        calls = []

        def fake_probe(worker, path):
            calls.append(('probe', [str(worker), 'probe', str(path)]))
            return dict(self.manifest)

        with p1, p2, p3, p4, \
                mock.patch.object(self.m, '_candidates', side_effect=lambda: next(sequence)), \
                mock.patch.object(self.m.subprocess, 'Popen', side_effect=lambda command, **kwargs: (calls.append(('bootstrap', command)) or Popen(command, **kwargs))), \
                mock.patch.object(self.m, '_manifest', return_value=dict(self.manifest)), \
                mock.patch.object(self.m, '_probe', side_effect=fake_probe):
            self.m._bootstrap(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)

        data = self.m._read()
        self.assertEqual(data['lease_generation'], 1)
        self.assertEqual(stat.S_IMODE(self.m.REG.stat().st_mode), 0o600)
        self.assertEqual(
            calls[0][1],
            [str(WORKER), 'bootstrap', str(self.m.STATE / '.bootstrap-manifest.json')],
        )
        self.assertEqual(sum(item[0] == 'probe' for item in calls), 2)

    def test_bootstrap_failure_kills_group_rolls_worker_and_removes_registration(self):
        sequence = iter(([], [4242]))
        p1, p2, p3, p4 = self.common()
        killed = []
        rollbacks = []
        with p1, p2, p3, p4, \
                mock.patch.object(self.m, '_candidates', side_effect=lambda: next(sequence)), \
                mock.patch.object(self.m.subprocess, 'Popen', Popen), \
                mock.patch.object(self.m, '_manifest', return_value=dict(self.manifest)), \
                mock.patch.object(self.m, '_probe', side_effect=self.m.E('post_probe_failed')), \
                mock.patch.object(self.m, '_kill', side_effect=lambda pgid: killed.append(pgid)), \
                mock.patch.object(self.m, '_worker', side_effect=lambda worker, op, arg: rollbacks.append((op, arg))):
            with self.assertRaises(self.m.E):
                self.m._bootstrap(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertEqual(killed, [777])
        self.assertEqual(rollbacks, [('rollback', '777')])
        self.assertFalse(self.m.REG.exists())

    def test_rebind_postwrite_probe_failure_restores_exact_previous(self):
        old = self.registration(lease_generation=1, registration_generation=4)
        self.write(old)
        Manager.generation = 2
        calls = 0

        def probe_registration(*_args, **_kwargs):
            nonlocal calls
            calls += 1
            if calls in (1, 2):
                return old, dict(self.manifest)
            raise self.m.E('forced_final_probe_failure')

        try:
            with mock.patch.object(self.m, '_probe_reg', side_effect=probe_registration), \
                    mock.patch.object(self.m, '_lease', return_value=2):
                with self.assertRaisesRegex(self.m.E, 'forced_final_probe_failure'):
                    self.m._rebind(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
            self.assertEqual(self.m._read(), old)
        finally:
            Manager.generation = 1

    def test_rebind_refreshes_fail_closed_adoption_evidence_for_same_identity(self):
        old = self.adoption_manifest()
        old.update({
            'schema_version': 1,
            'runtime_id': self.m.RID,
            'registration_generation': 4,
            'lease_generation': 1,
            'registered_at': 1,
            'source_task': 'old',
            'source_run': 'old',
        })
        self.write(old)
        fresh = dict(self.adoption_manifest(), state_evidence='NO_STRUCTURAL_BRIDGE')
        Manager.generation = 2
        try:
            with mock.patch.object(
                    self.m, '_probe', side_effect=[dict(fresh), dict(fresh), dict(fresh)]), \
                    mock.patch.object(self.m, '_lease', return_value=2):
                self.m._rebind(
                    self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2
                )
            data = self.m._read()
            self.assertEqual(data['registration_generation'], 5)
            self.assertEqual(data['lease_generation'], 2)
            self.assertEqual(data['state'], 'UNKNOWN')
            self.assertEqual(data['state_evidence'], 'NO_STRUCTURAL_BRIDGE')
            self.assertEqual(
                self.m._stable_adoption_identity(data),
                self.m._stable_adoption_identity(old),
            )
        finally:
            Manager.generation = 1

    def test_rebind_fail_closed_evidence_refresh_rejects_stable_identity_drift(self):
        old = self.adoption_manifest()
        old.update({
            'schema_version': 1,
            'runtime_id': self.m.RID,
            'registration_generation': 4,
            'lease_generation': 1,
            'registered_at': 1,
            'source_task': 'old',
            'source_run': 'old',
        })
        self.write(old)
        changed = dict(
            self.adoption_manifest(),
            state_evidence='NO_STRUCTURAL_BRIDGE',
            candidate_fingerprint='d' * 64,
        )
        Manager.generation = 2
        try:
            with mock.patch.object(self.m, '_probe', return_value=changed), \
                    mock.patch.object(self.m, '_lease', return_value=2):
                with self.assertRaisesRegex(
                    self.m.E, 'registered_identity_candidate_fingerprint_mismatch'
                ):
                    self.m._rebind(
                        self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2
                    )
            self.assertEqual(self.m._read(), old)
        finally:
            Manager.generation = 1

    def test_stale_registration_recovery_replaces_only_fully_proven_stale_adoption_identity(self):
        old, fresh = self.recovery_pair()
        self.write(old)
        Manager.generation = 2
        try:
            with mock.patch.object(self.m, '_probe', side_effect=[dict(fresh), dict(fresh), dict(fresh)]), \
                    mock.patch.object(self.m, '_lease', return_value=2), \
                    mock.patch.object(self.m, '_kill') as killed:
                self.m._stale_registration_recovery(
                    self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2
                )
            data = self.m._read()
            self.assertEqual(data['registration_generation'], 5)
            self.assertEqual(data['lease_generation'], 2)
            self.assertEqual(data['pid'], fresh['pid'])
            self.assertEqual(data['process_start_ticks'], fresh['process_start_ticks'])
            self.assertEqual(data['candidate_fingerprint'], fresh['candidate_fingerprint'])
            self.assertEqual(data['state'], 'UNKNOWN')
            self.assertEqual(data['state_evidence'], 'NO_STRUCTURAL_BRIDGE')
            killed.assert_not_called()
        finally:
            Manager.generation = 1

    def test_stale_registration_recovery_rejects_partial_pid_start_replacement(self):
        old, fresh = self.recovery_pair()
        fresh['pid'] = old['pid']
        fresh['window_identity'] = old['window_identity']
        self.write(old)
        with mock.patch.object(self.m, '_probe', return_value=fresh), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'recovery_pid_start_pair_not_replaced'):
                self.m._stale_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), old)

    def test_stale_registration_recovery_rejects_boot_or_namespace_continuity_drift(self):
        for label, mutate, code in (
            ('boot', lambda d: d.__setitem__('boot_id_sha256', 'e' * 64), 'recovery_boot_identity_changed'),
            ('container', lambda d: d.__setitem__('runtime_locator', 'docker:other-container:newid'), 'recovery_runtime_namespace_changed'),
            ('display', lambda d: d.__setitem__('display', ':2'), 'recovery_display_changed'),
            ('endpoint', lambda d: d.__setitem__('remote_view_endpoint', 'https://other:6902/'), 'recovery_remote_view_endpoint_changed'),
        ):
            with self.subTest(label=label):
                old, fresh = self.recovery_pair(); mutate(fresh); self.write(old)
                with mock.patch.object(self.m, '_probe', return_value=fresh), mock.patch.object(self.m, '_lease', return_value=2):
                    with self.assertRaisesRegex(self.m.E, code):
                        self.m._stale_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
                self.assertEqual(self.m._read(), old)

    def test_stale_registration_recovery_rejects_non_fail_closed_or_non_adoption_registration(self):
        old, fresh = self.recovery_pair()
        for label, mutate, code in (
            ('state', lambda d: d.update(state='IN_GAME', state_evidence='BRIDGE_3_OF_3'), 'recovery_registration_state_not_fail_closed'),
            ('proof', lambda d: d.pop('proof_kind'), 'recovery_adoption_registration_required'),
        ):
            with self.subTest(label=label):
                candidate = dict(old); mutate(candidate); self.write(candidate)
                with mock.patch.object(self.m, '_probe') as probe:
                    with self.assertRaisesRegex(self.m.E, code):
                        self.m._stale_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
                probe.assert_not_called()

    def test_stale_registration_recovery_requires_newer_generation_and_valid_fingerprint(self):
        old, fresh = self.recovery_pair()
        self.write(old)
        with mock.patch.object(self.m, '_probe') as probe:
            with self.assertRaisesRegex(self.m.E, 'recovery_generation_not_newer'):
                self.m._stale_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        probe.assert_not_called()

        self.write(old)
        bad = dict(fresh, candidate_fingerprint='e' * 64)
        with mock.patch.object(self.m, '_probe', return_value=bad), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'recovery_candidate_fingerprint_invalid'):
                self.m._stale_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), old)

    def test_stale_registration_recovery_rejects_probe_drift_and_rolls_back_after_commit(self):
        old, fresh = self.recovery_pair()
        changed = dict(fresh, window_identity='x11:0x17:pid:646:class:client/Tibia:title_sha256:' + 'e' * 64)
        self.write(old)
        with mock.patch.object(self.m, '_probe', side_effect=[dict(fresh), changed]), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'recovery_identity_changed_before_commit'):
                self.m._stale_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), old)

        self.write(old)
        with mock.patch.object(self.m, '_probe', side_effect=[dict(fresh), dict(fresh), changed]), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'recovery_identity_changed_after_commit'):
                self.m._stale_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), old)

    def test_boot_epoch_recovery_accepts_reused_pid_after_new_boot(self):
        old, fresh = self.recovery_pair()
        fresh['boot_id_sha256'] = 'e' * 64
        fresh['pid'] = old['pid']
        fresh['window_identity'] = (
            f"x11:0x17:pid:{fresh['pid']}:class:client/Tibia:title_sha256:" + 'b' * 64
        )
        fresh['candidate_fingerprint'] = self.m._recovery_candidate_fingerprint(fresh)
        self.write(old)
        Manager.generation = 2
        try:
            with mock.patch.object(self.m, '_probe', side_effect=[dict(fresh), dict(fresh), dict(fresh)]), mock.patch.object(self.m, '_lease', return_value=2):
                self.m._boot_epoch_registration_recovery(
                    self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2
                )
            data = self.m._read()
            self.assertEqual(data['boot_id_sha256'], fresh['boot_id_sha256'])
            self.assertEqual(data['pid'], old['pid'])
            self.assertEqual(data['process_start_ticks'], fresh['process_start_ticks'])
        finally:
            Manager.generation = 1
    def test_boot_epoch_recovery_rejects_fail_closed_boundary_violations(self):
        base_old, base_fresh = self.recovery_pair()
        base_fresh['boot_id_sha256'] = 'e' * 64
        base_fresh['candidate_fingerprint'] = self.m._recovery_candidate_fingerprint(base_fresh)
        cases = (
            ('same_boot', lambda o, f: f.__setitem__('boot_id_sha256', o['boot_id_sha256']), 'boot_epoch_not_changed'),
            ('old_state', lambda o, f: o.update(state='IN_GAME', state_evidence='BRIDGE_3_OF_3'), 'boot_epoch_registration_state_not_fail_closed'),
            ('fresh_state', lambda o, f: f.update(state='IN_GAME', state_evidence='BRIDGE_3_OF_3'), 'boot_epoch_fresh_state_not_fail_closed'),
            ('namespace', lambda o, f: f.__setitem__('runtime_locator', 'docker:other-container:newid'), 'boot_epoch_runtime_namespace_changed'),
            ('display', lambda o, f: f.__setitem__('display', ':2'), 'boot_epoch_display_changed'),
            ('endpoint', lambda o, f: f.__setitem__('remote_view_endpoint', 'https://other:6902/'), 'boot_epoch_remote_view_endpoint_changed'),
            ('mapping', lambda o, f: f.__setitem__('remote_view_mapping', 'PROVEN'), 'boot_epoch_remote_view_mapping_changed'),
            ('fence', lambda o, f: f.__setitem__('client_sha256', 'f' * 64), 'boot_epoch_exact_client_fence_failed'),
            ('inventory', lambda o, f: f.__setitem__('candidate_count', 2), 'boot_epoch_target_not_unique'),
            ('window', lambda o, f: f.__setitem__('window_identity', 'x11:0x17:pid:999:class:client/Tibia:title_sha256:' + 'b' * 64), 'boot_epoch_window_identity_invalid'),
            ('fingerprint', lambda o, f: f.__setitem__('candidate_fingerprint', 'f' * 64), 'boot_epoch_candidate_fingerprint_invalid'),
        )
        for label, mutate, code in cases:
            with self.subTest(label=label):
                old, fresh = dict(base_old), dict(base_fresh)
                mutate(old, fresh)
                self.write(old)
                with mock.patch.object(self.m, '_probe', return_value=fresh), mock.patch.object(self.m, '_lease', return_value=2):
                    with self.assertRaisesRegex(self.m.E, code):
                        self.m._boot_epoch_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.write(base_old)
        with mock.patch.object(self.m, '_probe') as probe:
            with self.assertRaisesRegex(self.m.E, 'boot_epoch_generation_not_newer'):
                self.m._boot_epoch_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        probe.assert_not_called()
    def test_boot_epoch_recovery_rejects_probe_drift_and_registration_race(self):
        old, fresh = self.recovery_pair(); fresh['boot_id_sha256'] = 'e' * 64
        fresh['candidate_fingerprint'] = self.m._recovery_candidate_fingerprint(fresh)
        changed = dict(fresh, window_identity='x11:0x18:pid:646:class:client/Tibia:title_sha256:' + 'f' * 64)
        self.write(old)
        with mock.patch.object(self.m, '_probe', side_effect=[dict(fresh), changed]), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'boot_epoch_identity_changed_before_commit'):
                self.m._boot_epoch_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), old)
        self.write(old); other = dict(old, source_task='other'); calls = 0
        def racing_probe(*_args):
            nonlocal calls
            calls += 1
            if calls == 1: self.write(other)
            return dict(fresh)
        with mock.patch.object(self.m, '_probe', side_effect=racing_probe), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'boot_epoch_registration_changed_before_commit'):
                self.m._boot_epoch_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), other)

    def test_boot_epoch_recovery_rolls_back_only_exact_own_commit(self):
        old, fresh = self.recovery_pair(); fresh['boot_id_sha256'] = 'e' * 64
        fresh['candidate_fingerprint'] = self.m._recovery_candidate_fingerprint(fresh)
        changed = dict(fresh, window_identity='x11:0x18:pid:646:class:client/Tibia:title_sha256:' + 'f' * 64)
        self.write(old)
        with mock.patch.object(self.m, '_probe', side_effect=[dict(fresh), dict(fresh), changed]), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'boot_epoch_identity_changed_after_commit'):
                self.m._boot_epoch_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), old)
        self.write(old); concurrent = dict(old, registration_generation=99, lease_generation=99, source_task='concurrent'); calls = 0
        def conflicting_probe(*_args):
            nonlocal calls
            calls += 1
            if calls == 3:
                self.write(concurrent)
                return dict(fresh, window_identity='x11:changed')
            return dict(fresh)
        with mock.patch.object(self.m, '_probe', side_effect=conflicting_probe), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'boot_epoch_rollback_registration_conflict'):
                self.m._boot_epoch_registration_recovery(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), concurrent)

    def test_parser_accepts_boot_epoch_registration_recovery_probe_shape(self):
        parsed = self.m.parser().parse_args(['boot-epoch-registration-recovery', '--task-id', 'OTC-TEST', '--session-id', 's', '--token-file', str(Path(self.temp.name) / 'tok'), '--probe', str(WORKER)])
        self.assertEqual(parsed.operation, 'boot-epoch-registration-recovery')
    def test_parser_accepts_stale_registration_recovery_probe_shape(self):
        parsed = self.m.parser().parse_args([
            'stale-registration-recovery', '--task-id', 'OTC-TEST', '--session-id', 's',
            '--token-file', str(Path(self.temp.name) / 'tok'), '--probe', str(WORKER),
        ])
        self.assertEqual(parsed.operation, 'stale-registration-recovery')

    def test_sanitized_environment_removes_credentials_capabilities_and_test_switch(self):
        with mock.patch.dict(os.environ, {
            'TIBIA_TEST_EMAIL': 'mail',
            'TIBIA_TEST_PASSWORD': 'pw',
            'TRACK_A_CANONICAL_LEASE_TOKEN': 'x',
            'SOME_CAPABILITY': 'y',
            'TRACK_A_CANONICAL_WORKER_CONTRACT_TEST': '1',
            'SAFE': 'ok',
        }, clear=True):
            env = self.m._env()
        self.assertEqual(env, {'SAFE': 'ok'})

    def test_real_worker_parser_accepts_transition_shape_and_rejects_extra_arg(self):
        output = Path(self.temp.name) / 'manifest.json'
        env = dict(os.environ, TRACK_A_CANONICAL_WORKER_CONTRACT_TEST='1')
        good = self.m.subprocess.run([str(WORKER), 'probe', str(output)], env=env, check=False)
        self.assertEqual(good.returncode, 0)
        self.assertTrue(output.exists())
        bad = self.m.subprocess.run([str(WORKER), 'probe', str(output), 'extra'], env=env, check=False)
        self.assertNotEqual(bad.returncode, 0)

    def test_worker_has_no_login_or_historical_shared_wireproxy_dependency(self):
        source = WORKER.read_text()
        self.assertNotIn('login_e2e', source)
        self.assertNotIn('$BASE/runtime/wireproxy.pid', source)
        self.assertIn('OTCLIENT_TIBIA_RE_ROLE=wireproxy', source)
        self.assertIn('WGCF_VER=2.2.32', source)
        self.assertIn('WP_VER=1.1.3', source)

    def test_transition_reuses_cancellation_safe_supervisor_primitives(self):
        source = SCRIPT.read_text()
        self.assertIn('_install_supervisor_signal_handlers', source)
        self.assertIn('_become_child_subreaper', source)
        self.assertIn('signal.pthread_sigmask', source)
        self.assertIn('fcntl.flock', source)

    def test_safe_detach_rejects_untracked_process_group_member(self):
        expected = set(self.manifest['tracked_processes'].values())
        with mock.patch.object(self.m, '_group_members', return_value=expected):
            self.m._assert_group_tracked(self.manifest)
        with mock.patch.object(self.m, '_group_members', return_value=expected | {9999}):
            with self.assertRaisesRegex(self.m.E, 'bootstrap_process_group_untracked'):
                self.m._assert_group_tracked(self.manifest)

    def test_manifest_requires_tracked_processes_and_process_group(self):
        path = Path(self.temp.name) / 'manifest.json'
        data = dict(self.manifest)
        data.pop('tracked_processes')
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(self.m.E, 'probe_manifest_missing_fields'):
            self.m._manifest(path)

    def adoption_manifest(self):
        return {
            'proof_kind': self.m.ADOPTION_PROOF_KIND,
            'pid': 4242,
            'display': ':1',
            'window_identity': 'x11:0x9:pid:4242:class:client/Tibia:title_sha256:' + 'a' * 64,
            'remote_view_endpoint': 'https://synology:6902/',
            'remote_view_mapping': 'UNKNOWN',
            'state': 'UNKNOWN',
            'state_evidence': 'BRIDGE_3_OF_3_SEMANTICS_UNPROVEN',
            'boot_id_sha256': self.identity['boot_id_sha256'],
            'process_start_ticks': self.identity['process_start_ticks'],
            'client_version': self.m.VER,
            'client_size': self.m.SIZE,
            'client_sha256': self.m.SHA,
            'runtime_locator': 'docker:otclient-track-a-kasmvnc:abc123',
            'inventory_scope': 'all_running_docker_containers',
            'inventory_complete': True,
            'candidate_count': 1,
            'candidate_fingerprint': 'c' * 64,
        }

    def kasm_args(self):
        return argparse.Namespace(
            task_id='OTC-TEST', session_id='s', token_file=Path(self.temp.name) / 'tok',
            worker=KASM_WORKER, probe=KASM_PROBE, worker_timeout=2,
            request_file=self.args.request_file, input_lock_timeout=0.2,
        )

    def kasm_preflight(self):
        data = {
            'schema': 'otclient.track-a.kasm-bootstrap.preflight.v1',
            'container_name': 'otclient-track-a-kasmvnc',
            'container_id': KASM_CONTAINER_ID,
            'display': ':1',
            'package_dir': '/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia',
            'client_path': '/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client',
            'client_size': self.m.SIZE,
            'client_sha256': self.m.SHA,
            'boot_id_sha256': 'd' * 64,
            'candidate_count': 0,
            'main_window_count': 0,
        }
        data['preflight_fingerprint'] = hashlib.sha256(
            json.dumps(data, sort_keys=True, separators=(',', ':')).encode()
        ).hexdigest()
        return data

    def kasm_launch(self):
        preflight = self.kasm_preflight()
        return {
            'schema': 'otclient.track-a.kasm-bootstrap.launch.v1',
            'preflight_fingerprint': preflight['preflight_fingerprint'],
            'container_name': 'otclient-track-a-kasmvnc',
            'container_id': KASM_CONTAINER_ID,
            'display': ':1',
            'package_dir': '/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia',
            'client_path': '/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client',
            'client_size': self.m.SIZE,
            'client_sha256': self.m.SHA,
            'pid': 4242,
            'process_start_ticks': self.identity['process_start_ticks'],
            'launch_method': 'docker_exec_detached_direct_env',
            'bootstrap_helper_residue': False,
        }

    def kasm_manifest(self):
        data = self.adoption_manifest()
        data['runtime_locator'] = 'docker:otclient-track-a-kasmvnc:' + KASM_CONTAINER_ID
        data['candidate_fingerprint'] = hashlib.sha256(
            f"{data['runtime_locator']}:{data['pid']}:{data['process_start_ticks']}:"
            f"{data['client_size']}:{data['client_sha256']}".encode()
        ).hexdigest()
        return data

    def prior_boot_registration(self, *, lease_generation=1, container_id=None):
        data = self.adoption_manifest()
        data.update({
            'schema_version': 1,
            'runtime_id': self.m.RID,
            'registration_generation': 7,
            'lease_generation': lease_generation,
            'registered_at': 1,
            'boot_id_sha256': 'b' * 64,
            'state': 'UNKNOWN',
            'state_evidence': 'NO_STRUCTURAL_BRIDGE',
            'runtime_locator': 'docker:otclient-track-a-kasmvnc:' + (container_id or KASM_CONTAINER_ID[:12]),
            'source_task': 'old',
            'source_run': 'old',
        })
        return data

    def _preflight_worker_writer(self, calls, records):
        queue = [dict(record) for record in records]
        def worker(_worker, operation, argument):
            calls.append(operation)
            if operation != 'preflight':
                raise AssertionError(operation)
            if not queue:
                raise AssertionError('unexpected preflight call')
            path = Path(argument)
            path.write_text(json.dumps(queue.pop(0)))
            path.chmod(0o600)
        return worker

    def _kasm_worker_writer(self, calls, preflight=None, launch=None):
        preflight = dict(preflight or self.kasm_preflight())
        launch = dict(launch or self.kasm_launch())
        def worker(_worker, operation, argument):
            calls.append(operation)
            path = Path(argument)
            if operation == 'preflight':
                path.write_text(json.dumps(preflight))
                path.chmod(0o600)
            elif operation == 'launch':
                path.write_text(json.dumps(launch))
                path.chmod(0o600)
            elif operation != 'rollback':
                raise AssertionError(operation)
        return worker

    def recovery_pair(self):
        old = self.adoption_manifest()
        old.update({
            'schema_version': 1,
            'runtime_id': self.m.RID,
            'registration_generation': 4,
            'lease_generation': 1,
            'registered_at': 1,
            'pid': 19590,
            'process_start_ticks': 76611792,
            'window_identity': 'x11:0x9:pid:19590:class:client/Tibia:title_sha256:' + 'a' * 64,
            'runtime_locator': 'docker:otclient-track-a-kasmvnc:oldid',
            'candidate_fingerprint': 'c' * 64,
            'source_task': 'old',
            'source_run': 'old',
        })
        fresh = self.adoption_manifest()
        fresh.update({
            'pid': 646,
            'process_start_ticks': 1394843,
            'window_identity': 'x11:0x17:pid:646:class:client/Tibia:title_sha256:' + 'b' * 64,
            'runtime_locator': 'docker:otclient-track-a-kasmvnc:newid',
            'state_evidence': 'NO_STRUCTURAL_BRIDGE',
        })
        fresh['candidate_fingerprint'] = self.m._recovery_candidate_fingerprint(fresh)
        return old, fresh

    def test_boot_epoch_registration_invalidate_parser_accepts_worker_shape(self):
        args = self.kasm_args()
        parsed = self.m.parser().parse_args([
            'boot-epoch-registration-invalidate', '--task-id', args.task_id,
            '--session-id', args.session_id, '--token-file', str(args.token_file),
            '--worker', str(args.worker), '--worker-timeout', '90',
        ])
        self.assertEqual(parsed.operation, 'boot-epoch-registration-invalidate')
        self.assertEqual(parsed.worker, KASM_WORKER)
        self.assertEqual(parsed.worker_timeout, 90)

    def test_boot_epoch_registration_invalidate_removes_only_proven_prior_boot_registration(self):
        old = self.prior_boot_registration()
        self.write(old)
        calls = []
        current = self.kasm_preflight()
        args = self.kasm_args()
        with mock.patch.object(self.m, '_worker', side_effect=self._preflight_worker_writer(calls, [current, current, current])), \
                mock.patch.object(self.m, '_lease', return_value=2), \
                mock.patch.object(self.m, '_kill') as killed, \
                mock.patch.object(self.m, '_probe') as probe:
            self.m._boot_epoch_registration_invalidate(
                args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2
            )
        self.assertEqual(calls, ['preflight', 'preflight', 'preflight'])
        self.assertFalse(self.m.REG.exists())
        killed.assert_not_called()
        probe.assert_not_called()

    def test_boot_epoch_registration_invalidate_rejects_same_boot_and_non_newer_generation(self):
        args = self.kasm_args()
        same = self.kasm_preflight(); same['boot_id_sha256'] = 'b' * 64
        unsigned = dict(same); unsigned.pop('preflight_fingerprint')
        same['preflight_fingerprint'] = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        self.write(self.prior_boot_registration())
        calls = []
        with mock.patch.object(self.m, '_worker', side_effect=self._preflight_worker_writer(calls, [same])), \
                mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'invalidation_boot_epoch_not_changed'):
                self.m._boot_epoch_registration_invalidate(
                    args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2
                )
        self.assertTrue(self.m.REG.exists())
        self.write(self.prior_boot_registration(lease_generation=2))
        with mock.patch.object(self.m, '_worker') as worker:
            with self.assertRaisesRegex(self.m.E, 'invalidation_generation_not_newer'):
                self.m._boot_epoch_registration_invalidate(
                    args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2
                )
        worker.assert_not_called()

    def test_boot_epoch_registration_invalidate_rejects_registration_boundary_violations(self):
        args = self.kasm_args()
        cases = []
        non_adoption = self.registration(); cases.append(('proof', non_adoption, 'invalidation_adoption_registration_required'))
        ingame = self.prior_boot_registration(); ingame.update(state='IN_GAME', state_evidence='BRIDGE_3_OF_3'); cases.append(('state', ingame, 'invalidation_registration_not_fail_closed'))
        other = self.prior_boot_registration(); other['runtime_locator'] = 'docker:other-container:' + KASM_CONTAINER_ID[:12]; cases.append(('namespace', other, 'invalidation_runtime_namespace_mismatch'))
        bad_id = self.prior_boot_registration(container_id='e' * 12); cases.append(('container', bad_id, 'invalidation_container_identity_mismatch'))
        for label, registration, code in cases:
            with self.subTest(label=label):
                self.write(registration)
                calls = []
                with mock.patch.object(self.m, '_worker', side_effect=self._preflight_worker_writer(calls, [self.kasm_preflight()])), \
                        mock.patch.object(self.m, '_lease', return_value=2):
                    with self.assertRaisesRegex(self.m.E, code):
                        self.m._boot_epoch_registration_invalidate(
                            args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2
                        )
                self.assertTrue(self.m.REG.exists())

    def test_boot_epoch_registration_invalidate_rejects_preflight_drift_and_registration_race(self):
        args = self.kasm_args()
        old = self.prior_boot_registration(); self.write(old)
        first = self.kasm_preflight()
        changed = dict(first, container_id='e' * 64); unsigned = dict(changed); unsigned.pop('preflight_fingerprint')
        changed['preflight_fingerprint'] = hashlib.sha256(json.dumps(unsigned, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        calls = []
        with mock.patch.object(self.m, '_worker', side_effect=self._preflight_worker_writer(calls, [first, changed])), \
                mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'invalidation_preflight_changed'):
                self.m._boot_epoch_registration_invalidate(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), old)

        racer = dict(old, registration_generation=99, source_task='racer')
        self.write(old); calls = []; writes = 0
        def worker(_worker, operation, argument):
            nonlocal writes
            calls.append(operation); Path(argument).write_text(json.dumps(first)); Path(argument).chmod(0o600); writes += 1
            if writes == 2: self.write(racer)
        with mock.patch.object(self.m, '_worker', side_effect=worker), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'invalidation_registration_changed'):
                self.m._boot_epoch_registration_invalidate(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertEqual(self.m._read(), racer)

    def test_boot_epoch_registration_invalidate_postdelete_failure_never_restores_stale_registration(self):
        args = self.kasm_args(); old = self.prior_boot_registration(); self.write(old)
        current = self.kasm_preflight(); calls = []; count = 0
        def worker(_worker, operation, argument):
            nonlocal count
            calls.append(operation); count += 1
            if count == 3:
                raise self.m.E('official_client_candidate_count:1')
            Path(argument).write_text(json.dumps(current)); Path(argument).chmod(0o600)
        with mock.patch.object(self.m, '_worker', side_effect=worker), mock.patch.object(self.m, '_lease', return_value=2):
            with self.assertRaisesRegex(self.m.E, 'official_client_candidate_count'):
                self.m._boot_epoch_registration_invalidate(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 2)
        self.assertFalse(self.m.REG.exists())
        self.assertEqual(calls, ['preflight', 'preflight', 'preflight'])

    def test_kasm_bootstrap_parser_accepts_worker_and_probe_shape(self):
        args = self.kasm_args()
        parsed = self.m.parser().parse_args([
            'kasm-bootstrap', '--task-id', args.task_id, '--session-id', args.session_id,
            '--token-file', str(args.token_file), '--worker', str(args.worker),
            '--probe', str(args.probe), '--worker-timeout', '90',
        ])
        self.assertEqual(parsed.operation, 'kasm-bootstrap')
        self.assertEqual(parsed.worker, KASM_WORKER)
        self.assertEqual(parsed.probe, KASM_PROBE)
        self.assertEqual(parsed.worker_timeout, 90)

    def test_kasm_bootstrap_commits_adoption_compatible_unknown_registration(self):
        calls = []
        manifest = self.kasm_manifest()
        args = self.kasm_args()
        with mock.patch.object(self.m, '_worker', side_effect=self._kasm_worker_writer(calls)), \
                mock.patch.object(self.m, '_probe', side_effect=[dict(manifest), dict(manifest), dict(manifest)]), \
                mock.patch.object(self.m, '_lease', return_value=1), \
                mock.patch.object(self.m, '_kill') as killed:
            self.m._kasm_bootstrap(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        data = self.m._read()
        self.assertEqual(calls, ['preflight', 'launch'])
        self.assertEqual(data['proof_kind'], self.m.ADOPTION_PROOF_KIND)
        self.assertEqual(data['runtime_locator'], manifest['runtime_locator'])
        self.assertEqual(data['candidate_fingerprint'], manifest['candidate_fingerprint'])
        self.assertEqual(data['state'], 'UNKNOWN')
        self.assertEqual(data['bootstrap_provenance'], 'kasm_create_new_v1')
        self.assertEqual(data['lease_generation'], 1)
        killed.assert_not_called()

    def test_kasm_bootstrap_refuses_preexisting_registration_before_worker(self):
        self.write(self.registration())
        args = self.kasm_args()
        with mock.patch.object(self.m, '_worker') as worker:
            with self.assertRaisesRegex(self.m.E, 'registration_already_present'):
                self.m._kasm_bootstrap(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        worker.assert_not_called()

    def test_kasm_bootstrap_launch_probe_mismatch_rolls_exact_worker_only(self):
        calls = []
        manifest = dict(self.kasm_manifest(), pid=4243)
        args = self.kasm_args()
        with mock.patch.object(self.m, '_worker', side_effect=self._kasm_worker_writer(calls)), \
                mock.patch.object(self.m, '_probe', return_value=manifest), \
                mock.patch.object(self.m, '_lease', return_value=1), \
                mock.patch.object(self.m, '_kill') as killed:
            with self.assertRaisesRegex(self.m.E, 'kasm_bootstrap_manifest_pid_mismatch'):
                self.m._kasm_bootstrap(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertEqual(calls, ['preflight', 'launch', 'rollback'])
        self.assertFalse(self.m.REG.exists())
        killed.assert_not_called()

    def test_kasm_bootstrap_final_probe_failure_removes_own_registration_and_rolls_back(self):
        calls = []
        manifest = self.kasm_manifest()
        args = self.kasm_args()
        with mock.patch.object(self.m, '_worker', side_effect=self._kasm_worker_writer(calls)), \
                mock.patch.object(self.m, '_probe', side_effect=[dict(manifest), dict(manifest), self.m.E('final_probe_failed')]), \
                mock.patch.object(self.m, '_lease', return_value=1), \
                mock.patch.object(self.m, '_kill') as killed:
            with self.assertRaisesRegex(self.m.E, 'final_probe_failed'):
                self.m._kasm_bootstrap(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertEqual(calls, ['preflight', 'launch', 'rollback'])
        self.assertFalse(self.m.REG.exists())
        killed.assert_not_called()

    def test_kasm_bootstrap_lease_drift_before_launch_never_attempts_launch(self):
        calls = []
        args = self.kasm_args()
        with mock.patch.object(self.m, '_worker', side_effect=self._kasm_worker_writer(calls)), \
                mock.patch.object(self.m, '_lease', side_effect=self.m.E('lease_generation_changed')), \
                mock.patch.object(self.m, '_probe') as probe:
            with self.assertRaisesRegex(self.m.E, 'lease_generation_changed'):
                self.m._kasm_bootstrap(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertEqual(calls, ['preflight'])
        probe.assert_not_called()

    def test_kasm_bootstrap_registration_race_before_commit_preserves_racer(self):
        calls = []
        args = self.kasm_args()
        manifest = self.kasm_manifest()
        racer = self.registration(registration_generation=9)
        racer['source_task'] = 'racer'
        probes = 0
        def probe(*_args):
            nonlocal probes
            probes += 1
            if probes == 2:
                self.write(racer)
            return dict(manifest)
        with mock.patch.object(self.m, '_worker', side_effect=self._kasm_worker_writer(calls)), \
                mock.patch.object(self.m, '_probe', side_effect=probe), \
                mock.patch.object(self.m, '_lease', return_value=1):
            with self.assertRaisesRegex(self.m.E, 'kasm_bootstrap_registration_race'):
                self.m._kasm_bootstrap(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertEqual(calls, ['preflight', 'launch', 'rollback'])
        self.assertEqual(self.m._read(), racer)

    def test_kasm_bootstrap_concurrent_replacement_after_commit_is_preserved(self):
        calls = []
        args = self.kasm_args()
        manifest = self.kasm_manifest()
        concurrent = self.registration(lease_generation=99, registration_generation=99)
        concurrent['source_task'] = 'concurrent'
        probes = 0
        def probe(*_args):
            nonlocal probes
            probes += 1
            if probes == 3:
                self.write(concurrent)
                raise self.m.E('final_probe_failed')
            return dict(manifest)
        with mock.patch.object(self.m, '_worker', side_effect=self._kasm_worker_writer(calls)), \
                mock.patch.object(self.m, '_probe', side_effect=probe), \
                mock.patch.object(self.m, '_lease', return_value=1):
            with self.assertRaisesRegex(self.m.E, 'kasm_bootstrap_rollback_registration_conflict'):
                self.m._kasm_bootstrap(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertEqual(calls, ['preflight', 'launch', 'rollback'])
        self.assertEqual(self.m._read(), concurrent)

    def test_kasm_bootstrap_rollback_worker_failure_surfaces_fail_closed(self):
        calls = []
        args = self.kasm_args()
        mismatch = dict(self.kasm_manifest(), pid=4243)
        base_worker = self._kasm_worker_writer(calls)
        def worker(worker_path, operation, argument):
            if operation == 'rollback':
                calls.append(operation)
                raise self.m.E('rollback_refused')
            return base_worker(worker_path, operation, argument)
        with mock.patch.object(self.m, '_worker', side_effect=worker), \
                mock.patch.object(self.m, '_probe', return_value=mismatch), \
                mock.patch.object(self.m, '_lease', return_value=1):
            with self.assertRaisesRegex(self.m.E, 'kasm_bootstrap_rollback_failed'):
                self.m._kasm_bootstrap(args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertEqual(calls, ['preflight', 'launch', 'rollback'])
        self.assertFalse(self.m.REG.exists())

    def test_kasm_bootstrap_provenance_is_additive_and_validated(self):
        manifest = self.kasm_manifest()
        registration = dict(manifest)
        registration.update({
            'schema_version': 1, 'runtime_id': self.m.RID, 'registration_generation': 1,
            'lease_generation': 1, 'registered_at': 1, 'state': 'UNKNOWN',
            'bootstrap_provenance': 'kasm_create_new_v1', 'source_task': 'new', 'source_run': 'new',
        })
        self.write(registration)
        self.assertEqual(self.m._read()['bootstrap_provenance'], 'kasm_create_new_v1')
        registration['bootstrap_provenance'] = 'wrong'
        self.write(registration)
        with self.assertRaisesRegex(self.m.E, 'kasm_bootstrap_provenance_invalid'):
            self.m._read()

    def test_adopt_existing_commits_without_process_mutation(self):
        manifest = self.adoption_manifest()
        with mock.patch.object(self.m, '_probe', side_effect=[dict(manifest), dict(manifest), dict(manifest)]), \
                mock.patch.object(self.m, '_lease', return_value=1), \
                mock.patch.object(self.m, '_kill') as killed:
            self.m._adopt_existing(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        data = self.m._read()
        self.assertEqual(data['pid'], 4242)
        self.assertEqual(data['lease_generation'], 1)
        self.assertEqual(data['registration_generation'], 1)
        self.assertEqual(data['proof_kind'], self.m.ADOPTION_PROOF_KIND)
        self.assertEqual(data['runtime_locator'], manifest['runtime_locator'])
        self.assertEqual(data['candidate_fingerprint'], manifest['candidate_fingerprint'])
        self.assertEqual(data['state_evidence'], 'BRIDGE_3_OF_3_SEMANTICS_UNPROVEN')
        killed.assert_not_called()

    def test_adopt_existing_identity_drift_before_commit_leaves_no_registration(self):
        first = self.adoption_manifest()
        changed = dict(first, candidate_fingerprint='d' * 64)
        with mock.patch.object(self.m, '_probe', side_effect=[dict(first), changed]), \
                mock.patch.object(self.m, '_lease', return_value=1):
            with self.assertRaisesRegex(self.m.E, 'adoption_identity_changed_before_commit'):
                self.m._adopt_existing(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertFalse(self.m.REG.exists())

    def test_adopt_existing_postcommit_drift_rolls_registration_back_only(self):
        first = self.adoption_manifest()
        changed = dict(first, window_identity='x11:changed')
        with mock.patch.object(self.m, '_probe', side_effect=[dict(first), dict(first), changed]), \
                mock.patch.object(self.m, '_lease', return_value=1), \
                mock.patch.object(self.m, '_kill') as killed:
            with self.assertRaisesRegex(self.m.E, 'adoption_identity_changed_after_commit'):
                self.m._adopt_existing(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        self.assertFalse(self.m.REG.exists())
        killed.assert_not_called()

    def test_adopt_existing_refuses_preexisting_registration(self):
        self.write(self.registration())
        with mock.patch.object(self.m, '_probe') as probe:
            with self.assertRaisesRegex(self.m.E, 'registration_already_present'):
                self.m._adopt_existing(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        probe.assert_not_called()

    def test_adoption_manifest_requires_complete_unique_inventory(self):
        path = Path(self.temp.name) / 'adopt.json'
        data = self.adoption_manifest()
        data['candidate_count'] = 2
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(self.m.E, 'adoption_target_not_unique'):
            self.m._manifest(path)

    def test_adoption_manifest_rejects_ingame_even_with_legacy_bridge_marker(self):
        path = Path(self.temp.name) / 'adopt.json'
        data = self.adoption_manifest()
        data['state'] = 'IN_GAME'
        data['state_evidence'] = 'BRIDGE_3_OF_3'
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(self.m.E, 'adoption_ingame_semantics_unproven'):
            self.m._manifest(path)

    def legacy_stale_adoption_registration(self):
        data = self.adoption_manifest()
        data.update({
            'schema_version': 1,
            'runtime_id': self.m.RID,
            'registration_generation': 1,
            'lease_generation': 1,
            'registered_at': 1,
            'state': 'IN_GAME',
            'state_evidence': 'BRIDGE_3_OF_3',
            'source_task': 'old',
            'source_run': 'old',
        })
        return data

    def test_legacy_bridge_ingame_registration_is_readable_but_stale(self):
        old = self.legacy_stale_adoption_registration()
        self.write(old)
        loaded = self.m._read()
        self.assertEqual(loaded, old)
        self.assertTrue(self.m._adoption_semantics_stale(loaded))
        with mock.patch.object(self.m, '_lease', return_value=1), mock.patch.object(self.m, '_probe') as probe:
            with self.assertRaisesRegex(self.m.E, 'adoption_registration_semantics_stale'):
                self.m._probe_reg(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1, False)
        probe.assert_not_called()

    def test_semantic_downgrade_rewrites_only_stale_adoption_state(self):
        old = self.legacy_stale_adoption_registration()
        self.write(old)
        fresh = self.adoption_manifest()
        with mock.patch.object(self.m, '_probe', side_effect=[dict(fresh), dict(fresh), dict(fresh)]), mock.patch.object(self.m, '_lease', return_value=1):
            self.m._semantic_downgrade(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        data = self.m._read()
        self.assertEqual(data['state'], 'UNKNOWN')
        self.assertEqual(data['state_evidence'], 'BRIDGE_3_OF_3_SEMANTICS_UNPROVEN')
        self.assertEqual(data['registration_generation'], 2)
        self.assertEqual(data['lease_generation'], 1)
        self.assertEqual(data['pid'], old['pid'])
        self.assertEqual(data['candidate_fingerprint'], old['candidate_fingerprint'])

    def test_semantic_downgrade_refuses_nonlegacy_registration(self):
        current = self.adoption_manifest()
        current.update({
            'schema_version': 1, 'runtime_id': self.m.RID, 'registration_generation': 2,
            'lease_generation': 1, 'registered_at': 1, 'source_task': 'new', 'source_run': 'new',
        })
        self.write(current)
        with self.assertRaisesRegex(self.m.E, 'semantic_downgrade_not_required'):
            self.m._semantic_downgrade(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)

    def test_parser_accepts_semantic_downgrade_probe_shape(self):
        parsed = self.m.parser().parse_args([
            'semantic-downgrade', '--task-id', 'OTC-TEST', '--session-id', 's',
            '--token-file', str(Path(self.temp.name) / 'tok'), '--probe', str(WORKER),
        ])
        self.assertEqual(parsed.operation, 'semantic-downgrade')

    def test_adopted_registration_gate_match_binds_runtime_locator(self):
        manifest = self.adoption_manifest()
        with mock.patch.object(self.m, '_probe', side_effect=[dict(manifest), dict(manifest), dict(manifest)]), \
                mock.patch.object(self.m, '_lease', return_value=1):
            self.m._adopt_existing(self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1)
        registration = self.m._read()
        changed = dict(manifest, runtime_locator='docker:otclient-track-a-kasmvnc:different')
        with self.assertRaisesRegex(self.m.E, 'registered_identity_runtime_locator_mismatch'):
            self.m._match(changed, registration)

    def test_parser_accepts_adopt_existing_probe_shape(self):
        parsed = self.m.parser().parse_args([
            'adopt-existing', '--task-id', 'OTC-TEST', '--session-id', 's',
            '--token-file', str(Path(self.temp.name) / 'tok'), '--probe', str(WORKER),
        ])
        self.assertEqual(parsed.operation, 'adopt-existing')


    def test_parser_accepts_guarded_dispatch_shape(self):
        request_file = Path(self.temp.name) / 'request.json'
        parsed = self.m.parser().parse_args([
            'guarded-dispatch', '--task-id', 'OTC-TEST', '--session-id', 's',
            '--token-file', str(self.args.token_file), '--probe', str(WORKER),
            '--worker', str(WORKER), '--request-file', str(request_file),
            '--worker-timeout', '3',
        ])
        self.assertEqual(parsed.operation, 'guarded-dispatch')
        self.assertEqual(parsed.worker, WORKER)
        self.assertEqual(parsed.probe, WORKER)

    def test_guarded_dispatch_requires_gate_b_before_input_lock_and_worker(self):
        events = []
        with mock.patch.object(self.m, '_probe_reg', side_effect=self.m.E('gate_b_failed')), \
                mock.patch.object(self.m, '_acquire_input_lock', side_effect=lambda *_a, **_k: events.append('input-lock')), \
                mock.patch.object(self.m, '_run_guarded_worker', side_effect=lambda *_a, **_k: events.append('worker')):
            with self.assertRaisesRegex(self.m.E, 'gate_b_failed'):
                self.m._guarded_dispatch(
                    self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1
                )
        self.assertEqual(events, [])

    def test_guarded_dispatch_holds_input_lock_across_worker_transaction(self):
        events = []
        self.write(self.registration())

        class Held:
            def __enter__(self):
                events.append('input-lock-enter')
            def __exit__(self, *_exc):
                events.append('input-lock-exit')

        def worker(*_args, **_kwargs):
            events.append('worker')
            return {'status': 'ABORTED', 'effect_count': 0}

        with mock.patch.object(self.m, '_probe_reg', return_value=(self.registration(), dict(self.manifest))), \
                mock.patch.object(self.m, '_acquire_input_lock', return_value=Held()), \
                mock.patch.object(self.m, '_emit_guarded_ready', return_value=None), \
                mock.patch.object(self.m, '_read_guarded_decision', return_value='COMMIT'), \
                mock.patch.object(self.m, '_run_guarded_worker', side_effect=worker):
            result = self.m._guarded_dispatch(
                self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1
            )
        self.assertEqual(result['effect_count'], 0)
        self.assertEqual(events, ['input-lock-enter', 'worker', 'input-lock-exit'])

    def test_guarded_decision_accepts_only_exact_commit_or_abort(self):
        import io
        self.assertEqual(self.m._read_guarded_decision(io.StringIO('COMMIT\n')), 'COMMIT')
        self.assertEqual(self.m._read_guarded_decision(io.StringIO('ABORT\n')), 'ABORT')
        for raw in ('commit\n', 'COMMIT extra\n', '\n', ''):
            with self.subTest(raw=raw):
                with self.assertRaisesRegex(self.m.E, 'guarded_dispatch_decision_invalid'):
                    self.m._read_guarded_decision(io.StringIO(raw))

    def test_guarded_request_rejects_nested_raw_runtime_field(self):
        path = Path(self.temp.name) / 'raw-request.json'
        path.write_text(json.dumps({
            'schema_version': 1,
            'action_hash': 'a' * 64,
            'parameters': {'pid': 123},
        }))
        with self.assertRaisesRegex(self.m.E, 'guarded_dispatch_request_raw_field_forbidden'):
            self.m._read_guarded_request(path)

    def test_guarded_worker_result_rejects_extra_raw_fields(self):
        def fake_run(*_args, **_kwargs):
            (self.m.STATE / '.guarded-dispatch-result.json').write_text(json.dumps({
                'status': 'CONFIRMED',
                'effect_count': 1,
                'action_hash': 'a' * 64,
                'pid': 123,
            }))
            return mock.Mock(returncode=0)

        with mock.patch.object(self.m.subprocess, 'run', side_effect=fake_run):
            with self.assertRaisesRegex(self.m.E, 'guarded_dispatch_worker_result_invalid'):
                self.m._run_guarded_worker(self.args, {'action_hash': 'a' * 64})

    def test_commit_revalidates_gate_b_before_worker(self):
        events = []
        registration = self.registration()
        calls = 0

        class Held:
            def __enter__(self):
                events.append('input-lock-enter')
            def __exit__(self, *_exc):
                events.append('input-lock-exit')

        def probe(*_args, **_kwargs):
            nonlocal calls
            calls += 1
            events.append(f'gate-b-{calls}')
            if calls == 3:
                raise self.m.E('identity_changed_before_commit')
            return registration, dict(self.manifest)

        self.args.request_file = Path(self.temp.name) / 'request.json'
        self.args.request_file.write_text('{"schema_version":1,"action_hash":"' + ('a' * 64) + '"}')
        with mock.patch.object(self.m, '_probe_reg', side_effect=probe), \
                mock.patch.object(self.m, '_acquire_input_lock', return_value=Held()), \
                mock.patch.object(self.m, '_read_guarded_decision', return_value='COMMIT'), \
                mock.patch.object(self.m, '_emit_guarded_ready', side_effect=lambda *_a: events.append('ready')), \
                mock.patch.object(self.m, '_run_guarded_worker', side_effect=lambda *_a, **_k: events.append('worker')):
            with self.assertRaisesRegex(self.m.E, 'identity_changed_before_commit'):
                self.m._guarded_dispatch(
                    self.args, self.guard, Lease, Manager(self.m.STATE), ('t', 's'), 1
                )
        self.assertNotIn('worker', events)
        self.assertEqual(events[:5], ['gate-b-1', 'input-lock-enter', 'gate-b-2', 'ready', 'gate-b-3'])


if __name__ == '__main__':
    unittest.main()
