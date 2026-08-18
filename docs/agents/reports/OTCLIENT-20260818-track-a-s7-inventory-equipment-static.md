# OTCLIENT Track A — S7 inventory/equipment static report

## Decision candidate

`ACCEPT_BOUNDED_PARTIAL`.

S7 proves the exact static QMeta boundaries for three core inventory message families and corrects handler ownership without using runtime or new official-client bytes.

## Exact promoted candidates

```text
TProtocolMessageQueue
  40  receivedSetInventoryMessage
  67  receivedDeleteInventoryMessage
  117 receivedPlayerInventoryMessage

TContainerProtocolMessageHandler
  11 handleSetInventoryMessage
  12 handleDeleteInventoryMessage
  13 handlePlayerInventoryMessage

TInventoryContainer
  QMeta 0x309a960 / qt_static_metacall 0xd15cf0
  0 inventoryChanged [signal]

TPlayerInventoryAndStatusController
  QMeta 0x2f6e440 / qt_static_metacall 0xd8cef0
  39 methods / 14 signals
  20 onInventoryChanged
```

## Important correction

The exact `TPlayerProtocolMessageHandler` QMeta (`0x30852a0`, `0xd1a920`, 22 methods / 22 signals) contains none of the three inventory `handle*Message` methods.

Therefore direct QMeta ownership is:

```text
inventory inbound handler = TContainerProtocolMessageHandler
```

not `TPlayerProtocolMessageHandler`.

## Registration type contracts

S1 exact artifact `9315562574` retains `TProtocolMessageQueue::registerServerMessage<T>` symbols for:

```text
GameserverMessageSetInventory
GameserverMessageDeleteInventory
GameserverMessagePlayerInventory
```

The concrete registered member pointer is not retained, so suffix-matched message→received-signal identity remains high inference rather than FACT.

## Still UNKNOWN

```text
TProtocolMessageQueue received* -> TContainerProtocolMessageHandler handle*
TContainerProtocolMessageHandler -> TInventoryContainer mutation
TInventoryContainer::inventoryChanged -> TPlayerInventoryAndStatusController::onInventoryChanged
runtime inventory delivery
```

## Provenance

```text
S7 run      32138692915
artifact    9324985568
digest      sha256:16b94a26815abcebe049f9e4731d3e1dd19675e4b981665592222358de32286d
QMeta source 31790507112 / 94736106350
S1 artifact 9315562574
```

## Isolation

No new client bytes or execution, no Synology/X11/VNC/process memory, no credentials/login/gameplay, no PR #528/#475 runtime observation or mutation, and no PR #302 modification.
