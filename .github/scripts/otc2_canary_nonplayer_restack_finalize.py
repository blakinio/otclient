from __future__ import annotations

import re
from pathlib import Path

UPDATED = "2026-08-04T12:47:00+02:00"
BASE = "133388d61b787fb1829d740d0a1db581dccc3c4e"
PRODUCT_HEAD = "f913e5ff5e4813e7ec2590122fc2ee3224aa901f"
RESTACK_HEAD = "3253268c94ff1e05ff8bbcba12b3713c7336d28e"
PR = 261
TASK = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
EVIDENCE = Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md")

task = TASK.read_text(encoding="utf-8")
task = re.sub(r'^updated: .*$', f'updated: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = re.sub(r'^required_base_commit: "[0-9a-f]{40}"$', f'required_base_commit: "{BASE}"', task, count=1, flags=re.MULTILINE)
task = re.sub(r'^last_progress_at: .*$', f'last_progress_at: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = task.replace("checkpoint_version: 36", "checkpoint_version: 37", 1)
task = re.sub(r'^updated_at: .*$', f'updated_at: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = re.sub(r'^observed_main: [0-9a-f]{40}$', f'observed_main: {BASE}', task, count=1, flags=re.MULTILINE)
task = re.sub(r'^base: [0-9a-f]{40}$', f'base: {BASE}', task, count=1, flags=re.MULTILINE)

recovery_pattern = re.compile(r"## Recovery checkpoint\n\n```yaml\n.*?\n```\n?", re.DOTALL)
recovery = f"""## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 3
  session_id: OTC2-20260804T1043+0200-nonplayer
  session_started_at: 2026-08-04T12:10:00+02:00
  checkpointed_at: {UPDATED}
  last_progress_at: {UPDATED}
  phase: unknown-nonplayer-appearance-current-main-restack
  exact_head: {RESTACK_HEAD}
  pull_request: {PR}
  active_operation: exact-head CI, protected merge and blocked-parent reconciliation on current main
  external_run_ids:
    - 30899069326
    - 30899073315
    - 30899539987
    - 30899539187
  operation_started_at: {UPDATED}
  wait_deadline_at: 2026-08-04T13:32:00+02:00
  check_generation: unknown-nonplayer-appearance-current-main
  checks_used: 4
  status: ready
  safe_to_resume: true
  resume_condition: Merge PR 261 only after the final restacked head passes all required checks; otherwise preserve the precise failure.
  next_action: Reconcile PR 261 terminal state, then continue the active parent task from its remaining item, nonzero-eviction, hidden, summon and extension blockers.
```
"""
if not recovery_pattern.search(task):
    raise RuntimeError("recovery checkpoint not found")
task = recovery_pattern.sub(recovery, task, count=1)
TASK.write_text(task, encoding="utf-8", newline="\n")

evidence = EVIDENCE.read_text(encoding="utf-8")
marker = "## Unknown non-player current-main restack"
if marker not in evidence:
    evidence += f"""

## Unknown non-player current-main restack

```yaml
pr: {PR}
current_base: {BASE}
validated_product_head: {PRODUCT_HEAD}
restack_head_before_metadata: {RESTACK_HEAD}
new_governance_read:
  - oteryn-client/AGENTS.md
  - oteryn-client/docs/architecture/ARCHITECTURE.md
  - oteryn-client/docs/architecture/decisions/ADR-001-dual-protocol-selection-and-async-transport.md
  - oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md
  - oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md
  - oteryn-client/docs/agents/PROGRAM.md
  - oteryn-client/docs/agents/WORKSTREAMS.md
adapter_isolation: PASS
changed_runtime_semantics_after_product_validation: false
final_exact_head_ci: pending
```
"""
EVIDENCE.write_text(evidence, encoding="utf-8", newline="\n")
