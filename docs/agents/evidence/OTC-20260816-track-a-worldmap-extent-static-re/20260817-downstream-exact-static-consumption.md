# Downstream exact-static consumption — final static dependency graph

## Scope and provenance

This checkpoint consumes the new governance-bounded producer Draft PR #446 (`OTC-20260817-track-a-worldmap-downstream-exact-static-evidence`) into consumer PR #367. It does not execute the official client, access process memory/runtime state, or modify client bytes.

Exact client fence remains:

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux
```

Producer #446 final evidence head:

```text
f7f16af614a88100cc82ff7ecf0b112cb2e0605c
```

Producer exact-head validation:

```text
Track A governance run  32003664983  SUCCESS
repository CI run        32003665239  SUCCESS
CI / Required job        95309109578  SUCCESS
```

Exact-file stages consumed:

```text
broad source run/job       32001356705 / 95302168871  SUCCESS
broad source artifact      9278519216
broad source digest        sha256:e10347435bece4cbedc7fca54b782cea76f9f1dab3b042082fe3bcc15f7c0728
broad hosted job           95302411849               SUCCESS
broad final artifact       9278527206
broad final digest         sha256:af12b2af9c725ca402224876c3cbd0c01306f47b37e717548c5817310dd3bc9b

targeted run/source job    32002326947 / 95304896213  SUCCESS
targeted source artifact   9278827774
targeted source digest     sha256:8f6a9feaea607475f6f9d25d200d858f52714f9384561bd4010405d26a78009a
targeted hosted job        95305039463               SUCCESS
targeted final artifact    9278833445
targeted final digest      sha256:7505aeae6e79e8829adf60261e1a3b50f27e0514f50136161e5f715a27124218

camera run/source job      32003150333 / 95307268007  SUCCESS
camera source artifact     9279105537
camera source digest       sha256:9b44a39558c50ce86243dece3b3fac19bb1f7619112e913fa45b647878d9e28d
camera hosted job          95307487191               SUCCESS
camera final artifact      9279111731
camera final digest        sha256:81620b3fd866e2203b2ed0a39a1a0979ba52b5e3af41b47ac7e247b09082effa
```

Durable producer evidence:

- `docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/20260817-worldmap-downstream-exact-static-evidence.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/20260817-worldmap-downstream-exact-static-evidence.json`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/20260817-worldmap-camera-neighborhood-evidence.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-downstream-exact-static-evidence/20260817-worldmap-camera-neighborhood-evidence.json`

## Exact `18 / 14` source chain — PROVEN

The previous unknown upstream source of `TWorldMapStorage` slot-12 input `rsi+0x38` is resolved.

### Handler constructor master default

Exact `TWorldmapProtocolMessageHandler` constructor:

```text
0x00803c01  lea rax,[rip+...] -> vptr 0x030871d8
0x00803c08  mov [rbx],rax
...
0x00803d6f  lea rax,[rip+...] -> 0x02f615a0
0x00803d76  mov [rbx+0x90],rax
0x00803d7d  mov rax,QWORD [rip+...] -> 0x01cdd958
0x00803d8b  mov [rbx+0xb0],rax
```

Exact static bytes at `0x01cdd958` start:

```text
12 00 00 00  0e 00 00 00  08 00 00 00  06 00 00 00
```

Thus:

```text
QWORD 0x01cdd958 = 0x0000000e00000012
DWORD low = 18
DWORD high = 14
```

**FACT:** Handler construction hardcodes `Handler+0xb0/+0xb4 = 18/14` as a default pair.

### Handler snapshot fanout

Existing consumer exact evidence proves `FullMap@0x00cec8d0` calls `0x00cdb770(owner)` where owner is the exact Handler. Producer #446 additionally recovers direct call `0x00cec955 -> 0x00cdb770`.

`0x00cdb770` constructs a geometry snapshot:

```text
0x00cdb772  lea rsi,[rdi+0x90]
0x00cdb78b  lea r14,[rsp+0x90]
0x00cdb793  mov rdi,r14
0x00cdb796  call 0x00bc6350
```

`0x00bc6350` copies packed QWORD fields:

```text
0x00bc6368  movq xmm0,QWORD [rsi+0x8]
0x00bc636d  movq xmm2,QWORD [rsi+0x38]
0x00bc6372  movq xmm1,QWORD [rsi+0x20]
...
0x00bc63af  movq QWORD [rax+0x38],xmm1
```

Because its source is `Handler+0x90`, source `+0x20` is exactly `Handler+0xb0`. Therefore snapshot `+0x38` receives the Handler master `18/14` QWORD when it is at its constructor default.

### Snapshot → exact Storage slot 12

Immediately after snapshot construction:

```text
0x00cdb79b  mov rdi,QWORD [Handler+0x10]
0x00cdb7a5  mov rsi,r14
0x00cdb7a8  mov rax,QWORD [rdi]
0x00cdb7ab  call QWORD [rax+0x60]
```

