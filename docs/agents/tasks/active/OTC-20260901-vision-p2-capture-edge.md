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
phase: worker_second_repair_ready_for_coordinator
branch: feat/OTC-20260901-vision-p2-capture-edge
base_branch: main
base_main: fb0c489f2ed166e872c4f197c6a78375a8576685
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T20:51:35+02:00
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
next_action: return exact-head-green Draft PR #827 to OTC-VISION-P2-COORDINATOR for independent re-review; worker must not self-promote or merge
invocation_started_at: 2026-09-01T16:58:39+02:00
last_progress_at: 2026-09-01T20:51:35+02:00
ci_checks_for_current_head: 2
ci_check_generation: second-repair-green-1f550b658ca6
terminal_ci_wait_started_at: 2026-09-01T20:47:34+02:00
terminal_ci_checks_for_current_generation: 2
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
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
updated_at: 2026-09-01T20:51:35+02:00
head: f3b149e38bc1f49808295d6762522ac78e95e859
head_semantics: implementation_commit_before_checkpoint_docs
branch: feat/OTC-20260901-vision-p2-capture-edge
pr: 827
status: ready
phase: worker_second_repair_ready_for_coordinator
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
  - coordinator comment 5497472188 identified the broader remaining gap: arbitrary non-empty per-call masks could still self-certify secret_safe.
  - focused RED required ReviewedSecretMaskPolicy at trusted composition time and failed because the published module lacked that contract.
  - ReviewedSecretMaskPolicy is immutable, binds a reviewed policy id, exact expected frame dimensions, deterministic non-empty regions and content-addressed policy_ref.
  - CaptureEdge constructor now requires ReviewedSecretMaskPolicy; CaptureEdge.capture exposes no secret_policy parameter.
  - frame dimensions that do not match the reviewed policy fail with CAPTURE_SECRET_POLICY_GEOMETRY_MISMATCH before RGB capture or artifact persistence.
  - CaptureEvidence records secret_policy_ref; masking still occurs in memory before PNG persistence/crop derivation.
  - branch was restacked conflict-free onto trusted main fb0c489f2ed166e872c4f197c6a78375a8576685, which includes promoted runtime-admission producer PR #838.
  - post-restack focused capture-edge suite passes 14/14; capture-edge plus existing vision-evidence suite passes 18/18.
  - post-restack py_compile, Track A runtime governance, checkpoint validation and git diff --check pass; changed paths remain exactly four worker-owned paths.
  - public-surface audit confirms capture parameters are self, run_id, evidence_root, max_binding_age_ns, crop and previous_full_sha256; legacy SecretSafetyPolicy is absent.
  - exact checkpoint head 1f550b658ca6f17c02f4aeec80fd01cc212122b5 passed GitHub CI run 33545702287 and Track A governance run 33545701984.
derived:
  - the arbitrary per-call secret-mask authority found in coordinator re-review is removed from the capture request surface.
  - no repository/static result proves real Official Tibia runtime capture behavior.
unknown:
  - independent coordinator re-review disposition on the second repaired generation.
  - real admitted Linux/Synology/Kasm read-only runtime verification; not authorized in this worker checkpoint.
conflicts: []
first_failure:
  marker: RED-REVIEWED-MASK-NOT-COMPOSITION-BOUND
  evidence: focused test test_reviewed_secret_policy_is_bound_to_edge_not_each_capture failed because ReviewedSecretMaskPolicy did not exist.
rejected_hypotheses:
  - any non-empty per-call mask is sufficient proof of secret safety: rejected by coordinator re-review and removed from the public capture API.
  - GitHub-only production patching should bypass the local RED-to-GREEN loop while the host is offline: rejected; production remained untouched until Molehill-PC returned online.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
  - docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
validation:
  - command: python -m unittest tests.tools.tibia_re_vision.test_capture_edge -q
    result: PASS
    evidence: 14 tests, zero failures/errors after restack.
  - command: python -m unittest tests.tools.tibia_re_vision.test_evidence tests.tools.tibia_re_vision.test_capture_edge -q
    result: PASS
    evidence: 18 tests, zero failures/errors after restack.
  - command: py_compile implementation and focused tests
    result: PASS
    evidence: both files compile.
  - command: Track A runtime governance changed-from fb0c489f2ed166e872c4f197c6a78375a8576685
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true.
  - command: checkpoint validator and git diff --check origin/main...HEAD
    result: PASS
    evidence: checkpoint schema valid and no whitespace/path-boundary finding.
blockers: []
next_action: return exact-head-green Draft PR #827 to OTC-VISION-P2-COORDINATOR for independent re-review; worker must not self-promote or merge.
```
