---
task_id: OTC-20260816-world-observation-atlas-boundary
status: investigating
agent: ChatGPT
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: documentation
phase: programme-reconciliation
branch: docs/OTC-20260816-world-observation-atlas-boundary
base_branch: main
start_sha: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
created: 2026-08-16T23:09:00+02:00
updated: 2026-08-16T23:09:00+02:00
risk: medium
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
owned_paths:
  - docs/agents/tasks/active/OTC-20260816-world-observation-atlas-boundary.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_WORLD_OBSERVATION_ATLAS_BOUNDARY.md
  - docs/agents/tasks/active/OTC-20260813-map-observation-export.md
  - docs/agents/tasks/archive/OTC-20260813-map-observation-export.md
modules_touched: []
reuses:
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
depends_on:
  - coordinator-promoted P0-STATE/worldmap evidence
  - coordinator-promoted P1 bridge on current main
blocks:
  - Track A observation-index/export implementation dispatch
cross_repository_tasks:
  - OTH-20260813-world-reconstruction-navigation
execution_mode: chat-github
execution_class: github_hosted
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
mutation_authorized: false
owner_funded_ai_api_authorized: false
---

# Track A world observation / Atlas boundary reconciliation

## Objective

Persist the current producer-side architecture for `OTS-20260813-world-reconstruction-navigation` after the programme evolved beyond the original Track-B/open-source-OTClient recorder design.

## Decisions

- Track A `official-client-re` / official native Linux Tibia client is the authoritative live producer.
- Track B is not used to produce Real Tibia verification evidence.
- PR #292 (`feat(client): add map observation recorder`) is closed unmerged as superseded because it instruments the wrong runtime/product for this programme.
- `MAP_OBSERVATION_V1` remains the normalized producer-neutral semantic record contract.
- Track A should maintain a local durable world-observation index and export deterministic sanitized changed-chunk bundles for separately authorized Atlas consumption.
- Initial integration is file/artifact based; no live Track A -> Atlas network service is required.
- Atlas requests semantic exploration missions/targets; it does not own the physical official-client runtime or blind input scripts.
- Track A RUNTIME remains the physical persistent login/display/input/gameplay/relogin evidence owner.

## Producer index requirements

The eventual Track A observation index should preserve:

- absolute x/y/z;
- completeness state;
- ordered tile contents;
- raw client identities/factual categories;
- deterministic tile fingerprint;
- exact producer/client provenance;
- first/last observation metadata and observation count;
- material history when the tile fingerprint changes;
- acquisition method when proven;
- enough source/session provenance to audit promoted bundles.

Repeated equivalent observations may be deduplicated by fingerprint while incrementing observation metadata. Changed observations retain history rather than silently overwriting evidence.

SQLite is a preferred implementation candidate, not a frozen semantic requirement.

## Export boundary

Promoted sanitized export should align with the consumer Atlas 128x128 world chunks and should export only dirty/changed chunks after initial state.

Raw client/appearance identity must never be silently converted to OTBM server identity. Identity mapping remains a separately verified consumer/integration step even when asset versions match.

## Access/coverage provenance

Track A should preserve acquisition method when it is established, for example:

- normal traversal;
- conditional traversal;
- transition;
- teleport;
- admin teleport;
- passive world stream;
- other verified method.

Observation does not prove normal-player reachability or a walk edge. Some tiles may only be verifiable with special/GM/admin teleport; those facts belong in provenance so Atlas can model accessibility independently from verification.

## Execution boundary

This reconciliation is `github_hosted`, `runtime_access: none` and grants no physical-runtime authority.

Future index/export implementation should default to hosted deterministic work under current Track A routing. Physical E2E is provided by RUNTIME and current runtime-admission gates. A producer task must not bootstrap or take over the canonical runtime as an implementation shortcut.

## First integration milestone

```text
exact official Linux client
-> structurally verified absolute tile observations
-> local index/deduplication
-> MAP_OBSERVATION_V1-compatible changed-chunk export
-> separately promoted sanitized consumer bundle
```

Autonomous exploration is a later milestone.

## Acceptance

- [x] wrong-product PR #292 is closed unmerged;
- [x] Track A producer authority is preserved;
- [x] producer-side index/export responsibilities are documented;
- [x] physical RUNTIME authority is not broadened;
- [x] cross-repository Atlas consumption remains a separately authorized/promoted boundary;
- [ ] stale original map-observation P0 task is archived/released;
- [ ] programme document is committed and validated;

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-16T23:09:00+02:00
status: investigating
branch: docs/OTC-20260816-world-observation-atlas-boundary
base_main: b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
proven:
  - MAP_OBSERVATION_V1 on current main already declares Track A as current authoritative producer.
  - current Track A routing separates hosted P0/P1/P2 work from physical RUNTIME evidence.
  - old PR #292 implements an open-source OTClient Map/Tile recorder and is therefore the wrong producer for this programme.
owner_decisions:
  - Track A agent should index discovered Global Tibia tile facts and deliver changed indexed data to Atlas.
  - Atlas must visualize verified/unverified coverage and accessibility, including tiles unavailable to an ordinary character.
  - Atlas should provide humans and agents with remaining verification targets.
unknown:
  - exact producer index engine and bundle encoding beyond frozen semantic requirements.
blockers: []
next_action: Finish producer boundary programme doc and archive the stale original P0 task, then open the documentation reconciliation PR for review/CI.
```
