# OTClient Comprehensive Audit and Delivery Plan

Audit date: 2026-07-25  
Task-start fork baseline: `blakinio/otclient` `main` at `715ba210e870304f66b5d5496899c6ea3ca9599d`  
Reviewed upstream baseline: `opentibiabr/otclient` `main` at `465b7a217e87502bb7f9980bf6e099718d0a9a49`  
Current synchronization base: `b352c3c5769f8e778085174fb82cb289bcebdd59`  
Current synchronization candidate: PR #26 at `3efc9a95ff91f48cc753af3dad024bd45d5137ce`  
Task: `OTC-20260725-comprehensive-options-upstream-audit`

## 1. Purpose

This audit answers five separate questions:

1. Which client systems and Tibia Global-like options exist in the current fork?
2. Which systems have runtime or CI evidence, which are only wired in source, and which contain deterministic defects?
3. Which functionality is missing or requires Canary, Oteryn Platform, protocol, platform or asset work?
4. Which net effects from the exact reviewed 16-commit `opentibiabr/otclient` range can be synchronized without regressing Oteryn Identity, tests, architecture or security?
5. Which work from `solchanel/otclient-15`, upstream issues and recent pull requests is suitable for selective adoption?

External repositories were used read-only. All branches, commits and pull requests created by this task are confined to `blakinio/otclient`.

## 2. Evidence levels

| Level | Meaning |
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

## 3. Executive assessment

### 3.1 Current strengths

| Area | Assessment | Evidence / notes |
|---|---|---|
| Oteryn Identity login | Runtime-proven foundation; production rollout still contract-gated | System-browser Authorization Code + PKCE, short-lived ticket, Gateway login, authoritative `world_id` routing and one-shot Game Session handoff are merged. Oteryn mode has no password fallback. |
| Security hardening | CI/runtime evidence | Shell-safe external URL launch, stale protocol callback protection and one-shot credential handling are present. |
| Test foundation | CI-proven | Deterministic C++ unit tests, Lua tests, InputMessage contracts and bounded loopback integration are merged. |
| Action bars and hotkeys | Strong source-wired foundation with lifecycle defects | Nine bars, profiles, drag/drop, item/spell/text/multi-action support, hotkeys and cooldown rendering exist. |
| Protocol/version architecture | Broad but uneven | Feature flags and version gates cover old and current protocols, but modern payloads need exact Canary fixtures. |
| Modular UI | Strong foundation | Most GUI work can remain in Lua/OTUI without renderer rewrites. |
| Asset installer | Security-sensitive and mature, with a known selection gap | Strict hashes and standard runtime paths exist. The upstream archive-selection idea is useful but remains deferred until mandatory installer evidence exists. |
| Windows CI | Current required platform policy | Fast/static and Lua checks remain required; final compiled validation uses the five-job Windows matrix only. |

### 3.2 Main gaps

| Area | Current result |
|---|---|
| Tibia Global option parity | Previous screenshot audit found 25 implemented, 7 partial, 24 missing and 2 visibly broken groups; this audit adds lifecycle/protocol defects. |
| Runtime acceptance | Many source-wired options lack interaction evidence at 1080p, 1440p, 4K and ultrawide resolutions. |
| Options architecture | No complete basic/advanced metadata registry, import/export model or Global-like hotkey split. |
| Screenshot subsystem | Modern client-event parsing exists, but capture policy, backlog, storage and folder workflow are incomplete. |
| Dynamic layout | Fixed side panels exist; arbitrary sidebars, complete layout-tree persistence and migration are missing. |
| Taskboard | Protocol identifiers/parser hooks exist, but no complete shipped `game_taskboard` module exists. |
| Modern 15.2x protocol | Monk login, level/XP/resource/Forge behavior and exact Canary compatibility need focused contracts. |
| Lifecycle safety | Character-list recreation, action-bar cooldown state and Forge callbacks have deterministic risks. |
| Performance | Startup, autostats, updater hashing, outfit rendering and scaled text remain unresolved areas. |

## 4. Current options and GUI status

The detailed option-by-option matrix remains in `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`. The highest-impact findings are summarized here.

### 4.1 Controls and hotkeys

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
- Issue #1229 reports item subtype handling at the hotkey boundary.
- Issues #1338 and #1358 report walking/classic-control interaction defects.

**Missing**

- OS-default/custom keyboard delay contract.
- Rotation modifier selector.
- Always-face-movement behavior.
- Basic/advanced filtering.

