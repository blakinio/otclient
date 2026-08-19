# TIBIA-RE-CREATURE-COMBAT static G0 — coordinator promotion audit

```yaml
date: 2026-08-19
source_task: OTC-20260819-track-a-creature-combat-static-g0
source_pr: 558
source_head: fa7871e7ee085601ab91a8b695e4db83f06b80e4
coordinator_review: 4970526774
coordinator_decision: ACCEPT
open_material_findings: 0
promotion_base: f13179df4aa99a946faf6ec9635d5d40370c6ff3
runtime_access: none
mutation_authorized: false
physical_e2e_required: false
```

## Independent verification

The coordinator independently downloaded producer artifact `9356949168` from successful run/job `32230171183 / 95998084380`.

ZIP SHA-256 reproduced GitHub artifact metadata exactly:

```text
d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7
```

The archive contains exactly four compact text evidence files and no packed/unpacked client bytes:

```text
creature-combat-qmeta.txt  8593 bytes
fence.txt                  310 bytes
protocol-strings.txt       15241 bytes
semantic-strings.txt       119513 bytes
```

Independently observed inner-file SHA-256 values:

```text
creature-combat-qmeta.txt  1daf73e0d8a64dc6d163de07f78ca2a4c6692bbb02e40c4d8b997b2858fc07bc
fence.txt                  3d6ecb09a850d49916491127981a93b0a55eccec66810ddeba0403888b537bcb
protocol-strings.txt       70e364f81184a0909152706bff7cbe0c3fc29f00695f014310da1bc86b08326a
semantic-strings.txt       f1816b5a9610bf48c73319481ba0d26b12e5ed4127d1b74821a64a9b76e8c176
```

Exact package fence from the artifact:

```text
PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
PACKED_SIZE=10214529
UNPACKED_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
UNPACKED_SIZE=52109920
CURRENT_PACKAGE_FENCE=PASS
RAW_CLIENT_RETAINED=false
```

The producer workflow at `bb0dc3a44a6e5daca2f81817696f91043f8c03d5` was independently reviewed. It parses QMeta/static-metacall ownership and method names, but does not recover or claim per-method native targets.

## Verified D06 structural evidence

Raw QMeta directly confirms:

```text
tibia::worldmap::TCreatureHUDOverlayController
  refreshCreatureHUDs
  update

tibia::worldmap::TCreatureHUDQmlRenderInfo
  SIGNALS=19
  nameChanged
  healthPercentChanged
  manaPercentChanged
  manaShieldPercentChanged
  healthColorChanged
  showCreatureNameChanged
  showHealthBarChanged
  showManaBarChanged
  showManaShieldBarChanged
  horizontalCreatureIconsChanged
  verticalCreatureIconsChanged
  fiendishMonsterChanged
  showBarsChanged
  showArcsChanged
  scaleFactorChanged
  comboPointsOrSereneStateChanged
  playerStatesChanged
  showSpecialConditionsChanged
  statusEffectsChanged
```

This is dedicated exact-current-package HUD structural evidence. It supports `D06 NOT_STARTED -> PARTIAL`, but does not prove the authoritative provider, icon/status schema, live values or update causality.

## Verified D07 structural evidence

Raw QMeta directly confirms `TBattleListController`, `TBattleListControllerStorage`, `TBattleListDataModel` and `TBattleListGameActionHandler`, including:

```text
isFilterActive
toggleFilter
requestOpenSecondaryBattleList
requestMakePrimary
onCreatureClicked
onCreatureTargetSelected
handleAttackFirstTargetGameAction
handleAttackNextTargetGameAction
handleAttackPreviousTargetGameAction
attackFirstTarget
attackNextOrPreviousTarget
filterDrawCommands
sortDrawCommands
```

Neutral static strings also retain battle-list filter/sort proxy and secondary-list action names. This supports `D07 NOT_STARTED -> PARTIAL`; exact enum meanings, sort criteria/tie-breaking, live membership and persistence remain unknown.

## Creature protocol/action boundary

Raw protocol strings directly confirm current generated creature server-message type names and `TProtocolMessageQueue::registerServerMessage<GameserverMessageCreature...>` template-string presence for the retained families, plus `GameclientMessageAttack` and `GameclientMessageFollow`.

The promoted evidence correctly treats these as structural/type/template-presence facts only. It does not claim final runtime dispatch, generated field semantics, action serialization, server acceptance or server/client effects.

Likewise, `TCreatureProtocolMessageHandler` has a current QMeta object with zero QMeta methods; no absence claim is made for non-QMeta handler code.

## Accepted task-local coverage

```text
D01 PARTIAL -> PARTIAL
D02 PARTIAL -> PARTIAL
D03 PARTIAL -> PARTIAL
D04 PARTIAL -> PARTIAL
D05 PARTIAL -> PARTIAL
D06 NOT_STARTED -> PARTIAL
D07 NOT_STARTED -> PARTIAL
D08 PARTIAL -> PARTIAL
C15 PARTIAL -> PARTIAL
C16 PARTIAL -> PARTIAL
C17 PARTIAL -> PARTIAL
```

Only D06 and D07 receive a status transition. No row is `DONE`; PR #536 shared coverage files remain untouched.

## Remaining UNKNOWN

- queue -> non-QMeta handler executable dispatch;
- handler -> model/storage mutation dataflow;
- authoritative live creature/HUD/battle-list values;
- exact HUD status/icon schemas;
- exact battle-list filter/sort semantics and persistence;
- target/action -> protocol serialization -> server/client effect causality;
- server acceptance;
- dedicated current-build cancel attack/follow path and live cancellation semantics;
- restart/relogin stability.

## Safety / E2E

No Synology/KasmVNC observation, client execution, credentials, login, gameplay, process-memory access, keyboard/mouse input, attack/follow stimulus or client mutation occurred. Physical E2E is `NOT_APPLICABLE` for this static documentation/evidence promotion.
