---
task_id: OTC-20260828-canonical-current-client-fence
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: tdd_red
branch: fix/OTC-20260828-canonical-current-client-fence
base_branch: main
base_main: 785d888e8392e32c8ba852d6db7c8de03db9d8be
created: 2026-08-28T15:40:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
canonical_boot_epoch_recovery: NOT_APPLICABLE
canonical_recovery: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
physical_e2e_required: false
implementation_authorized: true
owned_paths:
  - .github/scripts/tibia-official-client-re-canonical-live-session.sh
  - .github/scripts/test_tibia_official_client_re_canonical_live_session.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/test_tibia_official_client_re-kasm-existing-runtime-probe.py
  - .github/scripts/test_track_a_canonical_current_client_fence.py
  - .github/workflows/track-a-canonical-current-client-fence.yml
  - .github/workflows/track-a-canonical-live-governance.yml
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260828-canonical-current-client-fence.md
modules_touched:
  - track-a-canonical-live-runtime
reuses:
  - trusted-main promotion #752 exact current client and field6 runtime-observation boundary
  - merged canonical lease/transition/session worker
  - merged existing-runtime adoption probe
  - merged exact-current observer evidence from #744/#745/#746
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
---

# Objective

Repair the trusted canonical-live and runtime-admission exact-client contract so it admits the already independently promoted current official Linux client `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a` instead of the superseded `ed5469... / 52109920` cut.

This task is repository-only. It must not bootstrap, execute, authenticate, observe, mutate or control any official client. A later runtime successor must use the merged result under fresh admission and whatever Gate A/rebind/Gate B requirements the chosen runtime-access class requires.

# Root-cause boundary

The stale fence is not isolated to one launcher. Trusted `main` binds the superseded cut in the canonical session worker, the canonical transition/Gate-B controller, the Kasm existing-runtime adoption probe, the mandatory Track A runtime-admission contract, normative Track A/ADR/bootstrap governance and the canonical-live governance audit. Updating only one consumer would create a split-brain canonical identity contract and is forbidden.

# Acceptance

1. Hosted RED proves current trusted main still binds the canonical worker/governance contract to the superseded client; the focused contract must also explicitly falsify the mandatory runtime-admission fence.
2. Update the canonical worker, transition controller, adoption probe, runtime-admission contract, governance fence and normative current-client references as one coherent exact-client contract; do not preserve two competing "current" fences.
3. Historical evidence may keep historical client hashes when explicitly historical; only current canonical authority is updated.
4. Existing canonical session/transition/lease/adoption tests remain GREEN.
5. Fresh exact-current promotion evidence on trusted main is referenced as provenance; no new client download/execution is needed for this repair.
6. Exact-head CI, Track A agent governance and canonical-live governance must pass.
7. Fresh post-implementation audit must find zero material issues before merge.
8. No runtime, credentials, login, process memory or packet access from this PR.

next_action: prove a focused hosted RED specifically against the stale mandatory runtime-admission fence, then perform one coherent repository-only exact-client replacement across all current authority consumers.
