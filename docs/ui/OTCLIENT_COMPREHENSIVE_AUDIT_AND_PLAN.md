# OTClient Comprehensive Audit and Delivery Plan

Audit finalized: 2026-07-26  
Task-start fork baseline: `blakinio/otclient` `main` at `715ba210e870304f66b5d5496899c6ea3ca9599d`  
Reviewed upstream baseline: `opentibiabr/otclient` `main` at `465b7a217e87502bb7f9980bf6e099718d0a9a49`  
Final synchronized fork baseline: `38ef14010cc01b16824dd646022c6f5d3ba93146`  
Synchronization PR: #26, squash-merged after exact-head CI run `30176493622`  
Task: `OTC-20260725-comprehensive-options-upstream-audit`

## 1. Purpose and evidence rules

This audit answers five separate questions:

1. Which client systems and Tibia Global-like options exist in the current fork?
2. Which systems have runtime or CI evidence, which are only wired in source, and which contain deterministic defects?
3. Which functionality is missing or requires Canary, Oteryn Platform, protocol, platform or asset work?
4. Which net effects from the exact reviewed 16-commit `opentibiabr/otclient` range can be synchronized without regressing Oteryn Identity, tests, architecture or security?
5. Which work from `solchanel/otclient-15`, upstream issues and recent pull requests is suitable for selective adoption?

External repositories were used read-only. All branches, commits and pull requests created by this work are confined to `blakinio/otclient`.

| Evidence level | Meaning |
|---|---|
| Runtime-proven | Behavior was exercised in a compiled client or exact-version integration/rehearsal. |
| CI-proven | Relevant builds/tests passed on the exact commit, but full interactive behavior was not manually exercised. |
| Source-wired | A visible control/callback and plausible backing implementation are present. |
| Source-only | Definitions, parser support or dormant code exist, but a complete user flow is not exposed or proven. |
| Partial | Related behavior exists, but semantics, version coverage, lifecycle or UI exposure are incomplete. |
| Broken | A deterministic source defect or reproducible failure is confirmed. |
| Missing | No complete equivalent was found. |
| External dependency | Correct behavior requires matching Canary, Platform, protocol, assets or operating-system contracts. |

Presence in source is not equivalent to runtime correctness. Compilation is not evidence of interactive, protocol or server compatibility.

## 2. Executive assessment

### 2.1 Current strengths

| Area | Assessment | Evidence / notes |
|---|---|---|
| Oteryn Identity | Implemented and CI-backed foundation; production rollout remains contract-gated | System-browser Authorization Code + PKCE, short-lived ticket, Gateway login, authoritative `world_id` routing and one-shot Game Session handoff exist. Oteryn mode has no password fallback. |
| Security hardening | CI-backed | Shell-safe external URL launch, stale protocol callback protection and one-shot credential handling are present. |
| Test foundation | CI-proven | Deterministic C++ unit tests, Lua tests, InputMessage contracts and bounded loopback integration are available. |
| Action bars and hotkeys | Strong source-wired foundation with lifecycle defects | Nine bars, profiles, drag/drop, item/spell/text/multi-action support, hotkeys and cooldown rendering exist. |
| Protocol/version architecture | Broad but uneven | Feature flags and version gates cover old and current protocols; modern payloads still need exact Canary fixtures. |
| Modular UI | Strong foundation | Most GUI work can remain in Lua/OTUI without renderer rewrites. |
| Asset installer | Security-sensitive and mature, with a known selection gap | Strict hashes and standard runtime paths exist. Archive selection remains deferred until mandatory installer evidence exists. |
| Windows CI | Current required platform policy | Fast/static and Lua checks remain required; compiled validation uses the five-job Windows matrix. |

### 2.2 Main gaps

