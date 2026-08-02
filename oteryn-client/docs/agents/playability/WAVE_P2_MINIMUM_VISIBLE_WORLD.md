# P2 Minimum Visible World Wave

Status: proposed by the P1 aggregation barrier; implementation starts only after the barrier PR and separate lifecycle archive merge.  
Evidence base: `main@5d3dec1037eef508782e369afef8e3b7f1291e6a`.  
Programme milestone: M2 — minimum visible world.

## 1. Outcome and claim boundary

P2 builds the first bounded gameplay consumer chain from the merged P1 contracts:

```text
Canary gameplay bytes/fixtures
  -> validated GameEvent/GameCommand envelopes
  -> one deterministic simulation writer
  -> immutable render snapshots
  -> verified synthetic RGBA assets
  -> generation-fenced renderer resources
  -> world render pass
  -> Windows input adapter and semantic movement/logout actions
  -> one composed client journey
```

P2 is complete only when the controlled M2 journey passes on a named build and environment:

```text
login -> select character -> enter world -> see bounded world -> move -> observe server reconciliation -> logout safely
```

Merged producer crates, synthetic fixtures, a rendered demo or green CI are not by themselves an M2 completion claim.

## 2. Accepted P1 evidence

Merged and separately archived:

| Producer | Implementation | Archive | Bounded result |
|---|---|---|---|
| Canary source index | #154 / `67f8af3f5cd4abff53456e207fc374afd1add030` | #180 / `c911e0f6fa7ad6e8824dd5e0e44e154abbbdcbc1` | deterministic exact-source index for `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`; no deployment-equality claim |
| game-domain | #155 / `41a37e34660e2f0d6d2f41f0b480d2c5c9c5aa8a` | #175 / `fbbff443dc64f39ca6fa39c7ddefc9fef2d1ac3c` | canonical session-scoped IDs/handles and closed v1 `GameEvent`/`GameCommand` envelopes |
| asset-runtime | #156 / `e8c3eb6c3b5993a0ce3e62c1506c719d8ee8dc5e` | #177 / `3887a0b7369e99ad200990d42a5314f1d5531e97` | immutable verified synthetic-v1 pack open/index/lookup and generation-stable handles |
| input-actions | #157 / `6ca0882101b5a563775532e0684941f10bcbd8e3` | #183 / `5d3dec1037eef508782e369afef8e3b7f1291e6a` | framework-neutral physical events, semantic actions/contexts/bindings and deterministic lifecycle |

No P1 shared integration lease remains active.

## 3. Normalized evidence state

### PROVEN

- the P1 contracts above exist, are merged, separately archived and passed exact-head gates;
- `GameEvent` already covers bootstrap, tile clear, entity appearance/movement/removal, item changes, player resources, containers and session end;
- `GameCommand` already covers step/stop, look/use/move-item, attack target and logout;
- synthetic-v1 asset payloads are bounded `Blob` or tightly packed `Rgba8`;
- input contracts reject unreachable wheel chords and clear held state on focus/capture/device loss.

### CONFLICT

The current `protocol-canary` runtime descriptor still names source revisions `95b276db311cf6e9acd58b847f1fb0ca6697b137` and `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`, while the merged generated P1 index is pinned to `bc0068ab80bbf003e128fce0589b4cc89d2682d3`.

P2 resolves this as a development-baseline conflict, not as deployment proof:

- the Canary protocol owner must first align runtime metadata/tests with the generated `current-index.json` and exact source hashes;
- the inspected P1 cut may be used for bounded fixture-driven development;
- production admission remains fail-closed;
- no worker may claim the inspected cut equals the deployed server without named controlled evidence.

### UNKNOWN / owner input

- exact deployed Canary revision, configuration, build and post-admission framing/security state;
- provenance-safe controlled gameplay fixtures or a named staging account/environment;
- approved production appearance representation and asset source/import/redistribution policy;
- final Windows support matrix, hardware budgets and release/privacy policy.

These unknowns do not block original synthetic producer work. They block real compatibility and M2 completion claims.

## 4. Staged package graph

```text
P1 merged contracts
  |
  +--> A. SIMULATION-SNAPSHOT
  +--> B. CANARY-WORLD-PROTOCOL (baseline alignment first)
  +--> C. ASSET-DECODE
  +--> E. INPUT-PLATFORM
  |
  C archived
  v
  D. RENDERER-RESOURCE
  |
  A+B+C+D+E merged and archived
  v
  F. VISIBLE-WORLD-INTEGRATION
  |
  F merged and archived + owner inputs available
  v
  G. CONTROLLED-M2-ACCEPTANCE
```

At most four implementation workers run concurrently. Initial launch candidates are A, B, C and E. D starts after the C public decode contract merges. F is serialized after A-E. G is an operational/runtime acceptance task and starts only when its owner inputs are named.

