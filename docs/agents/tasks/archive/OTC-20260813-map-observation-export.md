---
task_id: OTC-20260813-map-observation-export
status: completed
agent: Codex
project_lane: otclient
lane: otclient
task_kind: contract-producer
phase: archived-bootstrap
base_branch: main
created: 2026-08-13T22:24:00+02:00
updated: 2026-08-16T23:09:00+02:00
risk: medium
related_pr: 291
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
implementation_merge_commit: 005158b5b9bf25fe77bd5fc10813a6388a072836
producer_ownership_correction_merge: b771cf53f01db02a27c9a2a4d9018e7592900111
ownership_released: true
superseded_by_task: OTC-20260816-world-observation-atlas-boundary
owned_paths: []
modules_touched: []
execution_mode: archived
---

# Map observation export — archived P0 bootstrap

## Result

This task originally froze the repository-local `MAP_OBSERVATION_V1` semantics and deterministic fixtures through PR #291. The core v1 invariants remain valid and live in `docs/agents/contracts/MAP_OBSERVATION_V1.md`.

The original task text incorrectly framed the future producer as the open-source OTClient/Track B Map/Tile runtime. That producer ownership was later corrected on current history through merged PR #362 / commit `b771cf53f01db02a27c9a2a4d9018e7592900111`: the current authoritative live producer is Track A `official-client-re` using the official native Linux Tibia client.

The obsolete open-source OTClient recorder implementation PR #292 was closed unmerged on 2026-08-16.

## Preserved P0 semantics

Version 1 continues to require:

- `tile_snapshot`, `tile_delta`, `transition_event`, `navigation_action_result`;
- distinct `FULL`, `EMPTY`, `PARTIAL`, `UNKNOWN` knowledge states;
- absence never interpreted as empty;
- ordered observed contents;
- raw client identity never assumed to be OTBM/server identity;
- exact producer/client provenance;
- non-secret session correlation;
- decoded resulting state for verified transition/action success;
- no credential/session secret material or raw packet payloads.

## Continuation

Current continuation is not this task. Resolve:

- `docs/agents/tasks/active/OTC-20260816-world-observation-atlas-boundary.md`;
- `docs/agents/programs/OTCLIENT_TIBIA_RE_WORLD_OBSERVATION_ATLAS_BOUNDARY.md`;
- current Track A P0/P1/RUNTIME/worldmap tasks and live ownership.

`next_action: none`
