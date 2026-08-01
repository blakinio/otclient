# Full-Playability Dependency and Parallelism Model

Status: programme coordination contract.  
This document defines how many agents may work safely, which contracts serialize work, and how integration occurs without conflicting ownership.

## 1. Operating principle

Maximize independent progress, not simultaneous edits.

Parallel work is safe when workers have:

- independent acceptance criteria;
- exclusive owned paths;
- merged producer contracts or explicit synthetic fixtures;
- no competing claim on a public type/schema;
- no concurrent shared-path lease;
- durable tasks, branches, draft PRs and checkpoints.

A long task or many files is not itself a reason to split. A split requires genuinely independent domains or ownership.

## 2. Programme control structure

```text
Portfolio owner
  |
  v
Playability wave coordinator
  |-- worker task A / branch / draft PR
  |-- worker task B / branch / draft PR
  |-- worker task C / branch / draft PR
  |-- worker task D / branch / draft PR
  `-- worker task E / branch / draft PR
       |
       v
Synchronization barrier
  -> deduplicate evidence
  -> resolve contracts/leases
  -> merge/archive in order
  -> accept next bounded wave
```

One coordinator owns a wave. The coordinator does not implement worker packages and does not remain active merely to wait.

## 3. Concurrency limits

### Discovery/research waves

- maximum: 1 coordinator + 5 workers;
- workers must produce independent documents/evidence paths;
- no source, manifest, lockfile, workflow or shared catalogue edits;
- aggregation occurs only after all completed/blocked outputs are durable.

### Implementation waves

- normal maximum: 1 coordinator + 4 workers;
- reduce to 1-2 workers when a shared public contract is unstable;
- only one contract producer per shared interface;
- only one shared integration lease holder;
- final app composition is always serialized.

### Validation

A fresh validator session is preferred after coherent implementation. It normally continues the same task unless validation is an independent cross-package deliverable.

## 4. Sole public contract producers

These contracts serialize downstream work and must have one accepted producer:

| Contract group | Sole producer before consumers | Consumers that may proceed after merge |
|---|---|---|
| gameplay IDs, session entity handles, `GameEvent`, `GameCommand` | game-domain contract task | protocol adapters, simulation, features, tests |
| simulation ownership/lifecycle and snapshot publication | simulation-core task | renderer extraction, view models, replay |
| render snapshot and logical resource handles | render-contract task or agreed game-domain slice | world renderer, effects, minimap |
| UI primitives, view-model binding and semantic UI actions | `ui-core` producer | inventory/chat/combat/selection/settings UI |
| normalized input actions/contexts | input-core producer | gameplay movement, UI bindings, hotkeys |
| audio intents/categories/voice handles | audio-core producer | gameplay/UI audio features |
| asset pack open/verify/index/lookup/decode handles | asset-runtime producer | renderer, UI/text, audio, importer tests |
| exact Canary gameplay mapping | protocol-specific producers by bounded message family | app/domain integration only after exact evidence |
| app lifecycle/composition | one integration owner | executable only |

Consumers may prepare private fixtures/adapters but may not publish substitute public types.

## 5. Candidate wave graph

This is a planning graph, not authorization beyond P0.

```text
P0 independent evidence inventories
  |
  v
P1 shared contract spine
  |-- GAME-CONTRACT (first sole producer)
  |-- ASSET-RUNTIME contract/open/lookup
  |-- UI/INPUT/AUDIO contract designs or bounded producers
  `-- exact Canary fixture acquisition plan
  |
  v
P2 minimum visible world
  |-- PROTOCOL-MAP ------+
  |-- WORLD-STATE -------+--> APP-VERTICAL-SLICE
  |-- ASSET-DECODE ------+
  |-- WORLD-RENDERER ----+
  `-- INPUT-MOVEMENT ----+
  |
  v
P3 core gameplay packages
  |-- entity/movement/combat
  |-- items/inventory/containers
  |-- chat/social/NPC
  |-- UI core + feature panels
  `-- audio/settings/relog
  |
  v
P4 daily-playable product
  |-- polished selection/HUD/minimap/hotkeys
  |-- launcher/update/pack signing
  |-- reconnect/recovery
  `-- performance/soak/accessibility
  |
  v
P5 exact supported feature parity
  |
  v
