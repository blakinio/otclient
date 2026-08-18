---
task_id: OTC-20260818-track-a-s8-creature-inbound-static
status: validating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: exact-head-validation
execution_mode: github_only
branch: research/OTC-20260818-track-a-s8-creature-inbound-static
base_branch: main
base_main: d53eec81bf718b1128fc8e7f9b0a53d991bf30bf
related_pr: 531
created: 2026-08-18T14:58:00+02:00
updated: 2026-08-18T15:04:00+02:00
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
  - .github/workflows/track-a-s8-creature-inbound-log-reuse.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s8-creature-inbound-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s8-creature-inbound-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s8-creature-inbound-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - sanitized exhaustive QMeta log from run 31790507112 / job 94736106350
  - S1 exact type/name artifact run 32112814216 / artifact 9315562574
depends_on:
  - OTC-20260818-track-a-s7-inventory-equipment-static
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
S8_RESULT: ACCEPT_BOUNDED_PARTIAL_CANDIDATE
QUEUE_CREATURE_SIGNAL_COUNT: 13
QUEUE_CREATURE_SIGNAL_OWNERSHIP: FACT
SUFFIX_MATCHED_HANDLE_METHODS_IN_RETAINED_QMETA: 0
TCREATURE_PROTOCOL_HANDLER_QMETA_METHODS: 0
TCREATURE_PROTOCOL_HANDLER_QMETA_SIGNALS: 0
TCREATURE_QMETA: FACT
TCREATURE_STORAGE_QMETA: FACT
TCREATURES_GAME_ACTION_HANDLER_QMETA: FACT
QUEUE_TO_CREATURE_HANDLER_DISPATCH: UNKNOWN_NON_QMETA_WINDOW_REQUIRED
CREATURE_HANDLER_TO_MODEL_STORAGE_MUTATION: UNKNOWN
RUNTIME_CREATURE_DELIVERY: NOT_OBSERVED
CREATURE_INBOUND_REPO_ONLY_QMETA_FRONTIER: EXHAUSTED
```

## Exact queue signals

```text
TProtocolMessageQueue
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

All 13 are inside the exact queue QMeta signal prefix.

## Global suffix-handle falsification

The 13 suffix-matched candidate names (`receivedX` -> `handleX`) were searched across every method of every retained exhaustive QMeta record. Result:

```text
QMeta suffix-matched handle hits = 0
```

This proves only that the retained QMeta corpus contains no such direct handle methods. It does not disprove a non-QMeta virtual/direct handler path.

## Exact handler/model/storage surfaces

```text
tibia::creatures::TCreatureProtocolMessageHandler
  QMeta 0x30cec80
  qt_static_metacall 0xd12510
  0 methods / 0 signals

tibia::creatures::TCreature
  QMeta 0x3077d00
  qt_static_metacall 0xd15f60
  5 methods / 5 signals
  0 positionWasUpdated
  1 playerKillerMarkChanged
  2 playerGuildFlagChanged
  3 playerPartyFlagChanged
  4 inspectionStateChanged

tibia::creatures::TCreatureStorage
  QMeta 0x3085ba0
  qt_static_metacall 0xd25b70
  3 methods / 3 signals
  0 playerAdded
  1 creatureUpdated
  2 creatureAppearanceUpdated
```

`positionWasUpdated` is an exact per-creature QMeta signal, not proof of authoritative local-player XYZ.

## Exact creature action QMeta surface

```text
tibia::creatures::TCreaturesGameActionHandler
  QMeta 0x3085060
  qt_static_metacall 0xd16340
  13 methods / 13 signals

0  publishGameAction
1  sendAttack
2  sendFollow
3  sendLookAtCreature
4  sendInspectPlayer
5  sendInviteToParty
6  sendJoinParty
7  sendRevokeInvitation
8  sendPassLeadership
9  sendLeaveParty
10 sendShareExperience
11 sendGreet
12 sendJoinAggression
```

These are QMeta action-boundary facts only; no wire emission/runtime behavior is claimed by S8.

## Typed queue registration contracts

S1 exact artifact `9315562574` contains `TProtocolMessageQueue::registerServerMessage<T>` template type symbols for all 13 corresponding exact protobuf messages. This proves member-pointer type contracts, not concrete registration member-pointer identities.

## Provenance

```text
S8 producer run 32139820275
artifact 9325415016
digest sha256:12aeb152a863a1d03cbb10c33dff2abf7b6f62eb8859becc2ff91cf52b27f19a
historical QMeta source 31790507112 / 94736106350
log sha256 481600615765a5bbc570888817f23b75ac5cf8b93fab693f3c461872c183ef70
S1 artifact 9315562574
sha256:583c8c217fa2eaa2411f79995473cd910b8803d8599f80574491ca27b8ab9860
```

# Acceptance

- [x] retained exact-build/repository evidence only;
- [x] 13 exact creature queue signals enumerated;
- [x] global QMeta suffix-handle search completed with zero hits;
- [x] exact 0/0 `TCreatureProtocolMessageHandler` QMeta surface recorded;
- [x] exact `TCreature` and `TCreatureStorage` surfaces recovered;
- [x] exact creature game-action QMeta surface recovered;
 [x] typed registration contracts verified in S1 artifact;
- [x] downstream non-QMeta dispatch/mutation retained UNKNOWN;
- [x] creature inbound repo-only QMeta frontier classified exhausted;
- [x] no runtime/new client/credentials/login/gameplay or PR #528/#475 observation;
- [ ] durable evidence/report;
- [ ] temporary producer removed;
- [ ] final CI/governance/review gates;
- [ ] coordinator promotion/closeout.

# Resume condition

Resume deeper creature inbound dispatch only with either:

1. an approved exact-build code/disassembly window containing the non-QMeta handler construction/dispatch path; or
2. a legal runtime after the active runtime owner releases or exposes a non-conflicting evidence surface.

Do not infer the missing edge from handler class-name proximity.
