import unittest

from tools.tibia_re_surveyor.runtime import CommandResult, DockerRuntimeProbe


class StaticRunner:
    def __init__(self, results):
        self.results = list(results)
        self.commands = []
    def run(self, args, timeout=15.0):
        self.commands.append(list(args))
        if not self.results:
            raise AssertionError(f"unexpected command: {args}")
        return self.results.pop(0)


class RuntimeTests(unittest.TestCase):
    def test_proc_start_ticks_parsing(self):
        fields = ["S"] + [str(value) for value in range(1, 25)]
        stat = "123 (client) " + " ".join(fields)
        self.assertEqual(int(fields[19]), DockerRuntimeProbe._start_ticks(stat))

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


if __name__ == "__main__":
    unittest.main()
