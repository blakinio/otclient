# OTCLIENT Track A — S4 creature/container evidence availability

Date: 2026-08-18  
Task: `OTC-20260818-track-a-s4-creature-container-evidence-census`  
PR: `#517`

## Decision

**Select container as the next independent static frontier.**

The repository-only census itself found similar overall occurrence density for creature and container evidence, so token counts alone do not choose a winner. The exact retained QMeta census does:

```text
TContainerProtocolMessageHandler: 35 methods / 11 signals
TContainerStorage:                 3 methods / 3 signals

TCreatureProtocolMessageHandler:   0 methods / 0 signals
TCreatureStorage:                  3 methods / 3 signals
```

This makes the container family materially more discriminating for another repo-only exact-static pass while the public current client no longer matches the pinned 15.32 build.

## Container starting graph

```text
GameserverMessageContainer
GameserverMessageCreateInContainer
GameserverMessageChangeInContainer
GameserverMessageDeleteInContainer
          |
          | promoted S1 lexical correspondence only
          v
receivedContainerMessage
receivedCreateInContainerMessage
receivedChangeInContainerMessage
receivedDeleteInContainerMessage
          |
          | UNKNOWN
          v
TProtocolMessageQueue / concrete owner
          |
          | UNKNOWN
          v
TContainerProtocolMessageHandler
  QMeta 0x3084fe0
  qt_static_metacall 0xd1e000
  35 methods / 11 signals
          |
          | UNKNOWN
          v
TContainerStorage
  primary vptr 0x308a1a0
  QMeta 0x308e720
  qt_static_metacall 0xd15af0
  3 methods / 3 signals
```

## Creature disposition

Creature is deferred, not rejected. Its storage remains a valuable exact anchor (`TCreatureStorage` primary vptr `0x308d078`, QMeta `0x3085ba0`, 3 signals), but `TCreatureProtocolMessageHandler` exposes `0` QMeta methods/signals in the retained census. A later creature proof likely needs another static construction/connection window or fresh exact-build source.

## Evidence producer

```text
run      32120910903
job      95660747269
artifact 9318473016
sha256   2759b4ec6e010485205f974bb726c2be350ffeed20a2417707cb207efd0b491d
```

No client download/execution and no physical runtime were used.

## Next bounded task

The next task should answer only:

```text
Who exactly owns the four receivedContainer* message surfaces,
what are their exact typed QMeta contracts if recoverable from committed evidence,
and what exact handler/storage edges can be proven without obtaining new client bytes?
```

Do not infer the queue/handler/storage connection from naming alone. If current committed exact evidence ends before the edge, stop at `UNKNOWN` rather than consuming PR #475 runtime.
