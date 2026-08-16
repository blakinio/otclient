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

The task remains active as `MORE_STATIC_RE_NEEDED`. Fresh GitHub-hosted staging of the exact installed `15.32.df7b29` game-client ELF remains blocked by the official CDN, but same-repository retained exact-client evidence has now yielded a materially stronger protocol/storage-side graph.

The owner-supplied current Linux archive was also preserved as an exact GitHub Actions artifact. Static inspection proves that archive is the Tibia launcher/updater distribution, not the historical 51,965,216-byte installed game-client ELF, so it is not silently substituted for the exact-client fence.

## Exact installed-client fence

```yaml
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_platform: official_native_linux_only
```

No current runtime identity is inferred from historical PID/PIE/display/session data.

## Owner-supplied official Linux package

The owner supplied `tibia.x64.tar.gz` on 2026-08-16.

```yaml
size_bytes: 29477141
sha256: 04a87c801d3855f4da1b07e201dff1f79acc8528c57c984131c3a2a88cb60ea7
contained_Tibia_Tibia_size: 1460808
contained_Tibia_Tibia_sha256: a5fc6e8ee8246868263c438539a54ea045bd048a1bea45f968fc2f498b682ca0
classification: launcher_updater_distribution
```

The exact archive was reproduced from the official CipSoft source, fenced by size and SHA-256, stored in the same repository as GitHub Actions artifact `9264329820`, downloaded back, and verified bit-identical with the owner upload. The binary is intentionally not committed to public Git history.

A GitHub-hosted probe using launcher-derived correct official manifest paths returned Cloudflare HTTP 403 for `tibiametadata.json`, Linux `package.json`, and `package.json.version`; therefore repeating the same request pattern is not justified.

## Geometry evidence upgrade

Retained artifact `9227370490` (`track-a-persistent-provenance-dump`, run `31821458677`, digest `sha256:991f5c22a7ffc1d23c6597307a49728b363863a5acd6dd754bff1222404c8e2d`) contains 90 raw strip rows.

Direct facts:

```text
Z=7, Y=32502, class=0: X=32537..32554 -> 18 consecutive X
Z=7, Y=32516, class=0: X=32537..32554 -> 18 consecutive X
Y delta between those two groups: 14
```

This proves the raw 18/14 geometry relationship but does **not** yet prove literal stored `width=18` / `height=14` fields.

## Observer producer-source provenance recovered

Historical workflow source commits recover the exact research observer mapping:

```text
CreateOnMap  -> 0x00cecc70
ChangeOnMap  -> 0x00cecf40
DeleteOnMap  -> 0x00cd4e20
FullMap      -> 0x00cec8d0
MapDescription strip capture -> 0x019a8ea3
```

Producer-source commits include `caa938463356ce9a8ece92e9ae908ba507f501a9` and `734f845deace5a26efa09b96a168bea0c05272f0`; verification commit `b15b41c8f14f4c148d163990031b8c3be6278343` confirms the persistent observer design. These names are research labels, not compiler/debug symbols.

## Exact fenced handler disassembly

Historical commit `c6aa95a18030ba14e8f780b5cd9ec135723a4cc2` created a SHA-fenced GDB disassembly job. Run `31804083206`, job `94778661881`, completed successfully against the exact installed-client SHA and retained these ranges in its job log:

```text
CreateOnMap    0x00cecb80..0x00ced150
ChangeOnMap    0x00cece50..0x00ced4b0
DeleteOnMap    0x00cd4d30..0x00cd54a0
FullMap        0x00cec790..0x00cecaa0
MapDescription 0x019a89c0..0x019a9000
```

### FullMap observer target `0xcec8d0`

Direct machine-code facts:

```text
resolved_event = event+0x20, with static fallback 0x313a820
resolved_event DWORD +0x18 -> ecx
resolved_event DWORD +0x1c -> edx
resolved_event DWORD +0x20 -> esi
resolved_event QWORD +0x18 -> rax
owner QWORD +0x98 <- rax
owner DWORD +0xa0 <- esi
```

The function constructs a local triple where the first two values are:

```text
(event DWORD +0x18) << 5
(event DWORD +0x1c) << 5
```

and the third is `event DWORD +0x20`, then passes that structure to the object at `owner+0x70` through virtual slot `+0x60`.

It also calls `0xcdb770(owner)`, iterates an RB-tree via `owner+0x30`, and later derives a boolean from `owner DWORD +0xa0 > 7` before calling `0x19a8a80`.

**FACT:** two adjacent payload integers are converted by exactly ×32 before a worldmap-owner virtual consumer.