### 4.2 Interface and status

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
- Issue #1518 reports a stale use-with cursor indicator.
- Issue #1435 reports scaled-text flicker.

**Missing**

- Big cursor option.
- Link-copy/open warning policy.
- Complete Global-like status bars around the viewport.
- Dynamic sidebar manager and complete layout persistence.

### 4.3 Console

**Present/source-wired**

- Info, event, own-status and others-status filters.
- Timestamps and level display.
- Channel tabs and private-message handling.

**Missing or partial**

- Explicit automatic PM-tab policy.
- Separate seconds-in-timestamps option.
- Complete channel persistence/unread acceptance tests.

### 4.4 Action bars

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

### 4.5 Miscellaneous, screenshots and help

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

The existing screenshot parser should be reused. The missing work is primarily capture service, settings, storage, privacy and platform integration.

## 5. Deterministic defects confirmed in current source

| Priority | Defect | Current disposition | Required next proof |
|---|---|---|---|
| P0 | Unknown-opcode recovery can revisit unread bytes and exhaust memory | Retained from upstream commit `cd4441e` in PR #26 | Preserve `skipBytes(unreadSize)`; existing InputMessage tests already prove header/body cursor semantics and EOF skip. |
| P0 | Asset installer may select an unrelated legacy ZIP | Upstream commit `465b7a2` reviewed, net effect deferred | Add release metadata fixtures, strict fallback tests, install-path proof and runtime-load verification. |
| P1 | Character list cannot reliably recreate OTUI after destroy/relogin | Confirmed source risk / issue #1775 | Absolute module layout paths, nil-safe failure and repeated Oteryn/legacy destroy/create tests. |
| P1 | Action-bar cooldown state is lost after relog | Confirmed source/lifecycle risk / issue #1776 | Module-lifetime listeners, session-scoped caches and restoration tests. |
| P1 | Wheel conviction summary reads shifted slots | Deterministic issue #1753 | Named indices and Lua contract tests. |
| P1 | Forge callbacks can outlive controller state | Deterministic issue #1691 | Cancel event handles or generation-guard callbacks. |
| P1 | Right Bar 3 clears wrong bar and duplicates ID | Confirmed | Map to bar 9, unique ID, Lua/OTUI test. |
| P1 | Inventory expiry cancellation checks wrong event | Confirmed | Correct event ownership and rapid-toggle test. |
| P2 | Walk-delay controls display wrong setup label | Confirmed | Correct labels and verify slider/value binding. |
| P2 | Disabled unused-expiry and dead status-bar controls | Incomplete exposure | Implement backing behavior or hide unsupported controls. |
| P2 | `showExpiryInInvetory` misspelling | Migration risk | Correct key with backward-compatible one-time migration. |

## 6. Exact reviewed 16-commit upstream synchronization

### 6.1 Baseline and merge policy

- recorded merge base: `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`;
- reviewed upstream head: `465b7a217e87502bb7f9980bf6e099718d0a9a49`;
- exact reviewed upstream-only count: 16;
- current PR #26 head: `3efc9a95ff91f48cc753af3dad024bd45d5137ce`;
- current PR #26 base: `b352c3c5769f8e778085174fb82cb289bcebdd59`;
- current-base net diff: 29 files;
- Oteryn enter-game/auth/session and shell-safe URL paths are absent from the net diff.

Repository settings allow squash merge only, and root `AGENTS.md` requires the repository-supported method. Therefore:

- PR #26 must squash-merge;
- upstream SHAs will not be preserved in `main` ancestry;
- the upstream head and table below are the durable synchronization baseline;
- future synchronization must compare from the recorded upstream head rather than infer state only from `main` ancestry.

### 6.2 Per-commit disposition

