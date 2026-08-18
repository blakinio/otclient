# Track A S8 — creature inbound static boundaries

Task: `OTC-20260818-track-a-s8-creature-inbound-static`  
Researcher PR: `#531`  
Execution: retained exact-build evidence only, `runtime_access: none`

## Result

The retained QMeta corpus gives a complete queue/model/storage boundary for the main creature-message family, but it **does not contain the creature protocol dispatch edge**.

```text
GameserverMessageCreature*/MoveCreature/ConfigureCreaturePodium
       ↓ registration type contracts
TProtocolMessageQueue received* signals                 FACT
       ↓
non-QMeta dispatch                                      UNKNOWN
       ↓
TCreatureProtocolMessageHandler                         exact QMeta = 0/0
       ↓
model/storage mutation                                  UNKNOWN
       ↓
TCreature / TCreatureStorage signals                    FACT
```

## Queue signals — FACT

```text
22  receivedMoveCreatureMessage
26  receivedCreatureUpdateMessage
27  receivedCreatureHealthMessage
28  receivedCreatureOutfitMessage
29  receivedCreatureSpeedMessage
30  receivedCreatureSkullMessage
31  receivedCreaturePartyMessage
32  receivedCreatureUnpassMessage
33  receivedCreatureMarksMessage
36  receivedCreatureDataMessage
44  receivedCreatureLightMessage
74  receivedCreatureTypeMessage
175 receivedConfigureCreaturePodiumMessage
```

All 13 belong to the exact `TProtocolMessageQueue` signal prefix (`QMeta 0x3085b60`, `qt_static_metacall 0xdf5fe0`, 355 methods / 192 signals).

## Global QMeta negative discriminator

For every queue signal above, the suffix-matched candidate `handleXMessage` was searched across all methods in the retained exhaustive QMeta corpus. Result:

```text
expected suffix handle names: 13
QMeta matches:                 0
```

Classification: **DISPROVEN inside the retained QMeta surface**.

This does not prove that the binary lacks those semantic handlers. It proves that the missing creature dispatch is not exposed as suffix-matched QMeta methods in the retained corpus.

## `TCreatureProtocolMessageHandler`

```text
tibia::creatures::TCreatureProtocolMessageHandler
QMeta               0x30cec80
qt_static_metacall  0xd12510
methods             0
signals             0
```

Classification: **FACT_EMPTY_0_0**.

The class identity itself has the earlier S1 direct code-to-string xref, but that does not establish any message edge.

## Creature model — FACT

```text
tibia::creatures::TCreature
QMeta               0x3077d00
qt_static_metacall  0xd15f60
5 methods / 5 signals

0 positionWasUpdated
1 playerKillerMarkChanged
2 playerGuildFlagChanged
3 playerPartyFlagChanged
4 inspectionStateChanged
```

`positionWasUpdated` is an exact per-creature signal only. It is not promoted as authoritative local-player XYZ.

## Creature storage — FACT

```text
tibia::creatures::TCreatureStorage
QMeta               0x3085ba0
qt_static_metacall  0xd25b70
3 methods / 3 signals

0 playerAdded
1 creatureUpdated
2 creatureAppearanceUpdated
```

The exact handler-to-storage mutation edge remains `UNKNOWN`.

## Creature action boundary — FACT

The same exact QMeta source exposes:

```text
tibia::creatures::TCreaturesGameActionHandler
QMeta               0x3085060
qt_static_metacall  0xd16340
13 methods / 13 signals

publishGameAction
sendAttack
sendFollow
sendLookAtCreature
sendInspectPlayer
sendInviteToParty
sendJoinParty
sendRevokeInvitation
sendPassLeadership
sendLeaveParty
sendShareExperience
sendGreet
sendJoinAggression
```

These are static QMeta action-boundary facts, not proof of their downstream wire implementation.

## Typed registration contracts

S1 artifact `9315562574` retains `TProtocolMessageQueue::registerServerMessage<T>` template type symbols for all 13 exact protobuf types corresponding to the queue signals. The concrete member pointer used at registration remains unknown.

## Provenance

```text
S8 producer run 32139820275
artifact 9325415016
digest sha256:12aeb152a863a1d03cbb10c33dff2abf7b6f62eb8859becc2ff91cf52b27f19a

historical exhaustive QMeta source
run 31790507112 / job 94736106350
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70

S1 type artifact
9315562574
sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

## Stop condition

```yaml
CREATURE_INBOUND_REPO_ONLY_QMETA_FRONTIER: EXHAUSTED
QUEUE_TO_CREATURE_HANDLER_DISPATCH: UNKNOWN_NON_QMETA_WINDOW_REQUIRED
CREATURE_HANDLER_TO_MODEL_STORAGE_MUTATION: UNKNOWN
RUNTIME_CREATURE_DELIVERY: NOT_OBSERVED
```

Deeper creature inbound RE now needs either an approved exact-build code/disassembly window or a later legal non-conflicting runtime surface. Repeating QMeta/name scans cannot resolve the missing edge.

## Isolation

No new official-client bytes, client execution, Synology/X11/VNC, process memory, credentials, login or gameplay. PR #528 and PR #475 runtime surfaces were not observed or mutated, and PR #302 was not modified.
