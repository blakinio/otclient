# OTCLIENT Track A — exhaustive inbound static census

Date: 2026-08-18  
Task: `OTC-20260818-track-a-s1-unfiltered-static-census`  
PR: `#509`  
Track: `official-client-re`  
Execution: GitHub-hosted static exact-file analysis only (`runtime_access: none`)

## Executive result

The exact official Linux Tibia `15.32.df7b29` client contains a stable generated protocol denominator of:

```text
349 total generated protocol message types
160 client -> server
189 server -> client
```

A fresh producer on run `32112814216` independently reproduced the same three protocol registries byte-for-byte as the earlier exact-build #473 sanitized artifact. This removes the historical 98-message capability regex as an exhaustive denominator: it was only a filtered discovery subset.

The same fresh pass recovered a much broader inbound-oriented static surface:

```text
542 handle/received/on/process-style method strings
148 relevant demangled protocol/storage/session/data types in the producer artifact
47 distinct *ProtocolMessageHandler class names with direct executable code-to-class-string xrefs
```

The resulting picture is not one monolithic inbound handler. The client contains many domain-specific native protocol handler classes, including dedicated player, creature, container, chat, market, store, quest, prey, sound, tutorial, trade and worldmap handlers. The exact wiring from generated message type to concrete handler dispatch remains a separate S2 proof problem.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
platform: official_native_linux_only
```

Fresh producer markers:

```text
run      32112814216
job      95635760592
result   SUCCESS
artifact 9315562574
digest   sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

The producer did not execute the client and deleted the packed/unpacked proprietary bytes before artifact upload.

## Independent denominator control

The prior #473 sanitized artifact is still available:

```text
run      32022209943
artifact 9285763750
digest   sha256:0f71be3021885f3f8881199c5f74839fca6c6c5081594fab48998298abaadbd6
```

Fresh versus control registry hashes:

| Registry | SHA-256 | Fresh == control |
|---|---|---|
| all 349 | `55f7cf2d6d4a63df6e24b8b156e38f1a2a64a9d6394357aa914661ab48fd983b` | yes |
| 160 client -> server | `621ecb7aa1a62aae559e8d793d1aebe9289d84811bc43c4339a7153458b553f0` | yes |
| 189 server -> client | `e642f661546c2e6e89ddcd77ac5e8aa9cd517408a309f95a3a367af943550d96` | yes |

## Inbound generated-message coverage

All 189 generated `GameserverMessage*` names are now durably persisted in:

```text
docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/protocol-server-to-client.txt
```

The corresponding 160 outbound names are persisted separately for denominator completeness.

A name-surface comparison found at least one plausible inbound-oriented native method string for 188/189 generated server message names. This is a discovery correlation only; matching names do not prove dispatch.

The automatic stem matcher missed only:

```text
GameserverMessageTrackQuestFlags
```

The exact binary independently contains:

```text
handleTrackedQuestFlagsMessage
receivedTrackedQuestFlagsMessage
onTrackedQuestFlagsChanged
```

This is a strong lexical naming variant (`Track` vs `Tracked`), but the direct generated-message -> method edge remains `UNKNOWN` until static control/dataflow proves it.

## Domain-specific handler architecture

Forty-seven distinct `*ProtocolMessageHandler` class-name strings have direct executable code xrefs in the exact binary. Representative handlers:

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

The complete 47-entry address catalogue is persisted in `protocol-handler-code-xrefs.tsv`.

The xrefs cluster in several generated-code regions and are compatible with Qt metaobject/metacast-related code, but this task does not promote that role. A later S2 discriminator should locate the exact surrounding function boundary, metaobject metadata and invoke dispatch table before assigning a semantic role.

## High-value non-worldmap static correlations

The exact binary contains the following generated-message and receive/handle string pairs or families.

### Player state

```text
GameserverMessagePlayerDataBasic
 -> handlePlayerDataBasicMessage
 -> receivedPlayerDataBasicMessage

GameserverMessagePlayerDataCurrent
 -> receivedPlayerDataCurrentMessage

GameserverMessagePlayerState
 -> receivedPlayerStateMessage

GameserverMessagePlayerInventory
 -> handlePlayerInventoryMessage
 -> receivedPlayerInventoryMessage

GameserverMessagePlayerSkills
 -> receivedPlayerSkillsMessage
 -> onPlayerSkillStatsChanged
```

The current-main relocation-aware resolver also uniquely confirms:

```text
TPlayerProtocolMessageHandler vptr 0x308a008
TPlayerData                   vptr 0x308ca70
```

What remains unknown is the exact static handler dispatch and handler -> `TPlayerData` mutation edge.

### Creatures

