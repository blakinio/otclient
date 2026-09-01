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
phase: trust_boundary_fail_closed_repair
branch: feat/OTC-20260901-vision-p2-capture-edge
base_branch: main
base_main: d1cb8722c3116a0e0aeb72b9b360712f43151f17
created: 2026-09-01T16:27:39+02:00
updated_at: 2026-09-01T23:40:00+02:00
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
current_blocker: no externally pinned reviewed secret-mask policy and canonical symlink-safe evidence-root consumer exists within the four owned worker paths; capture must remain fail closed
next_action: restack the fail-closed repair on current main, run exact local governance/path validation, push with a lease, and request coordinator classification of the missing trusted consumer
invocation_started_at: 2026-09-01T16:58:39+02:00
last_progress_at: 2026-09-01T23:40:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: current-main-revalidation-pending
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

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: 2026-09-01T22:50:00+02:00
  session_started_at: 2026-09-01T22:50:00+02:00
  checkpointed_at: 2026-09-01T23:05:00+02:00
  last_progress_at: 2026-09-01T23:05:00+02:00
  phase: benchmark_reclassification_repaired_local_validation
  exact_head: 14cb64db3ef13c753ba196529ee1f6672d215879
  pull_request: 827
  active_operation: local governance and checkpoint validation
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: benchmark-reclassification-repair
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: existing worker branch remains exclusively owned and the three reproduced benchmark findings remain unresolved
  next_action: run Track A governance and checkpoint/path validation on the repaired exact head, push with a lease, then request coordinator re-review of Draft PR #827
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T23:05:00+02:00
head: 14cb64db3ef13c753ba196529ee1f6672d215879
head_semantics: benchmark-reclassification repair implementation before current checkpoint docs
branch: feat/OTC-20260901-vision-p2-capture-edge
pr: 827
status: validating
phase: benchmark_reclassification_repaired_local_validation
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
  - coordinator comment 5500210008 mechanically proved promotion head b4a2664778d001344e3d0fdbd19ff4c9ac118e18 retained the benchmark-target capture_edge.py and test_capture_edge.py blobs, so prior ACCEPT is superseded.
  - focused RED reproduced the three repair categories: public CaptureEvidence constructor accepted caller-provided secret_safe/hash/binding fields; source_monotonic_ns was sampled after capture; and ReviewedSecretMaskPolicy was publicly constructible.
  - CaptureEvidence is now an immutable producer-issued opaque object; public construction and wrong-token issuance fail, and validation rejects an object allocated outside the producer issuance registry before reading caller fields.
  - ReviewedSecretMaskPolicy is now immutable and resolver-issued; CaptureEdge accepts only the exact policy issued by its composition-time resolver and rejects a foreign resolver policy when a resolver is explicitly bound.
  - source_monotonic_ns is sampled immediately before capture_rgb and is no longer replaced by a later post-capture/postcheck time.
  - local GREEN evidence after the repair: focused capture-edge 17/17, capture-edge plus existing vision evidence 21/21, complete vision suite 24/24, py_compile, ruff and diff check PASS.
  - coordinator comment 5497472188 identified the broader remaining gap: arbitrary non-empty per-call masks could still self-certify secret_safe.
  - focused RED required ReviewedSecretMaskPolicy at trusted composition time and failed because the published module lacked that contract.
  - ReviewedSecretMaskPolicy is immutable, binds a reviewed policy id, exact expected frame dimensions, deterministic non-empty regions and content-addressed policy_ref.
  - CaptureEdge constructor now requires ReviewedSecretMaskPolicy; CaptureEdge.capture exposes no secret_policy parameter.
  - frame dimensions that do not match the reviewed policy fail with CAPTURE_SECRET_POLICY_GEOMETRY_MISMATCH before RGB capture or artifact persistence.
  - CaptureEvidence records secret_policy_ref; masking still occurs in memory before PNG persistence/crop derivation.
  - branch was restacked conflict-free onto trusted main e883543403d5430d7b1d287f59043b23c98f37d6, which includes promoted runtime-admission producer PR #838.
  - post-restack focused capture-edge suite passes 14/14; capture-edge plus existing vision-evidence suite passes 18/18.
  - post-restack py_compile, Track A runtime governance, checkpoint validation and git diff --check pass; changed paths remain exactly four worker-owned paths.
  - public-surface audit confirms capture parameters are self, run_id, evidence_root, max_binding_age_ns, crop and previous_full_sha256; legacy SecretSafetyPolicy is absent.
derived:
  - producer-issued evidence plus validation-time issuance verification closes the public dataclass-forgery bypass without relaxing runtime/hash/geometry/crop fences.
  - the explicit resolver boundary makes the trusted composition root the policy issuance authority; a public direct policy constructor and cross-resolver policy injection cannot certify secret safety.
  - the arbitrary per-call secret-mask authority found in coordinator re-review is removed from the capture request surface.
  - no repository/static result proves real Official Tibia runtime capture behavior.
unknown:
  - exact-head GitHub CI/governance and independent coordinator re-review of this repair generation.
  - independent coordinator re-review disposition on the second repaired generation.
  - real admitted Linux/Synology/Kasm read-only runtime verification; not authorized in this worker checkpoint.
