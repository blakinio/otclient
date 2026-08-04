from __future__ import annotations

import os
import re
from pathlib import Path

UPDATED = "2026-08-04T08:31:00+02:00"
MERGE = "d41a8155547d197ee18f9f390091f32ee3e64af6"
IMPLEMENTATION_HEAD = "41cfd39b847911d708429b8e23d4d17f9c1dc417"
PR_NUMBER = os.environ.get("PR_NUMBER", "pending")

TASK = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
EVIDENCE = Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md")

task = TASK.read_text(encoding="utf-8")
replacements = {
    "status: validating": "status: blocked",
    "phase: entity-reconciliation-terminal-ci": "phase: item-catalogue-and-local-map-strip-blocker",
    "branch: feat/OTC2-20260803-canary-entity-reconciliation": "branch: main",
    "updated: 2026-08-04T08:22:00+02:00": f"updated: {UPDATED}",
    'required_base_commit: "2a7a179633bb345dc4013563967a89f4fc47d233"': f'required_base_commit: "{MERGE}"',
    "last_progress_at: 2026-08-04T08:22:00+02:00": f"last_progress_at: {UPDATED}",
    "ci_check_generation: entity-reconciliation-final-exact-head": "ci_check_generation: entity-reconciliation-merged",
    "ci_checks_for_current_head: 2": "ci_checks_for_current_head: 3",
}
for old, new in replacements.items():
    if old in task:
        task = task.replace(old, new, 1)

related_match = re.search(r"^related_prs: \[(.*?)\]$", task, flags=re.MULTILINE)
if related_match and PR_NUMBER != "pending":
    values = [value.strip() for value in related_match.group(1).split(",") if value.strip()]
    if PR_NUMBER not in values:
        values.append(PR_NUMBER)
        task = task[: related_match.start()] + f"related_prs: [{', '.join(values)}]" + task[related_match.end() :]

checkpoint_pattern = re.compile(r"# Durable checkpoint\n\n```yaml\n.*?\n```\n?", re.DOTALL)
checkpoint = f"""# Durable checkpoint

```yaml
checkpoint_version: 28
updated_at: {UPDATED}
observed_main: {MERGE}
status: blocked
phase: item-catalogue-and-local-map-strip-blocker
active_branch: none
implementation_pr: 252
implementation_head: {IMPLEMENTATION_HEAD}
implementation_merge: {MERGE}
closeout_pr: {PR_NUMBER}
merged_slice:
  remote_entity_movement_0x6D: complete
  remote_entity_removal_0x6C: complete_entity_only
  caller_owned_resolver: complete_read_only_contract
validation:
  product_head:
    sha: daa7e5b09c06551a6f4ad94a69d00cbf65319133
    rust_client_run: 30883311792
    windows_job: 91909062725
    supply_chain_job: 91909062730
    repository_ci_run: 30883312109
    repository_required_job: 91909281559
    result: PASS
  exact_final_head:
    sha: {IMPLEMENTATION_HEAD}
    rust_client_run: 30883672329
    windows_job: 91910151945
    supply_chain_job: 91910151992
    repository_ci_run: 30883672401
    repository_required_job: 91910412579
    result: PASS
  ready_state:
    repository_ci_run: 30883947811
    repository_required_job: 91911322995
    result: PASS
fresh_audit:
  exact_head: {IMPLEMENTATION_HEAD}
  comment_id: 5175281373
  result: PASS
  critical_open: 0
  high_open: 0
  material_medium_open: 0
  unresolved_review_threads: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated producer adapter over already decrypted and deframed logical messages; no real transport, admission, simulation mutation, renderer or reachable user journey.
pr_hygiene:
  implementation_pr_252: merged
  implementation_merge: {MERGE}
  open_related_prs: 0
  unresolved_review_threads: 0
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
ownership:
  protocol_canary: retained_by_active_blocked_parent_task
  shared_paths: released
blocker: General AddItem/non-empty map decoding still requires authoritative Current item-type and runtime branch metadata; local-player movement requires complete appended map-strip decoding; known/cache-eviction and non-player creature branches remain incomplete.
next_action: Merge an accepted authoritative Current item-decoding dependency, then resume complete non-empty map/tile and local-player movement map-strip families without inference.
```
"""
if not checkpoint_pattern.search(task):
    raise RuntimeError("durable checkpoint not found")
task = checkpoint_pattern.sub(checkpoint, task, count=1)
TASK.write_text(task, encoding="utf-8", newline="\n")

evidence = EVIDENCE.read_text(encoding="utf-8")
evidence = evidence.replace(
    f"Status: exact product validation passed on `daa7e5b09c06551a6f4ad94a69d00cbf65319133` / PR `#252`; final checkpoint CI pending.",
    f"Status: entity reconciliation slice merged as `{MERGE}`; parent protocol task remains blocked on authoritative item metadata and local-player map strips.",
    1,
)
marker = "## Entity reconciliation post-merge closeout"
if marker not in evidence:
    evidence += f"""

## Entity reconciliation post-merge closeout

```yaml
implementation_pr: 252
implementation_head: {IMPLEMENTATION_HEAD}
implementation_merge: {MERGE}
closeout_pr: {PR_NUMBER}
final_exact_head_validation:
  rust_client_run: 30883672329
  windows_job: 91910151945
  supply_chain_job: 91910151992
  repository_ci_run: 30883672401
  repository_required_job: 91910412579
  result: PASS
ready_state_validation:
  repository_ci_run: 30883947811
  repository_required_job: 91911322995
  result: PASS
fresh_audit:
  comment_id: 5175281373
  result: PASS
  material_findings_open: 0
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
parent_task_status: blocked
remaining_blockers:
  - authoritative Current item-type and runtime AddItem branch metadata
  - complete local-player appended map-strip decoding
  - complete known/cache-eviction and non-player creature branches
```
"""
EVIDENCE.write_text(evidence, encoding="utf-8", newline="\n")
