# OTCLIENT-TIBIA-RE — feature systems static G0

```yaml
report_date: 2026-08-19
repository: blakinio/otclient
task_id: OTC-20260819-track-a-features-static-g0
source_pr: 560
alias: TIBIA-RE-FEATURES
alias_primary_coverage: G01-G23,G32-G41
bounded_package: G01,G04,G05,G06
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
producer_run: 32229656311
producer_job: 95996576897
producer_artifact: 9356800104
```

## Result

This Draft researcher package adds the first dedicated current-public-package structural evidence for four read-only feature rows without acquiring Track A live-runtime authority.

**FACT:** producer run `32229656311` succeeded on exact head `9ae46d14807e46e76c044c336e50033b11fa3a1e`, reproduced the promoted public-package fingerprint, emitted 61 feature-matched QMeta classes plus 818 feature strings and 13 protocol strings, deleted packed/unpacked client bytes, and uploaded only compact text evidence as artifact `9356800104`.

**FACT:** the exact fetched package contains distinct structural surfaces for:

- Cyclopedia request/response handling, tab/navigation shell and subsystem controllers;
- Bestiary tracker transport, race storage, kill/unlock/loot presentation and tracking controls;
- charm selection/preview/slot/cost state plus explicit assign/remove controller actions;
- Monster Bonus Effects storage, dialog/QML state and client action type, including unlock/clear/assign/cost/assigned-monster fields.

**INFERENCE:** under the status definitions used by PR #536, this dedicated structural evidence is sufficient for the following **task-local proposals only**:

```text
G01 NOT_STARTED -> PARTIAL
G04 NOT_STARTED -> PARTIAL
G05 NOT_STARTED -> PARTIAL
G06 NOT_STARTED -> PARTIAL
```

The researcher does not edit PR #536's shared matrix/checklist and does not promote these proposals into canonical programme state.

## G01 — Cyclopedia shell / request-cache model

Current-public-package evidence binds `TCyclopediaProtocolMessageHandler` to explicit send/handle surfaces for monster Cyclopedia pages, map, character info and houses, while `TCyclopediaDialogController` owns tab switching, back navigation, a `DialogTab` enum and references to monsters/character/bonus-effects/map/houses/Bosstiary/boss-slots/magical-archive controllers.

**FACT:** dedicated request/response and UI-shell ownership exists.

**UNKNOWN:** exact message fields, handler-to-storage writes, cache data structure/lifetime/invalidation, reconnect/character-switch behavior and exact enum values.

Proposed state: `G01=PARTIAL`.

## G04 — Bestiary

Current-public-package evidence binds:

- `TBestiaryTrackerProtocolMessageHandler::{sendTrackBestiaryRace,handleBestiaryTrackerMessage}`;
- `TMonsterRaceStorage` change signals for classification/race details/unlocked-for-charms;
- `TCreatureTrackerWidgetController::{requestOpenBestiary,requestOpenBestiaryEntry}`;
- `TMonsterDialogController` navigation/tracking controls;
- `TQmlMonsterRace` fields including `raceID`, `unlockState`, `isFullyUnlocked`, `totalKills`, three detail-kill counters, `monsterLoot`, difficulty/rarity/stats/sensitivities/locations.

Generated type names include `GameserverMessageBestiaryTracker` and `GameclientMessageTrackBestiaryRace`.

**FACT:** Bestiary kill/unlock/loot/progress and tracker surfaces are structurally separated in the exact fetched package.

**UNKNOWN:** generated field schema, thresholds, authoritative server/static ownership, storage mutation code, tracker limits/order and runtime causality.

Proposed state: `G04=PARTIAL`.

## G05 — Charms

Current-public-package evidence binds `TMonsterDialogController::{viewSelectedCharm,removeSelectedCharm,assignSelectedCharm}` to QML read-side state containing `majorCharm`, `minorCharm`, selected ID/slot, available combobox entries, unassign cost and affordability. `TQmlPreviewCharm` exposes charm ID/name/description/unlock grade/icon/unassign cost, while `TQmlAvailableCharmFilter` exposes charm ID/name.

The package also contains `sendApplyClearingCharm` and generated `GameclientMessageApplyClearingCharm` type names.

**FACT:** charm selection/preview/assignment/removal surfaces are present.

**UNKNOWN:** wire fields, server validation, formulas/constraints, persistence and live success/error behavior. No resource-mutating charm action was executed.

Proposed state: `G05=PARTIAL`.

## G06 — Monster Bonus Effects

`TMonsterBonusEffectStorage` exposes changes to bonus effects, available/unlocked charm points, minor charm echoes, remaining assignable effects and reset cost. `TMonsterBonusEffectsDialogController` exposes unlock/clear/assign operations, selected effect, reset cost, remaining/unlocked charm counts and storage-change callbacks. `TQmlMonsterBonusEffect` exposes resource/clear costs, affordability, unlock grade, assigned state, assigned monster race and major/minor classification. `TCyclopediaProtocolMessageHandler` exposes send/receive surfaces, and generated type `GameclientMessageMonsterBonusEffectAction` is present.

**FACT:** the exact package has distinct read/model/controller/protocol surfaces for the system.

**UNKNOWN:** action enum and generated field schema, resource/cost formulas, server validation, response-to-storage mutation, persistence and live transitions. No unlock/clear/assign/reset action was executed.

Proposed state: `G06=PARTIAL`.

## Scope intentionally not claimed

This package does not claim progress for G02/G03, G07-G23, G24-G31 or G32-G41. Incidental QMeta matches for adjacent systems are census by-products, not evidence packages for those rows.

The complete `TIBIA-RE-FEATURES` alias remains unfinished after this bounded researcher package.

## Validation and provenance

```text
producer run:          32229656311 = SUCCESS
producer job:          95996576897 = SUCCESS
artifact:              9356800104
GitHub-reported digest sha256:779f2d1af266ad0327191a5fda1289a524884c1a9fdb2c4d351d3de3dcaab8d0
public-package fence:  PASS
raw client retained:   false
runtime access:        none
```

Extracted evidence file hashes are recorded in:

`docs/agents/evidence/OTC-20260819-track-a-features-static-g0/20260819-current-package-cyclopedia-bestiary-charms-bonus.md`.

No per-method native target addresses are promoted; this task deliberately avoids the jump-table heuristic rejected by the earlier world/minimap independent audit.

## Researcher handoff

The coordinator should independently audit the final exact Draft PR #560 head. It may accept, edit-promote or reject the four proposed deltas. This researcher branch must remain Draft-only and must not merge or mutate the shared coverage matrix itself.
