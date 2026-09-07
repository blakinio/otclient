from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[3]
PREFILTER = ROOT / "tools/tibia_re_control_center/docker_official_candidate_prefilter.py"
BOOTSTRAP = ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py"
PROBE = ROOT / ".github/scripts/tibia-official-client-re-kasm-existing-runtime-probe-compatible.py"
INVALIDATOR = ROOT / ".github/scripts/tibia-official-client-re-same-boot-zero-client-invalidate-compatible.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.prefilter = load(PREFILTER, "candidate_prefilter_tested")
        self.bootstrap = load(BOOTSTRAP, "candidate_bootstrap_compat_tested")
        self.probe = load(PROBE, "candidate_probe_compat_tested")

    def test_prefilter_accepts_current_official_process_signatures(self) -> None:
        cases = (
            "client /home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client\n",
            "Tibia /opt/tibia-package/Tibia/bin/client\n",
            "foo /x/Tibia/packages/Tibia/bin/client --flag\n",
        )
        for index, output in enumerate(cases):
            with self.subTest(index=index):
                calls = []
                def runner(command, output=output):
                    calls.append(tuple(command))
                    return output
                self.assertTrue(self.prefilter.container_requires_deep_scan("a" * 64, runner))
                self.assertEqual(calls[0][:3], ("docker", "top", "a" * 64))

    def test_prefilter_excludes_harmless_container_without_userspace_exec(self) -> None:
        calls = []
        def runner(command):
            calls.append(tuple(command))
            if command[:2] == ["docker", "top"]:
                return "sleep sleep infinity\nnginx nginx -g daemon off;\n"
            raise AssertionError(f"deep userspace execution must not occur: {command!r}")
        self.assertEqual([], self.bootstrap.candidate_rows("b" * 64, runner))
        self.assertEqual(1, len(calls))
        self.assertEqual(("docker", "top"), calls[0][:2])

    def test_hinted_bootstrap_container_remains_fail_closed_when_deep_exec_is_126(self) -> None:
        calls = []
        def runner(command):
            calls.append(tuple(command))
            if command[:2] == ["docker", "top"]:
                return "client /home/u/Tibia/packages/Tibia/bin/client\n"
            raise self.bootstrap.WorkerError("command_failed:docker:126")
        with self.assertRaisesRegex(self.bootstrap.WorkerError, "command_failed:docker:126"):
            self.bootstrap.candidate_rows("b" * 64, runner)
        self.assertTrue(any(call[:2] == ("docker", "exec") for call in calls))

    def test_hinted_bootstrap_exact_candidate_keeps_size_sha_start_proof(self) -> None:
        row = {
            "readable": True,
            "pid": 321,
            "exe": self.bootstrap._base.CLIENT_PATH,
            "size": self.bootstrap.SIZE,
            "sha256": self.bootstrap.SHA,
            "start_ticks": 654,
            "official_hint": True,
        }
        def runner(command):
            if command[:2] == ["docker", "top"]:
                return "client /home/u/Tibia/packages/Tibia/bin/client\n"
            if command[:2] == ["docker", "exec"]:
                return json.dumps([row]) + "\n"
            raise AssertionError(command)
        result = self.bootstrap.candidate_rows("b" * 64, runner)
        self.assertEqual(1, len(result))
        self.assertEqual(self.bootstrap.SIZE, result[0]["size"])
        self.assertEqual(self.bootstrap.SHA, result[0]["sha256"])
        self.assertEqual(654, result[0]["start_ticks"])

    def test_probe_harmless_container_avoids_shell_and_hinted_failure_stays_closed(self) -> None:
        calls = []
        def harmless(command):
            calls.append(tuple(command))
            if command[:2] == ["docker", "top"]:
                return "redis redis-server *:6379\n"
            raise AssertionError(f"shell must not be required: {command!r}")
        self.assertEqual([], self.probe.candidate_rows("c" * 64, harmless))
        self.assertFalse(any(call[:2] == ("docker", "exec") for call in calls))

        def hinted(command):
            if command[:2] == ["docker", "top"]:
                return "client /home/u/Tibia-x/bin/client\n"
            raise self.probe.ProbeError("command_failed:docker:126")
        with self.assertRaisesRegex(self.probe.ProbeError, "command_failed:docker:126"):
            self.probe.candidate_rows("c" * 64, hinted)

    def test_prefilter_failure_is_inventory_failure_not_absence(self) -> None:
        def runner(_command):
            raise RuntimeError("docker top unavailable")
        with self.assertRaisesRegex(self.bootstrap.WorkerError, "docker_top_failed"):
            self.bootstrap.candidate_rows("d" * 64, runner)
        with self.assertRaisesRegex(self.probe.ProbeError, "docker_top_failed"):
            self.probe.candidate_rows("d" * 64, runner)

    def test_invalidator_rebinds_only_approved_worker_path(self) -> None:
        text = INVALIDATOR.read_text(encoding="utf-8")
        self.assertIn("tibia-official-client-re-same-boot-zero-client-invalidate.py", text)
        self.assertIn("tibia-official-client-re-kasm-bootstrap-worker-compatible.py", text)
        self.assertIn("_base.APPROVED_WORKER = COMPAT_WORKER", text)
        for forbidden in ("os.replace(", "runtime-registration.json", "docker exec", "TIBIA_TEST_PASSWORD"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
