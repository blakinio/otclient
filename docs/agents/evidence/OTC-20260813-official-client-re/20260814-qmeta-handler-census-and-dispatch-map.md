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

The successful census reports:

```text
HANDLER_RECORD_COUNT=47
```

This exactly matches the earlier independent literal inventory count of 47 `*ProtocolMessageHandler` classes, providing a strong cross-check that the relocation-backed reconstruction covers the complete handler-class surface rather than a partial subset.

Each recovered record now has exact-version addresses for:

```text
record base
stringdata base
metadata base
static_metacall executable entry
extra/meta-types data pointer
method count
```

Examples:

```text
TLoginProtocolMessageHandler:      static_metacall +0xcf2aa0, methods 7
TChatProtocolMessageHandler:       static_metacall +0xd05f20, methods 13
TContainerProtocolMessageHandler:  static_metacall +0xd1e000, methods 35
TCreatureProtocolMessageHandler:   static_metacall +0xd12510, methods 0
TPlayerProtocolMessageHandler:     static_metacall +0xd1a920, methods 22
TGameProtocolMessageHandler:       static_metacall +0xd20e10, methods 25
TMarketProtocolMessageHandler:     static_metacall +0xdc4a80, methods 13
TNPCTradeProtocolMessageHandler:   static_metacall +0xdec960, methods 12
TPlayerTradeProtocolMessageHandler: static_metacall +0xded1d0, methods 9
TQuestLogProtocolMessageHandler:   static_metacall +0xde9270, methods 5
TEffectProtocolMessageHandler:     static_metacall +0xd338d0, methods 2
TWorldmapProtocolMessageHandler:   static_metacall +0xdf2a60, methods 14
```

The run also recovers concrete QMeta records for VIP, Friends, Minimap, Sound, Daily Reward, Prey, Imbuing, Cyclopedia, Store, Team Finder, Network Quality, Skill Wheel and the remaining protocol-handler classes.

### FACT — Creature and Player are structurally different

`TCreatureProtocolMessageHandler` has a valid relocation-backed QMeta record but reports:

```text
method_count=0
static_metacall=+0xd12510
```

Therefore this class exposes no own QMeta methods in this exact version. The earlier expectation that creature inbound handlers could simply be enumerated as QMeta methods on this class is rejected. Creature state still exists as explicit protocol messages in the binary, but the routing/handling path must be recovered through another layer (for example inherited/base dispatch, `TGameProtocolMessageHandler`, direct protobuf routing, or non-QMeta methods).

By contrast `TPlayerProtocolMessageHandler` has 22 own QMeta methods. Exact method order is:

```text
0  sendEnterWorld
1  sendGoNorth
2  sendGoEast
3  sendGoSouth
4  sendGoWest
5  sendStop
6  sendCancel
7  sendGoNorthEast
8  sendGoSouthEast
9  sendGoSouthWest
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

This is a direct structural action surface for movement/path/rotation and world-entry signalling. It does not yet claim safe runtime invocation or packet-layout details.

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

The v2 decoder maps each QMeta method index through the signed 32-bit jump table to its exact in-function case entry. Direct `E9 rel32` tail targets are reported only when the jump occurs before the next distinct case-entry boundary, fixing the first scanner's cross-case false-positive risk.

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

For `handleCloseChannelMessage`, the first unbounded scanner had incorrectly associated a later case's jump target. The bounded v2 result supersedes that claim and intentionally leaves its direct-tail target unassigned. The exact case entry `+0xd06060` remains proven.

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

The case entries themselves are exact QMeta dispatch facts. A direct-tail address is promoted only where the bounded block contains a direct near jump. No direct-tail claim is made for `handleCloseContainerMessage` because its block is not a simple direct-tail form.

### FACT — GameEvent and Effect simple dispatches

From the preceding static-metacall disassembly and method-index decode:

```text
TGameEventProtocolMessageHandler:
  index 0 publishGameAction       case +0xd20848 -> QMetaObject::activate
  index 1 handleGameEventMessage  case +0xd2080d -> direct tail +0x8374e0

TEffectProtocolMessageHandler:
  index 0 handleRemoveGraphicalEffectMessage  case +0xd339a8
  index 1 handleGraphicalEffectsMessage        case +0xd338f4
```

The Effect cases are currently promoted as exact case-entry addresses only; their logic is not assumed to be separate standalone tail functions.

## Research consequence

The previous broad `UNKNOWN` for Chat/Container executable handler offsets is now substantially resolved. We can instrument exact-version case entries or, where proven, direct-tail functions without relying on OCR or guessed message names.

The next high-value gates are:

1. decode `TPlayerProtocolMessageHandler +0xd1a920` jump table to exact movement/path/rotation send entries;
2. inspect all 25 `TGameProtocolMessageHandler` methods to determine whether current player/creature inbound state is routed there;
3. recover the non-QMeta creature-message routing path, because `TCreatureProtocolMessageHandler` itself has zero own methods;
4. recover selected Chat/Container protobuf/C++ argument layouts at the newly proven entries, starting with `handleTalkMessage`, `handleContainerMessage` and Create/Change/DeleteInContainer.

No live client mutation, credentials, packet injection or new runtime attach were used in these static experiments.
