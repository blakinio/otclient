---
task_id: OTC2-20260801-playability-p1-coordination
status: active
agent: "P1 contract-spine launch coordinator"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-coordination
phase: validation
branch: docs/OTC2-20260801-playability-p1-coordination
base_branch: main
created: 2026-08-01T22:24:00+02:00
updated: 2026-08-01T22:30:00+02:00
last_verified_commit: "b4b23be1362e1f38a69cc4e4fa766c6ce4fbf19b"
required_base_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
risk: medium
related_pr: 153
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-coordination.md
shared_path_lease: []
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: chat
context_pressure: medium
decomposition_decision: single
validation_level: focused
---

# Goal

Launch the accepted four-package P1 contract-spine wave from exact post-aggregation `main`, with exclusive ownership and a serialized shared integration lease.

# Dispatch result

| Worker | Branch | Draft PR | Initial head | Shared lease |
|---|---|---:|---|---|
| Canary source index | `tools/OTC2-20260801-playability-p1-canary-source-index` | #154 | `c86524850644e9d33373c88358a4eff904190e7f` | none required |
| Game-domain contracts | `feat/OTC2-20260801-playability-p1-game-domain-contract` | #155 | `074570a453dd6e8626b6c16ebf51d38bad2d8d1a` | not granted; first candidate after exclusive validation |
| Asset pack runtime | `feat/OTC2-20260801-playability-p1-asset-pack-runtime` | #156 | `326805dd1d18f18172365ec632b7a71e470ecb96` | not granted; waits for game-domain archive |
| Input actions | `feat/OTC2-20260801-playability-p1-input-actions` | #157 | `f2dbb5b983131d1e72464f9a95ad5d4f8a3b7d83` | not granted; waits for asset-runtime archive |

All workers start from `main@55fec043758e1928fd5d39831322a0c21f47589b`, initially own only their exclusive implementation/evidence paths and task path, and have one durable next action.

# Launch constraints

- `CANARY-SOURCE-INDEX` may integrate independently without root workspace changes.
- `GAME-DOMAIN-CONTRACT` is the first runtime public producer and first possible shared-lease holder after focused/component validation.
- `ASSET-PACK-RUNTIME` and `INPUT-ACTIONS` may implement exclusive crates now and stop at `integration_ready` until their serialized lease.
- No worker owns root workspace, lockfile, architecture policy, app composition, workflows or shared catalogues at launch.
- PR #23-owned `ACTIVE_WORK.md`, `MODULE_CATALOG.md` and `CHANGELOG.md` remain untouched.

# Acceptance

- [x] coordinator draft PR exists with one task path;
- [x] four worker branches/tasks/draft PRs exist;
- [x] exact exclusive paths are disjoint and match `WAVE_P1_CONTRACT_SPINE.md`;
- [x] no shared lease is granted at launch;
- [x] each worker checkpoint records the same accepted base and one next action;
- [x] coordinator checkpoint records exact worker PRs/heads;
- [ ] required CI and review gate pass;
- [ ] coordinator task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T22:30:00+02:00
head: b4b23be1362e1f38a69cc4e4fa766c6ce4fbf19b
branch: docs/OTC2-20260801-playability-p1-coordination
pr: 153
status: validating
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-coordination.md
proven:
  - P0 aggregation PR 151 and archive PR 152 are merged.
  - Four worker task/branch/draft PR lanes exist from exact main 55fec043.
  - Worker exclusive paths are disjoint and open PRs 23, 48 and 97 do not overlap them.
  - No shared integration lease is granted at launch.
derived:
  - Source-index may proceed and merge independently.
  - Runtime workers may develop exclusive paths concurrently but integrate serially.
unknown:
  - Exclusive implementation results and first shared-lease request.
conflicts: []
first_failure:
  marker: none
  evidence: all four dispatch writes and draft PR creations succeeded.
rejected_hypotheses:
  - Grant root workspace paths at launch: rejected by serialized lease contract.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-coordination.md
validation:
  - command: exact main/open PR/task/path ownership preflight
    result: PASS
    evidence: main 55fec043; unrelated open PRs own distinct paths.
  - command: four-lane dispatch reconciliation
    result: PASS
    evidence: PRs 154 through 157 exist with exact task paths, bases and empty shared leases.
blockers: []
next_action: Validate and merge coordinator PR 153, archive it separately, then execute source-index and game-domain exclusive work.
```
