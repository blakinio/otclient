# Track A P2 outbound sequence — coordinator promotion

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-sequence-provenance`  
Source Draft: PR #495  
Source final head: `4a98632046936fba070653196d91e9f82e6b07e7`  
Integration base: `main@0aed48da9a51730c590d0ffe4688f149b359a170`  
Decision: **ACCEPT_WITH_EDITS**

Exact client: `15.32.df7b29` / `51965216` / `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

## Independent verification

The coordinator independently checked the exact hosted decode from run `32044825898`, source job `95430326316`, hosted job `95430351866`, bounded window `0xb56d60..0xb57280`, SHA-256 `e5cf009bb1aec3065da4ff0dd3231268af1255cffa50fbb48f8817777907d557`.

Final source validation:

```text
Track A governance 32045117129 = SUCCESS
CI                 32045117287 = SUCCESS
CI / Required      95431242465 = SUCCESS
changed files      3
reviews/threads    0/0
one-shot workflow  removed
```

No runtime/login/world-map/process-memory/raw executable upload/owner-funded AI was used.

## Proven sequence producer

At `TGameserverDualConnection+0x80@0xb56d60`, `r15` is the exact `TGameserverDualConnection this` and the exact message is saved at entry and restored before its terminal header update.

When `message+0x34 != 3`, the low header DWORD is explicitly zeroed:

```text
b56f55  mov rax,[rsp+0x10]
b56f5a  mov DWORD PTR [rax],0x0
```

When `message+0x34 == 3`, the connection-object-local 32-bit counter is copied into the same message header and post-incremented:

```text
b57058  mov eax,DWORD PTR [r15+0x9c]
b5705f  mov DWORD PTR [rsi],eax
b57061  add eax,0x1
b57064  mov DWORD PTR [r15+0x9c],eax
```

PR #494 independently proves this exact `DWORD(message+0)` is serialized by `0xf50090` before the raw payload on the concrete QTcpSocket-bound path. Therefore sequence numbering is direct instruction/dataflow evidence, not an inference from field width or position.

Promoted classification:

```yaml
FRAMING: PROVEN
SEQUENCE: PROVEN
SEQUENCE_FIELD: FACT:DWORD(message+0)
SEQUENCE_OWNER: FACT:TGameserverDualConnection_this_plus_0x9c
SEQUENCE_MODE: FACT:message_plus_0x34_equals_3
SEQUENCE_UPDATE: FACT:store_current_then_increment_by_one
SEQUENCE_NONMATCHING_MODE: FACT:message_plus_0_zero
SEQUENCE_WIDTH: FACT:32_bit
SEQUENCE_INITIALIZATION_OR_RESET_POLICY: UNKNOWN
COMPRESSION: UNKNOWN
ENCRYPTION: UNKNOWN
FINAL_BINARY_EGRESS: PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
FINAL_SOCKET_OWNER: FACT:TGameserverTCPConnection
FINAL_OS_SOCKET_SYSCALL: UNKNOWN
```

The unknown initial/reset policy does not weaken the proven per-object post-increment mechanism. No lifetime/reset semantics beyond the instructions are claimed.

## Next frontier

Resolve the exact dynamic type and input/output semantics of the `TGameserverNetworkPacketRawDataProcessor this+0x8/+0x10` member object whose vslot `+0x20` fast target is `0xf85eb0` and vslot `+0x28` fast target is `0xb3ec30`. The `0xb3ec30` call is conditional on `message+0x28 == 2`; test encryption directly and keep compression independent.

Audit: `PASS_BOUNDED`, material findings open `0`. E2E: `NOT_APPLICABLE` — static exact-file/disassembly evidence only.
