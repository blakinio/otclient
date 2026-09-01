---
task_id: OTC-20260901-vision-p2-edge-transport
status: validating
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-EDGE-TRANSPORT
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: worker_ci_portability_repair_ready
branch: feat/OTC-20260901-vision-p2-edge-transport
base_branch: main
base_main: e883543403d5430d7b1d287f59043b23c98f37d6
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T22:37:15+02:00
risk: high
execution_class: github_hosted
execution_mode: isolated_worker_branch
preferred_execution: codex
run_scope: wave_1_worker
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
prompting_standard_version: 2.1
policy_version: 2
track_a_runtime_agent_admission_version: 1
routing_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
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
worktree: C:/Users/barte/otclient-vision-p2-edge-transport
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
depends_on:
  - PR #820 merged foundation
  - PR #824 merged Wave 0 coordinator cleanup
  - current main e883543403d5430d7b1d287f59043b23c98f37d6 after PR #839
related_prs:
  - PR #829 Wave 1 worker Draft
current_blocker: exact-head Package A/B CI failed only on an interpreter-dependent recursion-depth test; deterministic test repair is local and awaits publication
next_action: commit the deterministic parser-recursion test repair and CI checkpoint, rerun owned local gates, push the new head, then observe its exact-head CI
invocation_started_at: 2026-09-01T17:03:28+02:00
last_progress_at: 2026-09-01T22:37:15+02:00
ci_checks_for_current_head: 2
ci_check_generation: draft-d6c3a1e5-ci-failure-isolated
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
runtime_nonclaims:
  display_98_current_canonical_status: UNKNOWN
  rfb_6082_current_backend_mapping: UNKNOWN
  current_exact_client_pid: NOT_REGISTERED
  current_exact_client_session: NOT_REGISTERED
---

# OTC-VISION-P2-EDGE-TRANSPORT

## Mission

Implement a narrow authenticated bounded Synology-to-Molehill edge transport with versioned metadata and content-addressed artifacts, without generic shell, raw GUI control or authority expansion.

## Dispatch boundary

This task is bootstrapped by `OTC-VISION-P2-COORDINATOR`. The worker may mutate repository files only after its own isolated session validates the exact task, branch, worktree and Draft PR and confirms the ownership set below remains non-overlapping. Real Official Tibia runtime observation is **not authorized** by this record. Any later transition from `runtime_access: none` to `read_only` requires a coordinator-assigned single observation window, fresh exact-target proof, and a persisted valid read-only admission record before observation.

## Binding reads

- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`

## Owned paths

- `docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md`
- `docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md`
- `tools/tibia_re_control_center/agent_edge_transport.py`
- `tests/tools/tibia_re_control_center/test_agent_edge_transport.py`

Shared indexes/governance files, including `docs/agents/MODULE_CATALOG.md`, are not owned. Any required path outside this set is a coordinator ownership-extension request, not an implicit permission.

## Implementation discipline

Use RED-to-GREEN TDD for each behavior. Preserve the approved architecture and reuse the existing Control Center/session plane rather than creating a second control plane/store. Fake/hosted evidence can validate repository behavior but can never be reported as real-runtime success. The worker must open no additional implementation PR and must not merge/promote its own result; the coordinator classifies the Draft PR.

## Dispatch contract

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-EDGE-TRANSPORT
TASK_ID: OTC-20260901-vision-p2-edge-transport
TASK_RECORD: docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
PROJECT_LANE: otclient
BASE_MAIN: e883543403d5430d7b1d287f59043b23c98f37d6
BRANCH: feat/OTC-20260901-vision-p2-edge-transport
WORKTREE: C:/Users/barte/otclient-vision-p2-edge-transport
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
DEPENDENCIES:
  - PR #820 merged
  - PR #824 merged
runtime_access: none
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T22:37:15+02:00
head: d6c3a1e5b1b253c11dea52bb10cf83c45b75d103
head_semantics: published_exact_head_with_ci_failure_before_test_portability_repair_commit
branch: feat/OTC-20260901-vision-p2-edge-transport
pr: 829
status: validating
phase: worker_ci_portability_repair_ready
context_routes:
  - phase-2-read-only-coordination
  - track-a-governance
  - edge-transport
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
proven:
  - Draft PR #829 published exact head d6c3a1e5b1b253c11dea52bb10cf83c45b75d103 against main e883543403d5430d7b1d287f59043b23c98f37d6 with only four declared owned paths.
  - exact-head CI and Track A governance passed; Package A run 33555788479 and Package B run 33555788277 each failed only the same edge-transport recursion test.
  - both failed workflow logs report test_receiver_converts_json_recursion_failure_to_validation_error expected EDGE_FRAME_INVALID but received MISSING_FIELD on Ubuntu; all other 522 tests passed there with three skips.
  - the failure is an interpreter-dependent test assumption: fixed nesting depth 2000 does not reliably force json.loads RecursionError across environments.
  - production already explicitly converts RecursionError from json.loads into EDGE_FRAME_INVALID; no production behavior change is required for this CI repair.
  - the repaired test deterministically injects RecursionError at the parser seam and verifies the existing safe boundary mapping independent of interpreter recursion depth.
  - local repaired focused test passes; focused suite passes 30/30 and component suite passes 47/47.
  - Windows full discovery still has five reproducible unowned agent_api/agent_vision environment-specific errors; the prior Linux CI run proves those same tests pass on the hosted runner and they are not caused by this edge transport slice.
  - runtime_access remains none; no live runtime observation, mutation or physical action occurred.
derived:
  - the exact-head Package A/B failures belong to this task-owned test but not to production transport semantics; deterministic test repair is the smallest valid CI fix.
  - the worker must publish a new head and obtain fresh exact-head CI before returning the Draft PR for coordinator classification.
unknown:
  - exact-head CI outcome after publishing the deterministic recursion-test repair.
  - coordinator independent classification after a green exact head.
conflicts: []
first_failure:
  marker: CI-RECURSION-TEST-PORTABILITY
  evidence: Package A run 33555788479 and Package B run 33555788277 fail only test_receiver_converts_json_recursion_failure_to_validation_error on d6c3a1e5b1b253c11dea52bb10cf83c45b75d103.
rejected_hypotheses:
  - production RecursionError mapping is absent: rejected by source inspection and deterministic repaired test.
  - Package A/B contain broader regressions caused by edge transport: rejected; hosted logs show exactly one failure and independent Package A/B audits plus Package B browser E2E pass.
  - local Windows full-discovery errors are caused by edge transport: rejected; they are in unowned agent_api/agent_vision surfaces and hosted Linux exact-head execution passes those cases.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
  - docs/agents/reports/OTC-20260901-vision-p2-edge-transport.md
  - tools/tibia_re_control_center/agent_edge_transport.py
  - tests/tools/tibia_re_control_center/test_agent_edge_transport.py
validation:
  - command: GitHub exact-head workflow snapshot for d6c3a1e5b1b253c11dea52bb10cf83c45b75d103
    result: FAIL
    evidence: CI SUCCESS; Track A governance SUCCESS; Package A/B fail the same single portability test.
  - command: gh run view 33555788479 --log-failed; gh run view 33555788277 --log-failed
    result: PASS
    evidence: first actionable error isolated to the fixed-depth recursion expectation; hosted suite otherwise reports 522 passes and three skips.
  - command: deterministic repaired recursion-boundary test
    result: PASS
    evidence: injected RecursionError is converted to ValidationError code EDGE_FRAME_INVALID.
  - command: focused and protocol+transport suites after repair
    result: PASS
    evidence: 30/30 and 47/47 locally.
blockers:
  - fresh exact-head CI is required after publishing the repair.
next_action: commit the deterministic parser-recursion test repair and CI checkpoint, rerun owned local gates, push the new head, then observe its exact-head CI.
```