| Area | Current result |
|---|---|
| Tibia Global option parity | Prior screenshot audit found 25 implemented, 7 partial, 24 missing and 2 visibly broken groups; this audit adds lifecycle/protocol defects. |
| Runtime acceptance | Many source-wired options lack representative 1080p, 1440p, 4K and ultrawide interaction evidence. |
| Options architecture | No complete basic/advanced metadata registry, import/export model or Global-like hotkey split. |
| Screenshot subsystem | Modern client-event parsing exists, but capture policy, backlog, storage and folder workflow are incomplete. |
| Dynamic layout | Fixed side panels exist; arbitrary sidebars, complete layout-tree persistence and migration are missing. |
| Taskboard | Protocol identifiers/parser hooks exist, but no complete shipped `game_taskboard` module exists. |
| Modern 15.2x protocol | Monk login, level/XP/resource/Forge behavior and exact Canary compatibility require focused contracts. |
| Lifecycle safety | Character-list recreation, action-bar cooldown state and Forge callbacks have deterministic defects. |
| Performance | Startup, autostats, updater hashing, outfit rendering and scaled text remain unresolved areas. |

## 3. Current options and GUI status

The detailed option matrix remains in `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`.

### 3.1 Controls and hotkeys

**Present/source-wired**

- Regular, Classic and Left Smart-Click mouse modes.
- Loot mouse modes.
- Primary and secondary keybinds.
- Chat On/Off profiles with add/copy/rename/remove/search.
- Per-action-bar button hotkeys.
- Item, spell, text, target, equip, use and multi-action types.

**Partial or broken**

- `hotkeyDelay` is not proven equivalent to Global keyboard delay.
- `moveStack` is not a complete selectable stack modifier.
- Action Bar Hotkeys and Custom Hotkeys are not complete separate pages.
- Custom action creation exists, but `New Action` is hidden/disabled.
- Upstream reports identify item-subtype and walking/classic-control boundary defects.

**Missing**

- OS-default/custom keyboard delay contract.
- Rotation modifier selector.
- Always-face-movement behavior.
- Basic/advanced filtering.

### 3.2 Interface and status

**Present/source-wired**

- Native and animated cursors.
- Mouse target highlight.
- Creature names, health, mana, Harmony and text/HUD scaling.
- Loot value frames/corners.
- Inventory/container expiry display.
- Special-condition HUD/bar ordering controls.

**Partial or broken**

- `Show Cooldown Bar` maps to a differently scoped cooldown-window option.
- Inventory expiry refresh checks the wrong event before cancellation.
- `Show Expiry On Unused Items` is exposed but disabled.
- Customisable/status-bar controls lack usable IDs or option keys.
- Scaled-text flicker and stale use-with indicator reports remain open.

**Missing**

- Big cursor option.
- Link-copy/open warning policy.
- Complete Global-like status bars around the viewport.
- Dynamic sidebar manager and complete layout persistence.

### 3.3 Console

**Present/source-wired**

- Info, event, own-status and others-status filters.
- Timestamps and level display.
- Channel tabs and private-message handling.

**Missing or partial**

- Explicit automatic PM-tab policy.
- Separate seconds-in-timestamps option.
- Complete channel persistence/unread acceptance tests.

### 3.4 Action bars

**Present/source-wired**

- Three bottom, three left and three right bars.
- Assigned hotkey, object count, spell parameters, graphical cooldown, cooldown seconds and tooltips.
- Per-profile persistence and lock groups.
- Clear controls for individual bars.

**Concrete defects**

- Right Bar 3 reset targets bar 7 instead of bar 9.
- `clearRightBar3` is duplicated as another widget ID.
- Cooldown packets can arrive before action-bar listeners connect.
- Cooldown caches reset or ignore state at unsafe lifecycle points.
- `setupActionBar` can stop an overlay after `updateButton` restores it.
- Protocol cooldown state can be discarded when visual cooldown options are disabled.
- Simple runes do not consistently use the same restoration path as spells/multi-actions.

**Missing**

