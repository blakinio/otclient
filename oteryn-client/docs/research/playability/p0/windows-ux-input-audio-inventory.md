# P0 Windows UX, Input, Audio and Accessibility Inventory

Status cut: `main@21f0725f0beb46775951dd17f2587c67ebcdee12`  
Lane: `OTC2-20260801-playability-p0-ux` / PR #143  
Implementation/library selection authorized: **false**

## 1. Purpose

Define the user-visible Windows product workflows, platform interaction requirements, semantic input model, audio behavior and accessibility evidence needed for M2-M6.

This inventory translates current Rust architecture, W4/W5 evidence and representative legacy behavior into observable requirements. It does not make OTUI/Lua compatibility normative, select a UI/audio dependency or copy proprietary presentation.

## 2. Current evidence boundary

### Proven foundations

- `apps/client` owns one Windows main-thread `winit 0.30.13` application handler and deterministic shell state.
- Shell tests cover lifecycle state, focus, resize/zero-size state, scale-factor, keyboard, modifiers, mouse, cursor, wheel, IME event boundaries and idempotent close.
- `oteryn-renderer` owns one exact DX12 `wgpu` surface/device/queue boundary and deterministic CPU-side lifecycle with a constant clear/present adapter.
- Hosted Windows CI proves exact APIs compile and deterministic tests pass.
- Current technical-login composition can expose public phase text through the window title and uses explicit environment configuration.
- Normative architecture requires retained UI hierarchy/focus/accessibility, reactive view models, semantic actions, normalized input and an explicit audio voice/device owner.

### Unproven or absent

- no native Rust UI core, layout engine, text shaping, widget tree or accessibility tree;
- no product login/selection presentation;
- no game viewport/HUD/panels, docking or layout persistence;
- no semantic input contexts, bindings or conflict resolution;
- no mouse picking, drag/drop or capture contract;
- no audio backend, mixer, categories, positional/UI sound or device recovery;
- no interactive Windows launch, physical input, IME, clipboard, multi-monitor DPI or screen-reader evidence;
- no named dependency/library decision;
- no world/game domain/view-model/action contracts to consume.

Hosted CI cannot upgrade these states to compatibility claims.

## 3. Product workflow inventory

### 3.1 Launch and process shell

Start state:

- client installed or developer build selected;
- one clean process and profile;
- no stale modal or active input capture;
- exact Windows build/session type recorded.

Required behavior:

1. create one visible window without duplicate shell ownership;
2. show deterministic startup progress or a bounded recoverable error;
3. restore only validated window/layout settings within visible monitor bounds;
4. expose version/profile and diagnostics without secrets;
5. allow close from window controls, keyboard and fatal-error action;
6. release input/audio/UI/renderer resources before process exit.

Observable acceptance:

- no hidden background process or orphan thread after exit;
- focus, scale and window state match the OS;
- unsupported platform/session combinations fail clearly;
- startup does not block on network, asset conversion or shader preparation in the event callback.

### 3.2 Authentication and recoverable errors

The native UI never collects an Oteryn password.

Required screens/states:

- logged out / sign in;
- browser-opening progress;
- waiting for callback with cancel and safe timeout;
- exchanging/obtaining directory;
- stable safe error with one recommended action;
- account ready / character selection;
- credential/admission progress;
- recoverable failure requiring fresh entry, configuration check or reauthentication.

Acceptance:

- UI consumes safe view models only, not raw HTTP/server text;
- callback/ticket/session secret values never appear in widgets, clipboard, accessibility text, screenshots or diagnostics;
- cancel/close remains responsive during every asynchronous stage;
- stale completion cannot update a replacement screen/session;
- no silent legacy-password fallback.

### 3.3 World and character selection

Required capability:

- render authoritative worlds/characters from the merged directory contract;
- expose compatibility/availability safely;
- select only valid world-character relationships;
- explain absent/unsupported gameplay channel state rather than inventing routing;
- keyboard, mouse and accessibility navigation;
- stable loading, empty and recoverable error states;
- no credential or endpoint display.

M1 may use a bounded technical selection surface. Product polish remains M4, but the selection action contract should be stable before feature UI depends on it.

### 3.4 Game viewport and HUD

M2 minimum:

- one viewport consuming an immutable render snapshot;
- camera/floor context and local-character visibility;
- bounded HUD for connection/session state and minimum player feedback;
- semantic movement/camera actions;
- safe disconnect/logout action;
- no authoritative state inside widgets.

M3/M4 expansion:

- status bars, skills/stats/conditions/cooldowns;
- battle list and targeting feedback;
- inventory/equipment/container panels;
- chat console/channels/NPC/private messages;
- action bars, hotkeys and context menus;
- minimap and map controls;
- settings, social and feature-specific panels;
- notifications, confirmations and modal error flows.

Every feature UI reads its own bounded view model and emits semantic actions. It does not access sockets, packet types, renderer internals or another feature's private state.

