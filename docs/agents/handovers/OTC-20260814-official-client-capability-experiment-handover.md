# Track A official-client capability experiment handover

```yaml
programme: OTCLIENT-TIBIA-RE
track: official-client-re
repository: blakinio/otclient
owner_request: persist all current capability-research state in Git
status: ACTIVE_DISCOVERY_PROGRAM
source_of_truth: live repository + retained GitHub Actions evidence
```

## Scope

This handover persists the material findings and decisions from the current owner conversation about extracting every useful semantic capability from the official native Linux Tibia client and adding it to the Track A experiment programme.

It does not itself promote static binary evidence into a live runtime capability. Static presence remains a lead until revalidated on the current exact client SHA with the evidence gates defined in `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md`.

## Exact researched binary evidence

Retained successful GitHub Actions evidence for the researched official Linux client identifies:

```text
client version: 15.32.df7b29
client SHA256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Generated protocol inventory run `31651220862`, job `94295767215` established:

```text
PROTOCOL_MESSAGE_TOTAL=349
CLIENT_TO_SERVER_MESSAGE_SYMBOLS=160
SERVER_TO_CLIENT_MESSAGE_SYMBOLS=189
PROTOCOL_CAPABILITY_MESSAGE_COUNT=98
REQUIRED_OUTBOUND_SYMBOLS_PRESENT=true
```

Therefore 251 generated protocol message names were not covered by the old feature regex and require an unfiltered census before the programme can claim broad protocol coverage.

High-level QMeta inventory run `31651684700`, job `94297172395` established:

```text
HIGHLEVEL_ACTION_METHOD_COUNT=612
```

Targeted state/read inventory run `31652393473`, job `94299386259` established 121 targeted state/read/update hits and included a static `sendShareExperience` lead.

## High-value static capability families already surfaced

The binary evidence already exposes named surfaces for the following families. These are `STATIC_PRESENT` leads until live correlation proves stronger gates.

### Core movement, combat and world interaction

- `GameclientMessageGoNorth`, `GoEast`, `GoSouth`, `GoWest` and diagonals;
- `GameclientMessageGoPath`;
- rotate north/east/south/west;
- `Stop`, `Cancel`;
- `Attack`, `Follow`;
- `UseObject`, `UseTwoObjects`, `UseOnCreature`;
- `MoveObject`;
- `BrowseField`;
- look/inspect player/creature/object paths;
- battle list target-selection and attack-first/next/previous surfaces.

### Map, creatures and player state

Server-side generated messages and runtime classes include:

- `GameserverMessageFullMap`;
- `FieldData`, `ChangeOnMap`, `CreateOnMap`, `DeleteOnMap`;
- `MoveCreature`;
- creature health/light/outfit/party/skull/speed/type/unpass/update/data;
- `TCreatureStorage` and creature update signals;
- player basic/current data, skills, state, inventory and vocation-specific data;
- world-entered/session lifecycle surfaces;
- minimap and Cyclopedia map controllers/storage;
- world-map camera and coordinate-transform QML types.

### Inventory, containers, depot, stash and Quick Loot

Static surfaces include:

- `TContainerProtocolMessageHandler`;
- close/up/next-page/previous-page/update container;
- object-info requests;
- container sort;
- move content to managed containers;
- `TContainerStorage`;
- `TInventoryContainer`;
- object-count and object-info storage;
- stash and depot-search open/close;
- `TManagedContainerStorage`;
- Quick Loot / obtain-container selection, clear and open operations;
- item blacklist/whitelist configuration.

### Item semantic metadata

`TAppearanceTypeHelperQmlService` exposes static methods equivalent to:

```text
appearance/type ID -> object name
appearance/type ID -> object description
object name -> appearance/type ID
```

This is a high-priority live experiment because it may allow semantic item recognition without OCR and without an external lookup table.

### Player-to-player trade

Static evidence includes:

- `TPlayerTradeProtocolMessageHandler`;
- open/close player trade widget;
- `TPlayerTradeController`;
- own-side and counter-offer look operations;
- `TPlayerTradeObject` item-change state.

Live work must remain non-destructive and avoid valuable items.

### NPC conversation and NPC trade

Static evidence includes:

- NPC talk partners and NPC chat/channel state;
- `TNPCTradeProtocolMessageHandler`;
- `TNPCTradeStorage`;
- player and trader inventory change signals;
- `TNPCTradeController`;
- switch buy/sell;
- select/look trader goods.

Read-only live correlation is the default. Any purchase/sale experiment requires a harmless, bounded and reversible test with proven ABI/cost semantics.

### Party and shared experience

Targeted inventory surfaced `sendShareExperience`. The experiment programme must separately identify:

- party membership/invite/join/leave state where exposed;
- leader/member identity and status;
- shared-experience enable/disable action family;
- server confirmation/rejection state;
- any party-hunt analyzer coupling.

### Chat, channels and social state

Static evidence includes:

- `GameclientMessageTalk`;
- get/open/join/leave/private channel;
- invite/exclude from channel;
- close NPC channel;
- incoming `GameserverMessageTalk`, channel event/channels/open/close/private;
- `TChatChannelStorage`, `TChatProtocolMessageHandler`, `TChatStorage`, `TTextStorage`;
- `TFriendsProtocolMessageHandler`;
- `TVipStorage` and VIP widget model.

The target is structured semantic chat/social state rather than OCR-derived text.

### Skill Wheel, gems and presets

Static evidence includes:

- `GameclientMessageRequestSkillWheel`;
- `GameclientMessageApplySkillWheel`;
- `GameserverMessageSkillWheel`;
- `TSkillWheelStorage`;
- Gem Atelier inventory state;
- Skill Wheel dialog/page/preset-management controllers;
- use-server-wheel-as-current and skill-removal surfaces.

### Forge

Static evidence includes:

- `TExaltationForgeFusionPageController`;
- `TExaltationForgeTransferPageController`;
- fusion/resource/source/target object selection;
- Exaltation Forge/result dialog controllers.

Read-only state discovery precedes any mutating forge operation.

### Monster Bonus Effects, Bestiary/Bosstiary and Prey

Static evidence includes:

- `GameclientMessageMonsterBonusEffectAction`;
- `GameserverMessageMonsterCyclopediaBonusEffects`;
- `TMonsterBonusEffectStorage`;
- unlock/clear/assign bonus-effect UI/controller paths;
- Bestiary/Bosstiary trackers and dialogs;
- creature tracker;
- Prey dialog/render controllers.

No point/currency spending is authorized merely for proof.

### Taskboard, Bounty, Weekly Tasks and Soul Seals

Static evidence includes:

- `TTaskboardProtocolMessageHandler`;
- taskboard dialog;
- Bounty and Weekly Task entry points from the kill tracker;
- `TWeeklyTasksController`;
- Soul Seals dialog and monster-race ID payload.

This family is now an explicit census/live-experiment target rather than an incidental UI feature.

### Houses

Static evidence includes:

- `THousesStorage`;
- house information, character houses and limits;
- house selection;
- layer bounds;
- house world-map/viewport integration;
- move-out/cancel-transfer controller paths;
- Cyclopedia house actions/results.

Read-only discovery must be separated from financially or ownership-sensitive house actions.

### Rewards, returner state, calendar and news

Static evidence includes:

- Reward Wall controller;
- resting-area bonuses;
- fixed/pick-items reward collection paths;
- returner reward state;
- Daily Reward item picking;
- calendar and news controllers/storage.

Collection/spending actions are not required for initial proof.

### Imbuements

Static evidence includes:

- `TImbuementDurationsStorage`;
- imbued-object changes;
- imbuing protocol handler/dialog.

The live experiment should prioritize item IDs, slots, duration/expiry and current imbuement metadata as read-only state.

### Weapon Proficiency

Static evidence includes:

- Weapon Proficiency dialog/controller;
- weapon selection;
- shape/reshape/options dialogs;
- inspect-object coupling;
- object proficiency XP update surface.

Any mutating reshaping is out of initial proof scope.

### Market and economy surfaces

Static evidence includes:

- `TMarketProtocolMessageHandler`;
- `TMarketStorage`;
- market item details;
- own offers/history;
- offer cancel UI path;
- Store, premium, transaction history and transfer-credit dialogs.

Initial work is read-only. No real purchase, TC transfer or valuable market mutation is required for proof.

### Quest Log and trackers

Static evidence includes:

- `TQuestLogController`;
- quest tracker widget;
- request-open quest log dialog.

The live experiment should determine whether quest IDs/progress are structurally represented and whether updates arrive as dedicated protocol/state mutations or formatted text.

### Analytics/analyzers

`TSidebarWidgetsManager` names the following analyzer widget families:

```text
Loot Analyzer
Waste Analyzer
Impact Analyzer
Damage Input Analyzer
Hunting Session Analyzer
Progress Analyzer
Analytics Selector
Party Hunt Analyzer
```

Additionally `TGainWasteStorage` exposes looted/wasted items and metrics. The programme must test whether client-normalized XP/damage/loot/waste/supply/party-hunt values can be read directly rather than reconstructed from OCR or chat text.

### Server modal, death and disconnect intelligence

Static evidence includes:

- `TServerModalDialogProtocolMessageHandler` with structured `TServerModalDialogData`;
- `TGameSessionDisconnectReactionController`;
- game-session disconnect/modal reactions;
- death handling with `EDeathType` and `TFairFightFactor`;
- client-check close paths;
- world/session connection state.

This is a priority for autonomous agent resilience: detect warning/disconnect/death/session-loss state structurally and checkpoint/recover rather than relying on screenshots.

### Network, latency and connection state

Static evidence includes:

- `TGameserverDualConnection`;
- connection-used change signals;
- packet sequence flow processor;
- `TFPSLatencyIndicatorController`.

Live tests should determine whether latency, connection path, reconnect and sequence state are structurally readable.

### Sound events

Static evidence includes:

- `TGameSessionSoundProvider`;
- `TSoundStorage`;
- object ambience stream-count events;
- sound effect identifiers.

Sound may provide an additional structured event channel for world/UI correlation and should be inventoried, but must not substitute for stronger protocol/runtime evidence.

### Action bars, hotkeys and semantic UI

Static evidence includes:

- action bar controller;
- assign spell/object/text/passive ability actions;
- multi-action popup;
- object assignment with semantic IDs/types;
- hotkey use-object type;
- inventory and cooldown coupling;
- general dialog/window/sidebar/controller state.

The long-term goal is semantic invocation and state inspection without pixel-coordinate clicking.

## Mandatory extension experiments

The current programme explicitly requires extension experiments `E51-E75` in `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md`.

Highest-priority sequence:

1. `E51` unfiltered full census of all 349 generated message types;
2. `E52` unfiltered QMeta census, removing the earlier feature-name bias;
3. recover current live runner/login ownership and verify exact current official-client SHA;
4. structurally prove `IN_GAME` before capability tests;
5. map common inbound dispatch and outbound action dispatch;
6. correlate player position, HP/mana, world map/tiles and CreatureStorage;
7. independently map player trade and party/shared-experience families;
8. exercise the remaining E53-E75 capability families with read-only or reversible differential controls;
9. classify every still-unexplained message/class instead of dropping unknowns.

## Evidence policy

Use the programme gates:

```text
G0 STRUCTURAL OBSERVATION
G1 PASSIVE CORRELATION
G2 REVERSIBLE ACTION PROOF
G3 BOUNDED MUTATING ACTION PROOF
G4 STABLE BRIDGE/API
```

Do not promote:

```text
STATIC_PRESENT -> PROVEN LIVE API
QMeta method name -> safe callable ABI
protobuf type name -> decoded semantic fields
UI reaction -> server-authoritative confirmation
```

without the required differential/runtime controls.

All current-address and exact-layout findings are version-fenced. After restart/relogin or client update reacquire PID, PIE base, runtime objects and semantic resolvers.

## Safety and authorization boundaries

- official native Linux Tibia client Track A only;
- no Windows/Wine/Proton/mobile/browser evidence as authority;
- no attacks on server infrastructure or security-control bypass;
- never print/persist account secrets;
- do not use valuable inventory, market, store, forge, charm, wheel, reward or house mutations merely for proof;
- prefer passive/read-only experiments, then harmless reversible actions;
- do not message random players or interfere with other players;
- no OCR except login/bootstrap or visual cross-check when structural evidence is unavailable;
- do not consume owner Codex/API/token credentials unless separately and explicitly authorized.

## Durable files for this work

The current branch/PR carries the following durable research state:

```text
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
docs/agents/tasks/active/OTC-20260814-official-client-capability-experiment-sweep.md
docs/agents/handovers/OTC-20260814-official-client-capability-experiment-handover.md
```

## Current PR state at handover creation

```text
PR: #293
title: docs(tibia-re): add official-client capability experiment sweep
branch: docs/OTC-20260814-official-client-capability-experiment-sweep
base: main
previous verified head before this handover commit: edd592b7d187d8b3d6ba7173366a004de5651065
```

The previous PR snapshot showed 4 changed files, 1817 additions, 0 deletions, and CI run `31780682389` queued on that previous exact head. This handover commit changes the exact head, so CI must be rechecked on the new head before any green/exact-head closeout claim.

## Exact next action

```text
Refresh PR #293 exact head and exact-head CI after this handover commit. Keep the PR/task open until required documentation validation/CI is green and programme lifecycle rules permit terminal closeout. For runtime continuation, a fresh Track A worker must then resolve live runner/login ownership, current client SHA, structural IN_GAME and execute E51/E52 before relying on the old filtered inventories.
```
