# OTC-20260819 Track A feature systems G0 — current-public-package static evidence

```yaml
evidence_date: 2026-08-19
repository: blakinio/otclient
source_task: OTC-20260819-track-a-features-static-g0
source_pr: 560
producer_head: 9ae46d14807e46e76c044c336e50033b11fa3a1e
producer_run: 32229656311
producer_job: 95996576897
artifact_id: 9356800104
artifact_name: track-a-features-static-g0-32229656311
artifact_digest_source: GitHub Actions API
artifact_digest_reported: sha256:779f2d1af266ad0327191a5fda1289a524884c1a9fdb2c4d351d3de3dcaab8d0
runtime_access: none
client_executed: false
credentials_accessed: false
login_attempted: false
gameplay_performed: false
client_byte_mutation: false
raw_client_retained: false
```

## Exact public-package fence

The GitHub-hosted producer fetched the public Linux package and failed closed unless the promoted public-package fingerprint was reproduced:

```text
PACKED_SHA256=1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
UNPACKED_SHA256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
UNPACKED_SIZE=52109920
CURRENT_PUBLIC_PACKAGE_FENCE=PASS
FEATURE_QMETA_CLASSES=61
FEATURE_STRING_LINES=818
FEATURE_PROTOCOL_STRING_LINES=13
RAW_CLIENT_RETAINED=false
```

This fence identifies the exact public package fetched in producer run `32229656311`. It does **not** prove the bytes of a currently installed or canonical live runtime.

The artifact was downloaded with `gh run download` and the extracted text files were independently hashed on the researcher workstation:

```text
features-protocol-strings.txt  936    sha256:c05ed496bddd15f9857b820601daa88b0cf7f0484bc9cd4b048870d6472d628e
features-qmeta.txt             68342  sha256:fb153fed5966e1bebfa6910d9989f38655dd8469dc62d592c7bec0dc0fa11292
features-strings.txt           79170  sha256:267a0e4c7e511276a95b1d9430e84131041b6ec8251a43e7d756ec72afb533dd
fence.txt                      326    sha256:e8f7da77eb41efbbb507103879014dc84c1d80b0efef3de530870361c76cbcbf
```

The GitHub-reported artifact digest above was not independently reproduced as a ZIP digest on Windows; it is retained explicitly as API metadata rather than upgraded into an independent-integrity claim.

## G01 — Cyclopedia shell / request-cache model

Exact Qt metadata in the fetched package establishes:

```text
tibia::cyclopedia::TCyclopediaProtocolMessageHandler
  QMETA=0x30b7f80 STATIC_METACALL=0xd0ecc0 SIGNALS=13 METHODS=32
  sendOpenMonsterCyclopedia
  sendOpenMonsterCyclopediaMonsters
  sendOpenMonsterCyclopediaRace
  sendMonsterBonusEffectAction
  sendCyclopediaMapAction
  sendOpenCyclopediaCharacterInfo
  sendCyclopediaHouseAction
  monsterCyclopediaNewDetailsForMonster
  requestCloseCyclopediaDialog
  handleMonsterCyclopediaMessage
  handleMonsterCyclopediaMonstersMessage
  handleMonsterCyclopediaRaceMessage
  handleMonsterCyclopediaNewDetailsMessage
  handleMonsterCyclopediaBonusEffectsMessage
  handleCyclopediaMapMessage
  handleCyclopediaCharacterInfoMessage
  handleCyclopediaStaticHouseDataMessage
  handleCyclopediaCurrentHouseDataMessage

tibia::gamewindow::TCyclopediaDialogController
  QMETA=0x2f80fe0 STATIC_METACALL=0xd67540 SIGNALS=8 METHODS=17 PROPERTIES=19 ENUMS=1
  dialogTabChanged
  navigationBacklogChanged
  showDialog
  captureNavigationBacklogContextIfNeedAndShowDialog
  closeDialog
  requestClose
  requestTabSwitch
  requestBack
  itemInfoDialogController
  monstersDialogController
  characterInfoDialogController
  bonusEffectsDialogController
  mapDialogController
  housesDialogController
  bosstiaryDialogController
  bossSlotsDialogController
  magicalArchiveDialogController
  dialogTab
  backPossible
  enum DialogTab
```

**FACT:** a dedicated Cyclopedia protocol handler, dialog shell, tab switch/back-navigation surface, per-subsystem controller references and multiple inbound response handlers exist in the exact fetched package.

