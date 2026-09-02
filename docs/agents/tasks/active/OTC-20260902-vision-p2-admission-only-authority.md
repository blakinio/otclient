---
task_id: OTC-20260902-vision-p2-admission-only-authority
status: validating
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
updated_at: 2026-09-02T16:54:26+02:00
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
red_head: 41b3188ed0dd584389ca6f13e6b7583a948b95c5
implementation_head: c06f323f825935eca9887957cecaeb6e086e1818
owned_paths:
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - docs/agents/tasks/active/OTC-20260902-vision-p2-admission-only-authority.md
  - .github/workflows/tibia-re-control-center-core.yml
current_blocker: exact_head_ci_pending
next_action: commit and push the one-time Package A boundary plus final checkpoint, open a Draft PR, and require fully terminal exact-head CI before coordinator classification
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
## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T14:54:26Z
head: c06f323f825935eca9887957cecaeb6e086e1818
branch: fix/OTC-20260902-vision-p2-admission-only-authority
pr: null
status: validating
context_routes:
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - docs/agents/evidence/OTC-20260902-vision-p2-e2e-audit/real-edge-transport-e2e.md
owned_paths:
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - docs/agents/tasks/active/OTC-20260902-vision-p2-admission-only-authority.md
  - .github/workflows/tibia-re-control-center-core.yml
proven:
  - live Wave 3 transport E2E passes but zero-contract admission-only authority fails EDGE_RUNTIME_COMPOSITION_MISMATCH
  - trusted base is main 27f9bdd5f003c596529e7571343ae8bb053d5cff
  - TDD RED 41b3188ed0dd584389ca6f13e6b7583a948b95c5 fails at _issue_read_only_runtime_authority on the default composition
  - GREEN c06f323f825935eca9887957cecaeb6e086e1818 changes only authority-registry composition matching plus focused tests
  - admission-only mode requires configuration None exact RuntimeSignalResolver zero contracts and exact current binding
  - nonempty resolver without composition configuration remains rejected as EDGE_RUNTIME_COMPOSITION_MISMATCH
  - configured nonempty runtime path retains signature clock max-age and binding checks
  - focused new guard tests pass 2 of 2
  - bridge runtime-signal session reconciliation trusted-composition matrix passes 107 of 107
  - vision capture evidence Ollama foundation tests pass 19 of 19
  - py_compile Ruff I/F and git diff check pass
  - Package A exact boundary accepts only this task on exact branch base repo; wrong branch base and fork reject it
  - direct Codex usage remains zero and runtime_access remains none
derived:
  - the smallest safe repair is allowing an empty resolver only when no semantic configuration exists
  - no daemon runtime producer transport model capture or reconciliation behavior needs modification
unknown:
  - exact-head GitHub Actions result
  - fresh post-promotion live reconcile_vision result
conflicts:
  - none
first_failure:
  marker: default composition rejected admission-only zero-contract authority
  evidence: RED 41b3188ed reproduces EDGE_RUNTIME_COMPOSITION_MISMATCH
rejected_hypotheses:
  - accept arbitrary resolver when configuration is absent: rejected; nonempty resolver remains fail-closed
  - require a fixture reviewed contract for visual-only mode: rejected as fake authority
changed_paths:
  - tools/tibia_re_control_center/agent_edge_bridge.py
  - tests/tools/tibia_re_control_center/test_vision_p2_trusted_composition.py
  - docs/agents/tasks/active/OTC-20260902-vision-p2-admission-only-authority.md
  - .github/workflows/tibia-re-control-center-core.yml
validation:
  - command: focused admission-only and nonempty-resolver guards
    result: PASS
    evidence: 2 tests OK
  - command: bridge runtime-signal session reconciliation trusted-composition matrix
    result: PASS
    evidence: 107 tests OK
  - command: vision foundation capture evidence Ollama
    result: PASS
    evidence: 19 tests OK
  - command: py_compile Ruff I/F git diff check
    result: PASS
    evidence: all returned zero after import cleanup
  - command: Package A positive and negative boundary simulation
    result: PASS
    evidence: exact unexpected list empty; wrong branch wrong base fork each reject exact task
blockers:
  - exact-head GitHub Actions not yet run
next_action: commit and push the boundary plus checkpoint, open Draft PR, and require terminal exact-head CI before coordinator classification
```
