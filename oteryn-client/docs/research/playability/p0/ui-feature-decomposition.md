# P0 UI, Input and Audio Feature Decomposition

Status cut: `main@21f0725f0beb46775951dd17f2587c67ebcdee12`  
Lane: `OTC2-20260801-playability-p0-ux` / PR #143  
Implementation authorized: **false**

## 1. Objective

Decompose native presentation, input and audio into sole public contract producers and independent feature consumers without allowing `ui-core`, renderer, platform or audio runtime to absorb gameplay feature policy.

This is a planning graph. Package names are candidates until the P0 aggregation barrier accepts the smallest P1 producer set.

## 2. Non-negotiable boundaries

- OS events are normalized before features consume them.
- UI reads bounded view models and emits semantic actions.
- UI never emits wire messages or owns authoritative game state.
- Renderer consumes immutable/generation-stable render commands/snapshots and does not own widgets or feature policy.
- Audio features emit typed intents; only the audio runtime owns devices/mixing/voices.
- `ui-core` provides primitives only and cannot depend on concrete auth, inventory, chat, combat, market or settings features.
- every public action, view-model, resource and owner handle has one producer;
- async/platform results carry generations and cannot mutate replacement sessions/windows/devices;
- frame-critical UI/render/audio callbacks perform no blocking I/O, decoding or unbounded allocation;
- legacy OTUI/Lua behavior is evidence, not an API or runtime dependency.

## 3. Candidate contract spine

### 3.1 `ui-core` producer

Owns presentation-neutral primitives:

- `WidgetId`/tree generations and parent-child ownership;
- retained tree lifecycle;
- layout primitives: flex, grid, constraints/anchors where accepted;
- measured/arranged geometry and dirty propagation;
- clipping, scrolling and virtualization primitives;
- focus tree, focus traversal and modal/capture arbitration;
- accessible node primitives and semantic properties;
- typed style/theme tokens without feature policy;
- bounded text node contract consuming shaped-text handles;
- UI event dispatch and closed errors;
- render-command extraction contract independent of concrete renderer resources.

Must not own:

- character/inventory/chat/combat/market models;
- server capability rules;
- concrete product screens;
- game/domain commands;
- OS event types;
- GPU device/resource ownership;
- settings persistence or asset loading.

Focused acceptance:

- deterministic layout and dirty propagation;
- stable focus traversal/modal stack/capture release;
- clipping/scrolling/virtualization bounds;
- stale widget generation rejection;
- accessibility tree consistency;
- no dependency on feature/protocol/app categories.

### 3.2 View-model and semantic UI action producer

Candidate ownership may live in a narrow `ui-application-contracts` package or an accepted game-domain/application contract slice.

Owns:

- versioned/bounded common application view models;
- stable semantic UI actions such as sign-in, select character, retry, logout, open/close panel and confirm/cancel;
- action result/rejection model;
- feature capability/unavailable reason representation;
- common notification/modal descriptors containing safe classified text only;
- generation/session correlation.

Feature-specific models/actions belong to their feature producer, but must implement or compose through the common envelope rather than replace it.

### 3.3 `input-core` producer

Owns:

- normalized physical key/button/pointer/wheel/gamepad state;
- focus/capture/generation cleanup;
- deterministic event order;
- context stack;
- binding/chord/gesture representation;
- conflict and reserved-binding result;
- semantic `InputActionId`/dispatch envelope or an explicit bridge to the common action producer;
- rebinding candidate capture;
- typed settings representation for bindings.

Must not know sockets, Canary, inventory state or widget implementation details.

### 3.4 Text/platform-input producer

A bounded producer/adapter owns:

- text input versus physical key separation;
- IME composition/commit/cancel;
- clipboard abstraction with bounded validated strings;
- cursor/capture operations;
- DPI/monitor/window coordinate conversions;
- platform accessibility bridge once selected.

The abstraction may be implemented inside the platform/UI integration package, but its public contract has one owner and is independently testable.

### 3.5 `audio-core` producer

Owns:

- `AudioIntent`, category and priority contracts;
- logical resource/sound handles;
- listener/position model independent of protocol;
- voice IDs/generations and bounded voice policy;
- category/user gain and mute state;
- device lifecycle state and recoverable errors;
- prepared-buffer/stream contract;
- observable underrun/overflow diagnostics.

