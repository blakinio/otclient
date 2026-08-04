from __future__ import annotations

import re
from pathlib import Path

UPDATED = "2026-08-04T11:54:00+02:00"
BASE = "33da70afd159d9b9963e6e9d80398c298b26ff5d"
PR = 258
TASK = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
EVIDENCE = Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md")

task = TASK.read_text(encoding="utf-8")
task = re.sub(r'^updated: .*$', f'updated: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = re.sub(r'^required_base_commit: "[0-9a-f]{40}"$', f'required_base_commit: "{BASE}"', task, count=1, flags=re.MULTILINE)
task = re.sub(r'^last_progress_at: .*$', f'last_progress_at: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = task.replace("checkpoint_version: 33", "checkpoint_version: 34", 1)
task = re.sub(r'^updated_at: .*$', f'updated_at: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = re.sub(r'^observed_main: [0-9a-f]{40}$', f'observed_main: {BASE}', task, count=1, flags=re.MULTILINE)

recovery_pattern = re.compile(r"## Recovery checkpoint\n\n```yaml\n.*?\n```\n?", re.DOTALL)
recovery = f"""## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: OTC2-20260804T1043+0200-known-player
  session_started_at: 2026-08-04T10:43:00+02:00
  checkpointed_at: {UPDATED}
  last_progress_at: {UPDATED}
  phase: known-player-closeout-final-exact-head
  exact_head: pending_validation_record
  pull_request: {PR}
  active_operation: exact-head CI and protected closeout merge
  external_run_ids: []
  operation_started_at: {UPDATED}
  wait_deadline_at: 2026-08-04T12:34:00+02:00
  check_generation: known-player-closeout-final-exact-head
  checks_used: 0
  status: ready
  safe_to_resume: true
  resume_condition: Merge PR 258 only after all required checks pass on the exact final head.
  next_action: Reconcile PR 258 terminal state, then continue with the next source-proven non-player appearance family.
```
"""
if not recovery_pattern.search(task):
    raise RuntimeError("recovery checkpoint not found")
task = recovery_pattern.sub(recovery, task, count=1)
TASK.write_text(task, encoding="utf-8", newline="\n")

evidence = EVIDENCE.read_text(encoding="utf-8")
marker = "## Known-player closeout final current-main replay"
if marker not in evidence:
    evidence += f"""

## Known-player closeout final current-main replay

```yaml
closeout_pr: {PR}
base: {BASE}
final_diff_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
exact_head_validation: pending
```
"""
EVIDENCE.write_text(evidence, encoding="utf-8", newline="\n")
