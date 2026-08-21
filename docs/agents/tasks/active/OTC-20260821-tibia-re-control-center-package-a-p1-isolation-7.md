---
task_id: OTC-20260821-tibia-re-control-center-package-a-p1-isolation-7
status: waiting
agent: ChatGPT
project_lane: otclient
lane: P1-CONTROL-CORE
track_id: official-client-re
task_kind: repair
phase: audit
risk: medium
branch: feat/OTC-20260820-tibia-re-control-center-package-a
base_branch: main
created: 2026-08-21T13:34:00+02:00
updated: 2026-08-21T16:35:00+02:00
initial_base_sha: 5707af6c413cd9949f6c33b17744801cedef6eaf
related_pr: 628
parent_task: OTC-20260820-tibia-re-control-center-package-a
predecessor_repair_task: OTC-20260821-tibia-re-control-center-package-a-p1-isolation-6
fresh_isolation_authorized_by_owner: true
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
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: full_closeout
execution_mode: github_connector_plus_actions
execution_budget_minutes: 120
repair_cycles_for_current_gate: 3
validation_level: full
complete_user_facing_feature: false
owned_paths:
  - tools/tibia_re_control_center/execution.py
  - tools/tibia_re_control_center/fake.py
  - tools/tibia_re_control_center/recorder.py
  - tools/tibia_re_control_center/engine.py
  - tools/tibia_re_control_center/comparison.py
  - tools/tibia_re_control_center/artifact.py
  - tests/tools/tibia_re_control_center/test_isolation7_repairs.py
  - docs/agents/tasks/active/OTC-20260821-tibia-re-control-center-package-a-p1-isolation-7.md
  - docs/agents/tasks/archive/OTC-20260821-tibia-re-control-center-package-a-p1-isolation-7.md
---

# Package A P1 isolation 7

Fresh bounded repair task opened after independent exact-head review of PR #628 at `376660619f21b40cdc0dc8049835e7a5f6629875` against `main@5707af6c413cd9949f6c33b17744801cedef6eaf`.

## Exact findings

1. `PRRT_kwDOTVmdjs6bI0N5` — obtain final authority/capability as one guarded snapshot immediately before durable dispatch.
2. `PRRT_kwDOTVmdjs6bI0N6` — freeze every admitted JSON-serializable event sequence, including non-list Sequence implementations.
3. `PRRT_kwDOTVmdjs6bI0N-` — evaluate and latch abort conditions on every wait observation.
4. `PRRT_kwDOTVmdjs6bI0OC` — refuse Comparison PASS when required fields have zero checkpoint coverage.
5. `PRRT_kwDOTVmdjs6bI0OD` — validate requested status against Artifact v1 closed terminal status set.

## Authority

`runtime_access:none` permanently. No official-client process access, credentials, login, GUI/gameplay input, network listener, Track A mutation, transaction or unrelated refactor.

## Current action

One-shot isolation-seven repair driver is staged on the Package A branch. It will apply only the five bounded repairs, add focused deterministic regressions, run the full Package A suite plus both audits, Ruff and diff-check, remove itself, and push only after full PASS.

## Required gates

Focused deterministic regressions for all five findings; full Package A suite; both audits; Ruff; diff-check; exact-current-main; fresh independent exact-head review with zero P0/P1/material findings; Ready + squash merge only after all gates pass.

## Final repair-pass evidence

Isolation-seven pass 2 established 121/121 tests PASS, both Package A audits PASS, `RUNTIME_ACCESS_NONE=PASS`, fake one-step E2E PASS; it stopped only on Ruff B023/BLE001. Pass 3 fixes only those lint bindings while retaining the validated five-finding repair logic. Fresh exact-head independent review remains required after this commit.
