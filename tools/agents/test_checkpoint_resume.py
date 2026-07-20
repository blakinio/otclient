#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


checkpoint = load_module("checkpoint", ROOT / "tools/agents/checkpoint.py")


class CheckpointResumeTests(unittest.TestCase):
    def setUp(self):
        self.contract = checkpoint.load_contract(ROOT / "docs/agents/GOVERNANCE_CONTRACT.json")

    def sample(self):
        return {
            "checkpoint_version": "1", "updated_at": "2026-07-20T00:00:00Z", "head": "abc123",
            "branch": "docs/test", "pr": "1", "status": "implementing", "context_routes": ["none"],
            "owned_paths": ["docs/**"], "proven": ["checkpoint exists"], "derived": [], "unknown": [],
            "conflicts": [], "first_failure": {"marker": "none", "evidence": "none"},
            "rejected_hypotheses": [], "changed_paths": ["docs/test.md"],
            "validation": [{"command": "unit", "result": "PASS", "evidence": "local"}],
            "blockers": [], "next_action": "Run the final validation.",
        }

    def test_valid_checkpoint(self):
        self.assertEqual(checkpoint.validate_checkpoint(self.sample(), self.contract), [])

    def test_placeholder_next_action_rejected(self):
        data = self.sample(); data["next_action"] = "TODO"
        self.assertTrue(any("next_action" in e for e in checkpoint.validate_checkpoint(data, self.contract)))

    def test_compactness_limit_rejected(self):
        data = self.sample(); limit = self.contract.compactness_limits["proven"]
        data["proven"] = [f"fact {i}" for i in range(limit + 1)]
        self.assertTrue(any("compactness limit" in e for e in checkpoint.validate_checkpoint(data, self.contract)))


if __name__ == "__main__":
    unittest.main()
