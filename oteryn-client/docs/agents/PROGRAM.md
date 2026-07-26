# Oteryn Rust Client Program

Status: ordered implementation program. Live tasks and dependency state remain authoritative.

## Program rule

Do not start broad implementation from this roadmap alone. Every package requires a bounded task, owned paths, explicit dependencies, a draft PR and workstream-specific acceptance evidence.

## Gate 0 — Foundation audit

Goal: replace assumptions with verified inputs before production crate design is frozen.

Required outputs:

- selected Canary revision/protocol matrix;
- current Oteryn Identity, directory, ticket and routing contract summary;
- feature inventory and minimum playable slice;
- legal asset inventory and exclusions;
- baseline client behavior/performance scenes;
- target Windows hardware tiers;
- protocol and asset fixture plan;
- risk register and unresolved cross-repository decisions;
- recommendation whether any architecture detail needs an ADR amendment.

No production workspace bootstrap before this gate is accepted.

## Gate 1 — Workspace foundation

Packages:

1. Rust toolchain/workspace/lint/dependency policy.
2. Architecture dependency checker.
3. Core typed IDs, clocks, errors and cancellation primitives.
4. Structured tracing and secret-redaction foundation.
5. Deterministic test support and fake time.
6. Minimal Windows application shell with clean startup/shutdown.

Acceptance:

- Windows build and tests on exact head;
- forbidden dependency edges fail CI;
- no legacy runtime dependency;
- no speculative game/protocol implementation.

## Gate 2 — Asset and renderer vertical slice

Packages:

1. normalized asset schemas and synthetic source fixtures;
2. deterministic asset compiler prototype;
3. verified pack reader/runtime;
4. window/swapchain/device lifecycle;
5. sprite instancing and texture strategy benchmark;
6. chunked synthetic map extraction;
7. text/UI primitive rendering;
8. benchmark scenes and diagnostics overlay.

Acceptance:

- synthetic map renders without live server;
- resource/device resize and shutdown are deterministic;
- measured batching/frame-time evidence exists;
- asset corruption/security negatives pass.

## Gate 3 — Domain and simulation vertical slice

Packages:

1. domain identifiers/events/commands;
2. world chunk/entity storage;
3. deterministic simulation scheduler;
4. render snapshot extraction;
5. basic movement/interpolation test model;
6. normalized replay format and runner;
7. session-scoped reset/relog lifecycle tests.

Acceptance:

- replay produces deterministic final domain state;
- renderer consumes snapshots without mutable-domain access;
- repeated synthetic relogs leak no session state.

## Gate 4 — Account and selection flow

Packages:

1. platform URL launch and credential-store abstractions;
2. Oteryn Authorization Code + PKCE transaction;
3. account-session service;
4. world/character/gameplay-channel directory models;
5. enter-game, character and channel selection UI;
6. one-shot game-ticket transaction;
7. typed user-facing error actions.

Acceptance:

- negative OAuth/ticket tests pass;
- no password fallback or secret logging;
- Channel 1/2 selection is explicit;
- stale callbacks and duplicate tickets are rejected.

## Gate 5 — Canary protocol minimum playable slice

Packages follow the exact audit-selected Canary revision:

1. transport/session bootstrap;
2. handshake/login adapter;
3. map/tile decode;
4. entities/appearances;
5. movement and basic actions;
6. player stats;
7. inventory/containers;
8. chat;
9. combat target/basic state;
10. game logout/relog/reconnect behavior.

Acceptance:

- golden/malformed/fuzz fixtures;
- exact Canary producer/consumer pair recorded;
- Windows runtime evidence against the selected environment;
- gameplay-channel relog obtains a fresh ticket and session;
- unsupported pairs fail closed.

## Gate 6 — First-party feature completion

Independent feature workstreams:

- full game interface and docking;
- inventory/equipment/containers;
- chat/social surfaces;
- battle list;
- minimap;
- action bars/hotkeys/cooldowns;
- market/store where contracts exist;
- quests/bestiary/task systems where contracts exist;
- settings and accessibility;
- audio and effects.

Each feature remains server-driven and capability-gated. Do not implement UI based only on desired screenshots when authoritative behavior is unknown.

## Gate 7 — Launcher, updater and distribution

Packages:

1. signed release manifest contract;
2. downloader/staging/cancellation;
3. signature/hash verification;
4. atomic activation and rollback;
5. asset/client compatibility enforcement;
6. clean install/repair/uninstall policy;
7. crash reporting and support bundle redaction;
8. stable/beta channel policy.

Acceptance:

- tamper, interruption, rollback and disk-error tests;
- no unverified execution;
- exact Windows packaging/install evidence.

## Gate 8 — Native Oteryn protocol

This is cross-repository and starts only when the server contract exists.

Packages:

1. native transport/session ADR and contract;
2. schema generation and compatibility policy;
3. `protocol-oteryn` adapter;
4. snapshot/delta/resume behavior;
5. feature capability mapping;
6. differential domain/replay tests against Canary compatibility where meaningful;
7. staged rollout and fallback policy.

The domain, features, renderer and UI should not require architectural changes.

## Gate 9 — Extension platform

Optional and post-playable:

1. versioned extension ABI;
2. capability model;
3. WASM host with memory/fuel quotas;
4. private storage;
5. extension UI registration;
6. signing/provenance/user-consent policy;
7. abuse/security test suite.

Native plugins remain prohibited without a replacement ADR.

## Gate 10 — Production acceptance

Required evidence:

- feature acceptance matrix;
- security threat-model closure;
- exact client/server/asset compatibility matrix;
- minimum/recommended/high-refresh performance matrix;
- long soak and repeated relog/reconnect results;
- clean install/update/rollback;
- accessibility/localization review;
- diagnostics and support workflow;
- migration/rollback plan from the legacy client;
- no unlicensed assets or secrets.

## Parallelism policy

After the foundation gate, agents may work in parallel only on non-overlapping crates/paths with stable interfaces.

Good early parallel lanes:

- platform/application shell;
- asset compiler and synthetic fixtures;
- renderer synthetic slice;
- domain typed IDs/test support;
- audit follow-up contracts.

Bad parallelism:

- two agents defining domain events;
- two adapters editing the same compatibility contract;
- UI feature implementation before its view-model contract;
- renderer and asset format changing the same shared types independently;
- bootstrap crates before the audit gate.

## Stop conditions

Stop and record a blocker for:

- missing exact Canary evidence;
- missing asset redistribution rights;
- unresolved authentication/session contract;
- architecture dependency violation requiring a new ADR;
- secret/proprietary material in proposed fixtures;
- cross-repository atomic change without both sides ready;
- performance claim without reproducible measurement.
