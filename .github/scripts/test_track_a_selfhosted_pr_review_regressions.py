#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCANNER = ROOT / '.github/scripts/test_track_a_selfhosted_pr_boundary.py'
WORKFLOW = ROOT / '.github/workflows/tibia-official-client-re-canonical-live-lease.yml'

spec = importlib.util.spec_from_file_location('track_a_selfhosted_boundary', SCANNER)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

errors: list[str] = []

mixed = """  unsafe:\n    if: github.event_name == 'workflow_dispatch' || github.event_name == 'pull_request'\n    runs-on: [otclient, synology]\n"""
if module.pull_request_excluded(mixed):
    errors.append('mixed workflow_dispatch OR pull_request predicate was incorrectly accepted')

mixed_reversed = """  unsafe:\n    if: (github.event_name == 'pull_request') || (github.event_name == 'issue_comment')\n    runs-on: [otclient, synology]\n"""
if module.pull_request_excluded(mixed_reversed):
    errors.append('mixed pull_request OR issue_comment predicate was incorrectly accepted')

nested_non_event_or = """  safe:
    if: github.event_name == 'issue_comment' && (github.event.comment.body == 'A' || github.event.comment.body == 'B')
    runs-on: [otclient, synology]
"""
if not module.pull_request_excluded(nested_non_event_or):
    errors.append('nested non-event OR under issue_comment gate was incorrectly rejected')

safe = """  safe:\n    if: github.event_name == 'workflow_dispatch' && github.actor == github.repository_owner && github.ref == 'refs/heads/main'\n    runs-on: [otclient, synology]\n"""
if not module.pull_request_excluded(safe):
    errors.append('pure owner workflow_dispatch main-ref conjunction was incorrectly rejected')

text = WORKFLOW.read_text(encoding='utf-8')
block = dict(module.job_blocks(text)).get('isolated-selfhosted', '')
if "github.ref == 'refs/heads/main'" not in block.split('runs-on:', 1)[0]:
    errors.append('canonical lease self-hosted job does not require refs/heads/main before scheduling')

if errors:
    raise SystemExit('TRACK_A_SELFHOSTED_PR_REVIEW_REGRESSION_RED: ' + '; '.join(errors))
print('TRACK_A_SELFHOSTED_PR_REVIEW_REGRESSION=PASS')
