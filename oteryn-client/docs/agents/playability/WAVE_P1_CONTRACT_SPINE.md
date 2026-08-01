# P1 Contract Spine Wave

Status: accepted by the P0 aggregation barrier  
Wave ID: `OTERYN-PLAYABILITY-P1-CONTRACT-SPINE`  
Implementation authorized: **bounded per worker prompt**  
Normal concurrency: one coordinator plus at most four workers  
Current planning base: `main@6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b`

## 1. Objective

Create the smallest public contract spine that lets later M2 gameplay packages start without competing IDs, events, commands, asset handles or input actions. This wave does not implement simulation, map decoding, world rendering, UI feature screens, audio, app composition, production assets or real staging.

P1 contains four bounded packages:

1. `GAME-DOMAIN-CONTRACT` — sole producer of canonical gameplay identifiers and closed command/event envelopes;
2. `CANARY-SOURCE-INDEX` — mechanically generated exact-source protocol index and safe deterministic fixture metadata;
3. `ASSET-PACK-RUNTIME` — immutable synthetic-v1 pack open/verify/index/lookup runtime and logical handles;
4. `INPUT-ACTIONS` — normalized physical input and semantic action/context contracts independent of winit and UI features.

## 2. Why this is the smallest safe wave

P0 proved that gameplay consumers cannot start safely before one canonical game-domain producer exists. It also proved that:

- exact Canary source families are known, but numeric layouts and bootstrap order must be generated rather than copied;
- the current asset schema/compiler is synthetic test infrastructure, but an immutable verified runtime can be implemented without deciding production rights or import formats;
- semantic input actions can be produced independently, while UI core and feature screens must wait for stable domain/view-model/resource contracts;
- audio, simulation, snapshots, renderer resources and UI core remain subsequent producers.

No package in P1 may publish substitute versions of another package's public contracts.

## 3. Barrier gates before dispatch

The P1 coordinator must verify:

1. P0 aggregation PR and its separate lifecycle archive are merged;
2. exact current `main`, open PRs, active tasks, reviews and required CI;
3. none of the task/output paths below is already owned;
4. the four worker branches start from the same accepted base or explicitly restack before integration;
5. no worker initially owns root workspace, lockfile, architecture policy, app composition or shared catalogue paths;
6. the shared integration lease is granted to only one worker at a time;
7. PR #23-owned `ACTIVE_WORK.md`, `MODULE_CATALOG.md` and `CHANGELOG.md` remain untouched.

## 4. Package A — GAME-DOMAIN-CONTRACT

Prompt:

```text
oteryn-client/docs/agents/prompts/P1_GAME_DOMAIN_CONTRACT_AGENT.md
```

Proposed task and branch:

```text
OTC2-20260801-playability-p1-game-domain-contract
feat/OTC2-20260801-playability-p1-game-domain-contract
```

Exclusive implementation paths:

```text
oteryn-client/crates/game-domain/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
```

