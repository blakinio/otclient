#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
SCANNER = ROOT / ".github/scripts/test_track_a_selfhosted_pr_boundary.py"
CANONICAL = ROOT / ".github/workflows/tibia-official-client-re-canonical-live-lease.yml"
TASK = ROOT / "docs/agents/tasks/active/OTC-20260829-track-a-selfhosted-pr-boundary.md"
CONTRACT = ROOT / "docs/agents/contracts/TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md"


def fail(finding_id: str, message: str) -> None:
    raise SystemExit(f"{finding_id}: {message}")


def load_scanner():
    spec = importlib.util.spec_from_file_location("track_a_boundary_subject", SCANNER)
    if spec is None or spec.loader is None:
        fail("AUDIT-F001", "cannot load boundary scanner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_changed_paths(base: str) -> set[str]:
    # This is a reusable current-tree security audit, not a historical #795
    # patch allowlist. Future PRs may legitimately change unrelated files;
    # the repo-wide scanner below decides whether their self-hosted jobs are
    # safe. Keep only exact diff readability/non-empty hygiene here.
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-only", base],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as exc:
        fail("AUDIT-F002", f"cannot enumerate exact diff from {base}: {exc}")
    changed = {line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()}
    if not changed:
        fail("AUDIT-F003", "pull-request audit received an empty exact diff")
    return changed


def verify_predicate_counterexamples(module) -> None:
    fixtures = [
        (
            "github.event_name == 'workflow_dispatch' || github.event_name == 'pull_request'",
            False,
            "mixed dispatch/pull_request OR",
        ),
        (
            "(github.event_name == 'pull_request') || (github.event_name == 'issue_comment')",
            False,
            "reversed mixed pull_request OR",
        ),
        (
            "github.event_name == 'issue_comment' && (github.event.comment.body == 'A' || github.event.comment.body == 'B')",
            True,
            "nested non-event OR under issue_comment",
        ),
        (
            "(github.event_name == 'issue_comment' || github.event_name == 'workflow_dispatch') && github.actor == github.repository_owner",
            True,
            "OR of two non-PR event guards",
        ),
        (
            "(github.event_name == 'issue_comment' && github.actor == github.repository_owner) || (github.event_name == 'pull_request' && github.actor == github.repository_owner)",
            False,
            "nested PR-admitting branch",
        ),
        (
            "github.event_name != 'pull_request' && github.actor == github.repository_owner",
            True,
            "explicit pull_request exclusion",
        ),
        (
            "github.event_name != 'issue_comment' && github.actor == github.repository_owner",
            False,
            "inequality that still admits pull_request",
        ),
        (
            "github.actor == github.repository_owner",
            False,
            "no event constraint",
        ),
    ]
    for expression, expected_safe, label in fixtures:
        block = f"  audit:\n    if: {expression}\n    runs-on: [otclient, synology]\n"
        actual = module.pull_request_excluded(block)
        if actual is not expected_safe:
            fail(
                "AUDIT-F005",
                f"predicate classification mismatch for {label}: expected_safe={expected_safe} actual={actual}",
            )


def verify_canonical_gate() -> None:
    text = CANONICAL.read_text(encoding="utf-8")
    match = re.search(
        r"(?ms)^  isolated-selfhosted:\s*\n(?P<body>.*?)(?=^  [A-Za-z0-9_.-]+:\s*\n|\Z)",
        text,
    )
    if not match:
        fail("AUDIT-F006", "canonical isolated-selfhosted job not found")
    body = match.group("body")
    if "runs-on: [otclient, synology]" not in body:
        fail("AUDIT-F007", "canonical physical runner selector changed unexpectedly")
    prefix = body.split("runs-on:", 1)[0]
    required = (
        "github.event_name == 'workflow_dispatch'",
        "github.actor == github.repository_owner",
        "github.ref == 'refs/heads/main'",
    )
    missing = [item for item in required if item not in prefix]
    if missing:
        fail("AUDIT-F008", "canonical pre-scheduling gate missing: " + ", ".join(missing))
    if "||" in prefix:
        fail("AUDIT-F009", "canonical physical pre-scheduling gate unexpectedly contains OR")


def verify_no_runtime_authority() -> None:
    task = TASK.read_text(encoding="utf-8")
    for exact in (
        "runtime_access: none",
        "mutation_authorized: false",
        "credentials_allowed: false",
        "login_allowed: false",
        "physical_action_budget: 0",
        "physical_action_count: 0",
    ):
        if exact not in task.split("---", 2)[1]:
            fail("AUDIT-F010", f"task metadata missing exact no-runtime fence: {exact}")

    contract = CONTRACT.read_text(encoding="utf-8")
    required_contract_phrases = (
        "Repository workflow checks are defense in depth only",
        "offline and not busy",
        "fresh one-job environment",
        "GITHUB_RUN_ATTEMPT",
        "credentials/login remain forbidden",
    )
    missing = [item for item in required_contract_phrases if item not in contract]
    if missing:
        fail("AUDIT-F011", "secret-runner contract missing fail-closed invariant: " + ", ".join(missing))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="exact PR base SHA/ref for full-diff audit")
    args = parser.parse_args()

    verify_changed_paths(args.base)
    module = load_scanner()
    verify_predicate_counterexamples(module)
    verify_canonical_gate()
    verify_no_runtime_authority()
    print("TRACK_A_SELFHOSTED_PR_INDEPENDENT_AUDIT=PASS")
    print("AUDIT_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
