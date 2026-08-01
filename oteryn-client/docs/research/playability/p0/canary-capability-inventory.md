# P0 Canary Current Capability Inventory

Status cut: client repository `main@9c03a448457b1715818e094fdfdeade4a1450434`  
Producer cut inspected: `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`  
Producer release constants: Canary `3.6.1`, client version `1525`  
Profile: `ProtocolProfileId::Current` on the configured modern game port  
Lane: `OTC2-20260801-playability-p0-canary` / PR #140  
Implementation authorized: **false**

## 1. Purpose

Inventory the source-backed post-admission gameplay capability surface of the exact inspected Canary cut and group it into bounded future client packages without inventing wire constants, copying server implementation structure into the client domain, or claiming that the inspected repository cut is the deployed production cut.

The exact deployed environment must still pin the same repository revision, configuration, build and profile before a real compatibility claim.

## 2. Authoritative source map

Primary producer sources:

- `src/core.hpp` — `SERVER_RELEASE_VERSION = "3.6.1"`, `CLIENT_VERSION = 1525`;
- `src/server/network/protocol/protocol_profile.hpp` — profile IDs, transport/handshake layouts, support state, item mapper policy and feature flags;
- `src/server/network/protocol/protocol_profile.cpp` — exact `Current` profile, transport and enabled feature mask;
- `src/server/network/protocol/protocol_port_utils.hpp` — modern versus legacy profile/port routing;
- `src/server/network/protocol/protocol_session_hint.hpp` — bounded account-session/character/profile hint lease and consume behavior;
- `src/server/network/protocol/protocolgame.hpp` — complete declared Current/legacy game protocol parse/send surface;
- `src/server/network/protocol/protocolgame.cpp` — packet dispatch, exact wire layouts and build/profile gates;
- exact item, creature, player, market, prey, bestiary, forge, imbuement, party, guild, chat and other subsystem sources referenced by `protocolgame.cpp`.

For every future protocol package, `protocolgame.cpp` at the accepted cut remains the authoritative numeric opcode/layout source. This inventory deliberately does not hand-copy a numeric opcode table because stale or profile-mixed constants would be more dangerous than an explicit generated index.

## 3. Profile and transport facts

### Current profile

The exact inspected `currentProfile` is:

- ID: `ProtocolProfileId::Current`;
- client version: `1525`;
- wire family: `CipsoftVanilla`;
- RSA key family: `OpenTibia`;
- support state: `Enabled`;
- item mapper policy: `NotRequired`;
- handshake: server challenge before login;
- expected profile: `Current`;
- game transport: `CurrentGameSequence`;
- outer length: modern block count;
- encrypted payload: modern padding byte;
- inbound/outbound checksum: sequence;
- compression: official;
- sequence high bit signals compression.

The configured modern game port selects `Current`; legacy 11.00 and 8.60 ports select their respective profiles. Client code must not infer the profile only from a hostname or assume legacy wire layouts are interchangeable.

### Explicit Current feature flags

The inspected Current profile enables:

- `CurrentPayload`;
- `LoginSpeedFormula`;
- `ModernLoginSideSystems`;
- `ResourceBalancePackets`;
- `CustomMonkPackets`;
- `MarketPackets`;
- `ImbuementWindow`;
- `MemorialPackets`;
- `PlayerDataLevelPercentU16`;
- `GameEventPayload`;
- `OfficialTaskboardPackets`;
- `OfficialVocationSpecificPlayerData`;
- `OfficialWeaponProficiencyPayload`;
- `GraphicalEffectSourceByte`;
- `OfficialSoulSealsPackets`;
- `OfficialSkillWheelPayload`.

A declared method in `ProtocolGame` is evidence that the server implements a capability family, but a feature is release-required only after the aggregation barrier classifies it and a controlled environment proves its exact configuration/path.

### Session/profile binding

