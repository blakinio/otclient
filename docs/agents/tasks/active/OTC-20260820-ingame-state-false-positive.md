---
task_id: OTC-20260820-ingame-state-false-positive
status: validating
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
track_id: official-client-re
task_kind: implementation
phase: validate
branch: fix/OTC-20260820-ingame-state-false-positive
base_branch: main
base_sha: 8620310a91c53e63abc0bf51fe40bdb8a3ee6cef
risk: high
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
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
owner_funded_ai_api_authorized: false
owned_paths:
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - .github/workflows/track-a-native-login.yml
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_kasm_existing_runtime_probe.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - tests/tools/tibia_re_surveyor/test_operator_semantics.py
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/operators/TRACK_A_SURVEYOR_V2_READONLY.md
  - docs/agents/operators/TRACK_A_NATIVE_LOGIN.md
  - docs/agents/tasks/archive/OTC-20260820-runtime-namespace-hardening.md
  - docs/agents/evidence/OTC-20260820-ingame-state-false-positive/**
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260820-ingame-state-false-positive.md
modules_touched:
  - tibia-re-surveyor
  - canonical-live-kasm-adoption-probe
  - canonical-live-transition
  - track-a-native-login
reuses:
  - tools/tibia_runtime_bridge/**
  - final Surveyor run 32362197404
  - current exact client PID/bridge identity evidence
policy_version: 2
execution_mode: local_git_plus_github
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
context_pressure: medium
context_growth: stable
context_score: 8
decomposition_decision: single
heavy_validation_runs: 1
repair_cycles: 0
current_blocker: none
next_action: freeze implementation head, run exact-head CI/governance and independent audit, merge, then perform trusted-main semantic downgrade plus read-only login-screen negative E2E
---

# Track A in-game state false-positive repair

Fresh read-only observation on 2026-08-20 proved a semantic contradiction: the official client was visibly at the login form while the exact-peer bridge still returned one validated `player_protocol_handler`, one `gameserver_game_session`, and one `worldmap_handler`. Therefore `BRIDGE_3_OF_3` proves structural object presence only and cannot by itself prove an active in-game session.

The final Surveyor artifact/run remains valid for collector execution, namespace identity, coverage, privacy and manifest integrity. Its `STRUCTURAL_IN_GAME=PASS` and `OWNER_LOGIN_REQUIRED=NO` fields are invalidated and must be superseded.