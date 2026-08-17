# Track A P2 — nested DualConnection virtual-call resolution

Date: 2026-08-17  
Task: `OTC-20260817-track-a-p2-dual-nested-vcall-resolution`  
Research status: **DRAFT / NOT PROMOTED — READY FOR COORDINATOR REVIEW AFTER FINAL CI**

## Exact-client fence

All new source generations fenced the same official native Linux client before reading any additional file bytes:

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

No client process, process memory, runtime/login/gameplay state or world-map evidence was used. Source-side staging performed only exact-fenced bounded file-byte mapping. Semantic disassembly/classification ran on GitHub-hosted Ubuntu. No raw executable/package was uploaded.

## Inputs

Canonical coordinator-promoted chain from #450/#481:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same QByteArray/message
 -> TGameserverDualConnection +0x80@0xb56d60 / +0x78@0xb56970
```

Accepted predecessor artifact `9283858910` independently re-downloaded/re-hashed as:

```text
sha256:2df8405269431397f3da0601ef24d9a9a8787dc33f3b5fdd43774f1eca36922c
```

It proves the local `+0x78/+0x80` callsite dataflow used below.

## New bounded generations

### Generation 1 — candidate vtables and constructor xrefs

```text
run             32033753449 = SUCCESS
source job      95399308395 = SUCCESS
hosted job      95400245919 = SUCCESS
source artifact 9289952632
source digest   sha256:176a174bafd8f77fb82ff8ea3737b0850be5b0327dc2ba6065e0d9bf51574e5a
final artifact  9289961937
final digest    sha256:fa1cddd5410454d9f5b717afe0d625d404a7750fb82ffb4b8a9d288cbc9ac64a
```

### Generation 2 — constructor bridge

```text
run             32034648596 = SUCCESS
source job      95402114226 = SUCCESS
hosted job      95402454465 = SUCCESS
source artifact 9290206232
source digest   sha256:27e946c3a864aac6257675e3ff6403eec93476223efed400bd72907cdb10f1a4
final artifact  9290395475
final digest    sha256:a0b396081570a1729e964bf8c57ad726ab95d91e3cf54f6857ebb43248afdebf
bounded code    0xb4aea0..0xb4b800
```

### Generation 3 — exact receiver vslot qword

```text
run             32035436709 = SUCCESS
source job      95404656415 = SUCCESS
hosted job      95404893228 = SUCCESS
source artifact 9290490800
source digest   sha256:f70f2f1ecc4e4af15323c6bee8998938cc79c25c454d72101672c1d9a0a68fa6
final artifact  9290498273
final digest    sha256:4aa991a9912c3fb56cc08863ba94ac9e73e78a466a966c00353e85ce39a85323
code window     0xb4aea0..0xb4b800
data window     0x2f741c0..0x2f74250
```

The coordinator/researcher independently re-hashed all downloaded generation-2/3 ZIPs to the GitHub-recorded digests before interpreting their hosted outputs.

## `0xb56c93`: same message preserved

The canonical `TGameserverDualConnection +0x78@0xb56970` entry preserves its original second SysV argument:

```text
b5697b: mov r14,rsi
```

The surviving path is:

```text
b56c50: mov rbx,[r12]
b56c54: lea rsi,0xb3eda0
b56c5b: mov rax,[rbx]
b56c5e: mov rax,[rax+0x98]
b56c65: cmp rax,rsi
...
b56c6e: mov rdi,[rbx+0x20]
b56c72: lea rdx,0xf45cf0
b56c79: mov rax,[rdi]
b56c7c: mov rax,[rax+0x60]
b56c80: cmp rax,rdx
...
b56c89: mov rdi,[rdi+0x20]
b56c8d: mov rsi,r14
b56c90: mov rax,[rdi]
b56c93: call [rax+0x10]
```

Because #450 canonically identifies the `+0x78` second argument as the same post-`RawDataProcessor` message:

```yaml
b56c93_second_argument: FACT:original_b56970_second_argument_rsi
b56c93_same_message_preserved: FACT
```

## Exact outer and intermediate identities

Generation 1 recovered valid Itanium-style vtable headers plus RTTI names and exact guard slots.

Outer address point:

```text
vtable AP   0x3084ba8
RTTI        N5tibia7network34TGameserverNetworkPacketConnectionE
identity    tibia::network::TGameserverNetworkPacketConnection
AP+0x78     0xb3ed90
AP+0x80     0xb57470
AP+0x98     0xb3eda0
```

Intermediate address point:

```text
vtable AP   0x30b7a68
RTTI        N5tibia7network33TGameserverNetworkPacketProcessorE
identity    tibia::network::TGameserverNetworkPacketProcessor
AP+0x60     0xf45cf0
```

The exact forwarding methods are:

```text
b3eda0: mov rdi,[rdi+0x20]
        ... guard intermediate +0x60 against 0xf45cf0 ...
        mov rdi,[rdi+0x20]
        mov rax,[rdi]
        call [rax+0x10]

f45cf0: mov rdi,[rdi+0x20]
        mov rax,[rdi]
        jmp [rax+0x10]
