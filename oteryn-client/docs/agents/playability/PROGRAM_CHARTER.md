# Oteryn Rust Client Full-Playability Programme

Status: planning contract; implementation is not authorized by this document alone  
Programme lane: `otclient-v2` / `greenfield-rust`  
Initial platform: Windows desktop  
Server target: project-owned Oteryn Platform, Gateway and Canary compatibility

## 1. Outcome

Deliver an original Rust game client that a player can use as the primary Oteryn client from installation through authentication, character selection, gameplay and safe shutdown, with functional capability parity to the original Tibia client for the features that the exact supported Oteryn/Canary release exposes.

Parity is measured by user capability and observable behaviour. It does **not** mean:

- connecting to official Tibia services;
- cloning proprietary code, branding, assets or exact visual presentation;
- depending on the legacy C++/Lua/OTUI runtime;
- bypassing anti-cheat, authentication or server authority;
- claiming support for a feature the exact server/profile does not expose.

The legacy client and official client package may be used only as read-only behavioural evidence under the repository's legal and security rules.

## 2. Durable source of truth

In descending authority:

1. live Git, active task checkpoints, PR ownership and exact CI;
2. normative architecture and accepted ADRs;
3. exact producer revisions and sanitized evidence;
4. the living capability matrix in this programme;
5. historical wave documents and chat context.

No agent may infer product completion from a green build alone. Every milestone requires the named runtime, compatibility and user-observable evidence below.

## 3. Evidence vocabulary

Every capability uses one state:

- `PROVEN` — exact automated and/or runtime acceptance required by the capability has passed on a named head/build.
- `PARTIAL` — a bounded foundation exists, but an accepted invariant, user workflow or required compatibility is incomplete.
- `SYNTHETIC_ONLY` — behaviour is proven only against original synthetic fixtures/fakes.
- `UNKNOWN` — evidence is missing or stale; absence is not assumed.
- `BLOCKED` — a named external contract, legal decision, fixture or deployment dependency prevents safe progress.
- `ABSENT` — no owning implementation contract exists.
- `DEFERRED` — intentionally outside the current release milestone.

A capability reaches `PARITY_PROVEN` only when its exact Oteryn/Canary workflow passes the relevant automated, interactive and regression acceptance. Similar behaviour in the legacy client is evidence, not proof.

## 4. Non-negotiable architecture

All workers preserve the normative architecture:

- domain models and commands are independent of Canary/Oteryn packet layouts;
- mutable game state has one logical simulation writer;
- network adapters emit validated bounded domain events and consume typed commands;
- renderer consumes immutable/generation-stable snapshots and never owns authoritative state;
- UI consumes view models and emits semantic actions, never wire messages;
- input is normalized into actions before features consume it;
- asset runtime consumes immutable verified packs, not loose untrusted source files;
- frame-critical work never performs blocking network, filesystem, decode or shader preparation;
- every asynchronous result carries an owner/session generation;
- authentication, protocol, assets, updater and extensions fail closed;
- no greenfield crate depends on legacy `src/**`, `modules/**` or `mods/**`;
- public contracts have one producer and consumers do not create substitutes;
- material architecture changes require an ADR and coordinator decision.

## 5. Milestone ladder

### M0 — Technical entry foundation

Current state: materially completed as a bounded synthetic foundation, with real deployment still unproven. The independent closure audit residual `OTC2-POST-001` was closed by implementation PR #136 and lifecycle archive PR #137.

Required outcome:

- Windows executable, window and renderer initialize;
- native OAuth/PKCE, Gateway and Canary admission boundaries compose;
- fake-service E2E reaches typed `SessionEntered` and shuts down safely;
- architecture policy, source-open integrity and nonblocking shutdown findings are closed;
- the active secret flow and all audited release-required public secret-owner seams are closed within the documented best-effort project-owned-memory boundary.

M0 does not mean gameplay is visible or playable. Docs-only P0 discovery may proceed after lifecycle gates. M1 remains gated by controlled staging, deployment and real credential-bearing runtime evidence rather than by an unresolved package-local secret-owner finding.

### M1 — Controlled real technical login

A controlled project-owned staging environment proves:

- merged secret-owner completion PR #136 and archive PR #137 remain present on the exact validated base;
- exact Identity, Gateway and Canary revisions/configuration are pinned;
- the system browser returns through the dynamic loopback callback on supported Windows;
- TLS, DNS, firewall and issuer mapping are correct;
- one controlled account receives a directory and selects a character;
- Canary accepts exactly one credential and the client reaches the admission boundary;
- disconnect and replay rejection are observed without secret leakage.

M1 may still stop before map decoding.

### M2 — Minimum visible world

The first minimum-playable vertical slice proves:

- post-admission map description is decoded into stable domain events;
- one simulation owner builds a bounded world snapshot;
- verified runtime assets resolve required appearances;
- the renderer shows floors, tiles, items, the local character and basic creatures/effects;
- keyboard/mouse semantic movement and camera actions produce validated game commands;
- server movement/reconciliation updates the visible world;
- logout/disconnect returns to a safe selection or logged-out state;
- exact staging E2E: login -> see world -> move -> logout.

This is the first milestone that may be called **playable**, but it is not parity.

