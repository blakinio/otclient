---
task_id: OTC2-20260803-playability-p1-aggregation
status: validating
agent: "P1 playability barrier coordinator"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-aggregation
phase: final-exact-head-ci
branch: docs/OTC2-20260803-playability-p1-aggregation
base_branch: main
created: 2026-08-03T01:08:02+02:00
updated: 2026-08-03T01:23:00+02:00
last_verified_commit: "24fd7eec38603bf9522eb04902fbdc0fec214e39"
required_base_commit: "5d3dec1037eef508782e369afef8e3b7f1291e6a"
risk: high
related_pr: 184
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
  - oteryn-client/docs/agents/prompts/P2_CONTROLLED_M2_ACCEPTANCE_AGENT.md
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
last_progress_at: 2026-08-03T01:23:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-exact-head
terminal_ci_wait_started_at: 2026-08-03T01:23:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
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

# Material aggregation finding

The generated P1 Canary source index is pinned to `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`, while the existing `protocol-canary` runtime descriptor still names `95b276db311cf6e9acd58b847f1fb0ca6697b137` and accepted source cut `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`.

Disposition:

- this is a development-baseline conflict, not proof of deployed incompatibility;
- P2 CANARY-WORLD-PROTOCOL must first align runtime metadata/tests mechanically with the generated `current-index.json` and exact source hashes;
- production admission remains fail-closed;
- the inspected source cut is not treated as the deployed cut without named controlled evidence;
- field layouts not established by provenance-safe evidence remain explicit `UNKNOWN` and may not be guessed.

# Acceptance

- [x] live architecture handoff includes all four merged P1 producers and their exact boundaries;
- [x] capability matrix moves only evidence-backed P1 rows and keeps deployment/production claims bounded;
- [x] dependency model replaces the completed P1 graph with an accepted staged P2 graph;
- [x] P2 preserves one simulation/snapshot producer, one gameplay protocol adapter, one asset decoder, one renderer-resource producer, one platform input adapter and one serialized vertical-slice integration owner;
- [x] controlled M2 acceptance is a separate owner and cannot be replaced by synthetic composition;
- [x] worker packages have non-overlapping exclusive paths and an explicit shared integration lease order;
- [x] P2 completion remains the real M2 journey: controlled login -> visible world -> semantic movement -> server reconciliation -> safe logout;
- [x] no P2 worker may claim real compatibility without exact source/fixture/staging evidence;
- [x] all seven worker/acceptance prompts satisfy Prompting Standard 2.1 and cannot weaken acceptance;
- [x] exact changed-path and content audit passes with twelve authorized documentation paths and no retained workflow;
- [ ] final exact-head Rust Client and repository CI pass;
- [ ] review/comments/threads remain clean, barrier PR merges and the task is separately archived before worker launch.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-03T01:23:00+02:00
content_reviewed_head: 24fd7eec38603bf9522eb04902fbdc0fec214e39
branch: docs/OTC2-20260803-playability-p1-aggregation
pr: 184
status: validating
phase: final-exact-head-ci
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P2_MINIMUM_VISIBLE_WORLD.md
proven:
  - All four P1 implementations and separate archives are merged and all P1 shared leases are released.
  - Game-domain owns canonical gameplay IDs and the closed v1 GameEvent/GameCommand envelope.
  - Canary source-index publishes deterministic exact-source evidence without runtime/deployment compatibility claims.
  - Asset-runtime owns immutable verified synthetic-v1 pack lookup and generation-stable handles.
  - Input-actions owns framework-neutral physical and semantic input contracts.
  - P2 is staged as SIMULATION-SNAPSHOT, CANARY-WORLD-PROTOCOL, ASSET-DECODE, RENDERER-RESOURCE, INPUT-PLATFORM, VISIBLE-WORLD-INTEGRATION and CONTROLLED-M2-ACCEPTANCE.
  - Final PR diff contains exactly twelve owned documentation paths and no temporary workflow.
derived:
  - Initial safe P2 implementation concurrency is simulation, Canary protocol, asset decode and input platform, with serialized shared integration.
  - Renderer-resource follows asset-decode; visible-world integration follows all five producer archives.
  - Synthetic visible-world integration is a partial consumer and cannot establish M2.
unknown:
  - exact deployed Canary revision/configuration/build and controlled gameplay fixtures;
  - approved production asset source/import/redistribution and appearance representation;
  - approved staging environment/account and final Windows/performance/privacy budgets.
conflicts:
  - id: P1-AGG-CANARY-REVISION-001
    inspected_index: bc0068ab80bbf003e128fce0589b4cc89d2682d3
    runtime_descriptor: 95b276db311cf6e9acd58b847f1fb0ca6697b137
    historical_accepted_cut: 4b2d6f432d92628c42bde1d95daed6ae0d0eb88f
    disposition: bounded_P2_baseline_alignment_before_gameplay_parser
changed_paths:
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
  - oteryn-client/docs/agents/prompts/P2_CONTROLLED_M2_ACCEPTANCE_AGENT.md
validation:
  - command: live P1 implementation/archive/open-PR reconciliation
    result: PASS
    evidence: exact merges listed above; open PRs #23/#48/#97 do not overlap owned paths.
  - command: assertion-guarded living-contract patch
    result: PASS
    evidence: temporary trigger run 30772041402; first run 30772003133 failed only on new Markdown trailing whitespace and was causally repaired before commit.
  - command: exact changed-path and retained-workflow review
    result: PASS
    evidence: PR #184 has twelve authorized documentation paths, zero workflows, additions 1644 and deletions 145 on content-reviewed head.
  - command: architecture/capability/dependency/wave/prompt content audit
    result: PASS
    evidence: sole producers, claim boundaries, launch dependencies, shared lease order and controlled M2 gate are mutually consistent; zero open material content finding.
blockers: []
next_action: Run final exact-head Rust Client and repository CI, recheck clean reviews and current main, then mark PR ready, protected-merge, create the separate lifecycle archive and only after that launch the first safe P2 producer task.
```
