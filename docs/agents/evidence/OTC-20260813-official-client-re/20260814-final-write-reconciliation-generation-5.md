# Track A final-write reconciliation — generation 5

Date: 2026-08-14
Track: A — official native Linux Tibia client reverse engineering
Integration slice: `ci/OTC-20260815-track-a-verified-merge-slice-v2`
Supersedes integration attempt: PR `#297` / `ci/OTC-20260814-track-a-verified-merge-slice`

## Exact client fence

- version mapping: `15.32.df7b29`
- size: `51965216`
- SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- platform: official native Linux client only

The exact-build workflows cited below hard-check client size and SHA-256 before ELF analysis. The version string is the repository mapping for that digest/size pair.

## Branch reconciliation

At continuation start, `main` was `20919503467b7ea4812ac7176f4728be052e90bc`. The recovery-derived working branch had accumulated hundreds of commits relative to the merge-base, so it was **not** merged wholesale. The reviewed reconciliation was first isolated as PR `#297`. After the parallel-research coordination PR `#298` advanced `main`, repository rules required strict up-to-date `CI / Required`; rather than force/rebase the reviewed branch, this integration slice was rebuilt directly from `main@2b0a617ebea092afd21a0334337df9618a466386` with the same bounded evidence/reproducer payload plus the actionlint runner-label declaration.

Track B is out of scope and untouched.

## Corrected outbound ownership chain

### FACT

Exact-build recovery evidence establishes:

```text
semantic action
 -> TInternalGameActionRouter
 -> TProtocolMessageQueue builder
 -> clientMessageReadyToProcess
 -> Qt connection @ 0x19716a3
 -> heap QSlotObject invoker 0x7dd630
 -> TProtocolClientMessageProcessor
 -> TGameserverNetworkPacketRawDataProcessor
 -> TGameserverDualConnection
```

Retained owner fields:

- `+0xa00/+0xa08` -> `TProtocolClientMessageProcessor`; virtual `+0x10 = 0xc2df80`
- `+0xa10/+0xa18` -> `TGameserverNetworkPacketRawDataProcessor`; virtual `+0x10 = 0xb47130`
- `+0xc18/+0xc20` -> `TGameserverDualConnection`; virtual `+0x80 = 0xb56d60`, virtual `+0x78 = 0xb56970`, precondition `+0x90 = 0xb40370`

## Superseded model

### DISPROVEN / SUPERSEDED

```text
clientMessageReadyToProcess
 -> owner virtual +0x90 = 0x8409d0
 -> owner+0x88
 -> vtable 0x2f66288 +0xb8
 -> 0xb5b880
```

This model must not be promoted again. The real signal connection at `0x19716a3` uses heap `QSlotObject` invoker `0x7dd630`; the prior PMF `0x91` belongs to the preceding Qt connection. Independent ELF consistency checks also reject `0xb5b880` as the gameplay endpoint.

## TGameserverTCPConnection provenance

Primary exact-build workflow `tibia-official-client-re-gameserver-tcp-writer-provenance.yml`:

- run `31828102313`
- job `94857013988`
- run head `a9ad5731cea98b7517f8387288f6bcbc3b9fa3a9`
- conclusion `success`
- artifact id `9229609330`
- artifact digest `sha256:bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c`

The merge slice now preserves a hardened, `workflow_dispatch`-only version of this provenance probe at `.github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml`. The historical run/artifact above remains the provenance of the historical observation; the preserved workflow is the durable reproducer and adds fail-closed checks for its key static invariants.

### FACT — QMeta/type ownership

- QMetaObject `0x30b7d00`
- stringdata `0x1d4d2b0`
- metadata `0x1d4d1a0`
- `qt_static_metacall = 0xdd1cc0`
- class string: `tibia::network::TGameserverTCPConnection`
- method/type strings include `connected`, `disconnected`, `error`, `readyRead`, `onConnected`, `onError`, `QAbstractSocket::SocketError`, `onReadyRead`

### FACT — concrete QTcpSocket member construction

Exactly two direct QTcpSocket constructor callsites exist in the measured ELF:

```text
0x196ff2a
0x19702c7
```

Both construct a QTcpSocket and store the concrete socket pointer at receiver object member `+0x10`; the receiver vptr is `0x3084b38`. Both setup sequences bind callback `0xb46bd0`.

### FACT — direct RTTI slot proof

Follow-up workflow `.github/workflows/tibia-official-client-re-tcp-member-rtti.yml`:

- run `31833767461`
- job `94875322417`
- conclusion `success`
- artifact id `9231716774`
- artifact digest `sha256:2fee09b5cc85364223afe21a09d93cc817007853641ecaba8c2f36bbb6c5c83b`

The artifact directly resolves:

```text
[0x3084b38 - 0x8] -> RTTI 0x3080630
RTTI 0x3080630 -> tibia::network::TGameserverTCPConnection
```