Retained exact runtime evidence already fixes Handler `+0x10` object vptr to `0x0308ce70`; producer #437 proves that vptr is exact `TWorldMapStorage`. Its address-point `+0x60` is slot 12 `0x00cc6cd0`.

Exact slot-12 copy:

```text
0x00cc6cf3  movq xmm0,QWORD [rsi+0x38]
0x00cc6d2c  movq QWORD [Storage+0x48],xmm0
```

Therefore the load-bearing chain is now direct:

```text
hardcoded 18/14 @ 0x01cdd958
 -> Handler+0xb0/+0xb4 constructor default
 -> snapshot+0x38
 -> Handler+0x10 exact TWorldMapStorage vslot12
 -> Storage+0x48/+0x4c
 -> retained runtime exact values 18/14
```

### Mutability classification

```yaml
Handler master pair:
  constructor default: hardcoded 18/14
  complete later-writer census: UNKNOWN
TWorldMapViewport pair:
  constructor default: hardcoded 18/14
  later recomputation: PROVEN
TWorldMapStorage pair:
  constructor default: zero
  runtime update: mutable/copy-driven via slot 12
```

This answers the earlier constant/configuration question at the directly proven layers without claiming Handler post-construction immutability.

## Viewport dependency — PROVEN COMPUTED STATE

Exact Viewport constructor `0x00cbf680` consumes the same `0x01cdd958` literal:

```text
0x00cbf68b  lea rax -> vptr 0x0308c9a8
0x00cbf6b0  mov rax,QWORD [0x01cdd958]
0x00cbf6be  mov QWORD [Viewport+0x40],rax
```

So Viewport starts with `18/14` at its independent extent state.

Exact `0x00cbf700` later recomputes that state from Viewport inputs, consumes packed delta `15/11` from `0x01d63cd0`, performs signed packed arithmetic, writes the new Viewport extent and uses shift-by-5 / `0x1f` correction arithmetic.

**Dependency classification:** Viewport is a **computed geometry dependency**, not merely a duplicate static literal.

## Storage dependency — PROVEN BOUNDS / UPDATE / EVICTION

From #437 plus the prior consumer recovery:

- `Storage+0x18/+0x1c/+0x20` and `+0x30/+0x34/+0x38` are exact half-open lower/upper XYZ bounds;
- `Storage+0x48/+0x4c` are payload DWORDs of embedded exact `TWorldMapExtent` beginning at `Storage+0x40`;
- slot 12 replaces all three paired geometry regions;
- after replacement, out-of-bounds ordered nodes are removed;
- `Storage+0x88` participates in live node/collection count state;
- no fixed maximum Storage capacity/cache ceiling was recovered;
- the structure is extent/coordinate driven, not a literal 18×14 fixed allocation.

## RenderProvider dependency — PROVEN 32-CELL CLIPPING/INDEXING SURFACE

Exact identity:

```text
vptr      0x02f6c258
typeinfo  0x03089b70
class     tibia::worldmap::TWorldMapRenderProvider
primary slots 0..21
```

Curated load-bearing functions:

- slot 16 `0x00cd08b0`: fixed `0x30` record iteration plus `&0x1f` and signed shift/divide-by-32 coordinate processing;
- slot 14 `0x00cd2260`: rejects negative/out-of-range coordinates against dependency dimensions, linearizes accepted coordinates (`y*width+x` form) and bounds-checks indexed storage;
- slot 13 `0x00cd1e50`: iterates fixed `0x20` entries obtained from a virtual range and builds extent/ordered state;
- slots 10/11 `0x00cea540` / `0x00cec020`: repeated `&0x1f`, shift-by-5 and 32-multiple arithmetic;
- slot 21 `0x00ce9700`: `TWorldMapExtent` / `TWorldMapSubfieldExtent`-related state, fixed `0x20` allocation and bounded bit/modulo-style selection.

**Dependency classification:** RenderProvider is a direct **clipping/culling/indexing/iteration consumer** coupled to the 32-cell/chunk representation. It belongs in any future mutation dependency graph even though no client bytes are changed here.

## Picker dependency — PROVEN 32-CELL SCREEN/WORLD TRANSFORM SURFACE

Exact identity:

```text
vptr      0x02f6b7c8
typeinfo  0x03086888
class     tibia::worldmap::TWorldMapPicker
primary slots 0..7
```

- slot 5 `0x00cd0400`: packed coordinate conversion with `shl 5`, `0x1f` floor/sign correction, packed addition and arithmetic right shift by 5;
- slot 4 `0x00cd65b0`: range traversal with shift-by-5 and `0x20` stepping, building fixed `0x18` extent-like records;
- slot 7 `0x00ce80c0`: extent/range acquisition, shift-by-5, coordinate subtraction, bounds construction and fixed `0x28` candidate iteration.