| Commit | Change | Final disposition | Reason / acceptance |
|---|---|---|---|
| `465b7a2` | Select release archives by requested client version/tag | **Deferred; excluded from net diff** | Mandatory client-assets gate lacks release fixtures, install-path proof and runtime-load evidence. |
| `8af3aa4` | NPC trade quantity with equipped imbued items | **Retained with local lifecycle fix** | Corrects double subtraction; local follow-up stops tracker on terminate/game end. Interactive legacy/modern trade validation remains follow-up. |
| `caba9ce` | Pause/resume Stats collection | **Retained** | Useful diagnostics primitive; `g_stats.pause/resume` catalogued. |
| `350e506` | Rendering/preload ordering | **Deferred; excluded from net diff** | Upstream implementation imports `client/game.h` into framework core and reverses dependency direction. Reimplement through `ApplicationDrawEvents`. |
| `225ce4d` | Animator-driven always-animated outfit/mount phase | **Retained** | Compiled evidence exists; exact assets/runtime behavior remains unproven. |
| `89e7898` | NPC trade positioning/chat overlap | **Retained** | Low protocol risk; visual resolution checks remain follow-up. |
| `cee2851` | Restore `lastManualWalk` | **Retained** | Restores optional bot/manual-input coordination; public surface catalogued. |
| `dedc737` | `--user-dir` override | **Retained** | Useful portable/test isolation; public CLI surface catalogued. |
| `a7d1b39` | Correct pre-780 use-with source stack position | **Retained** | Version-specific correctness; 7.x fixture/runtime proof remains follow-up. |
| `fec1cca` | `TargetBot.Danger()` | **Retained** | Optional bot API; returns zero while disabled; catalogued. |
| `cd4441e` | Stop unknown-opcode busy loop/OOM | **Retained, high priority** | Defensive bounded parser behavior; existing InputMessage contracts reused. |
| `de0af30` | Fixed 1 GiB browser heap for Chrome 149 | **Retained with historical browser evidence only** | Original synchronization head passed browser build; current final policy does not claim browser compatibility. |
| `a28fc1c` | Ground-border use-with target | **Retained** | Interaction proof remains follow-up. |
| `e0092f0` | Browser Lua/UIGraph/shader compatibility | **Retained with historical browser evidence only** | Lua syntax is current; non-Windows runtime compatibility is not claimed. |
| `76a3260` | Reward-wall collect-source byte | **Deferred; excluded from net diff** | Missing exact Canary producer, shared `OTS-*`, compatibility matrix and paired tests. |
| `a4cbf1a` | Cocoa mouse delta | **Retained with historical macOS build evidence only** | Current Windows gate does not claim macOS runtime compatibility. |

### 6.3 Local safety adaptations and review findings

- NPC imbuement tracking now stops during module termination and game-session end, not only on NPC-close events.
- `g_stats.pause/resume`, `--user-dir`, `TargetBot.Danger()` and `lastManualWalk` are recorded in `MODULE_CATALOG.md`.
- A mistaken full-file replacement from a ranged fetch temporarily truncated `game_npctrader.lua`; the exact blob was restored immediately before the intended two cleanup lines were reapplied. Final net diff contains no lost content.
- A redundant unknown-opcode integration test was removed after existing unit contracts were found.
- GitHub's PR file endpoint lists nine current-main files due explicit base-update merge commits; authoritative `main...head` comparison contains 29 net files. Both views were reviewed.

### 6.4 Final synchronization acceptance gate

PR #26 may squash-merge only after:

1. authoritative current-base changed-file and full-diff review;
2. exact-head fast workflow/static checks;
3. exact-head Lua syntax checks;
4. exact-head Windows CMake Release;
5. exact-head Windows CMake Tests and CTest;
6. exact-head Windows Solution Debug, OpenGL and DirectX;
7. `CI / Required` success;
8. confirmation that Oteryn Identity/security boundaries are unchanged;
9. mergeability and no unresolved comments/review threads;
10. squash message recording upstream head, exact 16-commit reviewed range and three excluded effects.

Historical Linux/macOS/browser/Docker success on the original synchronization head remains supporting evidence only. Current repository policy does not compile or claim compatibility for dormant platforms.

## 7. `solchanel/otclient-15` selective review

### 7.1 Repository-level assessment

The repository diverges heavily and combines protocol changes, UI changes, workflow changes and binary image assets. It must not be bulk-merged.

An MIT repository file does not prove redistribution rights for third-party game graphics. Taskboard/CipSoft-like binary assets remain prohibited without separate provenance; Oteryn Taskboard must use original or independently licensed assets.

### 7.2 Protocol 15.22 clues

