import unittest

from tools.tibia_re_surveyor.runtime import CommandResult, DockerRuntimeProbe


class StaticRunner:
    def __init__(self, results):
        self.results = list(results)
    def run(self, args, timeout=15.0):
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


if __name__ == "__main__":
    unittest.main()
