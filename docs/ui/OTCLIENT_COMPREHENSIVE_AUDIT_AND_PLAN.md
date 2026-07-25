# OTClient Comprehensive Audit and Delivery Plan

Audit date: 2026-07-25  
Current fork baseline: `blakinio/otclient` `main` at `715ba210e870304f66b5d5496899c6ea3ca9599d`  
Upstream baseline: `opentibiabr/otclient` `main` at `465b7a217e87502bb7f9980bf6e099718d0a9a49`  
Task: `OTC-20260725-comprehensive-options-upstream-audit`

## 1. Purpose

This audit answers five separate questions:

1. Which client systems and Tibia Global-like options exist in the current fork?
2. Which of those systems have executable evidence, which are only present in source, and which contain known defects?
3. Which functionality is missing or requires Canary, Oteryn Platform, protocol, platform or asset work?
4. How should the exact 16 missing `opentibiabr/otclient` commits be synchronized without regressing Oteryn Identity, tests or security fixes?
5. Which work from `solchanel/otclient-15`, upstream issues and upstream pull requests is suitable for selective adoption?

External repositories are read-only sources. All branches, commits and pull requests created by this task are confined to `blakinio/otclient`.

## 2. Evidence levels

| Level | Meaning |
|---|---|
| Runtime-proven | The behavior was exercised in a compiled client or an exact-version integration/rehearsal. |
| CI-proven | Relevant builds/tests passed on the exact commit, but the full interactive behavior was not manually exercised. |
| Source-wired | A visible control or callback and its plausible backing implementation are present. |
| Source-only | Definitions, parser support or dormant code exist, but a complete user flow is not exposed or proven. |
| Partial | Related behavior exists, but semantics, version coverage, lifecycle or UI exposure are incomplete. |
| Broken | A concrete source defect or reproducible issue is known. |
| Missing | No complete equivalent was found. |
| External dependency | Correct behavior requires a matching Canary, Platform, protocol, assets or operating-system contract. |

Presence in source is not equivalent to runtime correctness. Open issues are treated as hypotheses until they are reproduced or a deterministic source defect is confirmed.

## 3. Executive assessment

### 3.1 Current strengths

| Area | Assessment | Evidence / notes |
|---|---|---|
| Oteryn Identity login | Runtime-proven foundation; production rollout still requires current contract revalidation | System-browser Authorization Code + PKCE, short-lived ticket, Gateway login, authoritative world routing and one-shot Game Session handoff are merged. Oteryn mode has no password fallback and does not persist bearer credentials. |
| Security hardening | CI/runtime evidence | Shell-safe external URL launch is merged; credential replay and stale protocol callback protections are present. |
| Test foundation | CI-proven | The merged test foundation provides deterministic C++ unit tests, Lua tests, protocol contracts and bounded loopback integration. |
| Action bars and hotkeys | Strong source-wired foundation, with lifecycle defects | Nine bars, up to 50 slots per bar, drag/drop, item/spell/text/multi-action support, profiles, hotkeys and cooldown rendering exist. |
| Protocol/version architecture | Broad but uneven | Feature flags and version gates cover old and current protocols. Some modern parsers contain unverified assumptions and verbose debug/discard behavior. |
| Modular UI | Strong foundation | Lua/OTUI modules make most GUI changes possible without rewriting the renderer. |
| Asset installer | Security-sensitive but mature | Strict manifest hashes and standard runtime paths exist. The current upstream archive-selection fix is important to prevent downloading an unrelated legacy archive. |

### 3.2 Main gaps

