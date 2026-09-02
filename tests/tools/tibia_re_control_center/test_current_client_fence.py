import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools.tibia_re_control_center.current_client_fence import (
    CURRENT_CLIENT_FENCE_MANIFEST,
    ClientFence,
    approved_historical_fences,
    approved_reconciliation_sources,
    current_client_fence,
    load_current_client_fence_manifest,
    main,
)

CURRENT = ClientFence(
    version="15.32.be4f48",
    size=52_105_824,
    sha256="552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1",
)
PREVIOUS = ClientFence(
    version="15.32.75d4a0",
    size=52_105_824,
    sha256="d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a",
)

class CurrentClientFenceTests(unittest.TestCase):
    def test_default_manifest_exposes_exact_current_and_history(self):
        manifest = load_current_client_fence_manifest()
        self.assertEqual(CURRENT, manifest.current)
        self.assertEqual(CURRENT, current_client_fence())
        self.assertIn(PREVIOUS, approved_historical_fences())
        self.assertEqual(
            (CURRENT, *approved_historical_fences()),
            approved_reconciliation_sources(),
        )
        self.assertTrue(CURRENT_CLIENT_FENCE_MANIFEST.is_file())

    def _write(self, document):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / "fence.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        self.addCleanup(temp.cleanup)
        return path

    def _valid(self):
        return {
            "schema_version": 1,
            "current": {"version": CURRENT.version, "size": CURRENT.size, "sha256": CURRENT.sha256},
            "approved_history": [
                {"version": PREVIOUS.version, "size": PREVIOUS.size, "sha256": PREVIOUS.sha256}
            ],
        }

    def test_github_env_cli_writes_legacy_and_sha256_names(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "github-env"
        self.assertEqual(0, main(["github-env", str(path), "--prefix", "EXPECTED"]))
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertIn(f"EXPECTED_VERSION={CURRENT.version}", lines)
        self.assertIn(f"EXPECTED_SIZE={CURRENT.size}", lines)
        self.assertIn(f"EXPECTED_SHA={CURRENT.sha256}", lines)
        self.assertIn(f"EXPECTED_SHA256={CURRENT.sha256}", lines)

    def test_shell_cli_emits_validated_current_fence(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(0, main(["shell", "--prefix", "TRACK_A_CURRENT_CLIENT"]))
        self.assertIn(f"TRACK_A_CURRENT_CLIENT_VERSION={CURRENT.version}", stream.getvalue())
        self.assertIn(f"TRACK_A_CURRENT_CLIENT_SIZE={CURRENT.size}", stream.getvalue())
        self.assertIn(f"TRACK_A_CURRENT_CLIENT_SHA={CURRENT.sha256}", stream.getvalue())
    def test_rejects_extra_root_field(self):
        document = self._valid()
        document["unexpected"] = True
        with self.assertRaisesRegex(ValueError, "manifest fields"):
            load_current_client_fence_manifest(self._write(document))

    def test_rejects_extra_fence_field(self):
        document = self._valid()
        document["current"]["unexpected"] = True
        with self.assertRaisesRegex(ValueError, "fence fields"):
            load_current_client_fence_manifest(self._write(document))

    def test_rejects_current_in_history(self):
        document = self._valid()
        document["approved_history"].append(dict(document["current"]))
        with self.assertRaisesRegex(ValueError, "current fence in history"):
            load_current_client_fence_manifest(self._write(document))

    def test_rejects_duplicate_history(self):
        document = self._valid()
        document["approved_history"].append(dict(document["approved_history"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate history"):
            load_current_client_fence_manifest(self._write(document))