Must not own gameplay event interpretation, asset importing, filesystem/network I/O in callback, widget state or feature settings screens.

### 3.6 Text/resource producer dependencies

Separate producers are required for:

- approved logical UI/font/audio resource handles from the asset runtime;
- text shaping/glyph runs and localization resolution;
- renderer-side UI/glyph resource realization.

`ui-core` consumes logical handles/shaped runs. It does not parse source fonts, build atlases or read loose files.

## 4. Candidate package dependency graph

```text
foundation / diagnostics
        |
        +--> ui-core primitives
        +--> input-core contracts
        +--> audio-core contracts
        +--> localization/text contracts
        +--> asset-runtime logical handles

common application view-model/action contracts
        |
        +--> auth-selection UI feature
        +--> gameplay HUD feature
        +--> inventory/container UI feature
        +--> chat/social UI feature
        +--> combat/battle-list feature
        +--> action-bar/hotkey feature
        +--> minimap feature
        +--> settings/layout feature
        `--> later exact-profile features

input-core + ui-core + feature actions
        -> UI/input application integration

audio-core + feature audio intents + asset handles
        -> audio runtime/device adapter

ui render commands + shaped text + resource handles
        -> renderer UI/text passes

merged UI/input/audio services
        -> app-runtime/apps-client composition (serialized owner)
