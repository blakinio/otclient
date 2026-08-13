---
task_id: OTC-20260813-map-observation-export
status: validating
agent: Codex
project_lane: otclient
lane: otclient
task_kind: contract-producer
phase: P0-contract-bootstrap
branch: docs/OTC-20260813-map-observation-export
base_branch: main
start_sha: dc18f795bf13cee37a115164da56a452aaa14f02
created: 2026-08-13T22:24:00+02:00
updated: 2026-08-13T20:48:59Z
risk: medium
related_pr: 291
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-map-observation-export.md
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
  - docs/agents/contracts/fixtures/map_observation_v1/**
  - tools/agents/validate_map_observation_v1_fixtures.py
modules_touched:
  - map-observation-contract
reuses:
  - src/client/map.h
  - src/client/tile.h
  - src/client/protocolgameparse.cpp
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
cross_repo_tasks: []
execution_mode: chat-github
decomposition_decision: split
---

# Map observation export — P0 producer contract

## Objective

Define the producer side of a versioned, non-secret observation contract that can export semantic map facts from the native Linux `blakinio/otclient` as local artifacts under shared coordination ID `OTS-20260813-world-reconstruction-navigation`.

This P0 task is contract/documentation only. It does not take over Track B PR #284, does not touch its live runtime namespace, and does not implement client steering or map capture yet.

## Track boundary

- This project is not Track A and does not analyze/control the official client.
- Any future live proof using `blakinio/otclient` against Tibia Global must remain inside the Track B native-Linux boundary and must first resolve current Track B ownership from live state.
- P0 may use stable repository-owned OTClient source facts but not another track's transient PID, container, port, display, state directory or session.
- Per `TIBIA_RESEARCH_TRACKS.md`, P0 keeps its fixture authority and acceptance in `blakinio/otclient`; no external repository is read, written, or made a dependency.

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

- [x] `MAP_OBSERVATION_V1.md` defines field semantics and forbidden data.
- [x] Producer shared ID is exactly `OTS-20260813-world-reconstruction-navigation`.
- [x] Contract distinguishes full snapshots, deltas, transitions and action results.
- [x] Completeness semantics prevent UNKNOWN -> EMPTY corruption.
- [x] Identity semantics prevent client ID -> OTBM/server ID guessing.
- [x] Contract contains no credential/session secret material.
- [x] Deterministic local JSONL fixtures cover the version-1 record shapes and negative invariants.
- [x] Future live implementation is explicitly gated on current Track B ownership and native Linux runtime rules.

## Future cross-repository evidence (not P0 acceptance)

- A separately authorized external consumer may demonstrate compatible ingestion
  after an explicit scope decision. That work cannot become a Track B runtime or
  contract dependency under the current repository-only research boundary.

## Codex routing

P0 does not require Codex. P1 is a good Codex candidate because it is a bounded multi-file C++ serializer/hook/test package; later local-navigation implementation is also suitable after the contract and runtime ownership are stable.

Owner-funded Codex/API quota is forbidden unless the owner explicitly authorizes that specific use. This task does not grant permission.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T20:48:59Z
head: c799a1bb38fc93a349255919fd1fb84820aefb64
branch: docs/OTC-20260813-map-observation-export
pr: 291
status: validating
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
context_routes:
  - repository-local P0 contract and fixture corpus
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-map-observation-export.md
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
  - docs/agents/contracts/fixtures/map_observation_v1/**
  - tools/agents/validate_map_observation_v1_fixtures.py
proven:
  - PR #291 owns only the P0 task and contract paths; PR #284 owns no overlapping path.
  - The repository-local JSONL corpus deterministically covers FULL, EMPTY, UNKNOWN, PARTIAL, transition, and navigation-result shapes.
  - The fixture validator passes and rejects collapsed UNKNOWN/EMPTY, unordered stacks, fabricated delete things, non-canonical JSON, and secret-shaped field names.
  - PR #291 review thread PRRT_kwDOTVmdjs6ZE1qI is resolved on the pushed contract head.
derived:
  - Repository-local fixture authority resolves the open review concern without reading or depending on an external repository.
unknown:
  - External consumer ingestion is not evidenced in this repository and is not part of this Track B contract gate.
conflicts:
  - The original P0 text made external acceptance implementation-blocking, conflicting with TIBIA_RESEARCH_TRACKS repository-only coordination.
first_failure:
  marker: exact-head validation pending
  evidence: contract commit c799a1bb38fc93a349255919fd1fb84820aefb64 is pushed to PR #291
rejected_hypotheses:
  - External repository acceptance is required for local P0: contradicted by TIBIA_RESEARCH_TRACKS.md repository-only rule and the PR review finding.
changed_paths:
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
  - docs/agents/contracts/fixtures/map_observation_v1/README.md
  - docs/agents/contracts/fixtures/map_observation_v1/records.jsonl
  - docs/agents/tasks/active/OTC-20260813-map-observation-export.md
  - tools/agents/validate_map_observation_v1_fixtures.py
validation:
  - command: python tools/agents/validate_map_observation_v1_fixtures.py
    result: PASS
    evidence: six-record deterministic corpus validated locally
  - command: git diff --check
    result: PASS
    evidence: working-tree P0 diff has no whitespace errors
blockers:
  - P0 requires exact-head PR validation before it can be merged; P1 must not start on this unmerged contract.
next_action: Observe the exact-head checks for the pushed P0 checkpoint and, if they pass, complete the required documentation audit and merge closeout before considering P1.
```
