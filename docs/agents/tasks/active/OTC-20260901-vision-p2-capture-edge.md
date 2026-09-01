---
task_id: OTC-20260901-vision-p2-capture-edge
status: ready
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-CAPTURE-EDGE
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: worker_ready_for_coordinator
branch: feat/OTC-20260901-vision-p2-capture-edge
base_branch: main
base_main: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T18:01:05+02:00
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
worktree: C:/Users/barte/otclient-vision-p2-capture-edge
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
  - docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
depends_on:
  - PR #820 merged foundation
  - PR #824 merged Wave 0 coordinator cleanup
  - main 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
related_prs:
  - PR #827 Wave 1 worker Draft
current_blocker: none
next_action: return Draft PR #827 to OTC-VISION-P2-COORDINATOR for classification/integration; this worker must not mark Ready or merge
invocation_started_at: 2026-09-01T16:58:39+02:00
last_progress_at: 2026-09-01T18:01:05+02:00
ci_checks_for_current_head: 2
ci_check_generation: implementation-head-8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38
terminal_ci_wait_started_at: 2026-09-01T17:58:40+02:00
terminal_ci_checks_for_current_generation: 4
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

# OTC-VISION-P2-CAPTURE-EDGE

## Mission

Implement the smallest secret-safe read-only capture edge for exact-bound screenshot/crop/hash evidence with provenance, geometry, time and full-frame binding; never synthesize input.

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

- `docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md`
- `docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md`
- `tools/tibia_re_vision/capture_edge.py`
- `tests/tools/tibia_re_vision/test_capture_edge.py`

Shared indexes/governance files, including `docs/agents/MODULE_CATALOG.md`, are not owned. Any required path outside this set is a coordinator ownership-extension request, not an implicit permission.

## Implementation discipline

Use RED-to-GREEN TDD for each behavior. Preserve the approved architecture and reuse the existing Control Center/session plane rather than creating a second control plane/store. Fake/hosted evidence can validate repository behavior but can never be reported as real-runtime success. The worker must open no additional implementation PR and must not merge/promote its own result; the coordinator classifies the Draft PR.

## Dispatch contract

```yaml
programme_id: OTC-VISION-P2-READONLY
worker_alias: OTC-VISION-P2-CAPTURE-EDGE
TASK_ID: OTC-20260901-vision-p2-capture-edge
TASK_RECORD: docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
PROJECT_LANE: otclient
BASE_MAIN: 0fe1ecb3569f1d8372209c857ab57f3b626c29ae
BRANCH: feat/OTC-20260901-vision-p2-capture-edge
WORKTREE: C:/Users/barte/otclient-vision-p2-capture-edge
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
  - docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
DEPENDENCIES:
  - PR #820 merged
  - PR #824 merged
runtime_access: none
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:01:05+02:00
head: 8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38
branch: feat/OTC-20260901-vision-p2-capture-edge
pr: 827
status: ready
context_routes:
  - phase-2-read-only-coordination
  - track-a-governance
  - capture-edge
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
  - docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
proven:
  - Draft PR 827 remains the exact pre-bound worker PR and live GitHub head equals implementation head 8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38.
  - runtime_access is none; all mutation/runtime-effect authorities are false and physical action budget/count are 0/0.
  - RED-to-GREEN focused tests cover exact binding/freshness, pre/post geometry binding, final binding-race closure, secret-safe in-memory masking, crop/full hash binding, content addressing, blank/black/change metadata, downstream integrity/currentness, fixed read-only Kasm/X11/ffmpeg command construction, and absence of an unchecked public vision-conversion bypass.
  - focused capture-edge suite passes 11/11; capture-edge plus existing vision-evidence suite passes 15/15; targeted py_compile passes.
  - local Track A runtime governance, checkpoint validation and git diff --check pass.
  - GitHub CI run 33529034080 and Track A agent runtime governance run 33529033773 both completed SUCCESS on exact implementation head 8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38.
  - the one broader agent_vision error and foundation synthetic-E2E failure reproduce unchanged from clean committed pre-implementation head dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b and are pre-existing outside worker ownership.
derived:
  - the repository/static capture-edge worker slice is ready for coordinator classification/integration.
  - no result in this worker proves real Official Tibia runtime capture behavior.
unknown:
  - independent coordinator review/integration disposition and any shared MODULE_CATALOG/CHANGELOG update.
  - real admitted Linux/Synology/Kasm read-only runtime verification; not authorized in this worker checkpoint.
conflicts: []
first_failure:
  marker: RED-CAPTURE-EDGE-MODULE-ABSENT
  evidence: the first focused test failed because tools.tibia_re_vision.capture_edge did not exist; subsequent behavior slices were also proven through focused RED before GREEN implementation.
rejected_hypotheses:
  - fake or hosted evidence can satisfy real-runtime acceptance: rejected by the Phase 2 contract.
  - the broad agent_vision snapshot error is caused by capture-edge changes: rejected by identical clean-baseline reproduction at dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b.
  - the foundation synthetic E2E failure is caused by capture-edge changes: rejected by identical clean-baseline reproduction at dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
  - docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
validation:
  - command: python -m unittest tests/tools/tibia_re_vision/test_capture_edge.py
    result: PASS
    evidence: 11 tests, 0 failures/errors.
  - command: python -m py_compile tools/tibia_re_vision/capture_edge.py tests/tools/tibia_re_vision/test_capture_edge.py
    result: PASS
    evidence: both files compile under local Python 3.12.
  - command: python -m unittest tests/tools/tibia_re_vision/test_evidence.py tests/tools/tibia_re_vision/test_capture_edge.py
    result: PASS
    evidence: 15 tests, 0 failures/errors.
  - command: Track A runtime governance validator for changed-from 0fe1ecb3569f1d8372209c857ab57f3b626c29ae and expected worker branch
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true.
  - command: GitHub CI run 33529034080 on 8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38
    result: PASS
    evidence: workflow completed with conclusion success.
  - command: GitHub Track A agent runtime governance run 33529033773 on 8685f7c6a8dae9e41d71f0acbe70a89a35a0ef38
    result: PASS
    evidence: workflow completed with conclusion success.
  - command: broader test_agent_vision and synthetic foundation E2E baseline comparison
    result: FAIL
    evidence: both observed failures reproduce from clean archive of committed pre-implementation head dd40d914fa5d05cdf5ff2957cc798ee7aa336d9b; no worker-owned file is involved.
blockers: []
next_action: return Draft PR #827 to OTC-VISION-P2-COORDINATOR for classification/integration; this worker must not mark Ready or merge.
```
