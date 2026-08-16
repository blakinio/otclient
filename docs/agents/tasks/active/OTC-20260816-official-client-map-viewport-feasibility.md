# OTC-20260816 — official-client map viewport feasibility

```yaml
task_id: OTC-20260816-official-client-map-viewport-feasibility
track: official-client-re
repository: blakinio/otclient
task_kind: research_documentation
phase: documenting
status: ACTIVE
base_branch: main
base_head: 3a5568f36ebc326afd246d0d2da45b5d8eecabfa
branch: docs/OTC-20260816-official-client-map-viewport-feasibility
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
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

## Track A runtime admission

This task intentionally uses the fail-closed static/documentation class described by the pending runtime-admission governance in PR #324 so the record remains safe if that contract lands before this PR closes.

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

No live runtime operation is authorized by this task.

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

- PR #300 owns Track A promotion/integration coordinator paths. This task must not edit its owned report/task/evidence or shared changelog/catalogue files.
- PR #303 owns its declared runtime-reacquisition surfaces. This task performs no runtime observation or mutation.
- PR #324 owns Track A runtime-agent governance. This task is documentation-only and records `runtime_access: none`.
- PR #302 supplied the exact static-ELF artifact used as evidence; this task consumes it read-only.

## Feature scope

```yaml
feature_scope:
  type: internal_only
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
```

## Acceptance inventory

1. A durable report records the exact official-client fence and provenance for every material finding.
2. Exact-binary evidence for `TWorldMapExtent`, `TWorldMapSubfieldExtent`, `TWorldMapStorage`, `TWorldMapViewport`, `TWorldMapCamera`, `TWorldmapProtocolMessageHandler`, `TWorldMapRenderProvider`, `onCameraViewportChanged` and `TMapScaleFactor` is preserved without committing client bytes.
3. The current `18 x 14` interpretation is not promoted beyond the strength of its retained evidence; raw-log retention limitations are explicit.
4. Feasibility is classified as INFERENCE, not implemented/proven patch support.
5. Unknowns include field offsets, fixed allocations, parser/serializer limits, renderer limits, server-side awareness requirements and maximum safe dimensions.
6. Quantitative candidate sizes distinguish linear dimension growth from tile-count growth.
7. The next experiment is bounded and starts with static field/callsite recovery; any future live mutation must independently pass current Track A runtime admission and ownership gates.
8. No proprietary binary/assets, credentials, private captures or personal data are committed.
9. Documentation/path/diff audit passes; runtime E2E is `NOT_APPLICABLE_WITH_REASON`.
10. Required exact-head GitHub checks pass and the PR reaches an intentional terminal state.

## Validation plan

```yaml
focused:
  - exact path/content review
  - provenance and claim-strength review
  - link/identifier consistency review
component: documentation-only; no product compilation required by BUILD_TEST_MATRIX
fresh_audit: proportionate final diff/path/contradiction/privacy/PR-hygiene review
e2e: NOT_APPLICABLE_WITH_REASON: documentation-only evidence checkpoint; no runtime behavior changed
final_ci: required repository checks on exact final head
```

## Current state

```yaml
PROVEN:
  - exact researched client fence exists on canonical main documentation
  - exact static artifact/run identifiers verified
  - selected worldmap/view/camera/storage/protocol/render semantic strings verified in downloaded artifact text
  - historical reversible-step run/job and workflow logic verified
DERIVED:
  - separate worldmap extent/storage/viewport/camera/protocol/render types make a larger viewport technically plausible
UNKNOWN:
  - exact patch points and maximum safe viewport
  - whether all relevant buffers are dynamic
  - whether terrain-only expansion can be separated from live entity awareness in the exact client
  - current canonical live runtime state for a future mutation experiment
CONFLICT: []
```

## Next action

Create the durable report and compact non-proprietary evidence extract, review the full branch diff, then complete documentation-only audit/CI/PR closeout.