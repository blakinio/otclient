# OTCLIENT-TIBIA-RE — creature/combat current-package static G0

```yaml
report_date: 2026-08-19
repository: blakinio/otclient
task_id: OTC-20260819-track-a-creature-combat-static-g0
pr: 558
alias: TIBIA-RE-CREATURE-COMBAT
alias_primary_coverage: D01-D08, C15-C17
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
producer_head: bb0dc3a44a6e5daca2f81817696f91043f8c03d5
producer_run: 32230171183
producer_job: 95998084380
producer_result: success
artifact_id: 9356949168
artifact_digest: sha256:d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7
```

## Result

This bounded researcher package revalidated creature/battle/combat structural surfaces on the current public native-Linux package and closed the dedicated static-evidence gap for `D06` and `D07`.

```text
D06 Creature HUD names/icons/status effects        NOT_STARTED -> PARTIAL
D07 Battle-list filters/sorting/secondary lists   NOT_STARTED -> PARTIAL
```

All other owned rows remain `PARTIAL`. No row becomes `DONE` from this static package, and no shared PR #536 coverage path is edited by the researcher.

Runtime combat semantics, server acceptance, live target causality, authoritative creature values and attack/follow/cancel effects remain `UNKNOWN`/unproven where the row requires `LIVE-STATE` or `LIVE-ACTION`.

## Producer history and repair evidence

The first producer generation `32228647135 / 95993567735` was cancelled while Ubuntu `apt-get` remained in dependency installation for the job timeout. No current package was fetched in that generation; cleanup confirmed no client artifact was retained.

The dependency-light repair removed `apt-get`. Generation `32230003488 / 95997593305` then proved:

```text
PYELFTOOLS_IMPORT=PASS
CURRENT_PACKAGE_FENCE=PASS
current QMeta enumeration=PASS
```

It failed only because `set -o pipefail` treated the intentional `sort -u | head` truncation SIGPIPE as a pipeline error. Cleanup succeeded and retained no raw client.

The second narrow repair removed that truncating pipeline shape. Final generation `32230171183 / 95998084380` passed every producer step, including cleanup and compact artifact upload.

## Current package fence

```text
PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
PACKED_SIZE=10214529
UNPACKED_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
UNPACKED_SIZE=52109920
CURRENT_PACKAGE_FENCE=PASS
RAW_CLIENT_RETAINED=false
```

The downloaded evidence ZIP independently hashes to exactly the GitHub artifact digest and contains only:

```text
creature-combat-qmeta.txt
fence.txt
protocol-strings.txt
semantic-strings.txt
```

## Current-build creature graph

### Creature model/storage/action

Current QMeta directly establishes:

```text
tibia::creatures::TCreature
  positionWasUpdated
  playerKillerMarkChanged
  playerGuildFlagChanged
  playerPartyFlagChanged
  inspectionStateChanged

tibia::creatures::TCreatureProtocolMessageHandler
  0 QMeta methods / 0 signals

tibia::creatures::TCreatureStorage
  playerAdded
  creatureUpdated
  creatureAppearanceUpdated

tibia::creatures::TCreaturesGameActionHandler
  publishGameAction
  sendAttack
  sendFollow
  sendLookAtCreature
  sendInspectPlayer
  party/share-experience actions
```

Current generated-message strings additionally retain `GameserverMessageCreatureData`, `CreatureUpdate`, `CreatureHealth`, `CreatureLight`, `CreatureMarks`, `CreatureOutfit`, `CreatureParty`, `CreatureSkull`, `CreatureSpeed`, `CreatureType`, `CreatureUnpass`, plus `GameclientMessageAttack` and `GameclientMessageFollow`.

For the server creature families, the artifact also retains `TProtocolMessageQueue::registerServerMessage<...>` instantiations.

This strengthens current-build structural provenance for `D01`, `D04`, `D05`, `C15` and `C16`, but does not prove runtime values or action effects.

### D06 — Creature HUD

Current QMeta directly establishes:

