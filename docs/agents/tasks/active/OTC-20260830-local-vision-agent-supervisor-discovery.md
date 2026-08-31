---
task_id: OTC-20260830-local-vision-agent-supervisor-discovery
status: waiting
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: discovery
phase: implementation_planning
branch: docs/OTC-20260830-local-vision-agent-supervisor-discovery
base_branch: main
base_main: 18ff83053f5c5d85c9bce6debab0f7fef6b79ecd
created: 2026-08-30T10:39:00+02:00
updated_at: 2026-08-30T11:44:10+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
implementation_authorized: false
prompting_standard_version: 2.1
policy_version: 2
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: phased
decomposition_reason: owner approved the architecture direction and written spec; the repository implementation plan is now committed and self-reviewed, while actual implementation remains a separately selected/authorized execution phase
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
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
approved_architecture: approach_c
approved_spec: docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md
implementation_plan: docs/superpowers/plans/2026-08-30-local-track-a-vision-agent-supervisor.md
owned_paths:
  - docs/agents/tasks/active/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/reports/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md
  - docs/superpowers/plans/2026-08-30-local-track-a-vision-agent-supervisor.md
modules_touched:
  - track-a-runtime-governance
  - tibia-re-control-center
  - local-model-supervisor
  - tibia-re-vision-benchmark
reuses:
  - existing tools/tibia_re_control_center Package A/B/C/D foundation
  - PR #790 TIBIA-RE-VISION-BENCHMARK and Qwen3-VL evidence/Ollama safety primitives
  - PR #801 Kasm canonical bootstrap and prior-boot invalidation
  - .github/scripts/tibia-official-client-re-control-center-bridge-transport.py
  - .github/scripts/tibia-official-client-re-input-lock.py
  - .github/scripts/track_a_game_window_state_qualification.py
  - .github/scripts/track_a_current_world_entered_anchor.py
  - existing local supervisor and local_worker MCP on Molehill-PC
related_prs:
  - PR #808: current Draft architecture/planning checkpoint
  - PR #615: old bounded Ollama PoC; candidate invariants only, do not merge wholesale; terminally supersede only after merged replacement proves required coverage
depends_on:
  - explicit owner choice/authorization of repository-only implementation execution workflow
blocks:
  - TRACK_A_AUTONOMOUS_VISION_GUI_RESEARCH
last_completed_step: owner approved the written design; implementation plan docs/superpowers/plans/2026-08-30-local-track-a-vision-agent-supervisor.md was committed, refined after self-review, and now maps the approved design onto existing Control Center and PR #790 reuse without enabling any runtime/effect path
current_blocker: OWNER_IMPLEMENTATION_EXECUTION_AUTHORIZATION_REQUIRED
next_action: owner selects and authorizes one repository-only implementation workflow — Subagent-Driven (recommended) or Inline Execution — while preserving runtime_access:none and all physical/credential authorities false
---

# Local vision-agent supervisor discovery

Architecture direction `Approach C` and the written design are owner-approved.

Formal design:

`docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`

Implementation plan:

`docs/superpowers/plans/2026-08-30-local-track-a-vision-agent-supervisor.md`

Planning reconciliation found that the approved persistent control/session plane should extend the existing `tools/tibia_re_control_center` foundation rather than create another backend. The plan keeps the production action executor unbound and separates Molehill deployment, Synology transport, Track A read-only binding, credential brokerage and current-client physical actions into later authorization boundaries.

This task is intentionally waiting for implementation workflow selection. It still grants no live-client observation, credentials, login, character selection, GUI input, process control, process-memory access or gameplay authority.