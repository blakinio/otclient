# P0 Functional Parity Scenario Catalogue

Status cut: `main@9c03a448457b1715818e094fdfdeade4a1450434`  
Lane: `OTC2-20260801-playability-p0-legacy` / PR #141  
Exact release-required scope selected: **no**

## 1. Purpose

Provide reusable user-observable scenarios for product classification, protocol/domain/UI decomposition and future automated/interactive E2E. Each scenario states start state, actions, observable result, recovery/negative behavior, milestone and evidence dependencies.

Legacy behavior is evidence for the expected user outcome. Implementation structure, visual design and proprietary content are excluded.

## 2. Scenario contract

Every accepted scenario later records:

```text
scenario ID and revision
release-required / later / deferred / owner decision
exact client build
exact producer/profile/build
approved asset pack/source revision
Windows/environment/hardware where interactive
start state and fixtures
player actions
expected domain events/commands
user-visible observable result
negative/recovery variants
privacy-safe evidence artifacts
pass/fail and known limitations
```

A scenario cannot become `PARITY_PROVEN` until exact producer support, automated checks and required interactive runtime evidence agree.

## 3. Milestone M1 scenarios

### `M1-AUTH-01` — native browser authentication

Start:

- clean logged-out client;
- approved controlled Identity/Gateway environment;
- disposable account;
- no active callback/listener/session.

Actions:

1. choose sign in;
2. system browser opens;
3. user completes authorization;
4. browser returns through dynamic loopback;
5. client obtains directory.

Observables:

- client never requests the Oteryn password;
- one browser transaction and one accepted callback;
- cancellable progress and stable phase/error text;
- worlds/characters appear only from authoritative directory;
- no secrets in UI/clipboard/accessibility/logs.

Negative variants:

- wrong state/path/peer;
- duplicate callback;
- timeout/cancel;
- TLS/DNS/HTTP failure;
- stale completion after a replacement attempt.

Dependencies: current Rust auth contracts, PR #144 controlled evidence plan.

### `M1-SELECT-01` — valid character/world selection

Start: authoritative directory loaded.

Actions: inspect entries, select a character/world and continue.

Observables:

- invalid relationships unavailable with reason;
- selected identity is explicit;
- selection emits one semantic entry request;
- no physical route is invented by UI.

Negative variants: unavailable world, incompatible client/profile, removed character, stale directory.

Dependencies: exact Platform/Gateway contract and future native selection UI.

### `M1-ENTRY-01` — one-shot Canary admission

Start: selected character/world, fresh credential and exact Current profile.

Actions: connect and enter.

Observables:

- credential handed off exactly once;
- ordered admission accepted by server and typed `SessionEntered` reached;
- no map/gameplay claim;
- clean disconnect and worker/socket teardown.

Negative variants: consumed/expired/wrong-character/wrong-profile credential, refusal/timeout/uncertain post-write failure, replay rejection.

Dependencies: exact Canary cut from PR #140, PR #144 staging plan.

### `M1-RECOVERY-01` — failed entry returns safely

Start: directory/selection available; controlled admission failure.

Actions: enter, observe failure, choose recommended action.

Observables:

- safe error code/action, no raw secret/backend text;
- pre-handoff failures may retry according to contract;
- post-handoff uncertainty requires fresh credential/auth action;
- stale session state destroyed.

## 4. Milestone M2 minimum visible world scenarios

### `M2-WORLD-01` — first stable visible world

Start: M1 admission proven; approved map fixture/source pack.

Actions: enter the selected character.

Observables:

- map bootstrap decoded into bounded domain events;
- one simulation owner publishes a stable snapshot;
- floor/tiles/items/local character/basic creatures/effects render from approved resources;
- named loading/error state ends in a complete frame;
- no loose untrusted runtime source read.

Negative variants: malformed/truncated/unsupported bootstrap; missing/incompatible asset; stale generation; decode/resource budget failure.

Dependencies: PR #140 map evidence, PR #142 pack/runtime decision, shared game/snapshot contracts.

### `M2-MOVE-01` — keyboard movement and reconciliation

Start: visible stable world and focused gameplay context.

Actions: press/release movement keys; optionally turn.

Observables:

- physical input becomes semantic movement action;
- validated command sent through domain/protocol boundary;
- server update changes authoritative position;
- camera/minimap/viewport follow consistently;
- held state clears on focus loss/disconnect/modal.

Negative variants: blocked tile/server rejection, stale key/session, latency/reconciliation, teleport.

### `M2-MOUSE-01` — viewport selection/camera action

Start: visible world with a selectable visible object/creature.

Actions: move/click pointer or use an accepted context action.

Observables:

- DPI-correct coordinate maps to a published domain/render handle;
- UI emits a semantic action, never wire bytes;
- stale/removed object is rejected safely;
- keyboard/accessibility alternative exists for mandatory action.

### `M2-EXIT-01` — logout/disconnect from visible world

Start: stable visible session.

Actions: normal logout or controlled server disconnect.

Observables:

- input/actions stop targeting the old session;
- domain/render/UI/audio session resources are released;
- client returns to selection/logged-out state per contract;
- no credential reuse or orphan worker/socket/window.