**Dependency classification:** Picker is a direct fixed-32 screen/world transform and bounds consumer. No primary Picker slot provides a promoted direct `18/14` literal writer.

## Camera dependency — EXACT CO-OWNERSHIP, NO PREIDENTIFIED MUTATION EDGE

Exact Camera identity:

```text
vptr      0x03083968
typeinfo  0x03080500
class     tibia::renderer::TWorldMapCamera
primary slots 0..4
```

Camera constructor/layout facts include two vector-state blocks, embedded address point `0x02f69278` around `+0x98/+0xb8`, scalar `Camera+0xd0 = 1.0` and zero/default surrounding state.

The dedicated camera discriminator enumerated all 11 exact Camera-vptr xrefs, staged 11 bounded neighborhoods totaling 225,280 source bytes and hosted-disassembled 37,325 unique instructions.

One exact higher-level world-map construction path proves co-ownership/coordination:

```text
0x007e73a4  counted Camera vptr 0x02f692a0
0x007e73ad  r15 = counted block +0x10 = inline Camera
0x007e73ca  exact Camera vptr 0x03083968
0x007e7478  higher_owner+0xc8 = Camera object
0x007e7471  higher_owner+0xd0 = Camera counted block
...
0x007e7bbd  rbp = higher_owner+0xa8
0x007e7bf5  call 0x00cbf700
```

`0x00cbf700` is the exact Viewport geometry recompute routine. Thus a higher-level world-map owner coordinates Viewport-compatible state at `+0xa8` and counted Camera at `+0xc8/+0xd0`.

Across those 11 exact Camera-vptr neighborhoods, no type-anchored Camera-field chain was recovered to Storage slot12, Handler master `18/14`, Storage `+0x48/+0x4c`, RenderProvider vptr or Picker vptr. This is a **bounded negative result**, not a global absence proof.

**Dependency classification:** Camera remains a **co-owned transform/post-change validation dependency**. No Camera mutation site or named projection formula is invented.

## Fixed allocation / mask / packing audit — RECOVERED DEPENDENCIES

The downstream exact evidence establishes relevant fixed representation surfaces:

```text
hardcoded pair      18/14 @ 0x01cdd958
Viewport delta      15/11 @ 0x01d63cd0
chunk/floor mask    0x1f
cell/chunk shift    5  (scale 32)
record/allocation   0x18, 0x20, 0x28, 0x30 on different consumers
```

These constants are not all candidate patch values. They classify dependent representations and loops that must be preserved/revalidated by a future mutation design.

## Final static dependency graph

```text
                         hardcoded packed 18/14
                              0x01cdd958
                              /          \
                             /            \
                Handler master default   Viewport default
                 +0xb0/+0xb4              +0x40/+0x44
                      |                         |
                      | snapshot builder        | 0xcbf700 recompute
                      | 0xbc6350                | + signed /32 geometry
                      v                         v
               snapshot+0x38             computed Viewport extent
                      |
                      | Handler+0x10 exact Storage vslot12
                      v
              TWorldMapStorage geometry/bounds
             +0x18/+0x1c ... +0x48/+0x4c
                      |
          +-----------+--------------+
          |                          |
   extent-driven Storage       TWorldMapExtent /
      filtering/eviction       TWorldMapSubfieldExtent
          |                          |
          +------------+-------------+
                       |
              RenderProvider consumers
           clipping / culling / indexing
                  fixed 32 grid
                       |
                    Picker
              screen/world transforms
                  fixed 32 grid

 higher-level owner: Viewport-compatible +0xa8 and Camera +0xc8/+0xd0
 Camera = co-owned transform/validation dependency; no exact extent mutation edge recovered
```

## Readiness decision

The downstream blocker recorded in the previous #367 checkpoint is resolved:

```yaml
upstream_source_of_storage_slot12_rsi_plus_0x38: PROVEN
render_clipping_culling_iteration: PROVEN
picker_screen_world_transform: PROVEN
camera_exact_layout_and_viewport_coownership: PROVEN
camera_direct_extent_mutation_edge_in_all_exact_vptr_neighborhoods: NOT_RECOVERED_BOUNDED
fixed_allocation_mask_packing_dependencies: PROVEN
complete_later_writer_census_for_handler_master_pair: UNKNOWN
named_camera_projection_formula: UNKNOWN
```

**Decision:** the static **dependency graph** is now sufficiently recovered to close the discovery task. Unknowns above are explicitly carried as constraints for any later mutation-design/physical-validation task; they do not justify inventing additional static patch sites.

```text
STATIC_PATCH_GRAPH_READY=true
MUTATION_DESIGN_READY=false
CLIENT_BYTE_MUTATION_AUTHORIZED=false
```

No patch bytes, patch addresses for modification, or mutation plan are designed by this checkpoint.