| Candidate | Assessment | Disposition |
|---|---|---|
| `0053457` — 15.22 compatibility | Partly superseded; includes no-op weekly parser and broad hard-coded version changes. | Do not cherry-pick; compare individual fields to exact Canary. |
| `c3f3d14` — missing 15.12 changes | Contains a Cyclopedia `levelPercent` double-read/desync risk and inappropriate error logging. | Reject wholesale; reimplement confirmed fields with fixtures. |
| `2744cac` — level-percent fix | Direction is plausible; exact transition version must match Canary/features. | Adapt only with feature-gated tests. |
| `44f8794` — dual compression | Networking-wide framing/proxy/TLS risk. | Defer until a demonstrated requirement and round-trip tests. |
| `3b47bab` — raw world name in `Protocol::send` | May overlap authoritative Oteryn Gateway routing and one-shot login. | Review separately; never replace `world_id` routing. |
| `3f49b19` — store/rewardwall formats | Potentially useful but payload-dependent. | Adapt only under exact cross-repository contract. |

### 7.3 Taskboard

The `b1a3e7e` proof of concept covers bounties, preferred/unwanted monsters, weekly tasks, shop, Soulseals, trackers and modal UI, but it is unsuitable for direct adoption because:

- it is a multi-thousand-line feature mixed with binary assets;
- action IDs, costs, difficulty and rewards are partly hard-coded client-side;
- current client already contains Taskboard protocol names/parsers;
- no exact Canary pair or cross-repository tests are recorded;
- lifecycle, malformed-payload, persistence and economy-authority tests are missing;
- binary asset provenance fails the current gate.

**Required design**

1. Canary remains authoritative for availability, prices, balances, progress, rewards and errors.
2. Reuse existing `GameTaskboard` and `parseTaskBoard*` entry points.
3. Create shared `OTS-*` contract with exact opcodes/subtypes/order/widths/optionals/gates.
4. Add C++ parser fixtures and Lua callback contracts before UI.
5. Build a controller-owned `modules/game_taskboard` module.
6. Use original Oteryn assets with source/license/hash records.
7. Fail closed on unsupported one-sided combinations.
8. Validate exact-version bounty, weekly, shop, preferred slots, Soulseals, trackers and relog flows.

Taskboard remains a separate milestone.

## 8. Upstream issue and PR triage

### 8.1 Repair immediately after synchronization

| Issue | Assessment | Planned action |
|---|---|---|
| #1775 character-list relog | UI path/lifecycle risk confirmed | Absolute module layout resolver, nil guards and repeated Oteryn/legacy recreation tests. |
| #1776 cooldowns after relog | Root cause confirmed | Focused action-bar lifecycle PR with Lua tests and relog scenario. |
| #1753 Wheel conviction indices | Static mismatch deterministic | Named index map and Lua contract test. |
| #1691 Forge expired callbacks | Scheduled-event lifecycle defect | Track/cancel handles or generation-guard callbacks. |
| Existing Global audit defects | Deterministic | Narrow repair PRs, not one broad redesign. |

### 8.2 Protocol and Canary contract queue

| Issue | Required proof |
|---|---|
| #1775 Monk 15.25 opcode/desync | Exact client/server packet, producer handler and Canary commit. |
| #1738 15.24 XP/fragments/portable Forge | Separate U16 percentage, XP, resource-ID and request/response tests. |
| #1743 Forge convergence | Exact 15.11 client/Canary pair and state transitions. |
| #1681 empty VIP list on 10.98 | 10.98 packet fixture and filtering/state test. |
| #1605 creature move/desync reports | Separate real client bug from mismatched assets/custom opcodes; test chargeable mapping 7.80–8.54. |
| #1729 mount crash/graphics | Exact assets, look type, packet and reproducible crash/log. |
| Reward Wall source semantics | Exact producer, consumer, source-byte meaning, rollout matrix and paired tests. |

### 8.3 Core interaction queue

| Issue | Priority | Plan |
|---|---:|---|
| #1562 container move/last-panel drag | P1 | Separate widget drag ownership from item drop zones and add regression. |
| #1437 miniwindow input focus | P1 | Audit keyboard grabbing, focus routing and modal overlays. |
| #1229 hotkey subtype | P1 | Add use/use-with/equip subtype fixtures and correct boundary. |
| #1030 attacked-creature hit ratio | P1 | Review top-thing selection and creature hit testing while walking. |
| #1518 stale use-with indicator | P2 | Continue pointer updates during targeting and clean up on cancel. |
| #1358 Classic LMB+RMB look | P2 | Deterministic mouse-chord state machine tests. |
| #1338 repeated walk keys | P2 | Measure repeat, walk lock and predictive behavior first. |
| #1741 renamed creature battle-list removal | P2 | Reindex/update by creature ID, not stale name. |

### 8.4 Performance/platform queue

