#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("tibia-official-client-re-canonical-xres-worker-adapter.py")
OWNER = Path(__file__).with_name("tibia-official-client-re-xres-window-owner.py")
WIRE = Path(__file__).with_name("tibia-official-client-re-xres-wire.py")


def load():
    spec = importlib.util.spec_from_file_location("canonical_xres_adapter_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


adapter = load()


class Tests(unittest.TestCase):
    def test_exact_legacy_window_block_is_replaced(self) -> None:
        source = "#!/usr/bin/env bash\n" + adapter.OLD_WINDOW + "\necho ok\n"
        result = adapter.patch(source, OWNER, WIRE)
        self.assertNotIn("search --onlyvisible --pid", result)
        self.assertIn("tibia-official-client-re-xres-window-owner.py", result)
        self.assertIn("--wire-helper", result)

    def test_anchor_drift_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "anchor count"):
            adapter.patch("#!/usr/bin/env bash\nwindow() { :; }\n", OWNER, WIRE)

    def test_duplicate_anchor_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "anchor count"):
            adapter.patch(adapter.OLD_WINDOW + adapter.OLD_WINDOW, OWNER, WIRE)

    def test_generated_minimal_shell_parses(self) -> None:
        source = "#!/usr/bin/env bash\nTOOL=/tmp/tool\n" + adapter.OLD_WINDOW
        result = adapter.patch(source, OWNER, WIRE)
        with tempfile.NamedTemporaryFile("w", delete=False) as handle:
            handle.write(result)
            path = Path(handle.name)
        try:
            completed = subprocess.run(
                ["bash", "-n", str(path)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
