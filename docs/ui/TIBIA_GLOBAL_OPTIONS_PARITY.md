# Tibia Global Options Parity Audit

Audit date: 2026-07-24  
OTClient baseline: `main` at `8f2b6a8878c9cbc243a29c8b2dad7c755ca7a260`  
Task: `OTC-20260724-global-client-options-audit`

## Purpose and limits

This document compares the option pages visible in the supplied Tibia Global screenshots with the current `blakinio/otclient` source. It also checks the corresponding public Tibia documentation.

This is a source audit, not a runtime acceptance test. `Implemented` means that a user-visible control and a plausible backing action were found in source. It does not claim that every option was exercised in a compiled client against every protocol version.

The public Tibia manual explains feature groups, but it does not publish a complete versioned inventory of every current checkbox. The supplied screenshots are therefore the exact comparison baseline for the visible settings.

No CipSoft graphics, fonts, icons or other proprietary assets are included in this audit.

## Sources

### OTClient

- `modules/client_options/options.lua`
- `modules/client_options/options.otui`
- `modules/client_options/data_options.lua`
- `modules/client_options/styles/controls/**`
- `modules/client_options/styles/interface/**`
- `modules/client_options/styles/misc/**`
- `modules/corelib/keybind.lua`
- `modules/game_actionbar/**`
- `modules/game_cooldown/cooldown.lua`

### Official Tibia documentation

- Interface manual: <https://www.tibia.com/gameguides/?section=interface&subtopic=manual>
- Controls manual: <https://www.tibia.com/gameguides/?section=controls&subtopic=manual>
- Starting the client and advanced options: <https://www.tibia.com/gameguides/?section=starting&subtopic=manual>
- Screenshot options: <https://www.tibia.com/support/?entryid=168&subtopic=gethelp>
- Configuration/minimap import and export: <https://www.tibia.com/support/?entryid=110&subtopic=gethelp>
- Redesigned options and hotkey categories: <https://www.tibia.com/news/?id=4505&subtopic=newsarchive>

## Status definitions

| Status | Meaning |
|---|---|
| Implemented | Equivalent visible option and backing behavior were found. |
| Partial | Related behavior exists, but the semantics, exposure or naming do not match Global. |
| Missing | No equivalent exposed option or backing option key was found in the inspected source. |
| Broken | A visible control exists, but source wiring contains a concrete defect or disables it. |
| Dependency | Correct implementation also needs platform, protocol, server or authentication work. |

## Executive result

The 58 screenshot-derived option groups classify as follows:

| Classification | Count |
|---|---:|
| Implemented | 25 |
| Partial | 7 |
| Missing | 24 |
| Broken | 2 |

The client already has strong parity in action bars, console filtering, cursor selection, loot colouring, item expiry display, mouse presets and keybind presets. The largest gaps are advanced/simple option filtering, exact input semantics, the Global hotkey-page split, Misc gameplay controls, screenshot automation, import/export and several newer interface toggles.

## Controls

### General controls

| Global option | Status | Current OTClient evidence | Gap / required action |
|---|---|---|---|
| Mouse Preset | Implemented | `mouseControlMode` exposes Regular, Classic and Left Smart-Click in `options.lua` and `styles/controls/general.otui`. | Align labels and defaults only if exact Global wording is required. |
| Loot: Right / modifier mode | Implemented | `lootControlMode` exposes Right, Shift+Right and Left. | Runtime interaction still needs acceptance testing. |
| Use Default Keyboard Delay | Missing | No corresponding option key or control was found. | Add platform-default mode and define how OS repeat settings are read. |
| Keyboard Delay | Partial | `hotkeyDelay` exists with a 30–250 ms slider, but it is named as a hotkey delay and no evidence establishes equivalence with Global's keyboard repeat/delay setting. | Trace the current consumer, then either rename it or implement a separate keyboard delay contract. |
| To Rotate Your Character Hold: Ctrl / Shift / Alt | Missing | No modifier selector was found. | Add persisted modifier selection and route map input through it. |
| Always turn towards the direction of movement | Missing | No exposed option key was found. | Add movement-facing behavior with deterministic input tests. |
| Press Ctrl to Drag Complete Stacks | Partial | `moveStack` exposes `Move stacks directly`, but there is no selector for the Global modifier behavior. | Verify current semantics and add explicit modifier-based stack dragging. |
| Show Advanced Options | Missing | The options window has no simple/advanced mode and always loads the same panels. | Add option metadata, filtering and persisted simple/advanced mode. |

### Hotkey sections

