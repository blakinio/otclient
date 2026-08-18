# OTCLIENT Track A — exhaustive inbound static census

Date: 2026-08-18  
Task: `OTC-20260818-track-a-s1-unfiltered-static-census`  
PR: `#509`  
Track: `official-client-re`  
Execution: GitHub-hosted static exact-file analysis only (`runtime_access: none`)

## Executive result

The exact official Linux Tibia `15.32.df7b29` client has a stable generated protocol denominator:

```text
349 total generated protocol message types
160 client -> server
189 server -> client
```

Fresh run `32112814216` reproduced all three registries byte-for-byte against the independent sanitized #473 control artifact. The historical 98-message capability-regex set is therefore a discovery subset, not the protocol denominator.

The broad static method selector returned `542` strings, but they are not all inbound handlers:

```text
handle*     149
received*   189
on*         204
TOTAL       542
```

The clean inbound receive-surface result is **189 exact `received*Message` strings** for **189 generated `GameserverMessage*` names**. Comparing stems gives `188` exact name matches and one naming variant:

```text
GameserverMessageTrackQuestFlags
receivedTrackedQuestFlagsMessage
```

This is FACT about exact-binary string presence and string comparison. It is not yet proof of a generated-message -> concrete receive-method dispatch edge.

The client also contains at least `47` distinct `*ProtocolMessageHandler` class names with direct executable code-to-class-string xrefs. This proves a broad, domain-partitioned protocol-handler **type surface**. It neither proves nor disproves a shared upstream dispatcher; that remains `UNKNOWN`.

## Exact client fence and producer

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
platform: official_native_linux_only
producer_run: 32112814216
producer_job: 95635760592
producer_result: SUCCESS
producer_artifact: 9315562574
producer_artifact_digest: sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

The producer did not execute the client. It deleted compressed/unpacked proprietary client bytes before artifact upload. It did not use Synology, X11/VNC, process memory, credentials, account/session values, login/gameplay or PR #475 runtime state.

## Independent denominator control

Prior sanitized exact-build control:

```text
run      32022209943
artifact 9285763750
digest   sha256:0f71be3021885f3f8881199c5f74839fca6c6c5081594fab48998298abaadbd6
```

Fresh and control registry hashes are identical:

| Registry | SHA-256 |
|---|---|
| all 349 | `55f7cf2d6d4a63df6e24b8b156e38f1a2a64a9d6394357aa914661ab48fd983b` |
| 160 client -> server | `621ecb7aa1a62aae559e8d793d1aebe9289d84811bc43c4339a7153458b553f0` |
| 189 server -> client | `e642f661546c2e6e89ddcd77ac5e8aa9cd517408a309f95a3a367af943550d96` |

Complete durable registries:

```text
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-client-to-server.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/received-message-methods.txt
```

## Receive-method name surface

For `188/189` generated inbound names, removing wrappers gives exactly the same stem:

```text
GameserverMessagePlayerDataCurrent -> receivedPlayerDataCurrentMessage
GameserverMessagePlayerState       -> receivedPlayerStateMessage
GameserverMessagePlayerInventory   -> receivedPlayerInventoryMessage
GameserverMessagePlayerSkills      -> receivedPlayerSkillsMessage

GameserverMessageCreatureData      -> receivedCreatureDataMessage
GameserverMessageCreatureHealth    -> receivedCreatureHealthMessage
GameserverMessageCreatureUpdate    -> receivedCreatureUpdateMessage
GameserverMessageMoveCreature      -> receivedMoveCreatureMessage

GameserverMessageContainer         -> receivedContainerMessage
GameserverMessageCreateInContainer -> receivedCreateInContainerMessage
GameserverMessageChangeInContainer -> receivedChangeInContainerMessage
GameserverMessageDeleteInContainer -> receivedDeleteInContainerMessage

GameserverMessageTalk              -> receivedTalkMessage
GameserverMessageChannels          -> receivedChannelsMessage
GameserverMessageChannelEvent      -> receivedChannelEventMessage
GameserverMessagePrivateChannel    -> receivedPrivateChannelMessage
```

The sole stem variant is `TrackQuestFlags` vs `TrackedQuestFlags`; the binary separately contains `handleTrackedQuestFlagsMessage` and `onTrackedQuestFlagsChanged`.

Classification:

```yaml
COMPLETE_189_RECEIVED_METHOD_STRING_SURFACE: FACT_STRING_PRESENCE
188_EXACT_STEM_MATCHES_PLUS_1_NAMING_VARIANT: FACT_STRING_COMPARISON
GENERATED_MESSAGE_TO_RECEIVED_METHOD_DISPATCH: INFERENCE_STATIC_LEXICAL_ONLY
```

## Protocol-handler type/code surface

The producer retained `148` relevant demangled protocol/storage/session/data types and `47` distinct `*ProtocolMessageHandler` class strings with direct executable xrefs. Representative classes:

```text
tibia::authentication::TLoginProtocolMessageHandler
tibia::chat::TChatProtocolMessageHandler
tibia::container::TContainerProtocolMessageHandler
tibia::creatures::TCreatureProtocolMessageHandler
tibia::game::TGameProtocolMessageHandler
tibia::game::TPlayerProtocolMessageHandler
tibia::game::TServerModalDialogProtocolMessageHandler
tibia::market::TMarketProtocolMessageHandler
tibia::network::TNetworkQualityProtocolMessageHandler
tibia::quickloot::TManagedContainersProtocolMessageHandler
tibia::questlog::TQuestLogProtocolMessageHandler
tibia::sound::TSoundProtocolMessageHandler
tibia::store::TStoreProtocolMessageHandler
tibia::trade::TPlayerTradeProtocolMessageHandler
tibia::worldmap::TWorldmapProtocolMessageHandler
```

The complete 47-entry catalogue is `protocol-handler-code-xrefs.tsv`. Every row is explicitly classified only as:

```text
DIRECT_CODE_TO_STRING_XREF
semantic_dispatcher_edge_proven=false
```

The xrefs are compatible with generated Qt/metaobject-related code, but this task does not promote that role without a bounded instruction/control-flow proof.

## Exact-build anchor revalidation

The current-main relocation-aware resolver uniquely re-resolved all configured anchors:

| Target | Primary vptr |
|---|---:|
| `TGameClient` | `0x3076908` |
| `TGameserverGameSession` | `0x3078ba0` |
| `TPlayerProtocolMessageHandler` | `0x308a008` |
| `TPlayerData` | `0x308ca70` |
| `TContainerStorage` | `0x308a1a0` |
| `TCreatureStorage` | `0x308d078` |
| `TWorldmapProtocolMessageHandler` | `0x30871d8` |

These are exact-file anchors, not current runtime addresses or live-object proof.

## Negative control: rejected family buckets

The temporary producer emitted convenience substring family buckets. Final audit rejected them as semantic evidence because substring collisions exist, e.g. `Mark` inside `Market` and `row` inside `Browse`. No durable conclusion depends on those buckets.

## Proven / inferred / unknown

```yaml
FACT:
  exact_generated_protocol_denominator: 349
  client_to_server_registry: 160
  server_to_client_registry: 189
  fresh_lists_match_independent_control_byte_for_byte: true
  broad_candidate_method_strings: 542
  handle_prefixed_strings: 149
  received_message_strings: 189
  on_prefixed_strings: 204
  exact_received_stem_matches: 188
  received_naming_variants: 1
  protocol_handler_classes_with_direct_code_string_xref: 47
  current_profile_vptr_anchors_unique: true

INFERENCE:
  generated_message_to_received_method_name_alignment: static_lexical_only
  native_protocol_handler_type_surface: domain_partitioned

UNKNOWN:
  generated_message_to_concrete_handler_dispatch
  received_method_to_handler_owner
  handler_to_storage_controller_mutation_edge
  common_upstream_inbound_dispatcher
  runtime_object_identity
  runtime_message_delivery
```

## Next non-conflicting static work

While PR #475 owns native-login/worldmap runtime work, the highest-value independent S2 frontiers are:

```text
1. TPlayerProtocolMessageHandler
   -> PlayerDataCurrent / PlayerState / PlayerInventory / PlayerSkills
   -> exact QMeta/dispatch targets
   -> static TPlayerData owner/mutation edge where provable

2. TCreatureProtocolMessageHandler
   -> CreatureData / CreatureHealth / CreatureUpdate / MoveCreature
   -> static TCreatureStorage edge

3. TContainerProtocolMessageHandler
   -> Container / Create / Change / DeleteInContainer
   -> static TContainerStorage edge

4. TChatProtocolMessageHandler
   -> Talk / Channels / ChannelEvent / PrivateChannel
   -> chat storage/controller edge
```

These are exact-file static tasks. They do not need to consume or observe PR #475's physical runtime.
