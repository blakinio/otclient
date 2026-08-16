# OTC-20260816-track-a-worldmap-extent-static-re — retained provenance recovery

```yaml
evidence_date: 2026-08-16
repository: blakinio/otclient
track: official-client-re
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
execution_class: github_hosted
runtime_access: none
client_mutation: false
owner_funded_ai_api_authorized: false
source_mode: retained_exact_client_artifact_and_log_analysis
```

This checkpoint continues static discovery without a new client download and without Synology execution. It consumes only already-retained artifacts/logs from `blakinio/otclient` and records neutral structural facts; no proprietary executable bytes are committed.

## Retained raw provenance artifact

FACT:

```yaml
artifact_id: 9227370490
artifact_name: track-a-persistent-provenance-dump
workflow_run: 31821458677
run_head: f23e9df548859d11520bbd2983c0df4e9923c2e7
artifact_digest: sha256:991f5c22a7ffc1d23c6597307a49728b363863a5acd6dd754bff1222404c8e2d
```

The artifact contains:

- `map-provenance-persistent-events.tsv`;
- `map-provenance-persistent-gdb.stdout`;
- `map-provenance-persistent-raw.log`;
- `map-provenance-persistent-strips.tsv`.

The producing workflow head is historical runtime evidence. This task did not execute it and does not promote its runtime PID/display/session as current state.

## Raw strip geometry upgrade

`map-provenance-persistent-strips.tsv` contains 90 directly retained rows. The seven columns are timestamp, X, Y, Z, an observer classification/index field, a captured pointer and a bounded raw object byte sample.

Direct row groups include:

```text
Y=32502 Z=7 class=0: X=32537..32554, 18 unique consecutive X
Y=32516 Z=7 class=0: X=32537..32554, 18 unique consecutive X
```

Therefore:

```yaml
FACT:
  z7_first_horizontal_sample_count: 18
  z7_first_horizontal_x_min: 32537
  z7_first_horizontal_x_max: 32554
  z7_second_horizontal_sample_count: 18
  z7_second_horizontal_x_min: 32537
  z7_second_horizontal_x_max: 32554
  y_difference_between_these_two_groups: 14
INFERENCE:
  baseline_geometry_consistent_with: 18_x_14
UNKNOWN:
  object_field_width: UNKNOWN
  object_field_height: UNKNOWN
  inclusive_exclusive_extent_semantics: UNKNOWN
```

This corrects the weaker statement in the feasibility checkpoint that the raw TSV rows were unavailable in the consumed artifact. They were absent from artifact `9221332209`, but are directly retained in separate artifact `9227370490`. The raw counts and coordinate differences above are now PROVEN. The interpretation that these are literally the stored viewport width/height remains an inference until the dimension fields are recovered.

The remaining strip rows are not collapsed into dimensions. They include additional observer classifications and Z=6 samples and therefore require their own semantic provenance before use as extent values.

## Historical breakpoint fence

The retained GDB transcript directly records five breakpoints:

```text
BP1 runtime 0x5586672e4c70 -> static exact-build lead 0x00cecc70
BP2 runtime 0x5586672e4f40 -> static exact-build lead 0x00cecf40
BP3 runtime 0x5586672cce20 -> static exact-build lead 0x00cd4e20
BP4 runtime 0x5586672e48d0 -> static exact-build lead 0x00cec8d0
BP5 runtime 0x558667fa0ea3 -> static exact-build lead 0x019a8ea3
historical PIE base: 0x5586665f8000
```

BP5 matches the already-retained exact-version common-map capture lead `0x19a8ea3`.

The event TSV contains only observer labels `CreateOnMap` and `ChangeOnMap`. Raw rows bind their `r8` function-pointer values to:

```text
CreateOnMap:r8  = 0x5586672e4c70 = BP1
ChangeOnMap:r8  = 0x5586672e4f40 = BP2
```

FACT: the retained observer output used those two labels and captured those exact function pointers.

UNKNOWN: the original state-local observer source that assigned the human-readable labels has not yet been recovered from Git. Consequently the labels remain `OBSERVER_ASSIGNED`, not independently promoted debug symbols.

