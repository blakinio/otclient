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

The task remains active as `MORE_STATIC_RE_NEEDED`. Fresh GitHub-hosted staging of the exact installed `15.32.df7b29` game-client ELF remains blocked, but retained same-repository exact-client evidence has materially strengthened the geometry, protocol-handler and storage-side graph.

The most important current result is now object-level rather than strip-only: a concrete dependency reached through the recovered worldmap handler's `owner+0x10` path stores the exact DWORD pair `18,14` at `+0x48/+0x4c`, while two coordinate-like pairs in that same object differ independently by exactly `18` and `14`. The object's historical static vptr is `0x0308ce70`.

This is strong evidence that `18×14` exists as explicit worldmap geometry state. It is still **not** a safe patch site because the object's exact class identity, field semantics, constructor/default writer and all material consumers have not yet been proven.

## Exact historical installed-client fence

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
```

No current PID/session/display/runtime authority is inferred from historical evidence.

## Owner-supplied official Linux package

The owner-supplied `tibia.x64.tar.gz` was verified as:

```yaml
size_bytes: 29477141
sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
contained_Tibia_Tibia_size: 1460808
contained_Tibia_Tibia_sha256: a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0
classification: launcher_updater_distribution
github_artifact: 9264329820
```

It is not the historical 51,965,216-byte installed game-client ELF and is not substituted for that fence. Launcher-derived official manifest probes in run `31949948886` returned Cloudflare HTTP 403; identical retries are not justified.

## Direct geometry evidence

Retained artifact `9227370490` (`track-a-persistent-provenance-dump`, run `31821458677`, digest `sha256:991f5c22a7ffc1d23c6597307a49728b363863a5acd6dd754bff1222404c8e2d`) preserves 90 raw strip rows plus historical memory/GDB observations.

### Strip facts

```text
Z=7, Y=32502: X=32537..32554 -> 18 consecutive X
Z=7, Y=32516: X=32537..32554 -> 18 consecutive X
Y delta = 14
```

### Concrete `owner+0x10` object

Two retained `ChangeOnMap` hits and one `CreateOnMap` hit share historical owner `0x55868276a460`. The observer runtime/static mappings produce one consistent historical PIE base:

```text
0x5586665f8000
```

The dependency reached through `owner+0x10` is historical runtime object `0x55867df448c0` with runtime vptr `0x558669684e70`, therefore exact static vptr:

```text
0x0308ce70
```

Stable decoded DWORDs across the retained hits:

```text
object+0x18 = 32537
object+0x1c = 32503
object+0x30 = 32555
object+0x34 = 32517
object+0x38 = 8
object+0x48 = 18
object+0x4c = 14
object+0x50 = 8
object+0x58 = 7
object+0x60 = 19
```

Exact arithmetic:

```text
32555 - 32537 = 18
32517 - 32503 = 14
```

**FACT:** an exact `18/14` pair is stored in a concrete object on the proven worldmap-handler dependency path, and the same object independently contains candidate bound pairs whose differences are `18/14`.

**INFERENCE:** `+0x18/+0x1c` and `+0x30/+0x34` are plausible lower/upper bounds, while `+0x48/+0x4c` are plausible width/height or extent fields. `TWorldMapViewport` is a plausible class correlation.

**UNKNOWN:** exact class identity, semantic field names/units, inclusive/exclusive convention, constructor/default writer and complete reader/writer graph.

The horizontal strip span `32537..32554` exactly matches the half-open interpretation `[32537,32555)`. The observed strip Y rows are one below the object's candidate Y pair, so a simple strip-to-field identity is not promoted.

Durable evidence:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-retained-owner-geometry-object.md`

## Handler-owner identity frontier

The first QWORD of the same common historical owner snapshot is runtime vptr `0x55866967f1d8`; subtracting the proven historical PIE base yields:

```text
handler-owner static vptr = 0x030871d8
```

The first retained vtable targets translate exactly to:

```text
0x00dee8c0
0x00dffb20
0x00e02c50
0x00826890
0x00826bc0
```

