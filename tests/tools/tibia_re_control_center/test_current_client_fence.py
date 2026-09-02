import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from tools.tibia_re_control_center.current_client_fence import (
    CURRENT_CLIENT_FENCE_MANIFEST,
    approved_historical_fences,
    approved_reconciliation_sources,
    current_client_fence,
    load_current_client_fence_manifest,
    main,
)

ROOT = Path(__file__).resolve().parents[3]
FOUNDATIONAL_CONSUMERS = (
    ROOT / "tools/tibia_re_control_center/agent_runtime_admission.py",
    ROOT / ".github/scripts/tibia-official-client-re-canonical-live-transition.py",
    ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py",
    ROOT / ".github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py",
    ROOT / ".github/scripts/tibia-official-client-re-canonical-live-session.sh",
)

WORKFLOW_CONSUMERS = (
    ROOT / ".github/workflows/track-a-surveyor-v2-readonly.yml",
    ROOT / ".github/workflows/track-a-kasm-canonical-bootstrap.yml",
    ROOT / ".github/workflows/track-a-canonical-client-fence-reconciliation.yml",
    ROOT / ".github/workflows/track-a-canonical-live-governance.yml",
    ROOT / ".github/scripts/tibia-official-client-re-canonical-client-fence-reconcile.py",
)


class CurrentClientFenceTests(unittest.TestCase):
    def _current(self):
        return current_client_fence()

    def _previous(self):
        history = approved_historical_fences()
        self.assertTrue(history)
        return history[0]

    def test_default_manifest_is_self_consistent(self):
        manifest = load_current_client_fence_manifest()
        self.assertEqual(manifest.current, self._current())
        self.assertEqual(
            (manifest.current, *manifest.approved_history),
            approved_reconciliation_sources(),
        )
        self.assertTrue(CURRENT_CLIENT_FENCE_MANIFEST.is_file())
        provenance = ROOT / manifest.current_provenance
        self.assertTrue(provenance.is_file())
        self.assertTrue(manifest.current_provenance.startswith("docs/agents/evidence/"))

    def test_foundational_consumers_use_canonical_loader_not_current_literals(self):
        current = self._current()
        for path in FOUNDATIONAL_CONSUMERS:
            text = path.read_text(encoding="utf-8")
            self.assertIn("current_client_fence", text, str(path))
            self.assertNotIn(current.version, text, str(path))
            self.assertNotIn(current.sha256, text, str(path))

    def test_current_identity_workflows_use_canonical_loader_not_current_literals(self):
        current = self._current()
        for path in WORKFLOW_CONSUMERS:
            text = path.read_text(encoding="utf-8")
            self.assertIn("current_client_fence", text, str(path))
            self.assertNotIn(current.version, text, str(path))
            self.assertNotIn(current.sha256, text, str(path))

    def _write(self, document):
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / "fence.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        self.addCleanup(temp.cleanup)
        return path

    def _valid(self):
        current = self._current()
        previous = self._previous()
        return {
            "schema_version": 1,
            "current": {
                "version": current.version,
                "size": current.size,
                "sha256": current.sha256,
            },
            "current_provenance": "docs/agents/evidence/OTC-20260902-canonical-current-client-fence-be4f48/result.json",
            "approved_history": [
                {
                    "version": previous.version,
                    "size": previous.size,
                    "sha256": previous.sha256,
                }
            ],
        }

    def test_github_env_cli_writes_legacy_and_sha256_names(self):
        current = self._current()
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        path = Path(temp.name) / "github-env"
        self.assertEqual(0, main(["github-env", str(path), "--prefix", "EXPECTED"]))
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertIn(f"EXPECTED_VERSION={current.version}", lines)
        self.assertIn(f"EXPECTED_SIZE={current.size}", lines)
        self.assertIn(f"EXPECTED_SHA={current.sha256}", lines)
        self.assertIn(f"EXPECTED_SHA256={current.sha256}", lines)

    def test_shell_cli_emits_validated_current_fence(self):
        current = self._current()
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            self.assertEqual(0, main(["shell", "--prefix", "TRACK_A_CURRENT_CLIENT"]))
        self.assertIn(
            f"TRACK_A_CURRENT_CLIENT_VERSION={current.version}", stream.getvalue()
        )
        self.assertIn(f"TRACK_A_CURRENT_CLIENT_SIZE={current.size}", stream.getvalue())
        self.assertIn(f"TRACK_A_CURRENT_CLIENT_SHA={current.sha256}", stream.getvalue())


    def test_rejects_unsafe_or_missing_current_provenance(self):
        for value in ("../outside.json", "docs/agents/evidence/missing/result.json"):
            with self.subTest(value=value):
                document = self._valid()
                document["current_provenance"] = value
                with self.assertRaisesRegex(ValueError, "current provenance"):
                    load_current_client_fence_manifest(self._write(document))

    def test_rejects_non_string_current_provenance_as_type_error(self):
        document = self._valid()
        document["current_provenance"] = 123
        with self.assertRaisesRegex(TypeError, "current provenance"):
            load_current_client_fence_manifest(self._write(document))

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


if __name__ == "__main__":
    unittest.main()