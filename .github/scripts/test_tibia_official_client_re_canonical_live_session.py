#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

WORKER = Path(__file__).with_name('tibia-official-client-re-canonical-live-session.sh')


class ToolrootResolverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def write_tool(path: Path) -> None:
        path.write_text('#!/bin/sh\nexit 0\n', encoding='utf-8')
        path.chmod(0o755)

    def make_root(self, name: str, complete: bool = True) -> Path:
        root = self.root / name
        (root / 'usr/bin').mkdir(parents=True)
        if complete:
            names = ('Xvfb', 'x11vnc', 'xdotool')
        else:
            names = ('Xvfb',)
        for binary in names:
            self.write_tool(root / 'usr/bin' / binary)
        (root / 'usr/share/X11/xkb').mkdir(parents=True)
        lib = root / 'usr/lib/x86_64-linux-gnu/libproxychains.so.4'
        lib.parent.mkdir(parents=True)
        lib.write_bytes(b'fixture')
        return root

    def run_resolver(self, candidates: list[Path]) -> subprocess.CompletedProcess[str]:
        env = dict(
            os.environ,
            TRACK_A_CANONICAL_WORKER_CONTRACT_TEST='1',
            TRACK_A_CANONICAL_TOOLROOT_TEST_CANDIDATES=';'.join(map(str, candidates)),
        )
        return subprocess.run(
            [str(WORKER), 'toolroot'],
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_selects_first_complete_root_and_skips_partial_root(self):
        partial = self.make_root('partial', complete=False)
        complete = self.make_root('complete', complete=True)
        result = self.run_resolver([partial, complete])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), str(complete))

    def test_rejects_symlink_root(self):
        complete = self.make_root('complete', complete=True)
        link = self.root / 'link'
        link.symlink_to(complete, target_is_directory=True)
        fallback = self.make_root('fallback', complete=True)
        result = self.run_resolver([link, fallback])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), str(fallback))

    def test_rejects_intermediate_symlink_escape_for_tools(self):
        escaped = self.make_root('escaped', complete=True)
        outside_bin = self.root / 'outside-bin'
        outside_bin.mkdir()
        for binary in ('Xvfb', 'x11vnc', 'xdotool'):
            self.write_tool(outside_bin / binary)
        shutil.rmtree(escaped / 'usr/bin')
        (escaped / 'usr/bin').symlink_to(outside_bin, target_is_directory=True)
        fallback = self.make_root('fallback-contained', complete=True)
        result = self.run_resolver([escaped, fallback])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), str(fallback))

    def test_fails_closed_when_no_complete_root_exists(self):
        partial = self.make_root('partial', complete=False)
        result = self.run_resolver([partial])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('TRACK_A_CANONICAL_SESSION_ERROR=toolroot_unavailable', result.stderr)

    def test_production_allowlist_is_fixed_and_test_override_is_contract_gated(self):
        source = WORKER.read_text(encoding='utf-8')
        self.assertIn('TOOLROOT_HOME="$BASE/toolroot"', source)
        self.assertIn('TOOLROOT_WORK=/work/_otclient_tibia_re_state/toolroot', source)
        self.assertIn('TRACK_A_CANONICAL_WORKER_CONTRACT_TEST', source)
        self.assertIn('TRACK_A_CANONICAL_TOOLROOT_TEST_CANDIDATES', source)
        self.assertIn('toolroot_complete "$persisted_toolroot" || die toolroot_unavailable', source)
        self.assertIn('printf \'%s\\n\' "$TOOL" >"$SESSION/toolroot"', source)
        self.assertIn('within_toolroot "$root_real" "$path"', source)
        self.assertNotIn('command -v "$1"', source)


if __name__ == '__main__':
    unittest.main()