- Auto-insert new spells policy.
- Dedicated Global-like Action Bar Hotkeys list.

### 3.5 Miscellaneous, screenshots and help

**Present/source-only**

- `Allow auto chase override` and feature-profile selector.
- Core screenshot/client-event parsing for legacy and 15.21+ events.
- Language selection and cache clearing.

**Missing user flow**

- Only-game-window capture.
- Five-second screenshot backlog.
- Auto-screenshot master switch and event matrix.
- Open screenshot folder.
- Options/minimap import/export.
- Purchase/container confirmation policies.
- Secure Global-like quick-login/session persistence.
- Inspect-me and nearby-corpse quick-loot policy.

The existing screenshot parser should be reused. Missing work is primarily capture service, settings, storage, privacy and platform integration.

## 4. Deterministic defects and current disposition

| Priority | Defect | Current disposition | Required proof |
|---|---|---|---|
| P0 | Unknown-opcode recovery can revisit unread bytes and exhaust memory | Fixed in merged PR #26 | Preserve bounded skip-to-EOF behavior and existing InputMessage contracts. |
| P0 | Asset installer may select an unrelated legacy ZIP | Reviewed; deferred | Release metadata fixtures, strict fallback tests, install-path proof and runtime-load verification. |
| P1 | Character list cannot reliably recreate OTUI after destroy/relogin | Active draft PR #31 | Absolute module paths, nil-safe failure and repeated legacy/Oteryn lifecycle tests. |
| P1 | Action-bar cooldown state is lost after relog | Confirmed / issue #1776 | Module-lifetime listeners, session caches and restoration tests. |
| P1 | Wheel conviction summary reads shifted slots | Confirmed / issue #1753 | Named indices and Lua contract tests. |
| P1 | Forge callbacks can outlive controller state | Confirmed / issue #1691 | Cancel event handles or generation-guard callbacks. |
| P1 | Right Bar 3 clears wrong bar and duplicates ID | Confirmed | Bar 9 mapping, unique ID and Lua/OTUI test. |
| P1 | Inventory expiry cancellation checks wrong event | Confirmed | Correct event ownership and rapid-toggle test. |
| P2 | Walk-delay controls display wrong setup label | Confirmed | Correct labels and slider/value binding verification. |
| P2 | Disabled unused-expiry and dead status-bar controls | Incomplete exposure | Implement backing behavior or hide unsupported controls. |
| P2 | `showExpiryInInvetory` misspelling | Migration risk | Correct key with backward-compatible migration. |

## 5. Exact 16-commit upstream synchronization

### 5.1 Final baseline and merge evidence

- recorded merge base: `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`;
- reviewed upstream head: `465b7a217e87502bb7f9980bf6e099718d0a9a49`;
- exact reviewed upstream-only count: 16;
- refreshed exact PR head: `4f9958c5b834e911e06ffb5e10f1193400f545e7`;
- exact-head CI run: `30176493622`, success;
- squash result in `main`: `38ef14010cc01b16824dd646022c6f5d3ba93146`;
- Oteryn enter-game/auth/session and shell-safe URL paths were absent from the synchronization net diff.

The final exact head passed Fast Checks, Lua Syntax, CMake Release, CMake Tests with CTest, Solution Debug, Solution OpenGL, Solution DirectX and `CI / Required`.

Repository settings allow squash merge only. Upstream SHAs are therefore documented as the durable comparison baseline rather than expected in `main` ancestry.

### 5.2 Per-commit disposition

