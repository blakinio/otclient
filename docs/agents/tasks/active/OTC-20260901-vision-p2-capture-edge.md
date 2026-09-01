---
task_id: OTC-20260901-vision-p2-capture-edge
status: validating
agent: ChatGPT
session_role: phase2_worker
worker_alias: OTC-VISION-P2-CAPTURE-EDGE
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: implementation
phase: worker_repair_local_validation_complete
branch: feat/OTC-20260901-vision-p2-capture-edge
base_branch: main
base_main: 54a20bbd8721e92d069974af14d6ebd2f4f5a55d
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T18:38:34+02:00
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
current_blocker: exact-head GitHub CI/governance pending on restacked secret-safety repair generation
next_action: commit and publish the restacked secret-safety repair generation, verify exact-head CI/governance, then return Draft PR #827 to OTC-VISION-P2-COORDINATOR for re-review
invocation_started_at: 2026-09-01T16:58:39+02:00
last_progress_at: 2026-09-01T18:38:34+02:00
ci_checks_for_current_head: 0
ci_check_generation: repair-unpublished-87dd4b914f47
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
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
updated_at: 2026-09-01T18:38:34+02:00
head: 87dd4b914f471fd70e5e632fad69edbfce86f888
branch: feat/OTC-20260901-vision-p2-capture-edge
pr: 827
status: validating
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
  - coordinator review comment 5496909848 returned the prior generation because an empty caller policy could self-certify secret_safe without machine-checkable proof.
  - RED test test_unproven_empty_secret_policy_fails_before_frame_capture_or_persistence failed because CaptureEdgeError was not raised before the repair.
  - repaired CaptureEdge.capture rejects empty secret_regions with CAPTURE_SECRET_POLICY_UNPROVEN before binding/frame-source use or artifact persistence.
  - deterministic non-empty masking remains the only accepted secret-safe path in this worker slice; masked crop/full content-addressing and runtime/geometry fences are preserved.
  - branch was restacked conflict-free onto trusted main 54a20bbd8721e92d069974af14d6ebd2f4f5a55d; exact changed paths remain the four declared worker-owned paths.
  - post-restack focused capture-edge suite passes 12/12 and capture-edge plus existing vision-evidence suite passes 16/16.
  - post-restack py_compile, Track A runtime governance, git diff --check, shell=True audit and production no_secret_fields-call audit pass.
derived:
  - the coordinator secret-safety finding is repaired in repository/static behavior and is ready for exact-head hosted verification.
  - no repository/static result proves real Official Tibia runtime capture behavior.
unknown:
  - exact-head GitHub CI/governance outcome for the restacked repair generation.
  - coordinator re-review disposition after hosted verification.
  - real admitted Linux/Synology/Kasm read-only runtime verification; not authorized in this worker checkpoint.
conflicts: []
first_failure:
  marker: RED-UNPROVEN-EMPTY-SECRET-POLICY
  evidence: focused RED expected CAPTURE_SECRET_POLICY_UNPROVEN but prior CaptureEdge.capture persisted/returned evidence instead.
rejected_hypotheses:
  - a caller-authored empty secret policy can prove a frame is secret-free: rejected by coordinator review and the repaired fail-closed contract.
  - a new caller-authored proof token is required: rejected; this repair admits only deterministic non-empty masking in this slice.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
  - docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
validation:
  - command: python -m unittest tests/tools/tibia_re_vision/test_capture_edge.py -q
    result: PASS
    evidence: 12 tests, zero failures/errors after restack.
  - command: python -m unittest tests/tools/tibia_re_vision/test_evidence.py tests/tools/tibia_re_vision/test_capture_edge.py -q
    result: PASS
    evidence: 16 tests, zero failures/errors after restack.
  - command: Track A runtime governance validator changed-from current trusted main
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true.
  - command: git diff --check origin/main...HEAD plus AST/public-surface audit
    result: PASS
    evidence: four owned paths only; shell=True=0; production no_secret_fields calls=0; unproven guard present.
blockers:
  - exact-head GitHub CI/governance is pending after publication.
next_action: commit and publish the restacked secret-safety repair generation, verify exact-head CI/governance, then return Draft PR #827 to OTC-VISION-P2-COORDINATOR for re-review.
```
