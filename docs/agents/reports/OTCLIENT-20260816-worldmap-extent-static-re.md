# OTCLIENT-TIBIA-RE — worldmap extent static dependency recovery

```yaml
report_date: 2026-08-16
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
subject: official native Linux Tibia client only
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
implementation_status: NOT_IMPLEMENTED
client_byte_mutation: NOT_PERFORMED
runtime_used_by_this_task: false
static_classification: MORE_STATIC_RE_NEEDED
static_patch_graph_ready: false
retained_evidence_research_path: BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
```

## Result

The retained GitHub-only investigation is now bounded to a real evidence boundary. The repository artifact inventory contains 493 artifacts; the complete inventory was reviewed and every admissible Track A artifact whose scope can answer the current `static/vtable/RTTI/provenance/writer-xref` questions was directly inspected. No retained artifact contains the exact vtable-header/typeinfo words or geometry-field writer xrefs required to finish the patch graph.

The strongest result remains materially positive for viewport expansion feasibility: a concrete worldmap dependency stores an exact `18×14` geometry pair and matching candidate bound deltas. A newly recovered inline control-block layout makes `TWorldMapViewport` a very strong class correlation, but direct RTTI identity is still not retained and therefore is not promoted to fact.

No client bytes were modified and no unsupported physical/runtime fallback was used.

## Proven concrete geometry

Historical retained artifact `9227370490` preserves two `ChangeOnMap` hits and one `CreateOnMap` hit with common owner `0x55868276a460` and exact historical PIE base `0x5586665f8000`.

The object reached through `owner+0x10` is:

```text
runtime object = 0x55867df448c0
runtime vptr   = 0x558669684e70
static vptr    = 0x0308ce70
```

Stable DWORDs:

```text
+0x18 = 32537
+0x1c = 32503
+0x30 = 32555
+0x34 = 32517
+0x38 = 8
+0x48 = 18
+0x4c = 14
+0x50 = 8
+0x58 = 7
+0x60 = 19
```

Exact relations:

```text
32555 - 32537 = 18
32517 - 32503 = 14
```

Retained strip rows independently show two Z=7 horizontal groups with `X=32537..32554` (18 values) and Y separation 14.

**FACT:** `18/14` is explicit stored state in a concrete object on the recovered worldmap-handler dependency path.

**INFERENCE:** the coordinate-like pairs are lower/upper bounds and `+0x48/+0x4c` are width/height or extent fields.

**UNKNOWN:** exact field names/units and exact class identity.

## Stronger shared-control-block evidence

The full raw `9227370490` archive contains a 2.28 MB GDB stdout plus raw/event/strip logs. It directly preserves:

```text
owner+0x18 companion = 0x55867df448b0
geometry object      = 0x55867df448c0
object offset        = companion + 0x10
companion static vptr = 0x02f683d0
retained DWORD counts = 13, 1
companion+0x10 begins with geometry object vptr
```

The same paired object/companion pattern repeats at owner `+0x20/+0x28` and `+0x30/+0x38`, with companion static vptrs approximately `0x02f70c60` / `0x02f70c98` and object static vptrs approximately `0x0308cfd8` / `0x0308d078`.

**FACT:** a polymorphic control-like block, two counter DWORDs and the object inline at `+0x10` are directly preserved.

**INFERENCE:** the layout is strongly consistent with libstdc++ `std::_Sp_counted_ptr_inplace<T>` / `std::make_shared<T>`. The exact build independently contains a counted `TWorldMapViewport` RTTI string at `0x1cabb60`, making the `18×14` object a **very strong `TWorldMapViewport` correlation**.

**UNKNOWN:** no retained typeinfo relocation connects control vptr `0x02f683d0` directly to that counted viewport RTTI, so exact class identity remains unproven.

## Handler/protocol graph

Research observer source maps:

```text
FullMap      0x00cec8d0
CreateOnMap  0x00cecc70
ChangeOnMap  0x00cecf40
DeleteOnMap  0x00cd4e20
MapDescription capture 0x019a8ea3
```

Exact-SHA-fenced historical disassembly (`run 31804083206`, job `94778661881`) proves:

- `FullMap@0xcec8d0` persists a three-value owner state and shifts two adjacent payload integers left by 5 (`×32`) before a worldmap-owner virtual call;
- `MapDescription@0x19a8a80` uses descriptor `+0x38/+0x3c/+0x40` as grid/divisor parameters, `+0x08/+0x0c` as coordinate bases and `+0x10/+0x48` in the alternate/floor transform;
- generated three-DWORD coordinates reach `owner+0x10 -> virtual slot +0xa0`;
- Create/Change/Delete reuse the same `owner+0x10` virtual-consumer family and repeated `owner+0xd8` state-comparison family;
- common helper `0xceca50` is shared by Create/Change and nested description handling, but its retained range ends before full completion.

The common handler owner's static vptr is proven as `0x030871d8`. `TWorldmapProtocolMessageHandler` is a strong semantic correlation, but its exact typeinfo relation is not retained.

## Storage lead

Neighbor `0xced1b0` proves a bucketed container rebuild:

