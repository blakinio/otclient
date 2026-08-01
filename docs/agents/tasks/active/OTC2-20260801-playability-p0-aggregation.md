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
updated: 2026-08-01T21:58:00+02:00
last_verified_commit: "dea7f0233d6f558e17ad105946493ad80f2d7603"
required_base_commit: "6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b"
risk: medium
related_pr: null
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

The barrier accepted a four-package P1 contract spine:

1. `CANARY-SOURCE-INDEX` — exact deterministic source/fixture evidence, no runtime public types;
2. `GAME-DOMAIN-CONTRACT` — sole gameplay IDs/handles and closed `GameEvent`/`GameCommand` producer;
3. `ASSET-PACK-RUNTIME` — immutable synthetic-v1 pack open/verify/index/lookup and logical handles;
4. `INPUT-ACTIONS` — normalized physical events and semantic action/context producer.

Integration order is serialized exactly as listed. Only one shared workspace/lockfile/architecture lease holder may integrate at a time. Simulation, protocol gameplay parsers, UI/audio, renderer resources and app composition remain outside P1.

# P0 evidence barrier

Merged and archived lanes:

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
- [ ] checkpoint validation, independent review and exact-head required CI pass;
- [ ] task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T21:58:00+02:00
head: dea7f0233d6f558e17ad105946493ad80f2d7603
branch: docs/OTC2-20260801-playability-p0-aggregation
pr: null
status: validating
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P0_DISCOVERY.md
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
  - P0 introduced no product implementation and retained exact evidence boundaries.
  - Matrix now classifies release-required, later and owner-decision capabilities.
  - P1 owns four disjoint exclusive package sets and one serialized shared integration lease.
  - Game-domain is the first gameplay public-contract producer.
derived:
  - Source-index may merge first because it publishes evidence and no workspace member.
  - Asset-runtime and input-actions may develop independently but integrate only after previous shared-lease archive.
  - Simulation/snapshot, protocol parsers, renderer resources, UI/audio and app composition require a post-P1 barrier.
unknown:
  - Exact deployed Canary cut/configuration/build.
  - Production asset source/local-import/redistribution approval.
  - Approved staging environment/account, final Windows support matrix, performance budgets, telemetry and release policy.
conflicts:
  - Historical Canary cuts remain conflicting deployment evidence; the inspected cut is not promoted to deployment truth.
  - Server-declared optional features remain later unless product scope explicitly promotes them.
first_failure:
  marker: none
  evidence: all owned documents were created/updated without path conflict.
rejected_hypotheses:
  - Start map/parser implementation in P1: rejected because shared game contracts and generated exact-source index must merge first.
  - Combine UI, input and audio into one producer: rejected because each owns a distinct public contract and UI/audio dependencies remain later.
  - Treat synthetic asset schema as production-ready: rejected; P1 runtime claim remains synthetic-v1 only.
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
  - command: live P0 worker/archive and open-PR ownership reconciliation
    result: PASS
    evidence: all five lanes merged/archived; unrelated #23/#48/#97 own no aggregation/P1 path.
  - command: evidence normalization review
    result: PASS
    evidence: source evidence, implementation state, deployment proof and owner decisions remain distinct.
  - command: Prompting Standard quality gate
    result: PASS
    evidence: each prompt has one role/objective, exact ownership, policy v2, staged validation, checkpoint and stop/final contracts.
  - command: changed-path compare against main@6808d8a9
    result: PASS
    evidence: exactly eight declared documentation paths.
blockers: []
next_action: Open the draft aggregation PR, run exact-head review/checkpoint/CI, then merge and archive the barrier task.
```
