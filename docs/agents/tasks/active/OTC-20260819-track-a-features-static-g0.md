---
task_id: OTC-20260819-track-a-features-static-g0
status: ready
session_id: chatgpt-20260819-tibia-re-features
session_role: researcher
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion-gate
branch: research/OTC-20260819-track-a-features-static-model
base_branch: main
base_main: cf90b84442dda730bdab93d8aa9f3236b7532ad8
source_pr: 560
source_head: PR_560_EXACT_HEAD_RECORDED_IN_GITHUB_METADATA
created: 2026-08-19T09:41:47+02:00
updated: 2026-08-19T10:04:10+02:00
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
  - docs/agents/tasks/active/OTC-20260819-track-a-features-static-g0.md
  - docs/agents/reports/OTCLIENT-20260819-track-a-features-static-g0.md
  - docs/agents/evidence/OTC-20260819-track-a-features-static-g0/**
retired_producer_path:
  - .github/workflows/track-a-features-static-g0.yml
dependencies:
  - promoted public-package fingerprint from PR #551
  - PR #536 is read-only planning input only; its shared matrix paths are not owned
related_prs:
  - 536
  - 550
  - 551
  - 555
  - 560
producer_run: 32229656311
producer_job: 95996576897
producer_artifact: 9356800104
producer_artifact_digest_reported: sha256:779f2d1af266ad0327191a5fda1289a524884c1a9fdb2c4d351d3de3dcaab8d0
---

# Track A feature-systems static G0

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
complete_user_facing_feature: false
physical_e2e: NOT_APPLICABLE
physical_e2e_reason: static GitHub-hosted reverse-engineering package with runtime_access none
```

## Producer result

```text
run/job: 32229656311 / 95996576897 = SUCCESS
producer_head: 9ae46d14807e46e76c044c336e50033b11fa3a1e
artifact: 9356800104
GitHub-reported artifact digest: sha256:779f2d1af266ad0327191a5fda1289a524884c1a9fdb2c4d351d3de3dcaab8d0
packed sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size: 52109920
current public package fence: PASS
QMeta classes: 61
feature strings: 818
protocol strings: 13
raw client retained: false
```

Task-local proposed deltas against PR #536 planning state:

```text
G01 NOT_STARTED -> PARTIAL
G04 NOT_STARTED -> PARTIAL
G05 NOT_STARTED -> PARTIAL
G06 NOT_STARTED -> PARTIAL
```

These proposals are not canonical promotions and the shared matrix/checklist remains untouched.

## Acceptance inventory

- [x] Fetch the public Linux package only in an ephemeral GitHub-hosted job and fail closed unless the exact promoted public-package packed/unpacked fingerprint is reproduced.
- [x] Enumerate exact-package Qt class ownership plus methods/signals/properties/enums for Cyclopedia/Bestiary/Charm/Monster Bonus surfaces.
- [x] Retain exact-package feature/protocol strings needed to distinguish controller/storage/handler/request/action boundaries.
- [x] Do not infer per-method code targets from heuristic jump-table recovery.
- [x] Classify all material conclusions as FACT / INFERENCE / UNKNOWN and keep current runtime semantics UNKNOWN.
- [x] Persist only compact text evidence; delete packed/unpacked client before artifact upload.
- [x] Leave G24-G31 economy-panel scope untouched and do not modify PR #536 shared matrix/checklist.
- [x] Record exact next discriminator for every remaining UNKNOWN needed before any row could become DONE.
- [x] Run proportional validation on the final rebased Draft content.
- [x] Stop at a Draft PR for coordinator review; do not self-promote or merge.

## Durable evidence

- `docs/agents/evidence/OTC-20260819-track-a-features-static-g0/20260819-current-package-cyclopedia-bestiary-charms-bonus.md`
- `docs/agents/reports/OTCLIENT-20260819-track-a-features-static-g0.md`
- GitHub Actions run `32229656311`, job `95996576897`, artifact `9356800104`.

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
phase: coordinator-promotion-gate
validation_level: proportional
last_completed_step: producer evidence persisted; producer workflow retired; branch rebased onto current main; final diff reduced to three task-owned documentation/evidence paths
next_action: coordinator independently audits exact Draft PR #560 head, checks final GitHub CI/governance, and promotes accepted deltas without mutating this researcher branch
```

## Invocation counters

```yaml
invocation_started_at: 2026-08-19T09:27:00+02:00
last_progress_at: 2026-08-19T10:04:10+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
```
