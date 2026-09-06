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
phase: validation
branch: runtime/OTC-20260906-be4f48-live-state-binding
base_branch: main
created: 2026-09-06T16:53:00+02:00
updated_at: 2026-09-06T17:18:00+02:00
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
  - .github/scripts/test_track_a_game_window_state_qualification.py
  - .github/scripts/test_track_a_game_window_state_workflow_contract.py
  - .github/workflows/track-a-game-window-state-qualification.yml
  - tests/tools/tibia_runtime_bridge/test_native_login_be4f48_bindings.py
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

The repaired reader derives the `TGameWindowController` primary vptr and `gameWindowState` backing member from the exact-current static analyzer after independently enforcing the current-client fence. The exact-current runtime-bridge profile is built only from already-proven be4f48 RTTI bindings so a replacement client can expose the bounded helper surfaces required by the parent executor.

## Authority

Repository-only. No Official Tibia process/container/window/session observation or mutation, no credential access, no login, no process-memory access and no physical action are authorized by this child task.

## Validation checkpoint

- TDD RED: exact-current rebind run `34041089509`, job `101507853478`, failed at the new contract before implementation.
- Material implementation head `0be62fba242a705271c113c4392308c4e77af07a`.
- Read-only gameWindowState contract: run `34041817089`, job `101509840902`, SUCCESS on material head.
- Exact-current be4f48 static rebind on material head: run `34041817100`, job `101509841008`, pending at this checkpoint after repository gate and public-package current fence passed.
- No live Synology qualification job ran from the PR; the physical job remained skipped by design.

## Acceptance

1. A `15.32.be4f48` bridge profile is exact-SHA-fenced and contains only current proven RTTI primary-vptr targets.
2. The live `gameWindowState` reader no longer trusts the historical anchor fence or a hard-coded member offset.
3. Reader binding is derived by `analyze_game_window_state()` from the exact executable and validates the returned 24-byte QString backing member.
4. The owner-gated read-only qualification workflow is current-fenced and carries the canonical manifest/provenance plus analyzer into its in-memory resolver bundle without `docker cp`.
5. Existing privacy/read-only output invariants remain unchanged.
6. Focused tests and Track A governance pass before merge.
