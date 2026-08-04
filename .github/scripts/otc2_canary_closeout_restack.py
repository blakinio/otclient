from __future__ import annotations

import re
import subprocess
from pathlib import Path

UPDATED = "2026-08-04T08:48:00+02:00"
SESSION_STARTED = "2026-08-04T07:54:00+02:00"
SESSION_ID = "OTC2-20260804T0754+0200-canary-continuation"
PR = 254
BRANCH = "docs/OTC2-20260803-canary-entity-reconciliation-closeout"
TASK = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
EVIDENCE = Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md")

main_head = subprocess.check_output(
    ["git", "rev-parse", "origin/main"], text=True
).strip()
pre_checkpoint_head = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True
).strip()

task = TASK.read_text(encoding="utf-8")

# Restack metadata onto the exact trusted current base.
task = re.sub(r'^updated: .*$', f'updated: {UPDATED}', task, count=1, flags=re.MULTILINE)
task = re.sub(
    r'^required_base_commit: "[0-9a-f]{40}"$',
    f'required_base_commit: "{main_head}"',
    task,
    count=1,
    flags=re.MULTILINE,
)
task = re.sub(
    r'^last_progress_at: .*$',
    f'last_progress_at: {UPDATED}',
    task,
    count=1,
    flags=re.MULTILINE,
)

# Remove stale blocker claims now resolved by merged PR #252.
task = task.replace(
    "  - accepted caller-owned position-and-stack-to-domain-handle resolver contract\n",
    "  - authoritative item-instance identity for generic removal and replacement\n",
    1,
)
task = task.replace(
    "  - complete movement map-strip and removal reconciliation families\n",
    "  - complete local-player appended map-strip reconciliation\n",
    1,
)
old_identity = """## Position/stack identity resolution

Remote movement and removal messages provide positions and stack indices. The merged protocol-neutral contracts require session-fenced domain handles. No accepted caller-owned resolver contract currently maps a position/stack observation to an authoritative entity or item handle without letting partial decoding mutate world state. Therefore movement and removal remain blocked rather than emitting guessed identities.
"""
new_identity = """## Position/stack identity resolution

Merged PR `#252` now provides a read-only caller-owned resolver for complete remote entity movement and entity-only removal. It supplies session-fenced entity identity and destination ordering only after bounded parsing succeeds, without mutating simulation. Generic item removal remains blocked because no authoritative item-instance resolver exists, and local-player movement remains blocked because its producer branch appends map-strip payloads whose general tile/item families are incomplete.
"""
if old_identity in task:
    task = task.replace(old_identity, new_identity, 1)

# Refresh the durable checkpoint base and closeout restack state.
task = task.replace(
    "observed_main: d41a8155547d197ee18f9f390091f32ee3e64af6",
    f"observed_main: {main_head}",
    1,
)
task = task.replace(
    "checkpoint_version: 28",
    "checkpoint_version: 29",
    1,
)
task = task.replace(
    "updated_at: 2026-08-04T08:31:00+02:00",
    f"updated_at: {UPDATED}",
    1,
)

recovery = f"""## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: {SESSION_ID}
  session_started_at: {SESSION_STARTED}
  checkpointed_at: {UPDATED}
  last_progress_at: {UPDATED}
  phase: entity-reconciliation-closeout-restack
  exact_head: {pre_checkpoint_head}
  pull_request: {PR}
  active_operation: protected closeout restack, exact-head CI and merge reconciliation
  external_run_ids:
    - 30884273540
    - 30884273648
    - 30884558259
  operation_started_at: {UPDATED}
  wait_deadline_at: 2026-08-04T09:33:00+02:00
  check_generation: closeout-restack-current-main
  checks_used: 0
  status: ready
  safe_to_resume: true
  resume_condition: Reconcile PR 254 against current main; merge only after its exact-head required checks pass, otherwise preserve the precise failure.
  next_action: Reconcile PR 254 terminal state, then retain the parent task at the authoritative item-catalogue and local-map-strip blocker.
```
"""
if "## Recovery checkpoint" in task:
    task = re.sub(
        r"## Recovery checkpoint\n\n```yaml\n.*?\n```\n?",
        recovery,
        task,
        count=1,
        flags=re.DOTALL,
    )
else:
    task = task.rstrip() + "\n\n" + recovery

TASK.write_text(task, encoding="utf-8", newline="\n")

evidence = EVIDENCE.read_text(encoding="utf-8")
marker = "## Closeout restack on current governance base"
if marker not in evidence:
    evidence += f"""

## Closeout restack on current governance base

```yaml
closeout_pr: {PR}
restacked_base: {main_head}
pre_checkpoint_head: {pre_checkpoint_head}
changed_runtime_paths: []
changed_closeout_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
product_validation_reused_from_exact_implementation_heads: true
final_closeout_exact_head_ci: pending
```
"""
EVIDENCE.write_text(evidence, encoding="utf-8", newline="\n")
