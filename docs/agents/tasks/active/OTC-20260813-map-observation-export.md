---
task_id: OTC-20260813-map-observation-export
status: investigating
agent: ChatGPT
project_lane: otclient
lane: otclient
task_kind: contract-producer
phase: P0-contract-bootstrap
branch: docs/OTC-20260813-map-observation-export
base_branch: main
start_sha: dc18f795bf13cee37a115164da56a452aaa14f02
created: 2026-08-13T22:24:00+02:00
updated: 2026-08-13T22:24:00+02:00
risk: medium
related_pr: null
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-map-observation-export.md
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
modules_touched:
  - map-observation-contract
reuses:
  - src/client/map.h
  - src/client/tile.h
  - src/client/protocolgameparse.cpp
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
cross_repo_tasks:
  - OTH-20260813-world-reconstruction-navigation
execution_mode: chat-github
decomposition_decision: split
---

# Map observation export — P0 producer contract

## Objective

Define the producer side of a versioned, non-secret observation contract that can export semantic map facts from the native Linux `blakinio/otclient` to the OTBM Atlas consumer under shared coordination ID `OTS-20260813-world-reconstruction-navigation`.

This P0 task is contract/documentation only. It does not take over Track B PR #284, does not touch its live runtime namespace, and does not implement client steering or map capture yet.

## Track boundary

- This project is not Track A and does not analyze/control the official client.
- Any future live proof using `blakinio/otclient` against Tibia Global must remain inside the Track B native-Linux boundary and must first resolve current Track B ownership from live state.
- P0 may use stable repository-owned OTClient source facts but not another track's transient PID, container, port, display, state directory or session.
- Cross-repository sharing is limited to the promoted versioned contract and non-secret observation artifacts.

## Producer contract requirements

Version 1 must represent:

1. `tile_snapshot` with absolute position, explicit completeness and ordered observed things;
2. `tile_delta` for later map updates;
3. `transition_event` with decoded before/after position evidence;
4. `navigation_action_result` with requested semantic step and decoded resulting state.

Required invariants:

- `FULL`, `EMPTY`, `PARTIAL` and `UNKNOWN` are distinct;
- no absent record is interpreted as an empty tile;
- raw client/appearance identity is preserved without pretending it is an OTBM/server ID;
- producer commit and client/protocol version are included;
- session ID is opaque and non-secret;
- authentication/session credentials and secret-bearing payloads are forbidden;
- ordering of observed tile things is stable and explicit;
- input emission alone cannot mark navigation success; decoded result state is required.

## Planned P1 integration points

After P0 is merged and Track B ownership is revalidated, a separate implementation task may instrument the already-decoded client map surface around:

- full tile descriptions produced by `ProtocolGame::setTileDescription`;
- map row/full-description updates;
- tile add/change/delete/update events;
- existing `Map`/`Tile` getters for semantic state;
- existing pathfinding for local same-floor navigation.

P1 must avoid duplicating packet parsing and must remain read-only with respect to canonical OTBM.

## Acceptance inventory

- [ ] `MAP_OBSERVATION_V1.md` defines field semantics and forbidden data.
- [ ] Producer/consumer shared ID is exactly `OTS-20260813-world-reconstruction-navigation`.
- [ ] Contract distinguishes full snapshots, deltas, transitions and action results.
- [ ] Completeness semantics prevent UNKNOWN -> EMPTY corruption.
- [ ] Identity semantics prevent client ID -> OTBM/server ID guessing.
- [ ] Contract contains no credential/session secret material.
- [ ] Future live implementation is explicitly gated on current Track B ownership and native Linux runtime rules.
- [ ] Otheryn consumer task is linked by exact task ID.

## Codex routing

P0 does not require Codex. P1 is a good Codex candidate because it is a bounded multi-file C++ serializer/hook/test package; later local-navigation implementation is also suitable after the contract and runtime ownership are stable.

Owner-funded Codex/API quota is forbidden unless the owner explicitly authorizes that specific use. This task does not grant permission.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T22:24:00+02:00
status: investigating
branch: docs/OTC-20260813-map-observation-export
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
proven:
  - Current OTClient source has semantic Map/Tile state and existing pathfinding primitives.
  - Track B PR #284 does not own this P0 task's planned documentation paths.
  - TIBIA_RESEARCH_TRACKS requires live OTClient-to-Global work to stay inside Track B and forbids sharing transient runtime ownership.
derived:
  - A versioned file/artifact contract is the lowest-coupling safe first integration boundary with Otheryn.
unknown:
  - Final physical encoding beyond deterministic readable P0 fixtures.
conflicts: []
blockers: []
next_action: Finalize MAP_OBSERVATION_V1.md and merge this P0 contract before any producer implementation begins.
```