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
original_blocker: BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
original_blocker_status: RESOLVED_BY_PR_437
static_classification: MORE_STATIC_RE_NEEDED
static_patch_graph_ready: false
remaining_blocker: DOWNSTREAM_EXACT_WORLD_MAP_CONSUMER_WINDOWS_NOT_DURABLY_STAGED
```

## Result

A new governance-bounded sanitized exact-client producer, Draft PR #437 (`OTC-20260816-track-a-worldmap-exact-static-evidence`), has resolved the exact identity/writer blocker that previously stopped PR #367. The producer fenced the official native-Linux client to version `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, and produced no raw-client artifact.

Source run `31972743782` / job `95227595548` produced artifact `9270235755`; hosted run `31972915689` / job `95228024727` produced the final sanitized artifact `9270276361`. In this continuation both artifact ZIP digests were independently checked and exactly matched producer metadata. The hosted artifact reports `WORLD_MAP_STATIC_HOSTED_VALIDATION=PASS` and `WORLD_MAP_STATIC_EVIDENCE_READY=true`.

No exhausted historical-artifact scan was repeated, no failed CDN fetch was retried, no live Synology/static-analysis fallback was used by #367, and no client bytes were changed.

Durable consumer evidence:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-new-exact-static-unblock-and-downstream-recovery.md`

## Exact identity correction

All three requested vtable/typeinfo windows are now exact:

```text
0x030871c8..0x030871d7 -> vptr 0x030871d8
bytes    0000000000000000b85f080300000000
typeinfo 0x03085fb8
class    tibia::worldmap::TWorldmapProtocolMessageHandler

0x0308ce60..0x0308ce6f -> vptr 0x0308ce70
bytes    0000000000000000f0b5080300000000
typeinfo 0x0308b5f0
class    tibia::worldmap::TWorldMapStorage

