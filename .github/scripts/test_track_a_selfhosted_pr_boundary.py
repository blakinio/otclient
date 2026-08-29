#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
SELF_HOSTED_RE = re.compile(
    r"(?m)^\s{4}runs-on:\s*(?:self-hosted|\[[^\n]*(?:self-hosted|otclient|synology)[^\n]*\])\s*(?:#.*)?$"
)
JOB_RE = re.compile(r"^  ([A-Za-z0-9_.-]+):\s*(?:#.*)?$")


def has_pull_request_event(text: str) -> bool:
    if re.search(r"(?m)^on:\s*\[[^\n]*\bpull_request\b", text):
        return True
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() != "on:":
            continue
        for candidate in lines[idx + 1 :]:
            if candidate and not candidate.startswith((" ", "\t")):
                break
            if re.match(r"^  pull_request:\s*", candidate):
                return True
        return False
    return False


def job_blocks(text: str):
    lines = text.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == "jobs:") + 1
    except StopIteration:
        return
    current_name = None
    current = []
    for line in lines[start:]:
        m = JOB_RE.match(line)
        if m:
            if current_name is not None:
                yield current_name, "\n".join(current)
            current_name = m.group(1)
            current = [line]
        elif current_name is not None:
            current.append(line)
    if current_name is not None:
        yield current_name, "\n".join(current)


def pull_request_excluded(block: str) -> bool:
    lines = block.splitlines()
    expression = ""
    for idx, line in enumerate(lines):
        m = re.match(r"^    if:\s*(.*)$", line)
        if not m:
            continue
        expression = m.group(1).strip()
        for continuation in lines[idx + 1 :]:
            if re.match(r"^    [A-Za-z0-9_.-]+:\s*", continuation):
                break
            if continuation.startswith("      "):
                expression += " " + continuation.strip()
        break
    if not expression:
        return False
    normalized = expression.replace('"', "'")
    if re.search(r"github\.event_name\s*!=\s*'pull_request'", normalized):
        return True
    if re.search(
        r"github\.event_name\s*==\s*'(?:issue_comment|workflow_dispatch|workflow_call|schedule)'",
        normalized,
    ):
        return True
    if re.search(r"github\.event_name\s*==\s*'pull_request'", normalized):
        return False
    # References such as github.event.issue.pull_request are payload fields, not
    # proof that the job can run for a pull_request event. Without an explicit
    # non-PR event gate, however, the job remains unsafe by default.
    return False


unsafe = []
for path in sorted(WORKFLOWS.glob("*.y*ml")):
    text = path.read_text(encoding="utf-8")
    if not has_pull_request_event(text):
        continue
    for job_name, block in job_blocks(text):
        if not SELF_HOSTED_RE.search(block):
            continue
        if not pull_request_excluded(block):
            unsafe.append(f"{path.relative_to(ROOT)}::{job_name}")

if unsafe:
    raise SystemExit(
        "TRACK_A_SELFHOSTED_PR_BOUNDARY_RED: PR-controlled self-hosted jobs: "
        + ", ".join(unsafe)
    )

print("TRACK_A_SELFHOSTED_PR_BOUNDARY=PASS")
