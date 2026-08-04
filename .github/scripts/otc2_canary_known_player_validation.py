from __future__ import annotations

import re
from pathlib import Path

UPDATED = "2026-08-04T11:08:00+02:00"
PRODUCT_HEAD = "e952aea38ce93d873b0303556164e3f7a118f1d5"
BRANCH = "feat/OTC2-20260804-canary-known-player-appearance"
PR = 256
RUST_RUN = 30894575347
WINDOWS_JOB = 91944323324
SUPPLY_JOB = 91944323203
CI_RUN = 30894574150
REQUIRED_JOB = 91944797163
AUDIT_COMMENT = 5176900934

TASK = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
EVIDENCE = Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md")

task = TASK.read_text(encoding="utf-8")
replacements = {
    "status: implementing": "status: validating",
    "phase: known-player-appearance-implementation": "phase: known-player-appearance-terminal-ci",
    "updated: 2026-08-04T10:52:00+02:00": f"updated: {UPDATED}",
    "last_progress_at: 2026-08-04T10:52:00+02:00": f"last_progress_at: {UPDATED}",
    "ci_check_generation: known-player-appearance-focused": "ci_check_generation: known-player-appearance-final-exact-head",
    "terminal_ci_checks_for_current_generation: 0": "terminal_ci_checks_for_current_generation: 2",
    "repair_cycles_for_current_gate: 0": "repair_cycles_for_current_gate: 1",
}
for old, new in replacements.items():
    if old in task:
        task = task.replace(old, new, 1)

task = task.replace(
    "shared_path_lease: []\nvalidation: pending\n```",
    f"""shared_path_lease: []
validation:
  product_head: {PRODUCT_HEAD}
  rust_client_run: {RUST_RUN}
  windows_job: {WINDOWS_JOB}
  supply_chain_job: {SUPPLY_JOB}
  repository_ci_run: {CI_RUN}
  repository_required_job: {REQUIRED_JOB}
  result: PASS
```""",
    1,
)

checkpoint_pattern = re.compile(r"# Durable checkpoint\n\n```yaml\n.*?\n```\n?", re.DOTALL)
checkpoint = f"""# Durable checkpoint

```yaml
checkpoint_version: 31
updated_at: {UPDATED}
observed_main: 694314af9162b4e435d4b269dbec6ebe7b0a83e4
status: validating
phase: known-player-appearance-terminal-ci
active_branch: {BRANCH}
pr: {PR}
base: 694314af9162b4e435d4b269dbec6ebe7b0a83e4
validated_product_head: {PRODUCT_HEAD}
changed_paths:
  - oteryn-client/crates/protocol-canary/src/lib.rs
  - oteryn-client/crates/protocol-canary/src/known_player.rs
  - oteryn-client/crates/protocol-canary/src/known_player/tests.rs
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/known-remote-player-appearance.hex
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
implementation:
  known_remote_player_appearance_0x6A_0x62: complete
  cache_mutation: false
validation:
  rust_client:
    run: {RUST_RUN}
    windows_job: {WINDOWS_JOB}
    supply_chain_job: {SUPPLY_JOB}
    locked_metadata: PASS
    formatting: PASS
    strict_workspace_clippy: PASS
    workspace_tests: PASS
    architecture: PASS
    supply_chain: PASS
  repository_ci:
    run: {CI_RUN}
    required_job: {REQUIRED_JOB}
    result: PASS
fresh_audit:
  exact_head: {PRODUCT_HEAD}
  comment_id: {AUDIT_COMMENT}
  result: PASS
  critical_open: 0
  high_open: 0
  material_medium_open: 0
  unresolved_review_threads: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated producer adapter over already decrypted and deframed logical messages; no real transport, admission, simulation mutation, renderer or reachable user journey.
temporary_workflows_remaining: 0
temporary_scripts_remaining: 0
shared_path_lease: []
ownership:
  protocol_canary: retained
  shared_paths: released
remaining_blocker: General AddItem/non-empty map decoding still requires authoritative Current item metadata; local-player movement requires complete map strips; nonzero cache eviction and non-player creature branches remain incomplete.
next_action: Run final exact-head CI for the validation checkpoint, mark PR 256 ready, protected-merge it, then persist the active blocked parent state and continue to the next complete source-proven family.
```
"""
if not checkpoint_pattern.search(task):
    raise RuntimeError("durable checkpoint not found")
task = checkpoint_pattern.sub(checkpoint, task, count=1)

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
  phase: known-player-appearance-terminal-ci
  exact_head: {PRODUCT_HEAD}
  pull_request: {PR}
  active_operation: final exact-head CI, protected merge and blocked-parent reconciliation
  external_run_ids:
    - {RUST_RUN}
    - {CI_RUN}
  operation_started_at: {UPDATED}
  wait_deadline_at: 2026-08-04T11:53:00+02:00
  check_generation: known-player-appearance-final-exact-head
  checks_used: 2
  status: ready
  safe_to_resume: true
  resume_condition: Merge PR 256 only after the validation-record head passes all exact-head required checks; otherwise preserve the precise failure.
  next_action: Reconcile PR 256 terminal state, then continue the parent task from its remaining item and non-player creature blockers.
```
"""
if recovery_pattern.search(task):
    task = recovery_pattern.sub(recovery, task, count=1)
else:
    task = task.rstrip() + "\n\n" + recovery
TASK.write_text(task, encoding="utf-8", newline="\n")

evidence = EVIDENCE.read_text(encoding="utf-8")
evidence = evidence.replace(
    f"Status: implementation validation pending on `{BRANCH}` / PR `#{PR}`.",
    f"Status: exact product validation passed on `{PRODUCT_HEAD}` / PR `#{PR}`; final validation-record CI pending.",
    1,
)
marker = "## Known ordinary remote-player appearance validation"
if marker not in evidence:
    evidence += f"""

## Known ordinary remote-player appearance validation

```yaml
product_head: {PRODUCT_HEAD}
rust_client:
  run: {RUST_RUN}
  windows_job: {WINDOWS_JOB}
  supply_chain_job: {SUPPLY_JOB}
  locked_metadata: PASS
  formatting: PASS
  strict_workspace_clippy: PASS
  workspace_tests: PASS
  architecture: PASS
  supply_chain: PASS
repository_ci:
  run: {CI_RUN}
  required_job: {REQUIRED_JOB}
  result: PASS
fresh_audit:
  comment_id: {AUDIT_COMMENT}
  result: PASS
  critical_high_material_medium_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated producer adapter over already decrypted and deframed logical messages; no real transport, admission, simulation mutation, renderer or reachable user journey.
```
"""
EVIDENCE.write_text(evidence, encoding="utf-8", newline="\n")
