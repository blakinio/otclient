# Track A S7 inventory/equipment static — coordinator promotion

Date: 2026-08-18  
Source Draft: PR #529  
Source final head: `ccf8d5c98d23e83918ad5e2f8880adc84dd81fef`  
Trusted promotion base: `main@066a5ba8b1811ef61d3aa8ac2ff3fc3601fe7b9d`  
Decision: **ACCEPT_BOUNDED_PARTIAL**

## Promoted exact-build boundaries

```text
TProtocolMessageQueue
  staticMetaObject 0x3085b60
  qt_static_metacall 0xdf5fe0
  355 methods / 192 signals
  40  receivedSetInventoryMessage
  67  receivedDeleteInventoryMessage
  117 receivedPlayerInventoryMessage

TContainerProtocolMessageHandler
  staticMetaObject 0x3084fe0
  qt_static_metacall 0xd1e000
  35 methods / 11 signals
  11 handleSetInventoryMessage
  12 handleDeleteInventoryMessage
  13 handlePlayerInventoryMessage

TInventoryContainer
  staticMetaObject 0x309a960
  qt_static_metacall 0xd15cf0
  1 method / 1 signal
  0 inventoryChanged [signal]

TPlayerInventoryAndStatusController
  staticMetaObject 0x2f6e440
  qt_static_metacall 0xd8cef0
  39 methods / 14 signals
  20 onInventoryChanged
```

## Architectural correction

The exact `tibia::game::TPlayerProtocolMessageHandler` QMeta record is `0x30852a0`, `qt_static_metacall 0xd1a920`, with 22 methods / 22 signals. It contains none of `handleSetInventoryMessage`, `handleDeleteInventoryMessage`, or `handlePlayerInventoryMessage`.

Therefore:

```yaml
INVENTORY_HANDLE_QMETA_OWNER: FACT:TContainerProtocolMessageHandler
TPLAYERPROTOCOLMESSAGEHANDLER_DIRECT_INVENTORY_HANDLE_OWNERSHIP: DISPROVEN_QMETA
```

This classification is limited to direct QMeta ownership; it does not disprove other non-QMeta relationships between player protocol state and inventory.

## Typed registration surface

S1 artifact `9315562574` contains exact `TProtocolMessageQueue::registerServerMessage<T>` template symbols for:

```text
GameserverMessageSetInventory
GameserverMessageDeleteInventory
GameserverMessagePlayerInventory
```

Each signature accepts a `TProtocolMessageQueue` member-function pointer taking `const T&`. The concrete member-pointer value used at each registration invocation is not retained.

Therefore:

```yaml
REGISTERED_MEMBER_POINTER_EQUALS_SUFFIX_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
```

## Retained UNKNOWNs

```yaml
QUEUE_SIGNAL_TO_CONTAINER_HANDLER_CONNECTION: UNKNOWN
CONTAINER_HANDLER_TO_INVENTORY_MUTATION: UNKNOWN
INVENTORY_CHANGED_TO_UI_CONTROLLER_CONNECTION: UNKNOWN
RUNTIME_INVENTORY_DELIVERY: NOT_OBSERVED
```

Matching names and the presence of `TInventoryContainer::inventoryChanged` / controller `onInventoryChanged` are not promoted into connection/dataflow edges without direct retained evidence.

## Evidence provenance

```text
S7 discriminator
run 32138692915
artifact 9324985568
digest sha256:16b94a26815abcebe049f9e4731d3e1dd19675e4b981665592222358de32286d

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

## Source exact-head validation

```text
CI 32139099029 = SUCCESS
Track A governance 32139098562 = SUCCESS
reviews = 0
unresolved review threads = 0
main freshness = 0 behind
```

No new official-client bytes, client execution, physical runtime, Synology/X11/VNC, process-memory access, credentials, login or gameplay were used. PR #528 and #475 runtime surfaces remained untouched. Physical E2E is `NOT_APPLICABLE` for this static exact-evidence task.