| Area | Current result |
|---|---|
| Tibia Global option parity | Previous screenshot audit: 25 implemented, 7 partial, 24 missing and 2 visibly broken groups. This audit adds further lifecycle and protocol defects. |
| Runtime acceptance | Many source-wired options lack interaction tests at 1080p, 1440p, 4K and ultrawide resolutions. |
| Options architecture | No basic/advanced metadata model; no complete import/export; hotkey sections do not match the Global split. |
| Screenshot subsystem | Modern client-event parsing exists, but the user-facing screenshot configuration, backlog, trigger policy and folder workflow are incomplete. |
| Dynamic layout | Fixed side panels exist; arbitrary sidebars, complete layout-tree persistence and migration are missing. |
| Taskboard | Protocol identifiers and parser hooks already exist, but no complete shipped `game_taskboard` UI module is present. |
| Modern 15.2x protocol | Partial support exists, but Monk login, 15.24 level/forge/resource behavior and exact Canary compatibility need focused contract tests. |
| Lifecycle safety | Action-bar cooldown listeners, Forge timers and character-list UI recreation have concrete lifecycle risks. |
| Performance | Startup, autostats, updater checksum work, outfit rendering and text scaling have unresolved upstream reports. |

## 4. Current options and GUI status

The detailed option-by-option matrix remains in `docs/ui/TIBIA_GLOBAL_OPTIONS_PARITY.md`. The most important conclusions are summarized below.

### 4.1 Controls and hotkeys

**Present/source-wired**

- Regular, Classic and Left Smart-Click mouse modes.
- Loot mouse modes.
- General keybind table with primary and secondary keys.
- Chat On/Off presets, add/copy/rename/remove and search.
- Per-action-bar button hotkeys.
- Item, spell, text, target, equip and use action types.

**Partial or broken**

- `hotkeyDelay` is not proven equivalent to Global keyboard delay.
- `moveStack` is not the same as a selectable complete-stack modifier.
- Action Bar Hotkeys and Custom Hotkeys are not exposed as complete separate pages.
- Custom action creation code exists, but the `New Action` control is hidden and disabled.
- Upstream issue #1229 reports item subtype being passed incorrectly by hotkeys; it requires a current-source reproduction and protocol/item fixture.
- Upstream issues #1338 and #1358 report walking/classic-control interaction defects.

**Missing**

- OS-default/custom keyboard-delay contract.
- Rotation modifier selector.
- Always-face-movement behavior.
- Basic/advanced option filtering.

### 4.2 Interface and status

**Present/source-wired**

- Native and animated cursors.
- Mouse target highlight.
- Creature names, health, player mana, Harmony and text/HUD scaling controls.
- Loot value frames/corners.
- Inventory/container expiry display.
- Special-condition HUD/bar ordering controls.

**Partial or broken**

- `Show Cooldown Bar` is represented by a differently named option that controls the full cooldown window.
- Inventory expiry refresh checks the wrong event before cancellation.
- `Show Expiry On Unused Items` is exposed but disabled.
- Customisable/status-bar checkboxes have no usable IDs or option keys.
- Upstream issue #1518 reports a stale use-with cursor indicator.
- Upstream issue #1435 reports flicker in scaled text.

**Missing**

- Big cursor option.
- Link-copy/open warning policy.
- Complete configurable Global-like status bars around the game viewport.
- Dynamic sidebar manager and complete layout persistence.

### 4.3 Console

**Present/source-wired**

- Info, event, own-status and others-status filters.
- Timestamps and level display.
- Channel tabs and core private-message handling.

**Missing or partial**

- Explicit automatic private-message tab policy.
- Separate seconds-in-timestamps option.
- Complete Global-like channel persistence/unread behavior acceptance tests.

### 4.4 Action bars

**Present/source-wired**

- Three bottom, three left and three right bars.
- Assigned hotkey, object count, spell parameters, graphical cooldown, cooldown seconds and tooltips.
- Per-profile persistence and lock groups.
- Clear controls for individual bars.

**Concrete defects**

- Right Bar 3 reset calls bar 7 instead of bar 9.
- `clearRightBar3` is duplicated as another widget ID.
- Active spell/rune cooldown packets can arrive before action-bar listeners are connected.
- Cooldown caches are reset or ignored at unsafe lifecycle points.
- `setupActionBar` can stop an overlay after `updateButton` restored it.
- Protocol cooldown state is discarded when both visual cooldown options are disabled.
- Simple runes do not consistently use the same restoration path as text spells and multi-actions.

**Missing**

- Auto-insert new spells policy.
- Dedicated Global-like Action Bar Hotkeys list.

### 4.5 Miscellaneous, screenshots and help

**Present/source-only**