**INFERENCE:** the handler/controller graph is consistent with a request/response-backed Cyclopedia shell with retained per-tab UI state. It is sufficient for a dedicated structural `G01=PARTIAL` proposal, but it does not prove a cache implementation or lifetime.

**UNKNOWN:** request payload fields, response-to-storage mutation, cache ownership/lifetime, invalidation rules, reconnect/character-switch behavior, exact `DialogTab` values and live navigation causality.

**Next discriminator:** recover generated message schemas plus handler-to-storage writes for one read-only Cyclopedia page, then prove cache reuse/invalidation with deterministic artifact or separately admitted live observation if static proof is exhausted.

## G04 — Bestiary kills / unlocks / loot / progress

Exact metadata establishes:

```text
tibia::cyclopedia::TBestiaryTrackerProtocolMessageHandler
  QMETA=0x30b7fc0 STATIC_METACALL=0xd0eae0 SIGNALS=1 METHODS=2
  sendTrackBestiaryRace
  handleBestiaryTrackerMessage

tibia::cyclopedia::TMonsterRaceStorage
  QMETA=0x30d6c40 STATIC_METACALL=0xd263d0 SIGNALS=4 METHODS=4
  monsterClassificationSummaryChanged
  monsterClassificationMonstersChanged
  monsterRaceDetailsChanged
  monsterRacesUnlockedForCharmsChanged

tibia::gamewindow::TCreatureTrackerWidgetController
  requestOpenBestiary
  requestOpenBestiaryEntry
  trackedCreatures
  widgetMode

tibia::gamewindow::TMonsterDialogController
  requestClassificationSelection
  requestMonsterSearch
  requestClassificationPageSwitch
  requestMonsterPageSwitch
  requestOpenBestiaryTrackerWidget
  requestToggleBestiaryTracking
  onMonsterClassificationSummaryChanged
  onMonsterRacesChanged
  onMonsterRaceDetailsChanged

tibia::gamewindow::TQmlMonsterRace
  raceID
  unlockState
  isFullyUnlocked
  totalKills
  details1Kills
  details2Kills
  details3Kills
  monsterDifficulty
  monsterRarity
  monsterLoot
  hitpointsString
  experienceString
  speedString
  armorString
  mitigationString
  monsterSensitivities
  monsterLocations
```

Exact protocol type strings include `GameserverMessageBestiaryTracker` and `GameclientMessageTrackBestiaryRace`.

**FACT:** the fetched package exposes dedicated Bestiary tracking transport names, race storage notifications, navigation/tracking controls and presentation fields for race ID, unlock state, kill thresholds/progress and loot/details.

**INFERENCE:** this is dedicated evidence beyond broad lexical presence and supports a task-local `G04=PARTIAL` proposal.

**UNKNOWN:** wire field numbers/types, kill-stage thresholds, authoritative server-vs-static field ownership, tracker ordering/limits, response-to-storage mutation code and live update causality.

**Next discriminator:** recover `MonsterCyclopedia*`/`BestiaryTracker` generated-message field schemas and bind at least one server response to `TMonsterRaceStorage` mutation without guessing from names alone.

## G05 — Charms selection / assignment

Exact metadata establishes:

```text
tibia::gamewindow::TMonsterDialogController
  viewSelectedCharm
  removeSelectedCharm
  assignSelectedCharm
  onSelectedCharmChanged

tibia::gamewindow::TQmlMonsterRace
  majorCharm
  minorCharm
  selectedCharmID
  unassignCostString
  canAffordCurrentlySelectedEffectUnassignment
  charmsInCombobox
  indexOfSelectedCharmInCombobox
  selectedCharmSlot
  selectedCharmChanged
  selectedCharmSlotChanged

tibia::gamewindow::TQmlAvailableCharmFilter
  name
  id

tibia::gamewindow::TQmlPreviewCharm
  name
  description
  unlockGrade
  icon
  charmID
  unassignCostInGold
```

Exact package strings include `assignSelectedCharm`, `removeSelectedCharm`, `sendApplyClearingCharm`, and generated type `GameclientMessageApplyClearingCharm`.

**FACT:** read-side charm selection/preview/slot/cost state and explicit assign/remove controller surfaces exist in the exact fetched package; a clearing-charm client message type also exists.

