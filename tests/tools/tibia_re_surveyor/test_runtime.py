import unittest
from pathlib import Path

from tools.tibia_re_surveyor.runtime import CommandResult, DockerRuntimeProbe, RuntimeProbeError


class StaticRunner:
    def __init__(self, results):
        self.results = list(results)
        self.commands = []
    def run(self, args, timeout=15.0):
        self.commands.append(list(args))
        if not self.results:
            raise AssertionError(f"unexpected command: {args}")
        return self.results.pop(0)




class TargetPidRunner:
    def __init__(self, result):
        self.result = result
        self.commands = []

    def run(self, args, timeout=15.0):
        self.commands.append(list(args))
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class RuntimeTests(unittest.TestCase):
    def test_proc_start_ticks_parsing(self):
        fields = ["S"] + [str(value) for value in range(1, 25)]
        stat = "123 (client) " + " ".join(fields)
        self.assertEqual(int(fields[19]), DockerRuntimeProbe._start_ticks(stat))

    def test_container_overrides_outside_otclient_namespace_are_rejected(self):
        with self.assertRaises(ValueError):
            DockerRuntimeProbe(target_container="freqtrade-portal-staging")
        with self.assertRaises(ValueError):
            DockerRuntimeProbe(control_container="unrelated-control")

    def test_stopped_target_is_fail_closed_read_only_unavailable(self):
        runner = StaticRunner([CommandResult(0, "false\n")])
        probe = DockerRuntimeProbe(runner=runner, now_fn=lambda: 1234)
        snapshot = probe.snapshot()
        self.assertFalse(snapshot["target_running"])
        self.assertEqual("NOT_PROVEN", snapshot["target_uniqueness"])
        self.assertEqual("READ_ONLY_UNAVAILABLE", snapshot["runtime_access"])
        self.assertEqual(1234, snapshot["observed_at_epoch"])

    def test_process_identity_never_reads_full_process_environment(self):
        fields = ["S"] + [str(value) for value in range(1, 25)]
        stat = "123 (client) " + " ".join(fields)
        runner = StaticRunner([
            CommandResult(0, "/opt/tibia/client\n"),
            CommandResult(0, "52109920\n"),
            CommandResult(0, "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8  /proc/123/exe\n"),
            CommandResult(0, stat),
        ])
        probe = DockerRuntimeProbe(runner=runner)
        identity = probe._process_identity(123)
        self.assertEqual(123, identity["pid"])
        self.assertTrue(identity["exact_fence_match"])
        flattened = " ".join(" ".join(command) for command in runner.commands)
        self.assertNotIn("/proc/123/environ", flattened)

    def test_target_client_census_is_scoped_to_declared_container(self):
        runner = TargetPidRunner(CommandResult(0, "123\n"))
        probe = DockerRuntimeProbe(runner=runner)
        self.assertEqual([123], probe._target_client_pids())
        self.assertEqual(
            [["docker", "exec", "otclient-track-a-kasmvnc", "pgrep", "-x", "client"]],
            runner.commands,
        )
        flattened = " ".join(" ".join(command) for command in runner.commands)
        self.assertNotIn("docker ps", flattened)
        self.assertNotIn("unrelated", flattened)

    def test_target_client_census_empty_is_not_proven(self):
        runner = TargetPidRunner(CommandResult(1, ""))
        probe = DockerRuntimeProbe(runner=runner)
        self.assertEqual([], probe._target_client_pids())

    def test_target_container_timeout_remains_fail_closed(self):
        runner = TargetPidRunner(RuntimeProbeError("target probe timed out"))
        probe = DockerRuntimeProbe(runner=runner)
        with self.assertRaises(RuntimeProbeError):
            probe._target_client_pids()

    def test_target_container_nonstandard_rc_remains_fail_closed(self):
        runner = TargetPidRunner(CommandResult(125, "", "docker exec unavailable"))
        probe = DockerRuntimeProbe(runner=runner)
        with self.assertRaises(RuntimeProbeError):
            probe._target_client_pids()

    def test_runtime_probe_and_operator_have_no_hostwide_docker_discovery(self):
        runtime_source = Path("tools/tibia_re_surveyor/runtime.py").read_text(encoding="utf-8")
        workflow = Path(".github/workflows/track-a-surveyor-v2-readonly.yml").read_text(encoding="utf-8")
        self.assertNotIn('["docker", "ps"', runtime_source)
        self.assertNotIn("docker ps", workflow)
        self.assertIn("EXTERNAL_CONTAINERS_SCANNED=false", workflow)
        self.assertIn("TARGET_UNIQUENESS_SCOPE=DECLARED_RUNTIME_NAMESPACE", workflow)


if __name__ == "__main__":
    unittest.main()
