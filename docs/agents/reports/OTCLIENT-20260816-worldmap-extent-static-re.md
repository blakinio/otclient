# OTCLIENT-TIBIA-RE — worldmap extent static dependency recovery

```yaml
report_date: 2026-08-16
repository: blakinio/otclient
track: official-client-re
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
subject: official native Linux Tibia client only
implementation_status: NOT_IMPLEMENTED
client_byte_mutation: NOT_PERFORMED
live_runtime_access: NOT_PERFORMED
static_classification: MORE_STATIC_RE_NEEDED
fresh_exact_binary_materialization: BLOCKED
retained_evidence_research_path: ACTIVE
```

## Result

Fresh GitHub-hosted staging of the exact `15.32.df7b29` executable remains blocked, but this no longer stops all static progress. Same-repository historical artifacts preserve raw strip rows, GDB event state, exact machine-code prefixes and a richer type census that were not consumed by the earlier feasibility report.

The task therefore remains active as `MORE_STATIC_RE_NEEDED`, not `BLOCKED`, while this retained evidence can still advance the dependency graph.

## Exact fence

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
```

No current runtime identity is inferred from historical PID/PIE/display/session data.

## Geometry evidence upgrade

Retained artifact `9227370490` (`track-a-persistent-provenance-dump`, run `31821458677`, head `f23e9df548859d11520bbd2983c0df4e9923c2e7`, digest `sha256:991f5c22a7ffc1d23c6597307a49728b363863a5acd6dd754bff1222404c8e2d`) contains 90 raw strip rows.

Direct facts:

```text
Z=7, Y=32502, class=0: X=32537..32554 -> 18 consecutive X
Z=7, Y=32516, class=0: X=32537..32554 -> 18 consecutive X
Y delta between those two groups: 14
```

This upgrades the raw counts/coordinate relationship to PROVEN. It does **not** yet prove that a `TWorldMapViewport` field literally stores width=18 and height=14.

```yaml
PROVEN:
  horizontal_sample_count: 18
  second_horizontal_sample_count: 18
  y_difference: 14
INFERENCE:
  geometry_consistent_with: 18_x_14
UNKNOWN:
  stored_dimension_fields: UNKNOWN
  inclusive_exclusive_semantics: UNKNOWN
```

## Retained map-event code leads

The same artifact records historical breakpoints under exact historical PIE base `0x5586665f8000`:

```text
0xcecc70  BP1 observer-assigned CreateOnMap
0xcecf40  BP2 observer-assigned ChangeOnMap
0xcd4e20  BP3 worldmap_partial_handler lead
0xcec8d0  BP4 viewport_shift_candidate_3 lead
0x19a8ea3 BP5 common_capture
```

The human-readable BP1/BP2 labels are proven as observer output, not independently recovered debug symbols; original state-local observer-source provenance remains unresolved.

The retained raw log contains 256-byte code prefixes at BP1/BP2. Offline disassembly directly proves:

### `0xcecc70` observer-assigned `CreateOnMap`

- reads event-like `+0x18`, `+0x20`, `+0x28`;
- loads owner-like `+0x10` and performs virtual dispatch through slot `+0xa0`;
- dereferences the secondary object from event-like `+0x20` and reads `+0x08`, `+0x28`, `+0x30`;
- contains direct-call leads `0x1b13c80`, `0x1ab4e50`;
- contains RIP-relative data leads `0x313a820`, `0x30874a8`, `0x2f615a0`, `0x314b480`.

### `0xcecf40` observer-assigned `ChangeOnMap`

- gates on `byte [event-like+0x10] & 1`;
- reads event-like `+0x18`, `+0x20`, `+0x28`;
- loads owner-like `+0x10` and performs the same virtual slot `+0xa0` dispatch;
- directly calls exact static leads `0x1822ec0` and `0xceca50`;
- later invokes a virtual function through slot `+0xf0` of a derived object;
- contains RIP-relative data leads `0x313a820`, `0x2f615a0`, `0x314b480`, `0x312faa8`.

These are exact retained-code facts. None of `+0x10/+0x18/+0x20/+0x28/+0x30` is promoted as a dimension field.

## Richer exact-static census

Retained artifact `9246756211` (`track-a-p0-static-elf-31883967070`, digest `sha256:2d3e423d05eef2e370e10c1dcc6afeab27ad2d3a04fe8ccfb2ba635575dabe74`) provides a broader exact string/type inventory.

It directly proves:

- `TWorldMapExtent`, `TWorldMapSubfieldExtent`, `TWorldMapViewport`, `TWorldMapStorage`;
- `TWorldmapProtocolMessageHandler`, `TWorldMapRenderProvider`, `TWorldMapCamera`, `TWorldMapPicker`;
- separate `std::shared_ptr` counted-control-block instantiations for storage, viewport, protocol handler, render provider, camera and picker;
- an instantiated `std::unordered_map<TWorldMapCoordinate, std::shared_ptr<TWorldMapTile>, ...>` and corresponding hash-node/shared tile/entity types;
- additional semantic surfaces including `TWorldMapSubfieldCoordinate`, `TWorldMapCalculateTileFunctionService`, `TWorldMapGetByteForStackPosition`, `TWorldMapGetCurrentCoordinate`, `TWorldMapGetItemPropertiesService`, `TCreatureHUDRenderProvider`, `TCreatureHUDOverlayController`, `TWorldMapGameActionProvider` and `TWorldMapGameActionHandler`.

**INFERENCE:** the target subsystems are likely separately allocated/shared-lifetime objects and the coordinate-to-shared-tile hash map is a strong backing-storage candidate. This makes a single global dimension integer controlling protocol/storage/render/camera/picking less plausible.

**UNKNOWN:** exact member ownership, object layout, map capacity/reserve/eviction rules and concrete dependency edges.

## Updated partial dependency graph

```text
retained event/update path
  0xcecc70 CreateOnMap label  ----\
                                  +-- shared owner+0x10 -> virtual slot +0xa0
  0xcecf40 ChangeOnMap label ----/    event +0x18/+0x20/+0x28
             |
             +--> exact common-helper lead 0xceca50
             +--> further consumers UNKNOWN

