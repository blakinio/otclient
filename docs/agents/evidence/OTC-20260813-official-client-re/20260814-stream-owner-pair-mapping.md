# Track A — stream owner pair mapping

Date: 2026-08-14
Track: A / official native Linux Tibia client RE
Branch: `ci/OTC-20260814-track-a-chatgpt-framing-recovery`
Exact client SHA256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
Workflow run: `31824297168`
Job: `94844644409`
Result: `SUCCESS`
Runner: `synology-otclient-01`
Artifact: `track-a-stream-owner-pairs-31824297168`, id `9228207514`, zip SHA256 `b74d5d011d374a2ab735f8a75df54cbd774d7ee7d3903ab3430ea37072ca5b5d`

## FACT — owner shared-pointer pairs

The exact setup function around `0x1970600..0x1971800` provides direct class-aware construction and store provenance for the previously unknown owner fields.

### `owner+0xc18/+0xc20` = `tibia::network::TGameserverDualConnection`

- counted-ptr-inplace vtable at `0x304c460` has RTTI name `std::_Sp_counted_ptr_inplace<tibia::network::TGameserverDualConnection,...>`;
- allocation starts at `0x1970775` (`0xe8` bytes);
- in-place object pointer is control-block `+0x10`, saved in `r15`;
- object constructor call: `0x19707a2 -> 0xb55430`;
- exact owner stores:
  - `0x19707b5`: `[owner+0xc18] = object`;
  - `0x19707bc`: `[owner+0xc20] = control block`.
- constructor `0xb55430` calls `QObject::QObject`, installs object vptr `0x30b7b68` at `0xb55457..0xb5545e`, and initializes connection/state members.

Classification: **PROVEN**.

### `owner+0x9f0/+0x9f8` = `tibia::protocol::TProtocolServerPacketProcessor`

- counted-ptr-inplace vtable `0x304c3b8` has RTTI name `std::_Sp_counted_ptr_inplace<tibia::protocol::TProtocolServerPacketProcessor,...>`;
- allocation begins at `0x1970be6` (`0x38` bytes);
- object begins at control-block `+0x10` (`rcx` at `0x1970c02`);
- exact owner stores:
  - `0x1970c71`: `[owner+0x9f0] = object`;
  - `0x1970c78`: `[owner+0x9f8] = control block`.
- the object's first two qwords are populated from an already constructed stream shared pointer (`block+0x10` / `block+0x18`), and its later member copies the `owner+0x9e0` server-message-processor pair.

Classification: **PROVEN**.

### `owner+0xa00/+0xa08` = `tibia::protocol::TProtocolClientMessageProcessor`

- counted-ptr-inplace vtable `0x304c2a0` has RTTI name `std::_Sp_counted_ptr_inplace<tibia::protocol::TProtocolClientMessageProcessor,...>`;
- allocation begins at `0x1971033` (`0x38` bytes);
- object begins at control-block `+0x10` (`rdx` at `0x197104f`);
- object vptr `0x2f6a208` is written at `0x1971056..0x197105d`; RTTI name for that address point is `tibia::protocol::TProtocolClientMessageProcessor`;
- exact owner stores:
  - `0x19710a7`: `[owner+0xa00] = object`;
  - `0x19710ae`: `[owner+0xa08] = control block`.

Classification: **PROVEN**.

### `owner+0xa10/+0xa18` = `tibia::network::TGameserverNetworkPacketRawDataProcessor`

- counted-ptr-inplace vtable `0x304c230` has RTTI name `std::_Sp_counted_ptr_inplace<tibia::network::TGameserverNetworkPacketRawDataProcessor,...>`;
- allocation begins at `0x1971217` (`0x38` bytes);
- object vptr `0x2f6a230` is written at `0x1971221..0x1971237`; RTTI name is `tibia::network::TGameserverNetworkPacketRawDataProcessor`;
- exact owner stores:
  - `0x197128d`: `[owner+0xa10] = object`;
  - `0x1971294`: `[owner+0xa18] = control block`.

Classification: **PROVEN**.

## FACT — additional transport construction

The same setup reconstructs both protocol directions.

### Read/server side

