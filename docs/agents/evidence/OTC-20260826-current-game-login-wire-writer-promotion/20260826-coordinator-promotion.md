# Coordinator promotion — current-build game-login wire writer

Date: 2026-08-26  
Source task: `OTC-20260826-current-game-login-wire-writer`  
Source Draft: PR #699  
Promotion PR: #706  
Decision: **ACCEPT_WITH_EDITS**

## Trust boundary

The coordinator did not treat the researcher summary as proof. The final source artifact was independently re-downloaded from GitHub Actions and re-hashed before review:

```text
source research head  3d87d729b73f868aefe1662c72af666a4921b1d8
source freeze head    7de745105ce06271ff45bcdf5e5eaf91268008e5
producer run          32998976901 = SUCCESS
artifact              9617908322
GitHub digest          sha256:a43ed724d00e18575d969859ad3345d69f2650ee5790d3dbcf13767de1b9ebf4
re-downloaded ZIP      sha256:a43ed724d00e18575d969859ad3345d69f2650ee5790d3dbcf13767de1b9ebf4
result.json            sha256:022a58f738b6586e9143f9e558cb19e89e4fdeb83cd4624a5c7a5cb9dbceddd7
```

The exact current package fence inside the artifact is independently consistent with the public package producer:

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

Safety markers also pass: `runtime_access:none`, no official-client execution/login, no secret access and no raw-client upload.

## Accepted current queue boundary

The exact current QMeta login method is method index `196`, case `0xde82a2`, with one terminal jump to adapter `0xbd3050`. The adapter loads receiver vslot `+0x68` and calls it with the copied login message.

Current `TProtocolMessageQueue` RTTI/vtable recovery is unique:

```text
RTTI       0x30ed548
vtable AP  0x30ed588
slot +0x68 -> 0xbd24a0
FDE        0xbd24a0..0xbd28c4
```

The coordinator accepts this as the current enqueue/queue boundary. It does **not** promote a synchronous direct edge from `0xbd24a0` to the later protocol processor; the asynchronous drain remains `UNKNOWN`.

## Accepted current outbound transform

Current RTTI/vtable targets are independently recovered for the exact binary, including:

```text
TProtocolClientMessageProcessor          +0x10 -> 0xc29350
TGameserverNetworkPacketRawDataProcessor +0x10 -> 0xb36c70
TGameserverDualConnection                +0x78 -> 0xb43920
TGameserverDualConnection                +0x80 -> 0xb43d10
TGameserverNetworkPacketProcessor        +0x68 -> 0xf4eca0
```

At RawDataProcessor `+0x10`, the artifact proves padding to an 8-byte boundary, storage of the padding-count byte and a mode-2 virtual transform. Current RTTI identifies that transform receiver as `shared::TXteaHelper`, vtable AP `0x2f82ea0`, slot `+0x28 -> 0xf71eb0`. `ENCRYPTION=XTEA` on this current mode-2 outbound path is accepted.

No separate compression transform appears inside the recovered canonical outbound transform window. This remains bounded negative evidence only; it is not generalized to unrelated/inbound paths.

## Accepted current sequence and framing

`TGameserverDualConnection +0x80` proves the current sequence field. For message mode `+0x34 == 3`, it writes `[this+0x9c]` to `message+0`, increments the owner and stores it back; the nonmatching branch writes zero.

A structural intersection of the current `TIODeviceWriter +0x58` references and direct `QDataStream::writeRawData` calls yields exactly one final frame serializer:

```text
FDE 0xf4edd0..0xf4ef15
```

Its outbound write order is:

```text
ceil(payload_length / 8)
-> dword(message+0)
-> raw transformed payload via QDataStream::writeRawData
```

Current PLT resolution gives:

```text
QDataStream::QDataStream(QIODevice*)  0x4d46d0
QDataStream::writeRawData(...)        0x4d6260
QTcpSocket::QTcpSocket(QObject*)      0x4d6bc0
```

The current setup graph constructs QTcpSocket objects and the current `TIODeviceWriter` constructor retains the supplied QIODevice pair, constructs its QDataStream and retains that stream at writer `+0x18/+0x20`. The coordinator accepts the Qt/QTcpSocket-bound binary writer boundary. The optional kernel syscall remains `UNKNOWN`.

## Track B comparison

The coordinator separately inspected current Track B code on `feat/OTC-20260813-tibia-global-login-lab`.

For client `>= 1405`, generic `Protocol::send()` already performs:

```text
padding-count byte + 8-byte padding
-> XTEA when enabled
-> 32-bit sequence when enabled
-> header block count
-> connection write
```

`OutputMessage::writeHeaderSize()` writes `(messageSize - 4) / 8`, matching the native block-count scalar after excluding the sequence dword. This outer transport shape is therefore structurally aligned with the current official client.

**Rejected next hypothesis:** changing generic outer padding/XTEA/sequence/framing after the structured `0x14`. Current evidence does not support it.

The remaining login-specific discrepancy is before that generic layer: Track B still constructs its legacy raw login/RSA preamble in `ProtocolGame::sendLoginPacket()`, while the official client enters the current typed queue path through `TProtocolMessageQueue::sendLogin`. This source task did not revalidate the exact current generated login-message field schema, so the coordinator does not promote or invent those fields.

## Accepted / withheld classifications

```yaml
accepted:
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
  track_b_outer_transport_shape: STRUCTURALLY_ALIGNED
  track_b_next_guess_should_change_outer_framing: REJECTED
withheld:
  queue_async_drain_to_client_processor: UNKNOWN
  current_generated_login_message_field_schema: UNKNOWN
  final_frame_receiver_concrete_rtti_name: UNKNOWN
  final_os_socket_syscall: UNKNOWN_OPTIONAL
  causal_explanation_of_track_b_0x14: UNKNOWN
```

## Source PR audit and disposition

Source PR #699 changed exactly six declared research/evidence files: one task-owned hosted workflow, two analyzer/test files and three task/evidence files. No proprietary binary, Track B file or credential material is present. Review/comment inventory is empty.

The source analyzer/workflow is intentionally **not promoted**. Only this independently reviewed docs/evidence result moves to trusted `main`.

Audit result:

```yaml
audit:
  result: PASS_BOUNDED
  decision: ACCEPT_WITH_EDITS
  independent_validator_role: coordinator
  primary_artifact_rehashed: true
  source_diff_reviewed: true
  material_findings_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: static docs/evidence promotion; no runtime behavior changes
```

After this promotion reaches trusted `main`, Track B #284 may consume these accepted facts. Its next bounded discriminator must target the **current login-specific payload representation/schema**, not resend the same packet or guess outer framing toggles.
