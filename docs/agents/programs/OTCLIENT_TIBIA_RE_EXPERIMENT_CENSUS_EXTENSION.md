# OTCLIENT-TIBIA-RE evidence-derived experiment extension

```yaml
programme: OTCLIENT-TIBIA-RE
track: official-client-re
subject: official native Linux Tibia client only
extends: docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
evidence_census: docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
mandatory: true
```

## Contract

This file is a mandatory additive extension of `OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md`. It is derived from exact-binary QMeta, generated-message, state/update and action-signature inventories rather than from a remembered Tibia feature list.

A future Track A worker executing the sweep must include every group below unless it has already been promoted into the base sweep. Static presence establishes a research target, not live capability success. Current-version SHA and structural `IN_GAME` must still be revalidated before live promotion.

## E51 — exhaustive protocol census

Enumerate and persist **all** generated protocol message symbols without a feature keyword filter.

Known exact-binary inventory boundary:

```text
349 total
160 client -> server
189 server -> client
98 selected by the historical capability regex
251 not classified by that regex
```

For every message record:

- exact generated type name;
- direction;
- namespace/family;
- serializer/deserializer if resolvable;
- handler/caller if resolvable;
- fields/types where resolvable;
- first live observation experiment;
- semantic classification or `UNCLASSIFIED`;
- current-client SHA.

Never discard an unknown message because its name lacks an expected feature keyword.

## E52 — exhaustive QMeta/controller/storage census

Enumerate all Tibia-owned QMeta classes and their methods/signals/properties rather than only regex matches. Cluster by namespace and dependency/call relationships.

Persist an `UNCLASSIFIED` bucket and manually inspect it for feature families missed by the original sweep.

Also enumerate the full protocol-message queue rather than only the 121 targeted state/read/update matches.

## E53 — party and shared-experience system

The exact researched binary contains the outbound QMeta surface `sendShareExperience` and inbound `GameserverMessageCreatureParty`.

Perform an unfiltered census for:

- Party;
- Invite;
- Join;
- Leave;
- Pass/Leadership;
- Shared Experience;
- member/shield state;
- party channel;
- party hunt analyzer;
- invite/accept/reject/cancel state.

Live experiments must use self-controlled/safe participants only and must not disturb unrelated players.

Target normalized state/actions such as:

```text
PartyState
PartyMember
PartyInvite
party.invite(...)
party.accept(...)
party.reject(...)
party.leave()
party.pass_leadership(...)
party.set_shared_experience(...)
```

Do not expose an action as supported until its actual live ABI and server-confirmed result are proven.

## E54 — player-to-player trade

The exact binary contains:

- `TPlayerTradeProtocolMessageHandler`;
- `TPlayerTradeObject`;
- `TPlayerTradeController`;
- player-trade widget open/close requests;
- own-side and counter-offer look operations.

Discover:

- trade request and partner identity;
- offered item model on both sides;
- item add/remove/change lifecycle;
- look-own/look-counteroffer;
- accept/reject/cancel;
- partner acceptance state if exposed;
- completion/cancellation/failure reason;
- inbound/outbound generated messages;
- common context-menu path to initiate trade.

Use only harmless controlled items/participants. Never risk valuable items for proof.

## E55 — server modal, death, disconnect and imminent-session-loss intelligence

Exact-binary surfaces include:

- `TServerModalDialogProtocolMessageHandler::openModalDialog(TServerModalDialogData)`;
- `TGameSessionDisconnectReactionController`;
- death dialog data including `EDeathType` and `TFairFightFactor`;
- logout confirmation;
- client close/session-close signals;
- two-factor/confirmation-code controllers.

Map:

- modal IDs/options/buttons/text/structured fields;
- disconnect reason and recovery path;
- kicked/session-invalid/reconnect state;
- death type and fair-fight factor;
- imminent logout/restart/save warnings where related inbound messages exist;
- safe agent checkpoint/recovery trigger.

Anti-cheat/client-check related symbols may be observed only as passive safety state. Never disable or bypass checks.

## E56 — semantic item/object metadata service

The exact binary exposes `TAppearanceTypeHelperQmlService` methods equivalent to:

```text
appearance ID -> name
appearance ID -> description
name -> appearance ID
```

Correlate these helpers with:

- `TObjectAppearanceInstanceInfoStorage`;
- object-count storage;
- Item Info;
- inspect-object data;
- market/loot/item tracking models;
- item tier/classification/charges/subtype;
- weapon proficiency XP when available.

This is high priority because it may convert raw appearance IDs into semantic objects without OCR or external lookup tables.

## E57 — full analyzer telemetry

The exact client names these sidebar analyzers:

- Loot Analyzer;
- Waste Analyzer;
- Impact Analyzer;
- Damage Input Analyzer;
- Hunting Session Analyzer;
- Progress Analyzer;
- Analytics Selector;
- Party Hunt Analyzer.

Together with `TGainWasteStorage` and item tracking, determine for every analyzer:

- underlying storage/controller;
- source events;
- locally derived vs server-authoritative fields;
- XP, damage, healing, loot, waste, supplies, time and party metrics;
- reset/session boundaries;
- normalized values useful to an agent.

Prefer reading the model directly instead of reconstructing analyzer values from rendered text.

## E58 — Taskboard, Bounty Tasks, Weekly Tasks and Soul Seals

Exact-binary evidence includes Taskboard controllers/protocol handler, Bounty/Weekly entry points, Soul Seals dialog with monster-race IDs and Weekly Tasks controller.

Map:

- task IDs/types/categories;
- monster/race IDs;
- progress/requirements;
- delivery items;
- rewards/costs;
- slot/unlock state;
- Soul Seal state;
- request/response/action messages;
- cache lifetime.

Purchase/reward-spend paths are read-only unless separately authorized.

## E59 — Monster Bonus Effects

Treat this as a dedicated system, not a generic Bestiary footnote.

Exact-binary surfaces expose:

- storage changes;
- remaining assignable effects;
- selected effect;
- unlock;
- clear;
- assign effect to monster;
- generated `MonsterBonusEffectAction`.

Map IDs, costs, assignment state, prerequisites, server responses and relation to monster race IDs. Do not spend/reset resources merely for proof.

## E60 — Weapon Proficiency

Exact-binary controllers expose weapon selection, inspect-object integration, proficiency XP change and shape/reshape/options dialogs.

Map:

- weapon/object IDs;
- current proficiency XP/progress;
- levels/stages/shapes/options;
- bonuses/effects if structurally represented;
- preview vs committed state;
- server requests/responses;
- relationship to Character Info/Inspect Item.

Do not perform irreversible reshape/commit operations for proof.

## E61 — Houses and Cyclopedia house actions

Exact-binary surfaces expose house storage, current/static house data, action results, house IDs, house actions/error codes, map viewport, select/center/make-visible and move-out/transfer-related UI.

Map read-only:

- house ID/name/location/world-map coordinate;
- ownership/character houses;
- limits/status;
- current/static data split;
- action availability and error codes;
- map/viewport integration.

Never initiate move-out or transfer merely for proof.

## E62 — Reward Wall, Daily Reward, returner state, Calendar and News

Map:

- reward streak/current reward;
- fixed-item/pick-item model;
- claimability;
- resting-area bonuses;
- returner information/state;
- calendar event model;
- news entries and updates;
- server vs local/static authority;
- notification/event-bus integration.

Do not consume strategically important rewards for proof.

## E63 — network connection lanes, reconnect, latency and FPS

Exact-binary surfaces include `TGameserverDualConnection`, connection-used changes, packet-sequence flow processing and an FPS/latency indicator controller.

Discover structurally:

- current game-server connection lane(s);
- lane change/failover events;
- socket/session association;
- latency/ping value and source;
- FPS/frame timing if exposed;
- reconnect progression;
- whether these can drive AgentHealth/ConnectionState events.

## E64 — sound/event cue stream

Exact-binary session sound and sound storage expose `soundsToPlayChanged`; ambience-object state carries `TSoundEffectID` and a world-map extent value.

Determine whether sound events expose semantic world information not otherwise available, including position/range/actor where present. Keep this low priority and never use sound as stronger proof than protocol/runtime state.

## E65 — action bars, hotkeys, passive abilities and multi-actions

Expand the base action-bar experiment with exact-binary surfaces for:

- spell assignment;
- object assignment;
- text action assignment;
- passive ability assignment;
- multi-action popup/buttons;
- `TActionButtonID`;
- appearance-instance ID;
- hotkey object-use mode;
- inventory/object-info updates.

