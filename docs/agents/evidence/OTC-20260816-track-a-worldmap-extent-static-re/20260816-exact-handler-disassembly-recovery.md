# OTC-20260816 — exact worldmap handler/disassembly recovery

```yaml
evidence_date: 2026-08-16
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
execution_mode: retained_same_repo_exact_client_evidence
runtime_used_this_task: false
client_executed_this_task: false
client_bytes_modified: false
owner_funded_ai_api_authorized: false
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

This checkpoint consumes historical same-repository evidence only. No new Synology job was launched for static RE and no current runtime state is inferred from the historical runner.

## Producer-source provenance recovered

Historical source commits recover the observer labels that were previously only visible in retained TSV output.

FACT:

```yaml
runtime_v2_source_commit: caa938463356ce9a8ece92e9ae908ba507f501a9
persistent_observer_source_commit: 734f845deace5a26efa09b96a168bea0c05272f0
persistent_observer_verification_commit: b15b41c8f14f4c148d163990031b8c3be6278343
observer_breakpoints:
  CreateOnMap: 0x00cecc70
  ChangeOnMap: 0x00cecf40
  DeleteOnMap: 0x00cd4e20
  FullMap: 0x00cec8d0
  MapDescription_strip_capture: 0x019a8ea3
```

The source literally constructed those breakpoints with the human-readable labels above. Therefore the label-to-offset mapping is no longer provenance-UNKNOWN. The labels remain **research observer labels**; they are not promoted to compiler/debug symbols.

## Exact fenced handler disassembly

Historical commit `c6aa95a18030ba14e8f780b5cd9ec135723a4cc2` created a fenced GDB disassembly workflow. Historical run `31804083206`, job `94778661881`, echoed the exact client SHA-256 above and completed successfully.

FACT — exact disassembly ranges retained in the job log:

```text
CreateOnMap    0x00cecb80..0x00ced150
ChangeOnMap    0x00cece50..0x00ced4b0
DeleteOnMap    0x00cd4d30..0x00cd54a0
FullMap        0x00cec790..0x00cecaa0
MapDescription 0x019a89c0..0x019a9000
```

The ranges deliberately include neighboring functions. Function boundaries below are asserted only where the retained machine code has a clear prologue/return boundary or where the observer source points at the entry.

## `FullMap` observer target — static `0xcec8d0`

The observer target at `0xcec8d0` has a normal function prologue and directly consumes the event-like second argument.

FACT:

```text
resolved_event = event+0x20 (null falls back to static object 0x313a820)
resolved_event DWORD +0x18 -> ecx
resolved_event DWORD +0x1c -> edx
resolved_event DWORD +0x20 -> esi
resolved_event QWORD +0x18 -> rax
owner QWORD +0x98 <- rax
owner DWORD +0xa0 <- esi
```

The same function builds a local object and performs:

```text
local DWORD #1 = event_dword_0x18 << 5
local DWORD #2 = event_dword_0x1c << 5
local DWORD #3 = event_dword_0x20
owner+0x70 -> virtual slot +0x60(local)
```

It then calls static `0xcdb770(owner)`, iterates an RB-tree reachable through `owner+0x30`, and for matching polymorphic entries resets byte `+0x130`.

Later it:

```text
compares owner DWORD +0xa0 against literal 7
sets a boolean to (owner+0xa0 > 7)
calls 0x19a8a80(..., boolean)
```

Classification:

```yaml
FACT:
  - two adjacent event integers are multiplied by exactly 32 before a worldmap-owner virtual call
  - the same two integers are copied together into owner+0x98 as one QWORD
  - a third integer is copied into owner+0xa0 and compared with 7
INFERENCE:
  - the pair at +0x18/+0x1c is coordinate/extent-like and the <<5 strongly supports a 32-tile subfield-to-tile conversion
  - owner+0x98/+0xa0 forms a persistent three-integer map-state tuple
UNKNOWN:
  - exact C++ field names
  - whether the +0x18/+0x1c pair is position, extent, subfield coordinate, or another packed geometry structure
  - whether owner+0xa0 is literally a Z/floor value despite the comparison with 7
