# World-map exact static evidence — consumer handoff for PR #367

## Disposition

```text
WORLD_MAP_STATIC_EVIDENCE_READY=true
consumer PR: #367
producer PR: #437
consumer branch modified by producer: false
client bytes modified: false
runtime access: none
```

This is the curated durable handoff from the exact official native-Linux Tibia client. It supersedes the broad displacement classification in the raw hosted bundle where a bounded code window could contain stack offsets or an adjacent function. Only type-anchored constructor/vtable evidence is promoted below; ABI-dependent conclusions are labeled as inference.

## Exact client fence and provenance

```text
version   15.32.df7b29
size      51965216
sha256    e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform  official native Linux
```

Physical read-only source staging:

```text
run       31972743782
job       95227595548
runner    synology-otclient-01
artifact  9270235755
name      track-a-worldmap-exact-static-source-31972743782
digest    sha256:039d22fe5f88a07784c4ddc32cf6b1d9c2d07a34e90ed5902ffd21d3acd5735b
```

Hosted recovery/validation:

```text
run       31972915689
job       95228024727
result    success
artifact  9270276361
name      track-a-worldmap-exact-static-final-recovery-31972915689
digest    sha256:0dc8d0a44e5a2550ef79c219bda14787796ef7accc0ab1627fecd7c6d55330bc
```

The source job recovered 3/3 requested identity windows, nine direct vptr xrefs and 49 bounded code windows totaling 52,992 raw code bytes. No raw client was uploaded. The official client was not executed by this producer; no process memory, canonical runtime state, X11/VNC/login/gameplay or client-byte mutation was used.

## Requested identity windows — exact recovery

### 1. `0x030871c8..0x030871d7` → vptr `0x030871d8`

```text
bytes       0000000000000000b85f080300000000
qword[-2]   0x0000000000000000
qword[-1]   0x0000000003085fb8
offset-top  0
typeinfo    0x03085fb8
name ptr    0x01cd59a0
RTTI        N5tibia8worldmap31TWorldmapProtocolMessageHandlerE
class       tibia::worldmap::TWorldmapProtocolMessageHandler
first slot  0x00dee8c0
```

The typeinfo pointer and typeinfo-name pointer are both backed by `.rela.dyn` `R_X86_64_RELATIVE` relations. The header is consistent with the Itanium ABI address-point layout: offset-to-top at `vptr-16`, typeinfo pointer at `vptr-8`.

Direct vptr xrefs recovered:

```text
0x00803c01
0x00803f8a
0x00826891
0x00826bc1
```

### 2. `0x0308ce60..0x0308ce6f` → vptr `0x0308ce70`

```text
bytes       0000000000000000f0b5080300000000
qword[-2]   0x0000000000000000
qword[-1]   0x000000000308b5f0
offset-top  0
typeinfo    0x0308b5f0
name ptr    0x01ce1c00
RTTI        N5tibia8worldmap16TWorldMapStorageE
class       tibia::worldmap::TWorldMapStorage
first slot  0x00dee8e0
```

The typeinfo/name relations are `.rela.dyn` `R_X86_64_RELATIVE`. This resolves the largest consumer-side identity ambiguity:

**FACT:** historical runtime object vptr `0x0308ce70` is `TWorldMapStorage`, not `TWorldMapViewport`.

Direct vptr xrefs recovered:

```text
0x0083f492
0x0083f682
0x00cbf37a
```

### 3. `0x02f683c0..0x02f683cf` → vptr `0x02f683d0`

```text
bytes       000000000000000020fb070300000000
qword[-2]   0x0000000000000000
qword[-1]   0x000000000307fb20
offset-top  0
typeinfo    0x0307fb20
name ptr    0x01ca9180
RTTI        St23_Sp_counted_ptr_inplaceIN5tibia8worldmap16TWorldMapStorageESaIvELN9__gnu_cxx12_Lock_policyE2EE
class       std::_Sp_counted_ptr_inplace<tibia::worldmap::TWorldMapStorage, std::allocator<void>, (__gnu_cxx::_Lock_policy)2>
first slot  0x006f3360
```

The typeinfo/name relations are `.rela.dyn` `R_X86_64_RELATIVE`.

Direct vptr xrefs recovered:

```text
0x007e9f04
0x00a464b1
```

This upgrades the previous `owner+0x10/+0x18` object/control-block inference in PR #367 to an exact `TWorldMapStorage` plus its counted allocation wrapper.

## `TWorldMapStorage` geometry layout

### Constructor anchors the object and all six requested offsets

At `0x00cbf37a` the constructor loads the exact Storage vptr and writes it to the object pointed to by `rbx`:

```text
0x00cbf37a  lea  rax,[rip+...]          -> 0x0308ce70
0x00cbf381  mov  QWORD PTR [rbx+0x18],0
0x00cbf389  mov  QWORD PTR [rbx],rax
0x00cbf3bc  mov  QWORD PTR [rbx+0x30],0
0x00cbf39b  lea  rax,[rip+...]          -> 0x02f61578
0x00cbf3a2  mov  QWORD PTR [rbx+0x40],rax
0x00cbf3cb  mov  QWORD PTR [rbx+0x48],0
```

