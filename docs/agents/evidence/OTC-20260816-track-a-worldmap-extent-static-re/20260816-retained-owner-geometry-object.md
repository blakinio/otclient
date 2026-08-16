# Retained owner geometry object — direct 18×14 field recovery

## Scope

This checkpoint continues task `OTC-20260816-track-a-worldmap-extent-static-re` using retained same-repository evidence only. It does not create current runtime authority, does not use Synology as a static-analysis fallback, and does not authorize or perform client-byte mutation.

Exact historical client fence remains:

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

## Provenance

Retained artifact:

```text
artifact  9227370490
name      track-a-persistent-provenance-dump
run       31821458677
head      f23e9df548859d11520bbd2983c0df4e9923c2e7
digest    sha256:991f5c22a7ffc1d23c6597307a49728b363863a5acd6dd754bff1222404c8e2d
```

The artifact preserves `map-provenance-persistent-events.tsv`, `map-provenance-persistent-raw.log`, `map-provenance-persistent-strips.tsv` and the GDB observer transcript.

The retained GDB transcript places the research observer breakpoints at:

```text
CreateOnMap runtime       0x5586672e4c70
ChangeOnMap runtime       0x5586672e4f40
DeleteOnMap runtime       0x5586672cce20
FullMap runtime           0x5586672e48d0
MapDescription runtime    0x558667fa0ea3
```

Subtracting their independently recovered static offsets yields one consistent historical PIE base:

```text
historical PIE base = 0x5586665f8000
```

This historical address translation is evidence provenance only; it is not a claim about any current process/session.

## Stable handler owner and `owner+0x10` object

All three retained event hits — two `ChangeOnMap` and one `CreateOnMap` — have the same handler owner:

```text
rdi = 0x55868276a460
rdx = 0x55868276a460
```

The owner snapshot contains the following stable object/control-like pointer pairs:

```text
owner+0x10 = 0x55867df448c0   owner+0x18 = 0x55867df448b0
owner+0x20 = 0x55866aa91b90   owner+0x28 = 0x55866aa91b80
owner+0x30 = 0x55867a883b00   owner+0x38 = 0x55867a883af0
owner+0x40 = 0x55866c5c1a40   owner+0x48 = 0x55866c5c1a30
owner+0x50 = 0x55866aaded40   owner+0x58 = 0x55866aaded30
owner+0x60 = 0x55866aab3d80   owner+0x68 = 0x55866aab3d70
owner+0x70 = 0x55866aa90430   owner+0x78 = 0x55866aa90420
owner+0x80 = 0x55867a88f280   owner+0x88 = 0x55867a88f270
```

The adjacent `object` / `object-0x10` pattern is consistent with shared-lifetime/control-block ownership but is not promoted to a semantic class claim without ABI/RTTI proof.

The object reached directly via `owner+0x10` is:

```text
runtime object       0x55867df448c0
runtime vptr         0x558669684e70
static vptr          0x0308ce70
owner+0x18 companion 0x55867df448b0
companion vptr       0x5586695603d0
static companion vptr 0x02f683d0
```

The static vptr values use the proven historical PIE base above.

## Direct geometry fields

The first 0x80 bytes of the `owner+0x10` target are stable across all three retained hits. Direct little-endian DWORD decoding gives:

| Object offset | Exact DWORD value |
|---|---:|
| `+0x18` | `32537` |
| `+0x1c` | `32503` |
| `+0x30` | `32555` |
| `+0x34` | `32517` |
| `+0x38` | `8` |
| `+0x48` | `18` |
| `+0x4c` | `14` |
| `+0x50` | `8` |
| `+0x58` | `7` |
| `+0x60` | `19` |

Two independent exact arithmetic relations occur in the same object:

```text
32555 - 32537 = 18
32517 - 32503 = 14
```

and the object separately stores:

```text
DWORD object+0x48 = 18
DWORD object+0x4c = 14
```

### FACT

- A concrete object directly reached through the handler's `owner+0x10` path stores an exact `18,14` pair at `+0x48/+0x4c`.
- The same object stores two coordinate-like pairs whose exact differences are independently `18` and `14`.
- The snapshot is stable across two retained `ChangeOnMap` hits and one retained `CreateOnMap` hit.
- The object's exact historical static vptr is `0x0308ce70`.
- Existing exact disassembly already proves the `owner+0x10 -> virtual slot +0xa0` path is shared by FullMap/Create/Change/Delete-family handling.

This upgrades the previous geometry evidence materially: `18×14` is no longer supported only by strip-span arithmetic; exact stored `18` and `14` values now exist in a concrete worldmap-handler dependency object.

### INFERENCE

- `+0x18/+0x1c` are plausible lower/minimum X/Y fields.
- `+0x30/+0x34` are plausible upper or max-exclusive X/Y fields.
- `+0x48/+0x4c` are plausible width/height or extent fields because they equal the corresponding pairwise differences.
- `owner+0x10/+0x18` is consistent with a `std::shared_ptr`-style object/control-block pair.
- `TWorldMapViewport` is a plausible class identity for the `owner+0x10` target, but this is not yet proven.

### UNKNOWN

- exact class identity of the object at `owner+0x10`;
- exact semantic field names and units for `+0x18/+0x1c/+0x30/+0x34/+0x48/+0x4c`;
- whether the upper pair is inclusive, exclusive or transformed;
- constructor/default writer for the `18/14` pair;
- all readers and writers of those fields;
- whether changing the pair alone would increase received, retained or rendered map area safely;
- render/camera/picker and storage constraints coupled to these values.

## Correlation with retained strip geometry

The retained Z=7 strip evidence contains horizontal groups:

```text
X = 32537..32554
```

which exactly matches the half-open interval interpretation:

```text
[32537, 32555) -> 18 X positions
```

The strip Y examples are `32502` and `32516`, while the object stores `32503` and `32517` in the candidate Y-bound fields. That one-row offset is material and prevents promoting a simple strip-to-field identity without recovering the transform/writer convention.

## RTTI discriminator still required

Exact-static census evidence already gives a candidate `TWorldMapViewport` typeinfo object start at `0x0308b590` from the proven typeinfo-name relocation at `0x0308b598 -> 0x01ce1b60`.

Under the Itanium ABI hypothesis, the object vptr `0x0308ce70` should be associated with a vtable header immediately before it. A direct relocation/word proof around `0x0308ce60..0x0308ce6f` linking that vtable to the candidate viewport typeinfo would upgrade the class identity. Current retained artifacts inspected in this continuation do not contain that decisive header/relocation window.

Therefore:

```text
TWorldMapViewport identity for vptr 0x0308ce70 = UNKNOWN
```

No class name is assigned by guess.

## Next static actions

1. recover retained or exact-static bytes/relocations around `0x0308ce60..0x0308ce6f` and identify the `0x0308ce70` vtable;
2. recover xrefs/writers for object fields `+0x48/+0x4c` and the candidate boundary fields;
3. compare sibling owner child vptrs, including `0x0308cfd8` and `0x0308d078`, against retained target RTTI/control-block surfaces;
4. continue the existing `0xceca50` and `0xced1b0` storage correlation;
5. follow proven consumers into render-provider, camera and picker bounds before any mutation design.

## Disposition

```text
classification: MORE_STATIC_RE_NEEDED
STATIC_PATCH_GRAPH_READY: false
client bytes modified: false
runtime used by this continuation: false
```

The recovered exact `18/14` object fields are a new load-bearing fact, but they are not yet a safe patch site.