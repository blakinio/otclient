# World-map exact-static evidence — second producer package

Task: `OTC-20260816-track-a-worldmap-exact-static-evidence`  
Producer Draft PR: `#437`  
Consumer: `OTC-20260816-track-a-worldmap-extent-static-re` / Draft PR `#367`

This is a bounded producer handoff. It does not modify the consumer branch, execute or patch the client, access a current client process/session/display, or use owner-funded AI/API tokens.

## Exact-client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runtime_access: none
client_executed: false
client_bytes_mutated: false
process_memory_accessed: false
canonical_runtime_accessed: false
raw_client_uploaded: false
```

Every second-pack source run re-hashed the read-only source file and failed closed on fence mismatch. Source-side processing emitted bounded sanitized byte windows only; GNU `objdump` ran on those windows on GitHub-hosted runners.

## Run / job / artifact provenance

| discriminator | run | source job / artifact | hosted job / final artifact | result |
|---|---:|---|---|---|
| broad vtable/caller census | `32002543926` | `95305539737 / 9278903625` | `95305685220 / 9278908515` | SUCCESS |
| targeted callers/constants/Render/Picker/Viewport/Camera | `32003065517` | `95307020627 / 9279071635` | `95307179088 / 9279075470` | SUCCESS |
| Storage producer / slot14 / Camera discriminator | `32003607118` | `95308578004 / 9279245326` | `95308725378 / 9279250068` | SUCCESS |
| ProtocolHandler Qt-metaobject identity | `32004356610` | `95310743900 / 9279498428` | `95310922681 / 9279503543` | SUCCESS |
| ProtocolHandler constructor dependency caller | `32004614539` | `95311482128 / 9279577899` | `95311635844 / 9279583871` | SUCCESS |
| final outer-owner cross-check | `32004839610` | `95312106162 / 9279649834` | `95312291576 / 9279654629` | SUCCESS |

Final run `32004839610` re-confirmed the exact fence and reported:

```text
WORLD_MAP_SECOND_PACK_BOUNDED_WINDOWS=51
WORLD_MAP_SECOND_PACK_BOUNDED_RAW_BYTES=57088
WORLD_MAP_SECOND_PACK_OUTER_OWNER_CALLERS=1
WORLD_MAP_SECOND_PACK_OUTER_OWNER_VTABLE_MEMBERSHIPS=0
WORLD_MAP_STATIC_HOSTED_VALIDATION=PASS
```

The final artifact digest is `sha256:f4605cc42e032d7ce3ca91bda17aa54dfdb2b8b427d8758fadc30d10748c30b7`.

## 1. Upstream source of Storage extent — PROVEN

### Exact class anchor

Existing first-pack RTTI remains authoritative:

```text
TWorldmapProtocolMessageHandler vptr 0x030871d8 typeinfo 0x03085fb8
TWorldMapStorage                 vptr 0x0308ce70 typeinfo 0x0308b5f0
TWorldMapViewport                vptr 0x0308c9a8 typeinfo 0x0308b590
```

Run `32004356610` additionally resolved Qt static metaobject `0x03087800`: its string-data block contains exact class name `tibia::worldmap::TWorldmapProtocolMessageHandler`; `static_metacall=0x00df2a60`. That dispatcher reaches `0x00cdb770`, so `0x00cdb770` is statically anchored to exact ProtocolHandler `this` rather than an anonymous owner.

### Where 18×14 is born

Exact ProtocolHandler constructor starts at `0x00803ab0` and installs the exact handler vptr at `0x00803c01`.

The constructor reads a packed QWORD at `0x01cdd958` and writes it to `Handler+0xb0/+0xb4`:

```text
0x00803d7d  mov rax,QWORD [rip+...] -> 0x01cdd958
0x00803d8b  mov QWORD [rbx+0xb0],rax
```

The exact static bytes at `0x01cdd958` begin:

```text
12 00 00 00  0e 00 00 00  08 00 00 00  06 00 00 00
```

Therefore:

```text
low DWORD  = 18
high DWORD = 14
```

**FACT:** `18×14` is a hardcoded constructor default in exact `TWorldmapProtocolMessageHandler`, not a value created by `TWorldMapStorage`.

### Handler master pair -> snapshot +0x38

Exact handler method `0x00cdb770`:

```text
0x00cdb772  lea rsi,[rdi+0x90]
0x00cdb78b  lea r14,[rsp+0x90]
0x00cdb793  mov rdi,r14
0x00cdb796  call 0x00bc6350
0x00cdb79b  mov rdi,QWORD [r12+0x10]
0x00cdb7a0  mov edx,1
0x00cdb7a5  mov rsi,r14
0x00cdb7a8  mov rax,QWORD [rdi]
0x00cdb7ab  call QWORD [rax+0x60]
```

`0x00bc6350` builds a 0x50-byte geometry aggregate with exact constituent vptrs `TWorldMapCoordinate` (`0x02f615a0`) and `TWorldMapExtent` (`0x02f61578`). The top-level wrapper type is not named and remains `UNKNOWN`.

Load-bearing copy:

```text
0x00bc6372  movq xmm1,QWORD [rsi+0x20]
...
0x00bc63af  movq QWORD [rax+0x38],xmm1
```

Because `0x00cdb770` passes `Handler+0x90` as the builder source, source `+0x20` is exactly `Handler+0xb0/+0xb4`. Thus the packed `18/14` constructor default reaches snapshot `+0x38` without a +1/-1 or inclusive/half-open conversion.

Existing exact Storage slot 12 `0x00cc6cd0` copies its input `+0x38` to `Storage+0x48/+0x4c`; exact write at `0x00cc6d2c` remains the first-pack proof.

### Receiver identity boundary

The second package statically proves that Handler `+0x10/+0x18` is a constructor-supplied shared pointer. `0x00804620` passes `outer+0x2f8/+0x300` as that first shared pointer when calling handler constructor `0x00803ab0` at `0x00804778`.

The first-pack exact Storage construction path writes the exact `TWorldMapStorage*` and counted control block to an `outer+0x2f8/+0x300` pair. The last discriminator found exactly one direct caller of `0x00804620` at `0x007de331`, but no Itanium-vtable membership for `0x00804620`; therefore equality of those outer-owner classes is **not** promoted from static structure alone.

Separately, read-only consumer state in #367 retains exact historical runtime evidence that fixes `Handler+0x10` object vptr to `0x0308ce70`; first-pack #437 RTTI proves that address point is exact `TWorldMapStorage`. This is a cross-check of a historical retained observation, not an assumption about a current PID/session/display.

Classification:

```yaml
hardcoded_handler_default_18_14: FACT
handler_b0_b4_to_snapshot_plus_38: FACT
snapshot_passed_to_handler_plus_10_vslot_12: FACT
handler_plus_10_exact_storage_from_static_structure_only: INFERENCE
handler_plus_10_exact_storage_with_retained_vptr_cross_check: FACT
complete_post_constructor_writer_census_for_Handler_b0_b4: UNKNOWN
```

`STORAGE_EXTENT_UPSTREAM_SOURCE_PROVEN=true` because the actual source of the pair is now exact, while the incomplete later-writer census is explicitly retained as an unknown.

## 2. Viewport — 18×14 is a default, not a fixed visible-size cap

Exact Viewport constructor `0x00cbf680` installs vptr `0x0308c9a8` and independently loads the same packed `18/14` literal:

```text
0x00cbf6b0  mov rax,QWORD [0x01cdd958]
0x00cbf6be  mov QWORD [Viewport+0x40],rax
```

The constructor also loads margin-like integer prefix `[1,2,1,2]` from `0x01d32ef0` into `Viewport+0x10..+0x1c`.

Exact dynamic setter `0x00cb2220` proves the pair can change:

```text
0x00cb2220  add esi,0x1f
0x00cb2223  add edx,0x1f
0x00cb222a  shr esi,5
0x00cb222d  shr edx,5
0x00cb2230  add esi,[rdi+0x10]
0x00cb2233  add edx,[rdi+0x18]
0x00cb2236  add esi,[rdi+0x14]
0x00cb2239  add edx,[rdi+0x1c]
0x00cb223c  mov [rdi+0x40],esi
0x00cb223f  mov [rdi+0x44],edx
```

For non-negative pixel dimensions this is exactly:

```text
viewport_width_tiles  = ceil(width_px / 32)  + field_10 + field_14
viewport_height_tiles = ceil(height_px / 32) + field_18 + field_1c
```

Exact recompute `0x00cbf700` uses packed base pair `15/11` from `0x01d63cd0`, the stored margins and signed /32 correction (`0x1f`, shift 5). With default `[1,2,1,2]` margins, the base pair also reaches `18/14`.

Exact Viewport slot 14 `0x00cb07b0` emits another 0x50 geometry aggregate and copies `Viewport+0x40/+0x44` to aggregate `+0x38`:

```text
0x00cb07b0  movq xmm1,QWORD [rsi+0x40]
...
0x00cb07fb  movq QWORD [rax+0x38],xmm1
```

**FACT:** Viewport visible geometry is computed/dynamic and therefore `18×14` is not a universal fixed render-window limit.

**UNKNOWN:** no direct type-anchored Viewport-slot14 -> Storage-slot12 edge was recovered by #437. The proven live Storage feed above is the ProtocolHandler path.

## 3. RenderProvider — dynamic clipping/indexing, no independent 18×14 cap recovered

Exact identity:

```text
vptr      0x02f6c258
typeinfo  0x03089b70
constructor/vptr xref 0x00ccfa02
```

Load-bearing exact functions include `0x00cd2260`, `0x00cd08b0`, `0x00cea540`, `0x00cd1e50`, and `0x00ce9700`.

Exact slot 14 `0x00cd2260` performs dynamic rectangle clipping/indexing:

```text
0x00cd22b1  js  reject
0x00cd22b3  mov esi,[rdi+0x38]       ; dynamic width
0x00cd22b6  cmp ecx,esi
0x00cd22b8  jge reject
...
0x00cd22c1  cmp eax,[rdi+0x3c]       ; dynamic height
0x00cd22c4  jge reject
0x00cd22c6  imul eax,esi
0x00cd22d0  lea esi,[rax+rcx]
...
0x00cd22e4  cmp rsi,rdx              ; backing vector/count check
```

Exact slot 16 `0x00cd08b0` walks 0x30-byte records and uses `&0x1f` plus arithmetic shift-by-5 / divide-by-32 coordinate processing. Other exact RenderProvider slots use the same 32-cell/chunk representation.

Constructor `0x00ccfa02` has one significant fixed allocation:

```text
0x00ccfb8e  mov edi,0x9fff6
0x00ccfc07  call allocator
0x00ccfc1c  lea r12,[rbp+0x9fff6]
0x00ccfc23  lea rax,[rbp+0x0a]
0x00ccfc2b  add rax,0x0a
```

`0x9fff6 = 655350 = 65535 * 10`, so this is exactly a fixed 65,535-record 10-byte table/allocation.

Classification:

```yaml
render_dynamic_clipping_indexing: FACT
fixed_32_representation: FACT
fixed_65535_x_10_record_allocation: FACT
that_allocation_is_a_tile_or_visible-extent_cap: UNKNOWN
independent_literal_18_or_14_render_limit: NOT_RECOVERED
```

`RENDER_LIMITS_RECOVERED=true` means the recovered relevant clipping/indexing/representation constraints are sufficient for downstream dependency analysis; it does not assert that every RenderProvider allocation has been semantically named.

## 4. Picker — fixed-32 screen/world transform and bounds

Exact identity:

```text
vptr      0x02f6b7c8
typeinfo  0x03086888
```

Load-bearing functions include `0x00cd0400`, `0x00cd65b0`, `0x00ce7aa0`, `0x00ce80c0`.

Exact slot 5 `0x00cd0400`:

```text
0x00cd040d  shl esi,5
0x00cd0417  movq xmm2,QWORD [0x01ce70c8]  ; [31,31] correction
...
0x00cd0437  pand xmm0,xmm2
0x00cd043b  paddd xmm0,xmm1
0x00cd043f  psrad xmm0,5
0x00cd0444  movq [output+0x8],xmm0
```

The output is exact `TWorldMapCoordinate` via vptr `0x02f615a0`. Other Picker paths perform range traversal, fixed `0x20` stepping and bounds/candidate processing.

**FACT:** Picker owns a fixed-32 coordinate-conversion/bounds surface.

**FACT:** no independent hardcoded Picker `18`/`14` limit was recovered.

`PICKER_BOUNDS_RECOVERED=true`.

## 5. Camera — partial exact geometry evidence, named projection remains unresolved

Exact Camera identity remains:

```text
vptr      0x03083968
typeinfo  0x03080500
```

Exact Camera initialization includes scalar `Camera+0xd0 = 1.0f` and zero/default surrounding state.

The requested prior dependency function `0x00ced1b0` is now bounded exactly far enough to establish:

```text
0x00ced437  mov rax,[rbx+0x30]
0x00ced43b  movss xmm5,[rax+0xd0]
0x00ced448  cvtss2sd xmm0,xmm5
0x00ced44c  mulsd xmm0,QWORD [0x029505a8]
```

Exact static double at `0x029505a8` is `32.0`.

However, the object type behind `self+0x30` in this function is not proven as `TWorldMapCamera`; therefore this cannot be promoted to a named Camera projection formula.

Read-only consumer cross-check: #367/#446 independently recovered exact Camera co-ownership with Viewport-compatible state and a bounded negative result for a direct Camera->Storage extent mutation edge. #437 does not copy that producer's ownership or alter #367.

Classification:

```yaml
camera_exact_identity: FACT
camera_default_scalar_plus_d0_1_0: FACT
0xced1b0_dependency_plus_d0_times_32: FACT
0xced1b0_dependency_is_TWorldMapCamera: UNKNOWN
named_Camera_world_to_screen_formula: UNKNOWN
named_Camera_screen_to_world_formula: UNKNOWN
```

`CAMERA_GEOMETRY_RECOVERED=false` under the user's strict acceptance definition.

## 6. Limit/capacity audit

| surface | result | classification |
|---|---|---|
| hardcoded `18/14` | `0x01cdd958`, consumed by Handler and Viewport constructors | FACT |
| Viewport dynamic visible extent | `/32 + margins`, exact slot `0x00cb2220` | FACT |
| fixed-32 / shift-5 / mask-0x1f | Viewport, RenderProvider, Picker | FACT |
| Storage half-open bounds | prior #437 slot14 proof | FACT |
| Storage fixed cache/node ceiling | not recovered | UNKNOWN |
| Render fixed allocation | `65535 * 10` bytes/records pattern | FACT |
| Render allocation = tile ceiling | not established | UNKNOWN |
| parser/network payload ceiling tied to 18×14 | not recovered in traced paths | UNKNOWN |
| complete later-writer census for Handler master `+0xb0/+0xb4` | incomplete | UNKNOWN |
| arithmetic overflow for extreme dimensions | possible from 32-bit arithmetic, no practical threshold proven | INFERENCE |

Accordingly:

```text
FIXED_TILE_LIMIT_FOUND=UNKNOWN
```

## Patch-candidate graph only — no mutation

No safe standalone parameter is promoted.

```text
packed hardcoded 18/14 @ 0x01cdd958
        |
        +--> ProtocolHandler ctor -> Handler+0xb0/+0xb4
        |       -> 0x00bc6350 snapshot+0x38
        |       -> Handler+0x10 virtual slot 12
        |       -> TWorldMapStorage slot12 0x00cc6cd0
        |       -> Storage+0x48/+0x4c
        |
        +--> Viewport ctor -> Viewport+0x40/+0x44
                ^
                | 0x00cb2220 recomputes from pixel dimensions /32 + margins
                |
          RenderProvider / Picker consume dynamic geometry through fixed-32 representation