| Global section | Status | Current OTClient evidence | Gap / required action |
|---|---|---|---|
| General Hotkeys | Implemented | Searchable action table with primary/secondary keys in `styles/controls/keybinds.otui`; actions are registered through `Keybind`. | Runtime conflict and reset tests are still required. |
| Action Bar Hotkeys | Partial | Per-button action-bar hotkey editing and separate hotkey sets exist in `modules/game_actionbar/**`. | Add a dedicated Global-like list/category page instead of requiring per-button editing. |
| Custom Hotkeys | Partial | `Keybind` supports item, spell, text and target actions; custom-hotkey editing code exists. The `New Action` control is hidden and disabled, and no Custom Hotkeys category is exposed. | Restore a supported creation workflow and separate category. |
| Hotkey presets and chat modes | Implemented | Add/copy/rename/remove, auto-switch, Chat On/Off and search are present. | Align layout and terminology only. |

## Interface

| Global option | Status | Current OTClient evidence | Gap / required action |
|---|---|---|---|
| Highlight Mouse Target | Implemented | `enableHighlightMouseTarget` calls `setDrawHighlightTarget`. | None beyond runtime validation. |
| Use Native Mouse Cursor | Implemented | `nativeCursor` switches to the platform cursor. | Validate Windows/Linux/macOS behavior separately. |
| Show Animated Mouse Cursor | Implemented | `showAnimatedCursor` controls map cursor animations and is mutually exclusive with native cursor. | None beyond runtime validation. |
| Show Big Mouse Cursor | Missing | No equivalent option key/control was found. | Add scalable cursor assets or vector/platform cursor sizing without copying proprietary assets. |
| Show Cooldown Bar | Partial | `showSpellGroupCooldowns` actually shows/hides the complete cooldown window in `game_cooldown/cooldown.lua`. | Rename the option to match behavior, or split group-icon visibility from window visibility. |
| Show Link Copy Warning | Missing | No equivalent option was found. | Add a confirmation policy for copied/opened links and define trusted-link behavior. |
| Colourise Loot Value | Implemented | `framesRarity` supports None, Frames and Corners. | Verify all consumers use one value source and colour scale. |
| Show Expiry in Inventory | Partial | Option and inventory reload action exist. Event cancellation checks the container event before removing the inventory event. | Fix the wrong event guard and add rapid-toggle regression coverage. |
| Show Expiry in Containers | Implemented | Option reloads open containers. | Verify protocol/item attributes for each supported version. |
| Show Expiry on Unused Items | Broken | The option key exists, but the OTUI checkbox is explicitly disabled. | Implement the missing item-state distinction or hide the unsupported control. |

## Console

| Global option | Status | Current OTClient evidence | Gap / required action |
|---|---|---|---|
| Show Info Messages | Implemented | `showInfoMessagesInConsole`. | None beyond message-class tests. |
| Show Event Messages | Implemented | `showEventMessagesInConsole`. | None beyond message-class tests. |
| Show Status Messages | Implemented | `showStatusMessagesInConsole`. | None beyond message-class tests. |
| Show Status Messages of Others | Implemented | `showOthersStatusMessagesInConsole`. | None beyond message-class tests. |
| Open New Tabs When Receiving Private Messages | Missing | Existing private-message options control display location, not automatic tab creation. | Add an explicit channel-creation policy. |
| Show Timestamps | Implemented | `showTimestampsInConsole`. | None beyond formatting tests. |
| Show Seconds in Timestamps | Missing | No separate option was found. | Add persisted precision selection and shared timestamp formatter. |
| Show Levels | Implemented | `showLevelsInConsole`. | None beyond formatting tests. |

## Action bars

| Global option group | Status | Current OTClient evidence | Gap / required action |
|---|---|---|---|
| Show Bottom Action Bars: All / 1 / 2 / 3 | Implemented | `actionBarShowBottom1..3`, group enable and three bottom bar instances. | Runtime layout tests at multiple resolutions. |
| Show Left Action Bars: All / 1 / 2 / 3 | Implemented | `actionBarShowLeft1..3` and three left bar instances. | Runtime layout tests at multiple resolutions. |
| Show Right Action Bars: All / 1 / 2 / 3 | Implemented | `actionBarShowRight1..3` and three right bar instances. | Runtime layout tests at multiple resolutions. |
| Show Assigned Hotkey | Implemented | `showAssignedHKButton`. | None beyond rendering tests. |
| Show Amount of Assigned Objects | Implemented | `showHKObjectsBars`. | None beyond item-count updates. |
| Show Spell Parameters | Implemented | `showSpellParameters`. | Verify spell metadata coverage per protocol. |
| Show Graphical Cooldown | Implemented | `graphicalCooldown`. | Verify spell/group/multi-use cooldown paths. |
| Show Cooldown in Seconds | Implemented | `cooldownSecond`. | Verify rounding and final-second transitions. |
| Show Action Button Tooltip | Implemented | `actionTooltip`. | None beyond content tests. |
| Auto-Insert New Spells | Missing | No equivalent option was found. | Define insertion target, duplicate handling and profile behavior. |
| Clear Bottom Action Bars | Implemented | Buttons call `resetAction(1..3)`. | Add confirmation if desired. |
| Clear Left Action Bars | Implemented | Buttons call `resetAction(4..6)`. | Add confirmation if desired. |
| Clear Right Action Bars | Broken | Right Bar 3 calls `resetAction(7)` instead of `resetAction(9)`; `clearRightBar3` is also reused as the ID of the global reset button. | Correct the mapping and assign unique IDs; add focused Lua/OTUI regression coverage. |