P6 production hardening/release
```

The coordinator may change package boundaries after P0 evidence, but must preserve one producer and milestone acceptance.

## 6. Safe parallel work examples

After merged contracts, these pairs may be independent:

- Canary map decoder and asset-runtime pack lookup;
- world-state implementation and renderer-resource implementation using agreed fixtures;
- chat feature and inventory feature after shared domain/UI contracts merge;
- audio backend and settings core;
- protocol negative/fuzz harness and renderer benchmark harness;
- launcher/update work and gameplay feature work when paths/contracts do not overlap;
- independent feature E2E scenarios with separate fixtures and output artifacts.

## 7. Work that must be serialized

Always serialize:

- competing definitions of `GameEvent`, `GameCommand`, entity/item/container IDs or snapshot schemas;
- architecture category/rule changes;
- root workspace membership, dependency policy and lockfile integration;
- `apps/client/**` final composition;
- production asset pack schema/signature changes;
- UI-core public primitives and concrete feature consumers before the core merges;
- exact Canary profile/build compatibility claims that share one fixture corpus or protocol state machine;
- cross-repository producer contract changes and client consumption;
- release activation/rollback changes.

## 8. Shared-path lease

Only one active task may hold any overlapping portion of this set:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
oteryn-client/deny.toml
oteryn-client/rust-toolchain.toml
oteryn-client/tools/architecture-check/**
oteryn-client/tests/architecture-fixtures/**
oteryn-client/apps/client/**
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
oteryn-client/docs/operations/RUST_WORKSPACE.md
.github/workflows/rust-client.yml
```

Lease rules:

1. worker claims exact paths in its task and PR after fresh overlap check;
2. other workers keep them read-only;
3. exclusive-path work may commit and reach `integration_ready`;
4. lease holder restacks on exact `main`, integrates root metadata and regenerates `Cargo.lock` with pinned Cargo;
5. focused/component/heavy validation runs on exact integrated head;
6. merge and separate archive release the lease;
7. next worker restacks and claims the released lease.

Manual lockfile conflict resolution, copied fragments, concurrent shared-doc edits and undocumented lease transfer are prohibited.

## 9. Worker lifecycle

Every worker:

1. verifies live main, active tasks, PRs, required CI, producer contracts and owned paths;
2. creates/claims one active task, branch and draft PR;
3. performs only minimal discovery required for its phase;
4. checkpoints after material findings/changes and before heavy/failure-prone work;
5. runs focused then component validation;
6. persists one coherent result;
7. obtains the integration lease only when ready;
8. runs heavy final validation on exact final head;
9. merges through the repository gate;
10. archives lifecycle in a separate PR;
11. exits with one next action or none.

A worker blocked by another task records `waiting`/`blocked`, releases its session and exits. It does not poll.

## 10. Coordinator barrier

At every barrier the coordinator:

- runs the control room and verifies live Git/PR/CI;
- confirms no stale worker is still writing;
- reads only compact checkpoints and referenced evidence indexes;
- normalizes `PROVEN`, `DERIVED`, `UNKNOWN` and `CONFLICT` results;
- updates the capability matrix;
- deduplicates or resolves contradictory recommendations;
- chooses the smallest safe next package set;
- assigns sole producers and leases;
- writes prompts compliant with `PROMPTING_STANDARD.md`;
- archives the barrier task instead of waiting for the next wave.

## 11. Producer-consumer merge strategy

Preferred sequence for each shared contract:

```text
producer discovery/design
-> producer implementation
-> focused/component validation
-> fresh validator
-> producer merge
-> producer lifecycle archive
-> consumer restack on exact merge
-> consumer integration and exact-head gates
```

Consumers may develop against an explicit private fixture contract only when:

- it cannot become a public substitute;
- the task states it will restack on the producer;
- no compatibility claim is made before exact producer integration.

## 12. Cross-repository changes

Changes to Oteryn Platform, Gateway or Canary are separate tasks/repositories with their own ownership and validation. Client workers:

- record exact producer revision and contract;
- do not write external repositories unless separately authorized;
- do not invent missing server fields/routing;
- mark client work `BLOCKED` when the producer contract is insufficient;
- resume only after the producer merge/revision is durable.

## 13. Evidence and artifacts

Prompts/checkpoints remain compact. Store large:

- packet/fixture indexes;
- generated compatibility matrices;
- screenshots/video;
- performance traces;
- fuzz corpora/results;
- build logs/binaries;
- staging run logs;

as repository/workflow artifacts or evidence indexes. Never store credentials, private captures, proprietary bytes or personal data.

## 14. Stop/escalation conditions

Stop and checkpoint when:

- ownership conflicts;
- a missing public producer blocks safe work;
- exact server/profile evidence conflicts;
- legal provenance is unresolved for required assets;
- a material architecture change is required;
- context pressure becomes unsafe;
- two heavy attempts fail;
- owner authorization is required for product scope, legal acceptance, production deployment or deferral.

Technical choices inside accepted ownership remain autonomous.
