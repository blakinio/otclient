# OTC-20260812 — worldmap reconstruction evidence pipeline

## Status

`IMPLEMENTED_TOOLING / REAL_CAPTURE_PENDING`

Repository: `blakinio/otclient`

Task: `docs/agents/tasks/active/OTC-20260812-worldmap-reconstruction.md`

Tool: `tools/tibia_worldmap_reconstruction/`

## Goal

Provide one durable pipeline that can turn separately authorized decoded official-client tile observations into a normalized reconstruction, compare that reconstruction with multiple map references, and produce an OTBM-ready static-tile plan without guessing missing semantics.

## Source hierarchy

### PROVEN repository/runtime evidence

- PR #48 is the live OTClient-owned official-client operational task and owns its runtime workflows/scripts.
- PR #48/canonical OTCLIENT-TIBIA-RE evidence records official Linux client `15.32.df7b29` and the decoded Worldmap boundary, including common ordered map routine `0x19a8a80` for that exact researched binary.
- Current reconstruction tooling is isolated from runtime operational paths and consumes only neutralized evidence.
- All material work/state for this pipeline is persisted in `blakinio/otclient`.

### UNKNOWN until supplied as explicit evidence

- semantic classification of specific live client IDs such as `4407`, `313`, `6379`, `19394`, `6217`;
- exact official appearance field/flag that proves `ground`, `border`, static object, creature or NPC for the current client version;
- exact current client appearance ID -> OTB/server ID mapping;
- complete real map coverage;
- authoritative monster/NPC respawn definitions.

These unknowns are intentionally not filled from chat memory or numerical resemblance.

## Canonical reconstruction stages

### 1. Observation

Input records contain:

```text
exact client_version
(x, y, z) -> ordered client content IDs + bounded provenance
```

Each observation requires non-empty `source` and `capture_id` provenance. Repeated observations of the same coordinate are merged only when their ordered contents agree. Distinct observed variants make the tile `CONFLICT`.

### 2. Appearance classification

A separate versioned appearance catalog assigns proven roles to client IDs:

- `ground` — candidate base floor for OTBM;
- `border` / `static` — static tile content;
- `dynamic`, `creature`, `npc` — observed dynamic presence, excluded from static OTBM output by default;
- `unknown` — unresolved and export-blocking.

Every catalog entry requires an evidence reference. Contradictory semantic combinations are rejected. The tool does not encode an unproven proprietary flag-name/offset interpretation.

### 3. Client ID -> OTB ID mapping

Mapping is a separate explicit evidence set:

```text
client_version + target otb_version
client appearance ID -> OTB/server item ID + evidence
```

No identity mapping is assumed. A missing mapping produces `UNMAPPED_ID` and blocks OTBM planning. Observation, catalog and mapping client versions must match exactly.

### 4. Static tile normalization

For each unambiguous observation the pipeline produces:

```text
client_version
otb_version
position
ground_client_id
ground_otb_id
ordered static_client_ids
ordered static_otb_ids
dynamic_client_ids
unmapped_client_ids
unknown_role_client_ids
observed_variants
```

Exactly one proven ground candidate is required for a normal exportable tile.

### 5. Reference comparison

Every reference is normalized independently to:

```text
source + otb_version
(x,y,z) -> ground_otb_id + ordered static_otb_ids
```

Planned comparison sources:

1. CrystalServer map/export;
2. Renemap export;
3. TibiaMaps-derived normalized reference where legally/technically available.

No source wins by default. Differences remain source-specific evidence. Duplicate reference coordinates and OTB-version mismatches are rejected.

Comparator statuses include:

- `MATCH`;
- `NOT_OBSERVED`;
- `REFERENCE_MISSING`;
- `GROUND_MISMATCH`;
- `CONTENT_MISMATCH`;
- `STACK_ORDER_MISMATCH`;
- `UNMAPPED_ID`;
- `UNKNOWN_ROLE`;
- `GROUND_UNRESOLVED`;
- `CONFLICT`.

Unresolved tile status is propagated before equality checks.

### 6. OTBM-ready plan

The current tool emits a neutral OTBM plan rather than binary OTBM bytes. Export is globally fail-closed when any included tile is unresolved or the snapshot is empty. An exportable plan contains only:

```text
client_version
otb_version
position
ground_otb_id
ordered static_otb_ids
```

A binary OTBM writer is a later mechanical consumer of this validated plan and must not become the place where missing ground/item semantics are guessed.

## Snapshot structural/provenance boundary

`validate_snapshot()` validates **schema and internal consistency**. For `status=OK` it now requires:

- exactly one observed variant;
- a mapped ground with no unresolved IDs;
- ground exactly once in that observed variant;
- no overlap between ground/static/dynamic client-ID roles;
- the multiset of ground + static + dynamic IDs to account for the full observed variant;
- static and dynamic client-ID order to agree with the order projected from the observed variant;
- matching static client/OTB array lengths.

This blocks a contradictory caller-supplied `OK` projection from reaching comparison/planning.

It does **not** cryptographically authenticate a fully self-consistent arbitrary snapshot or independently prove that its OTB IDs came from the verified mapping file. The evidence-authoritative path remains:

