---
task_id: OTC-20260821-surveyor-next-nonoverlap-gap
status: investigating
phase: investigate
agent: ChatGPT
project_lane: otclient
lane: P0-SURVEYOR
track_id: official-client-re
task_kind: discovery
risk: medium
policy_version: 2
branch: feat/OTC-20260821-surveyor-next-nonoverlap-gap
base_main: dce8bbd0e78ceea3681a1fe1dab40d3c19ed7458
execution_mode: chat
execution_reason: live GitHub coordination plus deterministic repository/static discovery; physical evidence is deferred until a selected reader is merged
execution_class: github_hosted
persistent_session_role: consumer_of_runtime_evidence
physical_e2e_required: true
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
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
owned_paths:
  - docs/agents/tasks/active/OTC-20260821-surveyor-next-nonoverlap-gap.md
modules_touched:
  - tibia_re_surveyor
depends_on:
  - OTC-20260821-surveyor-action-protocol-reader
blocks: []
feature_scope:
  type: backend_only
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: true
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: discovery_first
decomposition_reason: current gap ranking and non-overlap must be recomputed before the concrete reader implementation surface is safe to claim
invocation_started_at: 2026-08-21T21:27:00+02:00
last_progress_at: 2026-08-21T21:33:46+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: run the fresh repository-only Surveyor collect-all from current main, recompute remaining typed-reader ranking, exclude live overlaps, then promote this same task to the selected implementation slice
---

# Surveyor v2 next non-overlap typed-reader slice

## Goal

Continue Surveyor v2 from current `main` after terminal `OTC-20260821-surveyor-action-protocol-reader`. Select the highest-value current P0/P1 typed-reader gap that is safe and non-overlapping, then complete that reader through implementation, validation, audit, protected merge, trusted-main read-only physical E2E, durable evidence and terminal archival.

## Frozen owner authority

The current owner request authorizes the bounded Surveyor continuation and read-only physical acceptance. It explicitly forbids gameplay input, relogin, client restart and process-memory writes. No credential use, character selection, process-control, injection, network mutation or transaction/economy action is authorized.

## Discovery acceptance

- Current `main` is the source of truth; historical gap counts and runtime IDs are discovery evidence only.
- Run repository-only `--collect-all` first under `runtime_access: none`.
- Inspect live open PRs and active task ownership before selecting a reader.
- Exclude `world_minimap_typed_reader` while #475/#593 or successor ownership overlaps remain active.
- Rank by canonical P0/P1 blocker impact, downstream rows, exact-current-build evidence, bounded read-only discrimination feasibility, implementation size and non-overlap.
- Update this task to `implementation` and extend `owned_paths` only after the selected slice is proven non-conflicting.

## Runtime boundary

No official-client runtime may be observed under this checkpoint. Before any later physical read-only observation, re-admit this task with an explicit non-conflicting runtime namespace and fresh `target_uniqueness: PROVEN`. Mutation remains false throughout this task.

## Terminal acceptance

The selected slice is complete only after focused/static validation, exact-current-build resolver, collect-all/privacy PASS, fresh independent audit, required exact-head CI/governance, implementation merge, trusted-main read-only physical E2E, durable evidence, intentional terminal state for all related PRs, archival/removal of the active task record and released ownership.