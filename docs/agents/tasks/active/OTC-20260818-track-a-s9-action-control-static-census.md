---
task_id: OTC-20260818-track-a-s9-action-control-static-census
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: discovery
phase: exact-head-validation
execution_mode: github_only
branch: research/OTC-20260818-track-a-s9-action-control-static-census
base_branch: main
base_main: a10df477ce88183718ed855386ef96ba25b66320
related_pr: 535
created: 2026-08-18T15:12:00+02:00
updated: 2026-08-18T15:18:00+02:00
risk: low
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
owned_paths:
  - .github/workflows/track-a-s9-action-control-log-reuse.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s9-action-control-static-census.md
  - docs/agents/evidence/OTC-20260818-track-a-s9-action-control-static-census/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s9-action-control-static-census.md
modules_touched:
  - official-client-static-re
reuses:
  - sanitized exhaustive QMeta log from run 31790507112 / job 94736106350
  - promoted S8 creature action boundary
  - promoted S6 chat boundary
  - promoted S5/S7 container and inventory boundaries
depends_on:
  - OTC-20260818-track-a-s8-creature-inbound-static
blocks: []
non_overlap:
  - PR #528 native-login-to-ingame runtime is not observed or mutated.
  - PR #475 worldmap runtime is not observed or mutated.
  - PR #302 direct-player-position Draft is not modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: low
decomposition_decision: single
validation_level: focused
---

# Terminal research result

```yaml
S9_RESULT: ACCEPT_STATIC_ACTION_CATALOGUE_CANDIDATE
GAME_ACTION_HANDLER_QMETA_DENOMINATOR: 28
MOVEMENT_INTENT_BOUNDARY: FACT
PLAYER_PROTOCOL_MOVEMENT_SEND_BOUNDARY: FACT
ATTACK_FOLLOW_BOUNDARY: FACT
USE_USEWITH_BOUNDARY: FACT
MOVE_OBJECT_CONTAINER_BOUNDARY: FACT
CHAT_ACTION_BOUNDARY: FACT
INTERNAL_ACTION_ROUTER_QMETA: FACT
PER_ACTION_ROUTER_TO_PROTOCOL_EDGE: UNKNOWN
PER_ACTION_PROTOCOL_TO_SERIALIZED_MESSAGE_EDGE: UNKNOWN
PER_ACTION_RUNTIME_EFFECT: NOT_OBSERVED
STATIC_ACTION_CONTROL_CATALOGUE: EXHAUSTED_FOR_RETAINED_QMETA
```

## Denominator

The exact exhaustive QMeta source contains **28** classes whose type name ends in `GameActionHandler`. S9 retains the full denominator in the producer artifact and promotes detailed methods only for core gameplay-control classes.

## Movement — exact native/QMeta boundaries

```text
tibia::input::TPlayerMovementIntentHandler
QMeta 0x3085de0 / qt_static_metacall 0xdc9220
19 methods / 18 signals

sendGoNorth/East/South/West
sendGoNorthEast/SouthEast/SouthWest/NorthWest
sendGoPath
sendRotateNorth/East/South/West
sendStop
sendCancel
sendFollowZero
requestTimedCallback
```

```text
tibia::input::TPlayerMovementGameActionHandler
QMeta 0x3085260 / qt_static_metacall 0xdc4060
3 methods / 2 signals
publishGameAction
sendCancel
handleGameAction
```

```text
tibia::game::TPlayerProtocolMessageHandler
QMeta 0x30852a0 / qt_static_metacall 0xd1a920
22 methods / 22 signals
sendEnterWorld
sendGoNorth/East/South/West
sendStop / sendCancel
sendGoNorthEast/SouthEast/SouthWest/NorthWest
sendGoPath
sendRotateNorth/East/South/West
sendSetTactics
worldEntered
...
```

Matching movement names across these layers do not by themselves prove the concrete connection/dataflow edge.

## Attack/follow/look — FACT QMeta boundary

