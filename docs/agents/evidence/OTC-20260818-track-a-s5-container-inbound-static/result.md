# Track A S5 — container inbound static dispatch

Task: `OTC-20260818-track-a-s5-container-inbound-static`  
PR: `#518`  
Execution: GitHub-hosted reuse of already-sanitized exact-build evidence only; `runtime_access: none`.

## Exact build

```text
version 15.32.df7b29
size    51965216
sha256  e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

S5 did not download or execute the client.

## Exact QMeta log-reuse producer

```text
run      32122620894
job      95666177103
artifact 9319111338
digest   sha256:0e92295e1486540cf82233bdf7eb1c24b9c15c585f815f52a0847b340d4ee745
result   SUCCESS
```

It reused the historical exhaustive exact-SHA QMeta log:

```text
source run  31790507112
source job  94736106350
source head 9afdc76ca6fe238742f270e22d8ecf4abe5ba9a2
log sha256  481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70
```

## FACT — exact receive owner and signal indices

All four requested receive surfaces are methods of:

```text
tibia::protocol::TProtocolMessageQueue
staticMetaObject   0x3085b60
qt_static_metacall 0xdf5fe0
method_count       355
signal_count       192
```

Exact methods:

```text
62 receivedContainerMessage          argc=1 flags=0x6 QMeta-signal
64 receivedCreateInContainerMessage  argc=1 flags=0x6 QMeta-signal
65 receivedChangeInContainerMessage  argc=1 flags=0x6 QMeta-signal
66 receivedDeleteInContainerMessage  argc=1 flags=0x6 QMeta-signal
```

Adjacent container-family queue signals are also recovered:

```text
63  receivedCloseContainerMessage
147 receivedUpdateManagedContainersMessage
154 receivedSpecialContainersAvailableMessage
```

This promotes the four `receivedContainer*` names from S1 string presence to exact QMeta ownership and signal-index FACTs.

## FACT — exact container handler QMeta surface

```text
tibia::container::TContainerProtocolMessageHandler
staticMetaObject   0x3084fe0
qt_static_metacall 0xd1e000
method_count       35
signal_count       11
```

The four corresponding handler methods are exact QMeta non-signal methods:

```text
14 handleContainerMessage          argc=1 flags=0xa
18 handleCreateInContainerMessage  argc=1 flags=0xa
16 handleChangeInContainerMessage  argc=1 flags=0xa
17 handleDeleteInContainerMessage  argc=1 flags=0xa
```

S1 also retains a direct executable reference to the handler class-name string at `0xd290dd`; as before, that xref proves the executable reference only and is not treated as the semantic message-dispatch edge.

## FACT — exact container storage QMeta surface

```text
tibia::container::TContainerStorage
primary vptr       0x308a1a0
staticMetaObject   0x308e720
qt_static_metacall 0xd15af0
method_count       3
signal_count       3
```

Its exact signals are:

```text
0 containerUpdated        argc=2
1 containerRemoved        argc=1
2 manualSortModeChanged   argc=0
```

## FACT — typed queue registration contracts exist for all four server messages

S1 exact artifact `9315562574` (`sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860`) retains mangled type information that demangles to these template contracts:

```text
TProtocolMessageQueue::registerServerMessage<GameserverMessageContainer>(
  void (TProtocolMessageQueue::*)(GameserverMessageContainer const&))

TProtocolMessageQueue::registerServerMessage<GameserverMessageCreateInContainer>(
  void (TProtocolMessageQueue::*)(GameserverMessageCreateInContainer const&))

TProtocolMessageQueue::registerServerMessage<GameserverMessageChangeInContainer>(
  void (TProtocolMessageQueue::*)(GameserverMessageChangeInContainer const&))

TProtocolMessageQueue::registerServerMessage<GameserverMessageDeleteInContainer>(
  void (TProtocolMessageQueue::*)(GameserverMessageDeleteInContainer const&))
```

Therefore exact compile-time registration surfaces exist in `TProtocolMessageQueue` for all four protobuf types, and each registration contract accepts a queue member pointer taking the corresponding `const GameserverMessageX&`.

## Evidence boundary — do not overconnect the graph

The preserved evidence does **not** identify which concrete queue member pointer was supplied to each `registerServerMessage<T>` instantiation. The fact that the queue also owns the matching `receivedXMessage` QMeta signals is strong structural/lexical evidence, but the exact registration-member-pointer identity is not directly retained.

Likewise, no preserved connection-construction window proves:

```text
receivedContainer* signal -> TContainerProtocolMessageHandler::handle* method
```

and no preserved call/dataflow window proves:

```text
TContainerProtocolMessageHandler::handle* -> TContainerStorage mutation
```

Those edges remain `UNKNOWN` rather than being inferred from matched naming.

## Classification

```yaml
FOUR_CONTAINER_SERVER_MESSAGE_REGISTRATION_TYPE_CONTRACTS: FACT_TYPEINFO
FOUR_RECEIVED_CONTAINER_QMETA_OWNER: PROVEN_TProtocolMessageQueue
FOUR_RECEIVED_CONTAINER_QMETA_SIGNAL_INDICES: PROVEN
FOUR_CONTAINER_HANDLER_QMETA_METHODS: PROVEN_TContainerProtocolMessageHandler
TCONTAINERSTORAGE_QMETA_SURFACE: PROVEN
REGISTERED_MEMBER_POINTER_EQUALS_MATCHING_RECEIVED_SIGNAL: INFERENCE_HIGH_NOT_DIRECTLY_PROVEN
QUEUE_SIGNAL_TO_CONTAINER_HANDLER_CONNECTION: UNKNOWN
CONTAINER_HANDLER_TO_STORAGE_MUTATION: UNKNOWN
RUNTIME_CONTAINER_DELIVERY: NOT_OBSERVED
```

## Safety

```yaml
s5_client_downloaded: false
s5_client_executed: false
s5_runtime_access: none
s5_synology_access: false
credentials_used: false
login_performed: false
gameplay_performed: false
pr475_runtime_observed: false
pr475_runtime_mutated: false
```

## Next discriminator

A further static step is justified only if an already-sanitized exact-build connection/call window can be found for either:

1. queue `receivedContainer*` signal connection construction, or
2. `TContainerProtocolMessageHandler::handle*` downstream calls touching `TContainerStorage`.

Do not obtain a newer client and apply old VAs. Do not use PR #475 runtime to manufacture this evidence.
