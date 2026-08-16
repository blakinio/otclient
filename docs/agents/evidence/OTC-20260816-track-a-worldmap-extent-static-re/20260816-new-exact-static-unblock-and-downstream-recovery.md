# Track A worldmap exact-static unblock and downstream recovery

Date: 2026-08-16  
Consumer task: `OTC-20260816-track-a-worldmap-extent-static-re` / Draft PR #367  
Producer: `OTC-20260816-track-a-worldmap-exact-static-evidence` / Draft PR #437

## Admission and provenance

This continuation remains `runtime_access: none` and performs static/artifact analysis only. It does not execute or modify the client, access process memory, canonical runtime state, X11/VNC, login/session/gameplay state, or use owner-funded Codex/OpenAI API/tokens.

The new source is the bounded sanitized exact-client producer from PR #437. Its task explicitly records a coordinator-approved read-only file-staging exception, forbids client/process/canonical-runtime access, and declares `WORLD_MAP_STATIC_EVIDENCE_READY: true` for consumer PR #367.

Exact client fence:

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux
```

Producer source staging:

```text
run      31972743782
job      95227595548
result   SUCCESS
artifact 9270235755
sha256   039d22fe5f88a07784c4ddc32cf6b1d9c2d07a34e90ed5902ffd21d3acd5735b
```

Hosted recovery/validation:

```text
run      31972915689
job      95228024727
result   SUCCESS
artifact 9270276361
sha256   0dc8d0a44e5a2550ef79c219bda14787796ef7accc0ab1627fecd7c6d55330bc
```

The final artifact was independently downloaded through the GitHub connector in this continuation. Its ZIP SHA-256 is exactly `0dc8d0a44e5a2550ef79c219bda14787796ef7accc0ab1627fecd7c6d55330bc`; the source artifact ZIP independently hashes to `039d22fe5f88a07784c4ddc32cf6b1d9c2d07a34e90ed5902ffd21d3acd5735b`. The retained hosted validator reports:

```text
WORLD_MAP_STATIC_HOSTED_VALIDATION=PASS
WORLD_MAP_STATIC_HOSTED_DISASSEMBLY_BACKEND=gnu_objdump_bounded_binary
WORLD_MAP_STATIC_IDENTITY_WINDOWS_RECOVERED=3
WORLD_MAP_STATIC_GEOMETRY_OFFSETS_WITH_EVIDENCE=+0x18,+0x1c,+0x30,+0x34,+0x48,+0x4c
WORLD_MAP_STATIC_PRIORITY_0X48_18_WRITE=false
WORLD_MAP_STATIC_PRIORITY_0X4C_14_WRITE=false
WORLD_MAP_STATIC_EVIDENCE_READY=true
```

No exhausted historical artifact set was rescanned and no CDN fetch was repeated.

## FACT — all three identity windows are recovered

| Window / address point | Exact bytes | Typeinfo | Exact RTTI identity |
|---|---|---|---|
| `0x030871c8..0x030871d7` → `0x030871d8` | `0000000000000000b85f080300000000` | `0x03085fb8` | `tibia::worldmap::TWorldmapProtocolMessageHandler` |
| `0x0308ce60..0x0308ce6f` → `0x0308ce70` | `0000000000000000f0b5080300000000` | `0x0308b5f0` | `tibia::worldmap::TWorldMapStorage` |
| `0x02f683c0..0x02f683cf` → `0x02f683d0` | `000000000000000020fb070300000000` | `0x0307fb20` | `std::_Sp_counted_ptr_inplace<tibia::worldmap::TWorldMapStorage,...>` |

Each header has offset-to-top `0`; the typeinfo and type-name relations are backed by `.rela.dyn` relocation evidence in the sanitized producer bundle.

### Material correction to the old #367 hypothesis

**FACT:** the historical `owner+0x10` object carrying `+0x48=18`, `+0x4c=14` is `TWorldMapStorage`, not `TWorldMapViewport`.

**FACT:** its adjacent counted control block with address-point `0x02f683d0` is the counted allocation wrapper for `TWorldMapStorage`.

The previous `VERY_STRONG_INFERENCE` assigning this exact object/control pair to `TWorldMapViewport` is superseded and must not be used further.

## FACT — Storage geometry layout and exact writers

Exact `TWorldMapStorage` constructor anchor: `0x00cbf37a`.

The constructor installs Storage vptr `0x0308ce70` and initializes three geometry QWORD groups:

```text
Storage+0x18 QWORD = 0   -> DWORD +0x18/+0x1c
Storage+0x30 QWORD = 0   -> DWORD +0x30/+0x34
Storage+0x48 QWORD = 0   -> DWORD +0x48/+0x4c
```

It also installs exact `TWorldMapExtent` address-point `0x02f61578` at `Storage+0x40`. Therefore `Storage+0x48/+0x4c` are the first two DWORD payload positions inside the embedded exact `TWorldMapExtent` beginning at `Storage+0x40`.

Storage vtable slot 12 resolves to `0x00cc6cd0`. It copies the incoming geometry into the Storage object:

```text
[rsi+0x08] QWORD -> Storage+0x18
[rsi+0x20] QWORD -> Storage+0x30
[rsi+0x38] QWORD -> Storage+0x48
```

The same routine copies the associated DWORD components at input `+0x10/+0x28/+0x40/+0x48` into Storage `+0x20/+0x38/+0x50/+0x58`.

**FACT:** all requested geometry offsets `+0x18/+0x1c/+0x30/+0x34/+0x48/+0x4c` now have direct constructor and dynamic mutation coverage.

**FACT:** `+0x48/+0x4c` are written together by the QWORD copy at `0x00cc6d2c` from input `[rsi+0x38]`. The retained `18/14` are therefore not immutable constructor literals.

**UNKNOWN:** the upstream producer that computes/configures/parses the input QWORD at `rsi+0x38` in the dynamic event that produced `18/14` is not staged in this bundle.

## FACT — the first two coordinate groups are half-open 3D bounds

Storage vtable slot 14 resolves to `0x00cb01d0`. Its comparisons establish the following containment contract:

```text
Storage+0x18 <= x < Storage+0x30
Storage+0x1c <= y < Storage+0x34
Storage+0x20 <= z < Storage+0x38
```

This upgrades the old lower/upper-bound interpretation from inference to direct static evidence. For the retained runtime instance:

```text
32555 - 32537 = 18
32517 - 32503 = 14
```

The `18/14` pair at `+0x48/+0x4c` is separate embedded `TWorldMapExtent` payload; exact source-level member names and units remain unknown.

## FACT — Storage extent update drives node eviction and live count changes

The same Storage slot-12 mutator (`0x00cc6cd0`) traverses the Storage-owned ordered node structure after geometry replacement. The tree/sentinel surface uses Storage fields around `+0x68/+0x70/+0x78`, and out-of-bounds nodes are removed when their coordinate payload falls outside the new half-open bounds. Removal decrements `Storage+0x88` with:

```text
subq $0x1, [Storage+0x88]
```

Storage slot 17 (`0x00cc7d60`) reads `Storage+0x88` when sizing/exporting its node collection and traverses the same tree. Storage slot 18 (`0x00cc80c0`) also traverses the tree and filters/compares node coordinates against an extent-like input.

**FACT:** Storage extent updates are coupled to out-of-bounds entry eviction/removal, and `Storage+0x88` participates as the live collection-count/size value.

**UNKNOWN:** no maximum-capacity or eviction-policy limit is proven. Do not reinterpret the live count as a fixed capacity.

## FACT — coordinate-indexed Storage lookup is not a fixed 18×14 loop

Additional staged Storage virtual code walks an ordered structure rooted/sentinelled by the same Storage state and compares coordinate-like DWORDs in nodes. Matching nodes expose an object pointer subsequently used for virtual dispatch.

This establishes coordinate-indexed Storage lookup/traversal. The staged paths are extent-aware and tree-based; they do not expose a fixed loop bound of 18 or 14.

The exact C++ container/template type and exact pointed-to tile/content class are not promoted from these bounded bytes alone.

## FACT — exact `TWorldMapViewport` is a separate object with its own geometry computation

The same sanitized window that contains the Storage constructor also stages a distinct constructor beginning at `0x00cbf680` whose primary address-point is exact `TWorldMapViewport` vptr `0x0308c9a8`.

That constructor installs exact `TWorldMapExtent` address-point `0x02f61578` at `Viewport+0x38` and initializes its own fields, including:

```text
Viewport+0x48 = 8
Viewport+0x60 = 4
```

The following routine at `0x00cbf700` consumes Viewport fields including `+0x10/+0x18/+0x58`, recomputes geometry stored around `+0x28/+0x40`, resets `+0x48=8`, and performs signed arithmetic including an arithmetic right shift by 5.

**FACT:** `TWorldMapViewport` has its own independently computed geometry/extent state and is distinct from the historical Storage object that carried the retained `18/14` pair.

**INFERENCE:** the shift-by-5 is consistent with the already observed worldmap ×32 grid/scale boundary, but the exact source-level field names and semantic units are not proven here.

**UNKNOWN:** this bounded bundle does not directly prove the exact ownership/call edge that links Storage to this Viewport instance.

## Follow-on exact RTTI/vtable anchors

The producer also supplies exact anchors for the remaining downstream classes:

| Type | Typeinfo | Address-point | First staged slot |
|---|---:|---:|---:|
| `TWorldMapViewport` | `0x0308b590` | `0x0308c9a8` | `0x00dee920` |
| `TWorldMapRenderProvider` | `0x03089b70` | `0x02f6c258` | `0x00820970` |
| `TWorldMapCamera` | `0x03080500` | `0x03083968` | `0x00dedda0` |
| `TWorldMapPicker` | `0x03086888` | `0x02f6b7c8` | `0x008205c0` |
| `TWorldMapExtent` | `0x0306fc60` | `0x02f61578` | `0x007c24e0` |
| `TWorldMapSubfieldExtent` | `0x0307d1f8` | `0x02f63fa8` | `0x00748330` |

## Downstream bounded-code result

The current producer bundle materially advances Storage and separates Storage from Viewport, but it does **not** contain enough semantic downstream code to finish the complete patch/dependency graph:

- `TWorldMapRenderProvider@0x00820970`: the staged first-slot window is destructor/cleanup-heavy and exposes a broad member layout, but no direct clipping/culling/iteration rule is proven.
- `TWorldMapCamera@0x00dedda0` (and the staged CameraViewport first slot): the staged code is trivial/metaobject-like and does not expose projection/scale calculations.
- `TWorldMapPicker@0x008205c0`: the staged first-slot window is destructor/ownership cleanup and does not expose screen/world picking transforms.

Therefore no render clipping/culling rule, camera projection limit, picker screen/world transform, or final safe mutation site is invented.

## Updated classification

```yaml
original_blocker: BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
original_blocker_status: RESOLVED_BY_PR_437
identity_windows: 3_OF_3_PROVEN
geometry_requested_writers: PROVEN
historical_18_14_object_identity: TWorldMapStorage
historical_18_14_control_identity: counted_TWorldMapStorage
storage_half_open_3d_bounds: PROVEN
storage_extent_driven_oob_eviction: PROVEN
storage_live_collection_count_relation: PROVEN
viewport_separate_exact_identity_and_geometry: PROVEN
static_patch_graph_ready: false
static_classification: MORE_STATIC_RE_NEEDED
remaining_blocker: DOWNSTREAM_EXACT_WORLD_MAP_CONSUMER_WINDOWS_NOT_DURABLY_STAGED
```

The new evidence removes the old identity/writer blocker, but the task is not complete and no client-byte mutation is authorized.

## Exact next evidence frontier

Resume this same PR/task when the next bounded exact-client producer can stage:

1. callers/upstream producer for Storage slot 12, especially the object passed as `rsi` and the source of its `+0x38` QWORD;
2. non-destructor `TWorldMapRenderProvider` virtual/caller windows that expose iteration, clipping and culling;
3. non-meta `TWorldMapCamera` windows for projection/scale/viewport coupling;
4. non-destructor `TWorldMapPicker` windows for screen/world transforms and bounds;
5. exact fixed-allocation, mask, packing and loop-bound sites tied to those consumers.

Do not rescan the exhausted retained-artifact inventory, repeat the failed CDN fetch, use Synology as an unauthorized static-analysis fallback, or design a client-byte patch before this downstream dependency graph is complete.
