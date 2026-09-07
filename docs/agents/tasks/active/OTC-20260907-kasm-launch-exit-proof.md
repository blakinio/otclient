---
task_id: OTC-20260907-kasm-launch-exit-proof
status: implementing
agent: ChatGPT
session_id: kasm-launch-exit-proof-20260907
session_role: implementer
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: canonical_runtime_bootstrap_diagnostic
phase: implementation
branch: diag/OTC-20260907-kasm-launch-exit-proof
base_branch: main
base_main: 1b69a1f79ba5ab5bc63a73433670079276a6c7f8
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
physical_action_budget: 0
implementation_authorized: true
owned_paths:
  - .github/scripts/track_a_kasm_launch_exit_diagnose.py
  - .github/workflows/track-a-kasm-launch-exit-diagnostic.yml
  - tests/tools/tibia_runtime_bridge/test_kasm_launch_exit_diagnostic_contract.py
  - docs/agents/tasks/active/OTC-20260907-kasm-launch-exit-proof.md
  - docs/agents/tasks/active/OTC-20260907-kasm-launch-exit-diagnostic-live.md
modules_touched:
  - track_a_kasm_launch_exit_diagnostic
depends_on:
  - OTC-20260907-canonical-kasm-bootstrap-retry-v2-live
blocks:
  - OTC-20260906-native-login-physical-executor
---

# Canonical Kasm launch-exit proof mode

## Why proof mode changed

Trusted-main bootstrap attempts `34121830411` and `34124555199` both failed before registration despite a material launcher correction. The second attempt used the historically successful bin-root shape and completed `TRACK_A_KASM_BOOTSTRAP_ROLLBACK=PASS`. Immediate read-only Surveyor run `34124687615`, job `101750488697`, then proved `CANONICAL_REGISTRATION=ABSENT` and `TARGET_NAMESPACE_CLIENTS=0`.

A third bootstrap retry of the same shape is therefore prohibited. The next physical action must answer a narrower question: does the exact-current client process exit, stay alive without a window, or become window-ready, and what allowlisted startup-error class is observable if it exits?

## Diagnostic design

One owner-triggered trusted-main run may, under a fresh canonical lease and `guard-run`:

1. prove registration ABSENT and a canonical-Kasm zero-client/zero-window preflight;
2. launch exactly one plain exact-current client from the proven `bin/` working directory with no credentials, helpers, preload or lease variables;
3. persist only task-local PID/return-code/stdout/stderr scratch files;
4. observe for a bounded interval whether the exact process exits, remains alive without a Tibia window, or becomes window-ready;
5. emit only sanitized facts: outcome, numeric exit code when available, stdout/stderr nonempty booleans, and an allowlisted stderr class;
6. terminate only exact-current candidates created after the zero-state preflight when cleanup is required;
7. prove the same zero-client/zero-window canonical-Kasm state after cleanup.

Raw stdout/stderr, window titles, environment values, process memory, network payloads and credentials must not be retained or printed.

## Non-goals

This diagnostic does not write canonical registration, authenticate, select a character, enter gameplay, capture wire payloads, or mutate Track B.
