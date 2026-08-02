# Full-Playability Dependency and Parallelism Model

Status: programme coordination contract after P1 aggregation.
Current evidence base: `main@5d3dec1037eef508782e369afef8e3b7f1291e6a`.
Accepted next wave: `WAVE_P2_MINIMUM_VISIBLE_WORLD.md`.

This document defines safe concurrency, sole producers, shared-path leases and exact integration order. Maximize independent progress, not simultaneous edits.

## 1. Core operating rules

Parallel work is safe only when workers have:

- independent acceptance criteria;
- exclusive owned paths;
- merged producer contracts or explicit private synthetic fixtures;
- no competing claim on a public type/schema;
- no concurrent shared-path lease;
- durable tasks, branches, draft PRs and checkpoints;
- exact final restack and validation before merge.

Long duration, many files or slow CI do not justify a split. Ownership and independently testable outcomes do.

## 2. Coordinator topology

```text
Portfolio owner
  |
  v
Playability wave coordinator
  |-- bounded worker task / branch / draft PR
  |-- bounded worker task / branch / draft PR
  |-- bounded worker task / branch / draft PR
  `-- bounded worker task / branch / draft PR
       |
       v
Synchronization barrier
  -> reconcile evidence and live state
  -> serialize shared integration
  -> merge + separate archive per worker
  -> accept next bounded wave
