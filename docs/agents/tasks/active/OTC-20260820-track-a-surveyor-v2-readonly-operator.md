---
task_id: OTC-20260820-track-a-surveyor-v2-readonly-operator
status: ready
agent: ChatGPT
project_lane: otclient
lane: RUNTIME
task_kind: runtime_operator_implementation
phase: closeout
branch: ci/OTC-20260820-track-a-surveyor-v2-readonly-operator
base_branch: main
base_sha: 0447763982ef5db9efca652396cfac22e5a0cff4
risk: medium
owned_paths:
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - docs/agents/operators/TRACK_A_SURVEYOR_V2_READONLY.md
  - docs/agents/tasks/active/OTC-20260820-track-a-surveyor-v2-readonly-operator.md
  - docs/agents/tasks/archive/OTC-20260820-track-a-surveyor-v2-readonly-operator.md
modules_touched:
  - track-a-runtime-operator
reuses:
  - tools/tibia_re_surveyor/**
  - .github/workflows/track-a-native-login.yml peer-verification pattern
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
track_a_runtime_agent_admission_version: 1
execution_class: github_repository_implementation
runtime_access: none
persistent_session_role: none
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
current_blocker: none
next_action: revalidate this checkpoint-only delta with fresh exact-head CI/governance, then mark PR #618 ready and squash-merge if all gates remain green
---

# Surveyor v2 read-only physical operator

This task implements the operator only. It has `runtime_access:none` and MUST NOT dispatch or observe the physical client before the workflow is independently reviewed and merged to trusted `main`.

Acceptance:
- workflow_dispatch only, actor `blakinio`, explicit `ONE_SHOT_SURVEYOR_READ_ONLY` authorization string;
- runs only on `[otclient, synology]`;
- `permissions: contents: read` and no Secrets/env credential ingress;
- no login, input, signal, process control, injection, process-memory write, network mutation or transaction;
- fresh all-container exact-client census and target X11/PID proof before Surveyor execution;
- current native-helper bridge, when present, is accepted only after `SO_PEERCRED == exact client PID`; its three DISCOVER calls are read-only and state is `UNKNOWN` if helper cannot be proven;
- collect-all output privacy scan must PASS before artifact upload;
- output states explicitly distinguish `COLLECTOR_READY`, `STRUCTURAL_IN_GAME`, and `OWNER_LOGIN_REQUIRED`; unknown state never triggers a login request;
- physical dispatch belongs to the resumed/current runtime task, not this implementation task.


## Validation checkpoint

```yaml
checkpoint_version: 2
status: ready
phase: closeout
audited_workflow_head: e291c879a441b49dd26da94880da280cd0ec8d40
final_precheckpoint_head: 4b8591cacf54d0e10a454b064e9afd9f7d634162
pr: 618
runtime_access: none
workflow_dispatched: false
validation:
  yaml_parse: PASS
  diff_check: PASS
  actionlint_initial: FAIL_SC2016_SUMMARY_CONSTANT_QUOTING
  actionlint_fix: PASS_VIA_EXACT_HEAD_CI
  ci_run: 32347624928
  ci_result: SUCCESS
  track_a_governance_run: 32347624634
  track_a_governance_result: SUCCESS
independent_audit:
  review: 4980489547
  result: PASS
  material_findings_open: 0
final_delta_revalidation:
  review: 4980497129
  result: PASS
  material_findings_open: 0
authority:
  credentials_allowed: false
  login_allowed: false
  gui_input_authorized: false
  process_control_authorized: false
  mutation_authorized: false
runtime_e2e: NOT_APPLICABLE
runtime_e2e_reason: this PR implements the trusted operator only and intentionally does not dispatch the physical workflow before merge
next_action: exact-head CI/governance on this checkpoint-only head, then mark ready and squash-merge if green
```
