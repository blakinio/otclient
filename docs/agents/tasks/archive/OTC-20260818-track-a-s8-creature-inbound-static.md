---
task_id: OTC-20260818-track-a-s8-creature-inbound-static
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
source_pr: 531
source_final_head: 8b4080dd1b943b95bd3f5d626e3d8a8bcebc04b3
promotion_decision: ACCEPT_BOUNDED_PARTIAL
ownership_release_state: released
---

# Result

S8 exhausted the useful retained-QMeta creature inbound frontier without new client bytes or runtime.

## Promoted facts

`TProtocolMessageQueue` owns 13 exact creature-family signals:

```text
22 receivedMoveCreatureMessage
26 receivedCreatureUpdateMessage
27 receivedCreatureHealthMessage
28 receivedCreatureOutfitMessage
29 receivedCreatureSpeedMessage
30 receivedCreatureSkullMessage
31 receivedCreaturePartyMessage
32 receivedCreatureUnpassMessage
33 receivedCreatureMarksMessage
36 receivedCreatureDataMessage
44 receivedCreatureLightMessage
74 receivedCreatureTypeMessage
175 receivedConfigureCreaturePodiumMessage
```

`TCreatureProtocolMessageHandler` exact QMeta is `0x30cec80`, `qt_static_metacall 0xd12510`, with `0 methods / 0 signals`. A global exhaustive QMeta search found zero suffix-matched `handleXMessage` methods for the 13 queue signals.

`TCreature` exact QMeta exposes `positionWasUpdated`, killer/guild/party mark changes and `inspectionStateChanged`. `TCreatureStorage` exposes `playerAdded`, `creatureUpdated`, `creatureAppearanceUpdated`.

`TCreaturesGameActionHandler` exact QMeta exposes `sendAttack`, `sendFollow`, `sendLookAtCreature`, inspection and party actions.

S1 exact artifact also proves `registerServerMessage<T>` type contracts for all 13 exact protobuf message types.

## Retained boundary

```yaml
QUEUE_TO_CREATURE_HANDLER_DISPATCH: UNKNOWN_NON_QMETA_WINDOW_REQUIRED
CREATURE_HANDLER_TO_MODEL_STORAGE_MUTATION: UNKNOWN
RUNTIME_CREATURE_DELIVERY: NOT_OBSERVED
CREATURE_INBOUND_REPO_ONLY_QMETA_FRONTIER: EXHAUSTED
```

`positionWasUpdated` is not promoted as authoritative local-player XYZ.

## Provenance / validation

```text
S8 producer run 32139820275
artifact 9325415016
artifact digest sha256:12aeb152a863a1d03cbb10c33dff2abf7b6f62eb8859becc2ff91cf52b27f19a
historical QMeta source 31790507112 / 94736106350
S1 type artifact 9315562574
source CI 32140290731 = SUCCESS
source Track A governance 32140290336 = SUCCESS
reviews = 0
unresolved review threads = 0
```

No new client bytes or runtime, no credentials/login/gameplay, and no PR #528/#475 runtime observation or mutation.
