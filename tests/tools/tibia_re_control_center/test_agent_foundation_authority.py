from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.tools.tibia_re_control_center.test_agent_api import task_envelope
from tests.tools.tibia_re_control_center.test_package_b import decode, http_call
from tools.tibia_re_control_center.control_api import ControlApiServer


class AgentFoundationAuthorityTests(unittest.TestCase):
    def test_production_api_rejects_nonzero_physical_action_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            server = ControlApiServer(Path(temp)).start()
            try:
                status, _, raw = http_call(
                    server,
                    "POST",
                    "/v1/agent/tasks",
                    body=task_envelope(physical_action_budget=1),
                    request_id="foundation-budget-rejected",
                )
                payload = decode(raw)
                self.assertEqual(400, status, payload)
                self.assertEqual("PHYSICAL_ACTION_BUDGET_UNAVAILABLE", payload["code"])
                self.assertEqual([], server.domain.adapter.physical_effects)
            finally:
                server.close()


if __name__ == "__main__":
    unittest.main()