- `Allow auto chase override` and a feature-profile selector.
- Core screenshot/client-event parsing for old screenshot events and the 15.21+ variable client-event system.
- Language selection and cache clearing.

**Missing user flow**

- Only-game-window capture option.
- Five-second screenshot backlog.
- Auto-screenshot master switch and event matrix.
- Open screenshot folder.
- Export all options, export minimap and import options/minimap.
- Purchase/container-operation confirmation policies.
- Secure Global-like quick login/session persistence.
- Inspect-me and nearby-corpse quick-loot policy.

Screenshot event parsing should be reused; a second protocol parser must not be created. The missing work is primarily capture service, settings, event policy, storage, privacy and platform integration.

## 5. Deterministic defects confirmed in current source

| Priority | Defect | Status | Required fix |
|---|---|---|---|
| P0 | Unknown-opcode recovery can repeatedly revisit unread bytes and exhaust memory | Fixed by upstream commit `cd4441e`; included in synchronization candidate | Retain `skipBytes(unreadSize)` behavior and add malformed-packet regression coverage. |
| P0 | Client asset installer may select an unrelated legacy ZIP from a release | Fixed by upstream commit `465b7a2`; included in synchronization candidate | Retain version/tag scoring, macOS exclusion and strict codeload fallback; test release metadata fixtures. |
| P1 | Character list cannot reliably recreate its OTUI after destroy/relogin | Confirmed source risk and upstream issue #1775 | Resolve OTUI paths against `/modules/client_entergame/`, fail cleanly on missing layout and test destroy/create cycles, including Oteryn layout selection. |
| P1 | Action-bar cooldown state lost after relog | Confirmed by current lifecycle and upstream issue #1776 | Connect protocol-state listeners for module lifetime, scope caches per session, retain state independently of visual options and restore the greatest remaining individual/group cooldown. |
| P1 | Wheel conviction summary reads shifted slots | Deterministic upstream issue #1753 | Replace numeric magic indices with named indices and add a Lua contract test. |
| P1 | Forge scheduled callbacks can outlive controller state | Deterministic lifecycle risk in upstream issue #1691 | Store/cancel event handles or guard callbacks by controller generation before clearing callback tables. |
| P1 | Right Bar 3 clears the wrong bar and duplicates an ID | Confirmed source defect | Map to bar 9, assign unique IDs and add a Lua/OTUI contract test. |
| P1 | Inventory expiry cancellation checks the wrong event | Confirmed source defect | Correct event ownership and add rapid-toggle coverage. |
| P2 | Two walk-delay controls display the wrong setup label | Confirmed source defect | Correct labels and verify slider/value bindings. |
| P2 | Disabled unused-item expiry control and dead status-bar controls | Confirmed incomplete exposure | Implement real behavior and option keys, or hide unsupported controls. |
| P2 | `showExpiryInInvetory` misspelling | Maintainability/data-migration risk | Introduce corrected key with one-time backward-compatible migration. |

## 6. Exact 16-commit upstream synchronization

Comparison result:

- merge base: `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`;
- `opentibiabr/otclient:main` is exactly 16 commits ahead;
- `blakinio/otclient:main` is 21 commits ahead with Oteryn, tests, security and governance work;
- therefore a blind branch replacement is forbidden.

A local merge candidate exists in `blakinio/otclient` PR #26. It contains current `main` plus the exact upstream head and does not modify Oteryn enter-game/authentication, auth tests, session guards or shell-safe URL files.

