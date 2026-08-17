# OTC-20260817 — targeted exact protocol descriptor boundary

```yaml
evidence_date: 2026-08-17
repository: blakinio/otclient
task: OTC-20260817-track-a-worldmap-server-delivery-extent
pr: 473
execution_class: github_hosted
runtime_access: none
client_executed: false
client_bytes_modified: false
owner_funded_ai_api_used: false
exact_client_version: 15.32.df7b29
exact_client_size: 51965216
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Producer provenance

The bounded descriptor probe was intentionally repaired instead of being rerun identically after two failed parser heuristics.

```yaml
successful_producer_head: ae5778d1f8b0e79b77bfa68c14692a3d599b25c5
run_id: 32022973229
job_id: 95366330613
job_result: success
artifact_id: 9286040543
artifact_name: worldmap-server-delivery-descriptors-32022973229
artifact_zip_sha256: a7bba32855e73c6b2a29c5dfae4da04e0498bcae985b37de91ef79658dac6281
artifact_uploaded_bytes: 2194
raw_client_uploaded: false
```

The job completed all producer and upload steps successfully. It fetched the same compressed client fence, verified the exact decompressed SHA and emitted only bounded JSON/text evidence.

## FACT — one exact serialized descriptor was recovered

The targeted raw-`DescriptorProto` anchor recovered the exact `tibia.protobuf.shared.Coordinate` descriptor at client file offset `43359271`:

```yaml
Coordinate:
  descriptor_size: 45
  fields:
    - {number: 1, name: x, label: optional, type: uint32}
    - {number: 2, name: y, label: optional, type: uint32}
    - {number: 3, name: z, label: optional, type: uint32}
```

The bounded byte neighborhood begins with a directly readable serialized `shared.proto` / `tibia.protobuf.shared` block and the three field descriptors. This validates the targeted parser on a real exact-client descriptor rather than only on synthetic assumptions.

## FACT — requested protocol-message descriptors were not recoverable through this exact serialized-descriptor path

The same validated targeted scan did **not** recover a serialized top-level `DescriptorProto` for any of:

```text
Extent
MapFieldData
RowData
ColumnData
GameclientMessageLogin
GameclientMessageSecondaryLogin
GameclientMessageClientDetails
GameclientMessageEnterWorld
GameclientMessageSetClientOptions
GameserverMessageFullMap
GameserverMessageFieldData
GameserverMessageLeftColumn
GameserverMessageRightColumn
GameserverMessageTopRow
GameserverMessageBottomRow
GameserverMessageTopFloor
GameserverMessageBottomFloor
```

This is a bounded recovery failure, not proof that those C++/protobuf types have no fields.

## FACT — the visible `tibia.protobuf.protocol` token is not an inline raw protocol FileDescriptorProto

The exact binary contains one printable occurrence of `tibia.protobuf.protocol` in the bounded scan. Its neighborhood is a concatenated generated-type/name table beginning with strings such as:

```text
tibia.protobuf.protocol.GameserverMessage...
```

It is not laid out like the directly validated `shared.proto` serialized descriptor block around `Coordinate`. This explains why a strict raw `FileDescriptorProto` parser yielded zero protocol descriptor files even after the correct `message_type=4` fix.

## Failed attempts and repair record

```yaml
attempts:
  - run: 32022548050
    head: 888630af1de1d05be1f131df428360c9b4d215ba
    result: failure
    diagnosis: producer used FileDescriptorProto field 6 instead of message_type field 4
  - run: 32022815851
    head: 57b3068a16fe4d0ee9255fe20bbed4a17f272b9f
    result: failure
    diagnosis: corrected field number, but strict raw protocol FileDescriptorProto start/layout heuristic still did not match the exact generated layout
  - run: 32022973229
    head: ae5778d1f8b0e79b77bfa68c14692a3d599b25c5
    result: success
    diagnosis: targeted descriptor parser validated on Coordinate; protocol targets remain outside this recoverable raw-descriptor surface
```

No failed attempt was rerun identically. Under the task anti-stall/repair budget, this closes the descriptor-producer escalation rather than creating another increasingly broad workflow.

## Direct acceptance consequence

```yaml
OUTBOUND_EXPLICIT_EXTENT_MESSAGE_NAME: absent_in_complete_160_name_census
OUTBOUND_GENERIC_MESSAGE_EXTENT_FIELD_CENSUS: NOT_RECOVERED
INBOUND_MAP_DELIVERY_MESSAGE_DIRECTION: PROVEN_SERVER_TO_CLIENT
PROTOCOL_COORDINATE_FIELD_TYPES: x_y_z_uint32_proven
PROTOCOL_EXTENT_FIELD_SCHEMA: UNKNOWN
SERVER_MAP_DELIVERY_MODEL: UNKNOWN
SERVER_LARGER_RECTANGLE_SUPPORTED: UNKNOWN
SERVER_FULL_FLOOR_DELIVERY_SUPPORTED: UNKNOWN
SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED: UNKNOWN
SERVER_WHOLE_MAP_DELIVERY_SUPPORTED: UNKNOWN
MAX_SERVER_DELIVERABLE_EXTENT: UNKNOWN
```

The exact evidence is sufficient to prove map-payload directionality and to exclude a separately named outbound extent/range message from the complete generated-message-name census. It is **not** sufficient to rule out a negotiation field embedded in a generic outbound message or to prove a server maximum. The required model flag therefore remains `UNKNOWN`.