### M3 — Core gameplay loop

A player can perform normal hunting and interaction workflows:

- creature appearance, movement, health, conditions and effects;
- item use, look and movement;
- inventory, equipment and containers including drag/drop;
- chat channels, NPC text and private messaging where supported;
- targeting, attack/follow, battle list and basic combat feedback;
- skills, stats, cooldowns, status bars and death/logout paths;
- action bindings/hotkeys and basic settings;
- audio feedback required for the supported loop;
- reconnect/relog policy with fresh credentials where required.

M3 requires scenario E2E and soak evidence, not only packet/unit tests.

### M4 — Daily-playable product

The Rust client is usable as the regular Oteryn client:

- polished native login, world/character selection and recoverable error UX;
- stable game HUD, panels, docking/layout persistence and high-DPI behaviour;
- minimap, VIP/social, party/guild/channel workflows supported by the server;
- action bars, hotkeys, context menus and accessibility alternatives;
- typed settings and migrations;
- audio device recovery and category controls;
- launcher/install/update/repair/rollback path for controlled releases;
- crash-safe diagnostics, support bundle boundaries and privacy review;
- performance budgets pass on named hardware/scenes;
- multi-hour staging play sessions complete without material leaks, deadlocks or protocol drift.

### M5 — Supported feature parity

For the exact release/profile, the capability matrix contains no `ABSENT`, `UNKNOWN` or `BLOCKED` item classified as release-required.

This includes every supported gameplay/product workflow selected for parity, for example trade, depot, NPC commerce, quests, market, prey, imbuements, bestiary/charms, cyclopedia, wheel/gem systems or other version-specific features only when the exact Oteryn/Canary producer exposes them.

Each feature has:

- a named contract owner;
- protocol/domain/UI separation;
- positive and negative automated tests;
- exact staging scenario acceptance;
- localization/accessibility/error handling where user-visible;
- no undocumented legacy dependency.

### M6 — Production release readiness

Production readiness additionally requires:

- approved asset provenance, redistribution/import policy and signed pack process;
- signed launcher/client artifacts and atomic update rollback;
- installer/uninstaller and supported Windows matrix;
- release-channel and compatibility negotiation;
- security review, fuzzing of external parsers, dependency review and threat-model closure;
- performance, memory, GPU/device-loss, network-loss and long-soak acceptance;
- telemetry/diagnostics privacy decision;
- support, rollback and incident procedures;
- release candidate played through representative end-to-end scenarios.

## 6. Programme phases

The programme advances through bounded waves rather than one permanent mega-task:

1. `P0 Discovery and parity definition` — normalize exact capabilities, workflows, legal/runtime inputs and acceptance.
2. `P1 Contract spine` — sole producers for game events/commands, domain IDs, snapshots/view models/actions and asset runtime boundaries.
3. `P2 Minimum visible world` — map protocol, world state, verified assets, rendering, input and one real vertical slice.
4. `P3 Core gameplay` — movement/combat/items/containers/chat/UI/audio in independent feature packages after the spine stabilizes.
5. `P4 Daily-playable product` — polished UX, settings, reconnect, launcher/update and operational evidence.
6. `P5 Supported parity` — remaining exact-version features, compatibility matrix and complete scenario coverage.
7. `P6 Release hardening` — security, legal, performance, soak, packaging and production rollout.

Later coordinators may rename or regroup waves only when durable evidence shows a safer minimum-task decomposition. They must preserve milestone acceptance.

## 7. Parallelism policy

- One coordinator owns each synchronization wave and does not implement worker packages.
- Discovery waves may use up to five independent workers.
- Implementation waves normally use at most four workers, and fewer when public contracts overlap.
- Only one worker owns each public contract.
- Only one worker holds the root Cargo/lockfile/shared-document integration lease at a time.
- Workers with exclusive paths may progress to `integration_ready` while another lease holder merges, then restack.
- `apps/client/**` final composition has one owner at a time.
- Protocol, domain, renderer and UI work may proceed in parallel only against merged contracts or explicit synthetic contract fixtures.
- A worker never remains active merely to wait for another worker, CI, deployment or owner response.

## 8. Validation ladder

Every implementation package defines:

- **Focused:** changed-function/module tests, parser/property tests, deterministic fixtures or minimal reproduction.
- **Component:** crate/component build and bounded integration suite.
- **Heavy final:** exact Windows workspace, full tests, architecture policy, supply chain, repository CI and task-specific E2E/performance/runtime evidence.

After one heavy failure, isolate the first relevant error cheaply. A session normally performs at most two heavy attempts.

Hot-path claims additionally require named scene, build, hardware and frame-time/memory distribution. Real compatibility claims require named producer revision and controlled runtime evidence.

## 9. Programme completion rule

The programme is complete only when:

- all release-required capability rows are `PARITY_PROVEN` or explicitly `DEFERRED` by an owner-approved product decision;
- M1 through M6 acceptance is recorded on exact builds;
- no active task, unresolved release-required security finding, shared-path lease or unarchived implementation remains;
- the legacy client is no longer required for normal Oteryn play;
- release and rollback procedures are proven.

A coordinator may not declare completion because a large percentage of crates exists, login succeeds, a synthetic demo renders, or CI is green.
