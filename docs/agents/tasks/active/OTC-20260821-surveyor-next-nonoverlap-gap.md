---
task_id: OTC-20260821-surveyor-next-nonoverlap-gap
status: implementing
phase: implementing
agent: ChatGPT
project_lane: otclient
lane: P0-SURVEYOR
track_id: official-client-re
task_kind: implementation
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
  - docs/agents/tasks/archive/OTC-20260821-surveyor-next-nonoverlap-gap.md
  - docs/agents/evidence/OTC-20260821-surveyor-next-nonoverlap-gap/**
  - .github/workflows/track-a-surveyor-tests.yml
  - tools/tibia_re_surveyor/ui_settings.py
  - tools/tibia_re_surveyor/reader_registry.py
  - tools/tibia_re_surveyor/README.md
  - tests/tools/tibia_re_surveyor/test_ui_settings.py
  - tests/tools/tibia_re_surveyor/test_survey.py
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
decomposition_decision: phased
decomposition_reason: discovery selected one non-overlapping reader; the same task now owns implementation through validation, physical acceptance and closeout
invocation_started_at: 2026-08-21T21:27:00+02:00
last_progress_at: 2026-08-21T21:41:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
next_action: finish ui_settings_typed_reader implementation evidence, push PR #658, run exact-head CI/governance/audit, merge, then run trusted-main read-only physical acceptance
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

## Selected slice

Fresh repository-only collect-all on exact starting `main@dce8bbd0e78ceea3681a1fe1dab40d3c19ed7458` produced 169 rows, 12 aliases, 8 missing typed readers and privacy `PASS`. `world_minimap_typed_reader` ranked first at score 125 but is excluded by still-open overlapping PRs #475 and #593. `ui_settings_typed_reader` ranked second at score 65 and is the highest-ranked non-overlapping gap. Its prior exact-build UI/settings discovery task `OTC-20260819-track-a-ui-settings-static-model` is terminally archived with ownership released and no open UI/settings PR exists.

The implementation is deliberately bounded to the exact-build `tibia::config::TClientOptions` compiled model plus the two previously causally proven Master Volume persistence fields in `packages/Tibia/conf/clientoptions.json`. The reader does not claim complete settings semantics, live UI application state, `TClientOptions -> clientoptions.json` linkage, or QSettings linkage. It uses no process-memory access.

## Runtime boundary

No official-client runtime may be observed under this checkpoint. Before any later physical read-only observation, re-admit this task with an explicit non-conflicting runtime namespace and fresh `target_uniqueness: PROVEN`. Mutation remains false throughout this task.

## Terminal acceptance

The selected slice is complete only after focused/static validation, exact-current-build resolver, collect-all/privacy PASS, fresh independent audit, required exact-head CI/governance, implementation merge, trusted-main read-only physical E2E, durable evidence, intentional terminal state for all related PRs, archival/removal of the active task record and released ownership.