**INFERENCE:** these surfaces support a task-local `G05=PARTIAL` structural proposal.

**UNKNOWN:** assignment/clearing wire fields, server validation, cost formula, slot constraints, persistence, failure behavior and live mutation causality. No charm was assigned, removed, cleared or paid for by this task.

**Next discriminator:** recover generated clearing/assignment message schema and controller-to-message construction with a non-mutating static path; preserve all resource-spend behavior as unexecuted.

## G06 — Monster Bonus Effects

Exact metadata establishes:

```text
tibia::cyclopedia::TMonsterBonusEffectStorage
  QMETA=0x30d6d00 STATIC_METACALL=0xd26180 SIGNALS=7 METHODS=7
  bonusEffectsChanged
  availableCharmPointsChanged
  unlockedCharmPointsChanged
  availableMinorCharmEchoesChanged
  unlockedMinorCharmEchoesChanged
  remainingNumberOfAssignableBonusEffectsChanged
  resetAllCharmCostChanged

tibia::gamewindow::TMonsterBonusEffectsDialogController
  QMETA=0x2f91680 STATIC_METACALL=0xda2c60 SIGNALS=10 METHODS=45 PROPERTIES=23
  unlockBonusEffect
  clearBonusEffect
  assignBonusEffectToMonster
  findMonsterNameByRaceID
  onResetAllCharmsClicked
  canAssignMoreBonusEffects
  selectedBonusEffectId
  resetCostString
  remainingCharms
  numberOfUnlockedCharms
  onMonsterBonusEffectsChangedFromStorage
  onMonsterRacesUnlockedForCharmsChanged
  onRemainingNumberOfAssignableBonusEffectsChanged

tibia::gamewindow::TQmlMonsterBonusEffect
  id
  name
  description
  resourceCostString
  notEnoughResource
  clearCostString
  notEnoughGold
  unlocked
  unlockGrade
  assigned
  assignedMonsterRaceID
  isMinor
```

Exact protocol type strings include `GameclientMessageMonsterBonusEffectAction`; `TCyclopediaProtocolMessageHandler` exposes `sendMonsterBonusEffectAction` and `handleMonsterCyclopediaBonusEffectsMessage`.

**FACT:** the fetched package has distinct storage, dialog, QML state and protocol-action surfaces for bonus-effect availability, unlock, clear, assignment, selected effect, costs and assigned monster race.

**INFERENCE:** this supports a task-local `G06=PARTIAL` proposal while preserving server semantics as unknown.

**UNKNOWN:** action enum/field schema, resource/cost formula, reset/clear/assign validation, response-to-storage mutation, persistence and live success/error transitions. This task executed none of the mutating methods.

**Next discriminator:** recover `MonsterBonusEffectAction` generated-message fields/action variants and bind inbound bonus-effects message fields to storage state statically before considering any separately authorized live read-only correlation.

## Exact protocol strings retained

```text
tibia.protobuf.protocol.GameclientMessageApplyClearingCharm
tibia.protobuf.protocol.GameclientMessageMonsterBonusEffectAction
tibia.protobuf.protocol.GameclientMessageTrackBestiaryRace
tibia.protobuf.protocol.GameserverMessageBestiaryTracker
```

These strings prove generated type presence only; they do not prove wire field semantics or runtime causality.

## Bounded coverage consequence

Against the planning states visible on PR #536 at task start, the researcher proposes only this task-local delta:

```text
G01 Cyclopedia shell/request-cache model        NOT_STARTED -> PARTIAL
G04 Bestiary kills/unlocks/loot/progress        NOT_STARTED -> PARTIAL
G05 Charms selection/assignment                 NOT_STARTED -> PARTIAL
G06 Monster Bonus Effects                       NOT_STARTED -> PARTIAL
```

No shared matrix/checklist file is modified. G02/G03, G07-G23, G24-G31 and G32-G41 remain untouched by this package even when incidental matching class names appeared in the raw census.

`PARTIAL` here means a dedicated exact-fetched-package structural proof package now exists. It does not mean runtime semantics, persistence, wire schema or end-to-end behavior is complete.

## Safety boundary

No current runtime, installed client, account, credential, KasmVNC session, login, gameplay, resource spending, reroll, Forge/Imbuement commit or client-byte mutation was used. Physical E2E is not applicable to this static `runtime_access:none` package.
