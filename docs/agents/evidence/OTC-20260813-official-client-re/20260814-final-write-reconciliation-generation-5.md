# Track A final-write reconciliation — generation 5

Date: 2026-08-14
Track: A — official native Linux Tibia client reverse engineering
Continuation branch: `ci/OTC-20260814-track-a-final-write-continuation`

## Exact client fence

- version mapping: `15.32.df7b29`
- size: `51965216`
- sha256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- platform: native Linux only

The primary provenance workflow used below performs hard checks for both exact size and exact SHA-256 before inspecting the ELF. The version label is the canonical repository mapping for that exact digest/size pair.

## Live branch / PR reconciliation

Verified at continuation start:

- `main`: `20919503467b7ea4812ac7176f4728be052e90bc`
- PR `#289`: open draft, base `main`, primary head `4ac4a7546b182fcc11aaac3893c2a0116304f3e2`
- primary branch `ci/OTC-20260813-official-client-re-continuation`: `4ac4a7546b182fcc11aaac3893c2a0116304f3e2`
- recovery branch `ci/OTC-20260814-track-a-chatgpt-framing-recovery`: `a5e330ae12bb36db49bf8f897f3786b2069f912d`
- primary and recovery are diverged; the recovery branch contains the corrected outbound Qt connection reconstruction while primary contains later, independently-produced TCP/QMeta evidence.

The continuation branch was therefore created from the recovery head instead of writing to either active/shared branch.

## Corrected outbound chain

`FACT / exact-build evidence retained from recovery`:

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

Owner fields retained by the continuation:

- `+0xa00/+0xa08` -> `TProtocolClientMessageProcessor`; virtual `+0x10 = 0xc2df80`
- `+0xa10/+0xa18` -> `TGameserverNetworkPacketRawDataProcessor`; virtual `+0x10 = 0xb47130`
- `+0xc18/+0xc20` -> `TGameserverDualConnection`; virtual `+0x80 = 0xb56d60`, virtual `+0x78 = 0xb56970`, precondition `+0x90 = 0xb40370`

## Superseded model

`DISPROVEN / SUPERSEDED`:

```text
clientMessageReadyToProcess
 -> owner virtual +0x90 = 0x8409d0
 -> owner+0x88
 -> vtable 0x2f66288 +0xb8
 -> 0xb5b880
```

This model must not be promoted again. Recovery evidence establishes that the real signal connection at `0x19716a3` uses a heap `QSlotObject` invoker `0x7dd630`, while the old PMF `0x91` was taken from the preceding Qt connection. The old target also failed independent ELF consistency checks: the relevant vtable slot resolves to non-executable `0x313cce0`, `0xb5b880` is not an instruction boundary, and the workflow that promoted it hard-coded the value.

`CONFLICT`: primary evidence at/through `4ac4a754...` still contains wording that calls `0xb5b880` canonical. That wording is stale and is not accepted by this continuation.

## Primary TCP/QMeta evidence reconciled

Primary workflow:

- workflow: `.github/workflows/tibia-official-client-re-gameserver-tcp-writer-provenance.yml`
- run: `31828102313`
- job: `94857013988`
- run head: `a9ad5731cea98b7517f8387288f6bcbc3b9fa3a9`
- conclusion: `success`
- artifact: `track-a-gameserver-tcp-writer-provenance-31828102313`
- artifact id: `9229609330`
- artifact digest: `sha256:bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c`

The workflow hard-checks:

