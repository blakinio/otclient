---
task_id: OTC-20260818-track-a-s5-container-inbound-static
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
source_pr: 518
source_final_head: 9604ba9ab63a6a8017adc712ce4b3a0d1519521d
promotion_decision: ACCEPT_BOUNDED_PARTIAL
ownership_release_state: released
---

# Result

S5 reused only already-sanitized exact-build evidence and recovered exact container receive/handler/storage QMeta boundaries without downloading or executing the official client.

## Promoted facts

```text
TProtocolMessageQueue
  staticMetaObject 0x3085b60
  qt_static_metacall 0xdf5fe0
  355 methods / 192 signals
  62 receivedContainerMessage
  64 receivedCreateInContainerMessage
  65 receivedChangeInContainerMessage
  66 receivedDeleteInContainerMessage

TContainerProtocolMessageHandler
  staticMetaObject 0x3084fe0
  qt_static_metacall 0xd1e000
  35 methods / 11 signals
  14 handleContainerMessage
  18 handleCreateInContainerMessage
  16 handleChangeInContainerMessage
  17 handleDeleteInContainerMessage

TContainerStorage
  primary vptr 0x308a1a0
  staticMetaObject 0x308e720
  qt_static_metacall 0xd15af0
  0 containerUpdated
  1 containerRemoved
  2 manualSortModeChanged
```

S1 exact type information additionally proves four `TProtocolMessageQueue::registerServerMessage<T>` instantiations accepting queue member pointers typed for the exact corresponding `const GameserverMessageX&` message types.

## Evidence boundary

```yaml
REGISTERED_MEMBER_POINTER_EQUALS_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
QUEUE_SIGNAL_TO_CONTAINER_HANDLER_CONNECTION: UNKNOWN
CONTAINER_HANDLER_TO_STORAGE_MUTATION: UNKNOWN
RUNTIME_CONTAINER_DELIVERY: NOT_OBSERVED
```

Matched names are not promoted into call/connection edges without retained connection/dataflow evidence.

## Producer provenance

```text
S5 reuse run/job 32122620894 / 95666177103
artifact 9319111338
artifact digest sha256:0e92295e1486540cf82233bdf7eb1c24b9c15c585f815f52a0847b340d4ee745
historical QMeta source run/job 31790507112 / 94736106350
historical log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70
S1 artifact 9315562574
S1 artifact digest sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

## Source validation

```text
CI 32123671471 = SUCCESS
Track A governance 32123671344 = SUCCESS
reviews = 0
unresolved review threads = 0
source branch behind main = 0
```

Runtime E2E is `NOT_APPLICABLE`: static exact-evidence reuse only. S5 did not access Synology/X11/process memory, credentials, login or gameplay and did not observe/mutate PR #475 runtime.

Former task ownership is released after promotion merge.
