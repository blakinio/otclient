#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
        self.args = argparse.Namespace(
            task_id='OTC-TEST', session_id='s', token_file=root / 'tok',
            worker=WORKER, probe=WORKER, worker_timeout=2,
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