**FACT:** the constructor initializes three 64-bit geometry pairs:

```text
QWORD Storage+0x18 -> DWORD +0x18 / +0x1c
QWORD Storage+0x30 -> DWORD +0x30 / +0x34
QWORD Storage+0x48 -> DWORD +0x48 / +0x4c
```

All six requested DWORDs therefore have a direct initialization writer. The constructor value is zero; `18/14` are not constructor literals.

### `+0x48/+0x4c` belong to an exact `TWorldMapExtent` subobject

The vptr written at `Storage+0x40` is exactly:

```text
vptr       0x02f61578
typeinfo   0x0306fc60
RTTI       N5tibia8worldmap15TWorldMapExtentE
class      tibia::worldmap::TWorldMapExtent
RTTI str   0x01c8fee0
first slot 0x007c24e0
```

**FACT:** `Storage+0x48` and `Storage+0x4c` are the first two DWORD payload positions (`TWorldMapExtent+0x8/+0xc`) inside the embedded exact `TWorldMapExtent` beginning at `Storage+0x40`.

The exact member names/units are not recovered, so `width`/`height` remains an inference rather than a renamed fact.

## Direct geometry writers and readers

### Mutating writer — Storage vtable slot 12

Storage address point `0x0308ce70`, slot 12 (`0x0308ced0`) resolves to `0x00cc6cd0`. The function starts by preserving `this`:

```text
0x00cc6cd9  mov   r13,rdi
```

It reads three QWORD pairs from its second argument and writes them into the Storage object:

```text
0x00cc6ce4  mov   rax,QWORD PTR [rsi+0x8]
0x00cc6ceb  movq  xmm1,QWORD PTR [rsi+0x20]
0x00cc6cf3  movq  xmm0,QWORD PTR [rsi+0x38]

0x00cc6d12  mov   QWORD PTR [r13+0x18],rax
0x00cc6d26  movq  QWORD PTR [r13+0x30],xmm1
0x00cc6d2c  movq  QWORD PTR [r13+0x48],xmm0
```

**FACT:** one exact Storage virtual writer mutates all six requested DWORDs as three QWORD pairs. The `+0x48/+0x4c` pair comes from argument QWORD `rsi+0x38`.

Therefore `+0x48/+0x4c` are mutable/copy-driven at this layer, not immutable hardcoded `18/14` constants.

### Bounds reader — Storage vtable slot 14

Slot 14 (`0x0308cee0`) resolves to `0x00cb01d0`. It anchors `this` as `rbx`:

```text
0x00cb01d1  mov rbx,rdi
```

The exact comparisons are:

```text
0x00cb021f  cmp DWORD PTR [rbx+0x18],edx   ; reject if lower > value
0x00cb0224  cmp DWORD PTR [rbx+0x30],edx   ; reject if upper <= value
0x00cb0229  cmp DWORD PTR [rbx+0x1c],eax   ; reject if lower > value
0x00cb022e  cmp DWORD PTR [rbx+0x34],eax   ; reject if upper <= value
```

**FACT:** `+0x18/+0x30` and `+0x1c/+0x34` are used as lower/upper pairs in half-open containment logic:

```text
lower <= coordinate < upper
```

This directly supports the consumer's previous arithmetic `32555-32537=18` and `32517-32503=14`; it also establishes that the upper pair is max-exclusive in this reader path.

### Paired read/export — Storage vtable slot 13

Slot 13 (`0x0308ced8`) resolves to `0x00cb0180` and contains:

```text
0x00cb0180  mov rdx,QWORD PTR [rsi+0x18]
0x00cb0191  mov rcx,QWORD PTR [rsi+0x30]
0x00cb01ad  mov rdx,QWORD PTR [rsi+0x48]
0x00cb0184  mov rax,rdi
...
0x00cb01cc  ret
```

**INFERENCE:** the shape is consistent with an ABI hidden structure-return pointer in `rdi`, shifting Storage `this` to `rsi`. Under that interpretation this virtual method reads/exports all three paired regions, including `+0x48/+0x4c` as one QWORD. This ABI role is not promoted to FACT without a recovered signature.

## Coverage of requested offsets

