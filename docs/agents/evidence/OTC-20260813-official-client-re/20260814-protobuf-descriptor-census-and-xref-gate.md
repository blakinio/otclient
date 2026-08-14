# Protobuf descriptor census and xref gate — 2026-08-14

## Scope

Track A / `official-client-re` only. Subject: official native Linux Tibia client.

Exact client SHA256:

```text
e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Embedded protobuf descriptor census

Workflow:

```text
.github/workflows/tibia-official-client-re-protobuf-descriptor-census.yml
parser revision: 2
head: f3082b8e9070d390251e5ecf0338ed800e58f5b1
run: 31789613193
job: 94733342439
runner: synology-otclient-01
result: SUCCESS
```

The parser enumerated candidate serialized `FileDescriptorProto` records by requiring an exact protobuf field-1 framing of a `*.proto` filename, then structurally parsed descriptor/message/field records until the first invalid outer field. The run found exactly seven valid embedded descriptors:

```text
shared.proto
appearances.proto
map.proto
sounds-common.proto
sounds.proto
google/protobuf/descriptor.proto
google/protobuf/cpp_features.proto
```

### FACT — Coordinate schema is directly recovered

`shared.proto`, package `tibia.protobuf.shared`, contains `Coordinate` with exactly:

```text
field x: number=1, label=1, type=13 (uint32)
field y: number=2, label=1, type=13 (uint32)
field z: number=3, label=1, type=13 (uint32)
```

This independently confirms the previously decoded `Coordinate` field numbering and scalar types.

### FACT — selected game protocol messages are not present in these embedded FileDescriptorProto records

The census found no embedded descriptor definition for:

```text
GameserverMessageMoveCreature
GameserverMessagePlayerDataCurrent
GameserverMessageContainer
GameserverMessageTalk
GameclientMessageMoveObject
GameclientMessageAttack
GameclientMessageFollow
GameclientMessageTalk
GameclientMessageTradeObject
GameclientMessageGoPath
WorldmapObjectPosition
ObjectIdentifierAndPosition
```

This is a negative result about the **embedded FileDescriptorProto set only**. It does not mean these messages/types are absent from the client; their names are independently present in the exact binary and several are already proven protocol surfaces. Their field layouts therefore must be recovered from generated C++ metadata/accessors/disassembly/runtime objects rather than from serialized embedded file descriptors.

## First generic xref experiment

Historical exact-binary scan:

```text
head: 55dc75c830e571490be30a5c83a922a528c5931f
run: 31788735824
job: 94730524231
runner: synology-otclient-01
job conclusion: CANCELLED by workflow timeout
```

The Python scan nevertheless emitted `TRACK_A_XREF_GRAPH_COMPLETE=true` before GitHub recorded cancellation. Therefore its completed printed observations are usable with the timeout boundary recorded.

### FACT — absolute qword references to the selected literal strings were zero

For every scanned occurrence of the selected handler/method/outbound message literal strings, the experiment reported `qword_refs=0`. This includes the compact Chat/Container/Creature/Player/Effect/Market/Trade/Quest/GameEvent targets and the outbound `MoveObject`, `Attack`, `Follow`, `Talk`, `TradeObject`, `GoPath` names.

### LIMITATION

The v1 implementation rescanned the entire executable range for each literal occurrence, making it O(target-occurrences × executable-size). It completed the Python output only near the workflow timeout and the job was then cancelled. This is an implementation-performance failure, not evidence that broader metadata/code xrefs do not exist.

## Linear direct-RIP xref gate

Replacement experiment:

```text
.github/workflows/tibia-official-client-re-xref-graph-v2.yml
head: cfbe04c03de34f83646a82569c90dafaf342c129
run: 31789670398
job: 94733517691
runner: synology-otclient-01
result: SUCCESS
scanner: one linear executable pass
```

### FACT — tested literal addresses have zero direct RIP-relative LEA/MOV references

The linear scanner completed in seconds and reported:

```text
TOTAL_DIRECT_RIPREFS=0
TRACK_A_XREF_V2_COMPLETE=true
```

Every tested occurrence had `direct_riprefs=0`, including handler class literals, selected `handle*Message` literals, outbound `MoveObject/Attack/Follow/Talk/TradeObject/GoPath`, and inbound `MoveCreature/PlayerDataCurrent/Container/Talk`.

This validates the v1 observation with an efficient successful run: the tested code is not reached through a simple executable RIP-relative reference to the exact literal address in the LEA/MOV forms scanned.

## Classic Qt stringdata-layout hypothesis

Workflow:

```text
.github/workflows/tibia-official-client-re-qmeta-stringdata-reconstruct.yml
head: 56fb4409c01cd963a9fb651b83a78af4dcbef2a8
run: 31789875696
job: 94734149282
result: SUCCESS
```

The experiment tested a classic Qt-generated stringdata representation consisting of a fixed array of `(offset,length)` pairs immediately before the class string. It was calibrated across Worldmap, Chat, Container, Creature, Player, Effect, Market, NPC Trade, Player Trade, Quest and Game Event.

### FACT

Every class returned `table_candidates=0` while the workflow itself passed. Therefore that exact stringdata-layout hypothesis is rejected for these occurrences in this binary. This is not evidence that QMetaObject metadata is absent; it means the representation differs from the assumed classic layout or the observed strings are not the start of that generated structure.

## ELF relocation xref breakthrough

Workflow:

```text
.github/workflows/tibia-official-client-re-elf-relocation-xrefs.yml
head: 772a8b94138f651233be5526bc3af3fc5f0bc8d8
run: 31789986261
job: 94734485022
result: SUCCESS
```

The exact PIE ELF contains many `SHT_RELA` records, including `R_X86_64_RELATIVE` relocations whose addends point into the compact protocol/QMeta string regions. This explains why raw file qword searches and direct literal RIP references were insufficient: the load-time pointers are represented by relocation slots/addends rather than final in-file pointer values.

### FACT — independently known Worldmap metadata address is relocation-backed

For `TWorldmapProtocolMessageHandler`, the relocation scan found a nearby relocation:

```text
slot: 0x3087808
addend: 0x1cd8a54
```

`0x1cd8a54` is the same metadata-region address independently identified earlier during successful Worldmap QMeta dispatch reconstruction. This is strong calibration evidence that the ELF relocation route is reaching the actual generated metadata representation rather than an unrelated textual copy.

### FACT — regular protocol-handler relocation family

The relocation scan found nearby slots/addends in the same generated metadata region for multiple handlers, including:

```text
GameEvent: slot 0x3087788 -> addend 0x1cd7e3c
Chat:      slot 0x30877c8 -> addend 0x1cd8268
Worldmap:  slot 0x3087808 -> addend 0x1cd8a54
Container-related compact region: slot 0x3084f68 -> addend 0x1caef4c
```

The `GameEvent -> Chat -> Worldmap` slots differ by exactly `0x40`, which is consistent with a regular fixed-size generated metadata record family. This is currently a structural inference pending field-by-field record decoding; the addresses themselves are direct relocation facts.

### FACT — protobuf/message type strings are also relocation-backed at enclosing-name starts

For selected generated protobuf names, exact relocation addends commonly point to the beginning of the enclosing fully qualified/mangled type-name string rather than to the interior `GameclientMessage*`/`GameserverMessage*` substring. Examples observed in the successful run include relocation-backed strings containing:

- `tibia::protobuf::gameclientmessages::GameclientMessageMoveObject`
- `GameclientMessageAttack`
- `GameclientMessageFollow`
- `GameclientMessageTalk`
- `GameclientMessageTradeObject`
- `GameclientMessageGoPath`
- `tibia::protobuf::gameservermessages::GameserverMessageMoveCreature`
- `GameserverMessagePlayerDataCurrent`
- `GameserverMessageContainer`
- `GameserverMessageTalk`

This is a materially better route to generated protobuf metadata/default instances than xrefing the interior literal substring directly.

## Current QMeta record decoder

A follow-up exact-binary workflow is versioned as:

```text
.github/workflows/tibia-official-client-re-qmeta-relocation-records.yml
head introducing workflow: d23bcfadddcf63c89ac3e9cf2c0b35a0a0c90980
run: 31790093524
```

It treats the calibrated relocation slots as anchors and decodes the surrounding `0x40` candidate records, classifying each relocation addend as executable/data/string and finding executable RIP references to record fields. No result is promoted until that run reaches terminal state and its log is inspected.

## Research consequence

The direct paths below are rejected for selected literals:

```text
literal -> absolute qword pointer
literal -> direct executable RIP-relative LEA/MOV
classic immediate (offset,length) Qt stringdata table before class literal
```

The promoted direction is now:

```text
ELF RELA slot/addend -> generated metadata record -> static-metacall / descriptor / default-instance / accessor
```

Next deterministic gates:

1. decode the calibrated 0x40 relocation records around Worldmap/Chat/GameEvent and verify a code-pointer/static-metacall field;
2. once calibrated on Worldmap's already-known semantics, apply the record format to Chat/Container/Effect/Market/Trade/Quest/GameEvent;
3. follow generated protobuf relocation-backed fully qualified type-name structures toward descriptor/default-instance/accessor code for MoveCreature/player state/container/talk and outbound action messages;
4. perform runtime validation only after concrete version-fenced entry points are recovered.

No client login, packet injection, runtime attach, or owner interaction was required for these static experiments.