```text
GameserverMessageCreatureData    -> receivedCreatureDataMessage
GameserverMessageCreatureHealth  -> receivedCreatureHealthMessage
GameserverMessageCreatureUpdate  -> receivedCreatureUpdateMessage
GameserverMessageMoveCreature    -> receivedMoveCreatureMessage
```

Static class/type evidence independently contains `tibia::creatures::TCreatureProtocolMessageHandler`, and the current-main resolver uniquely confirms `TCreatureStorage` primary vptr `0x308d078`.

The handler -> storage edge remains `UNKNOWN`.

### Containers and inventory

```text
GameserverMessageContainer
GameserverMessageCreateInContainer
GameserverMessageChangeInContainer
GameserverMessageDeleteInContainer
GameserverMessageCloseContainer
GameserverMessagePlayerInventory
GameserverMessageSetInventory
GameserverMessageDeleteInventory
```

correlate with exact `handle*Message` / `received*Message` surfaces. Static type evidence contains `tibia::container::TContainerProtocolMessageHandler`; the current-main resolver uniquely confirms `TContainerStorage` primary vptr `0x308a1a0`.

The handler -> storage edge remains `UNKNOWN`.

### Chat/channel

```text
GameserverMessageTalk            -> handleTalkMessage / receivedTalkMessage
GameserverMessageChannels        -> handleChannelsMessage / receivedChannelsMessage
GameserverMessageChannelEvent    -> handleChannelEventMessage / receivedChannelEventMessage
GameserverMessageOpenChannel     -> handleOpenChannelMessage / receivedOpenChannelMessage
GameserverMessagePrivateChannel  -> handlePrivateChannelMessage / receivedPrivateChannelMessage
```

Static RTTI/type census contains both `tibia::chat::TChatProtocolMessageHandler` and chat storage/controller families. Concrete dispatch/storage wiring remains `UNKNOWN`.

## Exact-build resolver revalidation

All current profile targets re-resolved uniquely on the fresh exact client:

| Target | Primary vptr |
|---|---:|
| `TGameClient` | `0x3076908` |
| `TGameserverGameSession` | `0x3078ba0` |
| `TPlayerProtocolMessageHandler` | `0x308a008` |
| `TPlayerData` | `0x308ca70` |
| `TContainerStorage` | `0x308a1a0` |
| `TCreatureStorage` | `0x308d078` |
| `TWorldmapProtocolMessageHandler` | `0x30871d8` |

These are static exact-build anchors, not current runtime addresses or live-object proof.

## Family-bucket negative control

The producer emitted rough convenience family buckets. Full review rejected those buckets as semantic evidence because substring-only grouping creates collisions such as:

```text
Mark inside Market
row inside Browse
```

No result in this report depends on those buckets. Exact generated names, exact native method strings, exact class names and explicit xrefs remain the evidence sources.

## What is proven versus still open

```yaml
FACT:
  exact_generated_protocol_denominator: 349
  client_to_server_registry: 160
  server_to_client_registry: 189
  fresh_lists_match_independent_control_byte_for_byte: true
  inbound_oriented_method_strings: 542
  protocol_handler_classes_with_direct_code_string_xref: 47
  current_profile_vptr_anchors_unique: true

INFERENCE:
  generated_message_to_similar_handle_received_method_name: static_lexical_only
  handler_architecture: domain_partitioned_by_many_protocol_handler_types

UNKNOWN:
  exact_generated_message_to_handler_dispatch
  exact_handler_to_storage_controller_mutation_edge
  common_global_inbound_dispatcher
  runtime_object_identity
  runtime_message_delivery
```

## Next safe static work

While PR #475 owns the physical native-login/worldmap runtime lane, the highest-value independent S2 work is:

```text
1. Player inbound QMeta/dispatch graph
   TPlayerProtocolMessageHandler
   -> PlayerDataCurrent / PlayerState / PlayerInventory / PlayerSkills
   -> static TPlayerData ownership/mutation edge

2. Creature inbound QMeta/dispatch graph
   TCreatureProtocolMessageHandler
   -> CreatureData / CreatureHealth / CreatureUpdate / MoveCreature
   -> static TCreatureStorage ownership/mutation edge

3. Container inbound QMeta/dispatch graph
   TContainerProtocolMessageHandler
   -> Container / Create / Change / DeleteInContainer
   -> static TContainerStorage ownership/mutation edge

4. Chat inbound QMeta/dispatch graph
   TChatProtocolMessageHandler
   -> Talk / Channels / ChannelEvent / PrivateChannel
   -> chat storage/controller edge
```

These are static exact-file tasks and do not need to consume the serialized physical runtime. Worldmap semantics and native-login runtime propagation remain with #475.
