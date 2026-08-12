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

The helper never guesses a ground, item role or OTB ID. Any conflict or missing semantic mapping blocks the OTBM plan.

## Observation schema

Schema: `otclient.worldmap.observation.v1`

```json
{
  "schema": "otclient.worldmap.observation.v1",
  "observations": [
    {
      "position": {"x": 32000, "y": 32001, "z": 7},
      "contents": [100, 200, 300],
      "provenance": {"source": "bounded-runtime-capture", "capture_id": "example"}
    }
  ]
}
```

`contents` preserves the order observed in the decoded field message. IDs are client-side appearance/content IDs until an explicit mapping proves otherwise.

## Appearance-role catalog

Schema: `otclient.worldmap.appearance-catalog.v1`

```json
{
  "schema": "otclient.worldmap.appearance-catalog.v1",
  "appearances": [
    {"client_id": 100, "roles": ["ground"]},
    {"client_id": 200, "roles": ["border", "static"]},
    {"client_id": 900, "roles": ["creature", "dynamic"]}
  ]
}
```

Allowed roles are `ground`, `border`, `static`, `dynamic`, `creature`, `npc`, and `unknown`.

Role assignment must come from separately verified appearance metadata or equivalent producer evidence. The helper intentionally contains no hard-coded assertion that a proprietary field name, offset or numeric value has a particular meaning.

## OTB mapping

Schema: `otclient.worldmap.otb-mapping.v1`

```json
{
  "schema": "otclient.worldmap.otb-mapping.v1",
  "mappings": [
    {"client_id": 100, "otb_id": 1100},
    {"client_id": 200, "otb_id": 1200}
  ]
}
```

Mappings are version-sensitive evidence. A client ID is never assumed to equal an OTB/server ID.

## Reference map

Schema: `otclient.worldmap.reference.v1`

```json
{
  "schema": "otclient.worldmap.reference.v1",
  "tiles": [
    {
      "position": {"x": 32000, "y": 32001, "z": 7},
      "ground_otb_id": 1100,
      "static_otb_ids": [1200, 1300]
    }
  ]
}
```

CrystalServer, Renemap and TibiaMaps must each be normalized independently into this schema. Keep source identity/provenance outside the tile payload or in a surrounding evidence manifest; disagreement between sources is evidence, not permission to pick one silently.

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

`plan-otbm` emits only a neutral export plan. It does not write the binary OTBM container yet. The plan is exportable only if every included tile has one proven ground and all static IDs are mapped.

## Dynamic entities and spawns

Creature/NPC/dynamic roles are retained separately as `dynamic_client_ids` and are excluded from static OTBM item output by default. Observing a creature at a coordinate proves presence at that moment, not a spawn definition. Respawn radius, count and interval require repeated observations and a separate evidence model.

## Validation

Focused test command:

```bash
PYTHONPATH=. python3 tests/tools/tibia_worldmap_reconstruction/test_pipeline.py
```

The tests cover successful reconstruction/comparison/OTBM planning, conflicting captures, unresolved ground, unmapped IDs, stack-order differences and unknown appearance roles.