```text
stat(client) == 51965216
sha256(client) == e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

### FACT — QMeta object belongs to the TCP connection class

The exact artifact reports:

- QMetaObject `0x30b7d00`
- stringdata `0x1d4d2b0`
- metadata `0x1d4d1a0`
- `qt_static_metacall = 0xdd1cc0`
- string `0x1d4d310 = "tibia::network::TGameserverTCPConnection"`
- adjacent method/type strings include `connected`, `disconnected`, `error`, `readyRead`, `onConnected`, `onError`, `QAbstractSocket::SocketError`, and `onReadyRead`
- exact relocation at `0x30b7d00` is to `QObject::staticMetaObject@Qt_6`

The static metacall FDE is `0xdd1cc0..0xdd1ea9` and one dispatch path tail-jumps to `0xb46bd0` at `0xdd1e4e`.

### FACT — exactly two direct QTcpSocket constructor calls in the exact ELF

The exact static scan reports:

```text
QTCPSOCKET_CTOR_DIRECT_CALL_COUNT=2
QTCPSOCKET_CTOR_DIRECT_CALL_SITES=0x196ff2a,0x19702c7
```

Both call `_ZN10QTcpSocketC1EP7QObject@plt` at `0x4ddbc0`.

### FACT — construction dataflow reaches the object used by `0xb46bd0`

For the first construction at `0x196ff2a`:

- a `0x20` control block is allocated;
- the `QTcpSocket` object is constructed at control-block `+0x10` (`r12`);
- a separate `0x50` control block is allocated;
- its object begins at `rbx+0x10` and receives a QObject base;
- that object's vptr is set to address point `0x3084b38` at `0x196ff98`;
- its member at object `+0x10` receives the concrete QTcpSocket pointer (`[rbx+0x20] = r12`) at `0x196ff90`;
- the same object is used as the receiver for a Qt connection whose slot payload contains function `0xb46bd0` (`0x196ffc6`).

The second construction at `0x19702c7` repeats the same structure:

- QTcpSocket object at control-block `+0x10`;
- receiver QObject vptr `0x3084b38` at `0x197032e`;
- receiver object `+0x10` receives that QTcpSocket pointer at `0x197033d`;
- another Qt connection payload contains `0xb46bd0` at `0x197035f`.

### FACT — `0xb46bd0` writes through receiver `+0x10`

FDE `0xb46bd0..0xb46cce`:

- loads `[this+0x10]`;
- calls virtual slot `+0x120` twice with `QVariant` values;
- emits QMeta signal via `0x30b7d00`;
- converts QString data from receiver fields to local 8-bit;
- appends byte `0x0a`;
- invokes `QIODevice::write(QByteArray const&)` at `0xb46c75` using `[this+0x10]` as the device.

### DERIVED — concrete member identity pending direct RTTI slot proof

The construction/QMeta evidence strongly derives that the object with vptr `0x3084b38` is `tibia::network::TGameserverTCPConnection` and that its member `+0x10` is the just-constructed `QTcpSocket`. This is not promoted to the final type-layout FACT until the vtable header at `0x3084b38-0x8` is independently shown to reference RTTI `0x3080630` and the RTTI name is decoded.

The newline writer must also remain separated from binary gameplay framing until its semantic role is proven. A newline payload alone is not a Tibia gameplay-frame proof.

## Missing mandatory document

`UNKNOWN / repository gap`: `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` is named by the continuation prompt but is absent from both the inspected primary/recovery repository trees. The programme/canonical/agent execution documents remain available, so this is recorded as a documentation gap rather than a current P2 blocker.

## Active external run at handover

Run `31825417040`, job `94848268697`, workflow `Track A final socket write resolution` was still `queued` on the first live check. No duplicate was dispatched. Its terminal result must be consumed when available.

## Immediate continuation experiment

Next bounded exact-build experiment on this branch will:

1. resolve the vtable header and RTTI name for address point `0x3084b38`;
2. enumerate RTTI-backed vtable candidates for `TGameserverTCPConnection`, `TGameserverNetworkPacketConnection`, `TIODeviceWriter`, and `TProtocolWriter`;
3. dump QMeta metadata/stringdata words needed to map static-metacall method indices;
4. preserve exact SHA/size fencing;
5. continue from the concrete TCP member toward the binary writer without using the superseded `0xb5b880` model.
