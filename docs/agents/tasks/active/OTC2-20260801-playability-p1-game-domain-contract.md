---
task_id: OTC2-20260801-playability-p1-game-domain-contract
status: validating
agent: "P1 game-domain contract worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-game-domain-contract
phase: final-restacked-validation
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
base_branch: main
created: 2026-08-01T22:26:00+02:00
updated: 2026-08-02T19:28:00+02:00
last_verified_commit: "d50c3026bb02f582cb59482a4818fdc97cfa9525"
required_base_commit: "bfa694c988e19b1af427e25c3f97bbac1f2800d7"
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
last_progress_at: 2026-08-02T19:28:00+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement the sole protocol-neutral game-domain public contract producer defined by `P1_GAME_DOMAIN_CONTRACT_AGENT.md`.

# Acceptance

- [x] canonical generation-scoped gameplay IDs/handles exist;
- [x] closed/versioned `GameEvent` and `GameCommand` envelopes cover only the minimum shared M2 spine;
- [x] external identifiers, text, counts, capacities, coordinates and resources are bounded and stale generations fail deterministically;
- [x] no Canary, socket, simulation, renderer, UI, platform or app dependency leaks into the public API;
- [x] package formatting, strict Clippy and focused tests passed on implementation head `d50c3026`;
- [x] owned-path and public API review passed;
- [ ] exact-head heavy gates pass after final restack;
- [x] independent coordinator audit has no open material finding;
- [ ] PR is merged and the task is separately archived.

## Delivery classification

This task is an intentionally partial P1 public-contract producer. Protocol gameplay producers, simulation/snapshots, renderer/UI consumers, app composition and real staging remain later waves.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-02T19:28:00+02:00
head: def6d60c66c82aec9b901bbb196d3fc4c1e10638
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
pr: 155
status: validating
phase: final-restacked-validation
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
  integration: root workspace member and minimal Cargo.lock entry are present; existing architecture category and game-domain -> foundation edge cover the package.
proven:
  - Canonical IDs/handles, bounded values, redacted text and closed V1 event/command envelopes are implemented with no external dependency.
  - Cargo.lock diff contains only the new local oteryn-game-domain package.
  - Exact implementation head d50c3026 passed Rust Client run 30758572871 and repository CI run 30758572912.
  - Windows job 91524949710 passed locked metadata, rustfmt, strict Clippy, all workspace tests and architecture validation; Supply Chain job 91524949688 passed.
  - Ready-for-review CI run 30758722450 and CI / Required job 91525459029 passed.
  - PR comments, submitted reviews and unresolved review threads were clean before closeout.
  - Temporary coordinator PR 174 is closed without merge with zero final changed files.
  - Exact main bfa694c9 was merged into the task branch by isolated run 30758891031, producing def6d60c.
derived:
  - One final synchronize-triggered exact-head gate is required after the restack checkpoint commit.
unknown:
  - Final exact-head gate outcome after this checkpoint commit.
conflicts: []
first_failure:
  marker: cargo metadata --locked
  evidence: run 30757811461 rejected a stale lockfile.
  repair: pinned Cargo 1.94.0 regenerated the lockfile; unrelated indirect movement was restored with Cargo.
rejected_hypotheses:
  - Publish Canary-specific or speculative future contracts: rejected by protocol-neutral minimum-spine ownership.
  - Hand-edit Cargo.lock or bypass branch protection: rejected.
  - Merge from a stale base: rejected; exact main bfa694c9 is now the second parent of def6d60c.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/crates/game-domain/**
validation:
  - command: Rust Client run 30758572871
    result: PASS
    evidence: Windows 91524949710 and Supply Chain 91524949688 passed.
  - command: repository CI runs 30758572912 and 30758722450
    result: PASS
    evidence: CI / Required jobs 91525092757 and 91525459029 passed.
  - command: exact changed-path, public API, trust-boundary and review audit
    result: PASS
    evidence: fourteen authorized paths, minimal lockfile diff, no material finding or unresolved review state.
  - command: temporary exact-main restack run 30758891031
    result: PASS
    evidence: main bfa694c9 merged into task head def6d60c; harness removed and PR 174 closed with empty final diff.
blockers: []
next_action: Inspect Rust Client and repository CI on the new checkpoint head, mark ready, allow required ready-for-review CI to pass, then auto-merge and archive the task separately.
```
