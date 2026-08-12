---
task_id: OTC-20260812-worldmap-reconstruction
status: implementing
branch: feat/OTC-20260812-worldmap-reconstruction
base_branch: main
created: 2026-08-12
updated: 2026-08-12
related_pr: pending
owned_paths:
  - docs/agents/tasks/active/OTC-20260812-worldmap-reconstruction.md
  - docs/agents/reports/OTC-20260812-worldmap-reconstruction.md
  - tools/tibia-worldmap-reconstruction/**
  - tests/tools/tibia-worldmap-reconstruction/**
reuses:
  - PR #48 runtime/login evidence and official-client package reconstruction helpers as read-only evidence
  - PR #277 official-client runtime handover as read-only evidence until superseded or merged
depends_on:
  - PR #48 for any future live official-client capture; this task does not edit PR #48 paths
blocks: []
---

# OTC-20260812 — Worldmap reconstruction tooling

## Objective

Prepare a deterministic, fail-closed pipeline in `blakinio/otclient` that can ingest bounded live tile observations from the official client, classify tile contents from separately supplied appearance metadata, map client appearance IDs to server/OTB IDs when proven, compare reconstructed tiles against reference maps, and emit an OTBM-ready plan without guessing missing mappings.

## Authorization and scope

Allowed:

- repository-only tooling, tests and documentation in the owned paths above;
- read-only use of PR #48 and PR #277 evidence;
- neutral JSON/JSONL schemas and synthetic fixtures;
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

The E2E for this task is synthetic/neutral pipeline E2E: capture -> classify -> map -> compare -> OTBM plan. A real official-client capture remains owned by PR #48 or a separately coordinated successor and is not required to prove this repository tooling itself.

## Acceptance inventory

1. A versioned neutral observation schema stores `(x,y,z)`, ordered content IDs and provenance without secrets.
2. Repeated observations merge deterministically and conflicts remain explicit rather than silently overwritten.
3. Appearance classification is derived only from supplied metadata; unknown metadata remains `UNKNOWN`.
4. Client appearance ID -> OTB/server ID translation is explicit and versioned; unmapped IDs block OTBM export.
5. Ground selection is fail-closed: exactly one proven ground candidate is required for an exportable tile unless the reference format explicitly represents no-ground tiles.
6. Ordered static contents are preserved; dynamic entities can be retained separately without becoming static OTBM items by default.
7. Comparator reports `MATCH`, `NOT_OBSERVED`, `GROUND_MISMATCH`, `CONTENT_MISMATCH`, `STACK_ORDER_MISMATCH`, `UNMAPPED_ID`, and `CONFLICT` with coordinates.
8. OTBM planning refuses unresolved ground, unresolved ID mappings or capture conflicts.
9. Synthetic tests cover successful E2E plus malformed input, conflicting observations, missing ground, unmapped IDs and stack-order differences.
10. Documentation defines later comparison targets: CrystalServer, Renemap and TibiaMaps normalized into the same neutral tile model; no source is silently treated as authoritative when they disagree.

## Evidence boundaries

### PROVEN

- `blakinio/otclient` `main` at task start: `9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f`.
- PR #48 is open/draft on `ci/OTC-20260727-tibia-linux-runner-analysis` and owns its operational workflows/scripts/task record.
- PR #277 is open/draft and contains only `docs/agents/tasks/active/OTC-20260812-official-client-runtime-handover.md`.
- PR #48 task record preserves official-client identity, decoded Worldmap handler/common routine addresses and strict no-OCR/WARP safety boundaries.

### UNKNOWN / requires later evidence

- exact semantic name of every official `AppearanceInstance` field/offset used by the proprietary client;
- classification of specific live IDs such as `4407`, `313`, `6379`, `19394`, `6217` unless supplied official appearance metadata proves it;
- exact client appearance ID -> OTB/server ID mapping for the current official version;
- complete real-world map coverage, creature/NPC spawn definitions and dynamic state.

## Validation plan

- local/sandbox Python syntax and unit tests for the exact files written to Git;
- synthetic full pipeline E2E;
- full PR diff review;
- exact-head repository CI required by live PR graph;
- no Codex/funded-AI review; if repository policy requires an unavailable funded reviewer, record the blocker rather than consuming quota.

## Related PR policy

- PR #48 remains intentionally open and independently owned; this task must not close or mutate it.
- PR #277 may be closed as superseded only after this task preserves its useful handover evidence or links it durably.

## Checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-12T21:07:00+02:00
base_head: 9e68388c5dff5d803f2a7025ba138e7cdfdf0d3f
branch: feat/OTC-20260812-worldmap-reconstruction
status: implementing
proven:
  - non-overlapping ownership against PR #48 and PR #277
  - repository-only scope and no owner-funded AI authorization
unknown:
  - real appearance classifications and OTB mappings
conflicts: []
next_action: implement and validate the neutral reconstruction/comparison/OTBM-plan pipeline with synthetic E2E evidence
```
