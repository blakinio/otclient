# Hardened P2 post-serialization buffer evidence

Date: 2026-08-15
Task: `OTC-20260815-track-a-p2-post-serialization-buffer-boundary`
Track: `official-client-re`
Draft PR: #308
Promotion authority: coordinator PR #300
Classification: `PROMOTION_CANDIDATE / BUFFER_DATAFLOW_PROVEN`

## Exact source and client fence

```text
code-bearing head: 34f73b0c48198ba452caa505b4c0f3ae7e5b61d7
semantic run: 31903490468
artifact: 9251725866
GitHub artifact digest: sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
locally rechecked ZIP digest: sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
repository CI on code-bearing head: 31903493799 SUCCESS
version mapping: 15.32.df7b29
client size: 51965216
client sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

The artifact contains only sanitized textual outputs (`result.json`, `result.txt`, `evidence.txt`, `validation.log`); no proprietary client bytes, credentials, account state, live packet payloads or runtime capture were persisted.

## Semantic verdict — FACT

The hardened artifact states:

```text
P2_POST_SERIALIZATION_RESULT=BUFFER_DATAFLOW_PROVEN
HELPER_QIODEVICE_QDATASTREAM_BINDING=PROVEN
LOCAL_QBUFFER_BYTEFLOW=PROVEN
PERSISTENT_TPROTOCOLWRITER_QBUFFER_BINDING=PROVEN
COMMON_QBUFFER_QDATASTREAM_BINDING=PROVEN
OBJECT_LIFECYCLE_ORDER=QBUFFER_AND_QDATASTREAM_BINDING_CONSTRUCTED_BEFORE_SERIALIZER_USE
PROTOCOL_STAGE_ORDER=UNKNOWN
PROTOCOL_FRAMING=UNKNOWN
SEQUENCE=UNKNOWN
COMPRESSION=UNKNOWN
ENCRYPTION=UNKNOWN
FINAL_BINARY_EGRESS=UNKNOWN
```

The representation boundary is therefore:

```text
STRUCTURED_FIELDS
  -> retained QDataStream serialization
  -> QBuffer-backed QIODevice byte container
```

This is a concrete data-flow/representation claim, not a claim about the complete outbound protocol pipeline.

## Persistent retained-writer chain — FACT

The strengthened checker directly validates exact setup/disassembly bytes for the persistent chain rather than inferring it from vtable adjacency:

```text
persistent QBuffer shared pair [rbp-0x40 / rbp-0x38]
  -> saved pair pointer [rbp-0x1a0]
  -> helper 0x1960340
  -> TIODeviceWriter helper object
  -> TProtocolWriter retained helper +0x18 / +0x20
  -> retained intermediate writer
  -> TProtocolClientMessageProcessor retained intermediate
```

Key exact validation anchors include:

```text
0x1970c89  persistent QBuffer control allocation
0x1970cad  QBuffer constructor
0x1970cc6  QBuffer open
0x1970cf5  QBuffer object-pair store
0x1970cfc  QBuffer control-pair store
0x1970d0c  persistent pair pointer load
0x1970d16  helper 0x1960340 call
0x1970d63  TProtocolWriter AP 0x2f69dd0 load
0x1970d71  writer retains helper object at +0x18
0x1970d7e  writer retains helper control at +0x20
0x1970f31  intermediate AP 0x2f69e30 load
0x1970f3f  intermediate retains writer object at +0x18
0x1971068  processor retains intermediate object at +0x18
```

The retained type/address-point fence is:

```text
TIODeviceWriter AP 0x2f69d48 / RTTI 0x3080718
TProtocolWriter AP 0x2f69dd0 / RTTI 0x3080728
retained intermediate AP 0x2f69e30 / RTTI 0x3080748
```

## Helper and local QBuffer relationship — FACT

Helper `0x1960340`:

- receives the supplied QIODevice shared pair;
- retains its object/control pair at helper `+0x8/+0x10`;
- constructs `QDataStream(QIODevice*)` using the supplied device object;
- retains the QDataStream pair at helper `+0x18/+0x20`;
- establishes the QDataStream byte-order state used by the writer path.

Slot `0xc20c70` independently proves the same object model locally: it constructs a `QBuffer`, passes that QBuffer shared pair to helper `0x1960340`, serializes through the helper-retained QDataStream, and later exposes QBuffer bytes via `QBuffer::buffer()`.

The promoted serializer slots `0xc10960` and `0xc20290` are revalidated by the hardened checker as QDataStream serialization on the retained writer branch.

## Temporal boundary — FACT vs UNKNOWN

Direct construction/use flow proves only the local object-lifecycle ordering:

```text
QBuffer + QDataStream binding constructed before serializer use
```

It does **not** establish global protocol-stage order. In particular, this task does not identify where framing, sequence numbering, compression, encryption or final binary egress occur relative to this byte container.

## Negative controls

The hardened result explicitly records that it did not use:

- vtable adjacency as temporal proof;
- generic QBuffer/QIODevice census as proof;
- final-socket run `31825417040`;
- superseded sink models;
- assumed direct DualConnection writer ownership.

QBuffer container management is not relabeled as protocol framing.

## Remaining UNKNOWN / next P2 gate

```yaml
protocol_stage_order: UNKNOWN
protocol_framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
causal_local_harness: UNKNOWN
```

The next P2 task should start from this promoted-candidate retained QBuffer-backed QDataStream boundary and trace the first exact consumer/transform after the retained byte container toward framing/final egress. It must continue to distinguish object lifecycle from protocol-stage order and may not use the forbidden generic-census/final-socket shortcuts.