```

Renderer, protocol and feature crates may not define substitute UI/action/input/audio public types.

## 5. Producer merge order

Recommended sequence after P0 aggregation:

1. common gameplay/application identifiers and action/event envelope accepted by the game-contract producer;
2. `input-core` physical state/context/binding/action bridge;
3. `ui-core` retained tree/layout/focus/accessibility/render extraction primitives;
4. common UI view-model/action/notification envelope if not already in the game/application contract;
5. asset-runtime logical handles plus text/localization resource contract;
6. `audio-core` intent/category/device/voice contract;
7. renderer resource/UI/text integration contract;
8. one auth/selection feature and one minimum gameplay HUD/input feature against synthetic models;
9. serialized `apps/client` composition and interactive Windows acceptance;
10. independent feature UI packages after producer contracts merge.

P0 evidence may justify splitting or reordering, but consumers cannot merge compatibility claims before their sole producer.

## 6. Feature package decomposition

### 6.1 Authentication and selection UI

Consumes:

- safe account/entry public phases and actions;
- world/character directory view model;
- common error/action model;
- UI/input/text/accessibility primitives.

Owns:

- sign-in, browser-wait, callback/ticket/directory progress presentation;
- world/character selection;
- recoverable error and configuration guidance;
- account/selection-specific localization and accessibility;
- no password field for Oteryn profile.

Does not own OAuth, Gateway DTOs, credentials, routes or session worker lifecycle.

### 6.2 Gameplay viewport/HUD

Consumes render snapshot, player/HUD view models and semantic commands.

Owns:

- viewport composition and camera controls;
- status bars/basic player feedback;
- connection/session/recovery indication;
- HUD panel placement and visibility;
- minimum logout/disconnect action;
- no authoritative player/world state.

M2 producer should remain intentionally narrow.

### 6.3 Inventory/equipment/containers

Separate feature state/domain producer remains authoritative. UI owns:

- panels/slots/container windows;
- item selection/hover/drag previews;
- semantic look/use/move/equip actions;
- capability/unavailable and server rejection presentation;
- virtualized/large-container behavior;
- accessibility alternatives to drag/drop.

It does not mutate item ownership locally as final truth.

### 6.4 Chat/NPC/social

Owns:

- channel/tab/private/NPC presentation;
- bounded virtualized history view;
- text entry, IME and send action;
- safe links/clipboard policy;
- unread/notification/accessibility behavior;
- privacy-aware diagnostics and retention policy.

Raw packet/server text bypass into widgets is forbidden; text is validated/classified through the feature/domain contract.

### 6.5 Combat/battle list/targeting

Owns:

- battle-list presentation and sorting policy from accepted view models;
- attack/follow/stop semantic actions;
- target/follow state indication;
- cooldown/condition/combat feedback;
- mouse picking bridge using domain/render handles;
- keyboard/accessibility alternatives.

Server/domain state remains authoritative.

### 6.6 Action bar/hotkeys

Owns:

- action-slot configuration and presentation;
- binding to semantic capability actions;
- cooldown/availability display;
- conflict UI using input-core results;
- typed settings/migration;
- no packet or spell/item execution policy outside feature/domain commands.

### 6.7 Minimap

Owns:

- minimap view model/rendering controls;
- pan/zoom/floor/marker semantic actions;
- bounded persistence/import/export when later authorized;
- accessibility alternatives and status;
- no arbitrary map file or server routing ownership.

### 6.8 Settings/layout

Owns:

- typed settings screens and apply/reset actions;
- layout persistence/reset/safe mode;
- input binding UI;
- audio category/device UI;
- graphics/display options only after renderer/platform contracts expose safe capabilities;
- schema migration and scope (device/account/character/local profile).

Secrets are never regular settings.

### 6.9 Later feature panels

Trade, depot, NPC commerce, market, prey, imbuements, bestiary/charms, cyclopedia, wheel/gem systems and other exact-version panels are authorized only when PR #140 proves server support and PR #141 classifies user workflows as release-required or deferred.

Each is an independent feature package after shared contracts stabilize.

## 7. Safe parallelism after producers merge

Potentially independent:

- input-core and audio-core contract implementation;
- UI-core primitives and asset-runtime logical handle implementation;
- auth-selection UI and synthetic gameplay HUD after common UI/action contracts;
- chat and inventory feature UI after UI-core/common actions/domain producers;
- audio device backend and feature audio-intent adapters;
- accessibility/platform bridge research and renderer UI pass work with stable contracts.

Must serialize:

- definitions of common actions/view models;
- `ui-core` public primitives;
- input action/context schema;
- audio intent/device schema;
- text/glyph/resource handle contracts;
- root manifests/lockfile/category rules;
- `apps/client` final composition;
- shared layout/settings schemas.

## 8. Synthetic harnesses

### UI-core harness

- deterministic viewport/scale/time inputs;
- original synthetic trees/styles/text metrics;
- geometry, clipping, focus and accessibility snapshots;
- virtualization with bounded large lists;
- stale-generation and destruction/capture tests;
- no real GPU/device required for contract tests.

### Feature UI harness

- fake bounded view models and semantic action recorder;
- capability enabled/disabled states;
- loading/empty/error/recovery paths;
- localization expansion and keyboard-only flow;
- no server or protocol dependency.

### Input harness

- ordered normalized physical/text events;
- contexts, focus/capture, held-key cleanup;
- binding conflicts/reserved chords/repeat;
- DPI coordinate conversion fixtures;
- semantic action output recorder.

### Audio harness

- fake device lifecycle and deterministic clock;
- bounded prepared buffers/intents;
- category gain/mute/priority/voice stealing;
- stale-device generation and replacement;
- callback contract check for forbidden blocking/allocation operations where measurable;
- no copyrighted audio assets.

### Interactive harness

A later named Windows session records real window/input/IME/accessibility/audio behavior. It is separate from headless unit/component tests and from gameplay staging E2E.

## 9. Validation for implementation packages

Every package requires:

- focused deterministic tests for its state/contracts;
- exact architecture category/edge evidence;
- external input bounds and stable errors;
- teardown and stale-generation coverage;
- component composition against synthetic fixtures;
- exact Windows workspace CI and supply-chain checks;
- interactive Windows evidence where the claim is platform/device behavior;
- performance distributions for hot-path layout/render/audio changes;
- capability matrix update and separate lifecycle archive.

## 10. Product/architecture decisions deferred

P0 does not decide:

- UI framework/library implementation strategy;
- Windows accessibility API bridge;
- shaping/font/localization libraries;
- audio backend;
- exact visual theme/layout;
- default bindings;
- supported input/gamepad matrix;
- exact feature set for parity;
- final performance/resource budgets.

These become bounded producer decisions after evidence from all P0 lanes is aggregated.

## 11. Recommended smallest P1 candidates

Subject to the P0 barrier, the UX lane recommends no broad “implement UI” task. The smallest likely producers are:

1. normalized input/action context contract;
2. retained UI primitive/focus/accessibility contract with synthetic harness;
3. common application view-model/semantic UI action envelope, coordinated with game-domain contracts;
4. audio intent/category/device lifecycle contract;
5. text/localization/resource-handle decision after asset evidence.

Feature screens remain consumers and start only after the relevant producer merges.