conflicts: []
first_failure:
  marker: RED-BENCHMARK-FORGED-EVIDENCE-FRESHNESS-ISSUANCE
  evidence: focused test run failed with public CaptureEvidence forging accepted, post-capture freshness behavior, and no ReviewedSecretMaskPolicyResolver surface before the repair.
rejected_hypotheses:
  - content hashes, binding equality and caller-set secret_safe alone constitute trusted capture provenance: rejected because they are reproducible by caller-constructed evidence.
  - a post-capture/postcheck timestamp may represent the pixel acquisition time: rejected because it makes earlier pixels appear younger.
  - a syntactically valid public ReviewedSecretMaskPolicy is reviewed: rejected; issuance is now resolver-owned and edge-bound.
  - any non-empty per-call mask is sufficient proof of secret safety: rejected by coordinator re-review and removed from the public capture API.
  - GitHub-only production patching should bypass the local RED-to-GREEN loop while the host is offline: rejected; production remained untouched until Molehill-PC returned online.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
  - docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
validation:
  - command: focused RED `python -m unittest tests.tools.tibia_re_vision.test_capture_edge -q`
    result: FAIL
    evidence: 17-test run failed before repair: public forged evidence accepted, post-capture freshness rejected the new acquisition assertion, and resolver issuer was absent.
  - command: `python -m unittest tests.tools.tibia_re_vision.test_capture_edge -q`
    result: PASS
    evidence: 17 tests, zero failures/errors after repair.
  - command: `python -m unittest tests.tools.tibia_re_vision.test_evidence tests.tools.tibia_re_vision.test_capture_edge -q`
    result: PASS
    evidence: 21 tests, zero failures/errors after repair.
  - command: `python -m unittest discover -s tests/tools/tibia_re_vision -p 'test_*.py' -q`
    result: PASS
    evidence: 24 tests, zero failures/errors after repair.
  - command: py_compile and `ruff check tools/tibia_re_vision tests/tools/tibia_re_vision`
    result: PASS
    evidence: both changed modules compile and ruff reports all checks passed.
  - command: `python .github/scripts/test_track_a_agent_runtime_governance.py --changed-from origin/main --expected-branch feat/OTC-20260901-vision-p2-capture-edge`
    result: PASS
    evidence: TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true; changed tasks and branch-bound tasks both equal 1.
  - command: checkpoint validator, resume generator and changed-path audit
    result: PASS
    evidence: checkpoint validates, resume resolves this task, diff check passes, and origin/main...HEAD contains exactly the four owned paths.
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
next_action: run Track A governance and checkpoint/path validation on the repaired exact head, push with a lease, then request coordinator re-review of Draft PR #827; worker must not self-promote or merge.
```

## Context checkpoint — trust-boundary fail-closed repair

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T23:40:00+02:00
head: uncommitted
branch: feat/OTC-20260901-vision-p2-capture-edge
pr: 827
status: implementing
phase: trust_boundary_fail_closed_repair
proven:
  - coordinator comment 5500483713 reproduced direct token issue, registry injection, subclass issue, reflective evidence mutation, caller-created resolver, policy mutation, same-object binding mutation and unsafe caller root concerns.
  - underscore names, module globals, registries, object identity and frozen dataclasses cannot provide unforgeability in this Python boundary.
  - no trusted externally pinned reviewed mask-policy source or canonical symlink-safe evidence-root composition consumer is present in the worker-owned paths.
  - capture, direct persistence and SecretSafeCapture conversion now fail closed before an effect; module issuance tokens and registry are removed.
  - focused adversarial tests are GREEN: direct/subclass issuance, public incomplete policy, allocated/mutated evidence, attacker root, mutable binding snapshot and invalid/future monotonic samples.
derived:
  - this worker must not claim active secret-safe evidence production until a separately owned trusted composition consumer pins the reviewed expected policy and canonical evidence root.
unknown:
  - coordinator-owned trusted composition/consumer design and its exact path ownership.
  - exact-head CI/governance and coordinator re-review after restack.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-vision-p2-capture-edge.md
  - docs/agents/reports/OTC-20260901-vision-p2-capture-edge.md
  - tools/tibia_re_vision/capture_edge.py
  - tests/tools/tibia_re_vision/test_capture_edge.py
validation:
  - command: python -m unittest tests.tools.tibia_re_vision.test_capture_edge -q
    result: PASS
    evidence: 12 tests
  - command: python -m unittest tests.tools.tibia_re_vision.test_evidence tests.tools.tibia_re_vision.test_capture_edge -q
    result: PASS
    evidence: 16 tests
  - command: python -m unittest discover -s tests/tools/tibia_re_vision -p 'test_*.py' -q
    result: PASS
    evidence: 19 tests
  - command: py_compile, Ruff and git diff --check
    result: PASS
blockers:
  - trusted reviewed mask-policy and canonical evidence-root consumer are outside the worker-owned paths and have not been proven.
next_action: commit, restack on origin/main, rerun governance/checkpoint/path validation, push with a safe lease, then request coordinator classification; do not self-promote or merge.
```
