---
task_id: OTC-20260830-local-vision-agent-supervisor-discovery
status: waiting
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: discovery
phase: architecture_design
branch: docs/OTC-20260830-local-vision-agent-supervisor-discovery
base_branch: main
base_main: 18ff83053f5c5d85c9bce6debab0f7fef6b79ecd
created: 2026-08-30T10:39:00+02:00
updated_at: 2026-08-30T11:21:00+02:00
risk: high
execution_class: github_hosted
execution_mode: work
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
decomposition_reason: owner approved the architecture direction; the formal written spec is now committed and self-reviewed, but implementation planning remains blocked until the owner separately approves the written spec
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
owned_paths:
  - docs/agents/tasks/active/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/agents/reports/OTC-20260830-local-vision-agent-supervisor-discovery.md
  - docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md
modules_touched:
  - track-a-runtime-governance
  - local-model-supervisor
  - tibia-re-vision-benchmark
reuses:
  - PR #790 TIBIA-RE-VISION-BENCHMARK execution and Qwen3-VL evidence
  - PR #801 Kasm canonical bootstrap and prior-boot invalidation
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
  - existing local supervisor under C:/Users/barte/Documents/ChatGPT/llm/supervisor
  - existing local_worker MCP server registered in the local Codex configuration
  - .github/scripts/tibia-official-client-re-control-center-bridge-transport.py
  - .github/scripts/tibia-official-client-re-input-lock.py
  - .github/scripts/track_a_game_window_state_qualification.py
  - .github/scripts/track_a_current_world_entered_anchor.py
  - .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh
depends_on:
  - explicit owner approval of docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md
blocks:
  - TRACK_A_AUTONOMOUS_VISION_GUI_RESEARCH
last_completed_step: owner approved Approach C; formal design spec docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md was committed and self-reviewed for placeholders, consistency, scope and authority boundaries with no material defect found
current_blocker: OWNER_WRITTEN_SPEC_APPROVAL_REQUIRED
next_action: owner reviews and explicitly approves or requests changes to docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md; only after written-spec approval invoke the repository planning workflow
---

# Local vision-agent supervisor discovery

Architecture direction `Approach C` is owner-approved. The formal written design is now:

`docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`

The task is intentionally waiting at the second architectural gate: written-spec owner approval. This task still grants no live-client observation, credentials, login, character selection, GUI input, process control, process-memory access or gameplay authority, and it does not authorize implementation planning yet.