```text
tibia::worldmap::TCreatureHUDOverlayController
  refreshCreatureHUDs
  update

tibia::worldmap::TCreatureHUDQmlRenderInfo
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

The neutral static corpus also contains `CreatureHUD.qml` and the matching HUD type names.

**FACT:** name, health, icon, special-condition and status-effect HUD surfaces exist in the exact current package.

**INFERENCE:** this dedicated current-build evidence is sufficient for `D06 NOT_STARTED -> PARTIAL` under the PR #536 status contract.

**UNKNOWN:** authoritative provider/storage, status-effect schema/IDs, icon ordering and causal live updates remain unproven.

### D07 — Battle lists

Current QMeta directly establishes:

```text
tibia::gamewindow::TBattleListController
  onFilterButtonsVisibleClicked
  isFilterActive
  toggleFilter
  requestOpenSecondaryBattleList
  requestMakePrimary
  onCurrentlyHoveredCreatureChanged
  onCreatureClicked
  onCreatureTargetSelected

tibia::gamewindow::TBattleListControllerStorage
  battleListRemovedFromStorage
  widgetVisible
  widgetHidden
  triggerUpdate
  onLoginRampUpFinished
  onBattleListClosed

tibia::gamewindow::TBattleListDataModel

tibia::gamewindow::TBattleListGameActionHandler
  handleAttackFirstTargetGameAction
  handleAttackNextTargetGameAction
  handleAttackPreviousTargetGameAction
  attackFirstTarget
  attackNextOrPreviousTarget
  filterDrawCommands
  sortDrawCommands
```

Neutral current-package strings also include `BattleListWidgetOptions`, `EBattleListWidgetFilterKey`, `TBattleListDataModelSortFilterProxy`, `OpenSecondaryBattleList` and the dedicated secondary-battle-list game-action type.

**FACT:** dedicated filter, sort, secondary-list and target-selection structural surfaces exist in the exact current package.

**INFERENCE:** this is sufficient for `D07 NOT_STARTED -> PARTIAL`.

**UNKNOWN:** exact filter enum meanings, sort criteria/tie-breaking, live membership and secondary-list persistence remain unproven.

## D08 / C15-C17 action boundary

Current-package evidence includes:

```text
TBattleListController::onCreatureTargetSelected
TBattleListGameActionHandler::attackFirstTarget
TBattleListGameActionHandler::attackNextOrPreviousTarget
TCreaturesGameActionHandler::sendAttack
TCreaturesGameActionHandler::sendFollow
GameclientMessageAttack
GameclientMessageFollow
```

Neutral strings retain `AttackFirstTarget`, `AttackNextTarget`, `AttackPreviousTarget` and their game-action types.

This strengthens current-build structural evidence for `D08`, `C15` and `C16`, but those rows remain `PARTIAL` because target/action -> exact receiver/protocol serialization -> server/client effect is not proven here.

No dedicated current-build cancel-attack/follow structural name was recovered by this bounded filter. That absence is not negative proof. `C17` therefore remains `PARTIAL` from prior evidence without a new current-build semantic promotion.

## Row-by-row disposition

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

Exact remaining gates:

```text
D01-D05: LIVE-STATE plus exact non-QMeta dispatch/dataflow where applicable
D06: authoritative HUD provider/schema + causal live state
D07: exact filter/sort semantics + live membership/persistence
D08/C15/C16: LIVE-ACTION action->protocol->effect causality
C17: dedicated current-build cancel discriminator + LIVE-ACTION
```

## Safety and isolation

```yaml
client_executed: false
runtime_observed: false
synology_runtime_observed: false
kasmvnc_observed: false
credentials_accessed: false
login_attempted: false
gameplay_performed: false
attack_or_follow_stimulus: false
process_memory_accessed: false
client_byte_mutation: false
raw_client_uploaded: false
raw_client_retained: false
```

PR #528/#550 physical runtime, PR #536 shared coverage files, PR #539/S10 paths and PR #540 spawn/mechanics paths were not modified.

E2E: `NOT_APPLICABLE` — this is a static `runtime_access: none` reverse-engineering package. Physical combat E2E would be a separate later task under current runtime admission and ownership.

## Durable evidence

- `docs/agents/evidence/OTC-20260819-track-a-creature-combat-static-g0/20260819-current-package-creature-combat.md`
- final successful run `32230171183`, job `95998084380`, artifact `9356949168`
- artifact SHA-256 `d08fba81bbb41ef2f18e6967163ad59c6883b31392836104253c2a4e2f8abbf7`

The temporary producer workflow was removed before final Draft-head validation. Researcher delivery remains Draft-only and not canonically promoted until coordinator review.
