# OTC-20260819 Track A creature/combat G0 — current-package static evidence

```yaml
evidence_date: 2026-08-19
repository: blakinio/otclient
task_id: OTC-20260819-track-a-creature-combat-static-g0
pr: 558
alias: TIBIA-RE-CREATURE-COMBAT
producer_head: bb0dc3a44a6e5daca2f81817696f91043f8c03d5
workflow_run: 32230171183
job: 95998084380
artifact_id: 9356949168
artifact_name: track-a-creature-combat-static-g0-32230171183
artifact_digest: sha256:d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7
artifact_size_bytes: 16785
runtime_access: none
client_executed: false
credentials_accessed: false
login_attempted: false
gameplay_performed: false
client_byte_mutation: false
raw_client_retained: false
```

## Artifact verification

The downloaded GitHub Actions ZIP was independently hashed before reading its contents.

```text
ZIP_SHA256=d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7
FILES=4
creature-combat-qmeta.txt=8593 bytes
fence.txt=310 bytes
protocol-strings.txt=15241 bytes
semantic-strings.txt=119513 bytes
```

The ZIP digest exactly matches GitHub artifact metadata. No packed or unpacked client bytes are present.

## Exact current public package fence

```text
PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
PACKED_SIZE=10214529
UNPACKED_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
UNPACKED_SIZE=52109920
CURRENT_PACKAGE_FENCE=PASS
SEMANTIC_STRING_LINES=1200
PROTOCOL_STRING_LINES=226
RAW_CLIENT_RETAINED=false
```

**FACT:** the producer analyzed the current public native-Linux package fenced by the exact packed/unpacked hash and size above, then deleted both packed and unpacked client bytes before evidence upload.

## Creature model/storage/action QMeta

Current-package QMeta ownership includes:

```text
CLASS=tibia::creatures::TCreature
QMETA=0x30af0e0 STATIC=0xd0a530 SIGNALS=5 METHODS=5
  positionWasUpdated
  playerKillerMarkChanged
  playerGuildFlagChanged
  playerPartyFlagChanged
  inspectionStateChanged

CLASS=tibia::creatures::TCreatureProtocolMessageHandler
QMETA=0x30f2880 STATIC=0xd03760 SIGNALS=0 METHODS=0

CLASS=tibia::creatures::TCreatureStorage
QMETA=0x30b8400 STATIC=0xd19b30 SIGNALS=3 METHODS=3
  playerAdded
  creatureUpdated
  creatureAppearanceUpdated

CLASS=tibia::creatures::TCreaturesGameActionHandler
QMETA=0x30b7940 STATIC=0xd0a910 SIGNALS=13 METHODS=13
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

**FACT:** current-build creature object, storage and native creature-action QMeta surfaces exist.

**FACT:** the current-build `TCreatureProtocolMessageHandler` QMeta object has zero QMeta methods/signals. This preserves the historical S8 warning: QMeta absence does not prove absence of non-QMeta handler code.

**UNKNOWN:** exact queue -> non-QMeta handler executable dispatch and exact handler -> storage/model mutation dataflow are not established by this G0.

## Current generated creature protocol families

The retained current-package strings contain generated protobuf types and `TProtocolMessageQueue::registerServerMessage` instantiations for:

```text
GameserverMessageCreatureData
GameserverMessageCreatureUpdate
GameserverMessageCreatureHealth
GameserverMessageCreatureLight
GameserverMessageCreatureMarks
GameserverMessageCreatureOutfit
GameserverMessageCreatureParty
GameserverMessageCreatureSkull
GameserverMessageCreatureSpeed
GameserverMessageCreatureType
GameserverMessageCreatureUnpass
```

Client-to-server combat protobuf names retained by the same artifact include:

```text
GameclientMessageAttack
GameclientMessageFollow
```

**FACT:** these exact generated message families are present in the current package. For the server creature families, the retained strings also include the queue registration template instantiations.

**UNKNOWN:** this package does not prove each message's field semantics, runtime values, final dispatch target, or server-side acceptance/effect.

## D06 — Creature HUD names/icons/status effects

Current-package QMeta establishes a dedicated HUD surface:

```text
CLASS=tibia::worldmap::TCreatureHUDOverlayController
QMETA=0x30f7fe0 STATIC=0xe030a0 SIGNALS=0 METHODS=2
  refreshCreatureHUDs
  update

CLASS=tibia::worldmap::TCreatureHUDQmlRenderInfo
QMETA=0x30f8060 STATIC=0xe16080 SIGNALS=19 METHODS=19
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

Neutral current-package strings also retain `CreatureHUD.qml` and the matching HUD class/type names.

**FACT:** current-package HUD render-info ownership explicitly exposes creature name, health, horizontal/vertical icons, special conditions and status-effect change surfaces.

**INFERENCE:** this is a dedicated exact-current-build semantic package sufficient to move coverage row `D06` from `NOT_STARTED` to `PARTIAL`, but not to `DONE`.

**UNKNOWN:** exact status-effect IDs/schema, icon ordering/source, authoritative storage provider, runtime values and update causality remain unproven.

## D07 — Battle-list filters/sorting/secondary lists

Current-package QMeta establishes:

```text
CLASS=tibia::gamewindow::TBattleListController
QMETA=0x2f92880 STATIC=0xd3beb0 SIGNALS=3 METHODS=23
  onFilterButtonsVisibleClicked
  isFilterActive
  toggleFilter
  requestOpenSecondaryBattleList
  requestMakePrimary
  onCurrentlyHoveredCreatureChanged
  onCreatureClicked
  onCreatureTargetSelected

CLASS=tibia::gamewindow::TBattleListControllerStorage
QMETA=0x30cb620 STATIC=0xd2f3c0 SIGNALS=4 METHODS=8
  battleListRemovedFromStorage
  widgetVisible
  widgetHidden
  triggerUpdate
  onLoginRampUpFinished
  onBattleListClosed

CLASS=tibia::gamewindow::TBattleListDataModel
QMETA=0x30f3280 STATIC=0xd25390 SIGNALS=0 METHODS=0

CLASS=tibia::gamewindow::TBattleListGameActionHandler
QMETA=0x30ba540 STATIC=0xd46960 SIGNALS=1 METHODS=11
  handleAttackFirstTargetGameAction
  handleAttackNextTargetGameAction
  handleAttackPreviousTargetGameAction
  attackFirstTarget
  attackNextOrPreviousTarget
  filterDrawCommands
  sortDrawCommands
```

Neutral current-package strings additionally include:

```text
BattleListWidgetOptions
EBattleListWidgetFilterKey
N5tibia10gamewindow35TBattleListDataModelSortFilterProxyE
N5tibia5input51TGameActionOpenSecondaryBattleListInSpecificSidebarE
OpenSecondaryBattleList
```

**FACT:** a dedicated current-build battle-list controller/storage/data-model surface exists with explicit filter toggling, secondary-list opening, and draw-command filter/sort methods.

**INFERENCE:** this dedicated exact-current-build package is sufficient to move `D07` from `NOT_STARTED` to `PARTIAL`, but not to `DONE`.

**UNKNOWN:** exact filter enum semantics, sort criteria and tie-breaking, membership rules, secondary-list persistence and live list contents are not proven.

## D08 and C15-C17 combat/target controls

Current-build static evidence includes:

```text
TBattleListController::onCreatureTargetSelected
TBattleListGameActionHandler::handleAttackFirstTargetGameAction
TBattleListGameActionHandler::handleAttackNextTargetGameAction
TBattleListGameActionHandler::handleAttackPreviousTargetGameAction
TBattleListGameActionHandler::attackFirstTarget
TBattleListGameActionHandler::attackNextOrPreviousTarget
TCreaturesGameActionHandler::sendAttack
TCreaturesGameActionHandler::sendFollow
GameclientMessageAttack
GameclientMessageFollow
```

Neutral strings also retain `AttackFirstTarget`, `AttackNextTarget`, `AttackPreviousTarget` and their game-action types.

**FACT:** target-selection plus attack/follow structural surfaces are present in the current package.

**UNKNOWN:** target selection -> exact action receiver -> protocol serialization -> server/client effect is not proven here. This G0 does not overlap PR #539/S10 ownership and performs no gameplay input.

**UNKNOWN:** no dedicated current-build cancel-attack/follow structural name was recovered by this bounded filter. Absence from this artifact is not negative proof; `C17` remains supported only by prior bounded evidence until a dedicated current-build discriminator proves the cancellation path.

## Coverage consequence

Against the PR #536 row-status contract:

```text
D01 PARTIAL -> PARTIAL (current generated family corroboration; live queue semantics still missing)
D02 PARTIAL -> PARTIAL (current handler QMeta present; non-QMeta dispatch remains UNKNOWN)
D03 PARTIAL -> PARTIAL (current storage surface present; handler->mutation dataflow UNKNOWN)
D04 PARTIAL -> PARTIAL (current storage/lifecycle signals strengthened; live registry semantics UNKNOWN)
D05 PARTIAL -> PARTIAL (current state message families strengthened; authoritative live fields UNKNOWN)
D06 NOT_STARTED -> PARTIAL (dedicated current HUD QMeta/render-info package)
D07 NOT_STARTED -> PARTIAL (dedicated current battle-list/filter/sort/secondary-list package)
D08 PARTIAL -> PARTIAL (current target-selection/first-next-previous structure; LIVE-ACTION missing)
C15 PARTIAL -> PARTIAL (current sendAttack + GameclientMessageAttack; LIVE-ACTION missing)
C16 PARTIAL -> PARTIAL (current sendFollow + GameclientMessageFollow; LIVE-ACTION missing)
C17 PARTIAL -> PARTIAL (no new dedicated cancel proof; prior partial evidence only)
```

No row is `DONE` from this static package. Shared PR #536 coverage files are intentionally untouched; only the coordinator may promote accepted row deltas into canonical programme state.

## Negative controls and side effects

```yaml
synology_runtime_observed: false
kasmvnc_observed: false
process_memory_accessed: false
keyboard_mouse_input: false
login: false
credentials: false
gameplay: false
attack_or_follow_stimulus: false
client_executed: false
client_mutated: false
raw_client_uploaded: false
raw_client_retained: false
```

E2E: `NOT_APPLICABLE` — this is a `runtime_access: none` static reverse-engineering evidence package. Runtime combat causality remains a separate future gate.