Shared integration lease, granted only after exclusive-path validation:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
```

Public contract responsibility:

- session-scoped generations and canonical IDs for entities, creatures, items, containers, tiles/positions and player identity where required by M2/M3;
- closed, versioned `GameEvent` envelope for validated server-originated semantic events;
- closed, versioned `GameCommand` envelope for local semantic commands;
- explicit stale-generation rules, bounded text/value payloads and stable errors;
- no Canary opcodes/layouts, sockets, simulation state, renderer types, widgets or app composition.

Acceptance:

- one canonical type family, no duplicate identifier wrappers in downstream crates;
- deterministic equality/order/hash semantics where meaningful;
- constructors validate bounds and reject stale/invalid combinations;
- command/event variants cover only the minimum shared M2 spine plus explicit extension/version policy;
- focused property/negative tests and architecture edge evidence;
- no external dependency unless separately justified and accepted.

## 5. Package B — CANARY-SOURCE-INDEX

Prompt:

```text
oteryn-client/docs/agents/prompts/P1_CANARY_SOURCE_INDEX_AGENT.md
```

Proposed task and branch:

```text
OTC2-20260801-playability-p1-canary-source-index
tools/OTC2-20260801-playability-p1-canary-source-index
```

Exclusive paths:

```text
oteryn-client/tools/canary-protocol-index/**
oteryn-client/docs/evidence/playability/p1/canary-current-source-index.md
oteryn-client/docs/evidence/playability/p1/canary-current-fixture-index.md
docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md
```

Responsibility:

- mechanically inspect only the accepted producer cut `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3` unless live owner evidence replaces it;
- generate direction, numeric opcode, handler/send method, layout source path, profile/build gate, order/state prerequisite and proposed bounded package owner;
- generate fixture feasibility/provenance metadata using source-derived or project-original synthetic material;
- report conflicts and unsupported extraction instead of guessing;
- never store credentials, session keys, private captures, proprietary asset bytes or copied server implementation bodies.

This package publishes evidence/artifacts, not public runtime Rust types. It may merge before `GAME-DOMAIN-CONTRACT` and must not add a workspace member.

## 6. Package C — ASSET-PACK-RUNTIME

Prompt:

```text
oteryn-client/docs/agents/prompts/P1_ASSET_PACK_RUNTIME_AGENT.md
```

Proposed task and branch:

```text
OTC2-20260801-playability-p1-asset-pack-runtime
feat/OTC2-20260801-playability-p1-asset-pack-runtime
```

Exclusive implementation paths:

```text
oteryn-client/crates/asset-runtime/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
```

Read-only producer contract:

```text
oteryn-client/crates/asset-types/**
oteryn-client/tools/asset-compiler/**
```

Shared integration lease: the same root/architecture paths listed for package A, acquired only after A releases them.

Responsibility:

- open immutable synthetic-v1 packs through already-opened/capability-safe objects;
- verify schema/version, declared lengths/counts/ranges, hashes and full-file consistency;
- build a bounded immutable index and expose generation-stable logical lookup handles;
- reject malformed, overlapping, trailing, duplicate, unsupported or oversized input with stable errors;
- deterministic teardown/stale-generation behavior;
- no decode scheduling, GPU upload, loose-file access, production importer, remote download, signing key, rights claim or app activation.

Production schema/signing/local-import decisions remain later/owner decisions. P1 proves only the safe runtime spine over project-original synthetic fixtures.

## 7. Package D — INPUT-ACTIONS

Prompt:

```text
oteryn-client/docs/agents/prompts/P1_INPUT_ACTIONS_AGENT.md
```

Proposed task and branch:

```text
OTC2-20260801-playability-p1-input-actions
feat/OTC2-20260801-playability-p1-input-actions
```

Exclusive implementation paths:

```text
oteryn-client/crates/input-actions/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
```

Shared integration lease: the same root/architecture paths, granted after previous holders release it.

Responsibility:

- normalized physical key/button/pointer/wheel/text/focus/capture events;
- semantic action identifiers, contexts, bindings, modifier/chord and repeat policy;
- deterministic context precedence, conflict detection, held-state cleanup and stale-focus/capture behavior;
- bounded text and pointer data with stable errors;
- no winit types in public contracts, no widgets, no game-domain commands, no settings persistence, no default product keymap and no app composition.

Gameplay/UI consumers later map accepted semantic actions to merged `GameCommand` or UI actions.

## 8. Execution and merge order

Workers may develop exclusive paths in parallel after dispatch, but integration is serialized.

Accepted order:

```text
CANARY-SOURCE-INDEX
-> GAME-DOMAIN-CONTRACT
-> ASSET-PACK-RUNTIME
-> INPUT-ACTIONS
```

Rationale:

- source-index is tool/evidence-only and needs no shared workspace lease;
- game-domain must be the first merged public gameplay contract producer;
- asset runtime and input actions are independent public producers but share root/architecture integration paths, so they merge one at a time;
- every worker restacks on exact current `main` immediately before taking the shared lease;
- each merged worker receives a separate lifecycle archive before the next shared lease holder integrates.

A worker may reach `integration_ready` while another holder owns shared paths, then exits with one next action. It must not poll or copy lockfile fragments.

## 9. Validation ladder

### CANARY-SOURCE-INDEX

Focused:

- deterministic generator/parser unit tests;
- exact producer revision and source-path resolution;
- two consecutive generations are byte-identical;
- no secrets/private captures/proprietary bytes.

Component:

- generated index reconciled against representative bootstrap, map, entity, movement, player, item/container, chat and combat dispatch/send paths;
- contradiction review against P0 inventory.

Heavy final:

- repository required CI on exact final documentation/tool head;
- clean review/thread/ownership gate.

### Rust producer packages

Focused:

- package tests, malformed/boundary/stale-generation cases and public API review;
- `cargo fmt --check` and strict package Clippy using the pinned toolchain.

Component:

- package plus direct producer/consumer fixture tests;
- architecture checker with accepted category edges;
- deterministic teardown and no panic/unwrap on untrusted input.

Heavy final after shared integration:

- locked workspace metadata;
- full Windows workspace rustfmt, strict Clippy and tests;
- architecture validation;
- cargo-deny supply-chain gate;
- repository `CI / Required` on exact final head;
- clean review/thread/ownership gate.

After one heavy failure, isolate the first relevant error cheaply. No worker performs more than two heavy attempts in one session.

## 10. Explicit non-goals and later producers

Not in P1:

- simulation ownership and mutable world state;
- render snapshots, renderer resources/world rendering;
- Canary gameplay parser implementations;
- UI core, common view models or feature screens;
- audio backend/intents/resources;
- production asset schema/importers/signing/rights;
- real staging, deployment, credentials, packaging or release activation;
- `apps/client/**` composition.

Next barrier candidates after all four P1 packages merge/archive:

1. simulation/snapshot contract producer;
2. asset appearance/decode plus renderer-resource producers;
3. protocol-canary bootstrap/map packages consuming generated index and game-domain contracts;
4. UI-core/common action/view-model and audio-core producers;
5. controlled M1 staging task when owner/operations inputs exist.

## 11. Owner decisions that do not block P1

P1 may proceed using bounded synthetic/source evidence while these remain unresolved:

- exact deployed Canary revision/configuration/build string;
- production asset source, local-import and redistribution approval;
- approved staging environment and disposable account/character;
- final Windows support matrix;
- product performance budgets;
- telemetry/privacy and signing/release policy.

They block deployment/release claims and later production consumers, not these four contract-spine packages.

## 12. Completion rule

P1 is complete when all four packages are merged and separately archived, root/shared leases are released, public producers are unique, exact-head heavy gates are green and no app/gameplay consumer implementation was smuggled into the wave.
