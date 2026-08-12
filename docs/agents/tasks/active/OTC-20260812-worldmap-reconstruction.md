---
task_id: OTC-20260812-worldmap-reconstruction
status: validating
branch: feat/OTC-20260812-worldmap-reconstruction
base_branch: main
created: 2026-08-12
updated: 2026-08-12
related_pr: "#279"
owned_paths:
  - docs/agents/tasks/active/OTC-20260812-worldmap-reconstruction.md
  - docs/agents/reports/OTC-20260812-worldmap-reconstruction.md
  - tools/tibia_worldmap_reconstruction/**
  - tests/tools/tibia_worldmap_reconstruction/**
reuses:
  - PR #48 runtime/login evidence and official-client package reconstruction helpers as read-only evidence
  - PR #277 official-client runtime handover as read-only evidence
depends_on:
  - PR #48 only for future real official-client capture; this task does not edit PR #48 paths
blocks: []
---

# OTC-20260812 — Worldmap reconstruction tooling

## Objective

Prepare a deterministic, fail-closed pipeline in `blakinio/otclient` that can ingest bounded live tile observations from the official client, classify tile contents from separately supplied appearance evidence, map client appearance IDs to server/OTB IDs when proven, compare reconstructed tiles against reference maps, and emit an OTBM-ready plan without guessing missing mappings.

## Authorization and scope

Allowed:

- repository-only tooling, tests and documentation in the owned paths above;
- read-only use of PR #48 and PR #277 evidence;
- neutral JSON schemas and synthetic fixtures;
- comparison against normalized reference exports supplied later by the owner.

Forbidden:

- edits to PR #48 operational scripts/workflows/task paths;
- use of Codex or owner-funded AI/API quota;
- credentials, account/character data, authenticated screenshots, proprietary client binaries/assets or extracted proprietary bytes in Git;
- bypassing anti-cheat/security checks or modifying the official client;
- claiming an appearance/OTB mapping that was not proven by supplied metadata/evidence.

## Feature scope

```yaml
feature_scope:
  type: data_pipeline
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: internal_only
```

The E2E for this task is the neutral repository pipeline: observation -> classification -> mapping -> comparison -> OTBM-ready plan. A real official-client capture remains a separately coordinated runtime evidence producer and is not needed to prove this tooling implementation.

## Acceptance inventory

1. Observation records bind `(x,y,z)`, ordered content IDs and provenance to an exact `client_version`.
2. Repeated observations merge deterministically and distinct variants become `CONFLICT`.
3. Appearance roles require explicit per-entry evidence; unknown or contradictory roles fail closed.
4. Client appearance ID -> OTB/server ID mapping requires explicit per-entry evidence plus exact client/OTB versions; unmapped IDs block export.
5. Observation/catalog/mapping client versions must match exactly.
6. Ground selection is fail-closed: exactly one proven ground candidate is required for an exportable tile.
7. Ordered static contents are preserved; dynamic entities remain separate and do not become static OTBM items by default.
8. Comparator preserves unresolved tile states and distinguishes match, missing reference/observation, ground/content/stack mismatches and unresolved mappings.
9. Reference comparisons require explicit source and matching `otb_version`; duplicate coordinates are rejected.
10. OTBM planning refuses conflicts, unknown roles, unresolved ground, unmapped IDs and empty snapshots.
11. Synthetic tests cover success plus malformed/missing provenance, conflicting observations/mappings/roles, missing ground, unmapped IDs, stack order and version mismatches.
12. Documentation defines CrystalServer, Renemap and TibiaMaps as independent normalized references; disagreements remain evidence rather than silent precedence.

## Evidence boundaries

### PROVEN

- `blakinio/otclient` `main` at task start: `9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f`.
- PR #48 is open/draft on `ci/OTC-20260727-tibia-linux-runner-analysis` and owns its operational workflows/scripts/task record.
- PR #277 is open/draft and contains only `docs/agents/tasks/active/OTC-20260812-official-client-runtime-handover.md`.
- PR #48 task record preserves official-client identity, decoded Worldmap handler/common routine addresses and strict no-OCR/WARP safety boundaries.
- no existing appearance/OTB reconstruction helper was found in current `blakinio/otclient` code search before adding this task-scoped utility.

### UNKNOWN / requires later evidence

- exact semantic name of every official `AppearanceInstance` field/offset used by the proprietary client;
- classification of specific live IDs such as `4407`, `313`, `6379`, `19394`, `6217` unless supplied current-version appearance evidence proves it;
- exact client appearance ID -> OTB/server ID mapping for the current official version;
- complete real-world map coverage, creature/NPC spawn definitions and dynamic state.

## Validation record

```yaml
local_exact_blob_validation:
  pipeline_blob: 7fe70d87bcaa2ae97168b3d4db92ee55fc91547a
  test_blob: 4a83061528d4eaffbdfcca0c3bb01b5ebf2594d7
  result: PASS
focused_tests:
  command: PYTHONPATH=. python3 tests/tools/tibia_worldmap_reconstruction/test_pipeline.py
  tests: 12
  result: PASS
syntax:
  command: python3 -m py_compile tools/tibia_worldmap_reconstruction/pipeline.py tools/tibia_worldmap_reconstruction/cli.py
  result: PASS
synthetic_e2e:
  path: reconstruct -> compare -> plan-otbm
  result: PASS
  diff_status: MATCH
  exportable: true
pr: 279
pr_exact_head_ci: pending
```

No Codex or owner-funded AI/API quota was used.

## Related PR policy

- PR #48 remains intentionally open and independently owned; this task must not close or mutate it.
- PR #277 is a separate documentation handover and is not required for the correctness of this tool; do not close it from this task unless its lifecycle is handled separately.

## Checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-12T21:24:00+02:00
base_head: 9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f
branch: feat/OTC-20260812-worldmap-reconstruction
pr: 279
status: validating
proven:
  - non-overlapping ownership against PR #48 and PR #277
  - exact Git blobs match the locally tested implementation and test files
  - 12 focused tests, py_compile and synthetic CLI E2E pass
  - unresolved roles and version mismatches fail closed
unknown:
  - real appearance classifications and OTB mappings
conflicts: []
next_action: inspect exact-head PR #279 CI and full diff; repair any failure, then complete repository lifecycle
```