The action-bar engine creates nine bars and up to 50 buttons per bar. It supports drag/drop, item/spell/text actions, hotkeys, cooldowns, profiles and multi-action logic. This is one of the strongest parity areas in the current client.

## Miscellaneous

### Gameplay

| Global option | Status | Current OTClient evidence | Gap / dependency |
|---|---|---|---|
| Ask Before Buying Products | Missing | No exposed option found. | Add a client confirmation boundary around Store/product purchases. |
| Ask Before Stowing Container Content | Missing | No exposed option found. | Add confirmation to the stow action. |
| Ask Before Sorting Nested Containers | Missing | No exposed option found. | Add confirmation to nested sorting. |
| Ask Before Moving Contents of Nested Containers | Missing | No exposed option found. | Add confirmation to nested move operations. |
| Stay Logged In for Session | Missing | No Global-style option found. | Authentication/security design required; must not weaken Oteryn token/session handling. |
| Optimise Connection Stability | Missing | `optimizeFps` is graphics/application optimisation, not connection stability. | Define measurable networking behavior before adding a checkbox. |
| Quick Login | Missing | Oteryn Identity login is a separate authentication flow and is not this Global option. | Requires an explicit secure session/resume contract. |
| Use Alternate Font Renderer | Missing | No exposed option was found. | Platform/renderer implementation and font-licensing review required. |

### Loot and inspection

| Global option | Status | Current OTClient evidence | Gap / dependency |
|---|---|---|---|
| Allow All to Inspect Me | Missing | No exposed option found. | Requires Canary/protocol/account-policy support if the server enforces visibility. |
| Auto Chase Off | Partial | `autoChaseOverride` exists, but it controls whether auto chase may be overridden; it is not the same setting. | Define the exact login/combat-state behavior. |
| Quick Loot Nearby Corpses | Missing | No matching option found in the inspected options source. | Likely needs client selection logic plus Canary/protocol support and anti-abuse rules. |

The `Gameplay` and `Screenshots` entries are currently commented out in the options category definition. The visible `Misc.` page contains only `Allow auto chase override` and a generic client feature profile selector.

## Screenshots

| Global option | Status | Current OTClient evidence | Gap / required action |
|---|---|---|---|
| Only Capture Game Window | Missing | No screenshot settings page is loaded. | Add game-map-only and full-client capture targets. |
| Keep Backlog of the Last 5 Seconds | Missing | No capture ring buffer option was found. | Add bounded frame buffering with memory/performance limits. |
| Enable Auto Screenshots | Missing | No auto-screenshot option was found. | Add a screenshot service and persisted master switch. |
| Automatic event triggers | Missing | No trigger matrix was found. | Add event subscriptions for level, skill, achievement, bestiary, treasure, loot, boss, death, PvP, damage, healing, low health and List of Life events as supported. |
| Open Screenshot Folder | Missing | No button/page was found. | Add platform-safe folder creation and opening. |

A manual screenshot hotkey, if present elsewhere in the client, does not provide parity with the Global screenshot subsystem shown in the supplied screenshots.

## Other officially documented parity gaps

These are documented by Tibia but were not all represented as individual checkboxes in the supplied screenshots:

| Capability | Current assessment |
|---|---|
| Arbitrary number of sidebars | Partial. OTClient has fixed left/right and extra panels rather than an arbitrary sidebar manager. |
| Restore opened sidebar windows and sizes | Partial. Modules save some geometry, but the main interface only persists the bottom splitter in the inspected source. A complete layout-tree contract was not found. |
| Export All Options / Export Minimap / Import Options-Minimap | Missing from `styles/misc/help.otui`, which currently offers Wiki, Info, Clear Cache and Change Language. |
| Simple options first, advanced options on demand | Missing. |
| Separate General, Action Bar and Custom Hotkey dialogs | Partial, as described above. |
| Customisable status bars | Broken/incomplete exposure. Two status-bar checkboxes in `styles/interface/HUD.otui` have no IDs, while the inherited handler calls `setOption(self:getId(), ...)`; no matching option keys were found. |