```text
self+0x48 bucket-array base candidate
self+0x50 bucket-size/count term; clear size = value * 8
self+0x58 node-head candidate
self+0x60 count/state
replacement node size = 0x20 bytes
bucket placement uses unsigned division
```

This is structurally consistent with the exact-static `unordered_map<TWorldMapCoordinate, shared_ptr<TWorldMapTile>, ...>` surface. The same function later reads a float from dependency `self+0x30/+0xd0`, converts it to double and applies a scaling constant.

**FACT:** storage/hash-like rebuild and the `self+0x30/+0xd0` floating dependency are consumed together.

**UNKNOWN:** direct owning class, meaning of the float and whether the dependency is camera/render/viewport scale.

## Exact RTTI/type surfaces

Exact-static artifacts retain all target type names and counted-control-block names. Key anchors:

```text
TWorldMapExtent                         0x1c8fee0
TWorldMapSubfieldExtent                 0x1c9fe20
counted TWorldMapStorage                0x1ca9180
counted TWorldMapViewport               0x1cabb60
TWorldMapCamera                         0x1cabce0
counted TWorldMapCamera                 0x1cabd20
TWorldmapProtocolMessageHandler         0x1cd59a0
counted protocol handler                0x1cdba40
counted TWorldMapRenderProvider         0x1cdb580
TWorldMapPicker                         0x1cdb600
counted TWorldMapPicker                 0x1cdb640
TWorldMapRenderProvider                 0x1cddd20
TWorldMapViewport                       0x1ce1b60
TWorldMapStorage                        0x1ce1c00
literal TWorldMapExtentX                0x1cd9ad7
```

Retained type-name relocation leads include:

```text
0x3089b78 -> 0x1cddd20  RenderProvider name
0x308b598 -> 0x1ce1b60  Viewport name
```

They do not preserve the inverse typeinfo-to-vtable relation needed for the geometry object/control block.

## Complete retained-artifact boundary

The artifact inventory was paged across all 493 repository artifacts. Pages 4 and 5 contain no `track-a-*` artifacts. Older entries are OTClient/Windows/build material and are not admissible official Linux Track A evidence.

In addition to the P0/static/provenance artifacts already used by this task, this continuation directly downloaded and searched the remaining relevant artifacts, including:

```text
9233690471 static provenance
9231716774 tcp-member RTTI
9228275973 outbound-owner vtables
9228087310 transport vtable/RTTI
9228921041 login-origin write xrefs
9226966960 QIODevice write xrefs
9246854524 / 9246830425 / 9246826386 / 9246813407 / 9246799418 writer-vtable groups
9229251044 / 9229184085 / 9229127873 network-writer vtable census
9221392689 single-item-drag-only
```

The larger decompressed reports range from ~100 KB to ~1.5 MB and contain genuine ELF/vtable analysis, but their candidate sets are network/writer-scoped and contain none of the missing worldmap vptr/header relations. The final writer/network vtable artifacts likewise contain unrelated protocol/sessiondump vtables. The large single-item-drag artifact contains XWD screenshots only.

Full detail is recorded in:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-complete-retained-artifact-inventory.md`

## Current exact blocker

The following exact static windows are known to be decisive but are not durably retained:

```text
0x030871c8..0x030871d7 -> handler owner vptr 0x030871d8
0x0308ce60..0x0308ce6f -> 18/14 object vptr 0x0308ce70
0x02f683c0..0x02f683cf -> control vptr 0x02f683d0
```

Also missing:

- writer/xrefs for geometry fields `+0x18/+0x1c/+0x30/+0x34/+0x48/+0x4c`;
- exact direct ownership/capacity/eviction proof for `TWorldMapStorage`;
- complete render-provider clipping/culling/iteration constraints;
- camera projection/scale coupling;
- picker screen/world bounds and transforms;
- full audit of fixed allocations, loop bounds, masks and parser packing assumptions tied to the proposed extent change.

Therefore `STATIC_PATCH_GRAPH_READY=false` and no safe patch-site list can be asserted.

## Runtime cross-check

Trusted main advanced through RUNTIME graphics work. PR #405 / v7 reached exact-client `client_start` after the Qt XCB graphics repair, but again failed closed at `client_window_missing`. It produced no authoritative registration, no Gate B and no exact static staging for this task. The attempt is archived on main as governance-invalid.

The GitHub-hosted STATIC-RE task has no approved mechanism to silently convert that physical runner into a static-analysis fallback. No such access was used.

## Classification

```yaml
artifact_inventory_review: COMPLETE
admissible_static_vtable_rtti_provenance_candidates: INSPECTED
geometry_18_14_explicit_state: PROVEN
geometry_make_shared_layout: STRONG_INFERENCE
geometry_object_viewport_identity: VERY_STRONG_INFERENCE_NOT_DIRECT_RTTI_PROOF
required_worldmap_vtable_header_words: NOT_DURABLY_STAGED
geometry_writer_xrefs: NOT_DURABLY_STAGED
static_patch_graph_ready: false
classification: BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
```

Research should resume in this same task/PR only when an admissible producer supplies new exact static bytes. Re-scanning the retained inventory or repeating the already-failed identical CDN fetch is duplicate work and must not be used as a substitute for new evidence.
