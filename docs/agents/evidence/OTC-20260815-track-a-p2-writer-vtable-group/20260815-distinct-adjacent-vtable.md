# Track A P2 writer vtable-group classification

Task: `OTC-20260815-track-a-p2-writer-vtable-group`  
Draft PR: `#305`  
Executed head: `c479f58a1b45d6a4a2d4063d07ea83057532b8f7`  
Workflow run/job: `31884166982` / `95010894063` — `SUCCESS`  
Sanitized artifact: `9246799418`  
Sanitized artifact ZIP SHA-256: `d0bf06e8c973f351fe96037445de0586f30e5044f5d1a097bfc866b85c0df48f`

## Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

The workflow independently verifies three reviewed historical text artifacts before parsing:

```text
9231716774 / d99919403c001fbcc2a959346443c405f8a2234fb81438fbc6a626a1833edb82
9229609330 / bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c
9229251044 / 4b914f65d4a4eb3c91a39ce9918e8e4f865fadcf4853ab4af25ffa5d5f519520
```

All three source texts contain the exact client SHA fence.

## Result

```text
P2_VTABLE_GROUP_RESULT=PROVEN_DISTINCT_ADJACENT_ITANIUM_VTABLE_IDENTITY_NAME_UNKNOWN
P2_FIRST_WRITER_TRANSFORM_BOUNDARY=UNKNOWN
```

## FACT — `0x2f69e30` is a valid distinct Itanium address point

The reviewed RTTI/vtable artifact identifies canonical `TProtocolWriter` as:

```text
RTTI 0x3080728
primary address point 0x2f69dd0
offset-to-top 0
```

The bounded table window after that primary address point contains:

```text
absolute 0x2f69e20 -> 0x0          # offset-to-top
absolute 0x2f69e28 -> 0x3080748    # distinct typeinfo
absolute 0x2f69e30 -> 0x7de7f0     # first function
absolute 0x2f69e38 -> 0x7dfd60     # second function
```

Thus `0x2f69e30` is structurally a normal Itanium address point with its own typeinfo `0x3080748` and `offset-to-top=0`.

Its typeinfo differs from both:

```text
TProtocolWriter  0x3080728
TIODeviceWriter  0x3080718
```

## FACT — a separately allocated object receives `0x2f69e30`

The reviewed setup artifact independently contains the allocation/constructor sequence around `0x1970edd..0x1970f3b`:

- allocate `0x250` bytes;
- actual shared object begins at allocation `+0x10`;
- load address `0x2f69e30`;
- store it at the actual object's vptr.

This is not merely a scanner-window adjacency. A distinct allocated object is instantiated with `0x2f69e30`.

## DISPROVEN — simple secondary/base address-point interpretation of canonical `TProtocolWriter`

The initial hypothesis that `0x2f69e30` can simply be treated as a secondary/base-class address point belonging to canonical `TProtocolWriter` is rejected by the reviewed evidence:

- it has its own distinct typeinfo pointer `0x3080748`, not canonical `TProtocolWriter` typeinfo `0x3080728`;
- it is installed as the vptr of a separately allocated retained object.

This does **not** prove a semantic class name for RTTI `0x3080748`; it only prevents collapsing the object into canonical `TProtocolWriter` based on address adjacency.

## INFERENCE — `0x7de7f0 / 0x7dfd60` are teardown-like

Both reviewed functions load `0x2f69e30` and write it to `[this]`. `0x7de7f0` additionally releases linked/list state and clears object storage around `+0x208..+0x238`. This supports a bounded `TEARDOWN_LIKE` inference, not a symbol/name claim.

No framing/compression/encryption transition is proven by these functions.

## UNKNOWN

- semantic class name for RTTI `0x3080748`;
- base/inheritance relationship represented by that RTTI;
- first writer transform/framing boundary;
- gameplay framing/serialization order;
- final binary QIODevice/socket egress;
- relation of historical `0x3084c70 -> +0xd0 -> 0xb40630` table to canonical writer branch.

The historical `0x3084c70` family remains explicitly separate: its reviewed run reports `rtti=0`, no direct LEA xrefs, and `+0xd0 -> 0xb40630`. No provenance intersection with `0x2f69e30` is claimed.

## Effect on accepted PR #301 wording

PR #301's phrase `retained intermediate object (exact class UNKNOWN)` remains correct. The stronger statement is now:

```text
retained intermediate object
  vptr = 0x2f69e30
  Itanium typeinfo = 0x3080748
  semantic type name = UNKNOWN
  not collapsible into canonical TProtocolWriter by adjacency
```

The accepted `TProtocolClientMessageProcessor -> intermediate object -> retained shared TProtocolWriter` ownership relation is not invalidated.

## Researcher disposition proposal

`ACCEPT_WITH_EDITS` as bounded negative/type-structure evidence.

P2 remains incomplete. A later transform-order task must start from actual serialization/data-stream behavior or recover the name/role of RTTI `0x3080748`; it must not infer a transform boundary from vtable adjacency alone.
