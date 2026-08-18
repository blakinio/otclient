# Track A S1 unfiltered static census — result

Task: `OTC-20260818-track-a-s1-unfiltered-static-census`  
PR: `#509`  
Execution: `github_hosted`, `runtime_access: none`  
Exact client: `15.32.df7b29` / `51965216` / `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## Result

The bounded exact-file producer completed successfully without launching or observing the official client:

```text
run      32112814216
job      95635760592
result   SUCCESS
artifact 9315562574
sha256   583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

The raw compressed/unpacked official client was deleted before artifact upload. The artifact contains sanitized text/JSON only. No Synology, X11/VNC, process memory, credential/session value, login, gameplay, packet capture or PR #475 runtime surface was accessed.

## FACT — exhaustive generated-message denominator

Fresh exact-build census:

```text
PROTOCOL_MESSAGE_TOTAL=349
CLIENT_TO_SERVER=160
SERVER_TO_CLIENT=189
```

The fresh lists are byte-for-byte identical to the independent sanitized #473 control artifact (`run 32022209943`, artifact `9285763750`):

```text
protocol-all.txt
sha256 55f7cf2d6d4a63df6e24b8b156e38f1a2a64a9d6394357aa914661ab48fd983b

protocol-client-to-server.txt
sha256 621ecb7aa1a62aae559e8d793d1aebe9289d84811bc43c4339a7153458b553f0

protocol-server-to-client.txt
sha256 e642f661546c2e6e89ddcd77ac5e8aa9cd517408a309f95a3a367af943550d96
```

The complete 160/189 registries are persisted beside this report. The old 98-message capability-regex subset is therefore conclusively not an exhaustive protocol denominator.

## FACT — complete `received*Message` string denominator

The broader producer selector retained `542` candidate method strings, but full review split that set rather than calling all 542 inbound handlers:

```text
handle*     149
received*   189
on*         204
TOTAL       542
```

The exact result that matters for the inbound S1 denominator is:

```text
GENERATED_SERVER_MESSAGES=189
RECEIVED_MESSAGE_METHOD_STRINGS=189
EXACT_STEM_MATCHES=188
NAMING_VARIANTS=1
```

The complete 189-method receive surface is persisted in `received-message-methods.txt`.

For 188 entries the mapping obtained by removing `GameserverMessage` and `received...Message` wrappers is exactly equal. The sole name variant is:

```text
GameserverMessageTrackQuestFlags
receivedTrackedQuestFlagsMessage
```

The binary also contains `handleTrackedQuestFlagsMessage` and `onTrackedQuestFlagsChanged`.

Presence and denominator counts are **FACT**. The apparent one-to-one generated-message ↔ receive-method naming alignment is **INFERENCE_STATIC_LEXICAL_ONLY** until exact static dispatch/dataflow proves the edge.

## FACT — protocol-handler type/code surface

The fresh exact binary produced:

```text
148 relevant demangled protocol/storage/session/data types in the producer artifact
51 interesting strings with direct executable code xrefs
52 total retained direct code-to-string xrefs
47 distinct *ProtocolMessageHandler class names with direct code-to-class-string xrefs
```

Examples:

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
tibia::trade::TPlayerTradeProtocolMessageHandler
tibia::worldmap::TWorldmapProtocolMessageHandler
```

All 47 direct class-string xrefs are persisted in `protocol-handler-code-xrefs.tsv`. These xrefs prove exact executable references to the class-name strings. They do **not** prove that the referring instruction is the semantic message dispatcher.

The many domain-specific handler types prove a partitioned native handler **type surface**. They do not prove or disprove a shared upstream dispatcher/queue that routes into those handlers; that remains `UNKNOWN`.

## FACT — current-main exact-build anchors still resolve

The repository's relocation-aware resolver re-resolved every configured exact-build target uniquely:

```text
TGameClient                     primary vptr 0x3076908
TGameserverGameSession          primary vptr 0x3078ba0
TPlayerProtocolMessageHandler   primary vptr 0x308a008
TPlayerData                     primary vptr 0x308ca70
TContainerStorage               primary vptr 0x308a1a0
TCreatureStorage                primary vptr 0x308d078
TWorldmapProtocolMessageHandler primary vptr 0x30871d8
```

This is exact-file structural evidence only; no current runtime instance is claimed.

## High-value non-worldmap lexical correlations

These are name-surface correlations only, not proven call edges.

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

## UNKNOWN — exact inbound dispatch graph

This task does not prove:

```text
GameserverMessageX -> exact concrete handler function
receivedXMessage -> exact concrete handler owner
handler -> exact storage/controller mutation
one global/common inbound dispatcher
runtime delivery or causal state mutation
```

The producer deliberately reports `semantic_common_inbound_dispatcher = UNKNOWN`.

The direct class-string xrefs occur in several address clusters and are compatible with generated Qt metaobject/metacast-related code, but that role is not promoted without a bounded instruction/control-flow discriminator.

## Diagnostic family-bucket correction

The producer emitted convenience lexical family buckets. They are **not promoted** because naive substring rules can create false grouping, for example `Mark` inside `Market` or `row` inside `Browse`. Exact generated names, received method names, class types and xrefs are the durable evidence.

## Ranked non-conflicting S2 frontiers

While PR #475 owns the physical native-login/worldmap runtime lane, the best next static frontiers are:

1. `TPlayerProtocolMessageHandler` QMeta/dispatch graph for `PlayerDataCurrent`, `PlayerState`, `PlayerInventory`, `PlayerSkills`, followed by the static edge into `TPlayerData` where provable.
2. `TCreatureProtocolMessageHandler` dispatch graph for `CreatureData/Health/Update/MoveCreature`, followed by the static edge into `TCreatureStorage` where provable.
3. `TContainerProtocolMessageHandler` dispatch graph for `Container/Create/Change/DeleteInContainer`, followed by the static edge into `TContainerStorage` where provable.
4. `TChatProtocolMessageHandler` graph for `Talk/Channels/ChannelEvent/Open/Close/PrivateChannel`, followed by chat-storage/controller ownership where provable.

Worldmap semantic/runtime work remains excluded because PR #475 currently owns that physical frontier. Login/session runtime propagation is also not selected as the immediate follow-up while #475 is actively working the native world-entry chain.

## Classification

```yaml
GENERATED_MESSAGE_DENOMINATOR: FACT
COMPLETE_160_OUTBOUND_REGISTRY: FACT
COMPLETE_189_INBOUND_REGISTRY: FACT
COMPLETE_189_RECEIVED_METHOD_STRING_SURFACE: FACT_STRING_PRESENCE
188_EXACT_STEM_MATCHES_PLUS_1_NAMING_VARIANT: FACT_STRING_COMPARISON
GENERATED_MESSAGE_TO_RECEIVED_METHOD_EDGE: INFERENCE_STATIC_LEXICAL_ONLY
PROTOCOL_HANDLER_TYPE_PRESENCE: FACT
DIRECT_CODE_TO_HANDLER_CLASS_STRING_XREFS: FACT
MESSAGE_TO_CONCRETE_HANDLER_DISPATCH: UNKNOWN
RECEIVED_METHOD_TO_HANDLER_OWNER: UNKNOWN
HANDLER_TO_STORAGE_CONTROLLER_EDGE: UNKNOWN
COMMON_UPSTREAM_INBOUND_DISPATCHER: UNKNOWN
RUNTIME_BEHAVIOR: NOT_OBSERVED
```
