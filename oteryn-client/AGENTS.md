# Oteryn Client Agent Instructions

These instructions apply to every path under `oteryn-client/` and supplement the repository root `AGENTS.md`. The more restrictive rule wins.

## 1. Product direction

- Build a greenfield first-party client in Rust.
- Do not implement a line-by-line port of OTClient.
- Do not preserve C++ globals, Lua/OTUI compatibility or legacy module APIs merely because they exist.
- Canary is the first compatibility adapter. Oteryn is the target ecosystem and future native protocol owner.
- The engine and game domain must remain independent of both Canary and Oteryn wire formats.
- A world channel is a parallel gameplay instance selected at login or relog, not a network stream.
- Channel change happens through relog. Seamless in-game channel migration is out of scope unless a later ADR explicitly changes this.

## 2. Mandatory read order

Before any implementation task:

1. repository root `AGENTS.md`;
2. this file;
3. `docs/architecture/ARCHITECTURE.md`;
4. the architecture document owning the changed area;
5. `docs/agents/PROGRAM.md` and `docs/agents/WORKSTREAMS.md`;
6. all active Rust-client task records and open PRs;
7. the latest relevant audits and ADRs;
8. source, tests and contracts for the exact work package.

Do not rely on chat history as source of truth.

## 3. Audit gate

Production workspace bootstrap is blocked until the foundation audit is accepted.

The audit must establish at least:

- selected Canary revision and exact supported protocol range;
- legally usable asset inputs and prohibited inputs;
- feature inventory and minimum playable slice;
- measurable legacy baseline scenes;
- target Windows hardware tiers and graphics requirements;
- current Oteryn Identity and game-session contracts;
- unresolved cross-repository decisions.

Before the gate closes, agents may add architecture, audit evidence, synthetic fixtures, benchmark definitions and task records. They must not create speculative protocol constants, placeholder production crates or copied legacy assets.

## 4. Legacy client boundary

The repository's existing C++/Lua client is read-only evidence unless a separate legacy task owns it.

The Rust client must not:

- link legacy libraries;
- include files from `src/`;
- execute modules from `modules/` or `mods/`;
- load OTUI/OTML as its production UI format;
- depend on legacy globals or lifecycle semantics;
- copy unverified protocol assumptions;
- copy proprietary or unlicensed assets.

Permitted reuse is limited to independently verified behavior descriptions, legal metadata, synthetic test cases and fixtures whose provenance is documented.

## 5. Work visibility

Every substantial task must:

- use one dedicated branch and worktree;
- create a task record before implementation;
- open a draft PR early;
- declare exact `owned_paths`, crates/features touched, dependencies and blockers;
- update the task after discoveries, failures, decisions, tests and review changes;
- leave one exact next action in the handoff.

Use the root task system for repository-wide discoverability. Rust-client-local templates may add fields but may not replace root governance.

## 6. Dependency rules

Allowed conceptual direction:

```text
apps
  -> features
  -> application services
  -> game domain / simulation
  -> engine primitives
  -> platform abstractions
```

Protocol adapters depend on domain contracts, never the reverse.

Forbidden examples:

- `game-domain -> protocol-canary`;
- `renderer -> inventory feature`;
- `ui-core -> market feature`;
- `assets -> Oteryn Identity`;
- `platform -> game feature`;
- `protocol adapter -> concrete widget`;
- direct feature-to-feature state mutation.

Architecture tests must enforce crate dependency direction once the workspace exists.

## 7. Runtime invariants

- No global mutable `GameState` guarded by one broad mutex.
- No blocking file, network, decompression or shader work in the frame loop.
- Hot paths use bounded memory and bounded queues.
- Network and asset input is untrusted and validated before entering the domain model.
- Rendering consumes snapshots/extracted render data, not mutable simulation objects.
- UI consumes view models/signals, not protocol packets.
- The server remains authoritative for game state and action validity.
- Secrets never enter logs, crash payloads, replay files or extension APIs.

## 8. Modules and extensions

Core engine systems are compile-time Rust crates. First-party gameplay features are compile-time feature crates with explicit contracts. Optional third-party extensions, when enabled, run in a capability-limited WebAssembly sandbox.

Do not introduce native dynamic plugins or arbitrary extension filesystem/network access without a new security ADR.

## 9. Protocol and cross-repository work

Any change involving wire fields, identifiers, feature negotiation, authentication, session tickets, character/world/channel routing or assets requires:

- a shared coordination ID;
- exact producer and consumer versions;
- supported and unsupported pairs;
- rollout order and one-sided failure behavior;
- fixtures or runtime evidence on both sides;
- updates to the relevant cross-repository contract.

Record uncertainty; never invent Canary or Oteryn behavior.

## 10. Validation

Validation is proportional to the changed layer:

- docs: links, paths, consistency and complete diff review;
- domain: unit/property tests and deterministic replay cases;
- protocol: golden, malformed, truncated and fuzz cases;
- renderer: benchmark scenes, frame-time evidence and visual snapshots;
- UI: interaction, DPI, resolution and accessibility checks;
- assets/updater: signatures, hashes, path traversal, rollback and clean install;
- authentication: PKCE, callback, state, ticket replay and fallback-negative tests.

Never claim runtime, performance, server or platform compatibility without evidence from the exact tested revision.

## 11. Architecture changes

A change to a stable boundary requires an ADR. Do not silently alter:

- the greenfield Rust decision;
- protocol-adapter isolation;
- world-channel login/relog semantics;
- identity and one-shot ticket invariants;
- renderer snapshot boundary;
- extension sandbox requirement;
- signed updater and asset verification.
