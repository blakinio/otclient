---
task_id: OTC2-20260801-playability-p1-coordination
status: active
agent: "P1 contract-spine launch coordinator"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-coordination
phase: implementation
branch: docs/OTC2-20260801-playability-p1-coordination
base_branch: main
created: 2026-08-01T22:24:00+02:00
updated: 2026-08-01T22:24:00+02:00
last_verified_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
required_base_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
risk: medium
related_pr: null
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

# Accepted workers

1. `OTC2-20260801-playability-p1-canary-source-index` — evidence/tooling; no shared lease.
2. `OTC2-20260801-playability-p1-game-domain-contract` — first gameplay public producer and first shared-lease candidate.
3. `OTC2-20260801-playability-p1-asset-pack-runtime` — exclusive development now; shared integration only after game-domain archive.
4. `OTC2-20260801-playability-p1-input-actions` — exclusive development now; shared integration only after asset-runtime archive.

# Launch constraints

- All branches begin at `main@55fec043758e1928fd5d39831322a0c21f47589b`.
- Workers initially own only their exclusive paths and task path.
- No worker initially owns root workspace, lockfile, architecture policy, app composition, workflows or shared catalogues.
- `CANARY-SOURCE-INDEX` may integrate independently.
- `GAME-DOMAIN-CONTRACT` may request the first shared integration lease after focused/component validation.
- `ASSET-PACK-RUNTIME` and `INPUT-ACTIONS` may reach `integration_ready` but must not poll or modify shared paths.
- PR #23-owned `ACTIVE_WORK.md`, `MODULE_CATALOG.md` and `CHANGELOG.md` remain untouched.

# Acceptance

- [ ] coordinator draft PR exists with one task path;
- [ ] four worker branches/tasks/draft PRs exist;
- [ ] exact exclusive paths are disjoint and match `WAVE_P1_CONTRACT_SPINE.md`;
- [ ] no shared lease is granted at launch;
- [ ] each worker checkpoint records the same accepted base and one next action;
- [ ] coordinator checkpoint records exact worker PRs/heads;
- [ ] required CI and review gate pass;
- [ ] coordinator task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T22:24:00+02:00
head: 55fec043758e1928fd5d39831322a0c21f47589b
branch: docs/OTC2-20260801-playability-p1-coordination
pr: null
status: implementing
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
  - Open PRs 23, 48 and 97 do not overlap P1 exclusive paths.
  - None of the four P1 task/output path sets exists on current main.
derived:
  - Four workers may develop exclusive paths concurrently.
  - Shared workspace integration remains serialized and unassigned at launch.
unknown:
  - Worker PR numbers and initial heads until dispatch completes.
conflicts: []
first_failure:
  marker: none
  evidence: fresh launch ownership preflight passed.
rejected_hypotheses:
  - Grant all workers root workspace paths at launch: rejected due serialized lease contract.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-coordination.md
validation:
  - command: exact main/open PR/task/path ownership preflight
    result: PASS
    evidence: main 55fec043; no P1 path conflicts; unrelated PRs own distinct paths.
blockers: []
next_action: Open the coordinator draft PR, then create the four worker branches, task checkpoints and draft PRs from exact main.
```
