---
task_id: OTC2-20260801-playability-p1-game-domain-contract
status: validating
agent: "P1 game-domain contract worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-game-domain-contract
phase: exact-head-validation
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
base_branch: main
created: 2026-08-01T22:26:00+02:00
updated: 2026-08-02T19:13:27+02:00
last_verified_commit: "39d6cbb33ef217e8d867784a18d968aadcc7cbde"
required_base_commit: "55fec043758e1928fd5d39831322a0c21f47589b"
risk: high
related_pr: 155
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
  - oteryn-client/crates/game-domain/**
shared_path_lease:
  holder: OTC2-20260801-playability-p1-game-domain-contract
  granted_at: 2026-08-02T18:46:01+02:00
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
    - oteryn-client/tools/architecture-check/**
    - oteryn-client/tests/architecture-fixtures/**
    - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
    - oteryn-client/docs/operations/RUST_WORKSPACE.md
  release_condition: exact-head integration validation and merge or explicit rollback
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: github-only
context_pressure: high
decomposition_decision: single
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - protocol-canary gameplay producers
  - simulation and snapshots
  - renderer and UI consumers
  - app composition and real staging E2E
invocation_started_at: 2026-08-02T18:37:00+02:00
last_progress_at: 2026-08-02T19:13:27+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement the sole protocol-neutral game-domain public contract producer defined by `P1_GAME_DOMAIN_CONTRACT_AGENT.md`.

# Acceptance

- [x] canonical generation-scoped gameplay IDs/handles exist;
- [x] closed/versioned `GameEvent` and `GameCommand` envelopes cover only the minimum shared M2 spine;
- [x] external identifiers, text, counts, capacities, coordinates and resources are bounded and stale generations fail deterministically by construction and focused negative tests;
- [x] no Canary, socket, simulation, renderer, UI, platform or app dependency leaks into the public API;
- [ ] package formatting, strict Clippy and focused tests pass;
- [x] owned-path and public API review passed before the serialized shared lease;
- [ ] exact-head heavy gates pass after workspace integration;
- [ ] independent audit has no open material findings;
- [ ] PR is merged and the task is separately archived.

## Delivery classification

This task is an intentionally partial public-contract producer. It does not claim a playable user-facing feature. The missing producer/consumer layers remain assigned to later waves in `WAVE_P1_CONTRACT_SPINE.md` and the programme charter.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-02T19:13:27+02:00
head: 39d6cbb33ef217e8d867784a18d968aadcc7cbde
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
pr: 155
status: validating
phase: exact-head-validation
context_routes:
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/GITHUB_ONLY_EXECUTION.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_GAME_DOMAIN_CONTRACT_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
  - oteryn-client/crates/game-domain/**
shared_lease:
  state: granted
  reason: game-domain is the first accepted P1 runtime producer; PRs 154, 156 and 157 still modify only their exclusive task paths and no competing shared lease exists.
  integration: root workspace member and Cargo.lock are present; existing architecture category and game-domain -> foundation edge already covered the package, so no checker or fixture mutation was required.
proven:
  - P1 aggregation/archive authorize this sole public contract producer.
  - The crate reuses foundation SessionGeneration and introduces no external dependency.
  - Canonical IDs/handles, bounded values, redacted text and closed V1 event/command envelopes are implemented.
  - Full PR diff review showed only owned paths before the serialized shared lease.
  - Open P1 worker PRs 154, 156 and 157 have no shared workspace changes.
  - Cargo 1.94.0 regenerated only oteryn-client/Cargo.lock through temporary coordinator PR 174.
  - Temporary workflow was removed and PR 174 was closed without merge; its final diff is empty.
derived:
  - A task-record commit after lockfile generation is required to trigger retained pull-request workflows because GITHUB_TOKEN pushes do not recursively trigger Actions.
unknown:
  - Compiler, formatting, strict Clippy, tests, architecture and supply-chain outcome on the new exact head.
conflicts: []
first_failure:
  marker: cargo metadata --locked
  evidence: retained Rust Client run 30757811461 rejected the stale lockfile before compilation.
  causal_hypothesis: adding the workspace member without regenerating Cargo.lock left the package graph incomplete.
  repair: pinned Cargo 1.94.0 generated and committed only Cargo.lock at 39d6cbb33ef217e8d867784a18d968aadcc7cbde.
rejected_hypotheses:
  - Publish Canary-specific wire types: rejected by protocol-neutral ownership.
  - Add speculative economy, social, UI, renderer or simulation variants: rejected as outside the minimum P1 spine.
  - Hand-edit Cargo.lock: rejected because the task requires regeneration with pinned Cargo.
  - Retain or merge the temporary workflow: rejected; PR 174 was terminally closed with an empty final diff.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/crates/game-domain/**
validation:
  - command: live PR ownership and changed-path review
    result: PASS
    evidence: PR 155 owns the task, game-domain and serialized workspace integration; PRs 154, 156 and 157 remain exclusive.
  - command: independent static public API and trust-boundary review
    result: PASS
    evidence: no protocol/socket/simulation/renderer/UI/platform/app types; external text Debug is redacted and stable errors contain lengths/generations only.
  - command: cargo generate-lockfile with Rust/Cargo 1.94.0
    result: PASS
    evidence: temporary run 30758334844; committed lockfile head 39d6cbb33ef217e8d867784a18d968aadcc7cbde; harness removed and PR 174 closed without merge.
blockers: []
next_action: Inspect retained Rust Client and CI workflows on the exact task-record head, isolate the first actionable failure, and apply one targeted repair or proceed to audit when green.
```
