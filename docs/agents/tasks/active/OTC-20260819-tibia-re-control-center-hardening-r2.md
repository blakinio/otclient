---
task_id: OTC-20260819-tibia-re-control-center-hardening-r2
status: validating
agent: ChatGPT
project_lane: otclient
lane: P0-DESIGN-HARDENING
track_id: official-client-re
task_kind: architecture_contract_hardening
phase: validation
risk: medium
branch: docs/OTC-20260819-tibia-re-control-center-hardening-r2
base_branch: main
created: 2026-08-19T23:40:48+02:00
updated: 2026-08-20T00:17:54+02:00
initial_base_sha: fdabf235ed4438bd7c376932ed876bd0bbef019a
related_pr: 613
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
execution_mode: github_connector_after_local_runner_outage
owned_paths:
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_SCENARIO_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_COMPARISON_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_POLICY_BOUNDARY_V1.md
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
  - current Surveyor producer only after an accepted exact schema/commit/interface exists
  - blakinio/Oteryn-v2 docs/architecture/ADR-0007-native-end-to-end-test-platform.md
blocks:
  - Package A until a repaired exact head has P0/P1 NONE and PACKAGE_A_IMPLEMENTATION_READY=YES from a fresh independent audit
---

# TIBIA RE Control Center hardening remediation r2

## Goal

Close every material finding from independent audit review `4976939865`, reconcile the hardening with current `main`, and produce a truthful exact-head readiness candidate without implementing Package A or touching Track A runtime.

## Verified starting state

- Trusted `main` at initial claim: `fdabf235ed4438bd7c376932ed876bd0bbef019a`; live main advanced during remediation and must be rechecked at final validation.
- PR #605 exact audited head: `5e63a0ec988cf4fa7789274f13c9d654254e8e44`.
- Independent result on #605: `FAIL`, P0=0, P1=4, P2=4, `PACKAGE_A_IMPLEMENTATION_READY=NO`.
- #605 was closed unmerged as superseded after its unchanged exact head was audited.
- PR #613 is the sole Control Center hardening successor.
- PR #609/Ollama PoC merged into main and remains a related future consumer only; Policy Boundary v1 prevents it from becoming Control Center/safety authority.
- Surveyor remains a future accepted-producer dependency for Package C; historical PR numbers are discovery hints, not acceptance authority.
- This task has `runtime_access:none`; physical/runtime/browser E2E is `NOT_APPLICABLE` for this documentation/contract remediation.

## Acceptance criteria

- [x] Define all Scenario v1 safety-critical types and selector schemas without free-form core action ambiguity.
- [x] Make action success terminality and post-dispatch ambiguity semantics explicit.
- [x] Make STOP/reset state durable and fail closed across backend restart without violating dispatch-gate I/O discipline.
- [x] Close RequestLedger crash windows with durable pre-domain request/resource reservation and backend-global storage.
- [x] Reconcile normative read sets, task ownership, retry bounds and request-ledger topology.
- [x] Preserve the architecture boundary that Ollama/future policy is downstream of normalized state and bounded semantic requests, never deterministic safety/authority.
- [ ] Run final changed-file/self-review plus repository-required exact-head documentation/governance/CI validation on PR #613.
- [ ] Obtain a fresh genuinely independent audit of the final unchanged head before Package A readiness/merge.

## Remediation mapping

- `CC-AUD-001`: Scenario v1 now normatively defines `SideEffectBudget`, `AbortCondition`, `SemanticFieldPath` and closed per-kind entity/item/destination references.
- `CC-AUD-002`: Execution v1 makes `CONFIRMED` the only terminal successful lifecycle state.
- `CC-AUD-003`: Artifact/Execution v1 define durable backend-global STOP/reset plus backend-active/unclean-restart `recovery_required` behavior, including STOP-persistence-failure followed by crash.
- `CC-AUD-004`: Artifact/Control API v1 require preallocated final resource identity and durable RequestLedger `ACCEPTED` before resource creation/scheduling.
- `CC-AUD-005`: programme/MVP/audit normative sets include Artifact/Comparison and the new Policy Boundary contract where applicable.
- `CC-AUD-006`: successor owns the full changed contract/programme/prompt/task/catalog surface; #605 ownership is released/archived.
- `CC-AUD-007`: `retry.max_attempts` is `1..3` total attempts.
- `CC-AUD-008`: authoritative RequestLedger is backend-global and valid before any run directory exists.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-20T00:17:54+02:00
content_head_before_checkpoint_commit: 1bd53e79a01b62b12b2cad102fff45f4d8ea29fa
branch: docs/OTC-20260819-tibia-re-control-center-hardening-r2
pr: 613
status: validating
context_routes:
  - TIBIA_RE_CONTROL_CENTER_E2E
  - TIBIA_RE_CONTROL_CENTER_POLICY_BOUNDARY_V1
  - Track_A_runtime_access_none
proven:
  - independent review 4976939865 blocked Package A on four P1 and four P2 gaps on unchanged #605 head
  - all eight recorded #605 findings have explicit successor contract/task remediation
  - successor adds conservative active-backend/recovery-required semantics for STOP-persistence-failure-plus-crash
  - future policy/Ollama remains downstream of deterministic Control Center safety/authority
  - current-main drift observed through c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd touched only Surveyor-v2 prompt/evidence/task paths and did not overlap Control Center-owned paths
  - no runtime access is required or authorized
unknown:
  - final exact-head workflow/check result after the final metadata/content commit
  - fresh independent exact-head audit result
blockers:
  - fresh independent exact-head Control Center audit is required before Package A readiness/merge
next_action: inspect exact #613 diff/current main/open overlap, resolve any stale/contradictory text, then validate exact-head workflows and persist the final audit handoff SHA
```
