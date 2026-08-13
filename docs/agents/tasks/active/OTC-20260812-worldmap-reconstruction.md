---
task_id: OTC-20260812-worldmap-reconstruction
status: validating
branch: feat/OTC-20260812-worldmap-reconstruction
base_branch: main
created: 2026-08-12
updated: 2026-08-13
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
10. OTBM planning refuses conflicts, unknown roles, unresolved ground, unmapped IDs, malformed/forged snapshots and empty snapshots.
11. Synthetic tests cover success plus malformed/missing provenance, conflicting observations/mappings/roles, missing ground, unmapped IDs, stack order, version mismatches, forged `OK` state, bad snapshot types/statuses, duplicate snapshot coordinates and malformed reference arrays.
12. Documentation defines CrystalServer, Renemap and TibiaMaps as independent normalized references; disagreements remain evidence rather than silent precedence.

## Evidence boundaries

### PROVEN

- `blakinio/otclient` `main` at task start: `9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f`.
- PR #48 is open/draft on `ci/OTC-20260727-tibia-linux-runner-analysis` and owns its operational workflows/scripts/task record.
- PR #277 is open/draft and contains only its official-client runtime handover.
- PR #48 task record preserves official-client identity, decoded Worldmap handler/common routine addresses and strict no-OCR/WARP boundaries.
- no existing appearance/OTB reconstruction helper was found before adding this task-scoped utility.

### UNKNOWN / requires later evidence

- exact semantic name of every official `AppearanceInstance` field/offset;
- classification of specific live client IDs unless current-version appearance evidence proves it;
- exact client appearance ID -> OTB/server ID mapping for the current official version;
- complete real-world map coverage, creature/NPC spawn definitions and dynamic state.

## Fresh post-implementation audit — 2026-08-13

Finding `OTC279-AUD-001`:

```yaml
severity: high
confidence: high
evidence: tools/tibia_worldmap_reconstruction/pipeline.py compare() and build_otbm_plan() accepted caller-supplied snapshot tile fields without a complete snapshot validator
impact: a forged status=OK snapshot could carry malformed/unresolved values into comparison or an OTBM-ready plan
status: fixed
repair_commits:
  - d0c30b9218c15c359e5de7e901882ca7243b31b2
  - bcd5dcd06d344cc2c66b4aabcca733a3d3609f33
verification:
  - run 31653654639 job 94303192632 PASS
```

Repair:

- added strict `validate_snapshot()` and integer-array/optional-integer validators;
- `compare()` and `build_otbm_plan()` now validate the snapshot before use;
- `OK` requires exactly one observed variant, mapped ground, no unresolved IDs and matching static client/OTB lengths;
- conflict/unmapped/unknown-role statuses must contain evidence consistent with that status;
- duplicate snapshot coordinates, unsupported statuses, malformed types and malformed reference arrays fail closed;
- seven new regression cases were added, making the focused suite 19 tests.

## Validation record

```yaml
baseline_before_fresh_audit:
  focused_tests: 12 PASS
  syntax: PASS
  synthetic_e2e: PASS
  repository_ci_run: 31632613373 PASS
  note: superseded as final evidence by the fresh-audit repair
fresh_audit_repair:
  pipeline_commit: d0c30b9218c15c359e5de7e901882ca7243b31b2
  regression_commit: bcd5dcd06d344cc2c66b4aabcca733a3d3609f33
  validation_workflow_head: 9f5c69391d656d1b65c7f29b21f205d3360c12e3
  validation_run: 31653654639
  validation_job: 94303192632
  focused_tests: PASS_19_OF_19
  syntax: PASS
  synthetic_e2e: PASS
  synthetic_marker: SYNTHETIC_RECONSTRUCT_COMPARE_PLAN_PASS=true
  temporary_validation_workflow_removed_by: e447a31431b675effeb419892a35d7f22e5d321d
pr: 279
final_required_ci: pending on the final head after this checkpoint
```

The temporary validation workflow is no longer in the branch. The validation run remains supporting exact-code evidence; repository-required final CI must still pass on the final workflow-free head.

No Codex or owner-funded AI/API quota was used.

## Related PR policy

- PR #48 remains intentionally open and independently owned; this task must not close or mutate it.
- PR #277 is a separate documentation handover and is not required for correctness of this tool.

## Checkpoint

```yaml
checkpoint_version: 4
updated_at: 2026-08-13T02:15:00+02:00
branch: feat/OTC-20260812-worldmap-reconstruction
pr: 279
status: validating
proven:
  - fail-closed snapshot validation repair is implemented
  - focused repaired suite passed 19/19
  - Python syntax validation passed
  - synthetic CLI reconstruct -> compare -> plan-otbm E2E passed
  - temporary validation workflow was removed
unknown:
  - final required repository CI result on the workflow-free final head
  - independent fresh-context closeout audit availability
  - real appearance classifications and OTB mappings
conflicts: []
blockers: []
next_action: verify final exact-head repository CI, then complete fresh-context audit/PR hygiene and merge only if every closeout gate passes
```
