# OTCLIENT Track A — S8 creature inbound static report

## Decision candidate

`ACCEPT_BOUNDED_PARTIAL` with a terminal repo-only QMeta stop for creature inbound dispatch.

## Proven exact boundaries

```text
TProtocolMessageQueue
  13 creature-family receive signals
  indices 22, 26-33, 36, 44, 74, 175

TCreatureProtocolMessageHandler
  QMeta 0x30cec80 / qt_static_metacall 0xd12510
  0 methods / 0 signals

TCreature
  QMeta 0x3077d00 / qt_static_metacall 0xd15f60
  positionWasUpdated + mark/party/inspection signals

TCreatureStorage
  QMeta 0x3085ba0 / qt_static_metacall 0xd25b70
  playerAdded / creatureUpdated / creatureAppearanceUpdated

TCreaturesGameActionHandler
  QMeta 0x3085060 / qt_static_metacall 0xd16340
  sendAttack / sendFollow / sendLookAtCreature / party actions
```

A global exhaustive QMeta search finds **zero** suffix-matched `handleXMessage` methods for the 13 creature receive signals. That is a negative QMeta result, not evidence that a non-QMeta handler implementation is absent.

## Remaining boundary

```text
TProtocolMessageQueue receivedCreature*
       ↓
non-QMeta dispatch / handler construction = UNKNOWN
       ↓
TCreatureProtocolMessageHandler
       ↓
TCreature / TCreatureStorage mutation      = UNKNOWN
```

`positionWasUpdated` is not authoritative local-player XYZ proof.

## Repo-only stop

The creature inbound QMeta frontier is exhausted. Deeper proof requires an exact-build executable-code window or a later legal runtime evidence surface. More name/QMeta scans cannot close the missing edge.

## Provenance

```text
S8 run 32139820275
artifact 9325415016
sha256:12aeb152a863a1d03cbb10c33dff2abf7b6f62eb8859becc2ff91cf52b27f19a
QMeta source 31790507112 / 94736106350
S1 type artifact 9315562574
```

## Isolation

No new client bytes/runtime, no Synology/X11/VNC/process memory, no credentials/login/gameplay, and no PR #528/#475 runtime observation or mutation.