```

A coordinator owns one phase. It dispatches or aggregates, persists durable state and exits; it does not remain active to wait.

## 3. Concurrency limits

### Discovery/research

- maximum one coordinator plus five workers;
- docs/evidence-only workers use disjoint paths;
- no source, manifests, lockfile, workflows or shared catalogues;
- barrier starts only after every result is merged/archived or durably blocked.

### Implementation

- normal maximum one coordinator plus four workers;
- reduce to one or two when a shared public contract is unstable;
- one sole producer per public interface;
- one shared integration lease holder at a time;
- final `apps/client/**` composition is always serialized.

### Validation

A fresh validator session is preferred after coherent implementation. Validation normally continues the same task unless it is a separate cross-package deliverable.

## 4. Sole public contract producers

| Contract group | Sole producer | Consumers allowed only after merge |
|---|---|---|
| gameplay IDs/session handles/`GameEvent`/`GameCommand` | `game-domain` | Canary adapters, simulation, feature state, UI action mapping, tests |
| exact Canary source/opcode/layout evidence | `canary-protocol-index` tool/evidence | bounded Canary parser tasks |
| simulation ownership and render snapshot publication | P2 `simulation-core` | protocol-event integration, world renderer, later UI view models and replay |
| generation-fenced renderer resource handles/upload/cache | P2 `renderer-resource` after merged `asset-decode` | world renderer, effects, minimap, viewport picking |
| asset pack open/verify/index/lookup handles | `asset-runtime` | decode, renderer/UI/text/audio resource consumers |
| normalized physical input/actions/contexts | `input-actions` | P2 `input-platform`, visible-world binding map, later UI bindings/hotkeys |
| UI primitives/focus/accessibility | future `ui-core` | auth/selection/inventory/chat/combat/settings UI |
| common view models/semantic UI actions | future application UI contract producer | concrete feature UI packages |
| audio intents/categories/device handles | future `audio-core` | gameplay/UI audio features |
| app lifecycle/composition | one integration owner | executable only |

Consumers may prepare private fixtures/adapters while waiting, but may not publish substitute public types or claim compatibility.

## 5. Completed P1 graph

```text
P0 aggregation/archive
  -> CANARY-SOURCE-INDEX #154/#180
  -> GAME-DOMAIN-CONTRACT #155/#175
  -> ASSET-PACK-RUNTIME #156/#177
  -> INPUT-ACTIONS #157/#183
  -> P1 barrier
```

All four P1 producers and separate archives are merged on `main@5d3dec1037eef508782e369afef8e3b7f1291e6a`. All P1 shared leases are released.

The P1 source index pins inspected development evidence to `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`. Existing `protocol-canary` runtime descriptors still name older source cuts. This is an explicit development-baseline conflict that the P2 protocol owner must reconcile mechanically before implementing gameplay layouts. It is not deployment proof.

## 6. Accepted staged P2 graph and ownership

```text
P1 merged contracts
  |
  +--> SIMULATION-SNAPSHOT
  +--> CANARY-WORLD-PROTOCOL (baseline alignment first)
  +--> ASSET-DECODE
  +--> INPUT-PLATFORM
  |
  ASSET-DECODE archived
  v
  RENDERER-RESOURCE
  |
  all five producers archived
  v
  VISIBLE-WORLD-INTEGRATION
  |
  owner inputs + integration archive
  v
  CONTROLLED-M2-ACCEPTANCE
```

Initial maximum concurrency is four workers: simulation, Canary protocol, asset decode and input platform. Renderer-resource starts after asset-decode. Visible-world integration is serialized and alone owns `apps/client/**`. Controlled acceptance is a separate operational task.

### SIMULATION-SNAPSHOT

Exclusive:

```text
oteryn-client/crates/simulation-core/**
docs/agents/tasks/active/OTC2-*-playability-p2-simulation-snapshot.md
```

Sole mutable gameplay writer and immutable `RenderSnapshot` producer. No Canary, GPU, asset, UI or platform types.

### CANARY-WORLD-PROTOCOL

Exclusive:

```text
oteryn-client/crates/protocol-canary/**
oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
oteryn-client/tests/integration/canary-world-protocol/**
docs/agents/tasks/active/OTC2-*-playability-p2-canary-world-protocol.md
```

First aligns runtime metadata to the generated `bc0068ab…` index while preserving fail-closed real admission, then implements only exactly evidenced M2 bootstrap/map/entity/movement/logout mapping.

### ASSET-DECODE

Exclusive:

```text
oteryn-client/crates/asset-decode/**
docs/agents/tasks/active/OTC2-*-playability-p2-asset-decode.md
```

Sole bounded synthetic-v1 CPU RGBA producer. No loose files, production importer or GPU work.

### RENDERER-RESOURCE

Exclusive:

```text
oteryn-client/crates/renderer-resource/**
docs/agents/tasks/active/OTC2-*-playability-p2-renderer-resource.md
```

Starts after asset-decode. Sole generation-fenced upload/resource/cache producer; no world mutation or draw policy.

### INPUT-PLATFORM

Exclusive:

```text
oteryn-client/crates/input-platform/**
docs/agents/tasks/active/OTC2-*-playability-p2-input-platform.md
```

Sole Windows/winit adapter into `input-actions`; no product keymap or gameplay commands.

### VISIBLE-WORLD-INTEGRATION

Exclusive:

```text
oteryn-client/crates/world-renderer/**
oteryn-client/apps/client/**
oteryn-client/tests/integration/visible-world/**
oteryn-client/docs/evidence/playability/p2/synthetic-visible-world.md
docs/agents/tasks/active/OTC2-*-playability-p2-visible-world-integration.md
```

One serialized partial-consumer owner for world rendering, product movement/logout bindings and original synthetic E2E. It may not claim M2 complete.

### CONTROLLED-M2-ACCEPTANCE

Exclusive:

```text
oteryn-client/docs/evidence/playability/p2/controlled-m2-acceptance/**
docs/agents/tasks/active/OTC2-*-playability-p2-controlled-m2-acceptance.md
```

Runs only with named deployment, disposable identity, asset, Windows/device, privacy and authorization inputs. It proves or falsifies the complete real M2 journey and routes defects to their sole owners.

## 7. Shared integration lease

Only one active task may own any overlapping portion of:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
oteryn-client/rust-toolchain.toml
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/apps/client/**
docs/agents/ACTIVE_WORK.md
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
.github/workflows/rust-client.yml
```

P2 workers may be granted only the subset listed by their accepted prompt. `apps/client/**` is granted only to VISIBLE-WORLD-INTEGRATION. Workflows and PR #23-owned `ACTIVE_WORK.md`, `MODULE_CATALOG.md` and `CHANGELOG.md` are not granted unless a later explicit coordinator decision changes ownership.

Lease procedure:

1. worker proves exclusive-path implementation with focused/component validation;
2. coordinator verifies no stale writer and records the exact lease;
3. worker restacks on exact current `main`;
4. worker integrates workspace/category/docs and regenerates `Cargo.lock` with pinned Cargo;
5. worker runs exact-head heavy gates;
6. worker merges and creates a separate archive PR;
7. archive merge releases the lease;
8. next worker restacks and receives it.

Manual lockfile conflict resolution, copied fragments, hidden concurrent edits and undocumented lease transfer are prohibited.

## 8. Work allowed in parallel

During initial P2 exclusive-path development, at most four independent workers may own:

- simulation-core and render snapshot contracts;
- Canary baseline alignment/gameplay protocol mapping;
- synthetic-v1 asset decode;
- Windows/winit input-platform adapter.

A worker blocked on the serialized shared lease may commit a coherent exclusive-path result, mark `integration_ready`, checkpoint one next action and exit. It does not poll.

Renderer-resource starts after asset-decode merges. Visible-world integration starts only after all five producer tasks merge and separately archive. Controlled M2 acceptance starts only after integration archive and named owner inputs.

Safe supporting work includes private deterministic fixtures, parser negative corpora and non-overlapping benchmark harness design; none may publish substitute contracts or claim compatibility.

## 9. Work that must remain serialized

Always serialize:

- competing definitions of game IDs, `GameEvent`, `GameCommand`, snapshot, asset-handle, input-action, UI-core or audio-intent schemas;
- architecture category/rule changes;
- workspace membership/dependency policy/lockfile integration;
- `apps/client/**` composition;
- production asset schema/signature/activation;
- exact Canary profile/build compatibility claims using one fixture corpus/state machine;
- cross-repository producer changes and client consumption;
- release activation/rollback.

## 10. P2 non-goals

P2 does not authorize:

- broad inventory/container/chat/combat/social/modern-feature implementation;
- UI framework, settings, audio, minimap, launcher or updater work;
- production asset importer/signing/redistribution;
- guessed Canary field layouts or deployed-revision equality;
- official Tibia service compatibility;
- legacy runtime dependencies;
- production activation or release claims.

A-F packages deliver bounded producers/partial consumers. Only controlled M2 acceptance may establish the first playable milestone.

## 11. Post-P2 planning boundary

Planning only after controlled M2 PASS:

```text
P2 minimum visible world
  -> P3 core gameplay: items/containers/chat/combat/UI/audio
  -> P4 daily-playable product
  -> P5 selected exact-profile parity
  -> P6 production hardening/release
```

No P3 package starts merely because its design is listed. The P2 barrier and controlled acceptance must reconcile exact producer/runtime evidence and select bounded sole owners. Independent non-M2 work requires a separate explicit barrier decision.

## 12. Worker lifecycle

Every worker:

1. verifies exact main, task/checkpoint, PRs/reviews/CI, producers and paths;
2. creates one task, branch and draft PR;
3. performs only minimal discovery needed for the bounded phase;
4. implements one coherent result in exclusive paths;
5. checkpoints after material findings/changes and before long/failure-prone work;
6. runs focused then component validation;
7. obtains/restacks under shared lease only when ready;
8. runs heavy exact-head validation;
9. merges through repository gates;
10. archives in a separate PR;
11. exits with one next action or none.

## 13. Coordinator barriers

At every barrier the coordinator:

- verifies live Git/PR/CI/tasks and stale sessions;
- reads compact checkpoints and referenced evidence;
- normalizes `PROVEN`, `DERIVED`, `UNKNOWN`, `CONFLICT`;
- resolves producer names and duplicate recommendations;
- updates capability/dependency documents;
- chooses the smallest safe next package set;
- assigns sole producers and shared leases;
- writes prompts compliant with `PROMPTING_STANDARD.md`;
- archives the barrier task separately.

## 14. Cross-repository and owner decisions

Oteryn Platform, Gateway and Canary changes remain separate repository tasks. Client workers record exact producer revisions and fail closed when contracts are insufficient.

The following owner decisions do not block bounded original synthetic P2 producer work but block controlled M2, deployment or production claims:

- exact deployed Canary revision/configuration/build;
- staging environment/account policy;
- production asset rights/local-import/redistribution;
- Windows support matrix;
- performance budgets;
- telemetry/privacy;
- signing/release channels and selected M5 feature scope.

## 15. Evidence and artifacts

Prompts/checkpoints remain compact. Store large generated indexes, fixture metadata, traces, screenshots, performance results, fuzz corpora and logs as owned evidence/artifact outputs. Never store credentials, private captures, proprietary bytes or personal data.

## 16. Stop/escalation conditions

Stop and checkpoint on:

- ownership conflict or stale writer;
- missing public producer;
- source/profile evidence conflict;
- legal provenance required for current scope;
- material architecture change;
- unsafe context pressure;
- two failed heavy attempts;
- product/legal/deployment authorization requirement.

Technical choices inside accepted exclusive ownership remain autonomous.
