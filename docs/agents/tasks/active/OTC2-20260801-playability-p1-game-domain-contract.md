---
task_id: OTC2-20260801-playability-p1-game-domain-contract
status: implementing
agent: "P1 game-domain contract worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-game-domain-contract
phase: workspace-integration
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
base_branch: main
created: 2026-08-01T22:26:00+02:00
updated: 2026-08-02T18:46:01+02:00
last_verified_commit: "6a952480dccbb7af2042302a9479cdf8caa76c61"
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
last_progress_at: 2026-08-02T18:46:01+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
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
updated_at: 2026-08-02T18:46:01+02:00
head: 6a952480dccbb7af2042302a9479cdf8caa76c61
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
pr: 155
status: implementing
phase: workspace-integration
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
  reason: game-domain is first accepted P1 runtime producer; PRs 154, 156 and 157 still modify only their exclusive task paths and no competing shared lease exists.
  github_only_validation_note: existing Rust Client workflow validates only root workspace members, so the serialized lease is required to obtain real package and component evidence without adding an unauthorized temporary workflow.
proven:
  - P1 aggregation/archive authorize this sole public contract producer.
  - The crate reuses foundation SessionGeneration and introduces no external dependency.
  - Canonical IDs/handles, bounded values, redacted text and closed V1 event/command envelopes are implemented.
  - Full PR diff review shows only the task and exclusive crate paths before lease grant.
  - Open P1 worker PRs 154, 156 and 157 have no shared workspace changes.
derived:
  - Root workspace integration is the smallest permitted GitHub-only route to real fmt, Clippy, test and architecture evidence.
unknown:
  - Compiler and strict Clippy outcome until the integrated branch runs GitHub Actions.
conflicts: []
first_failure:
  marker: none
  evidence: no execution failure yet; pre-integration static review passed.
rejected_hypotheses:
  - Publish Canary-specific wire types: rejected by protocol-neutral ownership.
  - Add speculative economy, social, UI, renderer or simulation variants: rejected as outside the minimum P1 spine.
  - Add a temporary workflow: rejected because existing retained workflows can validate after the authorized serialized workspace integration.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-game-domain-contract.md
  - oteryn-client/crates/game-domain/**
validation:
  - command: live PR ownership and changed-path review
    result: PASS
    evidence: PR 155 owns only task plus crates/game-domain; PRs 154, 156 and 157 own only their task paths.
  - command: independent static public API and trust-boundary review
    result: PASS
    evidence: no protocol/socket/simulation/renderer/UI/platform/app types; external text Debug is redacted and stable errors contain lengths/generations only.
blockers: []
next_action: Restack PR 155 on exact main bfa694c9, add the leased workspace and architecture integration, then inspect the first exact-head Rust Client CI result.
```
