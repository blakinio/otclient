# Track A S8 creature inbound static — coordinator promotion

Date: 2026-08-18  
Source Draft: PR #531  
Source final head: `8b4080dd1b943b95bd3f5d626e3d8a8bcebc04b3`  
Trusted promotion base: `main@d53eec81bf718b1128fc8e7f9b0a53d991bf30bf`  
Decision: **ACCEPT_BOUNDED_PARTIAL**

## Promoted exact boundaries

```text
TProtocolMessageQueue
  QMeta 0x3085b60 / qt_static_metacall 0xdf5fe0
  355 methods / 192 signals
  13 creature-family receive signals at indices:
  22,26,27,28,29,30,31,32,33,36,44,74,175

TCreatureProtocolMessageHandler
  QMeta 0x30cec80 / qt_static_metacall 0xd12510
  0 methods / 0 signals

TCreature
  QMeta 0x3077d00 / qt_static_metacall 0xd15f60
  positionWasUpdated
  playerKillerMarkChanged
  playerGuildFlagChanged
  playerPartyFlagChanged
  inspectionStateChanged

TCreatureStorage
  QMeta 0x3085ba0 / qt_static_metacall 0xd25b70
  playerAdded
  creatureUpdated
  creatureAppearanceUpdated

TCreaturesGameActionHandler
  QMeta 0x3085060 / qt_static_metacall 0xd16340
  publishGameAction / sendAttack / sendFollow / sendLookAtCreature /
  sendInspectPlayer and party-action signals
```

## Negative discriminator

All 13 suffix-matched candidate `handleXMessage` names were searched across every method of the retained exhaustive QMeta corpus. Exact QMeta matches: `0`.

Therefore suffix-matched QMeta creature handler ownership is **DISPROVEN inside the retained QMeta surface**. This does not disprove a non-QMeta virtual/direct dispatch path.

## Registration contracts

S1 artifact `9315562574` contains exact `TProtocolMessageQueue::registerServerMessage<T>` type symbols for all 13 corresponding protobuf message types. Concrete registration member-pointer identities remain unknown.

## Retained UNKNOWNs / stop condition

```yaml
QUEUE_TO_CREATURE_HANDLER_DISPATCH: UNKNOWN_NON_QMETA_WINDOW_REQUIRED
CREATURE_HANDLER_TO_MODEL_STORAGE_MUTATION: UNKNOWN
RUNTIME_CREATURE_DELIVERY: NOT_OBSERVED
CREATURE_INBOUND_REPO_ONLY_QMETA_FRONTIER: EXHAUSTED
```

Deeper creature inbound proof requires an approved exact-build code/disassembly window or a later legal non-conflicting runtime surface. Repeating QMeta/name scans cannot close this edge.

`TCreature::positionWasUpdated` is not authoritative local-player XYZ proof.

## Provenance

```text
S8 producer run 32139820275
artifact 9325415016
sha256:12aeb152a863a1d03cbb10c33dff2abf7b6f62eb8859becc2ff91cf52b27f19a
QMeta source run/job 31790507112 / 94736106350
QMeta log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70
S1 artifact 9315562574
sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

## Source validation / isolation

```text
CI 32140290731 = SUCCESS
Track A governance 32140290336 = SUCCESS
reviews = 0
unresolved review threads = 0
```

No new client bytes, physical runtime, Synology/X11/VNC, process memory, credentials, login or gameplay. PR #528 and #475 runtime surfaces were untouched. Physical E2E is `NOT_APPLICABLE` for this static task.
