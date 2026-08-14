# Track A — queue QSlot consumer success

Date: 2026-08-14
Track: A / official native Linux Tibia client RE
Branch: `ci/OTC-20260814-track-a-chatgpt-framing-recovery`
Exact client SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
Workflow run: `31821495294`
Job: `94835543783`
Result: `SUCCESS`
Runner: `synology-otclient-01`

## FACT

1. The exact `clientMessageReadyToProcess` connection at `0x19716a3` uses a heap-allocated 24-byte Qt `QSlotObject`.
2. The signal wrapper is `0xde91b0` and is referenced at the connection site by `lea` at `0x197163c`.
3. The QSlotObject invoker is `0x7dd630`; the exact build contains one direct executable reference to this invoker, `lea 0x7dd630` at `0x1971670`.
4. The connection setup stores the containing owner pointer into the QSlotObject at `[slot_object+0x10]` before `QObject::connectImpl` at `0x19716a3`.
5. Therefore the previous interpretation that this edge was a PMF `{0x91,0}` / containing-owner virtual `+0x90` edge is not the implementation of this connection.
6. The `0x7dd630` invoker, on the active invoke path (`edi == 1`), loads the saved owner from `[slot_object+0x10]` and uses:
   - `owner+0xc18`, virtual `+0x90`, as a gate/check at `0x7dd654..0x7dd664`;
   - `owner+0xa00`, virtual `+0x10`, at `0x7dd675..0x7dd67f`;
   - `owner+0xa10`, virtual `+0x10`, at `0x7dd689..0x7dd693`;
   - `owner+0xc18`, virtual `+0x80`, at `0x7dd69d..0x7dd6a7`;
   - `owner+0xc18`, virtual `+0x78`, at `0x7dd6b4..0x7dd6be`.
7. A neighboring transport-relevant function beginning at `0x7dd3f0` uses the same owner family:
   - `owner+0xa10`, virtual `+0x18` at `0x7dd45e..0x7dd470`;
   - `owner+0x9f0`, including byte `[field+0x20]` at `0x7dd477..0x7dd487`.
8. In the `0x7dd3f0` function, the object loaded through `owner+0x9f0` is dereferenced to another object (`r12 = [field]`). Its vtable slot `+0xe8` is compared with concrete function `0xb40630` at `0x7dd500..0x7dd528`.
9. On the `+0xe8 == 0xb40630` fast path, the code obtains a `QBuffer` buffer, performs object virtual calls, then directly calls `QIODevice::write(QByteArray const&)@plt` at exact callsite `0x7dd563`.
10. Exact-build global direct calls to `QIODevice::write(QByteArray const&)@plt (0x4de370)` remain exactly five in the scanner used by this workflow: `0x7dd563`, `0xb4066b`, `0xb46c75`, `0xc4a848`, `0xd08642`.

## DERIVED

- `0x7dd630` is the correct structural consumer root for the `clientMessageReadyToProcess` Qt connection recovered at `0x19716a3`.
- `owner+0xc18`, `owner+0xa00`, `owner+0xa10`, and the `owner+0x9f0` object family are now higher-value provenance targets than the disproven containing-owner `+0x90` theory.
- The `0x7dd3f0` cluster is transport/framing-adjacent because it reaches a real `QIODevice::write` and shares owner fields with the proven queue consumer.
- The code around `0x7dd3f0` appears to support at least two dispatch paths: a concrete fast path recognized by vtable slot `+0xe8 == 0xb40630`, and a fallback indirect call through the observed `+0xe8` target. The semantic class names remain unknown.

## DISPROVEN / SUPERSEDED

- `clientMessageReadyToProcess -> containing owner virtual +0x90 -> 0x8409d0 -> 0xb5b880` is superseded and must not be used as the outbound serialization model.
- `0xb5b880` is not a validated function entry for this path and was previously introduced by workflow hardcoding rather than recovered from ELF state.

## UNKNOWN

- Concrete class/vtable identities for objects at `owner+0xc18`, `owner+0xa00`, `owner+0xa10`, and `owner+0x9f0`.
- Which of the five direct `QIODevice::write` callsites is the final Tibia gameplay socket write versus internal buffers/other subsystems.
- Exact framing, encryption/compression ordering, and final `QTcpSocket`/socket object for gameplay traffic.
- Whether `0x7dd3f0` is invoked directly as part of the same outbound message lifecycle for every gameplay message or only selected states/types.

## NEXT ACTION

Recover the derived-owner constructor/setup provenance for offsets `+0x9f0`, `+0xa00`, `+0xa10`, and `+0xc18`, including the concrete vtable/address-point of the object whose `+0xe8` slot equals `0xb40630`. Then intersect that provenance with the five exact `QIODevice::write` callsites and the existing QTcpSocket-bearing setup path before making any serializer/final-send claim.