```

## `MapDescription` — static `0x19a8a80`

`FullMap` directly calls `0x19a8a80`. The retained range proves substantial coordinate-generation arithmetic inside this function.

For a per-descriptor object held in `rbx`, the code directly reads:

```text
DWORD +0x08
DWORD +0x0c
DWORD +0x10
DWORD +0x38 -> r8d
DWORD +0x3c -> r9d
DWORD +0x40 -> esi
DWORD +0x48 -> edi
```

The exact arithmetic includes:

```text
product = DWORD[+0x3c] * DWORD[+0x38]
linear_value / product
signed division by DWORD[+0x40]
linear_value / DWORD[+0x3c]
signed division by DWORD[+0x38]
coordinate_1 += DWORD[+0x0c]
coordinate_2 += DWORD[+0x08]
```

When the boolean propagated from `owner+0xa0 > 7` is set, the path additionally incorporates `DWORD[+0x10]`, the remainder from division by `+0x40`, and `DWORD[+0x48]` into both generated coordinates.

The generated local structure is written as three consecutive DWORDs and passed to the object at `owner+0x10` through virtual slot `+0xa0`.

Classification:

```yaml
FACT:
  - descriptor fields +0x38/+0x3c/+0x40 participate directly as multiplicative/divisor grid parameters
  - descriptor +0x08/+0x0c are additive coordinate bases
  - descriptor +0x10/+0x48 participate in the alternate/floor-dependent transform
  - the result is a three-DWORD coordinate-like local consumed by owner+0x10 virtual slot +0xa0
INFERENCE:
  - +0x38/+0x3c/+0x40 are strong dimension/stride/depth candidates in the full-map description layout
  - this is a protocol-to-worldmap geometry surface and a likely dependency for any viewport/extent patch
UNKNOWN:
  - semantic names and units of each descriptor field
  - which fields correspond specifically to `TWorldMapExtent` versus `TWorldMapSubfieldExtent`
  - whether any of these fields is a fixed baseline viewport width/height
```

The historical strip-capture breakpoint `0x19a8ea3` lies inside this same function. At that point the code reads a nested item DWORD `+0x30` immediately before calling common helper `0xceca50`; this explains why the retained runtime strip rows and this static parser path can be correlated without promoting the row geometry to object-field semantics.

## `CreateOnMap` — static `0xcecc70`

FACT:

```text
owner = rdi
event = rsi
reads event +0x18
reads owner +0x10
resolved event+0x18 object -> QWORD +0x18 and DWORD +0x20
owner+0x10 object -> virtual slot +0xa0
reads event DWORD +0x28
reads event pointer +0x20
secondary object reads +0x08, +0x28 and +0x30
calls helper 0xceca50
result dispatches through virtual slot +0x90 or +0x98 depending on event+0x28 == 0xff
owner+0xd8 dependency is compared through a type/vfunc guard and its DWORD +0x98 is compared with the local map-state value
```

Direct static calls/leads include `0x1b13c80`, `0x1ab4e50`, `0xceca50`, and globals/static objects `0x313a820`, `0x30874a8`, `0x2f615a0`, `0x314b480`, `0x312faa8`.

## `ChangeOnMap` — static `0xcecf40`

FACT:

```text
tests BYTE[event+0x10] & 1
common/true path reads event+0x18, event+0x20, event+0x28
reads owner+0x10
owner+0x10 object -> virtual slot +0xa0
calls 0x1822ec0
calls common helper 0xceca50
result uses virtual slot +0xf0
owner+0xd8 path uses the same +0x98 comparison family as CreateOnMap
```

The flag-clear path beginning near `0xced0e0` consumes event+0x20, globals `0x3193220` / `0x3193228`, calls `0x1aac200` and `0x182ae20`, then dispatches through owner+0x80 object's virtual slot `+0xf0`.

## `DeleteOnMap` — static `0xcd4e20`

FACT:

```text
reads selector DWORD event+0x1c
selector 1 path reads event pointer +0x10
selector 2 path uses DWORD event+0x10 as an alternate value
owner+0x10 path again reaches virtual slot +0xa0
selector-1 path consumes a byte at +0x20 of the selected event object
owner+0xd8 path again performs the +0x98 comparison family and may call virtual slot +0x88
fallback/alternate path dispatches through owner+0x30 virtual slot +0xd8
```

This establishes that Create/Change/Delete all share a worldmap-owner dependency and a repeated map-state comparison path rather than being independent event handlers.

## Neighboring constructor-like surface — static `0xcd4d70`

This is a distinct function before the DeleteOnMap observer target.

FACT:

```text
calls QObject constructor
writes vptr-like static 0x3074848
BYTE +0x20 = 0
QWORD +0x10 = 0
QWORD +0x18 = 0
QWORD +0x28 = 0x2f61cc8
QWORD +0x30 = 0
QWORD +0x38 = 0
QWORD +0x40 = 0
```

INFERENCE: constructor/default-writer candidate for a protocol/event-side helper object. Exact class identity remains UNKNOWN.

## Neighboring hash-table rebuild surface — static `0xced1b0`

This is a separate function after the `ChangeOnMap` observer function returns.

FACT:

```text
requires object pointers at +0x10, +0x20 and +0x30 for its main path
uses object +0x48 as a bucket-array base candidate
uses object +0x50 in an 8-byte bucket memset size expression
uses object +0x58 as a linked-node head candidate
uses object +0x60 as a count/state field
clears the bucket array with memset(base, 0, +0x50 * 8)
sets +0x58 = 0 and +0x60 = 0 on clear
allocates replacement nodes of exactly 0x20 bytes
copies source node DWORD +0x08 and 16 bytes at +0x10
computes bucket placement with unsigned div by the retained bucket-count value
```

Classification:

```yaml
FACT:
  - this function rebuilds a bucketed linked-node structure with 0x20-byte nodes
