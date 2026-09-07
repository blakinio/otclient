---
task_id: OTC-20260907-zero-client-stage-diagnostics
status: implementing
agent: ChatGPT
session_id: zero-client-stage-diagnostics-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: recovery_observability
phase: implementation
branch: fix/OTC-20260907-zero-client-stage-diagnostics
base_branch: main
base_main: 0f342c9211a5b7214ed8fef8cea0f423115145ac
execution_mode: chatgpt
execution_class: repository_only
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
physical_e2e_required: false
credentials_allowed: none
parent_task: OTC-20260907-same-boot-recovery-diagnostics
depends_on:
  - OTC-20260907-same-boot-zero-client-diagnostic-live
owned_paths:
  - .github/scripts/track_a_kasm_zero_client_stage_diagnose.py
  - .github/workflows/track-a-kasm-zero-client-stage-diagnose.yml
  - tests/tools/tibia_runtime_bridge/test_kasm_zero_client_stage_diagnostic_contract.py
  - docs/agents/tasks/active/OTC-20260907-zero-client-stage-diagnostics.md
  - docs/agents/tasks/active/OTC-20260907-zero-client-stage-diagnostic-live.md
modules_touched:
  - Track A Kasm zero-client recovery observability
---

# OTC-20260907 — zero-client stage diagnostics

## Evidence

Merged diagnostic #976 ran once on trusted main `0f342c9211a5b7214ed8fef8cea0f423115145ac` as `34108176933 / 101697956345`. Admission and its diagnostic-only one-shot marker passed, canonical recovery lease generation `57` was acquired/validated, and the guarded read-only probe returned the sanitized worker error `command_failed:docker:126`. The lease was released. `CREDENTIAL_ACCESS=false` and `RUNTIME_MUTATION=false` were printed; no registration mutation, bootstrap, process control, auth or login occurred.

The approved Kasm bootstrap worker may execute Docker commands during six logical preflight stages: Docker inventory, display proof, package identity, boot identity, per-container candidate inventory and window inventory. Its generic `run()` error includes only command basename and return code, so `command_failed:docker:126` still does not identify the failing stage.

## Objective

Add one comprehensive stage-labeled read-only diagnostic around the unchanged approved worker. Run the same logical preflight sequence but label each fixed stage. For the all-running-container candidate loop, inspect every container read-only in one invocation and identify failures only by fixed role/ordinal (`target` or `non_target_N`) plus a strict sanitized worker code. Do not emit container names, command stderr, process content or untrusted strings.

## Acceptance

- PR-head is hosted/repository-only;
- production bootstrap/recovery workers remain unchanged;
- exact approved worker and central current-client fence are required;
- external canonical guard is proven held;
- diagnostic covers docker inventory, target resolution, display, package identity, boot identity, every candidate container and window inventory;
- all per-container candidate failures are collected in one diagnostic run where possible;
- output contains only fixed stage labels, integer counters and strict sanitized worker codes;
- no registration mutation, process launch/signal, bootstrap, credential access, auth, GUI input or recovery-marker reuse;
- live execution has a new task-local one-shot diagnostic marker and zero physical-action budget;
- deterministic contract, Track A governance, self-hosted boundary, actionlint and exact-head CI are green;
- after merge, run exactly once and use the stage evidence to select the actual recovery fix.