| Commit | Change | Disposition | Reason / acceptance |
|---|---|---|---|
| `465b7a2` | Select release archives by requested client version/tag | Accept | Security/correctness fix; prevents 15.25 from selecting `client-11.zip`. Preserve strict hashes and standard paths. |
| `8af3aa4` | NPC trade quantity with equipped imbued items | Accept with runtime test | Corrects double subtraction; validate legacy and modern trade modes plus tracker lifecycle. |
| `caba9ce` | Pause/resume Stats collection | Accept | Useful lifecycle/performance primitive; later add an explicit configuration policy. |
| `350e506` | Rendering/preload ordering | Accept pending platform builds | Prevents renderer-dependent preload behavior; requires Linux/Windows/macOS/browser compilation. |
| `225ce4d` | Animator-driven always-animated outfit/mount phase | Accept with asset tests | Likely addresses a class of animated mount issues; does not by itself prove all mount reports. |
| `89e7898` | NPC trade positioning/chat overlap | Accept as presentation fix | Low protocol risk; visually validate representative resolutions. |
| `cee2851` | Restore `lastManualWalk` | Accept | Restores expected bot/manual-input coordination without touching auth. |
| `dedc737` | `--user-dir` override | Accept | Useful portable/test isolation feature; validate path handling and no credential leakage. |
| `a7d1b39` | Correct pre-780 use-with source stack position | Accept with old-protocol fixture | Version-specific correctness; add 7.x packet/item test. |
| `fec1cca` | `TargetBot.Danger()` | Accept | Optional bot API addition; ensure default behavior remains zero/off. |
| `cd4441e` | Stop unknown-opcode busy loop/OOM | Accept, high priority | Defensive parser fix; add bounded malformed-message test. |
| `de0af30` | Fixed 1 GiB browser heap for Chrome 149 | Accept only with browser build | Platform-specific workaround; monitor memory footprint and browser compatibility. |
| `a28fc1c` | Ground-border use-with target | Accept with interaction test | Improves target selection; verify classic/regular controls. |
| `e0092f0` | Browser Lua/UIGraph/shader compatibility | Accept with browser tests | Removes unsupported Lua `goto`, exposes UIGraph and uses constant shader loop bounds. |
| `76a3260` | Reward-wall collect-source byte | Accept only against Canary contract | Client/Canary packet semantics must be tested together; source byte is inverted relative to the open-window byte. |
| `a4cbf1a` | Cocoa mouse delta | Accept with macOS build/input smoke | Isolated platform fix. |

### Synchronization acceptance gate

The candidate may merge only after:

1. exact changed-file and full-diff review;
2. Linux release and test builds;
3. Windows CMake tests and solution variants;
4. macOS build;
5. browser bundle build;
6. Docker build;
7. Lua syntax, Lua CTest, C++ unit, protocol and integration tests;
8. confirmation that Oteryn Identity files and security boundaries are unchanged;
9. PR mergeability and no unresolved review threads.

Android does not need to build for these exact paths unless the final diff or workflow marks it affected; desktop/browser success must not be generalized to Android.

## 7. `solchanel/otclient-15` selective review

### 7.1 Repository-level assessment

The repository is 33 commits ahead and 65 commits behind the current fork from an older merge base. Its complete diff combines protocol changes, UI changes, workflow changes and many binary image assets. It must not be bulk-merged.

The source repository carries an MIT file, but that does not establish redistribution rights for third-party game graphics. The fork policy therefore prohibits copying Taskboard/CipSoft-like binary assets without separate provenance. Any Oteryn Taskboard must use original or independently licensed assets.

### 7.2 Protocol 15.22 commits

| Candidate | Assessment | Disposition |
|---|---|---|
| `0053457` — “added 15.22 compatibility” | Partly superseded by current code. Current fork already has NPC chat opcode 28, Taskboard opcode 91, `GameTaskboard` feature gates and 15.2x parser hooks. The commit also contains a no-op weekly parser and broad hard-coded version changes. | Do not cherry-pick. Diff individual fields against current Canary and add only missing, tested gates. |
| `c3f3d14` — missing 15.12 changes | Contains useful clues, but its Cyclopedia stats patch reads `levelPercent` before and again inside a version branch, creating a double-read/desync risk. It also logs NPC data at error severity. | Reject wholesale. Reimplement only confirmed field widths/order with parser fixtures. |
| `2744cac` — level-percent fix | Direction is correct: U16 percentage must be normalized before callbacks. Exact transition version must match Canary/current feature flags. | Adapt with feature-gated tests; do not copy a hard-coded threshold blindly. |
| `44f8794` — dual compression | Networking-wide behavior with proxy/TLS/framing risk. | Defer until a real requirement and protocol-level round-trip tests exist. |
| `3b47bab` — raw world name through `Protocol::send` | May help proxy mode, but can overlap current Oteryn Gateway/world routing and one-shot login. | Review separately against Oteryn login tests; never replace authoritative `world_id` routing. |
| `3f49b19` — store/rewardwall formats | Potentially useful for modern protocol, but must be compared with upstream `76a3260` and Canary handlers. | Adapt only under an exact cross-repository contract. |