The ordered construction visible before `owner+0x9f0` includes:

1. `TGameserverDualConnection`;
2. first `TUnencryptedRawMessageStream` (`QBuffer`-derived), constructed at `0x19707f8..0x1970810`;
3. `shared::TCompressionHelper` / `TZlibInflateWrapper`;
4. `tibia::shared::TIODeviceReader`;
5. `tibia::protocol::TProtocolReader`;
6. `TProtobufServerMessageTranslator`;
7. `TProtocolServerMessageProcessor`;
8. `TProtocolServerPacketProcessor` -> stored at `owner+0x9f0`.

The `TProtocolServerPacketProcessor` object begins with the shared pointer to the first raw stream. Therefore `0x7dd3f0` loading `owner+0x9f0` and then dereferencing the first object qword reaches this **server/read-side raw stream**.

### Write/client side

After `owner+0x9f0`, setup constructs:

1. second `TUnencryptedRawMessageStream` at `0x1970cad..0x1970cc6`;
2. `tibia::shared::TIODeviceWriter`;
3. `tibia::protocol::TProtocolWriter`;
4. `shared::TRsaHelper` and Crypto++ RSA/random state;
5. `TProtobufObjectPositionHelper`;
6. `TProtobufClientMessageTranslator`;
7. `TProtocolClientMessageProcessor` -> stored at `owner+0xa00`;
8. `TGameserverNetworkPacketSequenceFlowProcessor` -> stored separately at `owner+0xc28/+0xc30`;
9. `TGameserverNetworkPacketRawDataProcessor` -> stored at `owner+0xa10`.

This establishes two distinct `TUnencryptedRawMessageStream` instances in the setup: the first feeds the read/server path, while the second is constructed immediately before `TIODeviceWriter`/`TProtocolWriter` and belongs to the client/write-side construction family.

## CORRECTION / CONFLICT RESOLUTION

Previous evidence correctly said `0x7dd3f0` shares owner state with the queue consumer and reaches `QIODevice::write`, but it did **not** prove `0x7dd630 -> 0x7dd3f0` as a direct downstream edge.

The new owner/class mapping shows:

- `0x7dd3f0` accesses `owner+0x9f0 = TProtocolServerPacketProcessor`;
- that processor's first field is the first/server-side `TUnencryptedRawMessageStream`;
- consequently the `QIODevice::write` at `0x7dd563` is consistent with feeding bytes into the inbound raw-message buffer, not proof of the final outbound gameplay socket write.

Classification: the description of `0x7dd3f0` as **outbound downstream** is **NOT PROVEN and should be treated as superseded**. Its precise signal semantics still need call/connection classification, but the class topology strongly identifies it with the server/read-side processing family.

## Outbound root after correction

The proven queue consumer `0x7dd630` now has concrete field identities:

- `owner+0xc18` -> `TGameserverDualConnection`;
- `owner+0xa00` -> `TProtocolClientMessageProcessor`;
- `owner+0xa10` -> `TGameserverNetworkPacketRawDataProcessor`.

Its active invoke path calls virtuals on exactly these three objects. These vtable slots, rather than the server-side `owner+0x9f0` cluster, are the next authoritative outbound targets.

## Workflow note

The optional final `readelf` symbol grep in run `31824297168` did not execute because plain `readelf` was absent from PATH. This did not affect the Python RTTI mapping or GDB disassembly and the job remained successful. Future workflows should use a verified toolroot `readelf` path or omit this optional step.

## NEXT ACTION

Resolve relocation-aware vtables and concrete targets for:

- `TGameserverDualConnection` vptr `0x30b7b68`, especially slots `+0x78`, `+0x80`, `+0x90` used by `0x7dd630`;
- `TProtocolClientMessageProcessor` address point `0x2f6a208`, especially `+0x10`;
- `TGameserverNetworkPacketRawDataProcessor` address point `0x2f6a230`, especially `+0x10` and `+0x18`.

Disassemble those exact targets and reconstruct their argument/data flow until the second/write-side `TUnencryptedRawMessageStream`, packet framing/sequence layer and `TGameserverTCPConnection`/`QTcpSocket` are ordered structurally.
