---
task_id: OTC-20260902-vision-p2-qwen-schema-repair
status: implementing
agent: ChatGPT
session_role: implementer
worker_alias: OTC-VISION-P2-QWEN-SCHEMA-REPAIR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: bugfix
phase: wave_3_finding_repair
branch: fix/OTC-20260902-vision-p2-qwen-schema-contract
base_branch: main
base_main: c16d180d336ba8aa9e1656807c79a44e81c15c66
created: 2026-09-02T14:44:00+02:00
updated_at: 2026-09-02T14:44:00+02:00
risk: medium
execution_class: repository_only
execution_mode: chat
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
implementation_authorized: true
mutation_authorized: false
credentials_allowed: false
login_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
owner_funded_ai_api_authorized: false
owned_paths:
  - tools/tibia_re_control_center/agent_vision.py
  - tests/tools/tibia_re_control_center/test_agent_vision.py
  - docs/agents/tasks/active/OTC-20260902-vision-p2-qwen-schema-repair.md
  - docs/agents/reports/OTC-20260902-vision-p2-qwen-schema-repair.md
  - docs/agents/evidence/OTC-20260902-vision-p2-qwen-schema-repair/**
current_blocker: production_prompt_does_not_declare_exact_model_observation_schema
next_action: commit causal TDD RED then minimally tighten the static production prompt without changing validator model digest profile or authority semantics
---

# Objective

Repair the Wave 3 live finding from PR #857: the exact Qwen model receives a valid byte-bound secret-safe capture but the production static prompt is too underspecified, so the model returns JSON that fails `validate_model_observation`.

# Frozen repair design

Change only the static production vision prompt so it explicitly requires exactly the six model-observation keys, exact screen-class enum, correct array types, no additional keys and no markdown. Keep the existing strict validator unchanged. Do not add fallback parsing, schema coercion, alternate models, prompt injection channels, authority fields or runtime behavior.

# Acceptance

1. TDD RED fails because the current prompt omits the exact schema contract.
2. Minimal GREEN changes only `agent_vision.py` prompt text plus the focused test.
3. Existing strict evidence/schema validation remains unchanged.
4. Focused AgentVision tests pass except any independently reproduced clean-main baseline limitation, which must remain explicitly classified rather than hidden.
5. Frozen vision benchmark/security tests and repository checks remain green.
6. No runtime observation, credentials, login, GUI input, process control, mutation, physical action or Codex invocation occurs in this repair task.