Find the generic semantic execution path behind each configured action and separate local configuration from server-bound action invocation.

## E66 — quick-loot/obtain containers and item filters

Expand Quick Loot to include exact client models for:

- loot container by object category;
- obtain container by object category;
- select/clear/open;
- use-main-backpack-as-fallback;
- managed containers;
- item blacklist/whitelist;
- depot/stash integration.

Map state transitions without destructive loot/container changes.

## E67 — Friends, VIP, Social, white/blacklist and Exiva options

Perform a complete census across Friends protocol, account search, Social dialog, VIP storage/widget/edit UI, white/blacklist and Exiva options.

Map read-only identity/status/group/description/notification fields before any mutation. Do not contact or modify unrelated players for proof.

## E68 — Inspect Player/Object, Item Info and Outfit Memorial

Map structured inspection data end to end:

```text
request
-> generated message
-> server response
-> TInspectObjectData model
-> Item/Player dialog
```

Include creature ID, appearance/object IDs, equipment/item data, Item Info tracking/filters, Outfit Memorial data and any richer fields that exist before UI text formatting.

## E69 — character/account/economy UI census, read-only

Static surfaces include Character Auction configuration, Character Trade, due-payment dialog, world transfer, main-character change, Store purchase/transactions and premium-related dialogs.

Census their models/messages only to understand the client architecture. These remain P3/read-only and must not trigger purchases, transfers, account trade or payment actions without separate explicit authorization.

## E70 — Minimap markers and world-map coordinate transforms

Expand map/minimap experiments with:

- minimap visible-area model;
- floor up/down;
- marker edit/storage;
- world-map camera and viewport;
- world/subfield coordinate <-> stretched pixel transforms;
- Cyclopedia map selected item/creature;
- relation to cached map and authoritative player coordinates.

Goal: structural navigation geometry without screen-coordinate automation.

## E71 — Boosted Creature, Boss difficulty, Bosstiary and trackers

Map boosted-creature state changes, Boss Tracker/Bosstiary actions and boss-difficulty dialog data as distinct structured systems. Correlate race/boss IDs, progress/state and server messages without resource-spending actions.

## E72 — Imbuement tracker/durations

Prioritize direct reading of `TImbuementDurationsStorage` and tracker state:

- imbued object identity;
- slot/effect/tier;
- duration/remaining time;
- expiration event;
- relation to inventory/equipment;
- Imbuing dialog preview/request messages.

No resource consumption for proof.

## E73 — Skill Wheel gems and presets

Extend Wheel experiments to include exact-binary gem inventory, Gem Atelier, preset-management controller, `useServerSkillWheelAsCurrent`, request/apply messages and client-preview vs server configuration.

## E74 — generic UI window/sidebar/modal state

Use exact common controller surfaces to determine whether a normalized semantic UI state can expose:

- dialog opened/closed;
- sidebar/widget type and open state;
- active modal;
- selected row/item/creature;
- confirmation buttons/options;
- current channel/tab;
- player-trade/depot-search window state;
- current context menu target/actions.

Do not reproduce the GUI tree when a smaller semantic model suffices.

## E75 — creative unclassified feature recovery

After the exhaustive unfiltered inventories, inspect all remaining unclassified namespaces/classes/messages. Known examples already surfaced include Highscores, Hirelings, offline training, vocation selection, Creature Podium, tutorials and sessiondump-related code.

For each candidate classify:

```text
USEFUL_AGENT_CAPABILITY
RESEARCH_ONLY
LOCAL_UI_ONLY
ACCOUNT_ECONOMY_READ_ONLY
UNSAFE_OR_IRRELEVANT
UNKNOWN
```

Every `USEFUL_AGENT_CAPABILITY` receives a bounded experiment. Preserve the others with rationale so future agents do not repeatedly rediscover them.

## Completion condition for the census extension

This extension is not complete when all names have merely been listed. Completion requires:

1. current official Linux client SHA/version reverified;
2. full 349-message equivalent census rerun on the current binary;
3. unfiltered QMeta/controller/storage census on the current binary;
4. every material subsystem classified;
5. P0/P1 systems correlated live where safely possible;
6. unsupported/unavailable/unsafe systems explicitly classified rather than omitted;
7. capability matrix and experiment evidence updated in Git;
8. exactly one executable `next_action` remains while the programme is incomplete.