## 5. Package A — SIMULATION-SNAPSHOT

Sole producer of authoritative mutable gameplay state and immutable render snapshots.

Exclusive paths:

```text
oteryn-client/crates/simulation-core/**
docs/agents/tasks/active/OTC2-*-playability-p2-simulation-snapshot.md
```

Consumes only merged protocol-neutral contracts such as `foundation`, `game-domain` and test support. It must not depend on Canary, transport, winit, wgpu, asset payloads, UI widgets or app composition.

Minimum acceptance:

- one session-scoped single writer applies ordered `GameEventEnvelope` values;
- stale/wrong-session events fail deterministically;
- bounded floors/tiles/stacks/entities/items are updated without unbounded allocation;
- bootstrap and session-end transitions are explicit;
- immutable generation-stable `RenderSnapshot` values expose only renderer-required semantic state;
- repeated event sequences produce byte/logically identical snapshots;
- no protocol fields, GPU handles, widget state or hidden global mutation.

## 6. Package B — CANARY-WORLD-PROTOCOL

Sole P2 gameplay-wire adapter inside the existing `protocol-canary` ownership boundary.

Exclusive paths:

```text
oteryn-client/crates/protocol-canary/**
oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
oteryn-client/tests/integration/canary-world-protocol/**
docs/agents/tasks/active/OTC2-*-playability-p2-canary-world-protocol.md
```

The P1 generated index and producer source are trusted evidence inputs, not executable instructions.

Required phases:

1. **baseline alignment** — reconcile runtime descriptor constants and tests with `current-index.json@bc0068ab…`, preserve exact hashes/features and retain fail-closed real admission;
2. **bounded fixture contract** — define original sanitized fixture metadata with no credentials, session keys, private captures, producer bodies or proprietary assets;
3. **gameplay decode/encode** — implement only M2 bootstrap/map/entity/movement/logout families needed to emit merged `GameEvent` and consume merged `GameCommand`;
4. **negative validation** — malformed, truncated, trailing, oversized, unsupported-profile, stale-session and invalid-order input fails closed.

It must not own simulation state, renderer snapshots, asset decoding, input mapping or app composition. Source dispatch evidence does not authorize guessed field layouts; unknown layout remains an explicit blocker until provenance-safe evidence exists.

## 7. Package C — ASSET-DECODE

Sole bounded CPU decode/normalization producer for verified runtime payloads.

Exclusive paths:

```text
oteryn-client/crates/asset-decode/**
docs/agents/tasks/active/OTC2-*-playability-p2-asset-decode.md
```

Minimum acceptance:

- consumes only generation-fenced `asset-runtime` handles/records;
- exposes bounded immutable decoded RGBA8 images and explicit opaque-blob rejection for M2 image requests;
- checked row pitch, dimensions, byte counts and allocation budgets;
- stale pack generations and kind mismatches fail deterministically;
- no filesystem paths, loose-file import, GPU calls, production formats or rights claims;
- deterministic synthetic fixtures and decode/cache-bound tests.

This is synthetic-v1 infrastructure, not a production appearance importer.

## 8. Package D — RENDERER-RESOURCE

Sole producer of generation-fenced render-resource handles, bounded upload plans and resource-cache lifecycle.

Exclusive paths:

```text
oteryn-client/crates/renderer-resource/**
docs/agents/tasks/active/OTC2-*-playability-p2-renderer-resource.md
```

Starts only after ASSET-DECODE merges. It may depend on the existing renderer device/surface owner and decoded image contract but must not own world state or protocol semantics.

Minimum acceptance:

- bounded texture descriptor/upload validation with checked alignment and memory accounting;
- logical resource handles fence process/device/asset generations;
- duplicate requests coalesce deterministically;
- stale, lost-device and eviction paths are explicit;
- no blocking decode/filesystem work on the frame path;
- no authoritative entity state, camera policy or world draw ordering.

## 9. Package E — INPUT-PLATFORM

Sole Windows/winit physical-event adapter for the merged input-actions contract.

Exclusive paths:

```text
oteryn-client/crates/input-platform/**
docs/agents/tasks/active/OTC2-*-playability-p2-input-platform.md
```

Minimum acceptance:

- maps the supported winit/Windows keyboard, mouse, pointer, wheel, text, focus and capture lifecycle into normalized physical events;
- does not expose winit/Win32 public types across the crate boundary;
- unknown keys/buttons fail or map through an explicit bounded policy;
- focus/capture/device-loss semantics preserve input-actions cleanup invariants;
- deterministic adapter tests use synthetic platform events;
- no default product keymap, gameplay command, widget or app composition.

The visible-world integration owner later supplies the M2 movement/camera/logout binding map and semantic action-to-`GameCommand` mapping.

