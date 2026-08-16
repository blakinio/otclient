# OTC-20260816 — official-client map viewport feasibility

```yaml
task_id: OTC-20260816-official-client-map-viewport-feasibility
policy_version: 2
project_lane: otclient
track: official-client-re
repository: blakinio/otclient
task_kind: discovery
implementation_authorized: false
phase: close
status: ready
base_branch: main
base_head: 3a5568f36ebc326afd246d0d2da45b5d8eecabfa
branch: docs/OTC-20260816-official-client-map-viewport-feasibility
pull_request: 325
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
session_id: chat-20260816-viewport-feasibility
session_role: validator
execution_mode: chat_github_connector
execution_reason: narrow repository documentation, primary GitHub evidence review and PR closeout require no owner-funded AI or local checkout
updated_at: 2026-08-16T08:42:00+02:00
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one cohesive evidence checkpoint with one report, one evidence index and one task lifecycle
validation_level: focused
session_rotation_count: 0
heavy_validation_runs: 0
stale_takeover_count: 0
human_interruptions: 0
```

## Objective

Persist the 2026-08-16 official-client investigation into whether the exact researched native Linux Tibia client can load/render a larger world-map tile area than its currently observed range, while separating proven binary/runtime evidence from derived feasibility and still-unknown patch limits.

## Authorization and scope

Documentation/evidence only. This task may create or edit only:

```text
docs/agents/reports/OTCLIENT-20260816-official-client-map-viewport-feasibility.md
docs/agents/evidence/OTC-20260816-official-client-map-viewport-feasibility/**
docs/agents/tasks/active/OTC-20260816-official-client-map-viewport-feasibility.md
docs/agents/tasks/archive/OTC-20260816-official-client-map-viewport-feasibility.md
```

It does not own or mutate official-client runtime, client bytes, workflows, Track A controller/registration state, PR #300 coordinator paths, PR #303 runtime surfaces, PR #324 governance paths, Track B, Canary/Otheryn, proprietary assets, credentials, captures with private data, or owner-funded AI/API resources.

## Track A runtime boundary

Authority for this task comes from the trusted-base `AGENTS.md` hierarchy and `docs/agents/TIBIA_RESEARCH_TRACKS.md` on `main`, not from pending PR prose or unmerged governance.

```yaml
track_id: official-client-re
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
```

No live runtime operation is authorized or performed by this task.

## Exact researched client fence

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
```

A different official-client build is outside the evidence boundary until independently revalidated.

## Trusted evidence inputs

- `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md` on the base head, including the exact client fence and common-map static capture lead `0x19a8ea3`.
- Exact-binary static run `31892019505`, head `a3068a6a9460525cb1946186cf439caf7832e176`, successful; artifact `9248797952`, `track-a-p0-static-elf-31892019505`, digest `sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584`.
- Exact historical structural movement run `31806312967`, job `94785974126`, head `ff8ebc6e2c3a1604d90c2b0439b60af2258b578a`, successful; artifact `9221332209`, digest `sha256:bd4be5b2f9d6cebf19fff6bdfa3677ad57c00ae4a376987f32b42e8a27907a4a`.
- Historical workflow source at `ff8ebc6e2c3a1604d90c2b0439b60af2258b578a`: `.github/workflows/tibia-official-client-re-persistent-reversible-step.yml`, which records counts and newly observed map-provenance strips after one step and its inverse.
- Repository and open-PR state inspected on 2026-08-16 before mutation.

Untrusted/stale narrative, historical PIDs/PIE addresses, old display assumptions and chat-only conclusions do not upgrade evidence.

## Related live work / overlap boundary

- PR #300 owns Track A promotion/integration coordinator paths. This task does not edit its owned report/task/evidence or shared changelog/catalogue files.
- PR #303 owns its declared runtime-reacquisition surfaces. This task performs no runtime observation or mutation.
- PR #324 owns pending Track A runtime-agent governance. This task does not consume that unmerged PR as authority and does not edit its paths.
- PR #302 supplied the exact static-ELF artifact used as evidence; this task consumes it read-only.

## Delivery classification

```yaml
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
implementation_status: documentation_evidence_checkpoint
user_facing_feature_complete: false
```

## Acceptance inventory

1. A durable report records the exact official-client fence and provenance for every material finding. **PASS**
2. Exact-binary worldmap extent/storage/viewport/camera/protocol/render semantic evidence is preserved without committing client bytes. **PASS**
3. The current `18 x 14` interpretation is not promoted beyond retained evidence strength; raw-log retention limitations are explicit. **PASS**
4. Feasibility is classified as derived/high-confidence research direction, not implemented/proven patch support. **PASS**
5. Field offsets, fixed allocations, parser/serializer limits, renderer limits, server-side awareness requirements and maximum safe dimensions remain explicit UNKNOWNs. **PASS**
6. Candidate sizes distinguish linear dimension growth from tile-count growth. **PASS**
7. The next experiment starts with static field/callsite recovery; future live mutation requires then-current Track A authority/ownership gates. **PASS**
8. No proprietary binary/assets, credentials, private captures or personal data are committed. **PASS**
9. Documentation/path/diff audit passes; E2E is `NOT_APPLICABLE` for the documented reason. **PASS**
10. Required exact-head GitHub checks and terminal PR state are required before `completed`. **PENDING FINAL CI/MERGE**

## Current evidence state

```yaml
PROVEN:
  - exact researched client fence exists on canonical main documentation
  - exact static artifact/run identifiers verified through GitHub Actions metadata
  - selected worldmap/view/camera/storage/protocol/render semantic strings verified in the downloaded exact artifact text
  - historical reversible-step run/job/workflow logic verified
