---
task_id: OTC-20260906-be4f48-live-state-binding
status: active
agent: ChatGPT
session_id: be4f48-live-state-binding-20260906
session_role: implementer
project_lane: otclient
lane: RUNTIME-P1-BRIDGE
track_id: official-client-re
task_kind: implementation
phase: test_first
branch: runtime/OTC-20260906-be4f48-live-state-binding
base_branch: main
created: 2026-09-06T16:53:00+02:00
updated_at: 2026-09-06T16:53:00+02:00
base_main: 8e92188be2fc1ea33cc17a4a53acf36c4e4a4f56
policy_version: 2
prompting_standard_version: 2.1
execution_mode: chatgpt
execution_reason: repository-only exact-current bridge profile and causal live-state reader repair before physical native-login execution
execution_class: github_hosted
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
persistent_session_role: none
physical_e2e_required: false
implementation_authorized: true
feature_scope: be4f48_live_state_binding
run_scope: bounded_repository_repair
continuation_policy: continue_until_real_stop
task_completion_policy: merge_then_parent_physical_qualification
parent_task: OTC-20260905-control-center-native-login-start
owned_paths:
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.be4f48.json
  - .github/scripts/track_a_game_window_state_qualification.py
  - tests/tools/tibia_runtime_bridge/test_be4f48_live_state_binding.py
  - docs/agents/tasks/active/OTC-20260906-be4f48-live-state-binding.md
modules_touched:
  - Track A native runtime bridge
reuses:
  - tools/tibia_runtime_bridge/game_window_state_rebind.py
  - tools/tibia_runtime_bridge/current_sha_native_login_gate.py
  - exact-current rebind run 34024784802
  - current-client fence contract
depends_on: []
blocks: []
---

# OTC-20260906 — be4f48 live-state binding

## Objective

Remove the historical `15.32.75d4a0` fence and hard-coded `gameWindowState` backing offset from the read-only live qualification reader before the parent native-login physical E2E.

The repaired reader must derive the `TGameWindowController` primary vptr and `gameWindowState` backing member from the exact-current static analyzer after independently enforcing the current-client fence. Add an exact-current runtime-bridge profile from already-proven be4f48 RTTI bindings so a replacement client can expose the bounded helper surfaces required by the parent executor.

## Authority

Repository-only. No Official Tibia process/container/window/session observation or mutation, no credential access, no login, no process-memory access and no physical action are authorized by this child task.

## Acceptance

1. A `15.32.be4f48` bridge profile is exact-SHA-fenced and contains only current proven RTTI primary-vptr targets.
2. The live `gameWindowState` reader no longer trusts the historical anchor fence or a hard-coded member offset.
3. Reader binding is derived by `analyze_game_window_state()` from the exact executable and validates the returned 24-byte QString backing member.
4. Existing privacy/read-only output invariants remain unchanged.
5. Focused tests and Track A governance pass before merge.