### 3.5 Panels, docking and persistence

Required product behavior:

- deterministic panel identity and docking zones;
- bounded resizable/minimum sizes;
- no panel can permanently hide the game viewport or mandatory exit/recovery action;
- layout persistence is typed, schema-versioned, size-bounded and recoverable;
- invalid/off-screen layouts reset safely;
- DPI/monitor changes preserve useful physical size and visibility;
- feature-unavailable panels are hidden/disabled with reason, never inert;
- reset-layout and safe-mode paths exist.

### 3.6 Modal, notification and error policy

- one explicit focus owner;
- modal stack depth is bounded;
- critical action text is stable and localized;
- raw backend text remains diagnostic-only;
- notifications have severity, lifetime and accessibility announcement policy;
- destructive/server-authoritative actions require confirmation only where product evidence supports it;
- repeated errors coalesce instead of flooding the UI;
- network loss and recovery do not create competing modal loops.

## 4. Windows platform acceptance matrix

| Area | Required scenarios | Current state |
|---|---|---|
| visible launch/present | launch, close, repeated launch on named desktop session | BLOCKED — no accepted interactive observation |
| resize/minimize/restore | physical window-manager interaction including zero-size transitions | BLOCKED |
| DPI | 100/125/150/200%, move between differently scaled monitors, taskbar/work-area changes | BLOCKED |
| focus | alt-tab, click activation, modal focus, focus loss while keys/buttons held | BLOCKED |
| keyboard | layout changes, modifiers, repeat, navigation, hotkey conflicts | event boundary only |
| text/IME | enable, composition, candidate UI, commit, cancel, focus switch, Unicode input | event boundary only |
| mouse | cursor mapping, high DPI, wheel precision, buttons, capture/release | event boundary only |
| clipboard | copy/paste allowed text, invalid/large input, privacy restrictions | ABSENT |
| drag/drop | internal item/panel drag, OS file drop policy, cancellation and capture loss | ABSENT |
| accessibility | names/roles/states, focus order, keyboard-only flow, scaling and screen-reader candidate | ABSENT |
| multi-monitor | placement, unplug/replug, primary change, negative coordinates | BLOCKED |
| session type | native desktop, VM, remote session policy | UNKNOWN |
| shutdown | close, logoff/shutdown policy, active async work, no orphan process | deterministic app close only |

Interactive evidence records exact OS edition/build, session type, display layout/scales, physical input/IME configuration, build SHA, actions and observed results.

## 5. Input requirements

### 5.1 Pipeline

```text
OS event
-> normalized physical state
-> deterministic ordered input event
-> active context stack
-> binding resolution/conflict policy
-> semantic action
-> application/domain command or UI action
```

Features must not inspect `winit` events directly.

### 5.2 Physical state owner

The input core owns:

- keyboard keys by physical/logical representation where required;
- modifiers;
- mouse position/buttons/wheel;
- focus and capture state;
- text/IME composition separately from gameplay keys;
- optional future gamepad state;
- monotonic event order and generation;
- clearing held/transient state on focus loss, session replacement and close.

It does not own game commands, widgets or feature policy.

### 5.3 Contexts

Initial contexts:

- `Global` — safe application actions such as close/help where allowed;
- `LoginSelection` — navigation and sign-in/selection actions;
- `Gameplay` — movement, camera, targeting and action bars;
- `ChatText` — text entry; suppress conflicting gameplay bindings;
- `Modal` — modal-owned actions; blocks lower contexts as defined;
- `DragCapture` — bounded pointer capture during an internal drag;
- `BindingCapture` — records a candidate binding without triggering it;
- `AccessibilityNavigation` — alternative navigation/actions where enabled.

Context push/pop is deterministic and generation-bound. A destroyed widget/session cannot retain capture.

### 5.4 Binding contract

A binding contains:

- semantic `ActionId` from the sole input-action producer;
- physical/logical chord or pointer gesture;
- context and priority;
- press/release/repeat behavior;
- optional accessibility alternative;
- platform/layout compatibility metadata.

Required behavior:

- conflicts are detected before commit;
- reserved OS/application chords cannot be captured silently;
- defaults are explicit and migration-tested;
- feature removal/capability changes preserve or explain orphaned bindings;
- import/export excludes secrets and is bounded;
- chat/text input does not leak keystrokes into gameplay actions;
- held movement clears on focus loss, modal takeover or disconnect.

### 5.5 Mouse picking and drag/drop

Viewport picking consumes published render/domain identifiers, not renderer-internal pointers.

Internal drag state records:

- source semantic object/slot;
- session/domain generation;
- pointer/capture generation;
- allowed target/action preview;
- cancellation reason.

On release, the UI emits one semantic action. The server/domain remains authoritative. Focus/capture loss, session replacement, invalid target or modal interruption cancels without duplicating an action.

OS file drop is denied by default and later enabled only for explicitly bounded import/support workflows.

## 6. Audio requirements

