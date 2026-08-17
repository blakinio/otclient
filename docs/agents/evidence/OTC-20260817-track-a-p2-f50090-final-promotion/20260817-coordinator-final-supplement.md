# Track A P2 `0xf50090` — final coordinator promotion supplement

Date: 2026-08-17  
Source task: `OTC-20260817-track-a-p2-f50090-downstream`  
Source Draft: PR #488 (closed unmerged)  
Supersedes source-head boundary used by merged promotion PR #489  
Final reviewed source head: `ebda1b1c01a801e749d3ec2ed5973705e8140969`  
Disposition: **ACCEPT_WITH_EDITS / FINAL SOURCE-HEAD REPAIR**

## Why this supplement exists

Promotion PR #489 merged canonical evidence from an earlier frozen #488 head. Before the researcher branch was terminally closed, #488 advanced to a later exact-head-only durable result that preserved the same bounded task scope but added independently verifiable type/symbol identities. This supplement repairs that lifecycle race without reopening research or creating a new frontier task.

## Exact client fence

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform official native Linux only
```

No live client process, process memory, login/gameplay, canonical runtime state or world-map evidence is used.

## Final #488 exact-head validation

```text
source head          ebda1b1c01a801e749d3ec2ed5973705e8140969
Track A governance   32038034263 = SUCCESS
CI                    32038034467 = SUCCESS
CI / Required         95412354038 = SUCCESS
changed files         exactly 3 durable P2 files
unresolved threads    0
one-shot surfaces     absent
```

Coordinator review on the final head classified the result `ACCEPT_WITH_EDITS`; material findings open: `0`. E2E is `NOT_APPLICABLE` because this is static exact-file/disassembly evidence only.

## Independent type/symbol proof

Current canonical `main` already contains the exact-build final-write reconciliation that directly resolves:

```text
TIODeviceWriter
  RTTI                 0x3080718
  vtable header start  0x2f69d38
  vtable address point 0x2f69d48

TProtocolWriter
  RTTI                 0x3080728
  vtable address point 0x2f69dd0
  RTTI base -> TIODeviceWriter
```

Canonical source:
`docs/agents/evidence/OTC-20260813-official-client-re/20260814-final-write-reconciliation-generation-5.md`.

Historical exact-SHA researcher artifact #308 was independently re-downloaded and re-hashed before use:

```text
run       31903490468
artifact  9251725866
sha256    f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
rehash    PASS
```

The sanitized artifact independently proves helper `0x1960340` binds a supplied QIODevice shared pair to a retained QDataStream at helper `+0x18/+0x20`; its disassembly also resolves exact PLT target:

```text
0x4dd250 = QDataStream::writeRawData(char const*, qint64)
```

The artifact is supporting static evidence only. Its historical coordinator PR state is not used as authority; every promoted identity above is independently checked against current canonical type evidence and exact immutable artifacts.

## Exact constructor binding to the current `0xf50090` receiver

The independently re-hashed nested-vcall generation-3 artifact `9290498273` (SHA-256 `4aa991a9912c3fb56cc08863ba94ac9e73e78a466a966c00353e85ce39a85323`) contains the exact constructor window `0xb4aea0..0xb4b800`.

Load-bearing sequence:

```text
b4b24b: lea rdi,[r14+0x10]
b4b253: mov rsi,[rbp-0x98]
b4b25a: mov [rbp-0xb8],rdi
b4b273: call 0x1960340
...
b4b2c2: mov rsi,[rbp-0xb0]
b4b2c9: lea rcx,0x2f741d8
b4b2d0: mov rdx,[rbp-0xb8]
b4b2db: mov [rsi+0x10],rcx
b4b2df: mov [rsi+0x18],rdx
```

The receiver object starts at `rsi+0x10`; therefore its member `this+0x08` is exactly `rdx`, the object initialized by helper `0x1960340`. Current canonical type evidence resolves that helper object as `TIODeviceWriter` AP `0x2f69d48` / RTTI `0x3080718`.

Thus:

```yaml
f50090_writer_member: FACT:this+0x08
f50090_writer_type: FACT:TIODeviceWriter
f50090_writer_vtable_ap: FACT:0x2f69d48
f50090_writer_rtti: FACT:0x3080718
f50090_writer_qiodevice_pair: FACT:writer+0x08/+0x10
f50090_writer_qdatastream_pair: FACT:writer+0x18/+0x20
f50090_writer_qdatastream_object: FACT:writer+0x18
```

## Final promoted `0xf50090` representation boundary

Generation-2/3 exact dataflow already proved that `0xf50090` receives the canonical same message, saves its original pointer, decomposes fields, and on the direct guarded raw-payload branch performs:

```text
payload pointer <- canonical message+0x10
payload length  <- canonical message+0x18
writer slot +0x58 guard == 0xcb2960
receiver        <- writer+0x18
call            -> 0x4dd250
```

Exact wrapper `0xcb2960` independently performs the same contract:

```text
rdx <- [argument+0x10]
rsi <- [argument+0x08]
rdi <- [writer+0x18]
-> 0x4dd250
```

Combining those exact dataflow facts with the independently verified writer/QDataStream identities yields:

```text
canonical same message
 -> 0xf50090
 -> structured message field decomposition
 -> TIODeviceWriter AP 0x2f69d48
 -> QDataStream object at writer+0x18
 -> QDataStream scalar serialization paths
 -> QDataStream::writeRawData(char const*, qint64) @ 0x4dd250
 -> bound QIODevice concrete type UNKNOWN
```

Promoted classifications:

```yaml
f50090_representation_boundary: FACT:STRUCTURED_MESSAGE_FIELDS_TO_TIODEVICEWRITER_QDATASTREAM
f50090_raw_payload_receiver: FACT:TIODeviceWriter+0x18_QDataStream
f50090_raw_payload_target: FACT:QDataStream::writeRawData@0x4dd250
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

`f50090_is_proven_final_binary_egress = DISPROVEN` means this exact function is positively classified as a serialization/QDataStream stage rather than a terminal socket-write stage. It does not rule out downstream network effects in the QIODevice bound to the stream.

## Programme handoff

The next technical frontier is the concrete QIODevice shared-pair provenance supplied to the current `TIODeviceWriter` at `b4b273 -> 0x1960340`, followed by its first post-serialization consumer. This supplement does **not** create or execute that new task in the current invocation.
