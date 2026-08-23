---
task_id: OTC-20260823-tibia-re-control-center-package-d-prep
status: implementing
agent: ChatGPT
project_lane: otclient
lane: P4-OFFICIAL-ADAPTER-PREP
track_id: official-client-re
task_kind: implementation
phase: design
risk: medium
branch: feat/OTC-20260823-tibia-re-control-center-package-d-prep
base_branch: main
base_main: 63100340f0dbe1aba16a20bc7febc8613291583d
created: 2026-08-23T12:40:12+02:00
updated: 2026-08-23T12:53:00+02:00
execution_mode: github_connector+github_actions
execution_reason: runtime-independent static Track A adapter preparation and deterministic repository validation
execution_budget_minutes: 120
execution_budget_reason: cohesive D-prep source mapping, hard-disabled adapter skeleton, repository-only E2E, fresh audit, exact-head CI, merge and lifecycle closeout
invocation_started_at: 2026-08-23T12:35:00+02:00
last_progress_at: 2026-08-23T12:53:00+02:00
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 9
estimate_confidence: medium
decomposition_decision: staged_prs
decomposition_reason: claim is merged first because the shared Package A workflow audits all Control Center source changes but intentionally does not admit unrelated task/evidence paths; implementation then uses a fresh branch and closeout evidence remains docs-only
validation_level: focused
session_id: chatgpt-20260823-package-d-prep
session_role: implementer
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
ci_checks_for_current_head: 0
ci_check_generation: claim
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
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
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
network_listener_allowed: false
official_client_access: false
real_package_d_runtime_authorized: false
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
execution_class: github_hosted
persistent_session_role: none
physical_e2e_required: false
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: true
implementation_status: in_progress
user_facing_feature_complete: false
missing_consumers:
  - future real Package D Official Tibia runtime adapter
  - current-runtime Track A E2E under separately admitted authority
owned_paths:
  - docs/agents/tasks/active/OTC-20260823-tibia-re-control-center-package-d-prep.md
  - docs/agents/tasks/archive/OTC-20260823-tibia-re-control-center-package-d-prep.md
  - docs/agents/evidence/OTC-20260823-tibia-re-control-center-package-d-prep/**
  - tools/tibia_re_control_center/official_adapter_contract.py
  - tests/tools/tibia_re_control_center/test_package_d_prep.py
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - tibia_re_control_center Official Tibia adapter preparation contract
  - Track A canonical authority/admission mechanisms (reuse by source reference only)
  - Control Center Scenario/Adapter semantic contracts (reuse only)
read_only_paths:
  - tools/tibia_runtime_bridge/**
  - tools/tibia_re_surveyor/**
  - existing Package A Control Center core files
  - Package B and Package C task/branch files
  - canonical Track A runtime state and authority surfaces
  - .github/scripts/tibia-official-client-re-canonical-live-lease
reuses:
  - tools/tibia_re_control_center/model.py semantic ActionRequest/EffectBound/Capability/AdapterIdentity types
  - tools/tibia_re_control_center/scenario.py supported action families and finite default EffectBound definitions
  - tools/tibia_re_control_center/execution.py coordinator one-shot dispatch commit semantics
  - existing Track A canonical lease/registration/supervisor/input-lock/evidence mechanisms by source reference only
depends_on:
  - Package A merge 13b3f02a07a176662d766352d9af39619775a73d
  - trusted-base Track A admission and canonical-runtime contracts at base_main
blocks: []
ownership_released: false
next_action: merge this task claim, branch from the resulting main, then implement the hard-disabled contract/tests plus same-PR catalogue/changelog updates
---

# Control Center Package D PREP — Official Tibia static adapter preparation

## Objective

Prepare the future Official Tibia adapter without touching any live Official Tibia runtime. Produce a source-backed Track A reuse map, a semantic action/evidence readiness matrix, the required external-guard ordering, and a hard-disabled typed adapter contract that cannot advertise or dispatch Official Tibia mutations.

## Authority boundary

This task is `runtime_access: none`. It must not inspect or mutate any Official Tibia process, container, KasmVNC/Remote Desktop surface, display/window, memory, credentials/login/session, network listener, canonical lease/registration state, Gate A/Gate B/rebind/bootstrap state, or physical gameplay. Historical/current runtime facts remain non-authoritative inputs for this static task.

## Preflight facts

- trusted `main` at claim start: `63100340f0dbe1aba16a20bc7febc8613291583d`
- Package A is merged at `13b3f02a07a176662d766352d9af39619775a73d`
- Package C is active on separate branch/PR and owns only its Surveyor provider/test/evidence/task paths; this D-PREP claim uses separate new paths
- no Package D branch existed at claim time
- the shared Package A workflow triggers on Control Center source/tests and its independent path audit intentionally rejects unrelated task/evidence paths; therefore task claim and final evidence/lifecycle closeout are docs-only PR stages around the implementation PR rather than weakening that audit

## Acceptance inventory

- [ ] Track A authority/identity/rebind/Gate/input/evidence reuse map is source-backed
- [ ] Scenario v1 action families have explicit readiness/evidence/gap rows
- [ ] no non-UNKNOWN Track A R/A grade is invented without current repository evidence
- [ ] at most one first-slice recommendation, otherwise `NO_ACTION_CANDIDATE_READY`
- [ ] finite EffectBound and post-effect confirmation requirements are explicit
- [ ] future dispatch order preserves external Track A guard continuously across final checks -> Control Center commit -> exactly one physical effect -> reconciliation
- [ ] local `dispatch_gate` is never described as the Track A authority mechanism
- [ ] STOP/control-generation invalidation is explicit after waiting for external authority
- [ ] semantic ActionRequest mapping exposes no raw key, GUI coordinate, opcode, address, pointer, process ID or bridge handle
- [ ] Official adapter identity alone grants no capability or mutation authority
- [ ] hard-disabled skeleton advertises no action capabilities
- [ ] hard-disabled skeleton refuses execution deterministically with `OFFICIAL_RUNTIME_NOT_ADMITTED`
- [ ] synthetic optimistic status cannot enable mutation
- [ ] repository-only request -> mapping/preflight -> refusal path proves zero physical dispatch
- [ ] Package A regression suite remains green
- [ ] no runtime/process/KasmVNC/Remote Desktop imports or calls are introduced
- [ ] fresh independent post-implementation audit passes
- [ ] exact-head required CI passes
- [ ] PR/task lifecycle is terminal and ownership released

## Validation evidence

Pending implementation. Physical Official Tibia E2E is intentionally outside this PREP task; repository-only E2E is required.
