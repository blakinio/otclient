---
task_id: OTC-20260830-local-vision-agent-supervisor-discovery
status: investigating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: docs/OTC-20260830-local-vision-agent-supervisor-discovery
base_branch: main
base_main: 18ff83053f5c5d85c9bce6debab0f7fef6b79ecd
created: 2026-08-30T10:39:00+02:00
updated_at: 2026-08-30T10:39:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
implementation_authorized: false
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: high
decomposition_decision: discovery_first
decomposition_reason: owner requested an architecture that joins existing local supervisor, local vision/OCR, bounded GUI control, chat/dashboard and Track A runtime governance; implementation boundary must be approved before code
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
depends_on:
  - owner approval of the future autonomous GUI/operator architecture
blocks:
  - TRACK_A_AUTONOMOUS_VISION_GUI_RESEARCH
last_completed_step: inspected current trusted-main Track A contracts, local Ollama supervisor, local models, benchmark evidence, Docker/Hermes state and disabled CUA registration
current_blocker: ARCHITECTURE_NOT_YET_APPROVED
next_action: present 2-3 architecture approaches and obtain explicit owner approval before writing the formal design spec or implementing any runtime/input change
---

# Local vision-agent supervisor discovery

Discovery-only checkpoint for reusing the owner's existing local Ollama/supervisor stack as the foundation for a future Track A autonomous vision/OCR operator. This task grants no live-client observation, login, input, credentials, process control or gameplay authority.
