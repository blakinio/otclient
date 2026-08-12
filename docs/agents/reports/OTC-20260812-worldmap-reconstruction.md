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
- PR #48 task evidence records official Linux client `15.32.df7b29` and the already decoded Worldmap boundary, including the common ordered map routine `0x19a8a80`.
- PR #277 preserves the earlier official-client runtime handover without adding proprietary material.
- Current reconstruction tooling is isolated from those operational paths and consumes only neutralized evidence.

### UNKNOWN until supplied as explicit evidence

- semantic classification of specific live client IDs such as `4407`, `313`, `6379`, `19394`, `6217`;
- exact official appearance field/flag that proves `ground`, `border`, static object, creature or NPC for the current client version;
- exact current client appearance ID -> OTB/server ID mapping;
- complete real map coverage;
- authoritative monster/NPC respawn definitions.

These unknowns are intentionally not filled from chat memory or numerical resemblance.

## Canonical reconstruction stages

### 1. Observation

Input records contain only:

```text
(x, y, z) -> ordered client content IDs + bounded provenance
```

Repeated observations of the same coordinate are merged only when their ordered contents agree. Distinct observed variants make the tile `CONFLICT`.

### 2. Appearance classification

A separate versioned appearance catalog assigns proven roles to client IDs:

- `ground` — candidate base floor for OTBM;
- `border` / `static` — static tile content;
- `dynamic`, `creature`, `npc` — observed dynamic presence, excluded from static OTBM output by default;
- `unknown` — unresolved and export-blocking.

The tool does not encode a proprietary flag-name/offset interpretation. An adapter may be added only after exact current-version evidence proves the mapping from official appearance metadata to these neutral roles.

### 3. Client ID -> OTB ID mapping

Mapping is a separate explicit evidence set:

```text
client appearance ID -> OTB/server item ID
```

No identity mapping is assumed. A missing mapping produces `UNMAPPED_ID` and blocks OTBM planning.

### 4. Static tile normalization

For each unambiguous observation the pipeline produces:

```text
position
ground_client_id
ground_otb_id
ordered static_client_ids
ordered static_otb_ids
dynamic_client_ids
unmapped_client_ids
unknown_role_client_ids
```

Exactly one proven ground candidate is required for a normal exportable tile.

### 5. Reference comparison

Every reference is normalized independently to:

```text
(x,y,z) -> ground_otb_id + ordered static_otb_ids
```

Planned comparison sources:

1. CrystalServer map/export;
2. Renemap export;
3. TibiaMaps-derived normalized reference where legally/technically available.

No source wins by default. Differences remain source-specific evidence.

Comparator statuses:

- `MATCH`;
- `NOT_OBSERVED`;
- `REFERENCE_MISSING`;
- `GROUND_MISMATCH`;
- `CONTENT_MISMATCH`;
- `STACK_ORDER_MISMATCH`;
- `UNMAPPED_ID`;
- `CONFLICT`.

This allows later reporting such as: observed official-client tile matches CrystalServer but differs from Renemap, or is absent from one reference.

### 6. OTBM-ready plan

The current tool emits a neutral OTBM plan rather than binary OTBM bytes. Export is globally fail-closed when any included tile is unresolved. An exportable plan contains only:

```text
position
ground_otb_id
ordered static_otb_ids
```

A binary OTBM writer is a later mechanical consumer of this already validated plan and must not become the place where missing ground/item semantics are guessed.

## Environment/static elements coverage

Once appearance role and OTB mappings exist, the same tile observation supports reconstruction of:

- floor/ground;
- borders;
- walls;
- doors;
- trees, rocks, furniture and decorations;
- containers and static/interactable items represented in the tile contents;
- stack order for the observed static contents;
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

Respawn radius/count/timing require repeated observations across time and must carry confidence/evidence rather than being written directly from one sighting.

## Reference comparison policy

For every coordinate, preserve independent results for each reference. The later aggregate report should classify at least:

- observed and equal in all references;
- observed, CrystalServer missing/different;
- observed, Renemap missing/different;
- observed, TibiaMaps missing/different;
- not observed by the official-client capture yet;
- observed but blocked by unresolved appearance/OTB mapping;
- conflicting live observations.

This is the basis for identifying actual missing CrystalServer/Renemap regions rather than assuming a file is more complete because it contains more tiles.

## Security/licensing boundary

Repository artifacts must contain only neutralized IDs/coordinates and synthetic test fixtures unless redistribution rights for a source are separately established. Do not commit:

- official client binaries;
- downloaded proprietary appearance/sprite/sound/map asset bytes;
- credentials/session material;
- account/character identity;
- authenticated screenshots;
- raw private captures containing protected data.

## Implemented files

- `tools/tibia_worldmap_reconstruction/pipeline.py` — validation, deterministic merge, classification, ID translation, comparison and fail-closed OTBM planning;
- `tools/tibia_worldmap_reconstruction/cli.py` — `reconstruct`, `compare`, `plan-otbm` commands;
- `tools/tibia_worldmap_reconstruction/README.md` — schemas and operator contract;
- `tests/tools/tibia_worldmap_reconstruction/test_pipeline.py` — focused synthetic pipeline coverage.

## Validation evidence

A local sandbox prototype using the same implementation content passed:

```text
PYTHONPATH=. python3 tests/tools/tibia_worldmap_reconstruction/test_pipeline.py
......
Ran 6 tests
OK
```

The exact files committed to Git must still be fetched/checked and exercised again before terminal completion, followed by the live repository PR check graph.

## Remaining real-world inputs

Tooling is prepared. Real reconstruction requires two evidence producers, neither of which may be guessed inside this task:

1. `observations.json` from a bounded decoded Worldmap capture owned/coordinated with PR #48;
2. current-version appearance-role + client-to-OTB mapping evidence.

Once those are supplied, the existing CLI can generate a normalized snapshot, source-specific diffs and an OTBM-ready plan immediately.