| Commit | Change | Final disposition | Reason / acceptance |
|---|---|---|---|
| `465b7a2` | Select release archives by requested client version/tag | **Deferred; excluded** | Mandatory asset gate lacks release fixtures, final-path and runtime-load evidence. |
| `8af3aa4` | NPC trade quantity with equipped imbued items | **Retained with local lifecycle fix** | Corrects double subtraction; tracker also stops on terminate/game end. |
| `caba9ce` | Pause/resume Stats collection | **Retained** | Useful diagnostics primitive; `g_stats.pause/resume` catalogued. |
| `350e506` | Rendering/preload ordering | **Deferred; excluded** | Upstream implementation reverses framework-to-client dependency direction. |
| `225ce4d` | Animator-driven always-animated outfit/mount phase | **Retained** | Compiled evidence exists; exact asset/runtime behavior remains unproven. |
| `89e7898` | NPC trade positioning/chat overlap | **Retained** | Low protocol risk; visual resolution checks remain follow-up. |
| `cee2851` | Restore `lastManualWalk` | **Retained** | Restores optional bot/manual-input coordination. |
| `dedc737` | `--user-dir` override | **Retained** | Useful portable/test isolation surface. |
| `a7d1b39` | Correct pre-780 use-with source stack position | **Retained** | Version-specific correctness; exact old-protocol proof remains follow-up. |
| `fec1cca` | `TargetBot.Danger()` | **Retained** | Optional bot API; returns zero while disabled. |
| `cd4441e` | Stop unknown-opcode busy loop/OOM | **Retained** | Defensive bounded parser behavior; existing InputMessage contracts reused. |
| `de0af30` | Fixed 1 GiB browser heap | **Retained with historical browser evidence only** | Current final policy does not claim browser compatibility. |
| `a28fc1c` | Ground-border use-with target | **Retained** | Interaction proof remains follow-up. |
| `e0092f0` | Browser Lua/UIGraph/shader compatibility | **Retained with historical browser evidence only** | Lua syntax is current; non-Windows runtime is not claimed. |
| `76a3260` | Reward-wall collect-source byte | **Deferred; excluded** | Missing exact Canary producer, shared `OTS-*`, matrix and paired tests. |
| `a4cbf1a` | Cocoa mouse delta | **Retained with historical macOS evidence only** | Current Windows gate does not claim macOS runtime compatibility. |

### 5.3 Local safety adaptations and audit findings

- NPC imbuement tracking now stops during module termination and game-session end, not only NPC-close events.
- `g_stats.pause/resume`, `--user-dir`, `TargetBot.Danger()` and `lastManualWalk` are catalogued as maintained interfaces.
- A mistaken ranged-read replacement temporarily truncated `game_npctrader.lua`; the exact prior blob was restored immediately before intended edits. Final diff contains no lost content. Never replace a complete file from a ranged fetch.
- A redundant unknown-opcode integration test was removed after existing unit contracts were found.
- The complete net diff and branch-history-only file list were both reviewed before merge.

## 6. `solchanel/otclient-15` selective review

The repository diverges heavily and combines protocol, UI, workflows and binary assets. It must not be bulk-merged. An MIT repository file does not prove redistribution rights for third-party game graphics.

### 6.1 Protocol clues

| Candidate | Assessment | Disposition |
|---|---|---|
| `0053457` — 15.22 compatibility | Partly superseded; includes no-op weekly parser and broad hard-coded changes. | Compare individual fields to exact Canary; do not cherry-pick. |
| `c3f3d14` — missing 15.12 changes | Contains a Cyclopedia `levelPercent` double-read/desync risk. | Reject wholesale; reimplement confirmed fields with fixtures. |
| `2744cac` — level-percent fix | Direction is plausible; transition version must match Canary/features. | Adapt only with feature-gated tests. |
| `44f8794` — dual compression | Networking-wide framing/proxy/TLS risk. | Defer until demonstrated and round-trip tested. |
| `3b47bab` — raw world name in `Protocol::send` | May overlap authoritative Oteryn routing. | Review separately; never replace Gateway `world_id`. |
| `3f49b19` — store/rewardwall formats | Potentially useful but payload-dependent. | Adapt only under exact cross-repository contract. |

### 6.2 Taskboard

