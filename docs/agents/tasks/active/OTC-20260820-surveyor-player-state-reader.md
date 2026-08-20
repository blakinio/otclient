---
task_id: OTC-20260820-surveyor-player-state-reader
status: implementing
phase: implement
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: implementation
risk: medium
policy_version: 2
execution_mode: chat_github_and_hosted_ci
execution_reason: current-build static resolver, deterministic tests, then one separately admitted physical read-only differential E2E
decomposition_decision: phased
decomposition_reason: one cohesive typed-reader lifecycle with hosted implementation followed by serialized physical validation
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
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
base_main: 2a2b607bf11818cdd6bfc4377c932a170e4be2a9
branch: feat/OTC-20260820-surveyor-player-state-reader
implementation_pr: null
physical_e2e_required: true
owned_paths:
  - tools/tibia_re_surveyor/**
  - tests/tools/tibia_re_surveyor/**
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - docs/agents/evidence/OTC-20260820-surveyor-player-state-reader/**
  - docs/agents/tasks/active/OTC-20260820-surveyor-player-state-reader.md
  - docs/agents/tasks/archive/OTC-20260820-surveyor-player-state-reader.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
excluded_overlap:
  - PR #302 historical direct-position branch remains read-only evidence; do not edit its .github/scripts or task paths
  - PR #475 worldmap runtime remains unrelated and must not be controlled or mutated
anti_stall:
  started_at: 2026-08-20T15:51:00+02:00
  required_check_generation: 0
  terminal_ci_checks_for_current_generation: 0
  repair_cycles: 0
  unchanged_state_checks: 0
last_completed_step: freshly rediscovered current-build TPlayerData qt_metacast relocation/vtable and current playerPosition signed-i32 triplet offsets
next_action: implement a fail-closed current-build resolver and provisional read-only player-state typed reader with deterministic hosted tests
---

# Surveyor v2 P0 player-state typed reader

## Objective

Replace the proven Surveyor movement zero-delta gap with the first bounded typed reader without importing historical-build addresses. The reader must rediscover its exact-current-build structural anchors, remain fail-closed and read-only, integrate with collect-all without semantic overclaim, pass deterministic hosted validation and a fresh independent audit, merge, then receive one owner-controlled physical movement differential E2E.

## Fresh discovery facts

At task start current `main` was `2a2b607bf11818cdd6bfc4377c932a170e4be2a9`. The physical runtime was observed non-invasively as one exact current client (`52109920`, `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`) in `otclient-track-a-kasmvnc`, display `:1`, with one matching Tibia window. Registration state is deliberately `UNKNOWN`; bridge structural presence is not `IN_GAME` proof.

Fresh exact-binary static analysis independently recovered:

- `playerPosition` xref at `0x82d101` in a routine that reads signed DWORDs at object-relative `+0x78/+0x7c/+0x80`;
- `tibia::game::TPlayerData` qt-metacast routine at `0xd40470`;
- relocation at `0x30c1818 -> 0xd40470` inside the QObject vtable surface;
- current primary TPlayerData address point `0x30c1810`, with RTTI/typeinfo neighborhood resolving to `N5tibia4game11TPlayerDataE`.

These are current-build facts only. Historical #302 values remain evidence, not authority.

## Promotion boundary

Implementation may expose a typed current-build **candidate** observation but must not label it authoritative player XYZ until the post-merge owner-controlled movement differential proves the expected causal delta. No agent-generated input, login/logout, restart, process control, process-memory write, injection or local model is permitted.
