# Track A S9 — native action/control static catalogue

Task: `OTC-20260818-track-a-s9-action-control-static-census`  
Researcher PR: `#535`  
Execution: retained exact-build QMeta evidence only, `runtime_access: none`

## Executive result

The retained exact QMeta corpus exposes a broad native action layer sufficient to identify the principal control entry surfaces needed by the official-client RE programme.

```text
input / UI intent
      ↓
*GameActionHandler / movement intent / internal router       FACT surfaces
      ↓
player/feature protocol send boundary                       FACT surfaces where QMeta exposes it
      ↓
concrete per-action QObject/direct call and serialization    UNKNOWN unless separately proven
      ↓
runtime/server effect                                       NOT_OBSERVED by S9
```

S9 found **28** QMeta classes whose type names end in `GameActionHandler`.

## Movement / turn / stop / path — FACT

`TPlayerMovementIntentHandler`:

```text
QMeta 0x3085de0
qt_static_metacall 0xdc9220
19 methods / 18 signals

sendGoNorth/East/South/West
sendGoNorthEast/SouthEast/SouthWest/NorthWest
sendGoPath
sendRotateNorth/East/South/West
sendStop
sendCancel
sendFollowZero
requestTimedCallback
```

`TPlayerMovementGameActionHandler`:

```text
QMeta 0x3085260
qt_static_metacall 0xdc4060
3 methods / 2 signals
publishGameAction
sendCancel
handleGameAction
```

`TPlayerProtocolMessageHandler` exposes the corresponding protocol-facing QMeta signals:

```text
QMeta 0x30852a0
qt_static_metacall 0xd1a920
22 methods / 22 signals

sendEnterWorld
sendGoNorth/East/South/West
sendStop / sendCancel
sendGoNorthEast/SouthEast/SouthWest/NorthWest
sendGoPath
sendRotateNorth/East/South/West
sendSetTactics
worldEntered
```

The matching method names do not alone prove the exact object connection from movement intent to this protocol boundary.

## Attack / follow / creature interaction — FACT

`TCreaturesGameActionHandler`:

```text
QMeta 0x3085060
qt_static_metacall 0xd16340
13 methods / 13 signals

sendAttack
sendFollow
sendLookAtCreature
sendInspectPlayer
sendInviteToParty
sendJoinParty
sendRevokeInvitation
sendPassLeadership
sendLeaveParty
sendShareExperience
sendGreet
sendJoinAggression
```

## Use / use-with / object interaction — FACT

`TUseWithGameActionHandler`:

```text
QMeta 0x3085120
qt_static_metacall 0xdc4480
5 methods / 4 signals

startTargetSelection
publishGameAction
sendUseTwoObjects
sendUseOnCreature
handleGameAction
```

`TGenericGameActionHandler`:

```text
QMeta 0x3085020
qt_static_metacall 0xdcb990
31 methods / 12 signals

sendTurnObject
sendUseObject
sendLook
sendBrowseField
sendMoveObject
...
handleLookAction
handleUseAction
handleMoveUpAction
handleRotateAction
...
```

These exact method names cover the programme's static boundaries for use, use-with, use-on-creature, look, rotate and move-object.

## Container / equipment actions — FACT

`TContainerGameActionHandler`:

```text
QMeta 0x30850a0
qt_static_metacall 0xd1dac0
23 methods / 9 signals

sendMoveObject
sendEquipObject
sendStashAction
sendOpenDepotSearch
sendCloseDepotSearch
sendDepotSearchType
sendOpenParentContainer
sendDepotSearchRetrieve

handleMoveObjectGameAction
handleTryToEquipGameAction
...
```

## Chat / NPC-facing talk actions — FACT

`TChatGameActionHandler`:

```text
QMeta 0x30851a0
qt_static_metacall 0xcff5b0
38 methods / 11 signals

sendGetChanneList
sendJoinChannel
sendOpenChannel
sendPrivateChannel
sendCloseNPCChannel
sendLeaveChannel
sendInviteToChannel
sendExcludeFromChannel
sendGuildMessage
sendTalkMessage
publishGameAction
```

The class also contains exact slots for channel manipulation and talk variants, including `handleSendTalkChatMessageToNpcGameAction`.

## Player actions — FACT

`TPlayerGameActionHandler`:

```text
QMeta 0x3085160
qt_static_metacall 0xd1a230
8 methods / 8 signals

publishGameAction
sendMount
sendGetOutfit
sendSetOutfit
sendSetCreaturePodiumConfiguration
sendSetHirelingName
sendSetTactics
sendInspectPlayer
```

## Internal routing boundary — FACT

`TInternalGameActionRouter`:

```text
QMeta 0x3074b20
qt_static_metacall 0xd20600
4 methods / 2 signals

publishGameActionInternal
publishGameActionBetweenRouters
handleGameActionInternal
handleGameActionFromOtherRouter
```

This proves an exact native game-action routing surface, not the concrete routing relationship for every action family.

## Full action-handler denominator

The exact retained QMeta census contains 28 `*GameActionHandler` types spanning chat, container, creatures, VIP, daily reward, effects, exaltation, exiva, player, battle list, input actions, market, minimap, prey, quest log, quick loot, skill wheel, store, trade, tutorial and world map.

The full list is preserved in `result.json` and producer artifact `9325847070`.

## Retained UNKNOWNs

```yaml
ACTION_LAYER_TO_PROTOCOL_CONNECTION: UNKNOWN
PER_ACTION_PROTOCOL_TO_SERIALIZED_MESSAGE: UNKNOWN
PER_ACTION_RUNTIME_EFFECT: NOT_OBSERVED
```

The previously promoted generic P2 outbound chain does not by itself prove a specific action method's producer-to-wire provenance. S9 therefore does not equate a `send*` QMeta signal name with confirmed server execution.

## Static-lane terminal condition

```yaml
STATIC_ACTION_CONTROL_CATALOGUE: EXHAUSTED_FOR_RETAINED_QMETA
PRINCIPAL_STATE_SURFACES: CATALOGUED_BY_S1_TO_S8
PRINCIPAL_ACTION_SURFACES: CATALOGUED_BY_S9
NEXT_MEANINGFUL_PROOF_REQUIRES: EXACT_CODE_WINDOW_OR_LEGAL_RUNTIME
```

Further repeated QMeta/name scans would add breadth but not close the causal edges that remain material. The next useful work is dataflow/connection proof from exact code windows or physical runtime after the active owner permits it.

## Provenance

```text
S9 producer run 32140983838
artifact 9325847070
digest sha256:12ddebc9aa1ff73f96370091c50e33a6cf3bf7b37a4cf8bc7007175861c5491d
historical exact QMeta source 31790507112 / 94736106350
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70
```

## Isolation

No new official-client bytes or execution, no Synology/X11/VNC/process memory, no credentials/login/gameplay, and no PR #528/#475 runtime observation or mutation.
