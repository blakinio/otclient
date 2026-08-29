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


def job_if_expression(block: str) -> str:
    lines = block.splitlines()
    for idx, line in enumerate(lines):
        m = re.match(r"^    if:\s*(.*)$", line)
        if not m:
            continue
        expression = m.group(1).strip()
        if expression in {">-", ">", "|-", "|"}:
            expression = ""
        for continuation in lines[idx + 1 :]:
            if re.match(r"^    [A-Za-z0-9_.-]+:\s*", continuation):
                break
            if continuation.startswith("      "):
                expression += " " + continuation.strip()
        return expression.strip()
    return ""


def _strip_outer_parentheses(expression: str) -> str:
    expression = expression.strip()
    while expression.startswith("(") and expression.endswith(")"):
        depth = 0
        quoted = None
        encloses_all = True
        for idx, ch in enumerate(expression):
            if quoted:
                if ch == quoted and (idx == 0 or expression[idx - 1] != "\\"):
                    quoted = None
                continue
            if ch in {"'", '"'}:
                quoted = ch
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and idx != len(expression) - 1:
                    encloses_all = False
                    break
        if not encloses_all or depth != 0:
            break
        expression = expression[1:-1].strip()
    return expression


def _split_top_level(expression: str, operator: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    quoted = None
    start = 0
    idx = 0
    while idx < len(expression):
        ch = expression[idx]
        if quoted:
            if ch == quoted and (idx == 0 or expression[idx - 1] != "\\"):
                quoted = None
            idx += 1
            continue
        if ch in {"'", '"'}:
            quoted = ch
            idx += 1
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and expression.startswith(operator, idx):
            parts.append(expression[start:idx].strip())
            idx += len(operator)
            start = idx
            continue
        idx += 1
    if parts:
        parts.append(expression[start:].strip())
    return parts


def _can_admit_pull_request(expression: str) -> bool:
    expression = _strip_outer_parentheses(expression)
    disjuncts = _split_top_level(expression, "||")
    if disjuncts:
        return any(_can_admit_pull_request(part) for part in disjuncts)
    conjuncts = _split_top_level(expression, "&&")
    if conjuncts:
        return all(_can_admit_pull_request(part) for part in conjuncts)

    normalized = expression.replace('"', "'")
    equality = re.search(r"github\.event_name\s*==\s*'([^']+)'", normalized)
    if equality:
        return equality.group(1) == "pull_request"
    inequality = re.search(r"github\.event_name\s*!=\s*'([^']+)'", normalized)
    if inequality:
        return inequality.group(1) != "pull_request"
    # Unknown predicates may be true during a pull_request event. Fail closed.
    return True


def pull_request_excluded(block: str) -> bool:
    expression = job_if_expression(block)
    return bool(expression) and not _can_admit_pull_request(expression)



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
