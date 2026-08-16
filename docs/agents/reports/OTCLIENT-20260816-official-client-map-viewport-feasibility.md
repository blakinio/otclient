# OTCLIENT-TIBIA-RE — official-client map viewport feasibility

```yaml
report_date: 2026-08-16
track: official-client-re
repository: blakinio/otclient
subject: official native Linux Tibia client only
research_mode: static_artifact_analysis_plus_historical_runtime_evidence_review
implementation_status: NOT_IMPLEMENTED
```

## Question

Can the official Tibia client used by Track A load/render more world-map tiles than the currently observed area, potentially several times more?

## Executive result

The current evidence supports **feasibility research**, not a completed patch.

```yaml
FACT:
  - the exact researched official client exposes distinct named worldmap extent, subfield-extent, storage, viewport, camera, protocol-handler and render-provider concepts
  - camera viewport-change and map-scale semantic names are present in the exact-binary analysis
  - the existing exact-SHA structural observer has captured edge/strip map updates during reversible movement
DERIVED_HIGH_CONFIDENCE:
  - increasing the loaded/rendered map area is technically plausible and is worth a targeted patch-point investigation
  - map storage/render/camera expansion may be separable from full live dynamic-entity awareness and should be studied as a separate axis
UNKNOWN:
  - exact width/height fields and patch sites
  - allocation/loop/parser limits
  - maximum safe dimensions
  - server-side willingness/ability to provide a larger live awareness area
  - whether terrain beyond live awareness can be rendered from retained/local map data without additional server state
NOT_PROVEN:
  - that any concrete larger size currently works
  - that a single constant change is sufficient
  - that the official server will send 2x-4x more live map state
```

The investigation therefore does **not** claim that `36 x 28` is already supported. It establishes a concrete, evidence-backed path for finding the real limit.

## Exact client evidence boundary