The `b1a3e7e` proof of concept covers bounties, preferred/unwanted monsters, weekly tasks, shop, Soulseals, trackers and modal UI, but is unsuitable for direct adoption because it mixes a large feature with binary assets, hard-coded economy values, no exact Canary pair and insufficient malformed/relog/lifecycle tests.

Required design:

1. Canary remains authoritative for availability, prices, balances, progress, rewards and errors.
2. Reuse existing `GameTaskboard` and `parseTaskBoard*` entry points.
3. Create a shared `OTS-*` contract with exact opcodes/subtypes/order/widths/optionals/gates.
4. Add C++ parser fixtures and Lua callback contracts before UI.
5. Build a controller-owned `modules/game_taskboard` module.
6. Use original Oteryn assets with source/license/hash records.
7. Fail closed on unsupported one-sided combinations.
8. Validate exact-version bounty, weekly, shop, preferred slots, Soulseals, trackers and relog flows.

Taskboard remains a separate cross-repository milestone.

## 7. Issue and work queue

### 7.1 Deterministic client repairs

| Issue/area | Assessment | Planned action |
|---|---|---|
| #1775 character-list relog | UI path/lifecycle risk confirmed | Draft PR #31 with absolute module path, nil-safe adapter and focused tests. |
| #1776 cooldowns after relog | Root cause confirmed | Module-lifetime protocol listeners, session caches and max remaining restoration. |
| #1753 Wheel conviction indices | Static mismatch deterministic | Named index map and Lua contract. |
| #1691 Forge expired callbacks | Scheduled-event lifecycle defect | Track/cancel handles or generation guard. |
| Existing Global audit defects | Deterministic | Narrow repair PRs, not one broad redesign. |

### 7.2 Protocol/Canary contract queue

- Monk 15.25 opcode/desync: exact client/server packet, producer handler and Canary commit.
- 15.24 XP/fragments/portable Forge: separate percentage, XP, resource-ID and request/response tests.
- Forge convergence: exact version pair and state transitions.
- VIP 10.98: exact packet fixture and filtering/state test.
- Creature move/desync: distinguish client defect from mismatched assets/custom opcodes.
- Reward Wall: exact producer, source-byte semantics, rollout matrix and paired tests.

### 7.3 Interaction and performance queue

- Container move/last-panel drag ownership.
- Miniwindow keyboard focus and modal routing.
- Hotkey item subtype boundaries.
- Creature target hit testing while walking.
- Stale use-with cursor cleanup.
- Classic LMB+RMB state machine.
- Repeated-walk-key measurement and predictive behavior.
- Renamed-creature battle-list reindexing by ID.
- Debug startup, autostats CPU, updater hashing, outfit preview performance and scaled-text flicker.
- Android/browser/macOS acceptance only after explicit platform policy changes.

## 8. Security and compatibility invariants

Every phase must preserve:

1. Oteryn mode never sends or stores the user's Oteryn password.
2. Oteryn mode never silently falls back to legacy password authentication.
3. OAuth state, callback path, PKCE and HTTPS endpoint validation remain strict.
4. Game Session credentials remain one-shot and clear after first normal handoff.
5. Auto-reconnect never replays an Oteryn Game Session credential.
6. Gateway `world_id` remains authoritative routing input.
7. External URLs remain exact argv values, never shell-interpolated commands.
8. Asset hashes and final runtime paths remain strict.
9. Unknown or malformed protocol data fails boundedly.
10. New protocol fields are feature/version gated and paired with exact Canary tests.
11. No proprietary assets are committed without demonstrated rights.
12. Framework primitives do not depend on client/game modules.
13. Dormant platform compatibility is not inferred from Windows CI.

## 9. Delivery roadmap

### Phase 0 — synchronize and stabilize the base: **complete**

- PR #26 exact-head Windows CI passed.
- Reviewed net effects were squash-merged as `38ef14010cc01b16824dd646022c6f5d3ba93146`.
- Upstream head and all 16 dispositions are recorded.
- Rendering/preload, Reward Wall and archive selection remain deferred.
- Post-merge archive PR #32 records terminal task metadata.

