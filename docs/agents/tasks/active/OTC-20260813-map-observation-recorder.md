---
task_id: OTC-20260813-map-observation-recorder
status: implementing
agent: Codex
project_lane: otclient
lane: otclient
track: otclient-global-login
track_alias: OTCLIENT-GLOBAL-LOGIN
task_kind: implementation
phase: design
branch: feat/OTC-20260813-map-observation-recorder
base_branch: main
start_sha: 005158b5b9bf25fe77bd5fc10813a6388a072836
created: 2026-08-13T21:14:46Z
updated: 2026-08-13T21:25:00Z
risk: medium
related_pr: null
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-map-observation-recorder.md
  - src/client/mapobservationrecorder.h
  - src/client/mapobservationrecorder.cpp
  - src/client/protocolgameparse.cpp
  - src/client/luafunctions.cpp
  - src/CMakeLists.txt
  - tests/unit/map/map_observation_recorder_test.cpp
  - tests/unit/map/CMakeLists.txt
modules_touched:
  - map-observation-recorder
  - protocol-game-map-state
reuses:
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
  - src/client/map.h
  - src/client/tile.h
  - src/client/thing.h
  - src/client/item.h
  - src/client/protocolgameparse.cpp
  - src/client/luafunctions.cpp
  - tests/support/**
depends_on:
  - PR #291 merged as 005158b5b9bf25fe77bd5fc10813a6388a072836
  - Track B PR #284 remains active with disjoint owned paths and runtime namespace
blocks:
  - runtime E2E until this task proves a unique native-Linux Track B namespace is available without conflicting with PR #284
cross_repo_tasks: []
execution_mode: codex
execution_reason: multi-file C++ implementation, focused tests, and build validation require a local checkout
decomposition_decision: single
feature_scope:
  type: contract_producer
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: producer_only
---

# Map Observation Recorder — P1

## Objective

Implement a disabled-by-default, read-only local JSONL recorder that exports
deterministic Map Observation Contract v1 records from OTClient's already
decoded `Map`/`Tile` state. The recorder must not parse raw packets, alter map
state, emit navigation input, resolve OTBM/server IDs, or contact a remote
service.

## Ownership and overlap

P0 is merged in `005158b5b9bf25fe77bd5fc10813a6388a072836`. P1 owns only the
paths declared above. Track B PR #284 owns its lab, workflow, login/version
compatibility files, and `docs/agents/MODULE_CATALOG.md`/`CHANGELOG.md`; this
task will not touch them. A later dedicated coordination change can catalogue
the recorder if PR #284 remains open when P1 reaches closeout.

## Acceptance inventory

- [ ] disabled-by-default recorder leaves normal protocol/map behavior unchanged;
- [ ] records come from decoded `Map`/`Tile` state after parser mutations;
- [ ] FULL, EMPTY, PARTIAL, and UNKNOWN cannot collapse;
- [ ] absolute positions, ordered things, raw identities, and factual subtype/state are preserved;
- [ ] snapshots/deltas and add/change/delete semantics remain distinct;
- [ ] local persistence is bounded and sink failure is non-fatal and visible;
- [ ] deterministic serialization tests pass, including secret exclusion;
- [ ] focused component validation passes;
- [ ] fresh audit has no material open finding;
- [ ] native-Linux Track B runtime E2E passes, or its exact ownership/resource barrier is recorded.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-13T21:25:00Z
head: 36021c5f519d3165b8d5bd1e7260f1fe9722b023
branch: feat/OTC-20260813-map-observation-recorder
pr: none
status: implementing
context_routes:
  - P1 local recorder implementation
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-map-observation-recorder.md
  - src/client/mapobservationrecorder.h
  - src/client/mapobservationrecorder.cpp
  - src/client/protocolgameparse.cpp
  - src/CMakeLists.txt
  - tests/unit/map/map_observation_recorder_test.cpp
  - tests/unit/map/CMakeLists.txt
proven:
  - P0 contract v1 is merged on main at 005158b5b9bf25fe77bd5fc10813a6388a072836.
  - Track B PR #284 owns no P1 declared path but does own its runtime namespace.
  - ProtocolGame mutates decoded Map/Tile state through setTileDescription and tile add/transform/remove handlers.
  - The repository provides nlohmann::ordered_json and an existing map unit-test target with tile builders.
derived:
  - The recorder can attach after existing decoded-state mutations without reparsing packet contents.
  - A bounded deferred JSONL queue avoids filesystem writes in the parser mutation handlers.
unknown:
  - Native-Linux runtime availability for a Track B smoke proof remains unverified.
conflicts:
  - MODULE_CATALOG.md and CHANGELOG.md are actively owned by Track B PR #284.
first_failure:
  marker: none
  evidence: none
rejected_hypotheses: []
changed_paths:
  - docs/agents/tasks/active/OTC-20260813-map-observation-recorder.md
  - src/client/mapobservationrecorder.h
  - src/client/mapobservationrecorder.cpp
  - src/client/luafunctions.cpp
  - src/client/protocolgameparse.cpp
  - src/CMakeLists.txt
  - tests/unit/map/CMakeLists.txt
  - tests/unit/map/map_observation_recorder_test.cpp
validation:
  - command: P0 merge and Track B ownership inspection
    result: PASS
    evidence: origin/main 005158b5b9bf25fe77bd5fc10813a6388a072836 and PR #284 changed-path inventory
  - command: implementation source inspection
    result: PASS
    evidence: recorder is Lua-enabled explicitly, disabled by default, and receives only decoded Map/Tile values
blockers: []
next_action: Run the focused map-recorder test build using the configured Windows test preset after initializing the supported MSVC developer environment.
```
