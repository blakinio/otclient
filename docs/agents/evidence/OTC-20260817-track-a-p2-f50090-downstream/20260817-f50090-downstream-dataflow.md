# Track A P2 — `0xf50090` downstream dataflow

Date: 2026-08-17  
Task: `OTC-20260817-track-a-p2-f50090-downstream`  
Research status: **DRAFT / NOT PROMOTED — READY FOR COORDINATOR REVIEW AFTER FINAL CI**

## Exact-client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

No live client process, process memory, login/gameplay, canonical runtime state or world-map evidence was used. Synology source stages only verified the retained regular exact file and copied bounded file-backed bytes. All disassembly and semantic classification ran on GitHub-hosted Ubuntu. No raw executable/package was uploaded.

## Canonical input

Coordinator promotion #487 proves the same post-`TGameserverNetworkPacketRawDataProcessor` message reaches exact target `0xf50090`:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same QByteArray/message
 -> TGameserverDualConnection+0x78@0xb56970
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8 +0x10
 -> 0xf50090
```

## Evidence generations

The first checkout-dependent producer never reached client/source access because GitHub `codeload` returned HTTP 429 while downloading pinned `actions/checkout`. One identical retry reproduced the same external failure. The replacement producer removed marketplace actions rather than retrying indefinitely.

### Generation 2 — `0xf50090` function

```text
producer head    ea8113028a07ef84518f4a8b705bcecd97604376
run              32037248323 = SUCCESS
source job       95410048084 = SUCCESS
hosted job       95410072413 = SUCCESS
main window      0xf50040..0xf50480
main sha256      1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
source candidate 1
```

### Generation 3 — writer constructor/wrappers

```text
producer head    8642b419ca8ef3034ba747f689a14e24cf9a0152
run              32037533068 = SUCCESS
source job       95410828633 = SUCCESS
hosted job       95410901806 = SUCCESS
main window      0xf50040..0xf50480
main sha256      1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea
ctor window      0x1960300..0x1960600
ctor sha256      bc03c482e3ae04c0f9a91288d5f79612b2f0f08680ef10ffecdf9a927ec0371f
vcall window     0xcb2900..0xcb29c0
vcall sha256     dc04038b7740f39095ed6ab599bc10048c368fab9eff126c3d0853930c62af14
source candidate 1
```

Both successful source stages revalidated exact file size/SHA, ELF64 little-endian structure and file-backed executable ranges. Source-side disassembly/semantic classification, process/runtime access, client execution/mutation and raw-client upload were absent.

## Independent accepted predecessor cross-check

Accepted exact-SHA PR #308 artifact `9251725866` / digest
`sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e`
was independently re-read. It proves:

```text
helper 0x1960340
 -> TIODeviceWriter vtable AP 0x2f69d48 / RTTI 0x3080718
 -> supplied QIODevice shared pair retained at +0x08/+0x10
 -> QDataStream(QIODevice*) constructed
 -> QDataStream object/control retained at +0x18/+0x20
 -> QDataStream::setByteOrder(...)
```

The same artifact identifies exact PLT target:

```text
0x4dd250 = QDataStream::writeRawData(char const*, qint64)
```

It also proves the general representation boundary `STRUCTURED_FIELDS -> QDataStream -> QIODevice byte container`, while explicitly keeping protocol framing, sequence, compression, encryption and final egress UNKNOWN.

## `0xf50090`: canonical argument and field decomposition

Exact entry:

```text
f50090: push r12
f50092: push rbp
f50093: mov  rbp,rsi
f50096: push rbx
f50097: mov  rbx,rdi
```

Thus the canonical same message is the original SysV second argument and is retained in `rbp`.

The function snapshots message fields:

```text
f5009e: movdqu xmm0,[rsi+0x8]
f500a3: mov    rax,[rsi+0x18]
f500ab: mov    [rsp+0x10],rax
f500b0: movaps [rsp],xmm0
```

so the direct snapshot is:

```text
message+0x08 -> stack+0x00
message+0x10 -> stack+0x08
message+0x18 -> stack+0x10
```

The whole original message pointer is not passed to any downstream call in this bounded function. `f50090_forwards_original_message_pointer_as_whole = DISPROVEN`.

## Exact writer identity

`0xf50090` obtains its writer from `this+0x08`. Exact constructor provenance from the predecessor object-construction window binds that member to an object initialized by helper `0x1960340`.

Generation 3 independently re-decodes the helper:

```text
1960342: lea rax,0x2f69d48
1960354: mov [rdi],rax
1960357: mov r13,[rsi]
196035a: mov rax,[rsi+0x08]
196035e: mov [rdi+0x08],r13
1960362: mov [rdi+0x10],rax
...
19603b8: call 0x4db6d0
19603c1: mov [rbx+0x18],r12
19603c5: mov [rbx+0x20],rbp
...
196040d: call 0x4dd070
```

Together with accepted #308 exact type/symbol evidence:

```yaml
f50090_writer_member: FACT:this+0x08
f50090_writer_type: FACT:TIODeviceWriter
f50090_writer_vtable_ap: FACT:0x2f69d48
f50090_writer_rtti: FACT:0x3080718
f50090_writer_qiodevice_pair: FACT:writer+0x08/+0x10
f50090_writer_qdatastream_pair: FACT:writer+0x18/+0x20
f50090_writer_qdatastream_object: FACT:writer+0x18
```

The exact concrete dynamic type of the **QIODevice bound to this particular TIODeviceWriter instance** remains UNKNOWN.

## Scalar serialization paths

`0xf50090` dispatches two scalar fields through TIODeviceWriter slots:

```text
f500ce: guard target 0xcb2930
f500e0: load writer vslot +0x30
...
f500f7: call 0x4dc3d0