## Exact retained machine-code recovery for BP1/BP2

The raw log contains 256-byte machine-code samples at both r8 targets. Offline disassembly of those retained bytes is deterministic and requires no client executable.

### BP1 / observer label `CreateOnMap` / static `0xcecc70`

Directly recovered instructions prove:

```text
prologue stores rdi as owner-like base (rbp) and rsi as event-like base (rbx)
[rsi+0x18] qword read
[rdi+0x10] qword read
virtual dispatch through object loaded from [rdi+0x10], vtable slot +0xa0
[event-like +0x20] qword read
[event-like +0x28] dword read
secondary object loaded from event-like +0x20 then reads +0x08, +0x28 and +0x30
```

Direct-call / RIP-relative static targets visible inside the retained 256-byte prefix include:

```text
call 0x1b13c80
call 0x1ab4e50
RIP-relative 0x313a820
RIP-relative 0x30874a8
RIP-relative 0x2f615a0
RIP-relative 0x314b480
```

These target addresses are exact-build code/data leads only; semantic names remain UNKNOWN until correlated with independent type/string/consumer evidence.

### BP2 / observer label `ChangeOnMap` / static `0xcecf40`

Directly recovered instructions prove:

```text
prologue stores rdi as owner-like base (rbp) and rsi as event-like base (rbx)
test byte [event-like+0x10] & 1; branch if clear
[event-like+0x18] qword read
[owner-like+0x10] qword read
virtual dispatch through object loaded from [owner-like+0x10], vtable slot +0xa0
[event-like+0x20] qword read
[event-like+0x28] dword read
direct call static 0x1822ec0
direct call static 0xceca50
later virtual call through slot +0xf0 of another object
```

Additional RIP-relative exact-build leads in the retained prefix:

```text
0x313a820
0x2f615a0
0x314b480
0x312faa8
```

The shared reads and shared virtual `owner+0x10 -> slot +0xa0` path establish a real code-structure relationship between the two observer-labeled map events. The common helper `0xceca50` is a new exact static lead for further retained-evidence correlation.

No claim is made that offsets `+0x10/+0x18/+0x20/+0x28/+0x30` are viewport dimensions. They are proven accesses in the retained event-handler prefixes only.

## Rich older exact-static census

Separate retained exact-static artifact:

```yaml
artifact_id: 9246756211
artifact_name: track-a-p0-static-elf-31883967070
workflow_run: 31883967070
run_head: eec9f6fcb065dd7762fa098ad78d1661b0060bd3
artifact_digest: sha256:2d3e423d05eef2e370e10c1dcc6afeab27ad2d3a04fe8ccfb2ba635575dabe74
```

contains a broader semantic census than the later feasibility extract. Direct exact strings include:

```text
0x1c8fee0  N5tibia8worldmap15TWorldMapExtentE
0x1c9fe20  N5tibia8worldmap23TWorldMapSubfieldExtentE
0x1ca9180  shared_ptr control block for TWorldMapStorage
0x1cabb60  shared_ptr control block for TWorldMapViewport
0x1cabce0  N5tibia8renderer15TWorldMapCameraE
0x1cabd20  shared_ptr control block for TWorldMapCamera
0x1cd59a0  N5tibia8worldmap31TWorldmapProtocolMessageHandlerE
0x1cdba40  shared_ptr control block for TWorldmapProtocolMessageHandler
0x1cdb580  shared_ptr control block for TWorldMapRenderProvider
0x1cdb600  N5tibia8worldmap15TWorldMapPickerE
0x1cdb640  shared_ptr control block for TWorldMapPicker
0x1cddd20  N5tibia8worldmap23TWorldMapRenderProviderE
0x1ce1b60  N5tibia8worldmap17TWorldMapViewportE
0x1ce1c00  N5tibia8worldmap16TWorldMapStorageE
```

It also contains the concrete instantiated container type:

```text
std::unordered_map<
  tibia::worldmap::TWorldMapCoordinate,
  std::shared_ptr<tibia::worldmap::TWorldMapTile>, ...>
```

