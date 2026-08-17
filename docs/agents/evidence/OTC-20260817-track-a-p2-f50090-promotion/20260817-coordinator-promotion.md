# Track A P2 nested-vcall target — coordinator promotion

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-dual-nested-vcall-resolution`  
Source Draft: PR #483  
Final reviewed source head: `349530d89051391998f1f88ce686bde59a2df2c8`  
Decision: **ACCEPT_WITH_EDITS**

## Exact client

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

## Independent verification

The coordinator did not use the researcher summary as proof. Generation-3 final artifact `9290498273` from run `32035436709` / hosted job `95404893228` was independently downloaded and re-hashed:

```text
sha256 4aa991a9912c3fb56cc08863ba94ac9e73e78a466a966c00353e85ce39a85323
```

Source job `95404656415` independently fenced the retained exact file by size/SHA and copied only bounded file-backed code/data windows. It performed no disassembly or semantic classification, accessed no process/runtime state, and uploaded no raw executable/package. Hosted Ubuntu decoded the bounded bytes.

Primary constructor bytes independently rechecked:

```text
b4b280: mov edi,0x28
b4b285: call 0x4df670
b4b298: mov [rbp-0xb0],rax
b4b29f: add rax,0x10
b4b2ab: mov [rbp-0xc0],rax
...
b4b2c9: lea rcx,0x2f741d8
b4b2db: mov [rsi+0x10],rcx
...
b4b2f9: mov edi,0x48
b4b2fe: call 0x4df670
b4b31d: lea rax,[r15+0x10]
b4b33e: lea rax,0x30b7a68
b4b345: mov [r15+0x10],rax
b4b35e: mov rax,[rbp-0xc0]
b4b369: mov [r15+0x30],rax
b4b397: mov [rbx+0x20],rax
```

The exact receiver table window independently decodes:

```text
vtable AP  0x2f741d8
AP-0x10    0
AP-0x08    0x30b7548
AP+0x00    0xb57b10
AP+0x08    0xb57ba0
AP+0x10    0xf50090
AP+0x18    0
```

## Accepted canonical result

Combined with the already canonical same-message handoff from #450/#481:

```text
persistent QBuffer
 -> TProtocolClientMessageProcessor+0x10@0xc2df80
 -> TGameserverNetworkPacketRawDataProcessor+0x10@0xb47130
 -> same QByteArray/message
 -> TGameserverDualConnection +0x78@0xb56970
 -> tibia::network::TGameserverNetworkPacketConnection
 -> tibia::network::TGameserverNetworkPacketProcessor
 -> receiver vtable AP 0x2f741d8 slot +0x10
 -> 0xf50090
```

Promoted classifications:

```yaml
b56c93_same_message_preserved: FACT
outer_type: FACT:tibia::network::TGameserverNetworkPacketConnection
outer_vtable_ap: FACT:0x3084ba8
intermediate_type: FACT:tibia::network::TGameserverNetworkPacketProcessor
intermediate_vtable_ap: FACT:0x30b7a68
final_receiver_vtable_ap: FACT:0x2f741d8
final_receiver_rtti_pointer: FACT:0x30b7548
final_receiver_exact_dynamic_type: UNKNOWN
b56c93_virtual_slot: FACT:+0x10
b56c93_concrete_target: FACT:0xf50090
b56c93_target_equals_b40630: DISPROVEN
b57042_same_message_preserved: DISPROVEN
```

`0xb40630` is therefore not the surviving same-message continuation from `0xb56c93`. The exact surviving downstream target is `0xf50090`.

## Still UNKNOWN

- semantic role of `0xf50090`;
- whether/where this chain reaches a concrete binary socket egress;
- final socket ownership;
- framing;
- sequence;
- compression;
- encryption;
- complete transport ordering beyond `0xf50090`.

`0xf50090` is not labeled framing/compression/encryption/socket/final-egress without direct downstream evidence.

## Validation / audit

Source final head `349530d89051391998f1f88ce686bde59a2df2c8`:

```text
Track A governance 32035805051 = SUCCESS
CI                 32035805264 = SUCCESS
CI / Required      95405920582 = SUCCESS
changed files      exactly 3 durable P2 files
reviews/threads    0/0
```

Source one-shot workflows/scripts were removed. `runtime_access:none`; physical E2E is `NOT_APPLICABLE` because this is static exact-file/disassembly evidence only.

Fresh coordinator audit: `PASS_BOUNDED`; material findings open: `0`.

## Next frontier

The next smallest falsifiable task is bounded exact-client disassembly/dataflow of `0xf50090`. Preserve the same second argument and determine only whether it directly reaches a concrete binary-write sink, forwards/transforms to another exact target, or falsifies this candidate egress branch. Keep framing/sequence/compression/encryption/socket semantics UNKNOWN unless exact dataflow proves them.
