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
  - repository-owned OTCLIENT-TIBIA-RE canonical evidence imports
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
- read-only use of PR #48 and repository-owned imported official-client evidence;
- neutral JSON schemas and synthetic fixtures;
- comparison against normalized reference exports supplied later by the owner.

Forbidden:

- edits to PR #48 operational scripts/workflows/task paths;
- use of Codex or owner-funded AI/API quota;
- credentials, account/character data, authenticated screenshots, proprietary client binaries/assets or extracted proprietary bytes in Git;
- claiming an appearance/OTB mapping that was not proven by supplied metadata/evidence;
- treating structural snapshot validation as cryptographic provenance authentication.

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
10. OTBM planning refuses conflicts, unknown roles, unresolved ground, unmapped IDs, malformed or internally inconsistent `OK` snapshots and empty snapshots.
11. Synthetic tests cover success plus malformed/missing provenance, conflicting observations/mappings/roles, missing ground, unmapped IDs, stack order, version mismatches, forged/inconsistent `OK` state, bad snapshot types/statuses, duplicate snapshot coordinates and malformed reference arrays.
12. Documentation defines CrystalServer, Renemap and TibiaMaps as independent normalized references; disagreements remain evidence rather than silent precedence.
13. Snapshot validation is explicitly bounded to schema/internal consistency; an arbitrary self-consistent snapshot is not treated as authenticated proof of mapping provenance.

## Evidence boundaries

### PROVEN

- `blakinio/otclient` `main` at task start: `9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f`.
- PR #48 is open/draft on `ci/OTC-20260727-tibia-linux-runner-analysis` and owns its operational workflows/scripts/task record.
- PR #48 and the canonical OTCLIENT-TIBIA-RE reports preserve official-client identity, decoded Worldmap evidence and strict no-OCR/WARP boundaries.
- no existing appearance/OTB reconstruction helper was found before adding this task-scoped utility.

### UNKNOWN / requires later evidence

- exact semantic name of every official `AppearanceInstance` field/offset;
- classification of specific live client IDs unless current-version appearance evidence proves it;
- exact client appearance ID -> OTB/server ID mapping for the current official version;
- complete real-world map coverage, creature/NPC spawn definitions and dynamic state;
- cryptographic authenticity of an arbitrary externally supplied snapshot/mapping document; the current tool validates structure and explicit evidence fields, not signatures.

## Fresh post-implementation audit — finding OTC279-AUD-001

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
- `compare()` and `build_otbm_plan()` validate the snapshot before use;
- `OK` requires exactly one observed variant, mapped ground, no unresolved IDs and matching static client/OTB lengths;
- conflict/unmapped/unknown-role statuses must contain evidence consistent with that status;
- duplicate snapshot coordinates, unsupported statuses, malformed types and malformed reference arrays fail closed;
- seven regression cases increased the focused suite to 19 tests.

## Fresh closeout audit — finding OTC279-AUD-002

A second independent diff/code audit found that the first repair still did not bind the decomposed fields of an `OK` tile back to `observed_variants`.

```yaml
severity: high
confidence: high
finding: OTC279-AUD-002
impact: a caller could keep status=OK while replacing observed_variants or independently changing ground/static/dynamic client-ID projections; the planner could then export a structurally contradictory snapshot
status: fixed
repair_commits:
  - eba161284a3d9444cca6cbeac3e5e5164dd250a7
  - 08704e2412a342e3e1618d9985d3d45801ea29c5
validation_workflow_head: 7427fe1676cdb64eb7293229ee32c8a69c0cf0dd
validation_run: 31681045961
validation_job: 94386320196
result: PASS
```

Second repair:

- `OK` ground must occur exactly once in its single observed variant;
- ground/static/dynamic client-ID roles may not overlap;
- the multiset of `ground + static + dynamic` must account for the entire observed variant;
- static and dynamic client-ID order must be the order projected from the observed variant;
- four regression cases cover variant mismatch, static-order mismatch, dynamic projection mismatch and role overlap;
- focused suite now passes 23/23;
- Python syntax validation passes;
- synthetic CLI `reconstruct -> compare -> plan-otbm` E2E passes with `SYNTHETIC_RECONSTRUCT_COMPARE_PLAN_PASS=true`.

The temporary second-audit validation workflow was removed by commit `4e03c5b7ed6578af9fbfd2cdeb240acb8e109c1f` after the proof.

## Snapshot provenance boundary

The snapshot format is an intermediate representation. Internal validation proves that a snapshot is structurally self-consistent; it does not cryptographically prove who produced it or that a fully self-consistent manually supplied OTB ID originated from the verified mapping document.

The authoritative pipeline remains:

```text
trusted bounded observations
+ verified appearance-role catalog
+ verified client->OTB mapping
-> reconstruct()
-> structurally validated snapshot
-> compare()/plan-otbm
```

If a future design accepts snapshots across an untrusted handoff boundary, add an authenticated evidence envelope or revalidate them against their original catalog/mapping inputs. Do not claim the current schema alone prevents a malicious party from fabricating an entirely self-consistent document.

## Validation record

```yaml
baseline_before_fresh_audit:
  focused_tests: 12 PASS
  syntax: PASS
  synthetic_e2e: PASS
  repository_ci_run: 31632613373 PASS
first_audit_repair:
  validation_run: 31653654639
  validation_job: 94303192632
  focused_tests: PASS_19_OF_19
  syntax: PASS
  synthetic_e2e: PASS
second_audit_repair:
  pipeline_commit: eba161284a3d9444cca6cbeac3e5e5164dd250a7
  regression_commit: 08704e2412a342e3e1618d9985d3d45801ea29c5
  validation_workflow_head: 7427fe1676cdb64eb7293229ee32c8a69c0cf0dd
  validation_run: 31681045961
  validation_job: 94386320196
  focused_tests: PASS_23_OF_23
  syntax: PASS
  synthetic_e2e: PASS
  synthetic_marker: SYNTHETIC_RECONSTRUCT_COMPARE_PLAN_PASS=true
  temporary_validation_workflow_removed_by: 4e03c5b7ed6578af9fbfd2cdeb240acb8e109c1f
pr: 279
final_required_ci: pending on final workflow-free documentation/code head
```

No Codex or owner-funded AI/API quota was used. All material work is persisted in `blakinio/otclient`.

## Related PR policy

- PR #48 remains intentionally open and independently owned; this task must not close or mutate it.
- Runtime/dedicated-runner waiting does not block merging this neutral repository pipeline because its required E2E is synthetic and explicitly internal-only; real capture is a later evidence producer input.

## Checkpoint

```yaml
checkpoint_version: 5
updated_at: 2026-08-13T10:15:00+02:00
branch: feat/OTC-20260812-worldmap-reconstruction
pr: 279
status: validating
proven:
  - first and second fail-closed snapshot repairs implemented
  - focused repaired suite passed 23/23 on exact repair head
  - Python syntax validation passed
  - synthetic CLI reconstruct -> compare -> plan-otbm E2E passed
  - snapshot trust/provenance boundary is documented without overclaiming authentication
  - temporary second-audit validation workflow was removed
unknown:
  - final required repository CI result on the final workflow-free head
  - real appearance classifications and OTB mappings
  - real official-client capture integration inputs
conflicts: []
blockers: []
next_action: verify final exact-head repository CI, full diff and review hygiene; merge PR #279 if every closeout gate passes, then archive the completed tooling task separately
```
