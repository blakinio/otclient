# QMeta relocation record layout — 2026-08-14

## Scope

Track A / `official-client-re` only. Subject: official native Linux Tibia client.

Exact client SHA256:

```text
e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Primary workflow evidence:

```text
.github/workflows/tibia-official-client-re-qmeta-relocation-records.yml
head: d23bcfadddcf63c89ac3e9cf2c0b35a0a0c90980
run: 31790093524
job: 94734812315
runner: synology-otclient-01
result: SUCCESS
```

The workflow decoded relocation-backed fixed-size records around independently calibrated protocol-handler metadata anchors. The records repeat every `0x40` bytes and contain eight qwords.

## FACT — the Worldmap record calibrates the structure

Worldmap record:

```text
record base: 0x3087800
qword +0x00: 0x0
qword +0x08: 0x1cd8a54
qword +0x10: 0x1cd8820
qword +0x18: 0xdf2a60
qword +0x20: 0x0
qword +0x28: 0x2f6ab00
qword +0x30: 0x0
qword +0x38: 0x0
```

Relocations classify:

- `+0x08 -> 0x1cd8a54` into read-only metadata/string-data region;
- `+0x10 -> 0x1cd8820` into read-only metadata region;
- `+0x18 -> 0xdf2a60` into executable segment;
- `+0x28 -> 0x2f6ab00` into writable/data segment.

`+0xdf2a60` is the same Worldmap dispatch function independently identified earlier by disassembly and jump-table reconstruction. That previous reconstruction maps its cases to `handleFullMapMessage`, row/column/floor handlers, `handleFieldDataMessage`, `handleCreateOnMapMessage`, `handleChangeOnMapMessage`, `handleDeleteOnMapMessage`, ambient light and Tibia time.

Therefore the executable pointer at record offset `+0x18` is directly calibrated as the Worldmap Qt static-metacall/dispatcher entry rather than merely an arbitrary code pointer.

## Structural record interpretation

Across the calibrated records the exact pattern is stable:

```text
+0x00  relocation type 1 / zero raw qword; executable code references address the record base
+0x08  R_X86_64_RELATIVE -> read-only string/metadata region
+0x10  R_X86_64_RELATIVE -> read-only metadata integer-table region
+0x18  R_X86_64_RELATIVE -> executable code
+0x20  zero / no relocation
+0x28  R_X86_64_RELATIVE -> data/writable-or-relro-associated region
+0x30  zero / no relocation
+0x38  zero / no relocation
record size: 0x40
```

**INFERENCE, high confidence:** this is the stripped PIE representation of a Qt `QMetaObject`-family generated record. The Worldmap calibration makes `+0x18 = static_metacall` effectively proven for Worldmap and strongly supports the same field role for records with the identical layout. Exact semantic names for every other pointer field remain subject to string/metadata-table decoding; do not over-label them yet.

## FACT — Chat static metacall entry recovered

Chat record:

```text
record base: 0x30877c0
+0x08 -> 0x1cd8268
+0x10 -> 0x1cd8060
+0x18 -> 0xd05f20 (executable)
+0x28 -> 0x2f6aa20
```

The record base itself has executable references including:

```text
0x7ffcbb
0x875f23
0xcf382e
0xcf3861
0xcf95d0
0xd05fe9
0xd0601c
0xde4040
0xe47144
0xe474a5
```

The exact binary independently contains the compact Chat method-name cluster:

```text
handleTalkMessage
handleMessageMessage
handleOpenChannelMessage
handleOpenOwnChannelMessage
handleCloseChannelMessage
handleChannelsMessage
handlePrivateChannelMessage
handleChannelEventMessage
handleNpcTalkPartersMessage
```

The next gate is to decode `0x1cd8268 / 0x1cd8060` and disassemble `+0xd05f20`, then map its cases to those names.

## FACT — GameEvent static metacall candidate recovered and prior addend corrected

GameEvent record:

```text
record base: 0x3087780
+0x08 -> 0x1cd7f44
+0x10 -> 0x1cd7ec0
+0x18 -> 0xd20800 (executable)
+0x28 -> 0x2f6a9e0
```

This **supersedes** the earlier provisional text that associated slot `0x3087788` with addend `0x1cd7e3c`. The exact record decoder proves the relocation at `0x3087788` has addend `0x1cd7f44`.

The exact binary independently has `TGameEventProtocolMessageHandler` and `handleGameEventMessage`, so `+0xd20800` is the calibrated executable static-metacall candidate for this handler record pending method-table decode.

## FACT — Effect static metacall candidate recovered

Effect record:

```text
record base: 0x30ce780
+0x08 -> 0x1d73f64
+0x10 -> 0x1d73ee0
+0x18 -> 0xd338d0 (executable)
+0x28 -> 0x2f762a0
```

The exact binary independently has the compact `TEffectProtocolMessageHandler` cluster:

```text
handleRemoveGraphicalEffectMessage
handleGraphicalEffectsMessage
```

Thus `+0xd338d0` is a high-confidence static-metacall entry for the Effect record, to be case-mapped next.

## Container-family caution

A record initially anchored from a nearby Container-region relocation exists at:

```text
record base: 0x3084f60
+0x08 -> 0x1cac968
+0x10 -> 0x1cac8c0
+0x18 -> 0xdcb130
+0x28 -> 0x2f65d80
```

However, **this record is not yet proven to be `TContainerProtocolMessageHandler`**. The literal `TContainerProtocolMessageHandler` occurs later in the read-only region around `0x1caef6a`, and neighboring fixed-size records are:

```text
base 0x3084fa0: +0x08 0x1cae518, +0x10 0x1cae3e0, +0x18 0xcf2aa0, +0x28 0x3080c80
base 0x3084fe0: +0x08 0x1caec88, +0x10 0x1cae760, +0x18 0xd1e000, +0x28 0x3080d00
```

Because `0x1caec88` is only about `0x2e2` bytes before the known Container class-name occurrence, `0x3084fe0 / +0xd1e000` is a stronger **candidate**, but this remains an inference until stringdata/metadata decoding proves class ownership. Do not promote `+0xdcb130` or `+0xd1e000` as Container without that proof.

## Neighboring 0x40-record families

Worldmap-adjacent records show a regular family:

```text
base 0x3087740: +0x18 -> 0xd1fde0
base 0x3087780: +0x18 -> 0xd20800  (GameEvent)
base 0x30877c0: +0x18 -> 0xd05f20  (Chat)
base 0x3087800: +0x18 -> 0xdf2a60  (Worldmap)
base 0x3087840: +0x18 -> 0xd15e40
base 0x3087880: +0x18 -> 0xd186f0
```

Effect-adjacent records likewise repeat at `0x40` byte spacing:

```text
base 0x30ce700: +0x18 -> 0xd227c0
base 0x30ce740: +0x18 -> 0xd1fd50
base 0x30ce780: +0x18 -> 0xd338d0  (Effect)
base 0x30ce7c0: +0x18 -> 0xd12ca0
base 0x30ce800: +0x18 -> 0xd12be0
```

These unlabeled neighbors are discovery candidates only until class ownership is decoded.

## Next deterministic gate

A follow-up workflow is versioned as:

```text
.github/workflows/tibia-official-client-re-qmeta-data-dump.yml
head introducing workflow: 16862d5a9d9978179e52eff0bfa256ff2e8af6bc
run: 31790262928
```

It dumps and tests the calibrated stringdata/metadata bases for Worldmap, Chat, GameEvent, Effect and Container candidates against multiple Qt relative-offset encodings. The immediate objective is to decode the Worldmap representation first, because its method semantics and static-metacall entry are already independently known, then apply the proven format to Chat and the unresolved Container/Creature/Player records.

No live client mutation, credential use, packet injection or new runtime attach was required for this evidence.