**INFERENCE:** this is strongly consistent with 32-tile subfield granularity and establishes a protocol-side geometry conversion that any extent change must respect.

**UNKNOWN:** exact field names and whether the source pair represents coordinate, extent, or another subfield-space geometry tuple.

### MapDescription `0x19a8a80`

The function directly reads per-descriptor fields:

```text
+0x08, +0x0c, +0x10,
+0x38, +0x3c, +0x40, +0x48
```

The exact arithmetic includes:

- product `DWORD[+0x3c] * DWORD[+0x38]`;
- division of a linear value by that product;
- signed division by `DWORD[+0x40]`;
- division by `DWORD[+0x3c]` followed by signed division by `DWORD[+0x38]`;
- additive coordinate bases from `+0x0c` and `+0x08`;
- alternate/floor-dependent incorporation of `+0x10`, a division remainder and `+0x48` when the FullMap boolean is set.

The generated local is three consecutive DWORDs and is passed through the object at `owner+0x10`, virtual slot `+0xa0`.

**FACT:** `+0x38/+0x3c/+0x40` directly participate as multiplicative/divisor grid parameters; `+0x08/+0x0c` are additive coordinate bases; `+0x10/+0x48` participate in the alternate transform.

**INFERENCE:** this is a concrete protocol-to-worldmap geometry surface and a high-value candidate for `TWorldMapExtent` / `TWorldMapSubfieldExtent` correlation.

**UNKNOWN:** semantic names, units and which field — if any — stores the baseline visible viewport dimensions.

### CreateOnMap `0xcecc70`

FACT:

- reads event `+0x18`, `+0x20`, `+0x28`;
- loads `owner+0x10` and dispatches through virtual slot `+0xa0`;
- follows the object from event `+0x20` and reads its `+0x08/+0x28/+0x30`;
- calls common helper `0xceca50`;
- dispatches result through virtual slot `+0x90` or `+0x98` depending on event `+0x28 == 0xff`;
- uses an `owner+0xd8` dependency whose `+0x98` state participates in a repeated map-state comparison family.

### ChangeOnMap `0xcecf40`

FACT:

- tests `BYTE[event+0x10] & 1`;
- common path reads event `+0x18/+0x20/+0x28`;
- uses the same `owner+0x10 -> vslot +0xa0` family;
- calls `0x1822ec0` and common helper `0xceca50`;
- later uses virtual slot `+0xf0`;
- repeats the `owner+0xd8` / `+0x98` state-comparison family.

The flag-clear branch also uses globals `0x3193220` / `0x3193228`, calls `0x1aac200` and `0x182ae20`, then reaches the object at `owner+0x80`, virtual slot `+0xf0`.

### DeleteOnMap `0xcd4e20`

FACT:

- selector is `DWORD event+0x1c`;
- selector-1 path uses event pointer `+0x10`;
- selector-2 path uses `DWORD event+0x10` as an alternate value;
- same `owner+0x10 -> vslot +0xa0` family appears;
- the repeated `owner+0xd8` / `+0x98` map-state comparison family appears again;
- alternate path reaches `owner+0x30 -> vslot +0xd8`.

Create/Change/Delete therefore share concrete worldmap-owner dependencies rather than being independent parsing islands.

## Storage/container lead `0xced1b0`

A neighboring function after the ChangeOnMap function returns rebuilds a bucketed linked-node structure:

```text
object +0x48 -> bucket-array base candidate
object +0x50 -> bucket count/size term; memset size is +0x50 * 8
object +0x58 -> node-head candidate
object +0x60 -> count/state
replacement node allocation size = 0x20 bytes
bucket placement uses unsigned division by retained bucket-count value
```

It clears the bucket array, resets `+0x58/+0x60`, then rebuilds 0x20-byte nodes from source state.

**INFERENCE:** strongly consistent with an `unordered_map` implementation and therefore a strong correlation candidate for the exact-static instantiated `unordered_map<TWorldMapCoordinate, std::shared_ptr<TWorldMapTile>, ...>` type.

**UNKNOWN:** direct owning class, whether this is literally a `TWorldMapStorage` member operation, and reserve/load-factor/eviction policy.

## Rich exact-static census

Retained artifact `9246756211` directly preserves exact type/control-block strings for:

- `TWorldMapExtent`;
- `TWorldMapSubfieldExtent`;
- `TWorldMapViewport`;
- `TWorldMapStorage`;
- `TWorldmapProtocolMessageHandler`;
- `TWorldMapRenderProvider`;
- `TWorldMapCamera`;
- `TWorldMapPicker`;
- separate shared-pointer counted-control-block instantiations for storage, viewport, protocol handler, render provider, camera and picker;
- `std::unordered_map<TWorldMapCoordinate, std::shared_ptr<TWorldMapTile>, ...>` and related hash-node/shared tile/entity instantiations.

