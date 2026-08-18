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

## FACT — unfiltered inbound-oriented static surface

The fresh exact binary contains:

```text
542 inbound-oriented handle/received/on/process-style method strings
148 relevant demangled protocol/storage/session/data types in the producer artifact
51 interesting strings with direct executable code xrefs
52 total retained direct code-to-string xrefs
47 distinct *ProtocolMessageHandler class names with direct code-to-class-string xrefs
```

Examples of directly present handler classes include:

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

All 47 direct class-string xrefs are persisted in `protocol-handler-code-xrefs.tsv`. These xrefs prove exact code references to the class-name strings. They do **not** by themselves prove that the referring instruction is the semantic message dispatcher.

## FACT — current-main exact-build anchors still resolve

The repository's relocation-aware resolver re-resolved every configured exact-build target uniquely:

```text
TGameClient                    primary vptr 0x3076908
TGameserverGameSession         primary vptr 0x3078ba0
TPlayerProtocolMessageHandler  primary vptr 0x308a008
TPlayerData                    primary vptr 0x308ca70
TContainerStorage              primary vptr 0x308a1a0
TCreatureStorage               primary vptr 0x308d078
TWorldmapProtocolMessageHandler primary vptr 0x30871d8
```

This is exact-file structural evidence only; no current runtime instance is claimed.

## INFERENCE — generated message names align strongly with native receive surfaces

A deliberately name-only pass found an exact/broader lexical `handle*` / `received*` / related method surface for `188 / 189` generated server messages.

High-value non-worldmap examples:

```text
GameserverMessagePlayerDataCurrent
 -> receivedPlayerDataCurrentMessage

GameserverMessagePlayerState
 -> receivedPlayerStateMessage

GameserverMessagePlayerInventory
 -> handlePlayerInventoryMessage
 -> receivedPlayerInventoryMessage

GameserverMessageCreatureHealth
 -> receivedCreatureHealthMessage

GameserverMessageCreatureUpdate
 -> receivedCreatureUpdateMessage

GameserverMessageMoveCreature
 -> receivedMoveCreatureMessage

GameserverMessageCreateInContainer
 -> handleCreateInContainerMessage
 -> receivedCreateInContainerMessage

GameserverMessageChangeInContainer
 -> handleChangeInContainerMessage
 -> receivedChangeInContainerMessage

GameserverMessageDeleteInContainer
 -> handleDeleteInContainerMessage
 -> receivedDeleteInContainerMessage

GameserverMessageTalk
 -> handleTalkMessage
 -> receivedTalkMessage

GameserverMessageChannels
 -> handleChannelsMessage
 -> receivedChannelsMessage
```

These are **STATIC_LEXICAL_ASSOCIATIONS**, not proven call edges. The only generated name not matched by the automatic stem rule was:

```text
GameserverMessageTrackQuestFlags
```

The binary separately contains `handleTrackedQuestFlagsMessage`, `receivedTrackedQuestFlagsMessage` and `onTrackedQuestFlagsChanged`, so the difference is consistent with a naming variant (`Track` vs `Tracked`) but is not promoted to a direct message-handler FACT here.

## UNKNOWN — exact inbound dispatch graph

This task does not prove:

```text
GameserverMessageX -> exact concrete handler function
handler -> exact storage/controller mutation
one global/common inbound dispatcher
runtime delivery or causal state mutation
```

The producer deliberately reports `semantic_common_inbound_dispatcher = UNKNOWN`.

The direct class-string xrefs occur in several address clusters and are compatible with generated Qt metaobject/metacast-related code, but that role is not promoted without a bounded instruction/control-flow discriminator.

## Diagnostic family-bucket correction

The producer also emitted convenience lexical family buckets. They are **not promoted** because naive substring rules can create false grouping, for example `Mark` inside `Market` or `row` inside `Browse`. Exact generated names, method names, class types and xrefs are the durable evidence; future semantic grouping must be explicit or dependency-derived.

## Ranked non-conflicting S2 frontiers

The best next static frontiers that do not require or consume PR #475's physical runtime are:

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
UNFILTERED_INBOUND_METHOD_STRING_CENSUS: FACT
PROTOCOL_HANDLER_TYPE_PRESENCE: FACT
DIRECT_CODE_TO_HANDLER_CLASS_STRING_XREFS: FACT
MESSAGE_TO_SIMILAR_METHOD_NAME: INFERENCE_STATIC_LEXICAL_ONLY
MESSAGE_TO_CONCRETE_HANDLER_DISPATCH: UNKNOWN
HANDLER_TO_STORAGE_CONTROLLER_EDGE: UNKNOWN
COMMON_INBOUND_DISPATCHER: UNKNOWN
RUNTIME_BEHAVIOR: NOT_OBSERVED
```
