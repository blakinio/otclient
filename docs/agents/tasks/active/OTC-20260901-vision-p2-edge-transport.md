---
task_id: OTC-20260901-vision-p2-edge-transport
status: ready
agent: unclaimed
session_role: phase2_worker
worker_alias: OTC-VISION-P2-EDGE-TRANSPORT
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: dispatch_ready
branch: feat/OTC-20260901-vision-p2-edge-transport
base_branch: main
base_main: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T16:31:41+02:00
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
  - main 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
related_prs:
  - PR #829 Wave 1 worker Draft
current_blocker: none
next_action: launch OTC-VISION-P2-EDGE-TRANSPORT in its isolated worker session, verify Draft PR #829 still matches this branch/worktree/ownership, read binding contracts, then write the first RED focused test at tests/tools/tibia_re_control_center/test_agent_edge_transport.py with runtime_access none
invocation_started_at: null
last_progress_at: 2026-09-01T16:31:41+02:00
ci_checks_for_current_head: 0
ci_check_generation: pr-bound-bootstrap
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
BASE_MAIN: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
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
updated_at: 2026-09-01T16:31:41+02:00
head: 2f79d907f3372f7c8215fb6f4e2034547038ecb8
branch: feat/OTC-20260901-vision-p2-edge-transport
pr: 829
status: ready
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
  - branch and isolated worktree were created by the coordinator from exact main 0fe1ecb3569f1d8372209c857ab57f3b626c29ae.
  - Draft PR 829 exists for this exact worker branch and was opened from bootstrap head 2f79d907f3372f7c8215fb6f4e2034547038ecb8.
  - PR 820 and PR 824 are merged prerequisites.
  - coordinator pairwise and refreshed-main ownership scans found no overlap for this worker ownership set.
  - bootstrap checkpoint, Track A runtime governance and git diff --check passed before PR binding.
  - runtime_access is none; all mutation/runtime-effect authorities remain false and physical action budget/count are 0/0.
derived:
  - the isolated worker may begin repository/static RED-to-GREEN work only after its own session revalidates this task, Draft PR, branch, worktree and ownership.
unknown:
  - implementation, focused test, review and exact-head CI outcomes.
  - any future real-runtime evidence; none is authorized or claimed at bootstrap.
conflicts: []
first_failure:
  marker: none
  evidence: no current failure; worker session has not yet claimed execution.
rejected_hypotheses:
  - fake or hosted evidence can satisfy real-runtime acceptance: rejected by the Phase 2 contract.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-edge-transport.md
validation:
  - command: coordinator refreshed-main and pairwise ownership scans
    result: PASS
    evidence: no worker-worker or active-main exact ownership conflicts.
  - command: bootstrap Track A governance and checkpoint validation
    result: PASS
    evidence: task was branch-bound and runtime_access none admission was valid before Draft PR binding.
  - command: live Draft PR creation readback
    result: PASS
    evidence: PR 829 opened Draft against main from feat/OTC-20260901-vision-p2-edge-transport at 2f79d907f3372f7c8215fb6f4e2034547038ecb8.
blockers: []
next_action: launch OTC-VISION-P2-EDGE-TRANSPORT in its isolated worker session, verify Draft PR #829 still matches this branch/worktree/ownership, read binding contracts, then write the first RED focused test at tests/tools/tibia_re_control_center/test_agent_edge_transport.py with runtime_access none.
```
