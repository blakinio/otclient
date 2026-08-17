# World-map downstream exact-static evidence — consumer handoff for PR #367

## Disposition

```text
WORLD_MAP_DOWNSTREAM_STATIC_EVIDENCE_READY=true
producer PR: #446
consumer PR: #367
runtime access: none
client executed: false
process memory accessed: false
canonical state accessed: false
client bytes mutated: false
raw client uploaded: false
```

This handoff contains the curated exact-client downstream evidence requested by PR #367 after it consumed producer #437. Broad source scans were used only to find candidate windows; facts below are restricted to exact type-anchored code, accepted prior exact-runtime correlation, or explicitly labeled inference. Raw vtable spillover and generic virtual-call false positives are excluded.

## Exact client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux
```

No official-client process was started. Both physical jobs only read the exact size/SHA-fenced ELF and emitted bounded sanitized windows.

## Provenance

Broad downstream staging:

```text
run              32001356705
source job       95302168871       SUCCESS
source artifact  9278519216
digest           sha256:e10347435bece4cbedc7fca54b782cea76f9f1dab3b042082fe3bcc15f7c0728
hosted job       95302411849       SUCCESS
final artifact   9278527206
digest           sha256:af12b2af9c725ca402224876c3cbd0c01306f47b37e717548c5817310dd3bc9b
bounded windows  236
raw code bytes   532736
```

Targeted reverse-vtable/data discriminator:

```text
run              32002326947
source job       95304896213       SUCCESS
source artifact  9278827774
digest           sha256:8f6a9feaea607475f6f9d25d200d858f52714f9384561bd4010405d26a78009a
hosted job       95305039463       SUCCESS
final artifact   9278833445
digest           sha256:7505aeae6e79e8829adf60261e1a3b50f27e0514f50136161e5f715a27124218
bounded windows  15
raw code bytes   38400
```

## Exact upstream origin of the `18 / 14` Storage pair

This resolves the main upstream question left open by #437.

### 1. Handler constructor has a hardcoded `18 / 14` master default

The exact `TWorldmapProtocolMessageHandler` constructor is anchored by its exact vptr:

```text
0x00803c01  lea  rax,[rip+...] -> 0x030871d8
0x00803c08  mov  QWORD PTR [rbx],rax
```

Later in the same constructor:

```text
0x00803d6f  lea  rax,[rip+...] -> 0x02f615a0
0x00803d76  mov  QWORD PTR [rbx+0x90],rax
0x00803d7d  mov  rax,QWORD PTR [rip+...] -> 0x01cdd958
0x00803d8b  mov  QWORD PTR [rbx+0xb0],rax
```

Exact bytes at `0x01cdd958` begin:

```text
12 00 00 00  0e 00 00 00  08 00 00 00  06 00 00 00
```

Therefore:

```text
QWORD 0x01cdd958 = 0x0000000e00000012
DWORD low         = 18
DWORD high        = 14
```

**FACT:** the Handler constructor directly initializes `Handler+0xb0/+0xb4` to the static literal pair `18 / 14`.

This is a constructor default. A complete post-construction writer census for this Handler master pair is not yet proven, so this evidence does **not** claim global immutability.

### 2. FullMap calls the exact geometry fanout on the Handler

Existing exact evidence in consumer PR #367 proves `FullMap@0x00cec8d0` directly calls `0x00cdb770(owner)` and that `owner` is the world-map Handler. The targeted scan independently recovered the direct call site `0x00cec955 -> 0x00cdb770`.

Inside `0x00cdb770`:

```text
0x00cdb772  lea  rsi,[rdi+0x90]
0x00cdb77f  mov  r12,rdi
0x00cdb78b  lea  r14,[rsp+0x90]
0x00cdb793  mov  rdi,r14
0x00cdb796  call 0x00bc6350
```

Thus `0x00bc6350` receives:

```text
output = snapshot @ r14
source = Handler+0x90
```

### 3. `0x00bc6350` copies the Handler master pair into snapshot `+0x38`

Exact body:

```text
0x00bc6368  movq  xmm0,QWORD PTR [rsi+0x8]
0x00bc636d  movq  xmm2,QWORD PTR [rsi+0x38]
0x00bc6372  movq  xmm1,QWORD PTR [rsi+0x20]
...
0x00bc63af  movq  QWORD PTR [rax+0x38],xmm1
```

Because `source = Handler+0x90`:

```text
source+0x20 = Handler+0xb0
```

**FACT:** snapshot `+0x38` receives the Handler `+0xb0/+0xb4` QWORD, whose constructor default is exactly `18 / 14`.

### 4. The snapshot is dispatched to `Handler+0x10` virtual slot `+0x60`

Immediately after snapshot construction:

```text
0x00cdb79b  mov  rdi,QWORD PTR [r12+0x10]
0x00cdb7a0  mov  edx,0x1
0x00cdb7a5  mov  rsi,r14
0x00cdb7a8  mov  rax,QWORD PTR [rdi]
0x00cdb7ab  call QWORD PTR [rax+0x60]
```

PR #367 retained exact runtime already proves this Handler `+0x10` object has static vptr `0x0308ce70`. Producer #437 proved that exact vptr is:

```text
tibia::worldmap::TWorldMapStorage
```

The accepted Storage address point `0x0308ce70` has slot 12 at address-point `+0x60`, resolving to:

```text
0x00cc6cd0
```

The targeted reverse-vtable discriminator found the canonical relation:

```text
address point  0x0308ce70
slot           12
slot address   0x0308ced0
function       0x00cc6cd0
typeinfo       0x0308b5f0
relation       RELA:R_X86_64_RELATIVE
offset-to-top  0
```

A second raw hit at `0x0028f728` is rejected: it has a RAW/non-relocation header and non-zero offset-to-top and is not promoted as an owning vtable.

### 5. Storage slot 12 copies snapshot `18 / 14` into Storage `+0x48/+0x4c`

Exact Storage function:

```text
0x00cc6cf3  movq  xmm0,QWORD PTR [rsi+0x38]
...
0x00cc6d2c  movq  QWORD PTR [r13+0x48],xmm0
```

**FACT — end-to-end chain:** 

```text
static literal 18/14 @ 0x01cdd958
  -> Handler constructor Handler+0xb0/+0xb4
  -> 0xbc6350 snapshot+0x38
  -> 0xcdb770 Handler+0x10 exact TWorldMapStorage slot12
  -> Storage+0x48/+0x4c
  -> historical exact runtime observation: 18/14