Existing typeinfo-name relocation leads include:

```text
0x3089b78 -> 0x1cddd20  TWorldMapRenderProvider typeinfo-name
0x308b598 -> 0x1ce1b60  TWorldMapViewport typeinfo-name
```

ABI candidate typeinfo starts `0x3089b70` and `0x308b590` remain hypotheses until their surrounding RTTI/vtable graph is recovered.

## Updated partial dependency graph

```text
FullMap event @0xcec8d0
  -> persistent map-state tuple owner+0x98/+0xa0
  -> two payload integers <<5 (= x32)
  -> owner+0x70 virtual slot +0x60
  -> 0x19a8a80 MapDescription
       -> descriptor grid fields +0x38/+0x3c/+0x40/+0x48
       -> coordinate bases +0x08/+0x0c/+0x10
       -> generated three-DWORD coordinate-like structure
       -> owner+0x10 virtual slot +0xa0
       -> nested record handling
       -> common helper 0xceca50

Create/Change/Delete
  -> owner+0x10 virtual slot +0xa0 family
  -> repeated owner+0xd8 map-state comparison family
  -> 0xceca50 used by Create/Change

neighbor 0xced1b0
  -> bucketed 0x20-byte node rebuild
  -> strong unordered_map/storage correlation candidate

TWorldMapExtent / SubfieldExtent / Viewport
  -> exact semantic identities present
  -> concrete field ownership still UNKNOWN

RenderProvider / Camera / Picker
  -> exact semantic/shared-lifetime identities present
  -> clipping/culling/transform readers still UNKNOWN
```

## Current patch graph matrix

| Graph element | Status |
|---|---|
| target subsystem/type presence | PROVEN |
| separate shared-control-block instantiations | PROVEN for storage/viewport/protocol/render/camera/picker |
| raw 18-sample geometry and Y delta 14 | PROVEN |
| observer label-source mapping | PROVEN as research-source provenance |
| exact bounded handler disassembly | PROVEN from exact SHA-fenced historical job log |
| FullMap payload ×32 conversion | PROVEN |
| MapDescription descriptor grid/divisor accesses | PROVEN |
| shared owner+0x10 virtual slot +0xa0 path | PROVEN across FullMap/Create/Change/Delete family |
| helper `0xceca50` involvement | PROVEN for Create/Change and nested description path |
| hash-table rebuild `0xced1b0` | PROVEN structure; storage identity INFERENCE |
| literal viewport width/height fields | UNKNOWN |
| exact extent/subfield field semantics | UNKNOWN |
| storage hash map direct ownership | INFERENCE / UNKNOWN direct-member relation |
| constructor/default dimension writers | UNKNOWN |
| all material readers/writers | UNKNOWN |
| fixed arrays/capacities/loop bounds/masks | INCOMPLETE |
| render iteration/clipping/culling | UNKNOWN |
| camera projection/scale coupling | UNKNOWN |
| picker bounds/screen-world transform | UNKNOWN |
| concrete safe patch sites | UNKNOWN |

## Fresh exact-client input blocker

The hosted blocker is now better characterized:

- PR #310 established prior DNS/HTTP-403 failures;
- task run `31947523640`, job `95165795953` produced `INPUT_BLOCKED`, artifact `9263709952`;
- independent P0 run `31947502633`, job `95165743019` produced the same class of blocker;
- current launcher-derived correct-manifest probe run `31949948886` returned Cloudflare HTTP 403 for all three correct official manifest endpoints.

No identical request retry is justified. No Synology static-analysis fallback is used.

## Next research frontier

1. recover the remainder and xrefs of common helper `0xceca50`;
2. correlate `0xced1b0` with `TWorldMapStorage` RTTI/vtable or the coordinate-to-tile unordered-map type;
3. recover concrete typeinfo/vtables/constructors for `TWorldMapExtent`, `TWorldMapSubfieldExtent`, `TWorldMapViewport`, `TWorldMapStorage`, `TWorldMapRenderProvider`, `TWorldMapCamera` and `TWorldMapPicker`;
4. follow `owner+0x70`, `owner+0x10`, `owner+0x80`, `owner+0xd8` virtual consumers into protocol/storage/render ownership;
5. inventory fixed literals, shifts, loop bounds, allocation sizes and clipping tests tied to the recovered geometry;
6. only after the complete dependency graph is coherent may a mutation design be proposed.

No GUI/runtime discriminator is currently required, and no client-byte mutation is authorized.