Therefore the object whose vptr is `0x3084b38` is directly proven to be `TGameserverTCPConnection`, and its `+0x10` member is the concrete QTcpSocket constructed in the two constructor paths above.

### Review correction — RTTI relocation classification

The first reproducer revision treated every relocation whose addend equalled a target RTTI address as a possible vtable typeinfo slot. That generic enumeration could also include an Itanium RTTI base-class reference (notably `TProtocolWriter`'s base pointer to `TIODeviceWriter`) and therefore could emit a spurious vtable candidate from adjacent RTTI data.

This does **not** promote that spurious candidate into canonical evidence. The merge-slice workflow is corrected to:

- separate RTTI base/non-vtable references from validated vtable typeinfo slots;
- require a plausible Itanium vtable header and executable first entry before emitting a vtable;
- stop vtable-slot enumeration at the first non-executable entry rather than scanning into adjacent RTTI/vtables;
- fail closed unless the expected TCP/writer type names, validated address points, TCP typeinfo match, `TProtocolWriter -> TIODeviceWriter` base relationship, and QMeta static-metacall facts resolve.

The historical run remains evidence for its directly inspected fields, not for any unvalidated generic candidate emitted by the older enumeration logic.

### FACT — writer RTTI hierarchy

The exact-build artifact directly resolves:

```text
TIODeviceWriter
  RTTI: 0x3080718
  vtable symbol/header start: 0x2f69d38
  vtable address point: 0x2f69d48

TProtocolWriter
  RTTI: 0x3080728
  vtable symbol/header start: 0x2f69dc0
  vtable address point: 0x2f69dd0
  RTTI base -> 0x3080718 (TIODeviceWriter)
```

Thus `TProtocolWriter : TIODeviceWriter` is a direct typeinfo fact. The previously carried `TProtocolWriter` RTTI value `0x3080700` is superseded by the exact relocation/typeinfo result `0x3080728`.

### FACT — `0xb46bd0` writes through the proven QTcpSocket member

Function FDE `0xb46bd0..0xb46cce`:

- loads receiver `[this+0x10]`;
- uses QMeta object `0x30b7d00`;
- converts QString data to local 8-bit;
- appends byte `0x0a`;
- calls `QIODevice::write(QByteArray const&)` at `0xb46c75` with receiver `+0x10` as device.

### DISPROVEN as binary gameplay proof

Although `0xb46bd0` is now proven to write through `TGameserverTCPConnection::QTcpSocket*`, its payload is QString/local-8-bit plus newline. It is therefore **not** promoted as the binary Tibia gameplay-frame sink without additional causal framing evidence.

## Canonical binary-sink experiment reconciliation

Primary workflow run `31837878926`:

- workflow: `.github/workflows/tibia-official-client-re-network-outbound-binary-sink.yml`
- head: `53adb80250beddb4e73e83703b972103a2ec2f77`
- conclusion: `success`

### DISPROVEN

Technical workflow success does not establish semantic success. The candidate raw write site reported as `0xc33259` belongs to a function operating on `QMatrix4x4`, not a network/gameplay egress path. The experiment also did not resolve the expected imported raw `QIODevice::write(char const*, qint64)` endpoint. Consequently this run does **not** close P2 and its candidate must not be promoted to canonical gameplay egress.

## Remaining P2 boundary

### UNKNOWN

Still required:

1. concrete ownership/reference path from `TGameserverDualConnection` into a writer object;
2. gameplay payload serialization/framing order;
3. compression/encryption/sequence transformation boundary;
4. final binary socket write or equivalent QIODevice/socket egress;
5. causal proof using a controlled local/custom harness.

The next bounded experiment should therefore trace the actual `TProtocolWriter`/`TIODeviceWriter` construction and virtual dispatch graph from the already-proven `TGameserverDualConnection` path rather than enumerate generic `QIODevice::write` callsites again.

## Active stalled run

Run `31825417040` (`Track A final socket write resolution`) remained `queued` on the most recent observation recorded by this reconciliation. Per anti-stall rules, no conceptual duplicate should be dispatched merely to bypass the queue; independent evidence work continues. If the run becomes terminal, its artifact must still be consumed and reconciled.

## Repository-model reconciliation

### SUPERSEDED documentation gap

An earlier continuation snapshot reported `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` as absent. Current `main` contains that normative execution model. The earlier absence report is therefore **SUPERSEDED** and must not be treated as a current repository gap.

## Durable continuation rule

Do not claim full Track A completion from this evidence alone. P2 remains open, and P1/P0/action/coverage/final-validation acceptance slices remain to be closed. Every promotion must preserve the exact client fence and FACT/INFERENCE/ASSUMPTION/RECOMMENDATION/UNKNOWN/DISPROVEN/SUPERSEDED classifications.
