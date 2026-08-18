---
task_id: OTC-20260818-track-a-s7-inventory-equipment-static
status: completed_bounded_partial
session_role: researcher_then_coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
execution_mode: github_only
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PHYSICAL_E2E_REQUIRED: false
source_pr: 529
source_final_head: ccf8d5c98d23e83918ad5e2f8880adc84dd81fef
promotion_decision: ACCEPT_BOUNDED_PARTIAL
ownership_release_state: released
---

# Result

S7 reused only already-sanitized exact-build/repository evidence and recovered the core inventory/equipment QMeta boundaries without touching runtime.

## Promoted facts

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

The exact `TPlayerProtocolMessageHandler` QMeta record (`0x30852a0`, `0xd1a920`, 22/22 signals) contains none of the three inventory `handle*Message` methods, so direct QMeta ownership there is disproven.

S1 exact artifact `9315562574` also proves `TProtocolMessageQueue::registerServerMessage<T>` type contracts for `GameserverMessageSetInventory`, `GameserverMessageDeleteInventory`, and `GameserverMessagePlayerInventory`.

## Retained boundaries

```yaml
REGISTERED_MEMBER_POINTER_EQUALS_SUFFIX_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
QUEUE_SIGNAL_TO_CONTAINER_HANDLER_CONNECTION: UNKNOWN
CONTAINER_HANDLER_TO_INVENTORY_MUTATION: UNKNOWN
INVENTORY_CHANGED_TO_UI_CONTROLLER_CONNECTION: UNKNOWN
RUNTIME_INVENTORY_DELIVERY: NOT_OBSERVED
```

## Provenance / validation

```text
S7 producer run 32138692915
artifact 9324985568
artifact digest sha256:16b94a26815abcebe049f9e4731d3e1dd19675e4b981665592222358de32286d

historical QMeta source 31790507112 / 94736106350
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70

S1 type artifact 9315562574
sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860

source CI 32139099029 = SUCCESS
source Track A governance 32139098562 = SUCCESS
reviews = 0
unresolved review threads = 0
```

No new client bytes/client execution, Synology/X11/VNC/process-memory access, credentials, login or gameplay. PR #528 and PR #475 runtime surfaces were not observed or mutated; PR #302 was not modified.
