# Tibia worldmap reconstruction helper

Task-scoped, fail-closed tooling for `OTC-20260812-worldmap-reconstruction`.

This directory does **not** contain Tibia assets, captures, credentials, account/character data or proprietary bytes. It consumes neutral JSON prepared from separately authorized evidence.

## Pipeline

```text
bounded live observations
  -> appearance-role catalog
  -> explicit client-id -> OTB-id mapping
  -> normalized snapshot
  -> reference diff
  -> OTBM-ready plan
```

The helper never guesses a ground, item role or OTB ID. Any conflict, version mismatch or missing semantic mapping blocks the relevant stage.

## Observation schema

Schema: `otclient.worldmap.observation.v1`

```json
{
  "schema": "otclient.worldmap.observation.v1",
  "client_version": "15.32.df7b29",
  "observations": [
    {
      "position": {"x": 32000, "y": 32001, "z": 7},
      "contents": [100, 200, 300],
      "provenance": {"source": "bounded-runtime-capture", "capture_id": "example"}
    }
  ]
}
```

`contents` preserves the order observed in the decoded field message. IDs are client-side appearance/content IDs until an explicit mapping proves otherwise. Every observation requires bounded provenance and the exact client version.

## Appearance-role catalog

Schema: `otclient.worldmap.appearance-catalog.v1`

```json
{
  "schema": "otclient.worldmap.appearance-catalog.v1",
  "client_version": "15.32.df7b29",
  "appearances": [
    {"client_id": 100, "roles": ["ground"], "evidence": "verified appearance metadata reference"},
    {"client_id": 200, "roles": ["border", "static"], "evidence": "verified appearance metadata reference"},
    {"client_id": 900, "roles": ["creature", "dynamic"], "evidence": "verified appearance metadata reference"}
  ]
}
```

Allowed roles are `ground`, `border`, `static`, `dynamic`, `creature`, `npc`, and `unknown`. Contradictory combinations such as `ground + creature`, `static + dynamic`, or `unknown + anything` are rejected.

Role assignment must come from separately verified appearance metadata or equivalent producer evidence. Every entry requires a non-empty `evidence` string. The helper intentionally contains no hard-coded assertion that a proprietary field name, offset or numeric value has a particular meaning.

## OTB mapping

Schema: `otclient.worldmap.otb-mapping.v1`

```json
{
  "schema": "otclient.worldmap.otb-mapping.v1",
  "client_version": "15.32.df7b29",
  "otb_version": "target-otb-version",
  "mappings": [
    {"client_id": 100, "otb_id": 1100, "evidence": "verified mapping source"},
    {"client_id": 200, "otb_id": 1200, "evidence": "verified mapping source"}
  ]
}
```

Mappings are version-sensitive evidence. Every mapping requires explicit evidence. A client ID is never assumed to equal an OTB/server ID, and the observation/catalog/mapping client versions must match exactly.

## Snapshot trust boundary

The snapshot is a deterministic **intermediate artifact**, not a cryptographically authenticated evidence envelope.

`validate_snapshot()` fail-closes malformed and internally inconsistent snapshot state. For an `OK` tile it verifies, among other things:

- exactly one observed variant exists;
- the ground client ID occurs exactly once in that variant;
- ground/static/dynamic client-ID roles do not overlap;
- every observed client ID is accounted for by ground/static/dynamic fields with matching multiplicity;
- static and dynamic client-ID ordering agrees with the observed variant;
- unresolved IDs are absent and static client/OTB arrays have matching lengths.

This prevents a caller from taking an observed variant and independently forging a contradictory `status=OK` projection that the planner would export.

It does **not** prove the external provenance of a fully self-consistent snapshot or cryptographically authenticate its OTB IDs. The authoritative evidence chain remains:

```text
trusted observations + verified appearance catalog + verified mapping
-> reconstruct()
-> validated snapshot
```

Do not accept an arbitrary third-party/manual snapshot as proof that a mapping was verified merely because it passes structural validation. If an untrusted handoff boundary is introduced later, add an authenticated evidence envelope or revalidate against the original catalog/mapping inputs rather than overstating what the snapshot schema proves.

## Reference map

Schema: `otclient.worldmap.reference.v1`

```json
{
  "schema": "otclient.worldmap.reference.v1",
  "source": "crystalserver",
  "otb_version": "target-otb-version",
  "tiles": [
    {
      "position": {"x": 32000, "y": 32001, "z": 7},
      "ground_otb_id": 1100,
      "static_otb_ids": [1200, 1300]
    }
  ]
}
```

CrystalServer, Renemap and TibiaMaps must each be normalized independently into this schema. Their source identities stay explicit. Duplicate coordinates are rejected, and the reference OTB version must match the reconstructed snapshot.

## Commands

Run from repository root:

```bash
python -m tools.tibia_worldmap_reconstruction.cli reconstruct \
  --observations observations.json \
  --catalog appearance-catalog.json \
  --mapping otb-mapping.json \
  --output snapshot.json

python -m tools.tibia_worldmap_reconstruction.cli compare \
  --snapshot snapshot.json \
  --reference crystalserver-reference.json \
  --output crystalserver-diff.json

python -m tools.tibia_worldmap_reconstruction.cli plan-otbm \
  --snapshot snapshot.json \
  --output otbm-plan.json
```

`plan-otbm` emits only a neutral export plan. It does not write the binary OTBM container yet. The plan is exportable only when at least one tile exists, every included tile has one structurally consistent mapped ground, all static IDs are mapped, no unresolved/conflicting state remains, and the snapshot was produced through the trusted evidence pipeline described above.

## Comparator statuses

The comparator preserves unresolved states instead of accidentally reporting a match. It may report:

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

## Dynamic entities and spawns

Creature/NPC/dynamic roles are retained separately as `dynamic_client_ids` and are excluded from static OTBM item output by default. Observing a creature at a coordinate proves presence at that moment, not a spawn definition. Respawn radius, count and interval require repeated observations and a separate evidence model.

## Validation

Focused test command:

```bash
PYTHONPATH=. python3 tests/tools/tibia_worldmap_reconstruction/test_pipeline.py
```

The focused suite covers successful reconstruction/comparison/OTBM planning, conflicting captures, unresolved ground, unmapped IDs, stack-order differences, unknown appearance roles, malformed/missing provenance, contradictory roles, conflicting mappings, client/OTB version mismatches, empty-plan rejection, malformed snapshot/reference types and inconsistent forged-`OK` snapshot projections.
