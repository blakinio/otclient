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

No `DIRECT_RIPREFS` line was emitted for the scanned literal-string addresses.

### LIMITATION

The v1 implementation rescanned the entire executable range for each literal occurrence, making it O(target-occurrences × executable-size). It completed the Python output only near the workflow timeout and the job was then cancelled. This is an implementation-performance failure, not evidence that broader metadata/code xrefs do not exist.

## Replacement xref gate

A linear one-pass replacement is now versioned as:

```text
.github/workflows/tibia-official-client-re-xref-graph-v2.yml
head introducing workflow: cfbe04c03de34f83646a82569c90dafaf342c129
run: 31789670398
```

It scans executable RIP-relative LEA/MOV references once and indexes only the selected literal VAs. This removes the multiplicative full-binary rescans from v1.

## Research consequence

The direct path `literal string -> absolute qword pointer -> code` is rejected for the tested literals. The next deterministic routes are:

1. consume the linear RIP-reference v2 result;
2. reconstruct Qt metadata structures from compact string tables and their integer offsets rather than assuming absolute string pointers;
3. locate generated protobuf descriptor/default-instance/accessor code for high-value messages whose serialized file descriptors are not embedded;
4. continue runtime validation only with version-fenced concrete entry points.

No client login, packet injection, runtime attach, or owner interaction was required for these static experiments.
