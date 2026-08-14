# QMeta protocol-handler census and dispatch map — 2026-08-14

## Scope

Track A / `official-client-re` only. Subject: exact official native Linux Tibia client SHA256:

```text
e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Complete relocation-backed protocol-handler census

Primary evidence:

```text
workflow: .github/workflows/tibia-official-client-re-qmeta-protocol-handler-census-v2.yml
head: 8cbd26fead9175b82d28460590dec4eaeed58d8f
run: 31790619327
job: 94736463933
runner: synology-otclient-01
result: SUCCESS
```

The v2 census removed the incorrect 0x40-alignment assumption from the first census and instead tests every relocation slot as a possible QMeta record `+0x08` field. A record is accepted only when `+0x08/+0x10/+0x18/+0x28` are `R_X86_64_RELATIVE`, `+0x18` points into an executable segment, `+0x08` decodes as the proven `(offset,length)` Qt string table, its first string contains `ProtocolMessageHandler`, and the `+0x10` metadata table has revision 13.

### FACT — all 47 protocol-handler classes are recovered as concrete QMeta records

The successful census reports `HANDLER_RECORD_COUNT=47`, exactly matching the earlier independent literal inventory count of 47 `*ProtocolMessageHandler` classes.

Examples:

```text
TLoginProtocolMessageHandler:       static_metacall +0xcf2aa0, methods 7
TChatProtocolMessageHandler:        static_metacall +0xd05f20, methods 13
TContainerProtocolMessageHandler:   static_metacall +0xd1e000, methods 35
TCreatureProtocolMessageHandler:    static_metacall +0xd12510, methods 0
TPlayerProtocolMessageHandler:      static_metacall +0xd1a920, methods 22
TGameProtocolMessageHandler:        static_metacall +0xd20e10, methods 25
TMarketProtocolMessageHandler:      static_metacall +0xdc4a80, methods 13
TNPCTradeProtocolMessageHandler:    static_metacall +0xdec960, methods 12
TPlayerTradeProtocolMessageHandler: static_metacall +0xded1d0, methods 9
TQuestLogProtocolMessageHandler:    static_metacall +0xde9270, methods 5
TEffectProtocolMessageHandler:      static_metacall +0xd338d0, methods 2
TWorldmapProtocolMessageHandler:    static_metacall +0xdf2a60, methods 14
```

The run also recovers concrete QMeta records for VIP, Friends, Minimap, Sound, Daily Reward, Prey, Imbuing, Cyclopedia, Store, Team Finder, Network Quality, Skill Wheel and the remaining protocol-handler classes.

## Creature, Player and GameProtocol separation

`TCreatureProtocolMessageHandler` has a valid relocation-backed QMeta record but `method_count=0`, and direct static-metacall disassembly shows `+0xd12510` is only `ret`.

**FACT:** this exact class exposes no own QMeta methods. The earlier expectation that creature inbound handlers could simply be enumerated here is rejected. Creature-state messages remain proven present in the exact binary, but their routing must be recovered through another protocol layer/direct generated-code path.

`TPlayerProtocolMessageHandler` has exactly 22 QMeta methods:

```text
0 sendEnterWorld
1 sendGoNorth
2 sendGoEast
3 sendGoSouth
4 sendGoWest
5 sendStop
6 sendCancel
7 sendGoNorthEast
8 sendGoSouthEast
9 sendGoSouthWest
10 sendGoNorthWest
11 sendGoPath
12 sendRotateNorth
13 sendRotateEast
14 sendRotateSouth
15 sendRotateWest
16 sendSetTactics
17 worldEntered
18 showSelectOutfitDialog
19 showConfigureCreaturePodiumDialog
20 showHirelingNameChangeConfiguration
21 publishGameAction
```

A separate exact-binary run:

```text
workflow: .github/workflows/tibia-official-client-re-player-gameprotocol-map.yml
head: 86876ec3938001d2385cdb9ab6a8067ea2c4be66
run: 31790730334
job: 94736807191
result: SUCCESS
```

also decodes all 25 `TGameProtocolMessageHandler` methods:

```text
sendEnterWorldMessage
sendInspectObject
sendClientDetails
sendSetClientOptions
sendSetVocation
sendStartOfflineTraining
loginSuccess
sessionEndInformation
requestOpenDeathDialog
deadMessage
settingHintsFromServer
worldTypeReceived
inspectObjectDataReceived
requestOpenInspectPlayerDialog
requestOpenOutfitMemorialDialog
requestShowMultiOfflineTrainingDialog
handleLoginSuccessMessage
handleSessionEndInformationMessage
handleSessionDumpStartMessage
handlePendingStateEnteredMessage
handleDeadMessage
handleInspectionListMessage
handleOutfitMemorialMessage
handleShowMultiOfflineTrainingDialogMessage
emitSendEnterWorldMessage
```

**FACT:** `TGameProtocolMessageHandler` is a login/session/death/inspection/general-game surface, not the missing current-player/creature-state handler group. This narrows creature/player-current routing away from this QMeta class.

## Exact Player movement/action dispatch map

Primary evidence:

```text
workflow: .github/workflows/tibia-official-client-re-player-jumptable-map.yml
head: 87a8f57261fef8bbada71502b11d1405ff1be345
run: 31790885910
job: 94737284156
runner: synology-otclient-01
result: SUCCESS
jump table: 0x1d713d0
```

All 22 QMeta methods have distinct exact case entries. High-value movement/action cases are:

```text
sendEnterWorld:    +0xd1acd8 -> common tail +0xd1abc0
sendGoNorth:       +0xd1aca8 -> common tail +0xd1abc0
sendGoEast:        +0xd1af10 -> common tail +0xd1abc0
sendGoSouth:       +0xd1aee0 -> common tail +0xd1abc0
sendGoWest:        +0xd1ae20 -> common tail +0xd1abc0
sendStop:          +0xd1ad08 -> common tail +0xd1abc0
sendCancel:        +0xd1add0 -> common tail +0xd1abc0
sendGoNorthEast:   +0xd1ada0 -> common tail +0xd1abc0
sendGoSouthEast:   +0xd1ad70 -> common tail +0xd1abc0
sendGoSouthWest:   +0xd1ae50 -> common tail +0xd1abc0
sendGoNorthWest:   +0xd1aeb0 -> common tail +0xd1abc0
sendGoPath:        +0xd1ae80 -> common tail +0xd1abc0
sendRotateNorth:   +0xd1af70 -> common tail +0xd1abc0
sendRotateEast:    +0xd1af40 -> common tail +0xd1abc0
sendRotateSouth:   +0xd1abc8
sendRotateWest:    +0xd1ab98
sendSetTactics:    +0xd1abf8
publishGameAction: +0xd1ac78 -> common tail +0xd1abc0
```

Signals/dialog entries include:

```text
worldEntered:                        +0xd1ad50 -> QMetaObject::activate
showSelectOutfitDialog:              +0xd1ad38 -> QMetaObject::activate
showConfigureCreaturePodiumDialog:   +0xd1ae00 -> QMetaObject::activate
showHirelingNameChangeConfiguration: +0xd1ac28
```

The common `+0xd1abc0` tail is a concrete convergence point for most movement/send cases. Its exact serializer/router semantics require separate disassembly before calling it a packet sender.

## Chat and Container exact dispatch mapping

Primary mapping evidence:

```text
workflow: .github/workflows/tibia-official-client-re-qmeta-jumptable-map-v2.yml
head: cf09cae9d6507eea254dc1830bee4caebff7448f
run: 31790639503
job: 94736526900
runner: synology-otclient-01
result: SUCCESS
```

### FACT — Chat inbound handlers have exact case entries

```text
handleTalkMessage:             case +0xd05fa0 -> direct tail +0xe460f0
handleMessageMessage:          case +0xd05fb0 -> direct tail +0xe3a010
handleOpenChannelMessage:      case +0xd05fc0 -> direct tail +0xe38c60
handleOpenOwnChannelMessage:   case +0xd05fd0 -> direct tail +0xe38ea0
handleCloseChannelMessage:     case +0xd06060 -> no bounded direct-tail claim
handleChannelsMessage:         case +0xd06080 -> direct tail +0xe47260
handlePrivateChannelMessage:   case +0xd06090 -> direct tail +0xe2ed00
handleChannelEventMessage:     case +0xd060a0 -> direct tail +0xe343a0
handleNpcTalkPartersMessage:   case +0xd06040 -> direct tail +0xe390e0
```

### FACT — Container inbound handlers have exact case entries

```text
handleSetInventoryMessage:                 case +0xd1e5c0 -> +0xe6f2f0
handleDeleteInventoryMessage:              case +0xd1e520 -> +0xe5f9a0
handlePlayerInventoryMessage:              case +0xd1e510 -> +0xe50c30
handleContainerMessage:                    case +0xd1e380 -> +0xe61360
handleCloseContainerMessage:               case +0xd1e360 -> no bounded direct-tail claim
handleChangeInContainerMessage:            case +0xd1e350 -> +0xe5fb60
handleDeleteInContainerMessage:            case +0xd1e3c0 -> +0xe5fcd0
handleCreateInContainerMessage:            case +0xd1e3b0 -> +0xe5fe40
handleObjectInfoMessage:                   case +0xd1e3a0 -> +0xe52f80
handleStashMessage:                        case +0xd1e390 -> +0xe51c20
handleShowMessageDialogMessage:            case +0xd1e4f0 -> +0xe56d60
handleSpecialContainersAvailableMessage:   case +0xd1e4e0 -> +0xe51730
handleDepotSearchResultMessage:            case +0xd1e4d0 -> +0xe51d90
handleDepotSearchDetailListMessage:        case +0xd1e4b8 -> +0xe5ffb0
handleCloseDepotSearchMessage:             case +0xd1e1a8 -> +0x4dedc0
```

### FACT — GameEvent and Effect simple dispatches

```text
TGameEventProtocolMessageHandler:
  publishGameAction       case +0xd20848 -> QMetaObject::activate
  handleGameEventMessage  case +0xd2080d -> direct tail +0x8374e0

TEffectProtocolMessageHandler:
  handleRemoveGraphicalEffectMessage case +0xd339a8
  handleGraphicalEffectsMessage       case +0xd338f4
```

## Research consequence

The executable QMeta surface is now concrete for Player movement/path/rotation, Chat inbound, Container inbound and broad protocol-handler class ownership. Current high-value next gates are:

1. disassemble and classify Player common tail `+0xd1abc0` without invoking it;
2. map exact `GameActionHandler` surfaces for `MoveObject`, `Attack`, `Follow`, `Talk` and `TradeObject`;
3. recover the non-QMeta creature-message routing path and player-current/player-data path;
4. recover selected argument layouts at proven Chat/Container handler entries.

No live client mutation, credentials, packet injection or new runtime attach were used in these static experiments.
