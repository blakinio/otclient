from __future__ import annotations

import re
from pathlib import Path

UPDATED = "2026-08-04T08:22:00+02:00"
HEAD = "daa7e5b09c06551a6f4ad94a69d00cbf65319133"
BRANCH = "feat/OTC2-20260803-canary-entity-reconciliation"
PR = 252

TASK = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
EVIDENCE = Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md")

task = TASK.read_text(encoding="utf-8")
replacements = {
    "status: implementing": "status: validating",
    "phase: entity-reconciliation-implementation": "phase: entity-reconciliation-terminal-ci",
    "updated: 2026-08-04T08:10:00+02:00": f"updated: {UPDATED}",
    "last_progress_at: 2026-08-04T08:10:00+02:00": f"last_progress_at: {UPDATED}",
    "ci_check_generation: entity-reconciliation-focused": "ci_check_generation: entity-reconciliation-final-exact-head",
    "ci_checks_for_current_head: 0": "ci_checks_for_current_head: 2",
    "repair_cycles_for_current_gate: 0": "repair_cycles_for_current_gate: 1",
}
for old, new in replacements.items():
    if old in task:
        task = task.replace(old, new, 1)

section_old = "shared_path_lease: []\nvalidation: pending\n```"
section_new = """shared_path_lease: []
validation:
  exact_product_head: daa7e5b09c06551a6f4ad94a69d00cbf65319133
  rust_client_run: 30883311792
  windows_job: 91909062725
  supply_chain_job: 91909062730
  repository_ci_run: 30883312109
  repository_required_job: 91909281559
  result: PASS
```"""
if section_old in task:
    task = task.replace(section_old, section_new, 1)

checkpoint_pattern = re.compile(r"# Durable checkpoint\n\n```yaml\n.*?\n```\n?", re.DOTALL)
checkpoint = f"""# Durable checkpoint

```yaml
checkpoint_version: 27
updated_at: {UPDATED}
observed_main: 2a7a179633bb345dc4013563967a89f4fc47d233
status: validating
phase: entity-reconciliation-terminal-ci
active_branch: {BRANCH}
pr: {PR}
base: 2a7a179633bb345dc4013563967a89f4fc47d233
validated_product_head: {HEAD}
changed_paths:
  - oteryn-client/crates/protocol-canary/src/lib.rs
  - oteryn-client/crates/protocol-canary/src/reconciliation.rs
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-entity-movement.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-entity-movement-trailing.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-entity-removal.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-entity-removal-invalid-stack.hex
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
implementation:
  remote_entity_movement_0x6D: complete
  remote_entity_removal_0x6C: complete
  caller_owned_resolver: complete_read_only_contract
validation:
  rust_client:
    run: 30883311792
    windows_job: 91909062725
    supply_chain_job: 91909062730
    locked_metadata: PASS
    formatting: PASS
    strict_workspace_clippy: PASS
    workspace_tests: PASS
    architecture: PASS
    supply_chain: PASS
  repository_ci:
    run: 30883312109
    required_job: 91909281559
    result: PASS
fresh_audit:
  exact_head: {HEAD}
  comment_id: 5175281373
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
remaining_blocker: General AddItem decoding still requires authoritative item-type and runtime branch metadata; local-player movement requires complete map-strip decoding.
next_action: Run final exact-head CI for this validation checkpoint, mark PR 252 ready, protected-merge it, then persist post-merge blocked parent state with no shared lease.
```
"""
if not checkpoint_pattern.search(task):
    raise RuntimeError("durable checkpoint not found")
task = checkpoint_pattern.sub(checkpoint, task, count=1)
TASK.write_text(task, encoding="utf-8", newline="\n")

evidence = EVIDENCE.read_text(encoding="utf-8")
evidence = evidence.replace(
    f"Status: implementation validation pending on `{BRANCH}` / PR `#{PR}`.",
    f"Status: exact product validation passed on `{HEAD}` / PR `#{PR}`; final checkpoint CI pending.",
    1,
)
validation_marker = "## Entity reconciliation validation"
if validation_marker not in evidence:
    evidence += f"""

## Entity reconciliation validation

```yaml
product_head: {HEAD}
rust_client:
  run: 30883311792
  windows_job: 91909062725
  supply_chain_job: 91909062730
  locked_metadata: PASS
  formatting: PASS
  strict_workspace_clippy: PASS
  workspace_tests: PASS
  architecture: PASS
  supply_chain: PASS
repository_ci:
  run: 30883312109
  required_job: 91909281559
  result: PASS
fresh_audit:
  comment_id: 5175281373
  result: PASS
  critical_high_material_medium_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: Isolated producer adapter over already decrypted and deframed logical messages; no real transport, admission, simulation mutation, renderer or reachable user journey.
```
"""
EVIDENCE.write_text(evidence, encoding="utf-8", newline="\n")