DERIVED:
  - separate worldmap extent/storage/viewport/camera/protocol/render concepts make a larger loaded/rendered area technically plausible
  - observed historical edge geometry is consistent with an 18_x_14 baseline, but the consumed downloadable artifact does not retain the raw TSV/job-log rows
UNKNOWN:
  - exact patch points and maximum safe viewport
  - whether all relevant buffers are dynamic
  - whether terrain-only expansion can be separated from live entity awareness in the exact client
  - current canonical live runtime state for any future mutation experiment
CONFLICT: []
```

## Fresh validator-role audit

```yaml
audit:
  result: PASS
  validator: chat-20260816-viewport-feasibility / validator role
  method:
    - reread trusted-base closeout, execution and Track A governance
    - inspect exact PR changed-path set and full relevant diff
    - recheck exact client/run/job/artifact provenance against primary GitHub metadata and downloaded artifact text
    - check claim-strength boundaries, ownership overlap, secrets/proprietary material, duplicate task PRs, reviews and threads
  findings:
    - id: OTC325-AUD-001
      severity: medium
      confidence: high
      evidence: initial task checkpoint before commit dbf3e88c3d8fa9fa721dc5cd913ddb287d946ad8
      impact: non-canonical v2 task/delivery classification and overly strong wording around pending PR #324 could mislead a later worker about authority
      disposition: fixed
      verification: remediated task record uses project_lane=otclient, task_kind=discovery, feature_scope.type=documentation and explicitly derives authority only from trusted main governance
  material_findings_open: 0
  informational_findings_open: 0
```

## Validation / PR hygiene

```yaml
focused_validation:
  changed_paths_reviewed: true
  full_pr_diff_reviewed: true
  provenance_rechecked_against_primary_github_metadata: true
  claim_strength_reviewed: true
  proprietary_or_secret_material_found: false
  ownership_overlap_found: false
component_validation:
  result: NOT_APPLICABLE
  reason: documentation/evidence-only change; no product/runtime code changed
e2e:
  result: NOT_APPLICABLE
  reason: documentation/evidence-only checkpoint; no executable or user-facing runtime behavior changed
pull_requests:
  related:
    - blakinio/otclient#325: current_delivery_pr
  duplicate_related_prs: 0
  unresolved_review_threads: 0
  requested_changes: 0
final_ci:
  state: PENDING
  head: to_be_frozen_by_this_closeout_commit
  required_checks: repository_required_exact_head_checks
post_merge:
  required: true
  action: archive this task and release branch/task ownership as the same entry-task lifecycle
```

## Anti-stall checkpoint

```yaml
invocation_started_at: 2026-08-16T08:31:00+02:00
last_progress_at: 2026-08-16T08:42:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
```

## Next action

Mark PR #325 ready, enable protected auto-merge if repository protection accepts it, and observe required exact-head CI/merge under the bounded terminal-CI contract; after merge, perform repository-mandated archival and ownership release.