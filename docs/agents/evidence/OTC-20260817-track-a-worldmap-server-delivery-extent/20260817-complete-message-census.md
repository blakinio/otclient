# OTC-20260817 — complete exact-client worldmap message census

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

## Scope

This record closes the message-name coverage gap left by historical run `31651220862`, job `94295767215`. That historical run recovered all 349 generated protocol-message names but printed only a deliberately filtered 98-name subset. Absence from that subset was therefore not admissible negative evidence.

No physical or canonical runtime was used. A temporary branch-only GitHub-hosted producer fetched the same exact public Linux client through the already-proven WARP path, checked both compressed and decompressed hashes, emitted only text evidence and deleted the compressed client before artifact upload.

## Producer provenance

```yaml
workflow: .github/workflows/track-a-worldmap-server-delivery-static.yml
producer_head: 553e447c0662892b0c1b9cab994c4545d09f22c8
run_id: 32022209943
job_id: 95364071999
result: success
artifact_id: 9285763750
artifact_name: worldmap-server-delivery-static-32022209943
artifact_zip_sha256: 0f71be3021885f3f8881199c5f74839fca6c6c5081594fab48998298abaadbd6
artifact_uploaded_bytes: 20525
artifact_file_count: 8
raw_client_uploaded: false
```

The job log reports successful exact-client hash verification and successful artifact finalization. The artifact contains only generated text/JSON inventories.

## FACT — complete generated-message inventory

```text
PROTOCOL_MESSAGE_TOTAL=349
CLIENT_TO_SERVER_MESSAGE_SYMBOLS=160
SERVER_TO_CLIENT_MESSAGE_SYMBOLS=189
```

The complete 160-name client-to-server list contains no generated message whose name includes any of:

```text
aware
range
extent
viewport
fullmap
fielddata
width
height
```

The only five names selected by the broader map/field/world/floor/row/column/etc. regex are:

```text
GameclientMessageBrowseField
GameclientMessageCyclopediaMapAction
GameclientMessageEnterWorld
GameclientMessageGetOfferDescription
GameclientMessageMarketBrowse
```

This is **bounded negative evidence at generated-message-name level only**. It does not prove that generic outbound messages such as `GameclientMessageClientDetails`, `GameclientMessageLogin`, `GameclientMessageSecondaryLogin`, `GameclientMessageEnterWorld` or `GameclientMessageSetClientOptions` lack extent/range fields.

## FACT — normal gameplay map-delivery families are server-to-client

The complete generated-message inventory contains these server-to-client map families:

```text
GameserverMessageFullMap
GameserverMessageFieldData
GameserverMessageLeftColumn
GameserverMessageRightColumn
GameserverMessageTopRow
GameserverMessageBottomRow
GameserverMessageTopFloor
GameserverMessageBottomFloor
GameserverMessageCreateOnMap
GameserverMessageChangeOnMap
GameserverMessageDeleteOnMap
GameserverMessageWorldEntered
```

The exact binary also contains server-queue registration type strings for the `FullMap`, row, column and floor messages and handler/QMeta-style names such as `handleFullMapMessage`, `receivedFullMapMessage`, `handleLeftColumnMessage`, `receivedTopFloorMessage`, etc. These establish directionality and client handling surfaces; they do not establish maximum server extent.

## FACT — protocol-schema leads present in the exact binary

The exact text census additionally recovers protobuf/type/schema leads:

```text
tibia::protobuf::protocol::Extent
N5tibia8protobuf8protocol6ExtentE
N5tibia8protobuf8protocol12MapFieldDataE
Extent
MapFieldData
ColumnData
RowData
AdditionalRowsTop
AdditionalRowsBottom
Columns
Rows
```

These strings show that extent/row/column concepts exist in the exact protocol implementation. Sorted string presence alone does not bind any field to a particular message and therefore is not used as a field-schema claim.

## FACT — accepted historical handler evidence remains compatible

Existing exact-client evidence in `docs/agents/evidence/OTC-20260816-track-a-worldmap-extent-static-re/20260816-exact-handler-disassembly-recovery.md` proves that the research-labelled `FullMap` handler at static `0x00cec8d0` consumes event-side map geometry, scales two adjacent integers by 32 and reaches the map-description path at `0x019a8a80`. That path uses descriptor fields `+0x38/+0x3c/+0x40` as multiplicative/divisor grid parameters plus additive coordinate bases and a floor-dependent transform.

This proves a real protocol-to-worldmap geometry path. It still does not name the server-side maximum or prove that client-local `18/14` changes what the server sends.

## Final classification boundary

The follow-on targeted descriptor producer has completed. Its bounded result is persisted in `20260817-targeted-descriptor-boundary.md`.

```yaml
SERVER_MAP_DELIVERY_DIRECTIONALITY: server_to_client_map_payload_families_proven
OUTBOUND_EXPLICIT_EXTENT_MESSAGE_NAME: absent_in_complete_160_name_census
OUTBOUND_GENERIC_MESSAGE_EXTENT_FIELD_CENSUS: NOT_RECOVERED
SERVER_MAP_DELIVERY_MODEL: UNKNOWN
SERVER_LARGER_RECTANGLE_SUPPORTED: UNKNOWN
SERVER_FULL_FLOOR_DELIVERY_SUPPORTED: UNKNOWN
SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED: UNKNOWN
SERVER_WHOLE_MAP_DELIVERY_SUPPORTED: UNKNOWN
MAX_SERVER_DELIVERABLE_EXTENT: UNKNOWN
```

Do not collapse `TopFloor`/`BottomFloor` names into a claim that an entire world floor is transferable. The names establish message families only.

## Static discriminator outcome

The targeted descriptor probe validated its parser against the exact serialized `tibia.protobuf.shared.Coordinate` descriptor but did not recover exact descriptors for `Extent`, the generic outbound target messages, or the map-delivery server messages. That bounded failure does not justify another broader producer. The remaining extent-control distinction requires the separately authorized physical causal experiment defined by `docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-extent.md`.
