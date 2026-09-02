---
task_id: OTC-20260902-vision-p2-qwen-schema-repair
status: waiting
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
pr: 859
created: 2026-09-02T14:44:00+02:00
updated_at: 2026-09-02T15:03:00+02:00
risk: medium
execution_class: repository_only
execution_mode: chat
execution_reason: bounded prompt-contract repair from a live Wave 3 finding; no official-client observation or owner-funded AI is needed for implementation
context_pressure: low
context_growth: stable
context_score: 3
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one prompt/schema bug with one production constant and one focused regression test
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
red_head: c4c21863dbd36f602e413ae108bd337b02cf8631
implementation_head: 5e0cd8c44ed136f6aca5ceaa458de2ee2dc39926
ci_boundary_head: 8e4ef537816e25db58b0c2d942c317f527b380da
repair_cycles_for_current_gate: 1
current_blocker: exact_head_ci_after_one_time_package_a_boundary_repair
next_action: publish the one-time Package A repair plus final checkpoint and require fully terminal exact-head CI before classification
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

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T13:03:00Z
head: 8e4ef537816e25db58b0c2d942c317f527b380da
branch: fix/OTC-20260902-vision-p2-qwen-schema-contract
pr: 859
status: waiting
context_routes:
  - tools/tibia_re_control_center/agent_vision.py
  - tools/tibia_re_vision/evidence.py
  - tests/tools/tibia_re_control_center/test_agent_vision.py
  - docs/agents/evidence/OTC-20260902-vision-p2-e2e-audit/live-qwen-schema-finding.md
owned_paths:
  - tools/tibia_re_control_center/agent_vision.py
  - tests/tools/tibia_re_control_center/test_agent_vision.py
  - docs/agents/tasks/active/OTC-20260902-vision-p2-qwen-schema-repair.md
  - .github/workflows/tibia-re-control-center-core.yml
proven:
  - Wave 3 live audit head 53df76bfa7f33926b388a4a3158df7ede2c47fbb records a real exact-Qwen failure because model observation JSON did not satisfy the strict six-field schema
  - repair trusted base is main c16d180d336ba8aa9e1656807c79a44e81c15c66
  - TDD RED c4c21863dbd36f602e413ae108bd337b02cf8631 fails specifically because the static prompt lacks quoted screen_class and the rest of the exact schema contract
  - GREEN 5e0cd8c44ed136f6aca5ceaa458de2ee2dc39926 changes only the static production prompt and leaves validator model digest profile scheduler and authority semantics unchanged
  - focused prompt provenance and endpoint contract tests pass 4 of 4
  - strict-output and schema-retry tests pass 2 of 2
  - AgentVision suite excluding the one previously clean-main reproduced Windows baseline method passes 56 of 56
  - frozen vision benchmark passes 34 of 34 and py_compile Ruff I/F plus git diff check pass
  - direct Codex worker or reviewer invocations remain zero and runtime_access remains none
  - first exact-head GitHub Package A falsification audit on 0d9f0d429918733a1976e48382164aedc845bbc8 failed only at declared path boundary for the mandatory repair task record; code and test paths were accepted
  - one-time boundary repair 8e4ef537816e25db58b0c2d942c317f527b380da admits only the exact repair task on exact branch base and head repo; exact simulation passes while wrong branch fork and wrong base all fail

derived:
  - the smallest repair is prompt-side schema specification rather than parser fallback or validator relaxation
  - a new live Qwen inference belongs to the fresh Wave 3 audit after this repair is promoted, not to this repository-only implementer
unknown:
  - exact-head GitHub Actions result after one-time Package A boundary repair
  - fresh post-promotion Wave 3 live Qwen result
conflicts:
  - none
first_failure:
  marker: production Qwen observation rejected by strict schema on the real full-masked physical capture
  evidence: PR 857 durable finding records seven model-observation validation errors with exact model/digest and empty residency restored afterward
rejected_hypotheses:
  - strict validator is too narrow: rejected because the frozen schema is intentional authority/provenance protection and must remain unchanged
  - model or digest must change: rejected because live admission proved the exact required model and digest before the schema failure
  - fallback coercion should repair malformed output: rejected because it would weaken fail-closed model-output handling
changed_paths:
  - .github/workflows/tibia-re-control-center-core.yml
  - tools/tibia_re_control_center/agent_vision.py
  - tests/tools/tibia_re_control_center/test_agent_vision.py
  - docs/agents/tasks/active/OTC-20260902-vision-p2-qwen-schema-repair.md
validation:
  - command: focused static prompt schema test
    result: PASS
    evidence: exact six keys enum array types no-extra-keys and no-markdown contract is present
  - command: filtered AgentVision suite excluding one pre-proven clean-main Windows baseline method
    result: PASS
    evidence: 56 tests OK
  - command: frozen vision benchmark
    result: PASS
    evidence: 34 tests OK
  - command: py_compile Ruff I/F and git diff check
    result: PASS
    evidence: all returned zero
  - command: exact Package A boundary logic with frozen changed paths
    result: PASS
    evidence: exact branch repo and base returns zero while wrong branch fork and wrong base each return nonzero
blockers:
  - final exact-head GitHub Actions after the one-time Package A boundary repair are pending
next_action: push the checkpoint head and require terminal exact-head CI before coordinator classification and Wave 3 restack
```
