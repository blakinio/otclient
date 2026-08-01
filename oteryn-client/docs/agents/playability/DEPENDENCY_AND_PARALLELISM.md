# Full-Playability Dependency and Parallelism Model

Status: programme coordination contract after P0 aggregation.  
Current evidence base: `main@6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b`.  
Accepted next wave: `WAVE_P1_CONTRACT_SPINE.md`.

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
| simulation ownership and snapshot publication | future `simulation-core` producer | world state integration, renderer extraction, UI view models, replay |
| render snapshot and renderer resource handles | future snapshot/renderer-resource producers | world renderer, effects, minimap, viewport picking |
| asset pack open/verify/index/lookup handles | `asset-runtime` | decode, renderer/UI/text/audio resource consumers |
| normalized physical input/actions/contexts | `input-actions` | platform adapter, gameplay mapping, UI bindings, hotkeys |
| UI primitives/focus/accessibility | future `ui-core` | auth/selection/inventory/chat/combat/settings UI |
| common view models/semantic UI actions | future application UI contract producer | concrete feature UI packages |
| audio intents/categories/device handles | future `audio-core` | gameplay/UI audio features |
| app lifecycle/composition | one integration owner | executable only |

Consumers may prepare private fixtures/adapters while waiting, but may not publish substitute public types or claim compatibility.

## 5. Accepted P1 graph

```text
P0 merged evidence + aggregation/archive
  |
  +--> P1 CANARY-SOURCE-INDEX  (tool/evidence, no workspace lease)
  |
  `--> P1 GAME-DOMAIN-CONTRACT (first gameplay public producer)
          |
          +-- shared lease released/archive complete
          v
      P1 ASSET-PACK-RUNTIME
          |
          +-- shared lease released/archive complete
          v
      P1 INPUT-ACTIONS
          |
          v
      P1 barrier
```

Exclusive-path development may overlap. Integration and merge order is exact:

1. `CANARY-SOURCE-INDEX`;
2. `GAME-DOMAIN-CONTRACT`;
3. `ASSET-PACK-RUNTIME`;
4. `INPUT-ACTIONS`.

The source-index task may merge first because it publishes evidence, not runtime types and requires no root workspace lease. Game-domain must be the first merged gameplay public contract. Asset-runtime and input-actions are independent but serialize root integration.

## 6. P1 package ownership

### CANARY-SOURCE-INDEX

Exclusive:

```text
oteryn-client/tools/canary-protocol-index/**
oteryn-client/docs/evidence/playability/p1/canary-current-source-index.md
oteryn-client/docs/evidence/playability/p1/canary-current-fixture-index.md
docs/agents/tasks/active/OTC2-20260801-playability-p1-canary-source-index.md
```

No shared lease and no workspace member.

### GAME-DOMAIN-CONTRACT

Exclusive:

```text
oteryn-client/crates/game-domain/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
```

First holder of the P1 shared integration lease.

### ASSET-PACK-RUNTIME

Exclusive:

```text
oteryn-client/crates/asset-runtime/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
```

Reads `asset-types` and `asset-compiler` but does not edit them. Second shared-lease holder after game-domain merge/archive.

### INPUT-ACTIONS

Exclusive:

```text
oteryn-client/crates/input-actions/**
docs/agents/tasks/active/OTC2-20260801-playability-p1-input-actions.md
```

Third shared-lease holder after asset-runtime merge/archive.

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

P1 workers may be granted only the subset listed by their accepted prompt. `apps/client/**`, workflows and PR #23-owned `ACTIVE_WORK.md`, `MODULE_CATALOG.md` and `CHANGELOG.md` are not granted in P1.

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

During P1 exclusive-path development:

- source-index tooling/evidence;
- game-domain crate implementation;
- asset-runtime crate implementation against current synthetic read-only schema;
- input-actions crate implementation with no platform/UI/game-domain public dependency.

A worker blocked on the lease may commit a coherent exclusive-path result, mark `integration_ready`, checkpoint one next action and exit. It does not poll.

After P1 producers merge, likely safe parallel pairs include:

- Canary map parser and asset decode;
- world-state and renderer-resource against merged contracts;
- input platform adapter and audio-core;
- UI-core and simulation-core when public dependencies are explicit;
- protocol negative/fuzz harness and renderer benchmark harness.

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

## 10. P1 non-goals

P1 does not authorize:

- simulation/world state/snapshots;
- map/entity/movement gameplay parser implementation;
- renderer resources/world rendering;
- UI core/view models/feature screens;
- audio core/backend/resources;
- production importers/assets/signing;
- staging/deployment/account use;
- launcher/release activation;
- app composition.

These require the P1 barrier and their own sole producers.

## 11. Candidate post-P1 graph

Planning only:

```text
merged P1 game-domain + source index + asset runtime + input actions
  |
  +--> simulation-core + snapshot contract
  +--> Canary bootstrap/map/entity/movement bounded parsers
  +--> asset appearance/decode + renderer-resource
  +--> platform input adapter
  +--> ui-core/common view-model/action contracts
  `--> audio-core
          |
          v
P2 minimum visible world vertical slice
          |
          v
P3 core gameplay
          |
          v
P4 daily-playable product
          |
          v
P5 selected exact-profile parity
          |
          v
P6 production hardening/release
```

No post-P1 package starts merely because its design is listed here. The P1 barrier must verify producer merges, evidence and ownership.

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

The following owner decisions do not block P1 synthetic/source contract work but block deployment or production claims:

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
