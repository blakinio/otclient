# P0 Legacy User Workflow Inventory

Status cut: `main@9c03a448457b1715818e094fdfdeade4a1450434`  
Lane: `OTC2-20260801-playability-p0-legacy` / PR #141  
Legacy runtime dependency authorized: **no**

## 1. Purpose

Inventory player-visible workflows and recovery expectations evidenced by the maintained legacy client. The inventory records outcomes, preconditions and evidence paths; it does not make legacy C++/Lua/OTUI class/module structure normative for Rust.

The exact release-required set remains subject to Canary capability evidence from PR #140 and product classification at the P0 aggregation barrier.

## 2. Evidence boundary

Primary maintained reference:

- `docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md` — layer ownership, auth/session invariants, feature/UI areas, settings/assets and test expectations.

Representative exact behavior paths inspected:

- `modules/game_interface/gameinterface.lua` — root game UI, viewport/panels, focus, geometry, input grab, logout/exit and game start/end lifecycle;
- `modules/game_inventory/inventory.lua` — equipment slots, inventory presentation, combat posture/fight/chase modes and feature-gated behavior;
- `modules/game_console/console.lua` — local/private/channel/NPC/monster message modes and presentation distinctions;
- `modules/game_minimap/minimap.lua` — player-position tracking, floor state, camera/cross position and persisted minimap behavior;
- `modules/client_entergame/**` — login/profile/selection/auth/session behavior, read-only for this lane;
- `modules/game_actionbar/**`, `modules/game_battle/**`, `modules/game_healthinfo/**`, `modules/game_skills/**`, `modules/game_containers/**`, `modules/game_hotkeys/**`, `modules/game_options/**` and other shipped feature modules — workflow evidence only where present;
- `src/client/**` and `modules/game_features/**` — authoritative legacy game/protocol state and negotiated feature evidence, not Rust design;
- `data/styles/**`, `data/images/ui/**`, `modules/**/*.otui` — presentation evidence only; no visual/asset copying.

Exact Canary/server facts must come from PR #140 or exact producer source, not from legacy assumptions alone.

## 3. Workflow classification

- **Core playability** — required to enter a visible world, move, interact, recover and leave safely.
- **Core gameplay** — ordinary hunting/interaction loop required for M3.
- **Daily product** — usability expected for regular play in M4.
- **Exact-profile parity** — version/feature-specific capability required only if the selected Oteryn/Canary profile exposes it and product scope includes it.
- **Intentional non-parity candidate** — legacy behavior that should be replaced for security, architecture, accessibility or maintainability.

## 4. Launch and login journey

### User outcome

The player can launch the client, choose the Oteryn profile, authenticate through the system browser, receive a world/character directory, select an allowed character/world and enter or receive a recoverable safe error.

### Preconditions

- supported client/profile and producer cuts;
- valid project-owned service configuration;
- network/TLS/browser loopback available;
- approved account/character;
- required assets/runtime present or a repair action exists.

### Actions and observables

1. launch one client process and visible window;
2. choose/sign into Oteryn without entering the main account password in the game client;
3. observe browser/auth progress and cancellation;
4. return through validated loopback callback;
5. see authoritative worlds/characters and availability/compatibility;
6. select a valid character/world/channel when the producer exposes it;
7. observe connection/admission progress;
8. enter the game or receive one stable recovery action.

### Recovery

- invalid/expired callback: authenticate again;
- directory/compatibility issue: refresh or return to login without credential reuse;
- one-shot credential failure after handoff: request a fresh credential, never replay;
- unsupported client/profile: update or select supported target;
- missing/corrupt approved assets: repair/import path, not arbitrary loose-file fallback;
- cancel/close: deterministic teardown.

### Evidence

`modules/client_entergame/**`, authentication/session paths listed in `LEGACY_OTCLIENT_ARCHITECTURE.md`, and current Rust W7 contracts. The legacy password path is not a parity requirement for the Oteryn profile.

Classification: core playability / M1.

## 5. Selection and relog journey

### User outcome

The player can inspect authoritative character/world information, choose one valid relationship, enter, later logout/relog and select another valid target without restarting the entire application when account-session policy allows.

Required behavior:

- clear selected character/world/channel identity;
- invalid or unavailable combinations disabled with reason;
- explicit connect/cancel/back actions;
- safe return to selection after normal logout or recoverable disconnect;
- new one-shot credential for every new game session;
- session-scoped state destroyed before replacement;
- account session and game session shown as separate lifetimes.

Evidence: `modules/client_entergame/**`, `modules/game_interface/**`, legacy architecture auth/session invariants.

Classification: core playability M1/M3; polished daily product M4.

## 6. Visible world and navigation

### User outcome

After admission the player sees the correct local world context and can navigate using keyboard/mouse actions while server state remains authoritative.

Required capabilities:

- initial map/floor/tile state;
- local character and visible creature/item/effect presentation;
- camera/floor context;
- keyboard walking/turning and mouse navigation where supported;
- server movement/teleport/reconciliation reflected visibly;
- held movement clears on focus loss/modal/disconnect;
- no UI or renderer owns authoritative position.

Legacy evidence:

- `modules/game_interface/gameinterface.lua` owns the game map panel, mouse grabber, panel geometry and game lifecycle presentation;
- `modules/game_minimap/minimap.lua` tracks local-player position, camera/cross position and active floor;
- `src/client/**` owns legacy map/game state.

Classification: core playability M2.

## 7. HUD, player state and status

### User outcome

The player can understand health/mana, skills/stats, conditions, cooldowns, connection state and important combat feedback.

Observable requirements:

- bounded, timely updates with unavailable/unknown distinguished from zero;
- condition/cooldown timing tied to accepted domain state;
- death/logout/disconnect state clearly changes available actions;
- important status does not rely on color alone;
- no fabricated values when protocol/profile lacks a capability;
- high-DPI and panel layout remain usable.

Evidence areas: `modules/game_healthinfo/**`, `modules/game_skills/**`, `modules/game_interface/**`, `src/client/**`.

Classification: minimum subset M2; full core gameplay M3; polish/accessibility M4.

## 8. Creature, targeting and combat loop

### User outcome

The player can discover visible creatures, select/attack/follow/stop according to server rules and understand target/combat outcomes.

Sequence:

1. creature appears/moves/changes health/state;
2. battle/viewport representation stays correlated;
3. player selects target by viewport or list;
4. semantic attack/follow/stop action is emitted;
5. server acceptance/rejection updates authoritative state;
6. damage/effects/conditions/death/cooldowns are visible;
7. target loss/disconnect clears stale selection safely.

Negative/recovery:

- stale/removed creature cannot remain actionable;
- unsupported command is disabled/explained;
- packet/order loss cannot leave UI claiming an authoritative target incorrectly;
- focus/modal state prevents accidental command leakage.

Evidence areas: `modules/game_battle/**`, `modules/game_interface/**`, combat controls in `modules/game_inventory/inventory.lua`, `src/client/**`.

Classification: core gameplay M3.

## 9. Inventory, equipment and containers

### User outcome

The player can inspect equipment/inventory/containers, look/use/move items and understand accepted/rejected server changes.

Legacy evidence:

- `modules/game_inventory/inventory.lua` maps equipment slots, feature-gated presentation and fight/chase posture controls;
- `modules/game_containers/**` and `src/client/**` provide container/item behavior evidence.

Required behavior:

- typed item/slot/container identity and capacity/state;
- open/close/nested/paginated containers where supported;
- look/use/use-with/move/equip/unequip semantic actions;
- drag/drop preview and keyboard/accessibility alternative;
- optimistic presentation, if any, reconciles to server truth;
- stack/count/weight/tier/feature metadata only when authoritative;
- stale source/target/session cancels the action;
- error/recovery is clear without duplicating a move.

Classification: core gameplay M3; daily-product layout/usability M4.

## 10. Chat, NPC and social text

### User outcome

The player can read/send supported local, channel, private and NPC communication and recover from unavailable/closed channels.

Legacy evidence:

`modules/game_console/console.lua` distinguishes say/whisper/yell, private, NPC, channel, management/highlight, monster and ignored message modes.

Required behavior:

- authoritative channel list/membership and message metadata;
- separate text entry from gameplay key actions;
- Unicode/IME, history navigation and keyboard focus;
- bounded virtualized history;
- unread/highlight/private/NPC semantics;
- safe links/clipboard and privacy-aware diagnostics;
- rate/error/rejection feedback;
- closed/unavailable channel handling;
- no raw packet/backend text bypassing validation/classification.

Classification: core gameplay M3; daily-product localization/accessibility/privacy M4.

## 11. NPC commerce, trade, depot and market

Candidate workflows, only when exact server/profile evidence exists:

- NPC conversation and buy/sell quantity/price confirmation;
- player trade invite, offer inspection, accept/cancel/change/rejection;
- depot/inbox/stash access and item movement;
- market browse/search/history/offer create/cancel/accept;
- server-authoritative balances, limits, fees and confirmation states;
- stale offer/session and network recovery.

Evidence areas: representative shipped feature modules and `src/client/**`; exact capability/version must come from PR #140.

Classification: exact-profile parity M5 unless product owner classifies a subset as M3/M4.

## 12. Action bars, hotkeys and settings

### User outcome

The player can bind semantic actions, see availability/cooldowns, resolve conflicts and persist safe settings/layout.

Evidence areas: `modules/game_actionbar/**`, `modules/game_hotkeys/**`, `modules/client_options/**`, feature settings, `modules/game_interface/**` persistence behavior.