0x02f683c0..0x02f683cf -> vptr 0x02f683d0
bytes    000000000000000020fb070300000000
typeinfo 0x0307fb20
class    std::_Sp_counted_ptr_inplace<tibia::worldmap::TWorldMapStorage,...>
```

**FACT:** the historical `owner+0x10` object carrying retained `+0x48=18`, `+0x4c=14` is `TWorldMapStorage`, not `TWorldMapViewport`.

**FACT:** the adjacent counted control block is the counted `TWorldMapStorage` allocation wrapper.

The previous strong Viewport correlation for this specific object/control pair is superseded by direct RTTI evidence.

## Storage geometry — exact writers and meaning

Exact Storage constructor `0x00cbf37a` installs vptr `0x0308ce70` and initializes:

```text
QWORD Storage+0x18 -> DWORD +0x18/+0x1c
QWORD Storage+0x30 -> DWORD +0x30/+0x34
QWORD Storage+0x48 -> DWORD +0x48/+0x4c
```

The same constructor installs exact `TWorldMapExtent` vptr `0x02f61578` at `Storage+0x40`, so `+0x48/+0x4c` are the first two DWORD payload fields inside the embedded `TWorldMapExtent` beginning at `+0x40`.

Storage vtable slot 12 at `0x00cc6cd0` mutates all three groups. The priority pair is copied as one QWORD at `0x00cc6d2c`:

```text
[rsi+0x38] -> Storage+0x48
```

Thus all requested offsets `+0x18/+0x1c/+0x30/+0x34/+0x48/+0x4c` have direct initialization and mutation coverage. The observed `18/14` are not constructor literals; the exact upstream producer of the slot-12 input at `rsi+0x38` remains `UNKNOWN`.

## Storage lower/upper bounds — PROVEN

Storage vtable slot 14 at `0x00cb01d0` directly enforces:

```text
Storage+0x18 <= x < Storage+0x30
Storage+0x1c <= y < Storage+0x34
Storage+0x20 <= z < Storage+0x38
```

Therefore the retained runtime coordinate pairs are exact half-open 3D lower/upper bounds. The historical arithmetic:

```text
32555 - 32537 = 18
32517 - 32503 = 14
```

is now directly correlated with Storage bounds plus a separate embedded extent payload `18/14`.

Exact C++ field names and units for the embedded extent payload remain unknown.

## Storage update, eviction and collection state

The Storage slot-12 geometry mutator traverses the Storage-owned ordered node structure after replacing bounds. Nodes outside the new half-open bounds are removed, and `Storage+0x88` is decremented on removal. Storage slots `0x00cc7d60` and `0x00cc80c0` independently traverse the same tree and consume `Storage+0x88` while exporting/filtering extent-aware entries.

**FACT:** geometry/extent changes drive out-of-bounds Storage entry removal.

**FACT:** `Storage+0x88` participates as a live node/collection count-size relation.

**UNKNOWN:** no fixed maximum capacity, cache ceiling or eviction-policy limit is proven from the staged bytes.

The staged lookup/traversal paths are coordinate-indexed and extent-aware rather than fixed loops bounded by literal 18/14.

## Exact Viewport separation

The new bounded bytes also stage a distinct exact `TWorldMapViewport` constructor at `0x00cbf680`, anchored by Viewport vptr `0x0308c9a8` / typeinfo `0x0308b590`.

It installs its own `TWorldMapExtent` subobject and initializes independent geometry fields including:

```text
Viewport+0x48 = 8
Viewport+0x60 = 4
```

A following geometry update routine at `0x00cbf700` recomputes Viewport state and performs signed arithmetic including an arithmetic right shift by 5.

**FACT:** Viewport has separate computed geometry state and is not the historical Storage object holding retained `18/14`.

**INFERENCE:** the shift-by-5 is consistent with the separately proven worldmap ×32 grid/scale boundary; exact source-level field semantics remain unproven.

**UNKNOWN:** this bundle does not directly establish the concrete Storage↔Viewport ownership/call edge.

## RenderProvider / Camera / Picker frontier

Exact RTTI/vtable anchors are now available:

```text
TWorldMapRenderProvider typeinfo 0x03089b70 vptr 0x02f6c258 first staged slot 0x00820970
TWorldMapCamera         typeinfo 0x03080500 vptr 0x03083968 first staged slot 0x00dedda0
TWorldMapPicker         typeinfo 0x03086888 vptr 0x02f6b7c8 first staged slot 0x008205c0
```

However the current bounded windows do not finish their semantic graph:

- RenderProvider first-slot evidence is dominated by destructor/member cleanup and does not prove clipping/culling/iteration bounds.
- Camera first-slot evidence is trivial/metaobject-like and does not expose projection/scale coupling.
- Picker first-slot evidence is destructor/ownership cleanup and does not expose screen/world transform logic.

No downstream rule is invented from destructor adjacency or class names alone.

## Current classification

```yaml
identity_windows_3_of_3: PROVEN
protocol_handler_identity: PROVEN
historical_18_14_object_identity: TWorldMapStorage_PROVEN
historical_control_block_identity: counted_TWorldMapStorage_PROVEN
geometry_six_requested_offsets_initialized: PROVEN
geometry_six_requested_offsets_mutated: PROVEN
storage_half_open_3d_bounds: PROVEN
storage_extent_driven_oob_eviction: PROVEN
storage_live_collection_count_relation: PROVEN
viewport_exact_separate_identity_and_geometry: PROVEN
upstream_source_of_storage_slot12_rsi_plus_0x38: UNKNOWN
render_clipping_culling_iteration: UNKNOWN
camera_projection_scale: UNKNOWN
picker_screen_world_transform: UNKNOWN
fixed_allocation_mask_packing_full_audit: INCOMPLETE
static_patch_graph_ready: false
classification: MORE_STATIC_RE_NEEDED
remaining_blocker: DOWNSTREAM_EXACT_WORLD_MAP_CONSUMER_WINDOWS_NOT_DURABLY_STAGED
```

## Next action

Continue this same task/PR only with a new bounded exact-client producer that stages:

1. the caller/upstream object feeding Storage slot 12, especially input `rsi+0x38`;
2. non-destructor RenderProvider virtual/caller windows for iteration/clipping/culling;
3. non-meta Camera projection/scale/viewport windows;
4. non-destructor Picker screen/world transform windows;
5. fixed-allocation, loop-bound, mask and packing sites tied to those paths.

Do not rescan the already exhausted retained inventory, repeat the identical failed CDN fetch, use physical Synology as an unauthorized static-analysis fallback, or design/modify client bytes before the complete downstream dependency graph is proven.
