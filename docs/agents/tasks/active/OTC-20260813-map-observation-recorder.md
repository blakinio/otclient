---
task_id: OTC-20260813-map-observation-recorder
status: waiting
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
updated: 2026-08-13T21:56:00Z
risk: medium
related_pr: 292
shared_coordination_id: OTS-20260813-world-reconstruction-navigation
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-map-observation-recorder.md
  - src/client/mapobservationrecorder.h
  - src/client/mapobservationrecorder.cpp
  - src/client/protocolgameparse.cpp
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

## Explicit local enablement

The recorder remains off unless the client settings contain both values below
before decoded map observations begin. The output is a user-chosen local JSONL
path; no network sink is configured.

```otml
map-observation-recorder-enabled: true
map-observation-recorder-output: /absolute/local/path/observations.jsonl
```

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
updated_at: 2026-08-13T21:56:00Z
head: 373297e0516f1083a8dbbcb7a024ecaa64e90fda
branch: feat/OTC-20260813-map-observation-recorder
pr: 292
status: waiting
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
  - PR #292 is a draft P1 implementation PR, based on the merged P0 head.
  - The configured Windows test preset currently fails while vcpkg builds OpenAL before any P1 translation unit is compiled: OpenAL 1.25.1 emits C3889 under MSVC 14.52.
  - The configured Linux test preset in Ubuntu WSL fails while vcpkg builds ALSA before any P1 translation unit is compiled because `autoconf`, `autoconf-archive`, `automake`, and `libtoolize` are absent.
  - CI run 31747079596 passed all required jobs on 373297e0516f1083a8dbbcb7a024ecaa64e90fda, but its `Build - Windows` job was intentionally skipped; it is not C++ build evidence.
derived:
  - The recorder can attach after existing decoded-state mutations without reparsing packet contents.
  - A bounded deferred JSONL queue avoids filesystem writes in the parser mutation handlers.
  - The recorder can read two explicit local settings once before its first observation, keeping its default state disabled without modifying Track B's Lua binding file.
unknown:
  - Native-Linux runtime availability for a Track B smoke proof remains unverified.
conflicts:
  - MODULE_CATALOG.md and CHANGELOG.md are actively owned by Track B PR #284.
  - An initial P1 commit touched src/client/luafunctions.cpp, which is owned by Track B PR #284; that touch is removed before the next P1 push and is not in the final-base diff.
first_failure:
  marker: windows-tests-vcpkg-openal
  evidence: OpenAL 1.25.1 C3889 with MSVC 14.52 during `cmake --preset windows-tests`, before CMake generated a P1 build target.
rejected_hypotheses: []
changed_paths:
  - docs/agents/tasks/active/OTC-20260813-map-observation-recorder.md
  - src/client/mapobservationrecorder.h
  - src/client/mapobservationrecorder.cpp
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
    evidence: recorder is disabled by default, has explicit local settings, and receives only decoded Map/Tile values after parser mutations.
  - command: `cmake --preset windows-tests && cmake --build --preset windows-tests --target otclient_tile_order_tests && ctest --preset windows-tests -R MapObservationRecorder`
    result: BLOCKED
    evidence: vcpkg OpenAL 1.25.1 C3889 under MSVC 14.52, before configuration generated the target.
  - command: `VCPKG_ROOT=/home/mole/vcpkg cmake --preset linux-tests` in Ubuntu WSL
    result: BLOCKED
    evidence: vcpkg ALSA requires missing autoconf, autoconf-archive, automake, and libtoolize before configuration generated the target.
  - command: GitHub Actions CI run 31747079596 on 373297e0516f1083a8dbbcb7a024ecaa64e90fda
    result: PASS_WITH_LIMITATION
    evidence: required static/syntax jobs passed; `Build - Windows` was skipped.
blockers:
  - The required Windows test preset cannot currently compile the repository's OpenAL dependency with the sole installed MSVC toolchain.
  - The available Ubuntu WSL environment lacks the system tools required for the configured Linux test preset's ALSA dependency.
  - Native-Linux Track B runtime E2E remains unavailable because PR #284 owns the only known runtime namespace.
next_action: Re-run the focused P1 target with a supported configured toolchain after the repository owner provides a non-conflicting native test environment with its declared dependencies installed.
```