f50100: guard target 0xcb2940
f50107: mov esi,[rbp+0x00]
f5010d: load writer vslot +0x38
...
f50121: call 0x4daaf0
```

Generation 3 independently confirms wrappers:

```text
cb2930: mov rdi,[rdi+0x18]
cb2934: movsx esi,si
cb2937: jmp 0x4dc3d0

cb2940: mov rdi,[rdi+0x18]
cb2944: jmp 0x4daaf0
```

Therefore both paths are structurally QDataStream scalar serialization operations because `writer+0x18` is the exact QDataStream object. Their exact overload names are not promoted here because this task did not independently resolve the two PLT symbols.

## Raw payload serialization path — exact semantic identity

The strongest payload edge in `0xf50090` is:

```text
f5012a: lea rdx,0xcb2960
f50134: mov rax,[writer.vtable+0x58]
f50138: cmp rax,rdx
...
f5013d: mov rsi,[rsp+0x08]   # value copied from canonical message+0x10
f50142: mov rdi,[rdi+0x18]    # writer QDataStream object
f50146: mov rdx,[rsp+0x10]    # value copied from canonical message+0x18
f50153: call 0x4dd250
```

Generation 3 independently confirms wrapper `0xcb2960`:

```text
cb2960: mov rdx,[rsi+0x10]
cb2964: mov rsi,[rsi+0x08]
cb2968: mov rdi,[rdi+0x18]
cb296c: test rsi,rsi
cb296f: je 0xcb2980
cb2971: jmp 0x4dd250
...
cb2980: mov rsi,[0x312fe68]
cb2987: jmp 0x4dd250
```

Accepted #308 exact PLT identity resolves the target:

```text
0x4dd250 = QDataStream::writeRawData(char const*, qint64)
```

Promoted-candidate bounded classifications:

```yaml
f50090_writer_slot_0x58_target: FACT:0xcb2960
f50090_raw_payload_pointer: FACT:value copied from canonical message+0x10
f50090_raw_payload_length: FACT:value copied from canonical message+0x18
f50090_raw_payload_receiver: FACT:TIODeviceWriter+0x18_QDataStream
f50090_raw_payload_target: FACT:QDataStream::writeRawData@0x4dd250
f50090_representation_boundary: FACT:STRUCTURED_MESSAGE_FIELDS_TO_TIODEVICEWRITER_QDATASTREAM
```

## Direct socket/final-egress disposition

The bounded function contains no direct QTcpSocket/socket-write sink. Its concrete downstream operations are TIODeviceWriter/QDataStream serialization, including exact `QDataStream::writeRawData`.

```yaml
f50090_direct_socket_sink: DISPROVEN
f50090_is_proven_final_binary_egress: DISPROVEN
current_tiodevice_concrete_type: UNKNOWN
final_binary_egress: UNKNOWN
final_socket_ownership: UNKNOWN
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
```

`f50090_is_proven_final_binary_egress: DISPROVEN` means only that this function is now positively typed as a serialization stage rather than a proven terminal socket sink. It does not exclude downstream effects inside the bound QIODevice.

## Current exact stage order

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same QByteArray/message
 -> TGameserverDualConnection+0x78@0xb56970
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8 +0x10
 -> 0xf50090
 -> message field decomposition
 -> TIODeviceWriter AP 0x2f69d48
 -> QDataStream scalar writes + QDataStream::writeRawData@0x4dd250
 -> bound QIODevice concrete type UNKNOWN
```

## Next smallest falsifiable frontier

Resolve the exact provenance/concrete dynamic type of the QIODevice shared pair supplied to the current `TIODeviceWriter` at constructor call `b4b273 -> 0x1960340`. Existing constructor dataflow narrows the pair to members copied from the `TGameserverNetworkPacketConnection` construction graph; the next task should determine whether this exact instance is QBuffer-backed or another QIODevice and then follow its first post-serialization consumer. Do not broaden into a generic Qt/socket census.

E2E: `NOT_APPLICABLE` — exact static file/disassembly evidence only.