### 7.3 Taskboard

The Taskboard commit `b1a3e7e` provides a large proof of concept covering bounty tasks, preferred/unwanted monsters, weekly tasks, a hunting-point shop, Soulseals, trackers and modal UI.

It is not ready for direct adoption because:

- it is a multi-thousand-line feature mixed with binary assets;
- action IDs, costs, difficulty tables and reward values are partly hard-coded client-side;
- many values are explicitly required to match server enums;
- current client already contains Taskboard protocol names/parsers, so blindly adding a second model would duplicate contracts;
- no matching exact Canary revision or cross-repository test pair is recorded;
- no focused lifecycle, malformed-payload, persistence, HTML/UI or economy-authority tests accompany the feature;
- binary asset provenance is not acceptable under the current repository gate.

**Recommended Taskboard design**

1. Treat Canary as authoritative for task availability, prices, balances, progress, rewards and error codes.
2. Reuse the existing `GameTaskboard` feature and `parseTaskBoard*` entry points after verifying their payloads.
3. Define a shared `OTS-*` contract with exact opcodes, subtypes, order, widths, optionals and version gates.
4. Add C++ parser fixtures and Lua callback contracts before UI integration.
5. Build `modules/game_taskboard` as a controller-owned module with deterministic event cleanup.
6. Use original Oteryn artwork and record source/license/hash.
7. Add feature-off behavior and fail closed on unsupported one-sided client/server combinations.
8. Validate bounty, weekly, shop, preferred slots, Soulseals, trackers, logout/relogin and malformed data against one exact Canary commit.

Taskboard should be a separate milestone, not part of the 16-commit upstream synchronization.

## 8. Upstream issue and pull-request triage

At audit time there were no open upstream pull requests returned by the live search. The recent merged upstream pull requests correspond to the 16-commit synchronization range. Open issues contain a mixture of deterministic source defects, incomplete reports, server/asset mismatches and old-protocol regressions.

### 8.1 Repair immediately after upstream synchronization

| Issue | Assessment | Planned action |
|---|---|---|
| #1776 cooldowns after relog | Root cause confirmed in current source | Focused action-bar lifecycle PR with Lua tests and normal relog integration scenario. |
| #1775 character-list relog | UI path/lifecycle risk confirmed | Absolute module-path resolver, safe recreation, nil guards and Oteryn/legacy layout tests. |
| #1753 Wheel conviction indices | Static index mismatch is deterministic | Named index map and Lua contract test. |
| #1691 Forge expired callbacks | Classic scheduled-event lifecycle defect | Track/cancel all Forge event handles or generation-guard callbacks. |
| Existing Global audit defects | Deterministic | One narrow “repair existing options” PR. |

### 8.2 Protocol and Canary contract queue

| Issue | Assessment | Required proof |
|---|---|---|
| #1775 Monk 15.25 opcode/desync | Separate from the login-server vocation label. Unhandled `0x01` after `0xC1` indicates a field/order or feature-gate mismatch. | Capture exact client/server packet fixture, identify producer handler and validate parser against exact Canary commit. |
| #1738 15.24 XP/fragments/portable Forge | Detailed and likely actionable; combines four independent defects. | Separate tests for U16 level percent, XP formula, fragment resource IDs and portable Forge request/response sequence. |
| #1743 Forge convergence | High-impact modern feature report | Exact 15.11 Canary/client pair and Forge state transitions. |
| #1681 empty VIP list on 10.98 | Reproduced by reporter but not on 8.60 | 10.98 packet fixture plus filtering/state test. |
| #1605 creature move desync | Mixed reports; many cases are custom opcode/assets/server mismatches. A concrete 7.80–8.54 chargeable-attribute bug is separately actionable. | Fix/test `ThingAttrChargeable` mapping for 7.80–8.54; do not mask unknown-opcode/server mismatches. |
| #1729 mount crash/graphics | Inconclusive and partly attributed to server bytes/assets; animator upstream fix may help. | Exact assets, look type, Canary packet and reproducible crash/log. |