```text
tibia::creatures::TCreaturesGameActionHandler
QMeta 0x3085060 / qt_static_metacall 0xd16340
13 methods / 13 signals

sendAttack
sendFollow
sendLookAtCreature
sendInspectPlayer
party actions
```

## Use/use-with/object actions — FACT QMeta boundaries

```text
tibia::input::TUseWithGameActionHandler
QMeta 0x3085120 / qt_static_metacall 0xdc4480
5 methods / 4 signals
startTargetSelection
publishGameAction
sendUseTwoObjects
sendUseOnCreature
handleGameAction
```

```text
tibia::input::TGenericGameActionHandler
QMeta 0x3085020 / qt_static_metacall 0xdcb990
31 methods / 12 signals
sendTurnObject
sendUseObject
sendLook
sendBrowseField
sendMoveObject
...
handleLookAction
handleUseAction
handleMoveUpAction
handleRotateAction
...
```

## Container/object movement — FACT QMeta boundary

```text
tibia::container::TContainerGameActionHandler
QMeta 0x30850a0 / qt_static_metacall 0xd1dac0
23 methods / 9 signals
sendMoveObject
sendEquipObject
sendStashAction
sendOpenDepotSearch
sendCloseDepotSearch
sendDepotSearchType
sendOpenParentContainer
sendDepotSearchRetrieve
handleMoveObjectGameAction
handleTryToEquipGameAction
...
```

## Chat — FACT QMeta boundary

```text
tibia::chat::TChatGameActionHandler
QMeta 0x30851a0 / qt_static_metacall 0xcff5b0
38 methods / 11 signals
sendGetChanneList
sendJoinChannel
sendOpenChannel
sendPrivateChannel
sendCloseNPCChannel
sendLeaveChannel
sendInviteToChannel
sendExcludeFromChannel
sendGuildMessage
sendTalkMessage
publishGameAction
```

The exact misspellings `sendGetChanneList` and other names are preserved from retained metadata.

## Player actions / router — FACT QMeta boundaries

```text
tibia::game::TPlayerGameActionHandler
QMeta 0x3085160 / qt_static_metacall 0xd1a230
8 methods / 8 signals
sendMount
sendGetOutfit
sendSetOutfit
sendSetCreaturePodiumConfiguration
sendSetHirelingName
sendSetTactics
sendInspectPlayer
```

```text
tibia::game::TInternalGameActionRouter
QMeta 0x3074b20 / qt_static_metacall 0xd20600
4 methods / 2 signals
publishGameActionInternal
publishGameActionBetweenRouters
handleGameActionInternal
handleGameActionFromOtherRouter
```

## Provenance

```text
S9 producer run 32140983838
artifact 9325847070
digest sha256:12ddebc9aa1ff73f96370091c50e33a6cf3bf7b37a4cf8bc7007175861c5491d
historical QMeta source 31790507112 / 94736106350
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70
```

# Static-lane stop condition

The retained QMeta corpus is now sufficient to catalogue the principal state and action surfaces, but not to prove the missing per-action connections or runtime effects. Further meaningful progress requires one of:

1. approved exact-build code/disassembly windows for the relevant QObject/direct-call/dataflow edges; or
2. legal runtime after the current runtime owner releases a non-conflicting evidence surface.

Repeated QMeta/name scans would no longer materially improve the causal model.

# Acceptance

- [x] retained exact-SHA/QMeta evidence only;
- [x] all 28 `*GameActionHandler` QMeta records enumerated;
- [x] required core-control class surfaces recovered;
- [x] movement/turn/stop/path boundaries classified;
- [x] attack/follow/look boundaries classified;
- [x] use/use-with/object/container boundaries classified;
- [x] chat/player/router boundaries classified;
- [x] wire/runtime effects explicitly not overclaimed;
- [x] no runtime/new client/credentials/login/gameplay or PR #528/#475 observation;
- [ ] durable evidence/report;
- [ ] temporary producer removed;
- [ ] final exact-head CI/governance/reviews;
- [ ] coordinator promotion/closeout and final static-lane stop.