Exact-static census evidence independently contains:

```text
N5tibia8worldmap31TWorldmapProtocolMessageHandlerE
St23_Sp_counted_ptr_inplaceIN5tibia8worldmap31TWorldmapProtocolMessageHandlerESaIvELN9__gnu_cxx12_Lock_policyE2EE
```

**FACT:** the common map-handler owner has static vptr `0x030871d8`.

**INFERENCE:** `TWorldmapProtocolMessageHandler` is a strong semantic candidate for that owner because the object is the common receiver for FullMap/Create/Change/Delete-family handling and the exact build contains the matching RTTI/control-block surfaces.

**UNKNOWN:** the decisive Itanium header/typeinfo relation immediately before that vptr. Exact discriminator window:

```text
0x030871c8..0x030871d7
```

No class name is promoted without that proof.

Durable evidence:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-owner-vptr-storage-scale-coupling.md`

## Observer producer-source provenance

Historical workflow source recovers the research-label mappings:

```text
CreateOnMap  -> 0x00cecc70
ChangeOnMap  -> 0x00cecf40
DeleteOnMap  -> 0x00cd4e20
FullMap      -> 0x00cec8d0
MapDescription strip capture -> 0x019a8ea3
```

Producer-source commits include `caa938463356ce9a8ece92e9ae908ba507f501a9` and `734f845deace5a26efa09b96a168bea0c05272f0`; verification commit `b15b41c8f14f4c148d163990031b8c3be6278343` confirms the persistent observer design. These are research labels, not compiler/debug symbols.

## Exact fenced handler disassembly

Historical exact-SHA-fenced run `31804083206`, job `94778661881`, preserves these bounded ranges:

```text
CreateOnMap    0x00cecb80..0x00ced150
ChangeOnMap    0x00cece50..0x00ced4b0
DeleteOnMap    0x00cd4d30..0x00cd54a0
FullMap        0x00cec790..0x00cecaa0
MapDescription 0x019a89c0..0x019a9000
```

### FullMap `0xcec8d0`

FACT:

```text
resolved event DWORD +0x18/+0x1c/+0x20 are consumed
owner QWORD +0x98 and DWORD +0xa0 persist the three-value state
first two payload integers are shifted left by 5 (= multiplied by 32)
scaled local is passed through owner+0x70 virtual slot +0x60
owner+0xa0 is later compared with 7
0x19a8a80 is called with the derived floor-dependent boolean
```

**INFERENCE:** the `×32` conversion strongly supports a subfield-to-tile geometry boundary.

### MapDescription `0x19a8a80`

FACT: per-descriptor fields `+0x38/+0x3c/+0x40` participate as multiplicative/divisor grid parameters; `+0x08/+0x0c` are additive coordinate bases; `+0x10/+0x48` participate in the alternate/floor-dependent transform. Generated three-DWORD coordinates reach the `owner+0x10` object through virtual slot `+0xa0`.

**INFERENCE:** this is a concrete protocol-to-worldmap geometry surface and a strong `TWorldMapExtent` / `TWorldMapSubfieldExtent` correlation target.

### Create/Change/Delete family

FACT:

- Create/Change/Delete share the `owner+0x10 -> vslot +0xa0` dependency family;
- Create/Change both call common helper `0xceca50`;
- repeated `owner+0xd8` / `+0x98` map-state comparison paths appear across the family;
- Change's alternate branch reaches `owner+0x80 -> vslot +0xf0`;
- Delete's alternate path reaches `owner+0x30 -> vslot +0xd8`.

### Common helper `0xceca50`

FACT from the retained exact prefix:

```text
uses source+0x10
reads global DWORD 0x3193220
calls 0x1aab810
one path reads owner+0x50 and owner+0x60
owner+0x50 object -> virtual slot +0xa0
owner+0x60 object -> virtual slot +0x10
```

The retained range still ends before full helper completion, so its full semantics remain `UNKNOWN`.

Durable detail:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-exact-handler-disassembly-recovery.md`

## Storage/container lead `0xced1b0`