### 8.3 Core interaction queue

| Issue | Priority | Plan |
|---|---:|---|
| #1562 container item move/last panel drag | P1 | Reproduce both videos, separate widget drag ownership from item drop zones and add interaction regression. |
| #1437 inputs cannot focus in miniwindows | P1 | Audit keyboard grabbing/focus routing and modal overlays. |
| #1229 hotkey subtype | P1 | Add item subtype fixtures for use/use-with/equip and correct call boundary. |
| #1030 poor attacked-creature hit ratio | P1 | Review top-thing selection versus creature hit testing while walking. |
| #1518 stale use-with indicator | P2 | Ensure crosshair/mouse-move updates continue during targeting and cleanup on cancel. |
| #1358 Classic LMB+RMB look | P2 | Build deterministic mouse-chord state machine tests. |
| #1338 repeated walk keys | P2 | Measure key repeat, walk lock and predictive walk behavior before changing timing. |
| #1741 renamed monster battle-list removal | P2 | Reindex/update battle entries by creature ID rather than stale name identity. |

### 8.4 Performance/platform queue

| Issue | Plan |
|---|---|
| #1731 slow debug startup | Profile module loading, debug logging and data parsing; do not optimize from a single extreme timing. |
| #1601 autostats CPU | Reuse upstream Stats pause/resume, then expose a policy/flag and measure idle CPU. |
| #1041 updater checksum freeze | Move hashing off the UI thread or incrementally yield with cancellation/progress. |
| #1447 outfit window performance | Profile outfit widget creation/animation and virtualize or cache previews. |
| #1435 scaled-text flicker | Inspect pixel rounding, camera interpolation and text cache invalidation. |
| #1011 audio source positioning | Add positional-audio unit/runtime test per backend. |
| #1612 HTML modules in `modules.zip` | Audit HTML resource loading through archive-backed resources. |
| #1694 Android build workflow | Document one supported workflow and validate independently; desktop builds are not evidence. |
| #1489/#1644 encryption crashes | Treat as separate packaging/security milestone; never weaken integrity checks. |

### 8.5 Defer or reject without better evidence

- Reports caused by mismatched `.dat`, `.spr`, `items.otb`, custom opcodes or custom server fields are not client bugs until an exact compatible pair reproduces them.
- Feature requests such as compressed assets, extended bot loot policies and HTML/CSS enhancements should not displace correctness/security work.
- Stale labels do not prove an issue is fixed; they only reduce confidence and require fresh reproduction.

## 9. Security and compatibility invariants

Every implementation phase must preserve:

1. Oteryn mode never sends or stores the user's Oteryn password.
2. Oteryn mode never silently falls back to legacy password authentication.
3. OAuth state, callback path, PKCE verifier/challenge and HTTPS endpoint rules remain strict.
4. Game Session credentials remain one-shot and are cleared after the first normal handoff.
5. Auto-reconnect never replays an Oteryn Game Session credential.
6. Gateway `world_id` remains the authoritative Oteryn routing source.
7. External URLs remain argv values, never shell-interpolated commands.
8. Asset hashes and final runtime paths remain strict.
9. Unknown or malformed protocol data fails boundedly; no busy loops, cursor rewind or uncontrolled allocation.
10. New protocol fields are version/feature gated and paired with exact Canary tests.
11. No proprietary CipSoft assets are committed without demonstrated redistribution rights.

## 10. Delivery roadmap

### Phase 0 — synchronize and stabilize the base

- Merge the exact 16 upstream commits only after full current-head CI.
- Add regression coverage for unknown-opcode bounded skip and versioned asset selection.
- Revalidate Oteryn auth/session tests on the merged base.
- Update stale module catalogue references to merged test/auth work.

**Exit:** all selected upstream commits are in `main`, all required builds/tests pass, and no Oteryn/security file regressed.

### Phase 1 — deterministic lifecycle and option repairs

