---
task_id: OTC2-20260801-playability-p0-aggregation
status: active
agent: "P0 playability barrier coordinator"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0-aggregation
phase: validation
branch: docs/OTC2-20260801-playability-p0-aggregation
base_branch: main
created: 2026-08-01T21:45:00+02:00
updated: 2026-08-01T22:08:00+02:00
last_verified_commit: "b6dfea73115d5a3687f1444e8fa4d07cfb07050d"
required_base_commit: "6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b"
risk: medium
related_pr: 151
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-aggregation.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_GAME_DOMAIN_CONTRACT_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_CANARY_SOURCE_INDEX_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_ASSET_PACK_RUNTIME_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_INPUT_ACTIONS_AGENT.md
shared_path_lease: []
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: chat
context_pressure: high
decomposition_decision: single
validation_level: heavy
---

# Goal

Aggregate all five merged and archived P0 evidence lanes into one normalized capability/dependency result and publish the smallest safe producer-first P1 contract-spine wave with compliant worker prompts.

# Result

The barrier accepted four bounded P1 packages in exact integration order:

1. `CANARY-SOURCE-INDEX` — deterministic exact-source and fixture evidence, no runtime public types;
2. `GAME-DOMAIN-CONTRACT` — sole gameplay IDs/handles and closed `GameEvent`/`GameCommand` producer;
3. `ASSET-PACK-RUNTIME` — immutable synthetic-v1 pack open/verify/index/lookup and logical handles;
4. `INPUT-ACTIONS` — normalized physical events and semantic action/context producer.

Only one shared workspace/lockfile/architecture lease holder may integrate at a time. Simulation, gameplay protocol parsers, renderer resources, UI/audio, app composition, deployment and production asset work remain outside P1.

# P0 evidence barrier

Merged and separately archived:

- Canary: PR #140 / archive #150;
- legacy workflows/parity: PR #141 / archive #149;
- asset source/runtime: PR #142 / archive #148;
- Windows UX/input/audio: PR #143 / archive #147;
- staging/E2E/release: PR #144 / archive #146.

Exact base: `main@6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b`.

# Acceptance

- [x] matrix reflects accepted P0 evidence without promoting source inventory to deployed compatibility;
- [x] every major unknown is evidenced, narrowed or assigned a named blocker/owner decision;
- [x] release-required, later and owner-decision capabilities are explicit;
- [x] P1 names sole producers, exact paths, dependencies, shared-lease rules, validation and merge order;
- [x] four prompts comply with `PROMPTING_STANDARD.md`;
- [x] exactly the eight owned documentation paths change;
- [x] checkpoint contract/review and exact-head heavy validation pass;
- [ ] task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T22:08:00+02:00
head: b6dfea73115d5a3687f1444e8fa4d07cfb07050d
branch: docs/OTC2-20260801-playability-p0-aggregation
pr: 151
status: ready
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
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-aggregation.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_GAME_DOMAIN_CONTRACT_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_CANARY_SOURCE_INDEX_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_ASSET_PACK_RUNTIME_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_INPUT_ACTIONS_AGENT.md
proven:
  - All five P0 reports and separate lifecycle archives are merged.
  - Matrix separates source evidence, implementation state, deployment proof and owner decisions.
  - P1 has four disjoint exclusive package sets and one serialized shared integration lease.
  - Game-domain is the first gameplay public-contract producer.
  - Exact-head Rust Client and repository CI passed on b6dfea73115d5a3687f1444e8fa4d07cfb07050d.
derived:
  - Source-index may merge first because it publishes evidence and no workspace member.
  - Asset-runtime and input-actions may develop independently but integrate serially after previous archives.
  - Simulation, parsers, renderer resources, UI/audio and app composition require a post-P1 barrier.
unknown:
  - Exact deployed Canary cut, configuration and build.
  - Production asset source, local-import and redistribution approval.
  - Staging account/environment, Windows matrix, budgets, privacy and release policy.
conflicts:
  - Historical Canary cuts remain conflicting deployment evidence.
  - Server-declared optional features are not automatically release requirements.
first_failure:
  marker: none
  evidence: validation completed without ownership, checkpoint, review or CI failure.
rejected_hypotheses:
  - Start gameplay parsers in P1: rejected until game contracts and generated source index merge.
  - Combine UI, input and audio: rejected because they own distinct public contracts.
  - Treat synthetic assets as production-ready: rejected; P1 runtime is synthetic-v1 only.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-aggregation.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_GAME_DOMAIN_CONTRACT_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_CANARY_SOURCE_INDEX_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_ASSET_PACK_RUNTIME_AGENT.md
  - oteryn-client/docs/agents/prompts/P1_INPUT_ACTIONS_AGENT.md
validation:
  - command: checkpoint governance contract review
    result: PASS
    evidence: all required fields, allowed status/result values and compactness limits pass.
  - command: live P0 archive and open-PR ownership reconciliation
    result: PASS
    evidence: all five lanes archived; unrelated PRs 23, 48 and 97 own no aggregation path.
  - command: Prompting Standard quality gate and cross-document consistency review
    result: PASS
    evidence: four prompts match the accepted tasks, paths, order, validation and stop contracts.
  - command: exact changed-file and review gate
    result: PASS
    evidence: exactly eight owned paths; no comments, reviews or unresolved threads.
  - command: Rust Client run 30715795977
    result: PASS
    evidence: Windows job 91411028596 passed metadata, format, strict Clippy, tests and architecture; Supply Chain 91411028605 passed.
  - command: repository CI run 30715796054
    result: PASS
    evidence: CI Required job 91411148134 passed.
blockers: []
next_action: Run final exact-head CI on this checkpoint commit, mark PR 151 ready, merge and archive the barrier task.
```
