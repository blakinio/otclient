---
task_id: OTC-20260902-vision-p2-admission-only-authority
status: implementing
agent: ChatGPT
session_role: implementer
worker_alias: OTC-VISION-P2-ADMISSION-ONLY-AUTHORITY-REPAIR
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: bugfix
phase: wave_3_finding_repair
branch: fix/OTC-20260902-vision-p2-admission-only-authority
base_branch: main
base_main: 27f9bdd5f003c596529e7571343ae8bb053d5cff
pr: null
created: 2026-09-02T16:47:00+02:00
updated_at: 2026-09-02T16:47:00+02:00
risk: medium
execution_class: repository_only
execution_mode: chat
execution_reason: bounded repair of the live Wave 3 admission-only composition finding
context_pressure: low
context_growth: stable
context_score: 3
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one authority-registry condition plus focused regression coverage
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
policy_version: 2
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
anti_idle_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
owner_funded_ai_api_authorized: false
owned_paths:
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - docs/agents/tasks/active/OTC-20260902-vision-p2-admission-only-authority.md
current_blocker: tdd_red_not_yet_recorded
next_action: add focused RED proving default composition rejects the required admission-only zero-contract mode
---

# Objective

Repair the real Wave 3 finding without expanding Phase 2: a freshly admitted read-only edge must be able to become current when no semantic runtime producer is configured. In that admission-only mode the resolver must contain zero reviewed contracts and no semantic runtime evidence may become current.

# Frozen design

- Preserve the existing one-shot composition-issued authority receipt and all exact task/run/runtime/client admission checks.
- When a nonempty reviewed runtime configuration is supplied, preserve the existing exact configuration/resolver signature checks unchanged.
- When no reviewed runtime configuration is supplied, admit only a typed `RuntimeSignalResolver` whose contract registry is empty.
- Do not allow an empty-mode resolver containing any contract, reviewed source, semantic evidence, fallback rule or caller-selected authority.
- Do not change transport, capture, Qwen, reconciliation rules, action authority or physical budget.

# Acceptance

1. TDD RED reproduces `EDGE_RUNTIME_COMPOSITION_MISMATCH` on default composition with exact read-only admission and a zero-contract resolver.
2. Minimal GREEN allows that exact admission-only mode.
3. The resulting edge may become current after heartbeat/observation while runtime status remains `UNKNOWN/current=false`.
4. Binding any reviewed source in admission-only mode fails because no contracts exist.
5. Existing configured reviewed-runtime behavior and all stale/forged/substitution protections remain green.
6. No runtime observation or physical action occurs in the repair task; Codex usage remains zero.
