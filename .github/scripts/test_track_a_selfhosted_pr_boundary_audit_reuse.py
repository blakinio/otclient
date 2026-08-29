#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / ".github/scripts/audit_track_a_selfhosted_pr_boundary.py"

spec = importlib.util.spec_from_file_location("boundary_audit_subject", AUDIT)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

future_pr_diff = """.github/scripts/audit_track_a_current_login_field6_admission.py
.github/scripts/test_track_a_current_login_field6_security_contract.py
.github/scripts/track_a_current_login_field6_runtime.sh
.github/workflows/track-a-current-login-field6-runtime.yml
docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
"""
with patch.object(module.subprocess, "check_output", return_value=future_pr_diff):
    changed = module.verify_changed_paths("future-base")
expected = {line for line in future_pr_diff.splitlines() if line}
if changed != expected:
    raise SystemExit(f"AUDIT_REUSE_RED: unrelated future PR paths were not accepted: {changed!r}")

with patch.object(module.subprocess, "check_output", return_value=""):
    try:
        module.verify_changed_paths("empty-base")
    except SystemExit as exc:
        if "AUDIT-F003" not in str(exc):
            raise
    else:
        raise SystemExit("AUDIT_REUSE_RED: empty diff must fail closed")

print("TRACK_A_SELFHOSTED_PR_BOUNDARY_AUDIT_REUSE=PASS")