| Issue | Plan |
|---|---|
| #1731 slow debug startup | Profile module loading, logs and data parsing. |
| #1601 autostats CPU | Reuse Stats pause/resume, expose explicit policy and measure idle CPU. |
| #1041 updater checksum freeze | Background/incremental hashing with cancellation/progress. |
| #1447 outfit window performance | Profile and virtualize/cache previews. |
| #1435 scaled-text flicker | Inspect rounding, interpolation and cache invalidation. |
| #1011 audio positioning | Add backend-specific positional-audio tests. |
| #1612 HTML modules in archive | Audit archive-backed HTML resource loading. |
| #1694 Android workflow | Validate independently only after platform policy changes. |
| #1489/#1644 encryption crashes | Separate packaging/security milestone; never weaken integrity checks. |

## 9. Security and compatibility invariants

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

## 10. Delivery roadmap

### Phase 0 — synchronize and stabilize the base

- Complete PR #26 exact-head Windows CI and squash merge.
- Record upstream head and 16-commit dispositions as durable synchronization baseline.
- Keep rendering/preload, Reward Wall and archive selection deferred to focused gated tasks.
- Revalidate Oteryn auth/session tests on subsequent affected changes.

**Exit:** reviewed net effects are in `main`, required Windows checks pass, and no Oteryn/security boundary regressed.

### Phase 1 — deterministic lifecycle and option repairs

- Character-list destroy/recreate fix.
- Action-bar cooldown relog restoration.
- Forge event cleanup.
- Wheel conviction index fix.
- Right Bar 3, duplicate ID, expiry event, labels and unsupported controls.
- Backward-compatible setting-key migration.

**Exit:** focused tests exist and login/logout/reload cycles do not leak state.

### Phase 2 — modern protocol 15.24/15.25 compatibility

- Monk login field/order investigation.
- Level-percent width normalization and XP formula.
- Fragment resources and Wheel balances.
- Portable Forge request/response flow.
- Store/Reward Wall under exact contracts.
- VIP 10.98 and chargeable 7.80–8.54 fixtures.

**Exit:** exact linked Canary/client pairs pass parser/output and integration tests.

### Phase 3 — options architecture

- Metadata-driven option registry.
- Basic/advanced filtering.
- Separate General, Action Bar and Custom Hotkey views.
- Seconds in timestamps, PM policy, big cursor, link warning and auto-insert spells.
- Schema-versioned settings/minimap import/export.

**Exit:** every control persists, migrates and changes observable behavior.

### Phase 4 — screenshots and layout

- Reuse existing client-event parser.
- Game-window/full-client capture service.
- Bounded five-second backlog.
- Event trigger policy and screenshot folder workflow.
- Dynamic sidebars and layout-tree persistence/migration.
- Original Oteryn skin/assets.

**Exit:** representative Windows resolution/DPI evidence and tested privacy/storage limits.

### Phase 5 — Taskboard

- Shared Canary/OTClient contract.
- Parser/output fixtures and gates.
- Controller-owned UI and original assets.
- Bounty, weekly, preferred slots, shop, Soulseals and tracker integration.
- Relog, malformed data, unsupported server and economy-authority tests.

**Exit:** exact-version cross-repository E2E passes and one-sided combinations fail closed.

### Phase 6 — interaction and measured performance

- Containers, focus, target hit testing, classic controls and cursor state.
- Startup, autostats, updater hashing, outfit performance and text flicker.
- Separate browser/macOS/Android acceptance only after explicit platform policy changes.

**Exit:** each change has reproduction evidence and measurable benefit.

## 11. Test and acceptance matrix

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

Final acceptance for a user-facing option requires:

1. correct visibility/basic-advanced classification;
2. persistence and migration;
3. observable backing behavior;
4. interaction with related settings;
5. unsupported-combination handling;
6. representative Windows resolution/DPI evidence;
7. exact server pairing when payload-dependent.

## 12. Immediate execution order

1. Finish PR #26 exact-head Windows CI and squash merge.
2. Finalize and merge audit PR #25, then archive its task.
3. Deliver character-list recreation repair.
4. Deliver action-bar cooldown lifecycle repair.
5. Deliver Wheel/Forge/options deterministic repairs.
6. Open focused tasks for asset archive selection and architecture-safe renderer preload only with their required evidence.
7. Start 15.24/15.25 contracts with exact Canary pairs.
8. Begin Taskboard only after protocol and asset provenance gates close.

This order removes known data-loss, desynchronization and lifecycle risks before adding broad UI or protocol surface.