```

### Mutability classification

```yaml
FACT:
  Handler constructor default: hardcoded static 18/14
  Storage constructor default: zero
  Storage geometry pair: mutable/copy-driven through slot 12
UNKNOWN:
  complete later-writer census for Handler+0xb0/+0xb4
  whether a runtime/configuration path can replace the Handler master pair after construction
```

So `18/14` is **not merely a runtime accident and not a Storage-local constant**: its exact constructor origin is a static Handler/Viewport-family default, and Storage receives it by copy.

## Exact `TWorldMapViewport` geometry default and recomputation

The exact Viewport constructor `0x00cbf680` installs vptr `0x0308c9a8` and directly consumes the same `0x01cdd958` packed literal:

```text
0x00cbf68b  lea  rax,[rip+...] -> 0x0308c9a8
0x00cbf6b0  mov  rax,QWORD PTR [rip+...] -> 0x01cdd958
0x00cbf6be  mov  QWORD PTR [rbx+0x40],rax
```

**FACT:** Viewport `+0x40/+0x44` has constructor default `18 / 14`.

But `0x00cbf700` later recomputes that pair:

```text
reads QWORD Viewport+0x10
reads QWORD Viewport+0x18
loads packed delta 15/11 from 0x01d63cd0
performs packed signed arithmetic
writes QWORD Viewport+0x40
sets Viewport+0x48 = 8
continues into signed divide-by-32 style arithmetic using 0x1f correction masks
```

Therefore the Viewport pair is not safely modeled as immutable even though its constructor default is exactly `18 / 14`.

## `TWorldMapRenderProvider` — direct bounds/culling/iteration dependencies

Exact identity:

```text
vptr      0x02f6c258
typeinfo  0x03089b70
RTTI      tibia::worldmap::TWorldMapRenderProvider
```

Curated primary vtable range is **slots 0..21**. Raw entries after slot 21 cross into adjacent vtables/metadata and are excluded.

Load-bearing exact functions:

### slot 16 — `0x00cd08b0`

FACT:
- iterates records with fixed `0x30` stride;
- performs coordinate arithmetic with `& 0x1f` and signed shift/divide-by-32 style operations;
- marks/filters records after these bounds calculations.

### slot 14 — `0x00cd2260`

FACT:
- consumes a dependency from `this+0x68`;
- rejects negative/out-of-range coordinates against dependency dimension fields;
- linearizes the accepted coordinate as a `y * width + x`-style index;
- bounds-checks the resulting indexed/vector range before use.

This is direct clipping/indexing evidence. Exact source member names are UNKNOWN.

### slot 13 — `0x00cd1e50`

FACT:
- obtains a range through another virtual producer;
- iterates fixed `0x20`-byte entries;
- constructs extent/ordered-state records during iteration.

### slots 10/11 — `0x00cea540` / `0x00cec020`

FACT: repeated `&0x1f`, shift-by-5 and 32-multiple arithmetic occurs in these world-map RenderProvider paths.

### slot 21 — `0x00ce9700`

FACT:
- constructs exact `TWorldMapExtent` / `TWorldMapSubfieldExtent`-related state;
- contains a fixed `0x20` allocation;
- includes bounded bit/modulo-style selection.

**INFERENCE:** together these are direct 32-cell/chunk render-iteration, culling and clipping dependencies that must be included in any extent patch graph.

## `TWorldMapPicker` — exact screen/world 32-cell coupling

Exact identity:

```text
vptr      0x02f6b7c8
typeinfo  0x03086888
RTTI      tibia::worldmap::TWorldMapPicker
```

Curated primary vtable range is **slots 0..7**.

### slot 5 — `0x00cd0400`

FACT:
- consumes packed coordinates;
- uses `shl 5`;
- applies `0x1f` sign/floor correction;
- uses packed add + arithmetic right shift by 5;
- writes the converted packed pair.

This is exact fixed-32 coordinate conversion evidence.

### slot 4 — `0x00cd65b0`

FACT:
- range traversal uses shift-by-5 arithmetic;
- iterates in steps of `0x20`;
- constructs `0x18`-byte extent-like records.

### slot 7 — `0x00ce80c0`

FACT:
- obtains an extent/range;
- uses `shl 5` and coordinate subtraction;
- builds bounds and iterates fixed `0x28`-byte candidates.

No primary Picker slot produced a promoted direct `18/14` literal writer. Its direct fixed coupling is the 32-cell conversion/bounds surface.

## `TWorldMapCamera` — exact layout, projection semantics still bounded UNKNOWN

Exact identity:

```text
vptr      0x03083968
typeinfo  0x03080500
RTTI      tibia::renderer::TWorldMapCamera
```

The primary virtual surface is only **slots 0..4** and is lifecycle/meta-heavy. Raw scan entries beyond that belong to adjacent vtables and are excluded.

Exact constructor/layout facts:
- direct Camera objects initialize approximately `0xe0` bytes;
- vptr `0x03083968` is installed;
- two 64-byte groups of vector constants are initialized from static data around `0x01cd5910..0x01cd5940`;
- embedded address point `0x02f69278` is installed in two subobjects around `Camera+0x98` and `Camera+0xb8`;
- `Camera+0xd0` is initialized to float bit pattern `0x3f800000` (`1.0`);
- surrounding fields are zero-initialized.

**INFERENCE:** this is transform/scale-like Camera state.

**UNKNOWN:** the current bounded evidence does not justify naming a projection matrix, asserting a projection formula, or selecting a Camera patch site.

## Fixed allocations / masks / packing recovered

FACT:
- exact `18/14` packed literal at `0x01cdd958`;
- exact Handler and Viewport constructors consume it;
- RenderProvider and Picker repeatedly use hard 32-cell arithmetic: shift-by-5, `&0x1f`, `0x20` stepping/allocation or equivalent signed conversion;
- fixed record/allocation sizes recovered on relevant paths include `0x18`, `0x20`, `0x28` and `0x30` depending on consumer.

No broad raw immediate hit is promoted merely because it occurred inside a large bounded window.

## Corrections to raw scans

1. Generic `call [vtable+0x60]` candidates are not Storage-slot12 facts unless the receiving object is type-anchored. The accepted chain uses `Handler+0x10` retained exact vptr `0x0308ce70` plus exact Storage RTTI.
2. Reverse-vtable candidate `0x0028f728` for function `0x00cc6cd0` is rejected. Canonical Storage address point `0x0308ce70`, slot 12, is relocation-backed and offset-to-top zero.
3. Broad vtable walks crossed into adjacent tables. Only RenderProvider slots `0..21`, Camera `0..4`, Picker `0..7` are promoted.

## Remaining UNKNOWNs

- complete later-writer census for Handler `+0xb0/+0xb4`;
- exact source member names/units of the geometry pairs;
- exact named Camera projection/viewport formula;
- whether widening the master `18/14` pair alone is sufficient — current evidence says it is coupled to Viewport recomputation, RenderProvider 32-grid bounds and Picker transforms;
- safe client-byte patch sites remain a consumer decision after complete dependency reconciliation.

No client bytes were modified and this producer does not propose a patch.