### Phase 1 — deterministic lifecycle and option repairs: **in progress**

- Character-list destroy/recreate fix — draft PR #31.
- Action-bar cooldown relog restoration.
- Forge event cleanup.
- Wheel conviction index fix.
- Right Bar 3, duplicate ID, expiry event, labels and unsupported controls.
- Backward-compatible setting-key migration.

**Exit:** focused tests exist and repeated login/logout/reload cycles do not leak or lose state.

### Phase 2 — modern protocol 15.24/15.25 compatibility

- Monk login field/order investigation.
- Level-percent width normalization and XP formula.
- Fragment resources and Wheel balances.
- Portable Forge request/response flow.
- Store/Reward Wall under exact contracts.
- VIP 10.98 and chargeable 7.80–8.54 fixtures.

**Exit:** exact linked Canary/client pairs pass parser/output and integration tests.

### Phase 3 — options architecture

- Metadata-driven option registry and basic/advanced filtering.
- Separate General, Action Bar and Custom Hotkey views.
- Seconds in timestamps, PM policy, big cursor, link warning and auto-insert spells.
- Schema-versioned settings/minimap import/export.

### Phase 4 — screenshots and layout

- Reuse existing client-event parser.
- Game-window/full-client capture service and bounded five-second backlog.
- Event trigger policy, screenshot folder workflow and tested privacy/storage limits.
- Dynamic sidebars and layout-tree persistence/migration.
- Original Oteryn skin/assets.

### Phase 5 — Taskboard

- Shared Canary/OTClient contract.
- Parser/output fixtures and gates.
- Controller-owned UI and original assets.
- Bounty, weekly, preferred slots, shop, Soulseals and tracker integration.
- Relog, malformed data, unsupported server and economy-authority tests.

### Phase 6 — interaction and measured performance

- Containers, focus, target hit testing, classic controls and cursor state.
- Startup, autostats, updater hashing, outfit performance and text flicker.
- Separate browser/macOS/Android acceptance after explicit policy changes.

## 10. Test and acceptance matrix

| Change type | Required minimum |
|---|---|
| Documentation | Current-base diff review and required lightweight CI. |
| Lua/module lifecycle | Lua syntax, focused Lua test and repeated init/terminate/login/logout. |
| OTUI/layout | Parse/load and representative Windows interaction/scaling evidence. |
| C++ core/framework | Focused tests plus final five-job Windows matrix. |
| Protocol parser/output | Framed fixture, malformed/truncated cases, gates and exact Canary pair. |
| Authentication | PKCE/callback/Gateway/session positive and negative tests. |
| Assets | Source/license/hash/path review, strict manifests, installation and runtime load. |
| Performance | Before/after measurement, cancellation/lifetime and no UI-thread stall. |
| Dormant non-Windows platform | Source review or historical evidence only; no current compatibility claim. |

Final acceptance for a user-facing option requires visibility classification, persistence/migration, observable behavior, related-setting interaction, unsupported-combination handling, representative Windows resolution/DPI evidence and exact server pairing when payload-dependent.

## 11. Immediate execution order

1. Merge archive PR #32 after lightweight CI.
2. Refresh, validate and squash-merge audit PR #25; archive its task.
3. Complete and merge character-list lifecycle PR #31.
4. Deliver action-bar cooldown lifecycle repair.
5. Deliver Wheel, Forge and deterministic options repairs as focused PRs.
6. Reconcile Oteryn presentation PR #23 after manual Windows visual approval.
7. Open asset archive-selection and architecture-safe renderer preload tasks only when their evidence gates are satisfiable.
8. Start modern protocol and Taskboard work only with exact Canary pairs and provenance-safe assets.

This order removes confirmed lifecycle and state-loss defects before adding broad UI or protocol surface.
