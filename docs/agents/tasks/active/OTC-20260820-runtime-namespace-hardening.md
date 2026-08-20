---
task_id: OTC-20260820-runtime-namespace-hardening
status: validating
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: implementation
phase: validate
branch: fix/OTC-20260820-runtime-namespace-hardening
base_branch: main
base_sha: 272ea49f5bf2d8651e22dfa776537e8ea61758e2
created: 2026-08-20T12:36:11+02:00
updated: 2026-08-20T12:36:11+02:00
risk: medium
owned_paths:
  - tools/tibia_re_surveyor/runtime.py
  - tests/tools/tibia_re_surveyor/test_runtime.py
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - docs/agents/operators/TRACK_A_SURVEYOR_V2_READONLY.md
  - tools/tibia_re_surveyor/README.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260820-runtime-namespace-hardening.md
  - docs/agents/tasks/archive/OTC-20260820-runtime-namespace-hardening.md
modules_touched:
  - tibia-re-surveyor
  - track-a-runtime-operator
reuses:
  - tools/tibia_re_surveyor/**
  - .github/workflows/track-a-surveyor-v2-readonly.yml
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
depends_on: []
blocks: []
cross_repository_task_ids: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: local_git_plus_github
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
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
invocation_started_at: 2026-08-20T12:36:11+02:00
last_progress_at: 2026-08-20T12:43:09+02:00
context_pressure: medium
context_growth: stable
context_score: 6
decomposition_decision: single
heavy_validation_runs: 0
repair_cycles: 0
ci_checks_for_current_head: 0
terminal_ci_checks_for_current_generation: 0
current_blocker: none
next_action: commit and push the namespace-scoped implementation, then run exact-head CI and independent audit on PR #623
---

# Track A Surveyor runtime namespace hardening

## Objective

Make the Surveyor v2 and its trusted read-only operator observe only the explicitly declared OTClient Track A runtime container. They must not enumerate or execute commands in unrelated Docker containers on the shared Synology host.

## Acceptance criteria

- 	ools/tibia_re_surveyor/runtime.py never calls host-wide docker ps and never executes pgrep or other discovery commands in unrelated containers.
- Runtime target proof is scoped to otclient-track-a-kasmvnc: exactly one client PID, exact current size/SHA fence, one matching X11 window and matching canonical registration when present.
- otclient-synology-runner is used only for allowlisted canonical control-plane metadata reads.
- .github/workflows/track-a-surveyor-v2-readonly.yml performs no all-container enumeration and no command against a container other than the declared Track A runtime target.
- Read-only target uniqueness is explicitly namespace-scoped and does not claim host-global Docker uniqueness.
- Focused tests prove no docker ps path exists, exact target singleton behavior is fail-closed, and external-container names never enter command execution.
- Documentation, module catalogue and changelog describe the namespace-scoped boundary accurately.
- Independent audit PASS, physical read-only E2E after merge PASS, final exact-head required CI PASS, zero review threads, terminal archive and ownership release.

## Implementation validation checkpoint

`yaml
checkpoint_version: 2
updated_at: 2026-08-20T12:43:09+02:00
status: validating
phase: validate
pr: 623
runtime_access: none
implementation:
  hostwide_docker_enumeration: removed
  target_container: otclient-track-a-kasmvnc
  control_container: otclient-synology-runner
  external_containers_scanned: false
  uniqueness_scope: DECLARED_RUNTIME_NAMESPACE
focused_validation:
  compileall: PASS
  unittest_discover: 23_PASS
  repository_only_collect_all: PASS
  aliases: 12
  telemetry_documents: 11
  privacy_scan: PASS
  manifest_present: true
  yaml_parse: PASS
  hostwide_discovery_refs: NONE
  diff_check: PASS
runtime_e2e: PENDING_POST_MERGE
blockers: []
next_action: exact-head CI and independent audit on the implementation head
`
