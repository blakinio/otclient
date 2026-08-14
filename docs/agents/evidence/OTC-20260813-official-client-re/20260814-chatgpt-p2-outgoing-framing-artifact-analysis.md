# Track A — ChatGPT P2 outgoing framing artifact analysis

Timestamp: 2026-08-14T18:42:00+02:00

Track: Track A / `official-client-re` / `OTCLIENT-TIBIA-RE` only.

## Repository / ownership boundary

This checkpoint is intentionally persisted on isolated recovery branch `ci/OTC-20260814-track-a-chatgpt-framing-recovery` because PR #289 head `e4c8334e73b04668a69b4cd2372b865248561ad5` was updated by another writer inside the current 45-minute lease window. No mutation of that writer's active branch/runtime is performed here.

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

The downloaded report begins with the exact client SHA/size fence and ends with `TRACK_A_OUTGOING_PAYLOAD_CONSUMERS_COMPLETE=true`.

## Reproduced structural chain

The artifact independently reports:

```text
PRIMARY_OWNER_VTABLE=0x308c408
PRIMARY_SLOT_90=0x8409d0
SUBOBJECT_VTABLE=0x2f66288
SUBOBJECT_SLOT_B8=0xb5b880
```

This is consistent with the previously recovered queue-to-owner delegation chain. The concrete next implementation body remains `0xb5b880`.

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
- **UNKNOWN:** protobuf or another generated serializer can still exist without these exported/literal names; the negative string result does not prove absence of protobuf/generated serialization.

## Network symbol surface

GDB dynamic-symbol queries in the report resolve:

```text
QIODevice::write(QByteArray const&)@plt = 0x4de370
QTcpSocket::QTcpSocket(QObject*)@plt   = 0x4ddbc0
```

`QIODevice`, `QAbstractSocket`, `QTcpSocket`, and `writeData` strings exist in the binary, but no dynamic symbol for `QIODevice::writeData` or `QAbstractSocket::writeData` was recovered by this query.

## Important call-graph correction

The report scans two independent bounded direct-call windows:

```text
subobject_slot_b8: start 0xb5b880 size 0x1000
downstream_helper: start 0xb222a0 size 0x1400
```

In those reported windows:

- no direct `call rel32` to `QIODevice::write(QByteArray const&)@plt (0x4de370)` is reported;
- the report does not itself establish a direct or indirect edge `0xb5b880 -> 0xb222a0`;
- therefore `0xb222a0` must not be promoted as a proven downstream child of `0xb5b880` merely because the workflow named it `DOWNSTREAM_HELPER_ROOT`.

Classification:

- **FACT:** `0xb5b880` has a large exact-binary body and numerous direct executable callees in the bounded window.
- **FACT:** `0xb222a0` was independently disassembled/scanned.
- **UNKNOWN:** whether `0xb222a0` lies on the same concrete outbound message path.
- **UNKNOWN:** exact serializer, framing transform, buffer-encryption/compression stage, and final `QIODevice`/`QTcpSocket` write site.

## Selected direct callees from `0xb5b880`

The artifact records executable direct targets including:

```text
0x6b23c0
0x7b9140
0x19a5eb0
0x6b24e0
0x7b7f20
0x78e800
0x19a3080
0xc33830
0x19b1d40
0x7b5a20
```

The included disassembly shows several of these are allocation/tree/container/value-copy helpers rather than an obvious socket-write primitive. This narrows the next experiment away from simple proximity/string heuristics.

## CI status observed during this slice

PR #289 exact head `e4c8334e73b04668a69b4cd2372b865248561ad5` has CI run `31818176071 = FAILURE`. The failing job is `94824765433 Fast Checks / Syntax and workflow validation`, specifically `yamllint`.

Fatal yamllint finding from the job log:

```text
docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-quantitative-coverage-baseline.yaml
63:147 [new-line-at-end-of-file] no new line character at the end of file
```

Seven Track A workflow comment-spacing findings are warnings, not the fatal error shown in this run.

## Next static experiment

Do not guess the serializer from `0xb5b880` adjacency. Build a reverse/direct-call provenance experiment that:

1. globally enumerates direct callsites to `QIODevice::write(QByteArray const&)@plt (0x4de370)` and other candidate byte-output Qt symbols;
2. reconstructs bounded caller functions around those sites;
3. builds a reverse direct-call graph from each write-site caller for a bounded depth;
4. independently builds a forward direct-call graph from the proven `0xb5b880` body/callees;
5. intersects both graphs and reports only structurally shared functions/edges;
6. separately scans for virtual/indirect call patterns where direct intersection is empty;
7. promotes framing/final-write only if an exact structural path is recovered.

No live-client effect is required for this next gate.
