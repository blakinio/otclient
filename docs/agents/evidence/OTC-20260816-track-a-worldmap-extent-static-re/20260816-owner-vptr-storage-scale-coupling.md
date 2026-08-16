# Handler-owner vptr and post-rebuild scale coupling

## Scope

This checkpoint continues `OTC-20260816-track-a-worldmap-extent-static-re` from retained same-repository historical evidence only. It does not create current runtime authority, does not use Synology as a static-analysis fallback, and does not authorize or perform client-byte mutation.

Exact historical client fence:

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

## Provenance

Two previously fenced retained sources are combined here:

1. runtime-memory/provenance artifact `9227370490`, run `31821458677`, digest `sha256:991f5c22a7ffc1d23c6597307a49728b363863a5acd6dd754bff1222404c8e2d`;
2. exact-SHA-fenced handler disassembly run `31804083206`, job `94778661881`.

The retained observer runtime/static mappings produce one consistent historical PIE base:

```text
historical PIE base = 0x5586665f8000
```

This is historical provenance only and is not a claim about any current process/session.

## Handler-owner primary vptr

Across the retained `CreateOnMap` / `ChangeOnMap` event snapshots, the same handler owner is present:

```text
owner runtime address = 0x55868276a460
```

The first QWORD of the owner snapshot is:

```text
runtime vptr = 0x55866967f1d8
```

Using the independently proven historical PIE base:

```text
0x55866967f1d8 - 0x5586665f8000 = 0x030871d8
```

Therefore:

```text
handler-owner static vptr = 0x030871d8
```

The retained vtable snapshot begins with runtime targets that translate to the following exact static addresses:

```text
0x5586673e68c0 -> 0x00dee8c0
0x5586673f7b20 -> 0x00dffb20
0x5586673fac50 -> 0x00e02c50
0x558666e1e890 -> 0x00826890
0x558666e1ebc0 -> 0x00826bc0
```

### FACT

- the common owner used by the retained map-event observations has exact historical static vptr `0x030871d8`;
- the first five retained vtable targets above are exact PIE translations from the same snapshot/base;
- exact-static census evidence independently contains the plain type name `N5tibia8worldmap31TWorldmapProtocolMessageHandlerE` at `0x1cd59a0` and the full `_Sp_counted_ptr_inplace<TWorldmapProtocolMessageHandler,...>` type string at `0x1cdba40`.

### INFERENCE

`TWorldmapProtocolMessageHandler` is a strong semantic candidate for the owner at static vptr `0x030871d8`, because the owner is the common receiver for the recovered FullMap/Create/Change/Delete family and the exact build contains the corresponding protocol-handler RTTI surface.

### UNKNOWN

The class identity is not promoted to FACT because the decisive Itanium vtable header/typeinfo relation immediately before `0x030871d8` has not been recovered. The exact discriminator window is:

```text
0x030871c8..0x030871d7
```

A proof must resolve the typeinfo pointer there (or an equivalent direct RTTI/control-block relation) to the protocol-handler type before naming the owner class.

## `0xced1b0` post-hash-rebuild dependency

The exact-SHA-fenced disassembly already proves that static `0xced1b0` rebuilds a bucketed linked-node structure with:

```text
self+0x48  bucket-array base candidate
self+0x50  bucket-count/size term
self+0x58  node-head candidate
self+0x60  count/state
node size  0x20 bytes
```

and uses `memset(base, 0, self+0x50 * 8)`, replacement-node allocation, shared-control/refcount-like handling, and unsigned division by the retained bucket-count value.

The retained exact code continues after the rebuild and adds a second dependency:

```text
lea  ..., [self+0x48]
rax = QWORD [self+0x30]
float value = DWORD/float [rax+0xd0]
value is converted to double and multiplied by the retained constant at static 0x29505a8
```

### FACT

- `0xced1b0` does not stop at rebuilding the bucketed `self+0x48..+0x60` structure;
- the same function subsequently consumes a floating-point value from the object referenced by `self+0x30`, at that dependency's `+0xd0` offset;
- this creates a direct static coupling between the candidate coordinate-to-tile hash structure and another polymorphic/owned dependency reachable at `self+0x30`.

### INFERENCE

The `self+0x30/+0xd0` floating-point value is scale/geometry/render-related candidate state because it is consumed immediately after the map-like bucket rebuild and participates in floating-point scaling arithmetic. It may help connect the storage candidate to viewport/render/camera dependencies.

### UNKNOWN

- exact owning class of `0xced1b0`;
- exact class identity of the `self+0x30` dependency;
- semantic name and unit of `+0xd0`;
- meaning/value of constant `0x29505a8`;
- whether this path implements camera scale, tile/world scale, render scale, load-factor normalization, or another unrelated floating calculation.

No render/camera class name is assigned by guess.

## Combined discriminator frontier

The retained evidence now exposes three high-value exact static identity windows:

```text
handler owner vptr        0x030871d8 -> header 0x030871c8..0x030871d7
18/14 geometry object     0x0308ce70 -> header 0x0308ce60..0x0308ce6f
18/14 control-like block  0x02f683d0 -> header 0x02f683c0..0x02f683cf
```

Exact-static string anchors relevant to those identities include:

```text
TWorldmapProtocolMessageHandler plain RTTI name       0x1cd59a0
counted TWorldmapProtocolMessageHandler type string   0x1cdba40
TWorldMapViewport plain RTTI name                     0x1ce1b60
counted TWorldMapViewport type string                 0x1cabb60
```

The previous exact-ELF graph probe matched the plain viewport name and a substring inside the counted name, but did not use the *full counted-type string start* `0x1cabb60` as a relocation target. Therefore absence of a retained counted-viewport relocation in that output is a coverage gap, not negative evidence.

## Next static actions

1. recover one of the exact vtable-header/typeinfo windows above from retained evidence;
2. explicitly target the full counted-type string starts (`0x1cabb60`, `0x1cdba40`) when an exact ELF becomes legally available again;
3. correlate the `self+0x30/+0xd0` dependency from `0xced1b0` with sibling owner-child vptrs and target RTTI surfaces;
4. continue writer/xref recovery for geometry-object `+0x48/+0x4c` and candidate bounds;
5. only after storage/render/camera/picker constraints are proven may mutation design begin.

## Disposition

```text
classification: MORE_STATIC_RE_NEEDED
STATIC_PATCH_GRAPH_READY: false
client bytes modified: false
runtime used by this continuation: false
Synology static RE used: false
```