Exact disassembly proves a bucketed linked-node rebuild:

```text
self+0x48 -> bucket-array base candidate
self+0x50 -> bucket count/size term; memset size = +0x50 * 8
self+0x58 -> node-head candidate
self+0x60 -> count/state
replacement node size = 0x20 bytes
bucket placement uses unsigned division by retained bucket-count value
```

This is structurally consistent with the exact-static instantiated `unordered_map<TWorldMapCoordinate, std::shared_ptr<TWorldMapTile>, ...>` surface.

A further exact coupling is now preserved: after the bucket rebuild, the same function reaches the dependency at `self+0x30`, reads a floating-point value at that object's `+0xd0`, converts it to double and multiplies it by the constant referenced at static `0x29505a8`.

**FACT:** the candidate map/hash rebuild and a floating-point dependency at `self+0x30/+0xd0` are consumed in the same function.

**INFERENCE:** the float is a scale/geometry/render-related candidate and may connect storage to viewport/render/camera state.

**UNKNOWN:** owning class of `0xced1b0`, exact class of `self+0x30`, meaning/unit of `+0xd0`, value/meaning of the constant, and whether the arithmetic is camera scale, render scale, world/tile scale or something unrelated.

No render/camera class name is assigned by guess.

## Exact-static RTTI/type frontier

Retained exact-static artifacts preserve all eight target type names plus separate shared-control-block instantiations for storage, viewport, protocol handler, render provider, camera and picker.

Important exact string anchors include:

```text
TWorldMapExtent                                      0x1c8fee0
TWorldMapSubfieldExtent                              0x1c9fe20
counted TWorldMapStorage                             0x1ca9180
counted TWorldMapViewport                            0x1cabb60
TWorldMapCamera                                      0x1cabce0
counted TWorldMapCamera                              0x1cabd20
TWorldmapProtocolMessageHandler                      0x1cd59a0
counted TWorldmapProtocolMessageHandler              0x1cdba40
counted TWorldMapRenderProvider                      0x1cdb580
TWorldMapPicker                                      0x1cdb600
counted TWorldMapPicker                              0x1cdb640
TWorldMapRenderProvider                              0x1cddd20
TWorldMapViewport                                    0x1ce1b60
TWorldMapStorage                                     0x1ce1c00
literal tibia::worldmap::TWorldMapExtentX            0x1cd9ad7
```

Known relocation leads:

```text
0x3089b78 -> 0x1cddd20  TWorldMapRenderProvider name
0x308b598 -> 0x1ce1b60  TWorldMapViewport name
```

Candidate typeinfo starts `0x3089b70` and `0x308b590` remain ABI hypotheses until surrounding RTTI/vtable relations are proven.

The previous exact-ELF graph probe searched the plain `TWorldMapViewport` name and also found it as a substring inside the counted-type string, but did **not** target the full counted-type start `0x1cabb60` as its own relocation target. Therefore the absence of a retained counted-viewport relocation in that output is a coverage gap, not negative evidence.

## Current exact discriminator windows

```text
handler owner vptr        0x030871d8 -> header 0x030871c8..0x030871d7
18/14 geometry object     0x0308ce70 -> header 0x0308ce60..0x0308ce6f
18/14 control-like block  0x02f683d0 -> header 0x02f683c0..0x02f683cf
```

The `owner+0x18` companion immediately before the geometry object is structurally consistent with a combined `std::_Sp_counted_ptr_inplace<...>` allocation (vptr, reference counters, object beginning at +0x10), but that remains an ABI/layout inference until its RTTI relation is recovered.

## Updated partial dependency graph