and related hash-node instantiations plus `shared_ptr<TWorldMapTile>` / `shared_ptr<TWorldMapEntity>` strings.

Classification:

```yaml
FACT:
  - the exact binary instantiates the coordinate-to-shared-tile unordered_map type
  - storage/viewport/camera/protocol/render/picker each have separately named shared_ptr counted-control-block instantiations
INFERENCE:
  - separately allocated/shared-lifetime worldmap subsystems are likely; a single global dimension integer controlling every subsystem is therefore less plausible
  - the coordinate->tile unordered_map is a strong backing-storage candidate for worldmap tiles
UNKNOWN:
  - whether that unordered_map is a direct member of TWorldMapStorage
  - bucket/reserve/capacity/eviction policy
  - exact ownership/member-pointer graph among the eight target classes
```

Additional exact semantic leads include:

```text
TWorldMapSubfieldCoordinate
TWorldMapCoordinate
TWorldMapCalculateTileFunctionService
TWorldMapGetByteForStackPosition
TWorldMapGetCurrentCoordinate
TWorldMapGetItemPropertiesService
TCreatureHUDRenderProvider
TCreatureHUDOverlayController
TWorldMapGameActionProvider
TWorldMapGameActionHandler
handleTeleportToCoordinateAction
handleAddBeneathMiddleWorldmapMessageGameAction
```

These names enlarge the consumer surface for later xref recovery but do not by themselves prove call edges.

## Picker namespace correction

The broader census proves exact `tibia::worldmap::TWorldMapPicker` RTTI/shared-control-block strings. A separate earlier search also surfaced a tooltip-side picker-related type. These must not be conflated; this viewport task's requested `TWorldMapPicker` target is directly represented in `tibia::worldmap` at `0x1cdb600`.

## Updated partial dependency graph

```text
retained map event source(s)
    BP1 0xcecc70 observer-assigned CreateOnMap
    BP2 0xcecf40 observer-assigned ChangeOnMap
       |  shared owner+0x10 -> virtual slot +0xa0
       |  event +0x18/+0x20/+0x28 reads
       +--> common exact helper lead 0xceca50 (BP2 proven; BP1 continuation not fully retained)
       +--> further direct/virtual consumers UNKNOWN

protocol/message semantic surface
    TWorldmapProtocolMessageHandler
       +--> concrete parser/update edge to BP1/BP2: NOT_YET_PROVEN

storage semantic surface
    TWorldMapStorage
       +--> coordinate -> shared_ptr<TWorldMapTile> unordered_map: STRONG_CANDIDATE, direct member UNKNOWN

extent/subfield/viewport
    TWorldMapExtent / TWorldMapSubfieldExtent / TWorldMapViewport
       +--> dimension fields: UNKNOWN
       +--> map-event helper relationship: UNKNOWN

render/camera/picker
    TWorldMapRenderProvider / TWorldMapCamera / TWorldMapPicker
       +--> separate shared-lifetime type surfaces: PROVEN
       +--> extent/viewport field consumers: UNKNOWN
```

## Static frontier after retained-evidence recovery

The exact-client hosted input blocker remains real, but it no longer means that no static progress is possible. Retained artifacts provide a second safe research path.

```yaml
STATIC_PATCH_GRAPH_READY: false
MORE_STATIC_RE_NEEDED: true
RUNTIME_DISCRIMINATOR_REQUIRED: false
BLOCKED_ON_NEW_EXACT_BINARY_MATERIALIZATION: true
RETAINED_EVIDENCE_RESEARCH_PATH: active
```

Next retained-evidence actions:

1. recover original observer-source provenance if any artifact/branch preserved it;
2. correlate exact BP/helper static addresses (`0xceca50`, `0xcecc70`, `0xcecf40`, `0xcd4e20`, `0xcec8d0`) against retained static/disassembly artifacts;
3. search retained exact-static artifacts for constructor/vtable/control-block xrefs around the eight target types;
4. audit retained type census for fixed-array/container/coordinate-area clues;
5. continue to mark every unproven field/edge `UNKNOWN` rather than using runtime as a shortcut.

No GUI/runtime escalation is justified by this checkpoint.