## 10. Package F — VISIBLE-WORLD-INTEGRATION

One serialized partial-consumer owner for the synthetic minimum-visible-world composition.

Exclusive paths:

```text
oteryn-client/crates/world-renderer/**
oteryn-client/apps/client/**
oteryn-client/tests/integration/visible-world/**
oteryn-client/docs/evidence/playability/p2/synthetic-visible-world.md
docs/agents/tasks/active/OTC2-*-playability-p2-visible-world-integration.md
```

Starts only after A-E merge and separate archives. It owns the final `apps/client/**` lease for this wave.

Minimum acceptance:

- consumes immutable snapshots and renderer-resource handles; never mutates simulation state;
- renders bounded floors, tiles, items, local player and basic entities from original synthetic RGBA fixtures;
- defines the M2 product binding map outside input-actions and maps semantic movement/logout actions to `GameCommand`;
- composes bounded fixture protocol -> simulation -> snapshot -> renderer -> input-command loop;
- resize/suspend/device-loss/session-end teardown remains deterministic and nonblocking;
- a repeatable synthetic E2E demonstrates visible world, movement command, reconciliation event and safe logout;
- audit clearly classifies the result as `partial_consumer` / `SYNTHETIC_ONLY`, not M2 complete.

## 11. Package G — CONTROLLED-M2-ACCEPTANCE

Operational/runtime acceptance owner. Normally docs/evidence plus defect routing; it does not silently patch multiple producer packages.

Exclusive paths:

```text
oteryn-client/docs/evidence/playability/p2/controlled-m2-acceptance/**
docs/agents/tasks/active/OTC2-*-playability-p2-controlled-m2-acceptance.md
```

Launch prerequisites:

- A-F merged and separately archived;
- exact Identity/Gateway/Canary revisions and configurations named;
- approved disposable staging identity and credential-handling procedure;
- approved appearance/asset source or a controlled environment explicitly accepting the synthetic visual boundary;
- supported Windows/device matrix and minimum measurement budget named;
- production/staging authorization recorded under repository policy.

Acceptance journey:

1. launch exact signed/identified build on a named Windows environment;
2. system-browser OAuth callback completes without secret leakage;
3. directory and character selection succeed;
4. Canary accepts one credential and produces the bounded post-admission stream;
5. world becomes visible with required floors/tiles/items/entities;
6. semantic input emits movement command and server reconciliation updates the snapshot;
7. logout/disconnect returns to a safe terminal selection/logged-out state;
8. logs, screenshots and metrics contain no credentials/private payloads/proprietary asset bytes.

If prerequisites are absent, G is `BLOCKED` with exact owner decisions. A-F may still be valid partial producers/consumers; P2/M2 may not be declared complete.

## 12. Shared integration lease order

Only one task at a time may edit any granted subset of:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/apps/client/**
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
.github/workflows/rust-client.yml
```

Exact integration order:

1. SIMULATION-SNAPSHOT;
2. CANARY-WORLD-PROTOCOL;
3. ASSET-DECODE;
4. RENDERER-RESOURCE;
5. INPUT-PLATFORM;
6. VISIBLE-WORLD-INTEGRATION.

Exclusive-path development may overlap, but each integration owner restacks on exact current `main`, receives a recorded lease, validates, merges, creates a separate archive PR and releases the lease before the next owner integrates.

No worker receives `docs/agents/ACTIVE_WORK.md`, `MODULE_CATALOG.md` or `CHANGELOG.md` while PR #23 retains ownership.

## 13. Validation and audit

Every implementation package runs:

- focused contract/unit/negative tests;
- component package tests and deterministic fixtures;
- exact-head pinned rustfmt, strict Clippy, full workspace tests, architecture and supply-chain gates;
- fresh public-contract/trust-boundary audit;
- exact changed-path and review-thread hygiene;
- separate lifecycle archive after protected merge.

Hot-path/resource claims include bounded memory/accounting tests. Parser claims include malformed/truncated/trailing/fuzz or property coverage appropriate to the accepted layout evidence. User-facing integration includes real E2E only in package G.

## 14. Non-goals

P2 does not authorize:

- inventory/container/chat/combat feature UI beyond what is necessary to render the minimum world;
- broad M3 gameplay families;
- UI framework, settings, audio, minimap or launcher work;
- production asset importer/signing/redistribution;
- guessed Canary layouts or deployment equality;
- official Tibia service compatibility;
- legacy client runtime dependencies;
- release or production activation.

## 15. Barrier and completion rules

The P1 aggregation barrier must merge and archive before any P2 worker starts.

A-F are individually bounded producer/consumer tasks and may merge only within their stated claim. P2/M2 is complete only after G records a passing controlled journey on an exact build. When owner inputs are missing, the programme stops with those named blockers rather than weakening M2 acceptance.