Required behavior:

- explicit action/binding identity;
- gameplay/chat/modal contexts;
- conflict/reserved-binding result before commit;
- action slot displays authoritative availability/cooldown;
- typed scope and migration;
- reset/default/import/export with bounds and no secrets;
- settings apply is observable and reversible where practical;
- unsupported capability settings are hidden/disabled with reason;
- layout restoration keeps mandatory UI visible.

Classification: action bindings core M3; full settings/layout daily product M4.

## 13. Minimap and map controls

### User outcome

The player can understand location/floor context, follow the local character, pan/zoom/reset and use supported markers/navigation without confusing minimap state with authoritative world routing.

Legacy evidence:

`modules/game_minimap/minimap.lua` tracks local player position, camera/cross position, active floor, world time presentation and persisted map state.

Required behavior:

- current location/floor follows accepted domain position;
- pan/zoom/floor/reset actions;
- map availability/unknown regions explicit;
- bounded marker/annotation persistence if included;
- no arbitrary untrusted minimap file import by default;
- no stale session position after relog;
- keyboard/accessibility alternatives.

Classification: daily product M4; minimum floor/camera context may exist in M2.

## 14. Audio and notifications

### User outcome

The player receives supported UI/game/positional feedback with category controls and safe device recovery.

Legacy audio behavior is evidence only. Rust requirements:

- typed audio intents from accepted domain/UI events;
- UI versus positional/category separation;
- bounded voice/prioritization;
- no frame/audio-callback I/O or decode;
- mute/gain settings and device replacement;
- important information also has non-audio presentation;
- source/rights approval from PR #142.

Classification: required core feedback M3 where selected; product controls/recovery M4.

## 15. Death, logout, disconnect and recovery

### Normal logout

- deliberate logout action;
- server/session closure when available;
- session-scoped state/UI/input/audio destroyed;
- return to safe selection/logged-out state;
- no credential replay.

### Death

- clear death/result presentation;
- invalid gameplay actions disabled;
- server-supported relog/selection action;
- no client-authoritative death/economy decisions.

### Network/server failure

- distinguish retryable pre-handoff from fresh-auth/relog-required post-handoff failures;
- no hidden infinite retry;
- user-visible stable action;
- stale world/UI/capture/target state cleared;
- support evidence remains secret-safe.

Evidence: `modules/game_interface/**`, `modules/client_entergame/**`, feature lifecycle modules and current Rust shutdown/session contracts.

Classification: core playability/gameplay M2-M3; polished recovery M4.

## 16. Installation, asset repair and update

Legacy behavior can inform:

- clean install/start;
- selected asset/version acquisition;
- progress/cancel/failure;
- digest validation before extraction;
- repair of missing/corrupt content;
- rollback/known-good behavior;
- user-facing incompatible version action.

Evidence: `modules/client_assets/**`, `docs/client-assets-auto-install.md`, open PR #97 and platform/update paths. No legacy downloader becomes a Rust runtime dependency, and third-party source availability does not establish rights.

Classification: daily product M4; production hardening M6.

## 17. Version-specific feature families

The legacy client contains or anticipates many feature-gated systems. Candidate families include:

- party/guild/VIP/social;
- trade/depot/stash/inbox;
- market;
- quests/quest log;
- prey/task/hunting systems;
- imbuements/forge/upgrades;
- bestiary/charms/cyclopedia;
- wheel/gem/vocation-specific systems;
- tournament/store/analytics or other profile-specific panels.

They are `UNKNOWN` until PR #140 proves exact server support and the aggregation barrier classifies them. Presence in legacy modules alone is not release scope.

## 18. Intentional non-parity candidates

Do not copy by default:

- Lua/global mutable service state and module load-order coupling;
- UI directly reading protocol or feature internals;
- widget IDs/OTUI layouts as public compatibility contracts;
- password login/fallback for the Oteryn profile;
- implicit retries or credential reuse;
- arbitrary downloadable/proprietary asset assumptions;
- inactive controls without an explanation;
- raw backend/OS errors shown to users;
- color-only or mouse-only mandatory interactions;
- unrestricted settings/import/export or unbounded persisted layout;
- bots/automation or anti-cheat circumvention behaviors;
- official-service automation.

The Rust product may intentionally improve accessibility, recovery, security and maintainability while preserving the accepted user outcome.

## 19. Cross-lane dependencies

| Requirement | Owning evidence |
|---|---|
| exact supported message/feature families | PR #140 |
| source/runtime/font/audio rights and handles | PR #142 |
| UI/input/audio core/feature decomposition | PR #143 |
| controlled scenarios, hardware, performance, soak and release evidence | PR #144 |
| final release-required/deferred classification | P0 aggregation barrier |

## 20. P0 boundary

This inventory authorizes no source, UI framework, protocol implementation, asset extraction or feature scope decision.