`ProtocolSessionHintStore` binds remote IP, profile, account-session hash, allowed character names, expiry and connection behavior through a claim/consume lease. The client should treat profile/session/character relationship as authoritative and one-session scoped. It must not reuse a consumed or stale session hint/credential.

## 4. Capability classification

- **Bootstrap mandatory** — required to reach a coherent Current game session and first world state.
- **Common gameplay** — ordinary movement, interaction, combat, items, chat and player state expected for M2/M3 when enabled.
- **Product/common optional** — daily-product or social/economy capabilities that may be enabled/configured.
- **Exact-profile optional** — modern/version-specific families that require explicit capability/product selection.
- **Operational/admin** — diagnostics, reports or staff features not automatically required for player parity.

## 5. Admission and world bootstrap

### Producer responsibilities

- login challenge and Current transport negotiation;
- game login/session authentication;
- exact profile/build checks;
- account/session hint consumption;
- initial player/session setup;
- world/map description and side-system bootstrap;
- initial player data, inventory, containers, channels, VIP/social and modern side systems as configured;
- terminal session/end information.

### State/order dependencies

```text
server challenge
-> client game-login payload
-> profile/session/character resolution
-> encryption/sequence transport active
-> player attach/login
-> initial map/world bootstrap
-> player/entity/item/UI side systems
-> ordinary packet dispatch
```

The Current Rust adapter presently stops at ordered enter-world admission and does not implement the producer’s map/bootstrap sequence. A future bootstrap package must record the exact ordered message family sequence from `protocolgame.cpp` and controlled fixtures rather than treating one marker as a complete world entry.

Classification: bootstrap mandatory / M1→M2.

Recommended bounded package: `protocol-canary-bootstrap` after shared domain IDs/events exist.

## 6. Map, floors and tile state

Source-backed family:

- initial map description;
- floor descriptions and tile serialization;
- viewport movement edges/rows/columns;
- tile add/update/remove/transform;
- teleport/position changes;
- browse-field/container projection where applicable;
- ambient/world-time or environmental state tied to map presentation.

Required client separation:

- wire parser emits bounded map/tile domain events;
- domain owns authoritative floor/tile/chunk state;
- renderer consumes immutable snapshots;
- minimap is a separate consumer and does not become authoritative world state.

State dependencies:

- accepted map dimensions/floor range/view geometry;
- known/unknown creature cache state;
- item/appearance mapping for every serialized stack entry;
- ordered application relative to creature movement, teleport and tile updates;
- full snapshot/recovery contract after missed or incompatible state.

Negative evidence required:

- truncated tile/floor streams;
- excessive counts/stack depth;
- invalid positions/floors;
- unknown item/appearance IDs;
- inconsistent known-creature references;
- trailing/unsupported payloads.

Classification: bootstrap mandatory and common gameplay / M2.

Recommended package: `protocol-canary-map` split from entity/visual parsing if the generated source index proves independently testable boundaries.

## 7. Creatures, appearances and world visuals

Source-backed family:

- known/unknown creature serialization and removed-known replacement;
- creature add/remove/move/teleport;
- name, health, direction, outfit/appearance, light, speed, skull/shield/emblem/type/icon/helper information where supported;
- local/other player, monster, NPC and summon/familiar distinctions;
- outfit/mount and attached/graphical effects;
- magic effects, distance projectiles and animated text;
- item/appearance serialization through `AddItem` and related visual metadata;
- Current graphical-effect source byte feature.

State dependencies:

- session-scoped creature/entity handles;
- known-creature cache and replacement semantics;
- exact appearance/item metadata from approved asset producer;
- feature/build gates;
- domain lifecycle before renderer resource realization;
- stale generation rejection on session/map replacement.

Classification: bootstrap/common gameplay / M2-M3.

Recommended packages:

- `protocol-canary-entity` — identity/lifecycle/movement/state;
- `protocol-canary-world-visual` — item/appearance/effect/projectile mappings after asset contracts merge.

## 8. Movement and navigation commands

Client→server declarations/source evidence include:

- auto-walk;
- directional movement/turn dispatch in the packet switch;
- teleport/admin-capability parse path where authorized;
- movement-related item throw/move interactions;
- follow mode and movement relationship;
- client fight modes and chase posture;
- mount toggle and related movement presentation where enabled.

Server→client dependencies include:

- authoritative creature/local-player movement;
- speed changes and Current login speed formula;
- teleport/reposition;
- map edge updates/reconciliation;
- floor transitions.

Required client behavior:

- semantic movement commands only;
- one simulation owner;
- no client authority over final position;
- bounded optional prediction/reconciliation only after protocol evidence;
- focus/disconnect/session replacement clears held movement;
- command/action generation correlated to current session.

Classification: common gameplay / M2-M3.

Recommended package: `protocol-canary-movement` consuming merged `GameCommand`/`GameEvent`/position contracts.

## 9. Player state, stats, skills, conditions and death

Source-backed family includes:

- player data and Current `PlayerDataLevelPercentU16` layout;
- health/mana and resource balances;
- skills and skill updates;
- conditions/icons, including Current icon/modern payload differences;
- speed, capacity, experience and progression values;
- cooldown/spell group behavior where emitted;
- vocation-specific player data;
- weapon proficiency detail payload with build-specific 15.25 gating;
- custom Monk data;
- soul seals;
- official skill wheel/gem payload;
- session-end/death/logout information;
- recent death/PvP/memorial-related data where enabled.

The producer source comments explicitly state that 15.25 builds are not byte-identical for weapon proficiency detail lists. Unknown builds keep a shorter shape. This proves that client build string and exact layout fixtures are mandatory compatibility inputs.

Required client separation:

- protocol fields map to stable domain state/events;
- UI consumes bounded view models;
- unavailable/unsupported differs from zero;
- timers use monotonic/server-derived accepted state;
- death/session end invalidates gameplay actions and stale state.

Classification:

- base health/mana/stats/skills/conditions/death: common gameplay M2-M3;
- vocation/weapon proficiency/soul seals/wheel/gems/memorial: exact-profile optional M5 unless selected earlier.

Recommended packages:

- `protocol-canary-player` for base player state;
- bounded feature packages for each exact-profile modern family after product selection.

## 10. Items, inventory, equipment and containers

Client→server declarations include:

- look at/world/battle-list/inspection;
- use item, use item with target, use with creature;
- throw/move item;
- close/up-arrow/update/seek container;
- browse field;
- open parent container;
- rotate/wrap/configure show-off item;
- quick loot, loot container and white/black list actions;
- depot search/open/close/detail/retrieve;
- reward chest collection;
- container action and character trade configuration actions.

Server→client family includes:

- item serialization through `AddItem`;
- inventory/equipment updates;
- open/update/close container;
- item inspection and object information;
- prices/resource balances;
- depot/inbox/stash counts/details;
- quick-loot and container metadata;
- item tier/classification/imbuement/forge data where supported.

State dependencies:

- exact item/appearance schema and profile mapping;
- stable session-scoped item/container/slot identifiers;
- stack/count/tier/attributes bounds;
- authoritative server result and stale-source/target rejection;
- one-shot semantic action/reconciliation contract.

Classification:

- look/use/move/inventory/equipment/container: common gameplay M3;
- depot/stash/quick loot/reward chest/advanced item systems: product/exact-profile M4-M5.

Recommended packages:

- `protocol-canary-items`;
- `protocol-canary-containers`;
- later `protocol-canary-depot-loot` if selected.

## 11. Chat, channels, NPC and text interactions

Source-backed declarations include:

- `parseSay`;
- open/close channel;
- channel invite/exclude;
- open private channel;
- server channel/private/NPC message sends;
- channel dialog/list/events/user membership;
- text window and house window interactions;
- greet and NPC interaction paths;
- modal-window answers;
- FYI/status/text messages;
- report/bug/rule-violation text paths.

Required client separation:

- exact wire text/message class becomes validated domain communication event;
- channel identity/membership/state is authoritative;
- text input is separate from gameplay key actions;
- raw markup/URLs/backend strings are not trusted UI content;
- bounded history and privacy-aware diagnostics;
- NPC/private/channel semantics remain distinct.

Classification:

- local/channel/private/NPC communication: common gameplay M3;
- management/report/admin channels: product/operational optional;
- house/text/modal windows: capability-dependent product/feature UI.

Recommended package: `protocol-canary-chat` with a separate safe text/modal representation if the shared UI contract requires it.

## 12. Combat, targeting and fight modes

Client→server declarations/source evidence:

- fight/chase modes;
- attack;
- follow;
- look in battle list;
- use-with-creature;
- party analyzer actions;
- join aggression and other exact modern combat-related actions;
- boss difficulty/selection and related feature paths.

Server→client family includes:

- creature health/state/effects;
- target/follow acknowledgements/state changes through ordinary game state;
- combat text/effects/projectiles;
- cooldowns/conditions/icons;
- party analyzer and boss-system data where configured.

Required client behavior:

- semantic target/attack/follow/stop commands;
- server-authoritative target and result;
- stale creature handles rejected;
- viewport, battle list, HUD and cooldown views correlate to one domain state;
- capability-gated commands unavailable with reason.

Classification: base combat common gameplay M3; boss/analyzer/special systems exact-profile M4-M5.

Recommended package: `protocol-canary-combat`, with modern boss/analyzer packages only after classification.

## 13. Party, VIP, guild and social

Source-backed declarations include:

- party invite/join/revoke/leadership/shared experience;
- party analyzer;
- VIP add/remove/edit/group actions;
- channel membership/invite/exclude;
- guild message editing and related social producer paths;
- friend-system action;
- team finder list/leader/member flows;
- familiars/summons and social grouping dependencies.

Required client domain/UI separation:

- authoritative membership/status/groups;
- semantic actions and stable rejection states;
- no UI-local authoritative membership;
- privacy and accessibility for presence/notifications;
- unsupported server feature hidden/disabled explicitly.

Classification: daily-product or exact-profile M4-M5 depending selected server profile/configuration.

Recommended packages: bounded `protocol-canary-party`, `protocol-canary-vip-social`, and `protocol-canary-team-finder` only if release-required.

## 14. NPC shop, player trade, depot and market

Client→server declarations include:

- shop look/buy/sell;
- request/look trade;
- market browse/create/cancel/accept;
- depot search/retrieve;
- offer description and object/price/resource queries.

Server→client family includes:

- shop lists/prices/transaction result;
- trade offers/state/result;
- depot/inbox/stash data;
- market browse/history/offer state;
- resource/currency balances;
- item inspection/prices.

Current profile explicitly enables `MarketPackets`.

Required client behavior:

- all economy values/state remain server-authoritative;
- bounded counts/prices/history/text;
- stale offer/session rejection;
- explicit confirmation/cancel/error states;
- privacy and no duplicate command after uncertainty.

Classification:

- NPC shop/trade may be core/daily based on product classification;
- depot/market/economy systems generally M4-M5 exact-profile.

Recommended bounded packages: `protocol-canary-shop-trade`, `protocol-canary-depot`, `protocol-canary-market`.

## 15. Quests, prey/tasks and progression systems

Source-backed declarations include:

- quest line;
- prey actions;
- task hunting actions;
- official taskboard packets;
- bestiary races/creatures/charms/entries/monster tracker;
- bosstiary data/slots/cooldowns/entry changes;
- cyclopedia character/map/monster and inspection paths;
- highscores;
- achievements/recent deaths/PvP or related progression records;
- team finder and feature-specific progression views.

Current profile explicitly enables `OfficialTaskboardPackets` and several modern payloads.

Classification: exact-profile optional M5 unless product owner selects an earlier daily-play requirement.

Recommended: one bounded package per accepted family; never a single “modern features” parser.

