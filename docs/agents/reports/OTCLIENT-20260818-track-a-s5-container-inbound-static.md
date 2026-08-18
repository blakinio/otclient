# OTCLIENT Track A — S5 container inbound static report

Date: 2026-08-18  
Task: `OTC-20260818-track-a-s5-container-inbound-static`  
PR: `#518`

## Promoted candidate facts from the bounded research

The container inbound graph is now statically resolved farther than S1:

```text
GameserverMessageContainer family
  -> exact TProtocolMessageQueue registerServerMessage<T> type contracts

TProtocolMessageQueue
  QMeta 0x3085b60 / qt_static_metacall 0xdf5fe0
  -> signal 62 receivedContainerMessage
  -> signal 64 receivedCreateInContainerMessage
  -> signal 65 receivedChangeInContainerMessage
  -> signal 66 receivedDeleteInContainerMessage

TContainerProtocolMessageHandler
  QMeta 0x3084fe0 / qt_static_metacall 0xd1e000
  -> method 14 handleContainerMessage
  -> method 18 handleCreateInContainerMessage
  -> method 16 handleChangeInContainerMessage
  -> method 17 handleDeleteInContainerMessage

TContainerStorage
  vptr 0x308a1a0
  QMeta 0x308e720 / qt_static_metacall 0xd15af0
  -> containerUpdated
  -> containerRemoved
  -> manualSortModeChanged
```

## Still deliberately unresolved

The preserved exact-build evidence does not contain the connection/call window needed to prove:

```text
TProtocolMessageQueue::receivedContainer*
  -> TContainerProtocolMessageHandler::handle*

TContainerProtocolMessageHandler::handle*
  -> TContainerStorage mutation
```

Matched names do not substitute for a connection/dataflow edge. These remain `UNKNOWN`.

## Evidence provenance

S5 normalized prior exact QMeta log:

```text
run 32122620894
job 95666177103
artifact 9319111338
sha256 0e92295e1486540cf82233bdf7eb1c24b9c15c585f815f52a0847b340d4ee745
```

Underlying exact QMeta census:

```text
run 31790507112
job 94736106350
source head 9afdc76ca6fe238742f270e22d8ecf4abe5ba9a2
```

Exact typed registration type-information came from S1 artifact:

```text
run 32112814216
artifact 9315562574
sha256 583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

## Current boundary

```yaml
CONTAINER_MESSAGE_REGISTRATION_SURFACE: PROVEN_TYPEINFO
RECEIVED_CONTAINER_SIGNAL_OWNER: PROVEN_TProtocolMessageQueue
CONTAINER_HANDLER_QMETA_METHOD_SURFACE: PROVEN
CONTAINER_STORAGE_QMETA_SURFACE: PROVEN
QUEUE_TO_HANDLER: UNKNOWN
HANDLER_TO_STORAGE: UNKNOWN
RUNTIME: NOT_OBSERVED
```

No new client bytes and no physical Track A runtime were consumed.