## 5. Milestone M3 core gameplay scenarios

### `M3-CREATURE-01` — creature lifecycle

Start: visible world with controlled creature fixtures.

Actions: creature enters, moves, changes health/condition and leaves/dies.

Observables:

- viewport and battle representation correlate;
- health/condition/effects are bounded and timely;
- removal clears stale target/follow/picking handles;
- unsupported fields are absent/unknown, not fabricated.

### `M3-COMBAT-01` — attack/follow/stop loop

Start: valid local character and target.

Actions: select target, attack or follow, observe feedback, stop/change target.

Observables:

- one semantic command per accepted action;
- server-authoritative target/state;
- battle list/viewport/HUD/cooldowns correlate;
- stale/removed targets are not actionable;
- focus/modal/chat input does not leak combat commands.

Negative variants: target unavailable/out of range/unsupported, server rejection, disconnect/death.

### `M3-ITEM-01` — look and use item

Start: visible item in world/inventory/container.

Actions: look, use or use-with according to capability.

Observables:

- typed source/target identity;
- safe server response/error;
- no local authoritative item mutation;
- stale/session replacement cancels;
- keyboard/accessibility alternative for context action.

### `M3-ITEM-02` — move/equip/unequip item

Start: inventory/container/equipment slots available.

Actions: drag/drop or alternative move action.

Observables:

- preview/capture is presentation-only;
- one semantic move command;
- authoritative accepted/rejected result reconciles UI;
- count/capacity/slot restrictions are explicit;
- no duplicate move after timeout/capture loss.

### `M3-CONTAINER-01` — container lifecycle

Start: an accessible container item or server-opened container.

Actions: open, navigate page/nesting where supported, move/use item, close.

Observables:

- stable container identity/revision;
- virtualized/bounded contents;
- closure/removal/session end invalidates stale views/actions;
- no feature UI private-state mutation by another feature.

### `M3-CHAT-01` — local/channel/private messaging

Start: accepted channel list and text context.

Actions: switch channel, enter Unicode/IME text, send, receive local/channel/private messages.

Observables:

- message type/channel/source/time classification;
- gameplay bindings suppressed during text entry;
- bounded history and unread/highlight behavior;
- privacy-safe diagnostics;
- channel close/unavailable/rate/rejection response.

### `M3-NPC-01` — NPC conversation

Start: supported nearby NPC and accepted protocol capability.

Actions: begin conversation, send text/choice, receive response, close/leave.

Observables:

- NPC messages distinct from private player messages;
- state resets on distance/session/NPC removal;
- no arbitrary raw markup/link execution;
- later commerce actions remain server-authoritative.

### `M3-PLAYER-01` — stats, skills and conditions

Start: active session with controlled player-state updates.

Actions: receive updates through normal gameplay.

Observables:

- values/unknown/unavailable are distinguished;
- cooldown/condition timing is deterministic;
- HUD/skills panels and accessibility text agree;
- malformed/unsupported fields fail safely.

### `M3-DEATH-01` — death and return path

Start: controlled player death.

Actions: observe death, choose supported return/relog action.

Observables:

- gameplay actions disabled appropriately;
- death/economy facts are server-authoritative;
- stale targets/drag/chat/session state cleaned;
- fresh session credential policy preserved.

### `M3-HOTKEY-01` — action binding and execution

Start: available semantic action and binding settings.

Actions: bind, resolve conflict, trigger, observe cooldown/result.

Observables:

- context/priority/repeat behavior explicit;
- reserved/conflicting chord handled before commit;
- feature/capability unavailable state explained;
- no direct socket action from input/UI.

### `M3-RELOG-01` — relog without full process restart

Start: active game session and valid account session where supported.

Actions: logout, select another character/world/channel, enter again.

Observables:

- old session resources destroyed;
- new generation and fresh credential;
- account session reused only according to accepted lifetime;
- no cross-session map/UI/target/chat/input state leak.

## 6. Milestone M4 daily-product scenarios

### `M4-LOGIN-UX-01` — polished login/selection recovery

Covers clean profile, loading/empty/error states, cancel/back/retry/authenticate-again/update actions, keyboard-only and accessibility navigation, high-DPI layout and secret-safe presentation.

### `M4-LAYOUT-01` — panel docking/layout persistence

Actions: open/close/dock/resize panels, change DPI/monitor, restart, corrupt settings and reset.

Observables:

- typed bounded schema/migration;
- mandatory UI remains visible;
- off-screen/invalid layout recovers;
- feature capability changes do not create inert panels.

### `M4-MINIMAP-01` — minimap daily use

Actions: follow position, pan/zoom/floor/reset, marker/navigation if included, relog/restart.

Observables:

- accepted domain position/floor;
- bounded persistence;
- stale session data cleared;
- inaccessible/unknown map areas explicit;
- no untrusted arbitrary file import.

### `M4-SOCIAL-01` — VIP/party/guild/channel workflows

Exact subscenarios depend on PR #140. Each requires authoritative membership/state, notifications, privacy, unavailable/recovery and accessibility behavior.