## 16. Imbuement, forge, wheel/gem and vocation-specific systems

Source-backed declarations include:

- open/apply/clear/close imbuement and results;
- forge open/data/error/result/history/skill stats;
- weapon proficiency;
- vocation-specific data/set vocation;
- custom Monk data;
- soul seals;
- skill wheel/gem payload;
- boss difficulty and modern feature presentation.

Current profile explicitly enables:

- `ImbuementWindow`;
- `OfficialVocationSpecificPlayerData`;
- `OfficialWeaponProficiencyPayload`;
- `OfficialSoulSealsPackets`;
- `OfficialSkillWheelPayload`;
- `CustomMonkPackets`.

These layouts are high-risk for build/profile drift and must consume exact generated layouts/fixtures. They are not prerequisites for M2/M3 unless the product scope explicitly says so.

Classification: exact-profile M5 by default.

Recommended: separate feature packages and scenario sets per family.

## 17. Audio, time, effects and presentation-support packets

The protocol source references:

- sound music/ambient/effect enumerations;
- source effect type;
- world/Tibia time;
- graphical effects and source byte;
- icons/conditions;
- FYI/modal/text windows;
- resource balances and presentation-support data.

PR #143 owns audio/UI contract requirements and PR #142 owns approved resource rights/runtime. The protocol adapter should emit typed audio/presentation intents/events, not open devices, load assets or create widgets.

Classification: core/daily/exact-profile according to selected scenarios and server feature support.

## 18. Operational/admin/report paths

The protocol declares bug reports, rule violation reports, client checks/details, transaction/object inspection, livestream/team/admin and other operational paths.

These are not automatically player release requirements. The aggregation barrier must classify them separately, with security/privacy review. Staff/admin capability must not be exposed merely because the server class declares a parser.

## 19. Recommended client package graph

Subject to shared P1 game contracts:

```text
protocol-canary-bootstrap
  -> protocol-canary-map
  -> protocol-canary-entity
  -> protocol-canary-world-visual
  -> protocol-canary-movement
  -> protocol-canary-player
  -> protocol-canary-items
  -> protocol-canary-containers
  -> protocol-canary-chat
  -> protocol-canary-combat
  -> selected social/economy/progression/modern feature packages
```

Dependencies:

- map/entity/movement consume canonical domain IDs, events and commands;
- world-visual consumes approved appearance/resource contracts from asset work;
- all feature packages consume shared bounded reader/writer primitives and exact profile/build metadata;
- no package mutates game state or UI directly;
- app composition occurs only after producer contracts merge.

## 20. Required generated source index before implementation

A focused producer-index task should mechanically extract at the accepted Canary cut:

- client→server dispatch opcode, handler and profile/build gate;
- server→client send method, opcode/layout and profile/build gate;
- state/order prerequisite;
- subsystem source dependencies;
- test/fixture references;
- capability classification and future package owner.

The generated index is evidence/artifact, not a hand-maintained public Rust API. Any discrepancy between this prose and exact source dispatch is resolved in favor of the accepted producer source and recorded as a conflict.

## 21. Current blockers and unknowns

- The inspected source cut is exact, but the deployed staging/production cut/configuration is not yet named.
- Numeric opcode/layout inventory has not been mechanically generated for this cut.
- Exact initial post-admission bootstrap order requires controlled source tracing/fixture execution.
- Build-specific Current layouts, including weapon proficiency and modern systems, need exact client build string/fixtures.
- Asset/appearance source and rights are unresolved in PR #142.
- Release-required versus deferred feature families require aggregation/product decisions.
- Some subsystems may be compiled/configured but disabled at runtime; declaration alone is not deployment proof.

## 22. P0 result

The exact inspected Canary source proves a broad Current-profile gameplay surface sufficient to decompose future work safely. It does not prove deployment compatibility, numeric layouts in the Rust client or product scope. Implementation must start with generated exact-source indexes and bounded fixtures, then proceed through sole shared domain contracts.
