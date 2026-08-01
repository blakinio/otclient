---
task_id: OTC2-20260801-playability-p0-aggregation
status: active
agent: "P0 playability barrier coordinator"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0-aggregation
phase: implementation
branch: docs/OTC2-20260801-playability-p0-aggregation
base_branch: main
created: 2026-08-01T21:45:00+02:00
updated: 2026-08-01T21:45:00+02:00
last_verified_commit: "6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b"
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

# Scope

Documentation and coordination only. No Rust/C++/Lua/OTUI source, manifests, lockfiles, workflows, producer repositories, deployment, credential use, assets or shared catalogue paths.

# P0 evidence barrier

Merged and archived lanes:

- Canary: PR #140 / archive #150;
- legacy workflows/parity: PR #141 / archive #149;
- asset source/runtime: PR #142 / archive #148;
- Windows UX/input/audio: PR #143 / archive #147;
- staging/E2E/release: PR #144 / archive #146.

Current exact base: `main@6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b`.

# Acceptance

- [ ] matrix reflects accepted P0 evidence without promoting source inventory to deployed compatibility;
- [ ] every major unknown is evidenced, narrowed or assigned a named blocker/owner decision;
- [ ] release-required, later/deferred and owner-decision capabilities are explicit;
- [ ] P1 names sole producers, exact paths, dependencies, shared-lease rules, validation and merge order;
- [ ] four prompts comply with `PROMPTING_STANDARD.md`;
- [ ] exactly the eight owned documentation paths change;
- [ ] checkpoint validation, independent review and exact-head required CI pass;
- [ ] task is separately archived after merge.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T21:45:00+02:00
head: 6808d8a9dd5a24a29c5ac96fe35bb463fe4da34b
branch: docs/OTC2-20260801-playability-p0-aggregation
pr: null
status: implementing
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
  - All five P0 worker reports and separate lifecycle archives are merged.
  - P0 implementation_authorized remained false and no product implementation was introduced.
  - Exact inspected Canary cut is source-backed but deployment equality remains unproven.
  - Existing technical-login foundations remain green and unchanged.
derived:
  - GAME-DOMAIN-CONTRACT must be the first merged public gameplay producer.
  - ASSET-PACK-RUNTIME, CANARY-SOURCE-INDEX and INPUT-ACTIONS can proceed independently within exclusive paths, but shared integration leases serialize root metadata.
  - UI core, audio core, simulation and protocol gameplay consumers belong after this first contract-spine wave.
unknown:
  - Exact deployed Canary cut/configuration/build.
  - Production asset source/local-import/redistribution approval.
  - Approved staging environment/account, final Windows support matrix and product budgets.
conflicts:
  - Historical Canary cuts differ; no deployment claim may select one without owner/operations evidence.
  - Server-declared optional features are not automatically release requirements.
first_failure:
  marker: none
  evidence: barrier ownership preflight found no path conflict with open PRs #23, #48 or #97.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-aggregation.md
validation:
  - command: live P0 worker/archive and open-PR ownership reconciliation
    result: PASS
    evidence: all five lanes merged/archived; only unrelated open PRs #23, #48 and #97 remain.
blockers: []
next_action: Write the normalized matrix, dependency graph, bounded P1 wave and four worker prompts, then validate the exact documentation head.
```
