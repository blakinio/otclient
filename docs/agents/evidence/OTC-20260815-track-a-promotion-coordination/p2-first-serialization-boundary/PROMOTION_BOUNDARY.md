# Track A P2 first concrete serialization boundary — promotion boundary

Coordinator disposition: **ACCEPT_WITH_EDITS**  
Source Draft: PR #306  
Source final head: `c13e6d8946d1407c880a07d76fcfd5f4bf07c80b`  
Canonical base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

## Exact source validation

Coordinator independently reviewed the source machine result, evidence report and reproducer at the final source head, then inspected the final source workflow artifact.

Final source gates:

- static workflow run `31893391887`: **SUCCESS**;
- final source repository CI run `31893395016`: `CI / Required` **SUCCESS**;
- source review threads: `0`;
- final static artifact `9249137864`, digest `sha256:c80014c2cc9b3db5b3406540e7d6d4efeef0301f63fd5858379614179b59398d`;
- artifact contents: sanitized text/result files only (`result.json`, `result.txt`, `validation.log`, `evidence.txt`), no proprietary client bytes.

The final artifact independently reproduces the same machine semantic result as the earlier semantic artifact `9249061176` used by the source `RESULT.json`.

Exact client fence reproduced by the source workflow:

```text
version_mapping=15.32.df7b29
size=51965216
sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform=official_native_linux_only
runner=synology-otclient-01
```

## Promoted FACT

The exact-build retained branch is:

```text
TProtocolClientMessageProcessor
  -> retained intermediate shared object
       AP 0x2f69e30
       RTTI 0x3080748
  -> retained shared TProtocolWriter
       AP 0x2f69dd0
       RTTI 0x3080728
```

The source reproducer revalidates this chain from exact ELF structure and setup byte provenance rather than inheriting prior Draft claims.

Within the identified intermediate vtable:

```text
+0x00 -> 0x7de7f0   lifecycle-like
+0x08 -> 0x7dfd60   lifecycle-like
+0x10 -> 0xc10960   first concrete non-lifecycle slot observed
+0x18 -> 0xc20290   next concrete serializer slot
+0x20 -> 0xc20c70   adjacent QBuffer-construction slot
```

At `0xc10960` exact disassembly proves:

- retained writer access through intermediate member `+0x18`;
- a message-derived value from the structured argument path;
- serialization through `QDataStream::operator<<(signed char)`.

At `0xc20290` exact disassembly proves:

- argument provenance preserved as `rbx <- rsi`;
- structured argument fields at `+0x30` and `+0x34`;
- serialization through `QDataStream::operator<<(signed short)`.

At `0xc20c70`, exact disassembly proves construction of `QBuffer`.

Therefore the promoted representation boundary is:

```text
structured/typed object argument
  -> retained TProtocolWriter-associated QDataStream serialization sink
```

Canonical semantic classification:

```text
SERIALIZATION_ONLY_PROVEN
```

## Coordinator edit

The source task title uses "first transform boundary". Promotion narrows **first** to:

> the first concrete non-lifecycle slot directly demonstrated in this identified intermediate vtable.

It does **not** mean the temporally first transform/serialization operation in the complete outbound pipeline.

The evidence does not yet establish that `0xc10960` is invoked before every other transform, framing, sequencing, compression or encryption operation in the real message path.

## Explicit UNKNOWN / NOT_PROVEN

The following remain `UNKNOWN`:

- temporal first operation in the complete outbound pipeline;
- temporal order of `QBuffer` construction relative to the serializer calls;
- framing order;
- sequence-number order;
- compression boundary/order;
- encryption boundary/order;
- final binary egress/socket ownership for this retained branch;
- causal local harness from structured message input to final transmitted bytes.

Direct DualConnection writer ownership remains `NOT_PROVEN`.

## Negative controls retained

Promotion does not use as proof:

- generic `QIODevice::write` enumeration;
- generic Qt/QMeta census;
- vtable adjacency alone;
- final-socket run `31825417040`;
- superseded `0xb5b880`, `0xb46bd0`, `0xc33259` sink models;
- stale writer RTTI `0x3080700`.

## Canonical capability change

Before this promotion:

```text
P2 = PARTIAL_writer_retention_and_intermediate_type_structure_proven_transform_order_final_egress_harness_open
```

After this promotion:

```text
P2 = PARTIAL_writer_retention_intermediate_type_and_qdatastream_serialization_proven_pipeline_order_final_egress_harness_open
```

This is real P2 progress but is not Track A completion.