```

No reachability is inferred from adjacency; the constructor below binds these members.

## Constructor binds the final receiver

Hosted generation-2 decode of `0xb4aea0..0xb4b800` establishes the object construction/dataflow.

The final receiver allocation is created as:

```text
b4b280: mov edi,0x28
b4b285: call 0x4df670
b4b298: mov [rbp-0xb0],rax        # allocation base
b4b29f: add rax,0x10
b4b2a3: mov [rax-0x10],0x2f74200
b4b2a7: mov [rax-0x8],rsi
b4b2ab: mov [rbp-0xc0],rax        # receiver = allocation+0x10
...
b4b2c2: mov rsi,[rbp-0xb0]
b4b2c9: lea rcx,0x2f741d8
...
b4b2db: mov [rsi+0x10],rcx        # receiver[0] = 0x2f741d8
```

The `TGameserverNetworkPacketProcessor` object is then constructed and bound to that receiver:

```text
b4b2f9: mov edi,0x48
b4b2fe: call 0x4df670
b4b303: mov r15,rax
...
b4b31d: lea rax,[r15+0x10]        # processor object
...
b4b33e: lea rax,0x30b7a68
b4b345: mov [r15+0x10],rax         # processor vptr
...
b4b35e: mov rax,[rbp-0xc0]
b4b369: mov [r15+0x30],rax         # processor this+0x20 = receiver
...
b4b397: mov [rbx+0x20],rax         # outer this+0x20 = processor object
```

Thus the live callsite chain is structurally bound:

```text
TGameserverNetworkPacketConnection this+0x20
 -> TGameserverNetworkPacketProcessor object
 -> processor this+0x20
 -> receiver with vtable address point 0x2f741d8
```

## Exact `+0x10` target

Generation 3 staged only the exact receiver table window and hosted validation read its qwords:

```text
receiver vtable AP        0x2f741d8
AP-0x10 offset-to-top     0
AP-0x08 RTTI pointer      0x30b7548
AP+0x00                   0xb57b10
AP+0x08                   0xb57ba0
AP+0x10                   0xf50090
AP+0x18                   0x0
```

Therefore:

```yaml
b56c93_receiver_vtable_address_point: FACT:0x2f741d8
b56c93_receiver_rtti_pointer: FACT:0x30b7548
b56c93_receiver_exact_dynamic_type: UNKNOWN
b56c93_virtual_slot: FACT:+0x10
b56c93_concrete_target: FACT:0xf50090
b56c93_target_equals_b40630: DISPROVEN
```

Combining the canonical same-message proof and the exact constructor/vtable binding gives the newly proven stage:

```text
TGameserverDualConnection +0x78@0xb56970
 -> same message preserved
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable 0x2f741d8 +0x10
 -> 0xf50090
```

`0xf50090` is an exact concrete downstream function target. This task does **not** classify it as framing, compression, encryption, final binary egress or a socket sink; those properties require direct evidence from that function/downstream dataflow.

## `0xb57042`: rejected as the same-message continuation

For the `+0x80` visible taken branch:

```text
b56ed4: movabs rsi,0x100000001
b56ee1: cmp rdx,rsi
b56ee4: je 0xb57030
...
b57042: call [rdx+0x10]
```

No instruction on that direct branch restores the entry message to `rsi` before the call.

```yaml
b57042_rsi_on_taken_branch: FACT:0x100000001
b57042_same_message_preserved: DISPROVEN
b57042_is_same_message_edge_to_b40630: DISPROVEN
```

## Current P2 classification

```yaml
b56c93_to_b40630: DISPROVEN
b56c93_to_f50090: PROVEN
DUALCONNECTION_TO_BINARY_EGRESS: UNKNOWN
FINAL_BINARY_EGRESS: UNKNOWN
FINAL_SOCKET_OWNER: UNKNOWN
FRAMING: UNKNOWN
SEQUENCE: UNKNOWN
COMPRESSION: UNKNOWN
ENCRYPTION: UNKNOWN
```

The exact stage order currently proven is:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same QByteArray/message
 -> TGameserverDualConnection +0x78@0xb56970
 -> TGameserverNetworkPacketConnection
 -> TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8 +0x10
 -> 0xf50090
```

## Negative controls / historical corrections

- `0xb4066b == TGameserverDualConnection +0x90 final egress`: DISPROVEN by #458/#481.
- direct `QTcpSocket*` sink at `0xb4066b`: DISPROVEN.
- surviving `0xb56c93 -> 0xb40630`: DISPROVEN; exact target is `0xf50090`.
- `0xb57042` as same-message continuation: DISPROVEN for the exact visible taken branch.
- `0xb46bd0`: QString/local8bit/newline path only; not binary gameplay-frame proof.
- `0xc33259`: QMatrix4x4/non-network; DISPROVEN network candidate.
- `0xb5b880`: SUPERSEDED historical endpoint model.
- no generic Qt write census, class-name-only inference, address adjacency or mere `QTcpSocket*` ownership is used as binary-gameplay proof.

## Next smallest falsifiable frontier

Disassemble a bounded exact-client window for `0xf50090` and track the **same second argument** through that function. Determine whether it:

1. directly reaches a concrete binary-write sink;
2. transforms/forwards the same QByteArray to another exact target; or
3. falsifies the current egress branch.

Do not classify framing/sequence/compression/encryption/socket ownership until direct dataflow from `0xf50090` warrants it.

E2E: `NOT_APPLICABLE` — exact static file/disassembly evidence only.
