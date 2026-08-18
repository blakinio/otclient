# Track A S7 — inventory/equipment static boundaries

Task: `OTC-20260818-track-a-s7-inventory-equipment-static`  
Researcher PR: `#529`  
Execution: GitHub-hosted exact-evidence reuse only, `runtime_access: none`

## Executive result

S7 proves the exact QMeta ownership boundaries for the three core inbound inventory message families and corrects an important architectural assumption:

```text
GameserverMessageSetInventory
GameserverMessageDeleteInventory
GameserverMessagePlayerInventory
        ↓
TProtocolMessageQueue received* signals
        ↓
[connection edge still UNKNOWN]
        ↓
TContainerProtocolMessageHandler handle* methods
        ↓
[mutation edge still UNKNOWN]
        ↓
TInventoryContainer / inventoryChanged
        ↓
[UI connection still UNKNOWN]
        ↓
TPlayerInventoryAndStatusController / onInventoryChanged
```

The matching inventory handle methods are **not** QMeta-owned by `TPlayerProtocolMessageHandler`; they belong to `tibia::container::TContainerProtocolMessageHandler`.

## Provenance

```text
S7 discriminator
run      32138692915
artifact 9324985568
digest   sha256:16b94a26815abcebe049f9e4731d3e1dd19675e4b981665592222358de32286d

historical exhaustive QMeta source
run 31790507112
job 94736106350
source head 9afdc76ca6fe238742f270e22d8ecf4abe5ba9a2
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70

S1 exact type/name artifact
run 32112814216
artifact 9315562574
digest sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

Exact client represented by the retained evidence:

```text
version 15.32.df7b29
size    51965216
sha256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

No new official-client bytes were obtained or executed by S7.

## FACT — queue receive surfaces

```text
tibia::protocol::TProtocolMessageQueue
staticMetaObject    0x3085b60
qt_static_metacall  0xdf5fe0
methods             355
signals             192
```

Exact inventory receive signals:

```text
40  receivedSetInventoryMessage
67  receivedDeleteInventoryMessage
117 receivedPlayerInventoryMessage
```

All three indices are within the exact signal prefix. Classification: **FACT**.

## FACT — actual inventory handler owner

The exhaustive QMeta corpus places all three corresponding `handle*Message` methods in:

```text
tibia::container::TContainerProtocolMessageHandler
staticMetaObject    0x3084fe0
qt_static_metacall  0xd1e000
methods             35
signals             11
```

Exact methods:

```text
11 handleSetInventoryMessage
12 handleDeleteInventoryMessage
13 handlePlayerInventoryMessage
```

Classification: **FACT** for class ownership, indices and names.

## DISPROVEN at QMeta ownership boundary — `TPlayerProtocolMessageHandler`

The exact QMeta record for:

```text
tibia::game::TPlayerProtocolMessageHandler
staticMetaObject    0x30852a0
qt_static_metacall  0xd1a920
methods             22
signals             22
```

contains movement/rotation/tactics/world/game-action signals but none of:

```text
handleSetInventoryMessage
handleDeleteInventoryMessage
handlePlayerInventoryMessage
```

Therefore:

```yaml
TPLAYERPROTOCOLMESSAGEHANDLER_DIRECT_QMETA_INVENTORY_HANDLE_OWNERSHIP: DISPROVEN
```

This does not claim `TPlayerProtocolMessageHandler` has no non-QMeta relationship to inventory state; only direct QMeta ownership of those methods is disproven.

## FACT — inventory state object QMeta

```text
tibia::container::TInventoryContainer
staticMetaObject    0x309a960
qt_static_metacall  0xd15cf0
methods             1
signals             1

0 inventoryChanged [signal]
```

Classification: **FACT** for the QMeta surface only.

## FACT — inventory/status UI controller QMeta

```text
tibia::gamewindow::TPlayerInventoryAndStatusController
staticMetaObject    0x2f6e440
qt_static_metacall  0xd8cef0
methods             39
signals             14
```

The signal prefix is:

```text
0  inventoryMinimizedChanged
1  soulpointsChanged
2  capacityChanged
3  playerStatesChanged
4  blessingChanged
5  chaseModeChanged
6  secureModeEnabledChanged
7  pvpModeChanged
8  exportModeButtonEnableChanged
9  showCapacityWarning
10 gamesessionDisconnected
11 dualWieldingChanged
12 showPlayerStatesInBarChanged
13 publishGameAction
```

Relevant downstream slots include:

```text
18 onPlayerCreatureAdded
19 onPlayerDataChanged
20 onInventoryChanged
21 onSlotClicked
22 onSlotEntered
23 onSlotExited
24 onSlotStartDrag
25 onSlotDragDropped
26 onSlotTargetSelected
29 onInventoryOptionsChanged
```

This strongly identifies the controller as a consumer/presenter of inventory/player state, but the concrete `TInventoryContainer::inventoryChanged -> controller::onInventoryChanged` connection is not retained in the current evidence set and remains UNKNOWN.

## FACT — typed queue registration contracts

S1 artifact `9315562574` contains exact generated template symbols:

```text
TProtocolMessageQueue::registerServerMessage<GameserverMessageSetInventory>
TProtocolMessageQueue::registerServerMessage<GameserverMessageDeleteInventory>
TProtocolMessageQueue::registerServerMessage<GameserverMessagePlayerInventory>
```

Their signatures encode a `TProtocolMessageQueue` member-function pointer accepting the corresponding `const T&`. This proves each registration **type contract**.

The concrete member-pointer value used at each registration call is not retained. Therefore:

```text
GameserverMessageSetInventory -> receivedSetInventoryMessage
GameserverMessageDeleteInventory -> receivedDeleteInventoryMessage
GameserverMessagePlayerInventory -> receivedPlayerInventoryMessage
```

is `INFERENCE_HIGH_NOT_DIRECTLY_PROVEN`, not FACT.

## Retained UNKNOWNs

```yaml
QUEUE_SIGNAL_TO_CONTAINER_HANDLER_CONNECTION: UNKNOWN
CONTAINER_HANDLER_TO_INVENTORY_MUTATION: UNKNOWN
INVENTORY_CHANGED_TO_UI_CONTROLLER_CONNECTION: UNKNOWN
RUNTIME_INVENTORY_DELIVERY: NOT_OBSERVED
```

No matched names are promoted into a QObject/direct-call edge without a connection or call-dataflow discriminator.

## Safety / non-overlap

```text
new official-client bytes = false
client execution          = false
runtime access            = none
Synology/X11/VNC          = false
process memory            = false
credentials/login         = false
gameplay                  = false
PR #528 runtime touched   = false
PR #475 runtime touched   = false
PR #302 modified          = false
```

Physical E2E is `NOT_APPLICABLE` for this static evidence-reuse task.