```text
common handler owner (static vptr 0x30871d8; exact class UNKNOWN)
  -> FullMap/Create/Change/Delete family
  -> owner+0x10 geometry object (static vptr 0x308ce70)
       -> exact +0x48/+0x4c = 18/14
       -> candidate bound deltas = 18/14
       -> exact class identity UNKNOWN
  -> owner+0x70 virtual +0x60 in FullMap scaled geometry path
  -> owner+0x80 virtual +0xf0 in Change alternate path
  -> owner+0xd8 repeated map-state comparison family

FullMap
  -> two payload values ×32
  -> 0x19a8a80 MapDescription
       -> descriptor grid/divisor fields
       -> generated three-DWORD coordinate
       -> owner+0x10 virtual +0xa0
       -> nested handling / 0xceca50

0xced1b0 candidate storage/container operation
  -> bucketed 0x20-byte-node rebuild at self+0x48..+0x60
  -> self+0x30 dependency -> float +0xd0
  -> floating scaling arithmetic

RenderProvider / Camera / Picker
  -> exact type/shared-lifetime surfaces present
  -> direct clipping/culling/transform field graph still UNKNOWN
```

## Patch graph matrix

| Graph element | Status |
|---|---|
| target subsystem/type presence | PROVEN |
| shared-control-block surfaces | PROVEN for storage/viewport/protocol/render/camera/picker |
| raw 18-sample geometry and Y delta 14 | PROVEN |
| concrete `owner+0x10` object stores exact `18/14` | PROVEN |
| candidate bound-pair differences `18/14` | PROVEN arithmetic; semantics INFERENCE |
| geometry object static vptr `0x308ce70` | PROVEN |
| common handler-owner static vptr `0x30871d8` | PROVEN |
| handler owner = `TWorldmapProtocolMessageHandler` | INFERENCE / RTTI proof missing |
| geometry object = `TWorldMapViewport` | INFERENCE / RTTI proof missing |
| FullMap payload ×32 conversion | PROVEN |
| MapDescription grid/divisor accesses | PROVEN |
| shared owner+0x10 virtual +0xa0 path | PROVEN |
| helper `0xceca50` involvement | PROVEN; completion INCOMPLETE |
| `0xced1b0` bucket/hash rebuild | PROVEN structure |
| `0xced1b0` -> `self+0x30/+0xd0` float coupling | PROVEN |
| direct `TWorldMapStorage` ownership | UNKNOWN |
| literal viewport width/height field names | UNKNOWN |
| extent/subfield semantic field mapping | UNKNOWN |
| constructor/default dimension writers | UNKNOWN |
| complete material reader/writer graph | UNKNOWN |
| storage capacity/eviction rules | UNKNOWN |
| fixed arrays/loop bounds/masks/parser assumptions | INCOMPLETE |
| render clipping/culling | UNKNOWN |
| camera projection/scale coupling | UNKNOWN; one scale-like candidate only |
| picker bounds/screen-world transform | UNKNOWN |
| concrete safe patch sites | UNKNOWN |

## Current blocker

The remaining high-value static questions require bytes/relocations not present in the retained artifacts inspected so far:

- one of the exact vtable-header/typeinfo windows above;
- direct writers/xrefs for geometry-object `+0x48/+0x4c` and candidate bounds;
- additional code windows completing `0xceca50` and identifying `0xced1b0` / `self+0x30` classes;
- render/camera/picker consumers and fixed-bound assumptions.

Fresh exact-client materialization on GitHub-hosted is still blocked by official delivery/CDN behavior. The task will not repeat an identical failed HTTP staging attempt and will not use Synology as an unauthorized static fallback.

## Next research frontier

1. recover retained vtable-header/typeinfo evidence for `0x30871d8`, `0x308ce70` or `0x2f683d0`;
2. if exact ELF access becomes legally available again, target full counted-type string starts `0x1cabb60` and `0x1cdba40` explicitly, not only plain names/substrings;
3. recover writers/xrefs for geometry-object `+0x48/+0x4c` and candidate bound fields;
4. correlate `0xced1b0` and its `self+0x30/+0xd0` dependency with storage/render/camera RTTI/vtables;
5. inventory fixed allocations, loops, masks, parser packing, clipping/culling and picker transforms;
6. only after the full dependency graph is coherent may mutation design begin.

No GUI/runtime discriminator is currently required, no client bytes were modified, and no owner-funded Codex/OpenAI API/token use occurred.