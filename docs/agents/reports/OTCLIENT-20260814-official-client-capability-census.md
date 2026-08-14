# OTCLIENT-TIBIA-RE official-client capability census

```yaml
track: official-client-re
subject: official native Linux Tibia client only
repository: blakinio/otclient
evidence_class: exact-binary static inventory plus existing version-fenced runtime evidence
researched_client_version: 15.32.df7b29
researched_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Purpose and evidence boundary

This report converts the broad static inventories already produced from the exact researched official Linux Tibia binary into a durable capability census for the Track A experiment sweep.

`STATIC_PRESENT` below means that a named QMeta class/method, generated protocol message, storage/controller or related semantic surface was recovered from the exact researched binary. It does **not** prove that the method is a normal live call site, that its ABI is fully understood, that a server accepts an action, or that the same location/shape exists in a newer client. Live capability promotion still requires the canonical G0-G4 evidence gates and current-version revalidation.

Do not reuse runtime addresses, heap pointers, PIDs or PIE bases from older runs. Static offsets are version-fenced leads only.

## Provenance

| Inventory | Run | Job | Result | Material result |
|---|---:|---:|---|---|
| capability QMeta inventory | `31651155741` | `94295569820` | PASS | 494 capability method hits, 460 direct QMeta dispatch targets in the exact-binary inventory |
| generated protocol inventory | `31651220862` | `94295767215` | PASS | 349 generated message symbols: 160 client->server, 189 server->client; 98 matched the original capability regex |
| high-level action QMeta inventory | `31651684700` | `94297172395` | PASS | direct log marker `HIGHLEVEL_ACTION_METHOD_COUNT=612` for the action-regex inventory |
| targeted state/update inventory | `31652393473` | `94299386259` | PASS | 121 targeted state/read/update method hits |
| action signature inventory | `31651501473` | `94296624884` | PASS | metadata correspondence for movement/rotate/attack/follow/use/move/talk/container action families |

### Count discrepancy

An older durable summary referred to 1004 high-level action methods. The direct retained log for run `31651684700` reports `HIGHLEVEL_ACTION_METHOD_COUNT=612`. Treat the values as different inventory/filter-count definitions until the old 1004 provenance is reconstructed. Do not use 1004 as the direct count for this run.

## Protocol coverage gap

The protocol inventory found exactly:

```text
PROTOCOL_MESSAGE_TOTAL=349
CLIENT_TO_SERVER_MESSAGE_SYMBOLS=160
SERVER_TO_CLIENT_MESSAGE_SYMBOLS=189
PROTOCOL_CAPABILITY_MESSAGE_COUNT=98
```

The 98 capability entries were selected by a deliberately narrow regex. Therefore **251 generated message names were not classified by that experiment**. A complete unfiltered census of all 349 generated message symbols is a mandatory follow-up; absence from the 98-name list is not evidence that a feature is absent.

## Exact generated-message surfaces already recovered

### Client to server

The filtered exact-binary inventory includes:

- session/world: `GameclientMessageEnterWorld`;
- movement: `GoNorth`, `GoEast`, `GoSouth`, `GoWest`, all diagonals, `GoPath`, `Stop`, `Cancel`, `RotateNorth/East/South/West`;
- combat: `Attack`, `Follow`;
- object interaction: `BrowseField`, `UseObject`, `UseTwoObjects`, `UseOnCreature`, `MoveObject`;
- containers: `CloseContainer`, `OpenParentContainer`, `SeekInContainer`, `UpContainer`, `ContainerAction`, `ManagedContainer`;
- chat/channels: `Talk`, `GetChannels`, `OpenChannel`, `JoinChannel`, `LeaveChannel`, `PrivateChannel`, `InviteToChannel`, `ExcludeFromChannel`, `CloseNPCChannel`;
- inspection/social: `InspectPlayer`, `LookAtCreature`;
- Skill Wheel: `RequestSkillWheel`, `ApplySkillWheel`;
- Cyclopedia: `CyclopediaMapAction`, `CyclopediaHouseAction`;
- Market: `MarketCancel`;
- monster bonus effects: `MonsterBonusEffectAction`;
- creature podium: `SetCreaturePodiumConfiguration`.

The targeted state inventory additionally exposed a version-fenced QMeta outbound surface named `sendShareExperience`, plus `sendToggleWrapState`, `sendSoulSealsFightMonsterMessage`, `sendSetVocationMessage` and Skill Wheel/Cyclopedia actions. `sendShareExperience` is strong static evidence for a party shared-experience action surface; its live ABI/result remains to be proven.

### Server to client

The filtered inventory includes:

- world/map: `WorldEntered`, `FullMap`, `FieldData`, `CreateOnMap`, `ChangeOnMap`, `DeleteOnMap`, `MoveCreature`, `Stop`;
- creatures: `CreatureData`, `CreatureUpdate`, `CreatureHealth`, `CreatureLight`, `CreatureMarks`, `CreatureOutfit`, `CreatureParty`, `CreatureSkull`, `CreatureSpeed`, `CreatureType`, `CreatureUnpass`;
- inventory/containers: `PlayerInventory`, `SetInventory`, `DeleteInventory`, `Container`, `CreateInContainer`, `ChangeInContainer`, `DeleteInContainer`, `CloseContainer`, `UpdateManagedContainers`, `SpecialContainersAvailable`;
- player state: `PlayerDataBasic`, `PlayerDataCurrent`, `VocationSpecificPlayerData`, `PlayerGoods`, `PlayerSkills`, `PlayerState`;
- chat/channels: `Talk`, `Channels`, `OpenChannel`, `OpenOwnChannel`, `CloseChannel`, `PrivateChannel`, `ChannelEvent`, `NpcTalkParters`;
- cooldown: `MultiUseDelay`;
- Cyclopedia/houses: `CyclopediaMapData`, current/static house data and house-action result;
- monster bonus effects: `MonsterCyclopediaBonusEffects`;
- Skill Wheel: `SkillWheel`;
- creature podium: `ConfigureCreaturePodium`.

## Evidence-derived client subsystem census

The following groups are directly evidenced by exact-binary class/method/storage names and should be included in the live experiment programme.

### Session, authentication, disconnect and safety state — STATIC_PRESENT

Observed surfaces include:

- `TAuthenticationProcessController`, including returner-reward state;
- `TCharacterSelectionController`, including autoclose/prevent-autoclose state;
- login confirmation-code and two-factor dialog controllers;
- `TGameSessionDisconnectReactionController`;
- `TServerModalDialogProtocolMessageHandler::openModalDialog(TServerModalDialogData)`;
- `TGameProtocolMessageHandler::requestOpenDeathDialog(EDeathType, TFairFightFactor, ...)`;
- `TDeathDialogController`;
- logout confirmation in `TButtonBarController`;
- `TGameClient` close/session movement-wakeup surfaces;
- `TAntiCheatController::requestCloseDueToClientCheck` and corresponding close request.

Research anti-cheat-related symbols only as passive safety/session evidence. Never use this work to disable or bypass client checks.

Experiment targets: structured login state, pending/world-entered, server modal dialogs, disconnect reason/reaction, death type/fair-fight data, logout confirmation, close requests, reconnect/recovery and imminent-session-loss signals.

### Player state, skills, conditions and cooldowns — STATIC_PRESENT

Targeted QMeta/state inventories exposed:

- `TPlayerData` and player-data message families;
- vocation changes;
- HP, max HP, mana and max mana state/update surfaces;
- `TPlayerSkillStats` / `GameserverMessagePlayerSkills`;
- soul points, capacity and player-state changes in `TPlayerInventoryAndStatusController`;
- resting-area state;
- mana-shield state in `TStatusBarController`;
- `TCooldownStorage`, including multi-use cooldown changes;
- creature HUD `statusEffectsChanged`.

Experiment targets: authoritative values, base/effective skills, state flags, buff/debuff IDs/lifetimes, mana shield, resting areas, cooldown groups and action exhaustion.

### Movement and pathing — STATIC_PRESENT with prior native-action leads

Exact message/action families include all eight movement directions, `GoPath`, stop/cancel and four rotations. Existing Track A evidence already provides version-fenced native-method leads for these families.

Experiment targets: authoritative before/after coordinates, autowalk/path state, stop/cancel semantics, path rejection and restart-stable resolver.

### Creatures, HUD and battle lists — STATIC_PRESENT

Observed:

- `TCreatureStorage::creatureUpdated` and `creatureAppearanceUpdated`;
- inbound creature data/update/health/light/marks/outfit/party/skull/speed/type/unpass;
- `TCreatureHUDOverlayController` and `TCreatureHUDQmlRenderInfo`, including name/icons/status effects;
- `TBattleListController`, including hovered creature, creature click and target selection;
- secondary battle lists;
- `TBattleListGameActionHandler::attackFirstTarget` and `attackNextOrPreviousTarget`;
- attack/follow generated messages.

Experiment targets: central creature registry, lifecycle/events, classification, battle-list filtering/sorting, first/next target selection, attacked/followed target and HUD state.

### Combat modes and PvP state — STATIC_PRESENT

`TPlayerInventoryAndStatusController` exposes at least a `onPvPModeYellowHandRequested` surface, while player-state messages and combat action handlers are present.

Experiment targets: all currently supported combat/PvP modes, local-vs-server authority and mode-change message paths.

### Inventory, object metadata and equipment — STATIC_PRESENT

Observed:

- inventory update storage/controller surfaces;
- `TObjectAppearanceInstanceInfoStorage::objectInfosChanged`;
- `TObjectCountStorage::objectCountsChanged`;
- `TAppearanceTypeListModel` changes for item price, item tracking, object counts and object proficiency XP;
- `TAppearanceTypeHelperQmlService` with exact semantic helper methods:
  - `getObjectAppearanceTypeNameForID`;
  - `getObjectAppearanceTypeDescriptionForID`;
  - `getObjectAppearanceTypeIDByName`.

The appearance helper is a high-value semantic metadata surface and should be tested early.

Experiment targets: equipment slots, item IDs/appearance IDs, count/subtype/tier/charges/duration, name/description lookup, proficiency XP and stable object metadata.

### Containers, stash, depot search and managed containers — STATIC_PRESENT

`TContainerProtocolMessageHandler` exposes close/up/next-page/previous-page/update, object-info requests, sort and move-content-to-managed-container operations. Other observed surfaces include:

- `TContainerStorage::containerUpdated/containerRemoved`;
- `TInventoryContainer::inventoryChanged`;
- stash open/close request surfaces;
- depot-search widget open/close and item selection;
- `TManagedContainerStorage`;
- special/managed-container inbound messages.

Experiment targets: complete open-container registry, parent hierarchy, pagination, sort criteria, stash/depot search, managed-container configuration and semantic object-info lookup.

### Quick loot and obtain containers — STATIC_PRESENT

`TLootContainerQMLInfo` exposes state and actions for loot and obtain containers by object category: select, clear and open. `TManageLootContainerDialogController` exposes whitelist/blacklist and container-management state.

Experiment targets: loot container assignments, obtain containers, fallback backpack, blacklist/whitelist, safe open/select/clear semantics and received managed-container updates.

### Loot tracking, gain/waste and hunting telemetry — STATIC_PRESENT

Observed:

- `TGainWasteStorage`: looted items, wasted items and metrics;
- `TItemTrackingStorage::itemDropTracked(TTrackedItem, TDroppedLoot)` and recent loot changes;
- `TLootTrackingWidgetController`;
- `TLootAndWasteWidgetController`;
- `THuntingSessionWidgetController`.

Experiment targets: whether these values are client-derived or server-originated, exact item/value/metric schemas and normalized agent telemetry.

### Full analyzer suite — STATIC_PRESENT

`TSidebarWidgetsManager` names these analyzer widgets explicitly:

- Loot Analyzer;
- Waste Analyzer;
- Impact Analyzer;
- Damage Input Analyzer;
- Hunting Session Analyzer;
- Progress Analyzer;
- Analytics Selector;
- Party Hunt Analyzer.

These should receive a dedicated state census because they may expose already-normalized combat, supply, XP and party-hunt metrics.

### Player-to-player trade — STATIC_PRESENT

Strong exact-binary evidence:

- `TPlayerTradeProtocolMessageHandler::requestOpenPlayerTradeWidget` / `requestClosePlayerTradeWidget`;
- `TPlayerTradeObject::itemChanged`;
- `TPlayerTradeController::lookOwnTradeSide` / `lookCounterOfferTradeSide`;
- sidebar trade widget open/close requests.

Experiment targets: request/partner identity, own/counteroffer item models, changes, look, accept/reject/cancel message families and completed/cancelled states. Mutating/acceptance tests must use harmless reversible controlled conditions.

### NPC interaction and NPC trade — STATIC_PRESENT

Observed:

- NPC talk partner storage/dialog changes;
- NPC-channel availability/removal;
- `TNPCTradeProtocolMessageHandler` open/close;
- `TNPCTradeStorage` player/trader inventory changes;
- `TNPCTradeController`: buy/sell switching, object selection, object context menu and look selected goods.

Experiment targets: NPC semantic dialog/options, trader offers, prices/counts, buy/sell paths and inventory result. Read-only/preview first.

### Chat, channels, private channels and channel moderation — STATIC_PRESENT

Observed client state/action surfaces cover:

- current available channels;
- channel open/reopen/remove and entry-added events;
- current/next/previous channel tabs;
- request channel list;
- private channel opening;
- invite/exclude player names;
- join/leave/open/close messages;
- talk and NPC channel close;
- white/blacklist UI and Exiva options.

Experiment targets: normalized incoming/outgoing message model, channel IDs/names/types, unread/current/secondary channels, private/NPC channels, invite/exclude and all server/system message categories.

### Friends, Social and VIP — STATIC_PRESENT

Observed:

- `TFriendsProtocolMessageHandler`;
- `TFriendsAccountSearchPageController`;
- `TSocialDialogController`;
- `TVipStorage` and `TVipWidgetDataModel` removal events;
- `TEditVipDialogController`;
- white/blacklist configuration.

Experiment targets: friend search, saved contacts/VIP identity, online/offline state where available, groups/icons/descriptions/notifications and add/edit/remove action paths without disturbing unrelated players.

### Party/shared experience — STATIC_PRESENT lead

The targeted QMeta inventory includes `sendShareExperience`, and the inbound protocol inventory includes `GameserverMessageCreatureParty`. This is direct static evidence that party/share-exp semantics exist in the binary, although the complete invite/join/leave/pass-leadership ABI was not established by the retained filtered logs.

Mandatory follow-up: unfiltered QMeta/protocol census specifically for `Party`, `Invite`, `Join`, `Leave`, `Leadership`, `Shared`, `Experience`, `Shield`, `Member` and related names, then live safe correlation.

### Cyclopedia shell and map — STATIC_PRESENT

Observed:

- `TCyclopediaProtocolMessageHandler`;
- `TCyclopediaMapStorage`;
- Cyclopedia map dialog selection/creature-click/minimap renderer;
- generated Cyclopedia map/house messages/actions.

Experiment targets: generic Cyclopedia request/cache model, active page/tab and reusable data/controller boundaries.

### Bestiary and charms — STATIC_PRESENT

Observed:

- creature tracker `requestOpenBestiary` and `requestOpenBestiaryEntry`;
- `TMonsterDialogController::requestOpenBestiaryTrackerWidget`;
- `removeSelectedCharm`;
- monster bonus-effect storage/controller families that may represent current bonus/charm-like systems.

Experiment targets: race IDs, kills, unlock stages, loot/progress, selected charm/bonus assignment, cache lifetime and server-vs-static metadata. Do not spend/reset character resources merely for proof.

### Monster bonus effects — STATIC_PRESENT

`TMonsterBonusEffectStorage` and `TMonsterBonusEffectsDialogController` expose changed state, remaining assignable effects, unlock, clear, assign-to-monster, selected-effect state and a generated `MonsterBonusEffectAction` message.

This deserves a separate experiment group rather than being folded into generic Bestiary.

### Bosstiary and boss difficulty — STATIC_PRESENT

Observed:

- Boss Tracker and Bosstiary open actions;
- `TBossDifficultySelectionProtocolMessageHandler` with dialog data;
- boss difficulty-selection controller.

Experiment targets: boss IDs/progress/slots and difficulty-selection semantics where current character/context permits safe read-only testing.

### Prey — STATIC_PRESENT

Observed `TPreyDialogController`, `TPreyRenderInfo`, grid/Bestiary prey-creature selection and Kill Tracker action to open Prey.

Experiment targets: slots, race IDs, bonus type/strength, remaining time, reroll/free-reroll/card/cost state. Do not spend resources for proof.

### Taskboard, Bounty Tasks, Weekly Tasks and Soul Seals — STATIC_PRESENT

Observed:

- Kill Tracker actions to open Bounty Tasks and Weekly Tasks;
- `TTaskboardDialogController`;
- `TTaskboardProtocolMessageHandler::openSoulSealsDialog(vector<TMonsterRaceID>)`;
- `TSoulSealsDialogController`;
- `TWeeklyTasksController`, including delivery-item click;
- a taskboard reward purchase confirmation controller.

Experiment targets: task IDs/progress/rewards, bounty/weekly state, Soul Seal monster IDs and request/response/actions. Purchase/paid paths remain read-only unless explicitly authorized.

### Skill Wheel, gems and presets — STATIC_PRESENT

Observed:

- generated `RequestSkillWheel`, `ApplySkillWheel`, `GameserverMessageSkillWheel`;
- `TSkillWheelGameActionHandler` and `TSkillWheelStorage`;
- `TSkillWheelDialogController` and page controller;
- remove-from-skill and use-server-wheel-as-current methods;
- Skill Wheel preset-management controller;
- gem inventory changes and `TGemAtelierPageController`.

Experiment targets: nodes/slices/points/prerequisites/perks/revelation/gems/presets/server-vs-preview configuration. Do not commit/reset valuable configuration merely for proof.

### Exaltation Forge — STATIC_PRESENT

Observed:

- `TExaltationForgeDialogController`;
- Fusion page: fusion/resource object selection and preview/open-dialog preparation;
- Transfer page: source/target state and preview/open-dialog preparation;
- result-dialog controller.

Experiment targets: dust/slivers/cores, item class/tier, fusion/transfer/convergence eligibility, costs/chances/previews and server requests. No actual valuable fusion/transfer for proof.

### Imbuements — STATIC_PRESENT

Observed `TImbuementDurationsStorage::imbuedObjectsChanged`, Imbuement Tracker and Imbuing dialog/protocol handler.

Experiment targets: imbued object IDs, slot/imbuement/tier/duration/remaining time and cost/material preview. Avoid resource consumption.

### Weapon Proficiency — STATIC_PRESENT

Observed:

- Character Info and Inspect dialogs can open weapon proficiency;
- `TWeaponProficiencyDialogController` with weapon selection and inspect-object data;
- reshape/shape/options controllers;
- object-proficiency XP change in appearance list model.

Experiment targets: proficiency state, weapon IDs, XP/progress, shapes/options and preview vs committed server state. Avoid irreversible reshaping.

### Market — STATIC_PRESENT

Observed:

- `TMarketController`: item/category selection, offer cancel, history, own offers and item details;
- `TMarketProtocolMessageHandler` open/close;
- `TMarketStorage::marketItemDetailsChanged`;
- generated `MarketCancel` in the filtered protocol inventory.

Experiment targets: complete request/response catalogue, offers/history/statistics/prices/amount/pagination/filter/sort, balances when supplied. Read-only; never create/accept offers for proof.

### Store and coin transaction UI — STATIC_PRESENT

Observed Store protocol/controller, purchase confirmation/success dialogs, transaction-history opening and coin-transaction details dialog.

Research only read-only product/category/balance/preview/transaction-history state. Never purchase anything for an experiment.

### Daily Reward, Reward Wall, resting bonuses and returner state — STATIC_PRESENT

Observed:

- Daily Reward item-pick controller;
- Reward Wall resting-area bonuses;
- fixed-item and pick-item collection request surfaces;
- `TNewsStorage::returnerInformationChanged`;
- authentication returner-reward state.

Experiment targets: streak/reward/calendar/claimability/resting/returner state. Do not consume strategically important rewards merely for proof.

### Quest Log and Quest Tracker — STATIC_PRESENT

Observed `TQuestLogController` and `TQuestTrackerWidgetController::requestOpenQuestLogDialog`.

Experiment targets: quest/mission IDs, state, description/progress, tracker entries and request/cache behavior.

### Houses and Cyclopedia house actions — STATIC_PRESENT

Observed:

- `THousesStorage`: house info, character houses, limits;
- Cyclopedia static/current house data and action-result messages;
- `THousesInfoDialogController`: filters, selected house, world-map viewport, move-out/cancel move-out/cancel transfer, `EHouseAction` and error code.

Experiment targets: read-only house catalogue/ownership/coordinates/actions/errors. Do not initiate transfers/move-out for proof.

### Inspect player/object, Item Info and Outfit Memorial — STATIC_PRESENT

Observed:

- inspect-object data vector and inspection-list window type;
- inspect-player dialog request with creature ID;
- Item Info selection/tracking/black-whitelisting;
- Outfit Memorial data/dialog;
- `GameclientMessageInspectPlayer` and `LookAtCreature`.

Experiment targets: structured inspection fields, object/player identity, item metadata and whether look/inspect responses provide richer structured data than rendered text.

### Character information, outfit, blessings and premium panels — STATIC_PRESENT

`TCharacterInfoDialogController` exposes Character Info routes to XP boost, Blessings, Item Info, outfit, Skill Wheel and Weapon Proficiency. Blessing and premium/store-related controllers are present.

Use for read-only state/model discovery; no purchases.

### Character auction/trade, world transfer and main-character change UI — STATIC_PRESENT

Observed `TCharacterAuctionConfiguration`, `TCharacterTradeDialogController`, due-payment dialog, world-transfer controller and main-character-change controller.

These are low-priority account/economy surfaces. Read-only state discovery only unless separately authorized; never commit account transfers/trades/payments for proof.

### Calendar and News — STATIC_PRESENT

Observed Calendar open/dialog and News storage/button/dialog, including returner information changes.

Experiment targets: structured event/calendar/news data and whether this can feed world/event intelligence.

### Server/world modal and notification intelligence — STATIC_PRESENT

The presence of `TServerModalDialogProtocolMessageHandler`, disconnect reaction controller, death dialog, chat/system storage and the large unclassified inbound protocol remainder strongly supports a first-class incoming-event census.

Mandatory experiment: enumerate all 189 server->client generated message names and correlate each observable family to handlers/runtime state/UI. Preserve unknown families as `UnknownIncomingEvent`; do not discard them because they do not match known words.

### Context menus and generic UI semantics — STATIC_PRESENT

Observed `TContextMenuController`, dialog base close events, message dialogs, select-amount dialogs, sidebar panel/widget managers, mouse cursor/drag-and-drop controllers and generic QML list/proxy models.

Experiment targets: target->available semantic actions, active dialog/modal/window/tab/row, selected object/creature and generic confirmation states.

### Action bars, hotkeys and multi-action buttons — STATIC_PRESENT

Observed spell/object/text/passive-ability assignment, multi-action popup, object assignment with `TActionButtonID`, appearance instance ID and `EHotkeyUseObjectType`, plus inventory/object-info reactions.

Experiment targets: complete action-bar/hotkey configuration model, target/use mode, cooldown overlay and the generic semantic execution path behind an assigned action.

### Minimap, markers and coordinate transforms — STATIC_PRESENT

Observed `TMinimapController`, edit-minimap-marker dialog and QML world-map camera/viewport coordinate-transform helpers.

Experiment targets: minimap visible area, floor movement, marker model, world<->screen coordinate transforms, cache scope and whether these can support structural navigation without pixel automation.

### Network lanes, reconnect and performance state — STATIC_PRESENT

Observed:

- `TGameserverDualConnection::connectionsUsedChanged(EConnectionsUsed)`;
- packet sequence flow processor reacting to connection changes;
- `TFPSLatencyIndicatorController`.

Experiment targets: current connection lane(s), connection changes/recovery, latency value/source, FPS/frame timing when structurally exposed and their usefulness to agent health monitoring.

### Sound/event cues — STATIC_PRESENT

Observed `TGameSessionSoundProvider`, `TSoundStorage::soundsToPlayChanged` and ambience-object stream counts keyed by `TSoundEffectID` and world-map extent.

Low-priority experiment: determine whether structured sound events carry useful world cues not otherwise exposed. Sound must not become a substitute for stronger state/protocol evidence.

### Creature podium — STATIC_PRESENT

Generated configure/set-creature-podium messages and a configure dialog controller are present.

Low-priority read-only census of podium configuration and object/outfit identifiers.

### Offline training, vocation selection and tutorials — STATIC_PRESENT

Observed multi-offline-training dialog, vocation-selection dialog, tutorial hint/overlay/controller helpers. Treat as low-priority session/UI capability surfaces.

### White/blacklists and Exiva options — STATIC_PRESENT

Observed dedicated white/blacklist dialog and Exiva options entry point plus configuration-change signals.

Experiment targets: local configuration model and, where applicable, any server-derived identity/state. Avoid altering unrelated social filters unless reversible.

### Highscores, hirelings and other feature surfaces — STATIC_PRESENT

Observed Highscores dialog and Hireling configuration dialog among the action-regex inventory. These should be part of the creative/unfiltered census rather than presumed irrelevant.

### Sessiondump player — STATIC_PRESENT

`tibia::sessiondump::TSessiondumpPlayer::paused` exists in the exact binary. Treat this as a research lead only; do not make it a normal Agent Game API dependency without a clear safe product need and evidence.

## Mandatory exhaustive census follow-up

The next static-analysis pass must not use a feature-keyword filter as the completeness boundary. Produce and persist:

1. all 349 generated protocol message names, split 160 client->server / 189 server->client;
2. all recovered Tibia-owned QMeta classes and every method/property/signal with types where resolvable;
3. all protocol-queue methods, not only the 121 targeted state regex hits;
4. all game-action handlers and high-level controller action surfaces;
5. namespace clustering and automatic candidate classification;
6. an `UNCLASSIFIED` bucket that is reviewed manually rather than discarded.

For every newly discovered feature family, add a bounded experiment to `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md` or record why it is not useful/safe.

## Promotion priorities

### P0

- session/world-entered/disconnect/modal/death health;
- player HP/mana/position/state/skills;
- world/map/creatures;
- battle target/attack/follow/movement;
- inventory/containers/object metadata;
- chat/incoming world/server events;
- common inbound dispatcher and common outbound action path;
- player trade and party/share-exp static surfaces;
- stable bridge/restart rediscovery.

### P1

- NPC trade/conversation;
- analyzers and gain/waste telemetry;
- quick loot/managed containers;
- context menu/action bars/hotkeys;
- Bestiary/bonus effects/Bosstiary;
- network health/latency;
- UI semantic state.

### P2

- Skill Wheel/gems/presets;
- Forge;
- Imbuements;
- Weapon Proficiency;
- Prey/Taskboard/Bounty/Weekly/Soul Seals;
- Quest Log;
- Houses;
- Market read-only.

### P3 / read-only account-economy surfaces

- Store;
- Character Auction/Trade/World Transfer/Main Character Change;
- Daily Reward collection;
- other purchase/transfer/irreversible dialogs.

## Safety boundaries

- Static presence is not permission to invoke an action.
- Do not bypass anti-cheat/client checks.
- Do not purchase, transfer, forge, imbue, reroll, reset, move out, trade valuable items, spend Tibia Coins or materially spend character resources for proof.
- Do not disturb unrelated players for party/trade/chat experiments.
- Prefer read-only, preview, self/NPC or controlled reversible experiments.
- Preserve secret/account data outside repository/logs/artifacts.

## Current conclusion

**FACT:** the exact researched official Linux client contains far more semantically named state/action/UI surfaces than the initial core experiment list. The static inventories directly expose dedicated subsystems for player trade, NPC trade, party shared experience, Skill Wheel, Forge, monster bonus effects, Prey, Taskboard/weekly/Soul Seals, Market, Houses, Imbuements, Weapon Proficiency, Quick Loot, analyzers, Friends/VIP, Quest Log, Reward Wall, network connection state, sound events, server modal/death handling, action bars/hotkeys and semantic appearance metadata.

**UNKNOWN:** which of these remain identical in the current upstream client and which can be safely promoted to G1-G4 through the current stable bridge. Reverify the current binary SHA first.

## Next action

Resolve the current official Linux client version/SHA and structural `IN_GAME` session, then run an **unfiltered full protocol/QMeta census** and begin live P0 correlation from common inbound dispatch + player position/HP/mana/world/creatures, while independently mapping player-trade and party/share-experience message/action families.