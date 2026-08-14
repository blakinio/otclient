# Track A — ChatGPT P2 outgoing framing artifact analysis

Timestamp: 2026-08-14T18:42:00+02:00
Correction applied: 2026-08-14T18:57:00+02:00

Track: Track A / `official-client-re` / `OTCLIENT-TIBIA-RE` only.

> **SUPERSEDED INTERPRETATION:** the P2 workflow printed `PRIMARY_SLOT_90=0x8409d0`, `SUBOBJECT_VTABLE=0x2f66288`, `SUBOBJECT_SLOT_B8=0xb5b880`, and `DOWNSTREAM_HELPER_ROOT=0xb222a0` as hard-coded labels. Later relocation-aware and connection-site validation disproved the claimed `clientMessageReadyToProcess -> owner virtual +0x90 -> ... -> 0xb5b880` path. The canonical correction is `20260814-chatgpt-network-handoff-correction.md` and machine record `experiments/EXP-20260814-network-handoff-correction.yaml`.

## Repository / ownership boundary

This checkpoint is persisted on isolated recovery branch `ci/OTC-20260814-track-a-chatgpt-framing-recovery` because PR #289 head `e4c8334e73b04668a69b4cd2372b865248561ad5` was updated by another writer inside the current 45-minute lease window. No mutation of that writer's active branch/runtime is performed here.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## P2 experiment

```yaml
workflow: .github/workflows/tibia-official-client-re-outgoing-payload-consumers.yml
workflow_commit: c15899ebef7cadb7ce6f4a302a28dff064f6b537
run: 31815819731
job: 94817115581
result: SUCCESS
runner: synology-otclient-01
artifact:
  id: 9225203231
  name: track-a-outgoing-payload-consumers-31815819731
  digest: sha256:e0ca5a09b4ad7ea57a78833ceefa737a8330db837aedfc4218efb53d9b126f86
  report_size_bytes: 345729
```

The report begins with the exact client SHA/size fence and ends with `TRACK_A_OUTGOING_PAYLOAD_CONSUMERS_COMPLETE=true`.

## What the P2 artifact actually proves

The workflow source shows the following values were emitted with literal `echo` statements and therefore are **not recovered facts by themselves**:

```text
PRIMARY_OWNER_VTABLE=0x308c408
PRIMARY_SLOT_90=0x8409d0
SUBOBJECT_VTABLE=0x2f66288
SUBOBJECT_SLOT_B8=0xb5b880
DOWNSTREAM_HELPER_ROOT=0xb222a0
```

Independent later ELF relocation validation does confirm:

```text
0x308c408 + 0x90 = 0x8409d0
```

but the Qt connection that carries `clientMessageReadyToProcess` does not use that virtual slot. Instead, it installs a QSlotObject with invoker `0x7dd630`; see the correction evidence.

Independent later ELF validation also proves:

```text
0x2f66288 + 0xb8 = 0x313cce0
executable = false
```

and linear disassembly proves `0xb5b880` lies inside an instruction beginning at `0xb5b87c`, so `0xb5b880` is not a conventional function entry for the claimed vtable slot.

## Negative protobuf/string evidence

The exact binary scan reports zero literal matches for:

```text
OutGoingMessagePayload
OutgoingMessagePayload
MessageBody
SerializeWithCachedSizesToArray
SerializeToArray
ByteSizeLong
```

Classification:

- **FACT:** these exact literal names were absent from this exact-binary scan.
- **DISPROVEN:** an earlier unverified hypothesis that an `OutGoingMessagePayload` literal/envelope was already recovered from this build.
- **UNKNOWN:** protobuf or another generated serializer can still exist without these exported/literal names; the negative string result does not prove absence of generated serialization.

## Network symbol surface

GDB dynamic-symbol queries in the report resolve:

```text
QIODevice::write(QByteArray const&)@plt = 0x4de370
QTcpSocket::QTcpSocket(QObject*)@plt   = 0x4ddbc0
```

`QIODevice`, `QAbstractSocket`, `QTcpSocket`, and `writeData` strings exist in the binary, but no dynamic symbol for `QIODevice::writeData` or `QAbstractSocket::writeData` was recovered by this query.

A later exact-binary recovery run (`31821085647`, job `94834146391`) confirms exactly five direct calls to `QIODevice::write(QByteArray const&)@plt`:

```text
0x7dd563
0xb4066b
0xb46c75
0xc4a848
0xd08642
```

Notably `0x7dd563` is only `0xcd` bytes before the real QSlotObject invoker `0x7dd630`, making that local code cluster a high-priority structural candidate. Proximity alone is not promoted as a call edge.

## P2 call-window limitations

The P2 report independently scans windows beginning at `0xb5b880` and `0xb222a0`, but does not establish a structural edge between them. Since `0xb5b880` is now disproven as the claimed slot entry, direct-call results obtained by linear byte scanning from that non-instruction boundary must not be used as a semantic forward call graph.

`0xb222a0` remains independently disassembled data only; its relationship to the outbound queue path is `UNKNOWN`.

## CI status observed during this slice

PR #289 head `e4c8334e73b04668a69b4cd2372b865248561ad5` has CI run `31818176071 = FAILURE`. The failing job is `94824765433 Fast Checks / Syntax and workflow validation`, specifically `yamllint`.

Fatal yamllint finding:

```text
docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-quantitative-coverage-baseline.yaml
63:147 [new-line-at-end-of-file] no new line character at the end of file
```

Seven Track A workflow comment-spacing findings are warnings, not the fatal error shown in this run.

## Current next static gate

Start from the corrected Qt connection:

```text
TProtocolMessageQueue at [owner+0x88]
  -> clientMessageReadyToProcess wrapper 0xde91b0
  -> QObject::connectImpl @ 0x19716a3
  -> QSlotObject invoker 0x7dd630
  -> stored containing-owner pointer at slot-object +0x10
```

Disassemble/classify `0x7dd630`, recover its call-operation branch and concrete consumer, then prove a structural path to one of the confirmed `QIODevice::write` callsites or to an indirect/virtual socket-write path. Do not return to the superseded `+0x90 -> 0x8409d0 -> 0xb5b880` hypothesis.