## Concrete source defects found during the audit

| Severity | Defect | Source |
|---|---|---|
| High for affected action | Clear Right Bar 3 resets action bar 7 instead of 9. | `modules/client_options/styles/interface/actionbars.otui` |
| Medium | Duplicate widget ID `clearRightBar3` is used for both the Right Bar 3 clear button and the global reset button. | `modules/client_options/styles/interface/actionbars.otui` |
| Medium | Inventory expiry refresh checks `showExpiryInContainers.event` before removing `showExpiryInInvetory.event`. | `modules/client_options/data_options.lua` |
| Medium | `Show Expiry On Unused Items` is user-visible but disabled. | `modules/client_options/styles/interface/interface.otui` |
| Medium | `Show Customisable Status Bars` and `Show Status Bars` have no IDs and no matching option entries, despite inheriting the generic option handler. | `modules/client_options/styles/interface/HUD.otui` |
| Low | Walk teleport and floor-change controls display `Walk delay after turn` in their setup callbacks. | `modules/client_options/styles/controls/general.otui` |
| Low / maintainability | The key `showExpiryInInvetory` is misspelled consistently. | `data_options.lua` and OTUI consumers |

## Recommended delivery plan

### Phase 0 — repair existing controls

No new product surface:

1. Fix Right Bar 3 reset mapping and duplicate ID.
2. Fix the inventory-expiry event guard.
3. Correct the walk-delay labels.
4. Either wire status-bar controls to real option keys or remove the dead controls.
5. Decide whether unused-item expiry is supported; enable and test it or hide it.
6. Rename `Show spell group cooldowns` to `Show Cooldown Bar` unless separate behavior is intended.

### Phase 1 — complete options architecture

Mostly Lua/OTUI plus focused tests:

1. Introduce option metadata: category, subgroup, basic/advanced visibility, dependency and tooltip.
2. Add `Show Advanced Options` and persist it.
3. Split General, Action Bar and Custom Hotkeys into supported views while reusing the current keybind/action-bar stores.
4. Add seconds in timestamps, private-message tab policy, big cursor, link warning and auto-insert-spell settings.
5. Add Help import/export for settings and minimap with schema/version validation.

### Phase 2 — input semantics

Lua plus framework input changes:

1. OS-default versus custom keyboard delay.
2. Rotation modifier selection.
3. Always face movement direction.
4. Explicit complete-stack drag modifier.
5. Conflict and interaction tests for mouse presets, hotkeys and chat modes.

### Phase 3 — gameplay, authentication and protocol options

Cross-module and potentially cross-repository:

1. Purchase/container confirmation policies.
2. Secure session persistence and quick login aligned with Oteryn Identity; never add password persistence as a shortcut.
3. Defined, measurable connection-stability mode.
4. Inspect-me visibility and nearby-corpse quick loot with Canary contracts where required.
5. Alternate renderer only after platform support and font licensing are clear.

### Phase 4 — screenshot service

Platform and event integration:

1. Manual capture service and output directory.
2. Game-window-only/full-client target selection.
3. Bounded five-second frame backlog.
4. Auto-screenshot trigger registry.
5. Platform-safe `Open Screenshot Folder`.
6. Performance, privacy and disk-space safeguards.

### Phase 5 — Global-like layout behavior

Separate from option checkbox parity:

1. Dynamic sidebar manager.
2. Drag/drop placement preview.
3. Complete layout persistence and versioned migration.
4. Multi-resolution, DPI and ultrawide validation.
5. Original Oteryn artwork rather than copied Global assets.

## Acceptance strategy for future implementation

Each parity option should be accepted only when all applicable layers are proven:

1. The control is visible in the expected basic/advanced mode.
2. The value persists and restores correctly.
3. The backing behavior changes observably.
4. Incompatible protocol/platform combinations fail closed or disable the control with an explanation.
5. Interaction tests cover conflicts with related options.
6. UI is checked at representative 1080p, 1440p, 4K and ultrawide resolutions.
7. Canary-dependent behavior is tested against an exact linked server revision.

## Conclusion

The current OTClient does not yet have full Tibia Global option parity. It has a mature action-bar and keybind foundation and implements roughly half of the screenshot-derived option groups directly. The most efficient path is to repair the concrete defects first, introduce a metadata-driven basic/advanced options architecture, then add input, gameplay/protocol and screenshot features in separate milestones.
