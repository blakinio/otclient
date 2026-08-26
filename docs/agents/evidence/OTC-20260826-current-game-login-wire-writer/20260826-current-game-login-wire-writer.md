# Current-build game-login wire-writer evidence

Date: 2026-08-26  
Task: `OTC-20260826-current-game-login-wire-writer`  
Source PR: `#699`  
Execution: exact-current GitHub-hosted static analysis only, `runtime_access: none`.

## Exact client fence

The final successful producer independently resolved and verified the current official native-Linux client:

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

Final proving generation:

```text
head      3d87d729b73f868aefe1662c72af666a4921b1d8
run       32998976901 = SUCCESS
artifact  9617908322
digest    sha256:a43ed724d00e18575d969859ad3345d69f2650ee5790d3dbcf13767de1b9ebf4
```

The producer used a disposable GitHub-hosted Ubuntu runner, fetched the public package through WARP, verified the package hashes before analysis, deleted proprietary client bytes before job completion, and uploaded only sanitized structural JSON. It did not execute the official client or access credentials, session state, process memory or gameplay.

## FACT — current `TProtocolMessageQueue::sendLogin` boundary

The current QMeta object is recovered independently:

```text
class            tibia::protocol::TProtocolMessageQueue
stringdata       0x1ce67c0
metadata         0x1ce35a0
qmetaobject      0x30b73e0
static_metacall  0xde76a0
jump_table       0x1da9304
method_count     355
signal_count     192
```

QMeta method index `196` is `sendLogin`, with case target `0xde82a2`. The case thunk has one terminal direct edge:

```text
0xde82ae -> 0xbd3050
```

The adapter is exact FDE `0xbd3050..0xbd34dd`. Inside it:

```text
bd31b4  mov rax,[r12]
bd31b8  mov rax,[rax+0x68]
...
bd31de  mov rsi,rsp
bd31e1  mov rdi,r12
bd31e4  call rax
```

Current RTTI/vtable reconstruction for `TProtocolMessageQueue` gives:

```text
RTTI       0x30ed548
vtable AP  0x30ed588
slot +0x68 -> 0xbd24a0
FDE        0xbd24a0..0xbd28c4
```

Therefore the current login queue chain through the exact queue virtual slot is proven. `0xbd24a0` performs queue/storage/synchronization work; this task does not invent a synchronous direct call from that enqueue boundary to the later client processor.

## FACT — current outbound P2 targets

Independent current-build RTTI/vtable recovery gives:

```text
TProtocolClientMessageProcessor          +0x10 -> 0xc29350
TGameserverNetworkPacketRawDataProcessor +0x10 -> 0xb36c70
TGameserverDualConnection                +0x78 -> 0xb43920
TGameserverDualConnection                +0x80 -> 0xb43d10
TGameserverNetworkPacketConnection       +0x78 -> 0xb53930
TGameserverNetworkPacketConnection       +0x80 -> 0xb68c70
TGameserverNetworkPacketProcessor        +0x60 -> 0xf39430
TGameserverNetworkPacketProcessor        +0x68 -> 0xf4eca0
```

These addresses were rediscovered from the `15.32.75d4a0` binary. Historical `df7b29` addresses were forbidden inputs to the locator and were not reused.

## FACT — padding and current XTEA transform

`TGameserverNetworkPacketRawDataProcessor +0x10 @ 0xb36c70` appends bytes until the working byte container is divisible by eight, then stores the padding amount in the first byte. The current path contains:

```text
b36d50  test sil,7
b36d54  jne  0xb36d38
...
b36dc5  mov byte ptr [rax],bl
```

The transform mode is then tested:

```text
b36dc7  cmp dword ptr [r12+0x28],2
...
b36df1  mov rax,[rsi]
b36df4  call qword ptr [rax+0x28]
```

Current RTTI identifies `shared::TXteaHelper` at RTTI `0x30adc00`, vtable AP `0x2f82ea0`, with slot `+0x28 -> 0xf71eb0`. Thus the mode-2 outbound transform is current-build XTEA, not an inferred historical address.

No separate compression transform was identified inside the recovered canonical outbound transform window. This is bounded negative evidence for this path, not a claim about unrelated/inbound code.

## FACT — sequence field

`TGameserverDualConnection +0x80 @ 0xb43d10` updates the first dword of the message. For message mode `+0x34 == 3`:

```text
b43efb  cmp dword ptr [rsi+0x34],3
b44008  mov eax,dword ptr [r15+0x9c]
b4400f  mov dword ptr [rsi],eax
b44011  add eax,1
b44014  mov dword ptr [r15+0x9c],eax
```

For the nonmatching branch it writes zero at `message+0` (`0xb43f0a`). The current outbound sequence field and incrementing owner are therefore proven.