```

A future mutation design must treat the shared literal, Handler master pair, Storage feed, Viewport computation, RenderProvider and Picker as a dependency graph. Changing only Viewport geometry is insufficient evidence for retaining/receiving more live world-map tiles. Changing `0x01cdd958` alone is also **not classified safe** because the complete Handler later-writer census, network semantics and every capacity effect are not proven.

## Answer to downstream question

**FACT:** the client has a dynamically recomputable Viewport extent, so the visible geometry is not fundamentally hard-capped at `18×14` by Viewport/RenderProvider/Picker.

**FACT:** the live Storage extent receives a ProtocolHandler master pair whose exact constructor default is hardcoded `18×14` and is copied through the geometry snapshot into Storage slot 12.

**INFERENCE:** expanding the window/Viewport alone can expose a larger render geometry, but it does not by itself prove the client will retain or receive additional live tiles outside the Handler/Storage extent.

**UNKNOWN:** whether a single safe client-only parameter can make the official protocol deliver and retain more live world-map tiles. No such standalone safe parameter is proven here.

## Consumer handoff flags

```text
WORLD_MAP_DOWNSTREAM_EVIDENCE_READY=true
STORAGE_EXTENT_UPSTREAM_SOURCE_PROVEN=true
RENDER_LIMITS_RECOVERED=true
CAMERA_GEOMETRY_RECOVERED=false
PICKER_BOUNDS_RECOVERED=true
FIXED_TILE_LIMIT_FOUND=UNKNOWN
```

The remaining Camera projection unknown is not a blocker for the bounded answer about where `18×14` originates or whether Viewport/Render/Picker contain an independent `18×14` hard cap. It remains a required post-change validation dependency for any future authorized mutation task.
