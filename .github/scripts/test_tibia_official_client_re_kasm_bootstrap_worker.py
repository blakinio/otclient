#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('tibia-official-client-re-kasm-bootstrap-worker.py')
FULL_ID = 'a' * 64
OTHER_ID = 'b' * 64


def load():
    spec = importlib.util.spec_from_file_location('kasm_bootstrap_worker_tested', SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeRunner:
    def __init__(self, module):
        self.m = module
        self.calls: list[tuple[str, ...]] = []
        self.containers = [(FULL_ID, module.TARGET_CONTAINER)]
        self.display_ok = True
        self.package = {
            'path': module.CLIENT_PATH,
            'regular': True,
            'symlink': False,
            'executable': True,
            'size': module.SIZE,
            'sha256': module.SHA,
        }
        self.candidates: dict[str, list[dict[str, object]]] = {FULL_ID: []}
        self.window_tree = '0x100 "Desktop": ()  1920x1080+0+0\n'
        self.process_identity: dict[int, dict[str, object]] = {}

    def __call__(self, command):
        cmd = tuple(str(value) for value in command)
        self.calls.append(cmd)
        if cmd[:4] == ('docker', 'ps', '--no-trunc', '--format'):
            return ''.join(f'{cid}\t{name}\n' for cid, name in self.containers)
        if 'xdpyinfo' in cmd:
            if not self.display_ok:
                raise self.m.WorkerError('command_failed')
            return 'DISPLAY_OK\n'
        if len(cmd) >= 6 and cmd[:2] == ('docker', 'exec') and cmd[-3:-1] == ('python3', '-c'):
            raise AssertionError(f'unrecognized python command shape: {cmd!r}')
        if len(cmd) >= 7 and cmd[:2] == ('docker', 'exec') and cmd[-4:-2] == ('python3', '-c'):
            script = cmd[-2]
            if script == self.m.PACKAGE_IDENTITY_SCRIPT:
                return json.dumps(self.package) + '\n'
            if script == self.m.CANDIDATE_SCRIPT:
                container_id = cmd[2]
                return json.dumps(self.candidates.get(container_id, [])) + '\n'
            if script == self.m.PROCESS_IDENTITY_SCRIPT:
                pid = int(cmd[-1])
                value = self.process_identity.get(pid)
                if value is None:
                    return json.dumps({'present': False}) + '\n'
                return json.dumps(value) + '\n'
            raise AssertionError(f'unrecognized python script: {cmd!r}')
        if 'xwininfo' in cmd:
            return self.window_tree
        if cmd[:3] == ('docker', 'exec', '-d'):
            return ''
        if '/bin/kill' in cmd:
            pid = int(cmd[-1])
            signal = cmd[-2]
            if signal in {'-TERM', '-KILL'}:
                self.process_identity.pop(pid, None)
            return ''
        raise AssertionError(f'unexpected command: {cmd!r}')


class Tests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.fake = FakeRunner(self.m)
        self.temp = tempfile.TemporaryDirectory()
        self.record = Path(self.temp.name) / 'record.json'

    def tearDown(self):
        self.temp.cleanup()

    def exact_candidate(self, pid=321, start=654, container_id=FULL_ID):
        return {
            'readable': True,
            'pid': pid,
            'exe': self.m.CLIENT_PATH,
            'size': self.m.SIZE,
            'sha256': self.m.SHA,
            'start_ticks': start,
            'official_hint': True,
            'container_id': container_id,
        }

    def exact_process_identity(self, pid=321, start=654):
        return {
            'present': True,
            'pid': pid,
            'exe': self.m.CLIENT_PATH,
            'size': self.m.SIZE,
            'sha256': self.m.SHA,
            'start_ticks': start,
        }

    def write_preflight(self):
        payload = self.m.collect_preflight(runner=self.fake)
        self.m.write_record(self.record, payload)
        return payload

    def test_preflight_accepts_only_zero_client_exact_kasm_target(self):
        payload = self.m.collect_preflight(runner=self.fake)
        self.assertEqual(payload['schema'], self.m.PREFLIGHT_SCHEMA)
        self.assertEqual(payload['container_name'], self.m.TARGET_CONTAINER)
        self.assertEqual(payload['container_id'], FULL_ID)
        self.assertEqual(payload['display'], self.m.TARGET_DISPLAY)
        self.assertEqual(payload['client_path'], self.m.CLIENT_PATH)
        self.assertEqual(payload['client_size'], self.m.SIZE)
        self.assertEqual(payload['client_sha256'], self.m.SHA)
        self.assertEqual(payload['candidate_count'], 0)
        self.assertEqual(payload['main_window_count'], 0)
        self.assertRegex(payload['preflight_fingerprint'], r'^[0-9a-f]{64}$')

    def test_preflight_rejects_target_container_cardinality_and_bad_full_id(self):
        for label, containers, code in (
            ('missing', [], 'target_container_count'),
            ('multiple', [(FULL_ID, self.m.TARGET_CONTAINER), (OTHER_ID, self.m.TARGET_CONTAINER)], 'target_container_count'),
            ('short-id', [('abc123', self.m.TARGET_CONTAINER)], 'target_container_id_invalid'),
        ):
            with self.subTest(label=label):
                self.fake.containers = containers
                with self.assertRaisesRegex(self.m.WorkerError, code):
                    self.m.collect_preflight(runner=self.fake)

    def test_preflight_rejects_display_or_package_identity_failure(self):
        self.fake.display_ok = False
        with self.assertRaisesRegex(self.m.WorkerError, 'display_unavailable'):
            self.m.collect_preflight(runner=self.fake)
        self.fake.display_ok = True
        for field, value, code in (
            ('regular', False, 'client_not_regular'),
            ('symlink', True, 'client_symlinked'),
            ('executable', False, 'client_not_executable'),
            ('size', self.m.SIZE + 1, 'client_size_mismatch'),
            ('sha256', '0' * 64, 'client_sha256_mismatch'),
        ):
            with self.subTest(field=field):
                self.fake.package = dict(self.fake.package)
                self.fake.package[field] = value
                with self.assertRaisesRegex(self.m.WorkerError, code):
                    self.m.collect_preflight(runner=self.fake)
                self.fake.package = {
                    'path': self.m.CLIENT_PATH, 'regular': True, 'symlink': False,
                    'executable': True, 'size': self.m.SIZE, 'sha256': self.m.SHA,
                }

    def test_preflight_rejects_existing_or_unverifiable_official_candidate(self):
        for label, row, code in (
            ('exact', self.exact_candidate(), 'official_client_candidate_count'),
            ('wrong-sha', dict(self.exact_candidate(), sha256='0' * 64), 'conflicting_official_client_candidate'),
            ('unreadable', {'readable': False, 'pid': 55, 'official_hint': True}, 'official_client_candidate_unverifiable'),
        ):
            with self.subTest(label=label):
                self.fake.candidates[FULL_ID] = [row]
                with self.assertRaisesRegex(self.m.WorkerError, code):
                    self.m.collect_preflight(runner=self.fake)
        self.fake.candidates[FULL_ID] = []

    def test_preflight_rejects_existing_tibia_main_window(self):
        self.fake.window_tree = '  0x200 "Tibia": ("client" "Tibia")  1200x800+0+0\n'
        with self.assertRaisesRegex(self.m.WorkerError, 'main_window_count'):
            self.m.collect_preflight(runner=self.fake)

    def test_launch_revalidates_preflight_then_binds_one_new_exact_client(self):
        preflight = self.write_preflight()
        candidate = self.exact_candidate()
        calls = 0
        original = self.fake.__call__

        def runner(command):
            nonlocal calls
            cmd = tuple(str(value) for value in command)
            if cmd[:3] == ('docker', 'exec', '-d'):
                result = original(command)
                self.fake.candidates[FULL_ID] = [candidate]
                calls += 1
                return result
            return original(command)

        launch = self.m.launch_from_preflight(self.record, runner=runner, sleeper=lambda _: None)
        self.assertEqual(calls, 1)
        self.assertEqual(launch['schema'], self.m.LAUNCH_SCHEMA)
        self.assertEqual(launch['preflight_fingerprint'], preflight['preflight_fingerprint'])
        self.assertEqual(launch['container_id'], FULL_ID)
        self.assertEqual(launch['pid'], candidate['pid'])
        self.assertEqual(launch['process_start_ticks'], candidate['start_ticks'])
        self.assertEqual(launch['launch_method'], 'docker_exec_detached_direct_env')
        self.assertIs(launch['bootstrap_helper_residue'], False)
        launch_calls = [call for call in self.fake.calls if call[:3] == ('docker', 'exec', '-d')]
        self.assertEqual(len(launch_calls), 1)
        launch_cmd = launch_calls[0]
        self.assertNotIn('sh', launch_cmd)
        self.assertNotIn('-c', launch_cmd)
        self.assertIn(self.m.CLIENT_PATH, launch_cmd)
        for forbidden in ('TIBIA_TEST_EMAIL', 'TIBIA_TEST_PASSWORD', 'TRACK_A_CANONICAL_LEASE_TOKEN', 'TRACK_A_CANONICAL_LEASE_TOKEN_FILE'):
            self.assertIn(forbidden, launch_cmd)

    def test_launch_rejects_stale_preflight_or_preexisting_client(self):
        preflight = self.write_preflight()
        preflight['container_id'] = OTHER_ID
        unsigned = dict(preflight)
        unsigned.pop('preflight_fingerprint')
        preflight['preflight_fingerprint'] = self.m._fingerprint(unsigned)
        self.m.write_record(self.record, preflight)
        with self.assertRaisesRegex(self.m.WorkerError, 'preflight_drift'):
            self.m.launch_from_preflight(self.record, runner=self.fake, sleeper=lambda _: None)

        self.fake.containers = [(FULL_ID, self.m.TARGET_CONTAINER)]
        self.fake.candidates[FULL_ID] = []
        self.write_preflight()
        self.fake.candidates[FULL_ID] = [self.exact_candidate()]
        with self.assertRaisesRegex(self.m.WorkerError, 'preflight_drift|official_client_candidate_count'):
            self.m.launch_from_preflight(self.record, runner=self.fake, sleeper=lambda _: None)

    def test_launch_rejects_no_or_multiple_postlaunch_targets(self):
        self.write_preflight()
        for label, rows in (
            ('none', []),
            ('multiple', [self.exact_candidate(), self.exact_candidate(pid=322, start=655)]),
        ):
            with self.subTest(label=label):
                self.fake.candidates[FULL_ID] = []
                original = self.fake.__call__
                def runner(command, rows=rows):
                    cmd = tuple(str(value) for value in command)
                    if cmd[:3] == ('docker', 'exec', '-d'):
                        result = original(command)
                        self.fake.candidates[FULL_ID] = rows
                        return result
                    return original(command)
                with self.assertRaisesRegex(self.m.WorkerError, 'postlaunch_target_not_unique'):
                    self.m.launch_from_preflight(self.record, runner=runner, sleeper=lambda _: None, attempts=2)

    def test_rollback_signals_only_exact_identity(self):
        launch = {
            'schema': self.m.LAUNCH_SCHEMA,
            'preflight_fingerprint': 'f' * 64,
            'container_name': self.m.TARGET_CONTAINER,
            'container_id': FULL_ID,
            'display': self.m.TARGET_DISPLAY,
            'package_dir': self.m.PACKAGE_DIR,
            'client_path': self.m.CLIENT_PATH,
            'client_size': self.m.SIZE,
            'client_sha256': self.m.SHA,
            'pid': 321,
            'process_start_ticks': 654,
            'launch_method': 'docker_exec_detached_direct_env',
            'bootstrap_helper_residue': False,
        }
        self.m.write_record(self.record, launch)
        self.fake.process_identity[321] = self.exact_process_identity()
        self.m.rollback_launch(self.record, runner=self.fake, sleeper=lambda _: None, attempts=1)
        kill_calls = [call for call in self.fake.calls if '/bin/kill' in call]
        self.assertEqual(len(kill_calls), 1)
        self.assertEqual(kill_calls[0][-2:], ('-TERM', '321'))
        flattened = ' '.join(' '.join(call) for call in self.fake.calls)
        for forbidden in ('pkill', 'killall', 'docker stop', 'docker restart', 'docker rm'):
            self.assertNotIn(forbidden, flattened)

    def test_rollback_refuses_identity_or_container_drift_before_signal(self):
        base = {
            'schema': self.m.LAUNCH_SCHEMA,
            'preflight_fingerprint': 'f' * 64,
            'container_name': self.m.TARGET_CONTAINER,
            'container_id': FULL_ID,
            'display': self.m.TARGET_DISPLAY,
            'package_dir': self.m.PACKAGE_DIR,
            'client_path': self.m.CLIENT_PATH,
            'client_size': self.m.SIZE,
            'client_sha256': self.m.SHA,
            'pid': 321,
            'process_start_ticks': 654,
            'launch_method': 'docker_exec_detached_direct_env',
            'bootstrap_helper_residue': False,
        }
        for label, mutate_container, mutate_identity, code in (
            ('container', True, None, 'rollback_container_drift'),
            ('start', False, ('start_ticks', 999), 'rollback_identity_drift'),
            ('path', False, ('exe', '/other/client'), 'rollback_identity_drift'),
            ('sha', False, ('sha256', '0' * 64), 'rollback_identity_drift'),
        ):
            with self.subTest(label=label):
                self.fake.calls.clear()
                self.fake.containers = [(OTHER_ID if mutate_container else FULL_ID, self.m.TARGET_CONTAINER)]
                identity = self.exact_process_identity()
                if mutate_identity:
                    identity[mutate_identity[0]] = mutate_identity[1]
                self.fake.process_identity = {321: identity}
                self.m.write_record(self.record, base)
                with self.assertRaisesRegex(self.m.WorkerError, code):
                    self.m.rollback_launch(self.record, runner=self.fake, sleeper=lambda _: None, attempts=1)
                self.assertFalse(any('/bin/kill' in call for call in self.fake.calls))


if __name__ == '__main__':
    unittest.main()
