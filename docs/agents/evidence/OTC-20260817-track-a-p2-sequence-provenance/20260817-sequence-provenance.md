# Track A P2 — outbound sequence provenance

Status: `DRAFT_NOT_PROMOTED / READY_FOR_COORDINATOR_REVIEW`  
Task: `OTC-20260817-track-a-p2-sequence-provenance`  
Base: `main@0aed48da9a51730c590d0ffe4688f149b359a170`  
Exact client: `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

Execution used one exact-fenced file-only source slice and GitHub-hosted semantic decode. `runtime_access:none`; no live runtime, process memory, login/gameplay, world-map, raw executable upload or owner-funded AI/API.

## Canonical input

PR #494 canonically proves framing and the ordered outbound field at `f50107`:

```text
scalar A framing field
 -> DWORD(message+0), semantics previously UNKNOWN
 -> raw payload
 -> TIODeviceWriter/QDataStream
 -> TGameserverTCPConnection-owned QTcpSocket
```

Accepted earlier exact bytes also prove:

- `TProtocolClientMessageProcessor` initializes the message low DWORD at `message+0` to zero as part of qword `0x0000000100000000`;
- `TGameserverNetworkPacketRawDataProcessor` transforms the QByteArray beginning at `message+0x8` and does not provide the sequence producer edge;
- the same message then reaches `TGameserverDualConnection +0x80@0xb56d60` before `+0x78@0xb56970`.

## New exact evidence

Workflow run `32044825898 = SUCCESS`:

```text
source job 95430326316 = SUCCESS
hosted job 95430351866 = SUCCESS
window 0xb56d60..0xb57280
window sha256 e5cf009bb1aec3065da4ff0dd3231268af1255cffa50fbb48f8817777907d557
```

The source job only exact-fenced the retained client and copied the bounded executable window. The hosted job independently reconstructed, hashed and disassembled it.

## FACT — same message retained by `DualConnection +0x80`

At entry:

```text
b56d62  mov r15,rdi              # TGameserverDualConnection this
b56d71  cmp DWORD PTR [rsi+0x28],0x1
b56d75  mov [rsp+0x10],rsi       # save exact message pointer
```

Before the terminal field update the exact saved message is restored:

```text
b56f46  mov rsi,[rsp+0x10]
b56f4b  cmp DWORD PTR [rsi+0x34],0x3
```

Thus the writes below target the same message later passed to `DualConnection +0x78` and serialized at `0xf50090`.

## FACT — non-sequenced branch explicitly writes zero

When `message+0x34 != 3`:

```text
b56f55  mov rax,[rsp+0x10]
b56f5a  mov DWORD PTR [rax],0x0
```

So `DWORD(message+0)` is explicitly zeroed on this branch.

## FACT — sequenced branch consumes and increments per-DualConnection counter

When `message+0x34 == 3`:

```text
b57058  mov eax,DWORD PTR [r15+0x9c]
b5705f  mov DWORD PTR [rsi],eax
b57061  add eax,0x1
b57064  mov DWORD PTR [r15+0x9c],eax
```

Because `r15` is the exact `TGameserverDualConnection this` saved at entry, `this+0x9c` is connection-object-local state. Each qualifying outbound message receives the current 32-bit counter value in `message+0`, then the object-local counter is incremented by one for the next qualifying message. Arithmetic is 32-bit and therefore wraps modulo `2^32` if exhausted; no stronger lifetime/reset claim is needed for this classification.

Canonical framing already proves this exact `DWORD(message+0)` is serialized before the raw payload. The combination is direct sequence-numbering dataflow, not an inference from width, position, class naming or packet adjacency.

Researcher classification:

```text
SEQUENCE=PROVEN
```

More precisely:

```yaml
sequence_field: FACT:DWORD(message+0)
sequence_owner: FACT:TGameserverDualConnection_this_plus_0x9c
sequence_mode: FACT:message_plus_0x34_equals_3
sequence_update: FACT:store_current_then_increment_by_one
sequence_nonmatching_mode: FACT:message_plus_0_set_to_zero
sequence_width: FACT:32_bit
sequence_wrap_behavior: FACT:modulo_2_pow_32_from_instruction_width
sequence_initial_value_or_reset_policy: UNKNOWN
```

The unknown initialization/reset policy does not weaken the proven per-object post-increment sequence mechanism on the outbound frames that enable it.

## Preserved boundaries

```text
FRAMING=PROVEN
SEQUENCE=PROVEN
COMPRESSION=UNKNOWN
ENCRYPTION=UNKNOWN
FINAL_BINARY_EGRESS=PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
FINAL_SOCKET_OWNER=TGameserverTCPConnection
FINAL_OS_SOCKET_SYSCALL=UNKNOWN
```

No compression or encryption meaning is assigned to `RawDataProcessor` padding, the helper at `0x1832b90`, or the conditional member transform from this task.

## Next frontier

The smallest remaining transport-semantic discriminator is the `RawDataProcessor this+0x8/+0x10` member object:

- vslot `+0x20` fast target `0xf85eb0` supplies padding bytes;
- vslot `+0x28` fast target `0xb3ec30` is invoked only when `message+0x28 == 2`.

Resolve the exact dynamic type/provenance of that member object and the concrete input/output effect of `0xb3ec30`. Use that to prove or disprove encryption first; compression remains independent unless direct bytes establish it.

Promotion authority: coordinator only.