| Offset | Initialized | Mutated | Read | Direct structural result |
|---|---|---|---|---|
| `+0x18` | yes, ctor QWORD `+0x18` | yes, slot 12 QWORD `+0x18` | yes, slot 14 | lower-bound component |
| `+0x1c` | yes, high DWORD of ctor QWORD `+0x18` | yes, high DWORD of slot-12 QWORD `+0x18` | yes, slot 14 | lower-bound component |
| `+0x30` | yes, ctor QWORD `+0x30` | yes, slot 12 QWORD `+0x30` | yes, slot 14 | upper-bound component |
| `+0x34` | yes, high DWORD of ctor QWORD `+0x30` | yes, high DWORD of slot-12 QWORD `+0x30` | yes, slot 14 | upper-bound component |
| `+0x48` | yes, ctor QWORD `+0x48` | yes, slot 12 QWORD `+0x48` | paired read in slot 13 (ABI inference) | first DWORD in embedded `TWorldMapExtent` |
| `+0x4c` | yes, high DWORD of ctor QWORD `+0x48` | yes, high DWORD of slot-12 QWORD `+0x48` | paired read in slot 13 (ABI inference) | second DWORD in embedded `TWorldMapExtent` |

A separate `[this+0x4c]` store is not required because exact constructor and mutator code use an 8-byte store at `this+0x48`, covering both DWORDs.

## Correlation with PR #367 retained runtime `18×14`

Consumer evidence file:

`docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-retained-owner-geometry-object.md`

records the same exact-vptr historical object with:

```text
+0x18 = 32537
+0x1c = 32503
+0x30 = 32555
+0x34 = 32517
+0x48 = 18
+0x4c = 14
```

and:

```text
32555 - 32537 = 18
32517 - 32503 = 14
```

The new exact-static evidence changes the interpretation materially:

- **FACT:** that object is `TWorldMapStorage`.
- **FACT:** the first two coordinate pairs are read as half-open lower/upper bounds.
- **FACT:** the `18/14` pair is inside embedded `TWorldMapExtent` and has a direct virtual writer at `0x00cc6d2c` that copies the complete pair from argument `rsi+0x38`.
- **FACT:** constructor/default for the pair is zero, so `18/14` are not fixed constructor constants.
- **UNKNOWN:** which upstream producer computes/configures/parses the QWORD passed at `rsi+0x38` in the dynamic event that yielded `18/14`.
- **INFERENCE:** `+0x48/+0x4c` are X/Y extent or width/height values because they are fields of `TWorldMapExtent` and equal the two half-open bound differences. Exact C++ member names and units remain unknown.

The raw hosted bounded windows did **not** contain a direct immediate store of decimal `18` to `this+0x48` or decimal `14` to `this+0x4c`. That is no longer a blocker to writer identification because the actual exact writer is a QWORD copy, not an immediate pair literal.

## Follow-on exact RTTI anchors

These identities are directly recovered and can be used by #367 for the next static graph step:

| Type | RTTI string | Typeinfo | vptr | First slot |
|---|---|---|---|---|
| `TWorldMapViewport` | `0x01ce1b60` | `0x0308b590` | `0x0308c9a8` | `0x00dee920` |
| `TWorldMapStorage` | `0x01ce1c00` | `0x0308b5f0` | `0x0308ce70` | `0x00dee8e0` |
| `TWorldMapRenderProvider` | `0x01cddd20` | `0x03089b70` | `0x02f6c258` | `0x00820970` |
| `TWorldMapCamera` | `0x01cabce0` | `0x03080500` | `0x03083968` | `0x00dedda0` |
| `TWorldMapPicker` | `0x01cdb600` | `0x03086888` | `0x02f6b7c8` | `0x008205c0` |
| `TWorldMapExtent` | `0x01c8fee0` | `0x0306fc60` | `0x02f61578` | `0x007c24e0` |
| `TWorldMapSubfieldExtent` | `0x01c9fe20` | `0x0307d1f8` | `0x02f63fa8` | `0x00748330` |

These are identity anchors only. They do not by themselves prove storage capacity/eviction, render culling iteration bounds, camera projection limits or picker screen/world clipping.

## Curated correction to raw analyzer output

The hosted artifact's generic displacement scanner tags every requested displacement inside a geometry-marked bounded window. A window beginning at the Storage constructor also contains later adjacent functions, and some vtable windows contain stack accesses such as `[rsp+0x4c]`. Therefore those generic hits are not used as direct class-field proof here.

The durable evidence above is restricted to:

1. exact Storage constructor code anchored by the `0x0308ce70` vptr write;
2. exact functions reached from the `TWorldMapStorage` vtable;
3. directly verified RTTI/vtable relationships;
4. explicit ABI inference where a hidden sret affects the `this` register.

## Remaining unknowns / consumer frontier

- exact RTTI identity of embedded vptr `0x02f615a0` at `Storage+0x10` and `Storage+0x28`;
- exact C++ field names/units for the six geometry DWORDs;
- upstream producer of the slot-12 input QWORD at `rsi+0x38`, hence the exact dynamic source of `18/14`;
- whether the source pair is parser-derived, computed from bounds, configured elsewhere, or copied from another object;
- storage capacity/eviction and fixed allocation limits;
- render iteration/culling bounds;
- camera projection/scale limits;
- picker screen/world limits and parser packing/masks beyond the evidence above.

No client patch or safe mutation site is proposed by this producer.
