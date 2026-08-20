---
task_id: OTC-20260820-surveyor-unrelated-container-timeout
status: ready
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
task_kind: bugfix
phase: closeout
branch: fix/OTC-20260820-surveyor-unrelated-container-timeout
base_branch: main
base_sha: 29f466b32192641f53ef691759e6589a6a185bd5
risk: low
owned_paths:
  - tools/tibia_re_surveyor/runtime.py
  - tests/tools/tibia_re_surveyor/test_runtime.py
  - docs/agents/tasks/active/OTC-20260820-surveyor-unrelated-container-timeout.md
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
related_physical_run: 32348184547
current_blocker: none
next_action: revalidate this checkpoint-only delta, require fresh exact-head CI/governance, then squash-merge PR #620 and rerun physical snapshot 32348184547 scenario from trusted main
---

# Surveyor unrelated-container timeout repair

Physical read-only run `32348184547` proved the exact target and `BRIDGE_3_OF_3`, then failed because `_candidate_containers()` treated a five-second `pgrep` timeout in unrelated `freqtrade-portal-staging` as fatal. This repository-only repair must skip probe failures for unrelated containers only. Failure to inventory the designated Tibia target remains fatal/fail-closed.


## Validation checkpoint

```yaml
checkpoint_version: 2
status: ready
phase: closeout
pr: 620
audited_implementation_head: c510eda342bc9b871ed6d2878cfcf5f5914686ca
triggering_live_run: 32348184547
triggering_live_evidence:
  exact_client_candidates: 1
  target_exact_clients: 1
  target_window_matches: 1
  target_uniqueness_operator_preflight: PROVEN
  canonical_registration: PRESENT
  canonical_lease_generation: 17
  registration_lease_generation: 17
  structural_state_result: PASS_BRIDGE_3_OF_3
  owner_login_required: NO
  collector_failure: unrelated freqtrade-portal-staging pgrep timeout
focused_validation:
  compileall: PASS
  unittest_discover: 21_PASS
  diff_check: PASS
exact_head_validation_on_audited_implementation:
  ci_run: 32349013859
  ci_result: SUCCESS
  track_a_governance_run: 32349013586
  track_a_governance_result: SUCCESS
independent_audit:
  review: 4980681187
  validator: local Ollama qwen3.5:9b
  prompt_eval_count: 4180
  result: PASS
  material_findings_open: 0
safety_semantics:
  unrelated_probe_failure: SKIP_AND_INCREMENT_UNRESOLVED
  unresolved_probe_allows_uniqueness_proven: false
  target_probe_failure: HARD_FAIL
  runtime_authority_change: false
blockers:
  - checkpoint-only delta requires narrow revalidation and fresh exact-head CI/governance
next_action: revalidate this delta, then merge #620 if exact-head gates remain green and rerun the same trusted read-only physical operator
```
