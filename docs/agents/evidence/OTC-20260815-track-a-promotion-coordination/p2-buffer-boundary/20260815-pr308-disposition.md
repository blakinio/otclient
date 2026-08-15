# Coordinator disposition — PR #308 post-serialization buffer boundary

Date: 2026-08-15
Programme: `OTCLIENT-TIBIA-RE`
Track: `official-client-re`
Source task: `OTC-20260815-track-a-p2-post-serialization-buffer-boundary`
Source Draft PR: #308
Source final release head: `7153ba4f0799a2c6b81eeeb62e4b1320e386c924`
Source code-bearing head: `34f73b0c48198ba452caa505b4c0f3ae7e5b61d7`
Disposition: `ACCEPT_WITH_EDITS`
Promotion authority: coordinator PR #300

## Exact client fence

```text
version mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official native Linux only
```

## Independent validation

The coordinator did not rely on the PR summary alone. It independently checked:

- supporting semantic run `31903141897`;
- hardened semantic run `31903490468`, `SUCCESS`;
- hardened artifact `9251725866`;
- GitHub artifact digest `sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e`;
- downloaded ZIP digest, independently rechecked and identical;
- code-bearing repository CI `31903493799`, `SUCCESS`;
- exact final release-head CI `31903882606` on `7153ba4f0799a2c6b81eeeb62e4b1320e386c924`, `SUCCESS`;
- all six PR files are inside the declared task-owned paths;
- code-bearing head -> release head changed only the task record and final sanitized evidence;
- source review submissions: zero;
- source review threads: zero.

## Promoted FACT — representation/data-flow boundary

The exact-build hardened artifact reports:

```text
P2_POST_SERIALIZATION_RESULT=BUFFER_DATAFLOW_PROVEN
HELPER_QIODEVICE_QDATASTREAM_BINDING=PROVEN
LOCAL_QBUFFER_BYTEFLOW=PROVEN
PERSISTENT_TPROTOCOLWRITER_QBUFFER_BINDING=PROVEN
COMMON_QBUFFER_QDATASTREAM_BINDING=PROVEN
```

The promoted representation boundary is therefore:

```text
structured fields
  -> retained QDataStream serialization
  -> QBuffer-backed QIODevice byte container
```

This strengthens the previously promoted retained-writer QDataStream evidence from #306. It is a concrete object/data-flow relationship, not a generic Qt/QBuffer census and not an inference from vtable adjacency.

## Promoted FACT — persistent retained-writer provenance

The strengthened checker directly validates the exact-build setup/disassembly path:

```text
persistent QBuffer shared pair [rbp-0x40 / rbp-0x38]
  -> saved pair pointer [rbp-0x1a0]
  -> helper 0x1960340
  -> TIODeviceWriter helper object
  -> TProtocolWriter retained helper +0x18 / +0x20
  -> retained intermediate writer
  -> TProtocolClientMessageProcessor retained intermediate
```

Promoted exact type/address-point fence:

```text
TIODeviceWriter AP 0x2f69d48 / RTTI 0x3080718
TProtocolWriter AP 0x2f69dd0 / RTTI 0x3080728
retained intermediate AP 0x2f69e30 / RTTI 0x3080748
```

Relevant validated exact anchors include:

```text
0x1970c89  persistent QBuffer control allocation
0x1970cad  QBuffer constructor
0x1970cc6  QBuffer open
0x1970cf5  QBuffer object-pair store
0x1970cfc  QBuffer control-pair store
0x1970d0c  persistent pair pointer load
0x1970d16  helper 0x1960340 call
0x1970d63  TProtocolWriter AP load
0x1970d71  writer retains helper object at +0x18
0x1970d7e  writer retains helper control at +0x20
0x1970f31  retained intermediate AP load
0x1970f3f  intermediate retains writer object at +0x18
0x1971068  processor retains intermediate object at +0x18
```

The hardened checker also revalidates serializer slots `0xc10960` and `0xc20290` and the local QBuffer slot `0xc20c70`.

## Promoted FACT — local lifecycle order only

Direct construction/use data flow proves:

```text
QBuffer/QDataStream binding is constructed before serializer use
```

Coordinator edit: this statement is limited to **object lifecycle order**. It must not be restated as global outbound protocol-stage order.

## Explicit UNKNOWN / non-promoted boundary

The source artifact itself correctly leaves:

```yaml
protocol_stage_order: UNKNOWN
protocol_framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
causal_local_harness: UNKNOWN
```

These remain canonical UNKNOWNs after promotion.

In particular, this disposition does not prove:

- where or whether framing occurs after the QBuffer-backed serialization boundary;
- packet/message sequence-number insertion;
- compression or encryption ordering;
- final binary egress or socket ownership;
- direct `DualConnection` writer ownership;
- causal parity against a local controlled protocol harness.

## Negative controls retained

The promotion does not use as proof:

- vtable adjacency as temporal ordering;
- generic QIODevice/QBuffer/QByteArray census;
- generic Qt/QMeta census;
- historical final-socket run `31825417040`;
- superseded sink models / stale writer RTTI;
- unproven direct DualConnection writer ownership.

QBuffer container management is not relabeled as protocol framing.

## Canonical P2 state after promotion

```yaml
retained_intermediate_type: PROVEN
retained_tprotocolwriter_type: PROVEN
retained_qdatastream_serialization: PROVEN
persistent_qbuffer_backed_qiodevice_binding: PROVEN
local_object_lifecycle_order: PROVEN
protocol_stage_order: UNKNOWN
framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
causal_local_harness: UNKNOWN
P2_COMPLETE: false
```

## Next P2 discriminator

The next P2 research task should start from the promoted retained QBuffer-backed QDataStream boundary and recover the **first exact consumer/transform after that retained byte container** toward framing/final egress. The worker must distinguish local object lifecycle from protocol-stage ordering and must not use generic census or the historical final-socket run as proof.

Source PR #308 remains a Draft research source and should be closed unmerged after this bounded promotion is durable.
