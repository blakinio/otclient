---
task_id: OTC2-20260803-playability-p1-aggregation
status: active
agent: "P1 playability barrier coordinator"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-aggregation
phase: evidence-reconciliation
branch: docs/OTC2-20260803-playability-p1-aggregation
base_branch: main
created: 2026-08-03T01:08:02+02:00
updated: 2026-08-03T01:08:02+02:00
required_base_commit: "5d3dec1037eef508782e369afef8e3b7f1291e6a"
risk: high
related_pr: null
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p1-aggregation.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P2_MINIMUM_VISIBLE_WORLD.md
  - oteryn-client/docs/agents/prompts/P2_SIMULATION_SNAPSHOT_AGENT.md
  - oteryn-client/docs/agents/prompts/P2_CANARY_WORLD_PROTOCOL_AGENT.md
  - oteryn-client/docs/agents/prompts/P2_ASSET_DECODE_AGENT.md
  - oteryn-client/docs/agents/prompts/P2_RENDERER_RESOURCE_AGENT.md
  - oteryn-client/docs/agents/prompts/P2_INPUT_PLATFORM_AGENT.md
  - oteryn-client/docs/agents/prompts/P2_VISIBLE_WORLD_INTEGRATION_AGENT.md
shared_path_lease: []
implementation_authorized: false
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: discovery
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
decomposition_decision: single
validation_level: heavy
complete_user_facing_feature: false
invocation_started_at: 2026-08-03T01:08:02+02:00
last_progress_at: 2026-08-03T01:08:02+02:00
ci_checks_for_current_head: 0
ci_check_generation: none
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Aggregate the four merged and separately archived P1 contract-spine packages, update the live architecture/capability/dependency state, and publish the smallest safe staged P2 minimum-visible-world wave with sole producers, exact ownership, integration order, validation and closeout contracts.

# Barrier evidence

Merged and separately archived on exact base `main@5d3dec1037eef508782e369afef8e3b7f1291e6a`:

- Canary source index: implementation PR #154 / merge `67f8af3f5cd4abff53456e207fc374afd1add030`; archive PR #180 / merge `c911e0f6fa7ad6e8824dd5e0e44e154abbbdcbc1`;
- game-domain contracts: implementation PR #155 / merge `41a37e34660e2f0d6d2f41f0b480d2c5c9c5aa8a`; archive PR #175 / merge `fbbff443dc64f39ca6fa39c7ddefc9fef2d1ac3c`;
- asset pack runtime: implementation PR #156 / merge `e8c3eb6c3b5993a0ce3e62c1506c719d8ee8dc5e`; archive PR #177 / merge `3887a0b7369e99ad200990d42a5314f1d5531e97`;
- input actions: implementation PR #157 / merge `6ca0882101b5a563775532e0684941f10bcbd8e3`; archive PR #183 / merge `5d3dec1037eef508782e369afef8e3b7f1291e6a`.

All P1 shared integration leases are released. Open PRs #23, #48 and #97 own no barrier path.

# Acceptance

- [ ] live architecture handoff includes all four merged P1 producers and their exact boundaries;
- [ ] capability matrix moves only evidence-backed P1 rows and keeps deployment/production claims bounded;
- [ ] dependency model replaces the completed P1 graph with an accepted staged P2 graph;
- [ ] P2 preserves one simulation/snapshot producer, one gameplay protocol adapter, one asset decoder, one renderer-resource producer, one platform input adapter and one serialized vertical-slice integration owner;
- [ ] worker packages have non-overlapping exclusive paths and an explicit shared integration lease order;
- [ ] P2 completion remains the real M2 journey: controlled login -> visible world -> semantic movement -> server reconciliation -> safe logout;
- [ ] no P2 worker may claim real compatibility without exact source/fixture/staging evidence;
- [ ] all worker prompts satisfy Prompting Standard 2.1 and cannot weaken acceptance;
- [ ] exact changed-path, link/content, review and heavy CI gates pass;
- [ ] barrier PR merges and the task is separately archived before worker launch.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-03T01:08:02+02:00
head: pending_first_commit
branch: docs/OTC2-20260803-playability-p1-aggregation
pr: null
status: active
phase: evidence-reconciliation
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
proven:
  - All four P1 implementations and separate archives are merged.
  - Game-domain owns canonical gameplay IDs and the closed v1 GameEvent/GameCommand envelope.
  - Canary source-index publishes deterministic exact-source evidence without runtime compatibility claims.
  - Asset-runtime owns immutable verified synthetic-v1 pack lookup and generation-stable handles.
  - Input-actions owns framework-neutral physical and semantic input contracts.
  - No P1 shared lease remains active.
derived:
  - P2 may consume the merged contracts but may not publish substitutes.
  - M2 requires staged producers plus one later serialized app-composition/E2E owner; green producer crates alone are insufficient.
unknown:
  - exact deployed Canary revision/configuration/build and controlled gameplay fixtures;
  - approved production asset source/import/redistribution and appearance representation;
  - approved staging environment/account and final Windows/performance budgets.
conflicts: []
changed_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p1-aggregation.md
validation:
  - command: live P1 implementation/archive/open-PR reconciliation
    result: PASS
    evidence: exact merges listed above; open PRs #23/#48/#97 do not overlap owned paths.
blockers: []
next_action: Reconcile merged public APIs and current capability rows, then define the smallest staged P2 ownership graph and write its wave contract and worker prompts.
```