## FACT — final frame serializer

A structural intersection of the current `TIODeviceWriter +0x58` target references and direct `QDataStream::writeRawData` calls yields one serializer FDE:

```text
0xf4edd0..0xf4ef15
```

Its ordered write path is:

```text
f4ee02  writer = [this+8]
f4ee06  lea rsi,[payload_length+0xe]
f4ee0a  add payload_length,7
f4ee15  cmovns rsi,rax
f4ee1c  sar rsi,3
f4ee37  write first scalar
f4ee47  esi = dword ptr [message+0]
f4ee61  write second scalar
f4ee7d  rsi = raw payload pointer
f4ee82  rdi = writer QDataStream at [writer+0x18]
f4ee86  rdx = raw payload length
f4ee93  call 0x4d6260
```

Current PLT resolution proves `0x4d6260 = QDataStream::writeRawData(char const*, qint64)`. The first scalar is the signed-safe `ceil(payload_length / 8)` value; the second is the message dword populated by the sequence stage; then the raw transformed payload is written.

A current vtable candidate at address point `0x2f95fd8` has slot `+0x10 -> 0xf4edd0`. Construction references for that address point are present in FDE `0xb5a0d0..0xb5a9bd`. Its concrete RTTI name is not promoted by this task and remains `UNKNOWN`.

## FACT — QIODevice/QDataStream/QTcpSocket construction graph

Current Qt PLT addresses are independently resolved:

```text
QTcpSocket::QTcpSocket(QObject*)       0x4d6bc0
QDataStream::QDataStream(QIODevice*)   0x4d46d0
QDataStream::writeRawData(...)         0x4d6260
```

The current main setup FDE `0x1956320..0x19591f9` contains the two QTcpSocket constructor calls `0x195636a` and `0x1956707` and installs `TGameserverTCPConnection` vtable AP `0x30b6438`.

The `TIODeviceWriter` constructor FDE is `0x1946510..0x1946652`. It retains the supplied shared QIODevice pair at writer `+0x08/+0x10`, constructs `QDataStream(QIODevice*)` from that object, and retains the QDataStream pair at writer `+0x18/+0x20`. The network construction graph calls this helper at `0xb5a4a3`, `0xb5a80b` and `0xb5a89a`; the final frame uses that writer's QDataStream.

This proves the current Qt-bound binary writer boundary. The optional kernel-level `send`/`write` syscall below Qt remains outside scope and `UNKNOWN`.

## Structural comparison with Track B

Track B's generic `Protocol::send()` already follows the same outer shape for `>= 1405`:

```text
padding byte + pad to 8
-> XTEA when enabled
-> 32-bit sequence when sequenced packets are enabled
-> header size derived from encrypted payload blocks
-> socket write
```

Its `OutputMessage::writeHeaderSize()` writes `(messageSize - 4) / 8`, matching the current native frame's block-count scalar once the sequence dword is excluded. Its sequence is also a 32-bit pre-payload field.

Therefore **the current evidence does not support changing the generic outer framing as the next hypothesis**.

The remaining material difference is before that generic layer: Track B `ProtocolGame::sendLoginPacket()` still constructs the legacy raw login preamble/RSA layout (`ClientPendingGame`, OS/protocol/version/assets/session fields) while the official-client research surface dispatches login through `TProtocolMessageQueue::sendLogin` and a separate native queue/serialization path. This task does not revalidate the exact current generated login-message field schema, so it does not authorize inventing or guessing those fields.

## Classification

```yaml
current_exact_client_fence: PROVEN
current_sendlogin_qmeta_case: PROVEN
current_sendlogin_adapter: PROVEN
current_queue_vslot_plus_0x68_target: PROVEN
current_padding: PROVEN
current_xtea_mode2_transform: PROVEN
current_sequence: PROVEN
current_framing: PROVEN
current_qdatastream_raw_write: PROVEN
current_qt_bound_binary_writer: PROVEN
final_os_socket_syscall: UNKNOWN_OPTIONAL
queue_async_drain_to_client_processor: UNKNOWN
current_generated_login_message_field_schema: UNKNOWN
track_b_outer_transport_shape: STRUCTURALLY_ALIGNED
track_b_next_guess_should_change_outer_framing: REJECTED
```

## First unproven boundary

The exact first unproven causal edge in a single synchronous login chain is the asynchronous drain from `TProtocolMessageQueue +0x68 @ 0xbd24a0` into the recovered client/raw/network processor chain. The current-build downstream wire contract itself is independently proven and is sufficient to falsify outer-framing guesses.

No game login, credential read, session capture, process observation or Track B mutation occurred in this task. Physical E2E is `NOT_APPLICABLE` because this is static exact-file protocol reconstruction.
