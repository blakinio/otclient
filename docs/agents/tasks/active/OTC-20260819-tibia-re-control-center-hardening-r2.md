---
task_id: OTC-20260819-tibia-re-control-center-hardening-r2
status: implementing
agent: ChatGPT
project_lane: otclient
lane: P0-DESIGN-HARDENING
track_id: official-client-re
task_kind: architecture_contract_hardening
phase: remediation
risk: medium
branch: docs/OTC-20260819-tibia-re-control-center-hardening-r2
base_branch: main
created: 2026-08-19T23:40:48+02:00
updated: 2026-08-19T23:40:48+02:00
initial_base_sha: fdabf235ed4438bd7c376932ed876bd0bbef019a
related_pr: ""
supersedes_pr: 605
independent_audit_review_id: 4976939865
independent_audit_head: 5e63a0ec988cf4fa7789274f13c9d654254e8e44
independent_audit_result: FAIL
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
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
context_pressure: high
context_growth: stable
decomposition_decision: phased
execution_mode: local_checkout
owned_paths:
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-hardening-r2.md
  - docs/agents/tasks/archive/OTC-20260819-tibia-re-control-center-hardening.md
depends_on:
  - merged Control Center design PR #600
  - merged audit-prompt PR #602
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - current trusted-main Track A authority/registration/Gate/supervisor/input-lock contracts
  - tools/tibia_runtime_bridge/**
  - PR #592 Surveyor only after an accepted exact producer state
  - blakinio/Oteryn-v2 docs/architecture/ADR-0007-native-end-to-end-test-platform.md
blocks:
  - Package A until a repaired exact head has P0/P1 NONE and PACKAGE_A_IMPLEMENTATION_READY=YES from a fresh independent audit
---

# TIBIA RE Control Center hardening remediation r2

## Goal

Close every material finding from independent audit review `4976939865`, reconcile the hardening with current `main`, and produce a truthful exact-head readiness candidate without implementing Package A or touching Track A runtime.

## Verified starting state

- Current trusted `main` at claim: `fdabf235ed4438bd7c376932ed876bd0bbef019a`.
- PR #605 exact audited head: `5e63a0ec988cf4fa7789274f13c9d654254e8e44`.
- Independent result: `FAIL`, P0=0, P1=4, P2=4, `PACKAGE_A_IMPLEMENTATION_READY=NO`.
- PR #609/Ollama PoC merged into current main and remains a related future consumer only.
- Surveyor PR #592 is still an unaccepted Draft producer dependency for future Package C.
- This task has `runtime_access:none`; physical/runtime E2E is `NOT_APPLICABLE` for this documentation/contract remediation.
## Acceptance criteria

- [ ] Define all Scenario v1 safety-critical types and selector schemas without free-form core action ambiguity.
- [ ] Make action success terminality and post-dispatch ambiguity semantics explicit.
- [ ] Make STOP/reset state durable and fail closed across backend restart without violating dispatch-gate I/O discipline.
- [ ] Close RequestLedger crash windows with durable pre-domain request/resource reservation and backend-global storage.
- [ ] Reconcile normative read sets, task ownership, retry bounds and request-ledger topology.
- [ ] Preserve current-main no-kill/adoption/Ollama changes while keeping Ollama downstream of Control Center contracts.
- [ ] Run documentation/governance validation and exact-head CI on the successor PR.
- [ ] Obtain a fresh genuinely independent audit of the final unchanged head before Package A readiness/merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-19T23:40:48+02:00
head: b29c79e0e7a20f239181343293f05eaa0fdaae6f
branch: docs/OTC-20260819-tibia-re-control-center-hardening-r2
pr: none
status: implementing
context_routes:
  - TIBIA_RE_CONTROL_CENTER_E2E
  - Track_A_runtime_access_none
proven:
  - independent review 4976939865 blocks Package A on four P1 contract gaps
  - branch is reconciled with main fdabf235ed4438bd7c376932ed876bd0bbef019a
  - no runtime access is required or authorized
unknown:
  - final exact-head independent-review result after remediation
blockers: []
next_action: repair CC-AUD-001 through CC-AUD-008, then run focused documentation/governance validation
```
