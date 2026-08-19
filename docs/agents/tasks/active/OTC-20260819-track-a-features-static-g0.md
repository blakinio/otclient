---
task_id: OTC-20260819-track-a-features-static-g0
status: investigating
session_id: chatgpt-20260819-tibia-re-features
session_role: researcher
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: research/OTC-20260819-track-a-features-static-model
base_branch: main
base_main: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
created: 2026-08-19T09:41:47+02:00
updated: 2026-08-19T09:41:47+02:00
risk: low
execution_mode: chat
execution_class: github_hosted
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
implementation_authorized: true
e2e_required: false
decomposition_decision: single
owned_paths:
  - .github/workflows/track-a-features-static-g0.yml
  - docs/agents/tasks/active/OTC-20260819-track-a-features-static-g0.md
  - docs/agents/reports/OTCLIENT-20260819-track-a-features-static-g0.md
  - docs/agents/evidence/OTC-20260819-track-a-features-static-g0/**
dependencies:
  - promoted public-package fingerprint from PR #551
  - PR #536 is read-only planning input only; its shared matrix paths are not owned
related_prs:
  - 536
  - 550
  - 551
  - 555
---

# Track A feature-systems static G3

## Objective

Execute the owner alias `TIBIA-RE-FEATURES` as a bounded draft-only researcher package. This first package targets the coherent read-only feature cluster:

```text
G01 Cyclopedia shell/request-cache model
G04 Bestiary kills/unlocks/loot/progress
G05 Charms selection/assignment
G06 Monster Bonus Effects
```

The alias mission remains `G01-G23` plus `G32-G41`; this task intentionally does not claim the whole mission complete. It establishes the first dedicated current-public-package static model without spending resources, rerolling, committing Forge/Imbuement operations, logging in, or using the physical runtime.

## Authority and isolation

```yaml
repository: blakinio/otclient
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
promotion_authority: coordinator_only
researcher_delivery: draft_pr_only
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
```

No writes are authorized to PR #536 shared coverage files, PR #550 economy-panel paths, PR #555 fence-governance paths, Track B, or any Synology runtime namespace.

## Feature scope

```yaml
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
complete_user_facing_featurezfalse
physical_e2e: NOT_APPLICABLE
physical_e2e_reason: static GitHub-hosted reverse-engineering package with runtime_access none
```

## Acceptance inventory

- [ ] Fetch the public Linux package only in an ephemeral GitHub-hosted job and fail closed unless the exact promoted public-package packed/unpacked fingerprint is reproduced.
- [ ] Enumerate exact-package Qt class ownership plus methods/signals/properties/enums for Cyclopedia/Bestiary/Charm/Monster Bonus surfaces.
- [ ] Retain exact-package feature/protocol strings needed to distinguish controller/storage/handler/request/action boundaries.
- [ ] Do not infer per-method code targets from heuristic jump-table recovery.
- [ ] Classify all material conclusions as FACT / INFERENCE / UNKNOWN and keep current runtime semantics UNKNOWN.
- [ ] Persist only compact text evidence; delete packed/unpacked client before artifact upload.
- [ ] Leave G24-G31 economy-panel scope untouched and do not modify PR #536 shared matrix/checklist.
- [ ] Record exact next discriminator for every remaining UNKNOWN needed before any row could become DONE.
- [ ] Run proportional validation on the final draft head.
- [ ] Stop at a Draft PR for coordinator review; do not self-promote or merge.

## Admission record

```yaml
track_id: official-client-re
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
```

## Recovery checkpoint

```yaml
policy_version: 2
phase: investigate
validation_level: focused
last_completed_step: live-state and ownership preflight completed; isolated worktree created
next_action: run the bounded GitHub-hosted feature census, persist compact evidence/report, remove the temporary workflow, and checkpoint the Draft PR for coordinator review
```

## Invocation counters

```yaml
invocation_started_at: 2026-08-19T09:27:00+02:00
last_progress_at: 2026-08-19T09:41:47+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
```