- Character-list destroy/recreate path fix.
- Action-bar cooldown relog restoration.
- Forge scheduled-event cleanup.
- Wheel conviction index fix.
- Right Bar 3, duplicate ID, expiry event, labels, status/unused-expiry controls.
- Backward-compatible setting-key migration.

**Exit:** focused tests exist for every defect and login/logout/reload cycles do not leak events/widgets/callbacks.

### Phase 2 — modern protocol 15.24/15.25 compatibility

- Monk login `0xC1`/following-field investigation.
- Level-percent feature-width normalization and modern XP formula.
- Fragment resource identifiers and Wheel balance display.
- Portable Forge resource requests and stable Fusion-tab data flow.
- Store/rewardwall packet formats.
- VIP 10.98 and chargeable 7.80–8.54 fixtures.

**Exit:** exact linked Canary/client commit pairs pass parser/output tests and real integration scenarios.

### Phase 3 — complete options architecture

- Metadata-driven option registry: category, subgroup, basic/advanced, dependency, tooltip and availability reason.
- Show Advanced Options.
- Separate General, Action Bar and Custom Hotkey views.
- Seconds in timestamps, PM tab policy, big cursor, link warning and auto-insert spells.
- Settings/minimap import/export with schema versioning and validation.

**Exit:** controls persist, restore, migrate and alter observable behavior; unavailable features are disabled with an explanation.

### Phase 4 — screenshot and layout systems

- Reuse existing client-event parser.
- Capture service for game-window/full-client screenshots.
- Bounded five-second backlog with memory/disk safeguards.
- Auto-event trigger policy and screenshot folder workflow.
- Dynamic sidebars, drop preview, complete layout-tree persistence and migration.
- Original Oteryn skin/assets.

**Exit:** 1080p, 1440p, 4K and ultrawide interaction/scaling evidence; privacy and storage limits tested.

### Phase 5 — Taskboard

- Shared Canary/OTClient protocol contract.
- Parser/output fixtures and feature gates.
- Controller-owned UI module and original Oteryn assets.
- Bounty, weekly, preferred slots, shop, Soulseals and tracker integration.
- Logout/relogin, malformed data, unsupported server and economy-authority tests.

**Exit:** exact-version cross-repository E2E passes; one-sided combinations fail closed.

### Phase 6 — interaction and performance backlog

- Containers, miniwindow focus, target hit testing, classic controls and cursor state.
- Startup profiling, autostats policy, updater checksum background work, outfit performance and text flicker.
- Browser/macOS/Android/platform-specific acceptance.

**Exit:** each issue has reproduction evidence, measurable improvement and no regression in adjacent controls.

## 11. Test and acceptance matrix

| Change type | Required minimum |
|---|---|
| Lua/module lifecycle | Lua syntax, focused Lua test, repeated init/terminate and login/logout interaction. |
| OTUI/layout | Parse/load test, representative resolutions, focus/drag/drop interaction. |
| Protocol parser/output | InputMessage/OutputMessage fixture, malformed/truncated packet, version/feature gates, exact Canary pair. |
| C++ framework | Linux compile/tests plus affected Windows/macOS/browser build. |
| Authentication | Existing PKCE/callback/Gateway/session tests and production-like rehearsal where contract changes. |
| Assets | License/source/hash/path review, strict manifest tests and runtime loading. |
| Performance | Before/after measurement, cancellation/lifecycle behavior and no UI-thread stalls. |

Final acceptance for any user-facing option requires:

1. correct visibility/basic-advanced classification;
2. persistence and migration;
3. observable backing behavior;
4. interaction with related settings;
5. unsupported-combination handling;
6. resolution/DPI evidence;
7. exact server pairing when payload-dependent.

## 12. Immediate execution order

1. Finish CI and merge review for the 16-commit synchronization candidate.
2. Deliver the character-list recreate fix.
3. Deliver the action-bar cooldown lifecycle fix.
4. Deliver Wheel/Forge/options deterministic repairs.
5. Start the 15.24/15.25 cross-repository protocol milestone.
6. Only then begin the Taskboard implementation milestone.

This order removes known data-loss/desync/lifecycle risks before adding large new UI and protocol surface.