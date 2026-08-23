#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name('tibia-official-client-re-control-center-bridge-transport.py')
TRANSITION = Path(__file__).with_name('tibia-official-client-re-canonical-live-transition.py')


def load():
    spec = importlib.util.spec_from_file_location('package_d_transport_tested', SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakePopen:
    def __init__(self):
        self.stdin = object()
        self.stdout = object()
        self.returncode = None

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        return 0

    def terminate(self):
        self.returncode = -15


class Tests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.repo = Path(__file__).resolve().parents[2]
        self.command = [
            sys.executable,
            str(TRANSITION.resolve()),
            'guarded-dispatch',
            '--task-id', 'OTC-TEST',
            '--session-id', 'session-test',
            '--token-file', '/private/token.path',
            '--probe', str(Path(__file__).with_name('tibia-official-client-re-canonical-live-session.sh').resolve()),
            '--worker', str(Path(__file__).with_name('tibia-official-client-re-canonical-live-session.sh').resolve()),
            '--request-file', '/private/request.json',
        ]

    def test_invalid_command_is_rejected_before_process_start(self):
        with mock.patch.object(self.m.subprocess, 'Popen') as popen, \
                self.assertRaisesRegex(self.m.TransportError, 'track_a_transport_command_invalid'):
            self.m.start_transition_process(['sh', '-c', 'true'], self.repo)
        popen.assert_not_called()

    def test_valid_command_uses_exact_no_shell_private_pipe_shape(self):
        fake = FakePopen()
        with mock.patch.object(self.m.subprocess, 'Popen', return_value=fake) as popen:
            wrapped = self.m.start_transition_process(self.command, self.repo)
        popen.assert_called_once_with(
            self.command,
            cwd=self.repo.resolve(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            close_fds=True,
            shell=False,
        )
        self.assertIs(wrapped.stdin, fake.stdin)
        self.assertIs(wrapped.stdout, fake.stdout)

    def test_wait_translates_subprocess_timeout_to_builtin_timeout(self):
        fake = FakePopen()
        fake.wait = mock.Mock(side_effect=subprocess.TimeoutExpired(self.command, 0.1))
        with mock.patch.object(self.m.subprocess, 'Popen', return_value=fake):
            wrapped = self.m.start_transition_process(self.command, self.repo)
        with self.assertRaises(TimeoutError):
            wrapped.wait(timeout=0.1)

    def test_transport_never_reads_token_file_contents(self):
        with tempfile.TemporaryDirectory() as td:
            token = Path(td) / 'token'
            token.write_text('secret-never-read', encoding='utf-8')
            command = list(self.command)
            command[command.index('/private/token.path')] = str(token)
            with mock.patch.object(Path, 'read_text', side_effect=AssertionError('token read')), \
                    mock.patch.object(self.m.subprocess, 'Popen', return_value=FakePopen()):
                self.m.start_transition_process(command, self.repo)


if __name__ == '__main__':
    unittest.main()