INFERENCE:
  - the structure is strongly consistent with an `unordered_map` implementation
  - it is a strong candidate to correlate with the exact-static instantiated `unordered_map<TWorldMapCoordinate, shared_ptr<TWorldMapTile>, ...>` type already retained in artifact 9246756211
UNKNOWN:
  - owning C++ class
  - whether this is directly `TWorldMapStorage`
  - eviction/reserve/load-factor semantics
```

This weakens the hypothesis that the visible-world storage is one fixed rectangular array, while leaving parser/render scratch buffers and extent structures open to fixed dimensions.

## Common helper `0xceca50`

The retained FullMap range covers the beginning of this function.

FACT:

```text
rdi = output/result-like argument
rsi = owner-like argument
rdx = source-like argument
rcx = second source-like argument
uses rdx+0x10
reads global DWORD 0x3193220
calls 0x1aab810
on one path reads owner +0x50 and owner +0x60
owner+0x50 object -> virtual slot +0xa0
owner+0x60 object -> virtual slot +0x10
```

The current retained range ends before the helper completes. Its full semantics remain UNKNOWN and it remains a high-value xref/disassembly target.

## Patch-graph progress

```text
FullMap event
  -> persistent map-state tuple owner+0x98/+0xa0
  -> two payload integers scaled by 32
  -> owner+0x70 virtual consumer
  -> 0x19a8a80 MapDescription-like coordinate generation
       -> descriptor grid/divisor fields +0x38/+0x3c/+0x40/+0x48
       -> additive bases +0x08/+0x0c/+0x10
       -> generated three-DWORD coordinate
       -> owner+0x10 virtual +0xa0
       -> nested records
       -> 0xceca50 common helper

Create/Change/Delete
  -> same owner+0x10 virtual +0xa0 family
  -> same owner+0xd8 map-state comparison family
  -> 0xceca50 for Create/Change

neighbor 0xced1b0
  -> bucket-array/node rebuild
  -> candidate storage/unordered-map correlation
```

This is a materially stronger protocol/storage-side graph than the earlier 256-byte prefix checkpoint. It is still insufficient for `STATIC_PATCH_GRAPH_READY` because target type ownership, viewport dimension fields, render/camera/picker clipping/transform consumers, and complete fixed-bound/allocation auditing remain unresolved.

## Next deterministic static targets

1. recover the remainder/xrefs of `0xceca50` and name its owner dependencies;
2. correlate `0xced1b0` with `TWorldMapStorage` RTTI/vtables or the coordinate-to-tile unordered-map instantiation;
3. recover typeinfo/vtables/constructors for `TWorldMapExtent`, `TWorldMapSubfieldExtent`, `TWorldMapViewport`, `TWorldMapStorage`, `TWorldMapRenderProvider`, `TWorldMapCamera` and `TWorldMapPicker`;
4. follow the `owner+0x70`, `owner+0x10`, `owner+0x80`, `owner+0xd8` virtual consumers into protocol/storage/render ownership;
5. inventory all literals, shifts, loop bounds, allocation sizes and clipping tests tied to the recovered geometry before any mutation design.