### 6.1 Ownership

`audio-core` is the sole producer for:

- `AudioIntent`/category contract;
- logical sound/resource handles;
- voice identity/generation;
- device lifecycle state;
- category/user gains and mute policy;
- stable recoverable errors.

Concrete gameplay/UI features emit intents. They do not open devices or decode files.

### 6.2 Required categories

Candidate categories, finalized by the P1 producer:

- master;
- UI/notifications;
- ambient/environment;
- creature/combat/effects;
- music if selected by product scope;
- voice/other future categories only if supported.

UI sound and positional world sound remain distinct. Category controls and mute state are typed settings with migration.

### 6.3 Real-time rules

The output callback must avoid:

- filesystem/network access;
- unbounded allocation;
- blocking locks or waits;
- logging with arbitrary strings;
- decoding/decompression;
- game-domain mutation.

Decode/stream preparation occurs on bounded workers. Voice count, stream buffers and queues have explicit budgets and overflow/prioritization policy.

### 6.4 Device lifecycle

Required states:

```text
Uninitialized
Opening
Ready(device generation)
Unavailable(recoverable reason)
Replacing
Closing
Closed
```

Required scenarios:

- no output device at startup;
- default device changed;
- active device removed and reattached;
- format/sample-rate negotiation failure;
- callback underrun/overrun observation;
- suspend/resume and process close;
- rapid setting/category changes;
- stale device completion after replacement.

Audio failure must not block the main event loop or corrupt gameplay. Product policy decides whether play continues silently with a visible recoverable warning.

### 6.5 Positional behavior

Positional intents use domain positions/entity handles and a listener/camera snapshot. They do not contain protocol types. Distance, panning, occlusion and priority behavior require deterministic tests and named interactive/audio-device evidence before parity claims.

## 7. Accessibility and localization

Required core capabilities:

- accessible name, role, state, value and action for interactive elements;
- deterministic keyboard focus order and visible focus indicator;
- keyboard-only completion of login, selection, minimum gameplay/logout and settings;
- semantic alternatives for pointer-only actions;
- scalable text/layout without clipped mandatory actions;
- high-contrast/readability decision and color-independent status cues;
- reduced motion/flashing policy where relevant;
- screen-reader announcement policy for modal/errors/notifications/chat;
- localization keys separated from backend/raw server text;
- expansion, pluralization and Unicode/IME tests;
- per-feature review of information density and virtualization.

No accessibility claim is made until a named Windows accessibility API/library strategy and interactive candidate testing are accepted.

## 8. Privacy and security

- secrets never enter widget text, accessibility nodes, clipboard, layout/settings or screenshots;
- private chat and personal data are excluded/redacted from diagnostics/reference images;
- OS file drops and clipboard input are bounded and validated;
- URL launch is direct and never shell-interpolated;
- UI cannot override authoritative routing, inventory, combat or economy state;
- asset/font/audio resources are resolved from approved verified runtime packs;
- unsupported or malformed view-model data fails boundedly;
- developer inspector/support captures require privacy classification and explicit user action.

## 9. Evidence ladder

### Headless/focused

- state/context/binding/action unit tests;
- layout/focus/accessibility-tree primitives;
- view-model/action compile barriers;
- drag/capture cancellation and stale-generation tests;
- audio intent/device state and bounded voice-priority tests;
- typed settings migrations;
- synthetic text/localization expansion;
- no feature dependency in `ui-core`.

### Component

- UI tree/render extraction against original synthetic fixtures;
- input context -> semantic action integration;
- audio intent -> prepared voice/mixer graph without a real device;
- feature panels against fake view models/actions;
- renderer resource/UI pass integration;
- architecture-category and dependency policy.

### Interactive Windows

- named OS/session/display/input/IME/audio/accessibility setup;
- visible scenarios in the platform matrix;
- real device replacement/capture/focus/DPI behavior;
- screenshots/video only as supporting artifacts with structured results;
- no compatibility inference from hosted compile CI.

## 10. Owner decisions and blockers

| Decision | State | Owner/output needed |
|---|---|---|
| native UI technology and Windows accessibility bridge | UNKNOWN | bounded P1/P2 decision with prototype evidence |
| text shaping/font stack | UNKNOWN | UI/text producer plus asset rights evidence from PR #142 |
| audio backend | UNKNOWN | bounded audio-core decision; architecture names `cpal` only as an example |
| final default bindings/action taxonomy | UNKNOWN | input producer plus parity scenarios from PR #141 |
| final feature panel set | UNKNOWN | P0 aggregation from PR #140/#141 evidence |
| Windows support/DPI/IME/accessibility matrix | UNKNOWN | product/UX/release owner after interactive evidence |
| audio resources and rights | UNKNOWN | PR #142 and owner/legal decision |

## 11. P0 boundary

This inventory authorizes no UI/audio dependency, source code, assets, screenshots, product visual design or accessibility compatibility claim.