TWorldmapProtocolMessageHandler
             +--> semantic surface PROVEN
             +--> concrete edge to the retained event/update path UNKNOWN

TWorldMapStorage
             +--> semantic/shared-lifetime surface PROVEN
             +--> coordinate -> shared_ptr<TWorldMapTile> unordered_map STRONG_CANDIDATE
             +--> direct-member/capacity/eviction relationship UNKNOWN

TWorldMapExtent / TWorldMapSubfieldExtent / TWorldMapViewport
             +--> semantic identities PROVEN
             +--> concrete dimension fields/default writers UNKNOWN
             +--> relation to 0xceca50/0xcecc70/0xcecf40 UNKNOWN

TWorldMapRenderProvider / TWorldMapCamera / TWorldMapPicker
             +--> semantic/shared-lifetime surfaces PROVEN
             +--> extent/viewport field readers, clipping/culling/transforms UNKNOWN
```

## Current patch graph matrix

| Graph element | Status |
|---|---|
| target subsystem/type presence | PROVEN |
| separate shared-control-block instantiations | PROVEN for storage/viewport/protocol/render/camera/picker |
| raw 18-sample geometry and Y delta 14 | PROVEN |
| literal viewport width/height fields | UNKNOWN |
| map-event handler code prefixes | PROVEN for retained BP1/BP2 samples |
| shared owner+0x10 virtual slot +0xa0 path | PROVEN for BP1/BP2 prefixes |
| helper `0xceca50` involvement | PROVEN for BP2 prefix |
| protocol handler -> BP1/BP2 edge | UNKNOWN |
| storage hash map direct ownership | INFERENCE / UNKNOWN direct-member relation |
| constructor/default dimension writers | UNKNOWN |
| all material readers/writers | UNKNOWN |
| fixed arrays/capacities/loop bounds/masks | INCOMPLETE |
| protocol full-map/strip/floor parser assumptions | UNKNOWN |
| render iteration/clipping/culling | UNKNOWN |
| camera projection/scale coupling | UNKNOWN |
| picker bounds/screen-world transform | UNKNOWN |
| concrete patch sites | UNKNOWN |
| safe isolated-change consequence | UNKNOWN |

## Fresh exact-client input blocker

The existing hosted source failures remain valid:

- PR #310: DNS failure then HTTP 403;
- this task: run `31947523640`, job `95165795953`, same-URL Referer/compressed strategy -> `INPUT_BLOCKED`, artifact `9263709952`;
- independent P0 run `31947502633`, job `95165743019` -> same class of blocker, artifact `9263704543`.

No further blind HTTP variant is justified. Synology is not used as a static fallback.

## Next research frontier

Retained evidence remains useful. Next actions are:

1. recover/verify observer-source provenance for the `CreateOnMap`/`ChangeOnMap` labels;
2. correlate `0xceca50`, `0xcecc70`, `0xcecf40`, `0xcd4e20`, `0xcec8d0` with remaining retained disassembly/static artifacts;
3. recover typeinfo/vtable/control-block xrefs where prior artifacts contain sufficient relocation data;
4. inspect retained type/container census for fixed-allocation, coordinate-area and visibility clues;
5. only when retained evidence is exhausted, the unresolved fresh-executable staging remains the external static input blocker.

No GUI/runtime discriminator is currently required, and no client-byte mutation is authorized.