All official-client claims in this report are fenced to:

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
```

The canonical source is `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md`.

A different client version, size, SHA or platform requires fresh evidence. Historical PID/PIE/runtime addresses are not reusable.

## Static official-client findings

Exact-binary run `31892019505` completed successfully on head `a3068a6a9460525cb1946186cf439caf7832e176` and produced artifact:

```yaml
artifact_id: 9248797952
name: track-a-p0-static-elf-31892019505
digest: sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584
```

Selected semantic evidence from that artifact is preserved in:

`docs/agents/evidence/OTC-20260816-official-client-map-viewport-feasibility/20260816-evidence.md`

The exact analyzed binary contains names corresponding to:

- `tibia::worldmap::TWorldMapExtent`;
- `tibia::worldmap::TWorldMapSubfieldExtent`;
- `tibia::worldmap::TWorldMapStorage`;
- `tibia::worldmap::TWorldMapViewport`;
- `tibia::renderer::TWorldMapCamera`;
- `tibia::worldmap::TWorldmapProtocolMessageHandler`;
- `tibia::worldmap::TWorldMapRenderProvider`;
- `onCameraViewportChanged`;
- `TMapScaleFactor` / `MapScaleFactor`.

This is a materially stronger starting point than a blind search for literal `18` and `14`: it identifies the client subsystems whose constructors, fields, call sites and consumers must be traced.

### What this does and does not prove

**PROVEN:** the exact binary contains these separate semantic/type surfaces.

**NOT PROVEN:** the internal object layouts, the fields that store current dimensions, dynamic-versus-fixed allocation, execution order, or a public supported configuration knob.

The type separation is therefore an architectural lead, not evidence that one integer controls the entire map.

## Existing Worldmap capture lead

The canonical Track A state retains an exact-version static common-map capture lead:

```text
0x19a8ea3
```

Historical use of that lead decoded `(x,y,z)` plus ordered map contents. The static offset remains only a version-fenced lead; transient runtime addresses must never be reused.

This gives the programme an existing observation point for validating any future dimension change without inventing a new blind instrumentation strategy.

## Current 18 x 14 interpretation

Historical reversible-movement run `31806312967`, job `94785974126`, completed successfully on exact head `ff8ebc6e2c3a1604d90c2b0439b60af2258b578a`.

The workflow:

`.github/workflows/tibia-official-client-re-persistent-reversible-step.yml`

SHA-fenced the official client, captured one movement step and its inverse, counted structural observer events/strips and printed the newly appended map-provenance rows.

During the 2026-08-16 investigation the successful job output showed:

```text
TRACK_A_STRIP_COUNTS=0,33,88
```

and one `z=7` edge sequence spanning consecutive X values `32537..32554`, i.e. 18 positions inclusive; the orthogonal edge observation matched a 14-position separation.

### Evidence-strength correction

The downloadable run artifact `9221332209` contains only `before.xwd`, `forward.xwd` and `inverse.xwd`, not the TSV rows or job log. Therefore the durable classification of the numeric `18 x 14` result is:

```yaml
classification: DERIVED_FROM_OBSERVED_JOB_LOG
confidence: high
raw_rows_preserved_in_consumed_artifact: false
```

A future mutation experiment must recapture/persist the raw structural rows before promoting this numerical geometry to a stronger durable proof.

The cumulative values `33` and `88` are **not** viewport dimensions and must not be interpreted as such.

## Why a larger map is plausible

The exact client provides separate semantic concepts for:

```text
extent
subfield extent
storage
viewport
camera
protocol handler
render provider
```

This suggests a design in which at least some of these responsibilities can be traced independently.

**DERIVED / HIGH CONFIDENCE:** a larger world-map area is technically plausible enough to justify targeted reverse engineering.

The strongest next hypothesis is not “replace 18 with 36 everywhere”. It is:

> determine which limits belong to data extent/storage, which belong to protocol/live awareness, and which belong only to camera/render viewport.

This distinction matters because increasing all three together may multiply network and dynamic-state cost unnecessarily.

## Two expansion axes that must remain separate

### A. Full live awareness expansion

The server/client path would deliver and maintain a larger area containing current dynamic state such as creatures, moving objects and effects.

Potential consequences include increased:

- protocol payload volume;
- map update work on movement/floor changes;
- dynamic entity bookkeeping;
- CPU and memory cost;
- possible server-side range assumptions.

This requires protocol/server compatibility evidence and cannot be inferred from renderer capability alone.

### B. Terrain/cache/render expansion

The client would render a larger static/retained map area while live dynamic awareness remains smaller.

This is attractive because the exact client exposes distinct storage/viewport/camera/render concepts, but it remains a hypothesis until object layouts and data provenance are traced.

If feasible, this axis could provide a much wider visual map without requiring every dynamic entity in the larger rectangle to be live-updated by the server.

## Candidate size ladder

Current interpreted baseline:

```text
18 x 14 = 252 tiles/floor
```

Useful experiment targets:

| Candidate | Tiles/floor | Tile-count multiplier |
|---|---:|---:|
| `18 x 14` | 252 | `1.00x` |
| `26 x 20` | 520 | `2.06x` |
| `32 x 24` | 768 | `3.05x` |
| `36 x 28` | 1008 | `4.00x` |

These are test targets only. Doubling both linear dimensions quadruples the number of tiles per floor, so “2x wider and 2x taller” is not a 2x-cost experiment.

A safer first mutation should be smaller than `26 x 20`—for example a one-column/one-row or similarly minimal increase—to expose hidden fixed assumptions before scaling.

## Unknowns that block an implementation claim

The investigation has **not** yet recovered:

1. constructor/default writes for current worldmap width/height;
2. exact fields in `TWorldMapExtent`, `TWorldMapSubfieldExtent` or `TWorldMapViewport`;
3. all readers/writers of those fields;
4. fixed-size arrays, stack buffers, masks, bit widths or loop bounds tied to current geometry;
5. protocol parser/serializer floor/row/column assumptions;
6. `TWorldMapStorage` capacity and eviction strategy;
7. camera/render clipping/culling constraints;
8. interaction/picking/HUD assumptions at larger extents;
9. server-side live-awareness limits for the exact protocol;
10. bandwidth/CPU/GPU/RAM cost at larger dimensions;
11. whether a terrain-only outer ring can use retained/local map data safely and coherently;
12. the maximum safe dimensions.

Until these are resolved, any statement such as “official client supports 36 x 28” is false/unproven.

## Required static-first experiment

The next bounded research package should remain `runtime_access: none` initially and produce a dependency graph before changing client bytes.

### Phase 1 — recover dimension ownership

1. Find xrefs and constructors for `TWorldMapExtent`, `TWorldMapSubfieldExtent` and `TWorldMapViewport`.
2. Identify candidate dimension fields and initial/default writes.
3. Trace every read/write of those candidates.
4. Look specifically for paired width/height math, inclusive/exclusive edge offsets and floor-dependent projection adjustments.

### Phase 2 — trace consumers

Trace candidate dimensions into:

- `TWorldMapStorage`;
- `TWorldmapProtocolMessageHandler`;
- `TWorldMapRenderProvider`;
- `TWorldMapCamera`;
- picking/HUD/coordinate transforms;
- movement/floor-change strip generation/consumption.

### Phase 3 — fixed-limit audit

Search for:

- fixed-size allocations;
- constant loop bounds;
- clipping rectangles;
- masks/packing widths;
- row/floor serializers/parsers;
- temporary stack arrays;
- cache dimensions;
- assumptions in teleport/floor-change/reposition paths.

### Phase 4 — patch graph

Produce a table:

```text
candidate field/constant
-> writers
-> readers
-> allocation dependencies
-> protocol dependencies
-> render dependencies
-> safety consequence if changed alone
```

Only after this graph is coherent should a binary mutation be designed.

## Future mutation ladder

Any future live mutation is a separate task and must use the current Track A runtime governance rather than historical displays/PIDs/session assumptions.

Recommended order:

1. exact-SHA revalidation;
2. current runtime admission/ownership gates;
3. smallest positive dimension change;
4. login/world-entry validation;
5. north/east/south/west edge updates;
6. movement and inverse movement;
7. floor up/down;
8. teleport/reposition;
9. item/creature/effect changes at old and new boundaries;
10. renderer/picking/HUD validation;
11. resource measurements;
12. only then scale toward `26 x 20`, `32 x 24`, `36 x 28` as evidence allows.

A failure at a smaller size should be diagnosed before attempting a larger one.

## Runtime governance boundary

This report itself performs no live runtime operation.

```yaml
runtime_access: none
mutation_authorized: false
```

Historical `:98`, `6082`, PID/session state or prior runtime addresses are not authorization for a future experiment. The future worker must resolve the then-current trusted Track A governance, registration, lease, ownership and exact-client state before observing or mutating a live client.

## Security and licensing

No official client binary, proprietary assets, credentials, account/session data or private captures are committed by this research checkpoint.

Binary/type names, offsets, hashes, workflow/run IDs and compact neutral evidence are retained only for internal compatibility/research continuation. Anti-cheat bypass or disabling client checks is outside scope.

## Final conclusion

The investigation establishes a **high-confidence feasibility lead**, not an implemented feature:

> The exact official Tibia `15.32.df7b29` binary contains distinct worldmap extent/storage/viewport/camera/protocol/render surfaces and already has a structural map-update observation path. This makes a larger loaded/rendered map area a credible technical target. The actual patch points, safe maximum and server-awareness relationship remain UNKNOWN and must be recovered through static dependency analysis before any live mutation.

The immediate engineering target is therefore **dimension-ownership and dependency recovery**, not a blind `18x14 -> 36x28` patch.