# Track A S5 container inbound static — coordinator promotion

Date: 2026-08-18  
Source Draft: PR #518  
Source final head: `9604ba9ab63a6a8017adc712ce4b3a0d1519521d`  
Trusted promotion base: `main@5afdfbde6c6e5b5bb8defe6c3eb2e36d3469bd0e`  
Decision: **ACCEPT_BOUNDED_PARTIAL**

## Promoted exact-build boundaries

```text
TProtocolMessageQueue
  staticMetaObject 0x3085b60
  qt_static_metacall 0xdf5fe0
  method_count 355
  signal_count 192
  signal 62 receivedContainerMessage
  signal 64 receivedCreateInContainerMessage
  signal 65 receivedChangeInContainerMessage
  signal 66 receivedDeleteInContainerMessage

TContainerProtocolMessageHandler
  staticMetaObject 0x3084fe0
  qt_static_metacall 0xd1e000
  method_count 35
  signal_count 11
  method 14 handleContainerMessage
  method 18 handleCreateInContainerMessage
  method 16 handleChangeInContainerMessage
  method 17 handleDeleteInContainerMessage

TContainerStorage
  primary vptr 0x308a1a0
  staticMetaObject 0x308e720
  qt_static_metacall 0xd15af0
  signal 0 containerUpdated
  signal 1 containerRemoved
  signal 2 manualSortModeChanged
```

All four required `receivedContainer*` entries are exact QMeta signals owned by `TProtocolMessageQueue`. All four corresponding `handle*` entries are exact QMeta methods owned by `TContainerProtocolMessageHandler`.

## Typed queue registration surface

S1 exact artifact `9315562574` retains `TProtocolMessageQueue::registerServerMessage<T>` type information for all four message types. Each instantiation takes a queue member pointer accepting the corresponding exact `const GameserverMessageX&` type.

The retained type information does not identify the specific member pointer value supplied at each registration call. Therefore:

```yaml
REGISTERED_MEMBER_POINTER_EQUALS_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
```

## Retained UNKNOWNs

```yaml
QUEUE_SIGNAL_TO_CONTAINER_HANDLER_CONNECTION: UNKNOWN
CONTAINER_HANDLER_TO_STORAGE_MUTATION: UNKNOWN
RUNTIME_CONTAINER_DELIVERY: NOT_OBSERVED
```

The coordinator explicitly rejects promotion of matched queue/handler names into a connection edge without a retained QObject connection/call-dataflow discriminator.

## Evidence provenance

```text
S5 log-reuse run 32122620894
job 95666177103
artifact 9319111338
digest sha256:0e92295e1486540cf82233bdf7eb1c24b9c15c585f815f52a0847b340d4ee745

historical exhaustive QMeta source
run 31790507112
job 94736106350
source head 9afdc76ca6fe238742f270e22d8ecf4abe5ba9a2
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70

S1 type-info artifact
run 32112814216
artifact 9315562574
digest sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

## Source exact-head validation

```text
CI 32123671471 = SUCCESS
Track A governance 32123671344 = SUCCESS
reviews = 0
unresolved review threads = 0
main freshness / behind = 0
```

No new official-client download/execution, physical runtime, Synology/X11/process memory, credentials, login or gameplay was used by S5. PR #475 runtime remained untouched. Physical E2E is `NOT_APPLICABLE` for this static exact-evidence task.
