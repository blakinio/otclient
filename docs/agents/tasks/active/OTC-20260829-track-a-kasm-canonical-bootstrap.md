---
task_id: OTC-20260829-track-a-kasm-canonical-bootstrap
status: implementing
agent: ChatGPT
session_role: implementer
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: infrastructure
phase: implementation_prior_boot_invalidation
branch: feat/OTC-20260829-track-a-kasm-canonical-bootstrap-v2
base_branch: main
base_main: 08c31195fd2f44224badf1b6bdff85192495898b
created: 2026-08-29T17:34:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
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
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
physical_e2e_required: false
implementation_authorized: true
owned_paths:
  - .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py
  - .github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/test_tibia_official_client_re_canonical_live_transition.py
  - .github/scripts/test_track_a_kasm_canonical_bootstrap_workflow.py
  - .github/scripts/test_track_a_agent_runtime_governance.py
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - .github/workflows/track-a-kasm-canonical-bootstrap.yml
  - docs/agents/tasks/active/OTC-20260829-track-a-kasm-canonical-bootstrap.md
  - docs/agents/evidence/OTC-20260829-track-a-kasm-canonical-bootstrap/**
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/superpowers/plans/2026-08-29-track-a-kasm-canonical-bootstrap.md
modules_touched:
  - track-a-canonical-live-runtime
  - track-a-kasm-runtime-access
reuses:
  - PR #799 owner-approved Kasm bootstrap design
  - PR #798 reusable self-hosted boundary audit
  - PR #796 current V4 trusted-main/self-hosted admission hardening
  - .github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py
  - .github/scripts/tibia-official-client-re-canonical-live-transition.py
  - .github/scripts/tibia-official-client-re-canonical-live-guard.py
depends_on:
  - docs/superpowers/specs/2026-08-29-track-a-kasm-canonical-bootstrap-design.md
blocks:
  - LIVE_GAME_WINDOW_STATE_CAUSAL_VALIDATION
current_blocker: PRIOR_BOOT_REGISTRATION_PRESENT_ZERO_CLIENT
next_action: TDD the approved metadata-only boot-epoch-registration-invalidate addendum, then resume the guarded two-phase live workflow
---

# Track A Kasm canonical bootstrap implementation

Repository-only implementation of the owner-approved KasmVNC-aware `create_new` canonical bootstrap. This task cannot execute, start, stop, signal, inspect process memory, authenticate, or otherwise mutate the official client runtime. Physical execution requires a separate trusted-main RUNTIME task after this implementation is merged and closed.
