#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name('tibia-official-client-re-input-lock.py')


def load():
    spec = importlib.util.spec_from_file_location('input_lock_tested', SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Tests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_acquire_creates_safe_regular_file(self):
        lock = self.m.InputLock(self.root)
        with lock.acquire(timeout_seconds=0.2, cancelled=lambda: False):
            st = lock.path.lstat()
            self.assertTrue(stat.S_ISREG(st.st_mode))
            if not sys.platform.startswith('win'):
                self.assertEqual(stat.S_IMODE(st.st_mode), 0o600)
            if hasattr(os, 'getuid'):
                self.assertEqual(st.st_uid, os.getuid())

    def test_symlink_path_is_rejected(self):
        target = self.root / 'target'
        target.write_text('x')
        path = self.root / 'input.lock'
        path.symlink_to(target)
        lock = self.m.InputLock(self.root)
        with self.assertRaisesRegex(self.m.InputLockError, 'input_lock_unsafe'):
            with lock.acquire(timeout_seconds=0.2, cancelled=lambda: False):
                self.fail('must not acquire symlink')

    def test_cancellation_refuses_before_acquire(self):
        lock = self.m.InputLock(self.root)
        with self.assertRaisesRegex(self.m.InputLockError, 'input_lock_cancelled'):
            with lock.acquire(timeout_seconds=0.2, cancelled=lambda: True):
                self.fail('must not acquire after cancellation')

    def test_second_holder_times_out_while_first_holds(self):
        first = self.m.InputLock(self.root)
        second = self.m.InputLock(self.root)
        with first.acquire(timeout_seconds=0.2, cancelled=lambda: False):
            with self.assertRaisesRegex(self.m.InputLockError, 'input_lock_timeout'):
                with second.acquire(timeout_seconds=0.05, cancelled=lambda: False):
                    self.fail('second holder must not acquire concurrently')

    def test_missing_canonical_state_root_is_rejected(self):
        missing = self.root / 'missing'
        lock = self.m.InputLock(missing)
        with self.assertRaisesRegex(self.m.InputLockError, 'input_lock_state_root_unavailable'):
            with lock.acquire(timeout_seconds=0.2, cancelled=lambda: False):
                self.fail('input lock must not create canonical state root')
        self.assertFalse(missing.exists())

    def test_replaced_lock_path_is_rejected_against_open_fd(self):
        lock = self.m.InputLock(self.root)
        fd = lock._open_safe()
        try:
            lock.path.unlink()
            lock.path.write_bytes(b'replacement')
            with self.assertRaisesRegex(self.m.InputLockError, 'input_lock_replaced'):
                lock._validate_fd_path(fd)
        finally:
            os.close(fd)


if __name__ == '__main__':
    unittest.main()