```text
trusted observations + verified appearance catalog + verified mapping
-> reconstruct()
-> structurally validated snapshot
-> compare()/plan-otbm
```

If snapshots later cross an untrusted handoff boundary, add an authenticated envelope or revalidate them against the original mapping/catalog inputs instead of overstating the current format.

## Environment/static elements coverage

Once appearance-role and OTB mappings exist, the same tile observation supports reconstruction of:

- floor/ground;
- borders;
- walls;
- doors;
- trees, rocks, furniture and decorations;
- containers and static/interactable items represented in tile contents;
- observed static stack order;
- multiple z-levels as separately observed coordinates.

Dynamic entities are deliberately separated from static geometry.

## NPC and monster/spawn policy

A decoded creature/NPC on a tile may support an observation record for presence, identity/appearance and movement if those fields are separately proven. It does **not** by itself prove a spawn definition.

A later spawn-reconstruction model must distinguish:

```text
observed presence
observed appearance/disappearance
observed movement
candidate spawn origin
candidate spawn radius
candidate amount
candidate respawn interval
confirmed spawn definition
```

Respawn radius/count/timing require repeated observations across time and evidence.

## Reference comparison policy

For every coordinate, preserve independent results for each reference. The later aggregate report should classify at least:

- observed and equal in all references;
- observed, CrystalServer missing/different;
- observed, Renemap missing/different;
- observed, TibiaMaps missing/different;
- not observed by the official-client capture yet;
- observed but blocked by unresolved appearance/OTB mapping;
- conflicting live observations.

This avoids assuming a source is more complete merely because it contains more tiles.

## Security/licensing boundary

Repository artifacts must contain only neutralized IDs/coordinates and synthetic test fixtures unless redistribution rights for a source are separately established. Do not commit:

- official client binaries;
- downloaded proprietary appearance/sprite/sound/map asset bytes;
- credentials/session material;
- account/character identity;
- authenticated screenshots;
- raw private captures containing protected data.

## Implemented files

- `tools/tibia_worldmap_reconstruction/pipeline.py` — validation, version/evidence fencing, deterministic merge, classification, ID translation, snapshot consistency validation, comparison and fail-closed OTBM planning;
- `tools/tibia_worldmap_reconstruction/cli.py` — `reconstruct`, `compare`, `plan-otbm` commands;
- `tools/tibia_worldmap_reconstruction/README.md` — schemas, operator contract and snapshot trust boundary;
- `tests/tools/tibia_worldmap_reconstruction/test_pipeline.py` — focused synthetic pipeline coverage.

## Audit history

### OTC279-AUD-001 — caller-supplied snapshot validation gap

The original compare/plan paths trusted snapshot fields too much. Repair added `validate_snapshot()`, type/range/status constraints and first forged-`OK` regression coverage.

Evidence:

```yaml
repair_commits:
  - d0c30b9218c15c359e5de7e901882ca7243b31b2
  - bcd5dcd06d344cc2c66b4aabcca733a3d3609f33
validation_run: 31653654639
validation_job: 94303192632
focused_tests: PASS_19_OF_19
```

### OTC279-AUD-002 — `OK` projection not bound to observed variant

Fresh closeout review found that `status=OK`, `observed_variants`, ground/static/dynamic client IDs could still contradict each other while individually satisfying the first validator.

Repair:

```yaml
pipeline_commit: eba161284a3d9444cca6cbeac3e5e5164dd250a7
regression_commit: 08704e2412a342e3e1618d9985d3d45801ea29c5
validation_workflow_head: 7427fe1676cdb64eb7293229ee32c8a69c0cf0dd
validation_run: 31681045961
validation_job: 94386320196
focused_tests: PASS_23_OF_23
syntax: PASS
synthetic_e2e: PASS
synthetic_marker: SYNTHETIC_RECONSTRUCT_COMPARE_PLAN_PASS=true
workflow_removed_by: 4e03c5b7ed6578af9fbfd2cdeb240acb8e109c1f
```

The four added regression cases cover:

- observed variant mismatch;
- static client order mismatch;
- dynamic projection mismatch;
- static/dynamic role overlap.

## Current validation evidence

Exact second-audit workflow logs show:

```text
.......................
Ran 23 tests
OK
WORLDMAP_FOCUSED_VALIDATION_PASS=true
SYNTHETIC_RECONSTRUCT_COMPARE_PLAN_PASS=true
```

The temporary validation workflow was removed after the proof. Final repository-required CI on the workflow-free final documentation/code head remains the closeout gate.

No Codex or owner-funded AI/API quota was used.

## Remaining real-world inputs

Tooling is prepared. Real reconstruction still requires evidence producers that may not be guessed inside this task:

1. `observations.json` from a bounded decoded Worldmap capture owned/coordinated with PR #48 or an authorized successor;
2. current-version appearance-role evidence;
3. current-version client-to-OTB mapping evidence.

Once supplied, the CLI can generate normalized snapshots, source-specific diffs and an OTBM-ready plan. Full global coverage, binary OTBM serialization and spawn reconstruction are separate later evidence/consumer phases.
