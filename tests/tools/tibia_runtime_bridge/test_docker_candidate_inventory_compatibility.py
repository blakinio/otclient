from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[3]
BOOTSTRAP = ROOT / ".github/scripts/tibia-official-client-re-kasm-bootstrap-worker-compatible.py"
PROBE = ROOT / ".github/scripts/tibia-official-client-re-kasm-existing-runtime-probe-compatible.py"
INVALIDATOR = ROOT / ".github/scripts/tibia-official-client-re-same-boot-zero-client-invalidate-compatible.py"
SCOPE = ROOT / "docs/agents/contracts/TRACK_A_CANONICAL_KASM_RUNTIME_SCOPE_V1.md"
TARGET = "a" * 64
FOREIGN = "b" * 64


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.bootstrap = load(BOOTSTRAP, "canonical_scope_bootstrap_tested")
        self.probe = load(PROBE, "canonical_scope_probe_tested")

    def test_bootstrap_scans_only_canonical_kasm_container(self) -> None:
        calls: list[str] = []

        def deep(container_id, _runner):
            calls.append(container_id)
            return []

        self.bootstrap._original_candidate_rows = deep
        containers = [
            (TARGET, self.bootstrap._base.TARGET_CONTAINER),
            (FOREIGN, "unrelated-service"),
        ]
        result = self.bootstrap.exact_candidates(containers, lambda _command: "")
        self.assertEqual([], result)
        self.assertEqual([TARGET], calls)

    def test_bootstrap_rejects_missing_or_duplicate_canonical_container(self) -> None:
        for containers in (
            [(FOREIGN, "unrelated-service")],
            [(TARGET, self.bootstrap._base.TARGET_CONTAINER), (FOREIGN, self.bootstrap._base.TARGET_CONTAINER)],
        ):
            with self.subTest(containers=containers):
                with self.assertRaisesRegex(self.bootstrap.WorkerError, "target_container_count"):
                    self.bootstrap.exact_candidates(containers, lambda _command: "")

    def test_probe_collect_skips_every_noncanonical_container(self) -> None:
        calls: list[str] = []
        self.probe._base.docker_containers = lambda _runner: [
            (TARGET, self.probe._base.TARGET_CONTAINER),
            (FOREIGN, "unrelated-service"),
        ]

        def deep(container_id, _runner):
            calls.append(container_id)
            return []

        self.probe._original_candidate_rows = deep

        def fake_collect(runner):
            for container_id, _name in self.probe._base.docker_containers(runner):
                self.probe._base.candidate_rows(container_id, runner)
            return {"inventory_scope": "legacy", "candidate_count": 1}

        self.probe._base.collect = fake_collect
        payload = self.probe.collect(lambda _command: "")
        self.assertEqual([TARGET], calls)
        self.assertEqual("canonical_kasm_container", payload["inventory_scope"])

    def test_no_synology_wide_prefilter_or_foreign_exec_dependency_remains(self) -> None:
        for path in (BOOTSTRAP, PROBE):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("docker_official_candidate_prefilter", text)
            self.assertNotIn("docker top", text)
            self.assertIn("TARGET_CONTAINER", text)
        scope = SCOPE.read_text(encoding="utf-8")
        self.assertIn("otclient-track-a-kasmvnc", scope)
        self.assertIn("Other Docker containers on the Synology host are outside", scope)
        self.assertIn("MUST NOT be executed into", scope)

    def test_invalidator_rebinds_only_approved_scoped_worker_path(self) -> None:
        text = INVALIDATOR.read_text(encoding="utf-8")
        self.assertIn("tibia-official-client-re-same-boot-zero-client-invalidate.py", text)
        self.assertIn("tibia-official-client-re-kasm-bootstrap-worker-compatible.py", text)
        self.assertIn("_base.APPROVED_WORKER = COMPAT_WORKER", text)
        for forbidden in ("os.replace(", "runtime-registration.json", "docker exec", "TIBIA_TEST_PASSWORD"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