### `M4-SETTINGS-01` — typed settings/migrations

Actions: change graphics/UI/input/audio/accessibility settings, apply/restart/import/reset/migrate.

Observables:

- correct scope;
- safe apply/rollback;
- secret exclusion;
- bounded import/export;
- unsupported value recovery;
- no hidden dependence on legacy keys.

### `M4-AUDIO-01` — audio categories/device recovery

Actions: adjust category gains/mute, remove/change default device, continue play, close.

Observables:

- no event-loop stall;
- explicit recoverable silent/device state;
- bounded voices/queues;
- important information also visual/accessibility-visible;
- no source/decode I/O in real-time callback.

### `M4-WINDOW-01` — Windows desktop matrix

Actions: resize/minimize/restore, move across DPI monitors, focus/alt-tab, IME, clipboard, physical input, device/surface recovery.

Observables follow PR #143/#144 named interactive evidence requirements.

### `M4-INSTALL-01` — install/update/repair/rollback

Start: clean/previous/corrupt/interrupted states.

Actions: install, launch, update, interrupt, repair, rollback, uninstall.

Observables:

- authenticated exact artifacts;
- atomic activation and known-good rollback;
- no partial content activation;
- provenance/notices and privacy-safe support result.

### `M4-SOAK-01` — representative multi-hour play

Mix movement/combat/items/containers/chat/panels/audio/relog/recovery.

Observables: bounded frame/memory/resource/queue behavior, no deadlock/protocol drift/orphan state, named hardware/build/scene evidence.

## 7. Milestone M5 exact-profile parity scenario families

Every family is conditional on exact PR #140 support and product classification:

| Family | Minimum scenario shape |
|---|---|
| trade | invite -> inspect offers -> change -> accept/cancel/reject -> cleanup |
| depot/inbox/stash | open -> inspect/move -> limits/rejection -> close/relog |
| NPC commerce | browse -> quantity/price -> buy/sell/reject -> balance/state update |
| market | search/filter -> inspect -> create/cancel/accept -> fees/history/error |
| quests | log/state update -> objective/result -> persistence/relog |
| prey/tasks/hunting | configure/select -> server update -> progress/reward/error |
| imbuements/forge/upgrades | inspect inputs/cost/chance -> confirm -> authoritative result/recovery |
| bestiary/charms/cyclopedia | browse/search/unlock/select -> authoritative state/error |
| wheel/gems/vocation systems | inspect/allocate/confirm/reset -> authoritative result/version gates |
| store/tournament/other | explicit owner decision, privacy/economy and server-support evidence |

For each accepted family:

- one contract owner;
- exact protocol/domain/UI separation;
- positive/negative automated tests;
- controlled staging scenario;
- localization/accessibility/recovery;
- no undocumented legacy dependency.

## 8. Cross-cutting negative scenarios

### Input/data safety

- malformed/truncated/trailing/duplicate/oversized protocol or asset input;
- unsupported capability/version/profile;
- stale session/entity/item/container/resource generation;
- invalid text/Unicode/markup/link/clipboard/file drop;
- bounds/overflow/allocation/decode failure.

### Lifecycle

- focus/capture loss during movement/drag/modal;
- window close during auth/connect/world load;
- disconnect during command/asset decode/UI action;
- device/audio replacement and stale completion;
- repeated login/logout/relog and process restart;
- server restart invalidation.

### Privacy/security

- no credentials/password/tickets/session keys in UI/logs/artifacts;
- private chat/personal data excluded from diagnostics/replay unless explicitly redacted/approved;
- no proprietary asset/capture in Git;
- no official-service automation or anti-cheat bypass.

### Recovery

Every terminal failure maps to one safe action such as retry, choose another target, return to selection, update, repair, authenticate again or exit. No uncontrolled panic, hidden infinite retry or permissive fallback.

## 9. Evidence classes by scenario

- **Unit/focused:** state, parser, action, layout, binding, resource and error invariants.
- **Component:** protocol/domain/UI/resource composition against original synthetic fixtures.
- **Replay:** normalized sanitized deterministic events/commands or approved exact wire fixtures.
- **Interactive Windows:** user-visible UI/input/audio/device/DPI/accessibility outcomes.
- **Controlled staging:** exact client/producer/profile/account/server correlation.
- **Performance/soak:** named scene/build/hardware distributions and resource/lifecycle evidence.
- **Release:** install/update/signing/rollback/support/privacy manifest.

Compilation or a screenshot alone is never sufficient for a runtime/parity scenario.

## 10. Product classification inputs

The P0 aggregation barrier must label each scenario/family:

- `RELEASE_REQUIRED` with target milestone;
- `LATER` with dependency/owner;
- `DEFERRED` by explicit product decision;
- `OWNER_DECISION_NEEDED`;
- `BLOCKED` by exact producer/legal/deployment evidence.

M5 cannot pass while a release-required scenario remains unsupported, unknown or blocked.

## 11. P0 boundary

This catalogue authorizes no implementation, protocol constant, UI design, asset, server call, account use or final parity scope.
