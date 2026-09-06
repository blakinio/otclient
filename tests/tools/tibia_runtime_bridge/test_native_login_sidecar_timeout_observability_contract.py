from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
WORKER = ROOT / ".github/scripts/track_a_native_login_be4f48_physical.py"


class SidecarTimeoutObservabilityContractTests(unittest.TestCase):
    def test_probe_runner_preserves_allowlisted_partial_stdout_on_timeout(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        required = (
            "def _run_probe_sidecar(",
            "subprocess.TimeoutExpired",
            "sidecar_probe_process_timeout",
            "_classify_sidecar_probe_failure",
            "partial_stdout",
            "_base._clean_env()",
        )
        for needle in required:
            with self.subTest(needle=needle):
                self.assertIn(needle, text)
        self.assertNotIn("exc.stderr", text)
        self.assertNotIn("str(exc)", text)

    def test_sidecar_probe_uses_probe_specific_runner_not_base_run(self) -> None:
        text = WORKER.read_text(encoding="utf-8")
        start = text.index("def sidecar_probe(")
        end = text.index("\ndef precheck(", start)
        probe = text[start:end]
        self.assertIn("_run_probe_sidecar(", probe)
        self.assertNotIn("completed = _base._run([", probe)


if __name__ == "__main__":
    unittest.main()
