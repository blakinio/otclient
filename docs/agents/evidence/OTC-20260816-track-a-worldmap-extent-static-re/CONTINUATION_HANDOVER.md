# Continuation handover — worldmap extent static RE

Continue the existing task/branch/PR. Do not create a replacement research programme or competing consumer PR.

```yaml
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
branch: research/OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
phase: investigate
execution_class: github_hosted
runtime_access: none
mutation_authorized: false
owner_funded_ai_api_authorized: false
static_classification: MORE_STATIC_RE_NEEDED
static_patch_graph_ready: false
original_blocker: BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
original_blocker_status: RESOLVED_BY_PR_437
remaining_blocker: DOWNSTREAM_EXACT_WORLD_MAP_CONSUMER_WINDOWS_NOT_DURABLY_STAGED
```

## Required startup

Read current repository governance, the active task, this handover, the current report, and the newest evidence first. Revalidate live `main`, PR #367 head/reviews/CI, ownership and overlapping tasks before any mutation.

Mandatory current evidence entry point:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-new-exact-static-unblock-and-downstream-recovery.md`

Do not use owner-funded Codex/OpenAI API/tokens. Do not modify client bytes.

## New exact-static producer already consumed

Draft PR #437 / task `OTC-20260816-track-a-worldmap-exact-static-evidence` is the bounded sanitized producer for #367 and declares `WORLD_MAP_STATIC_EVIDENCE_READY=true`.

Exact client fence:

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Producer evidence:

```text
source run/job/artifact  31972743782 / 95227595548 / 9270235755
source artifact sha256   039d22fe5f88a07784c4ddc32cf6b1d9c2d07a34e90ed5902ffd21d3acd5735b
hosted run/job/artifact  31972915689 / 95228024727 / 9270276361
hosted artifact sha256   0dc8d0a44e5a2550ef79c219bda14787796ef7accc0ab1627fecd7c6d55330bc
hosted validation        PASS
```

Both artifact ZIP digests were independently checked while consuming them. No exhausted historical inventory was rescanned and no failed CDN fetch was repeated.

## Exact corrections now authoritative for this task

All three previously missing identity windows are proven:

```text
0x030871d8 -> tibia::worldmap::TWorldmapProtocolMessageHandler
0x0308ce70 -> tibia::worldmap::TWorldMapStorage
0x02f683d0 -> counted TWorldMapStorage control block
```

The historical object with retained `+0x48=18`, `+0x4c=14` is **TWorldMapStorage**, not `TWorldMapViewport`. The previous strong Viewport inference for that exact object/control pair is superseded and must not be revived.

## Storage graph recovered

Exact anchors:

```text
Storage ctor             0x00cbf37a
Storage slot-12 mutator  0x00cc6cd0
priority pair copy       0x00cc6d2c: [rsi+0x38] QWORD -> Storage+0x48
Storage slot-13 export   0x00cb0180
Storage slot-14 bounds   0x00cb01d0
TWorldMapExtent vptr     0x02f61578 at Storage+0x40
```

Proven half-open 3D bounds:

```text
Storage+0x18 <= x < Storage+0x30
Storage+0x1c <= y < Storage+0x34
Storage+0x20 <= z < Storage+0x38
```

All requested geometry DWORDs `+0x18/+0x1c/+0x30/+0x34/+0x48/+0x4c` now have exact initialization and mutation coverage.

The Storage geometry mutator traverses its ordered node structure and removes entries outside new bounds; removal decrements `Storage+0x88`. Additional virtuals use `+0x88` while traversing/exporting/filtering the same extent-aware structure. This proves extent-driven out-of-bounds removal and a live collection-count relation, but not a fixed maximum capacity.

The upstream producer of slot-12 input `rsi+0x38` that dynamically supplies the embedded extent pair remains `UNKNOWN`.

## Viewport graph recovered separately

Exact `TWorldMapViewport` constructor:

```text
constructor 0x00cbf680
vptr        0x0308c9a8
typeinfo    0x0308b590
```

It has its own extent/geometry state, including constructor values `Viewport+0x48=8` and `Viewport+0x60=4`. Adjacent geometry update `0x00cbf700` recomputes Viewport state and includes signed shift-by-5 arithmetic.

Do not infer a direct Storage↔Viewport ownership edge merely from code locality; that exact edge is still `UNKNOWN`.

## Remaining exact frontier

Current producer anchors downstream classes but stages only insufficient first-slot semantics for the final patch graph:

```text
TWorldMapRenderProvider vptr 0x02f6c258 / first staged slot 0x00820970
TWorldMapCamera         vptr 0x03083968 / first staged slot 0x00dedda0
TWorldMapPicker         vptr 0x02f6b7c8 / first staged slot 0x008205c0
```

The staged RenderProvider/Picker code is destructor/cleanup-heavy; Camera first-slot code is trivial/metaobject-like. Do not invent clipping, culling, projection, scale or picking rules from these windows.

## Exact next action

Obtain a **new bounded exact-client producer bundle** for:

1. the caller/upstream object feeding Storage slot 12, especially the source of `rsi+0x38`;
2. non-destructor `TWorldMapRenderProvider` virtual/caller windows for iteration/clipping/culling;
3. non-meta `TWorldMapCamera` windows for projection/scale/viewport coupling;
4. non-destructor `TWorldMapPicker` windows for screen/world transforms and limits;
5. fixed-allocation, loop-bound, mask and packing sites tied to those paths.

Then continue this same PR #367. Do not rescan the exhausted retained-artifact set, repeat the identical failed CDN fetch, use Synology as an unauthorized static-analysis fallback, or design a client-byte patch until the downstream graph is complete.
