---
task_id: OTC-20260820-track-a-surveyor-v2
status: validating
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: research_infrastructure
phase: closeout
branch: feat/OTC-20260820-track-a-surveyor-v2
base_branch: main
base_sha: c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd
created: 2026-08-20T08:49:00+02:00
updated: 2026-08-20T09:55:00+02:00
risk: medium
related_pr: "616"
owned_paths:
  - tools/tibia_re_surveyor/**
  - tests/tools/tibia_re_surveyor/**
  - docs/agents/tasks/active/OTC-20260820-track-a-surveyor-v2.md
  - docs/agents/tasks/archive/OTC-20260820-track-a-surveyor-v2.md
  - docs/agents/evidence/OTC-20260820-track-a-surveyor-v2/**
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - tibia-re-surveyor
reuses:
  - PR #592 TIBIA-RE Surveyor v1 exact implementation blobs
  - tools/tibia_runtime_bridge/**
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
  - docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md
  - docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md
depends_on: []
blocks: []
cross_repository_task_ids: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
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
invocation_started_at: 2026-08-20T08:49:00+02:00
last_progress_at: 2026-08-20T09:55:00+02:00
current_blocker: none
next_action: commit this audit/validation checkpoint, revalidate its checkpoint-only delta, then require fresh exact-head CI/governance before readiness and squash merge
---

# TIBIA-RE Surveyor v2 implementation

## Objective

Create the canonical repository-side Surveyor v2 implementation from current `main`, reusing the exact Surveyor v1 implementation from PR #592 rather than duplicating it, and add deterministic passive collect-all output for all twelve TIBIA-RE aliases.

This implementation task has `runtime_access:none`. It does not touch the physical official client. A later separately admitted runtime-validation task may consume the merged implementation for the first live collect-all run.

## Acceptance criteria

- Import/reuse the functional Surveyor v1 foundation from #592 on current main.
- Preserve canonical 169-row coverage parsing and fail-closed no-promotion semantics.
- Emit deterministic per-alias views for all twelve aliases.
- Emit `missing-readers.json` ranked from actual missing/unavailable evidence surfaces and canonical dependency priority.
- Emit `summary.md` plus `manifest.sha256` over generated output.
- Preserve exact runtime/build/admission provenance when runtime input is available.
- Treat unavailable/incompatible bridge readers as UNKNOWN/UNAVAILABLE rather than using historical offsets or ad-hoc injection.
- Keep collector runtime behavior passive/read-only; no login, input, process control, process-memory write, network mutation or transactions.
- Add focused tests for alias completeness, deterministic output, missing-reader ranking, provenance/guardrails and path safety.
- Update `MODULE_CATALOG.md` and `CHANGELOG.md` because this introduces reusable research tooling.
- Obtain fresh independent audit, exact-head CI/governance and terminal PR/task closeout before claiming completion.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-20T08:49:00+02:00
head: c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd
branch: feat/OTC-20260820-track-a-surveyor-v2
pr: none
status: implementing
phase: implement
runtime_access: none
proven:
  - current main is c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd at task creation
  - PR #592 remains open Draft at 90fb32f69173a6e621dfe6bd34c6f2e494076655 and is 19 commits behind current main
  - #592 exact head CI and Track A agent governance were green but it has no independent review
  - Spark local edits from the prior session were not pushed to GitHub and are unavailable as durable source state
unknown:
  - first future live-runtime availability and exact current physical admission
conflicts: []
validation:
  - command: none yet
    result: NOT_RUN
    evidence: implementation not yet imported
blockers: []
next_action: import #592 code/test blobs onto this current-main branch and implement the v2 collect-all layer
```

## Final implementation validation checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-20T09:55:00+02:00
audited_implementation_head: d103238b45aa5feb90ae7914d1e83dbd8e44d0b8
branch: feat/OTC-20260820-track-a-surveyor-v2
pr: 616
status: validating
phase: closeout
runtime_access: none
implementation_result:
  canonical_rows: 169
  alias_views: 12
  subsystem_telemetry_documents: 11
  missing_typed_readers: 11
  current_bridge_profile_state: NO_EXACT_CURRENT_PROFILE
  collector_has_input_path: false
  full_process_environment_read: false
  semantic_promotion_allowed: false
focused_validation:
  compileall: PASS
  unittest_discover: 17_PASS
  repository_only_collect_all: PASS
  privacy_scan: PASS
  manifest_present: true
  diff_check: PASS
exact_head_validation_on_audited_implementation:
  ci_run: 32344898863
  ci_result: SUCCESS
  track_a_agent_governance_run: 32344898266
  track_a_agent_governance_result: SUCCESS
  track_a_canonical_live_governance_run: 32344898169
  track_a_canonical_live_governance_result: SUCCESS
independent_audit:
  review_id: 4980263059
  validator: local Ollama qwen3.5:9b on Molehill-PC
  num_ctx: 65536
  prompt_eval_count: 46738
  result: PASS
  material_findings_open: 0
self_review_dispositions:
  - stale PR #592 keepalive/input prototype intentionally removed; current task has no owner authorization for anti-idle mutation
  - runtime probe no longer reads complete /proc/PID/environ merely to discover DISPLAY
  - bridge profile compatibility is dynamically censused and fails closed when no exact current SHA profile exists
  - raw character-bearing window titles are not retained in v2 output
runtime_e2e: NOT_APPLICABLE
runtime_e2e_reason: repository implementation task has runtime_access:none; the first physical collect-all is a separate admitted runtime-validation task after trusted-base merge
blockers:
  - this checkpoint changes only the task record after the independent implementation audit and therefore needs narrow delta revalidation plus fresh exact-head CI/governance
next_action: narrow-audit this checkpoint-only delta, then verify fresh exact-head CI/governance and merge PR #616 if all gates remain green
```
