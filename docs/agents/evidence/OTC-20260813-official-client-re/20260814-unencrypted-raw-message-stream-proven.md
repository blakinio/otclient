# Track A — `TUnencryptedRawMessageStream` transport vtable proven

Date: 2026-08-14
Track: A / official native Linux Tibia client RE
Branch: `ci/OTC-20260814-track-a-chatgpt-framing-recovery`
Exact client SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
Workflow run: `31824001391`
Job: `94843696871`
Result: `SUCCESS`
Runner: `synology-otclient-01`
Artifact: `track-a-transport-vtable-rtti-31824001391`, id `9228087310`, zip SHA256 `a8755bf378f494ec8f895d563d12f61cf43bf59f12fa5fb6b6dc3d6ad68705e1`

## FACT

1. A relocation-aware strict exact-build rescan for a vtable address point whose `+0xe8` entry resolves to local method `0xb40630`, requiring mapped non-executable RTTI, returns exactly one candidate:

   `0x3084c58`, `offset_to_top=0`, RTTI `0x3080660`.

   Output: `STRICT_VTABLE_E8_CANDIDATE_COUNT=1`.
2. RTTI `0x3080660` is non-executable (`segment flags 0x6`) and is `__si_class_type_info`.
3. RTTI name at `0x1cac0e0` is exactly:

   `N5tibia7network28TUnencryptedRawMessageStreamE`

   i.e. `tibia::network::TUnencryptedRawMessageStream`.
4. The single-inheritance RTTI base pointer at `0x3080670` relocates to `_ZTI7QBuffer`. Therefore `TUnencryptedRawMessageStream` structurally derives from Qt `QBuffer` on this exact build.
5. Relocation-resolved inherited vtable entries at address point `0x3084c58` include Qt methods from `QBuffer`, `QIODevice`, and `QObject`, including:
   - `QBuffer::metaObject`, `qt_metacast`, `qt_metacall`;
   - `QObject::event/eventFilter/timerEvent/childEvent/customEvent`;
   - `QBuffer::connectNotify/disconnectNotify`;
   - `QIODevice::isSequential/reset/bytesAvailable/bytesToWrite/waitForReadyRead/waitForBytesWritten/readLineData/skipData`;
   - `QBuffer::open/close/pos/size/seek/atEnd/canReadLine/readData/writeData`.
6. Local destructor slots are:
   - `+0x18 = 0x7dcbd0` — resets vptr to `0x3084c58`, then tail-jumps to `QBuffer::~QBuffer`;
   - `+0x20 = 0x7dcbe0` — resets vptr, calls `QBuffer::~QBuffer`, then deletes the object.
7. Local class-specific entries immediately following the inherited QBuffer virtual surface are:
   - `+0xe8 = 0xb40630`;
   - `+0xf0 = 0xb40690`;
   - `+0xf8 = 0xb40710`.
8. `0xb40630` calls `QBuffer::buffer()`, performs class virtual bookkeeping, and directly invokes `QIODevice::write(QByteArray const&)` at `0xb4066b`.
9. `0xb40690` manipulates/removes bytes from the `QBuffer` backing QByteArray and performs the same class virtual bookkeeping family.
10. `0xb40710` is a thin wrapper over `QIODevice::readAll()`.
11. `TUnencryptedRawMessageStream` instances are explicitly constructed in the large network setup path. At `0x19707f8` and `0x1970cad`, code calls `QBuffer::QBuffer(QObject*)` on an in-place object at allocation/control-block `+0x10`, then writes vptr `0x3084c58` to that object and opens it with mode value `3`.
12. The same setup region contains concrete owner-field stores:
   - `owner+0xc18` / `owner+0xc20` are assigned as an object-pointer/control-block pair at `0x19707b5..0x19707bc` for an object constructed just before the first `TUnencryptedRawMessageStream` instance;
   - `owner+0x9f0` / `owner+0x9f8` are assigned as another pointer/control-block pair at `0x1970c6a..0x1970c78`, immediately before the second `TUnencryptedRawMessageStream` construction.
   These two stores are proven, but the class identity of the objects being stored at those exact pair assignments requires the surrounding allocation chain to be followed further before equating either field directly with `TUnencryptedRawMessageStream`.

## DISPROVEN

- The raw candidate `0x280e00` from the earlier broad scan is not retained by the strict non-executable-RTTI predicate. The strict candidate count is exactly one, so it must not be treated as a peer vtable candidate.

## DERIVED

- `TUnencryptedRawMessageStream` is a concrete buffering/stream layer in the recovered outbound transport family, not merely an unrelated QIODevice, because its unique local `+0xe8` method is the exact target devirtualized by the `0x7dd3f0` transport cluster and that cluster shares owner state with the proven `clientMessageReadyToProcess` consumer `0x7dd630`.
- The presence of `UnencryptedRawMessageStream` establishes a named layer of the transport stack, but does **not** prove that bytes passed to this layer are final unencrypted Tibia wire bytes; higher/lower framing, encryption, compression, and socket layers still need structural ordering proof.

## UNKNOWN

- Exact mapping of each owner pair `+0x9f0/+0x9f8`, `+0xa00/+0xa08`, `+0xa10/+0xa18`, `+0xc18/+0xc20` to concrete stream/wrapper classes.
- Class of the object assigned at `owner+0xc18` just before the first raw-stream construction.
- Class of the object assigned at `owner+0x9f0` just before the second raw-stream construction.
- Exact relation/order among raw stream, protocol framing, any encryption/compression layer, and the final `QTcpSocket`.
- Final gameplay socket write site.

## NEXT ACTION

Disassemble/reconstruct the complete setup slices around `0x19706f0..0x1970f80` and the constructor used at `0xb55430`. Map each consecutive allocation/control-block/in-place object to the owner shared-pointer pairs `+0x9f0/+0x9f8`, `+0xa00/+0xa08`, `+0xa10/+0xa18`, `+0xc18/+0xc20`; resolve each vptr RTTI/base class; then order those objects against `TUnencryptedRawMessageStream` and the known QTcpSocket-bearing setup path.
