---
task_id: OTC2-20260801-playability-p1-game-domain-contract
status: completed
agent: "P1 game-domain contract worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-game-domain-contract
phase: archived
branch: feat/OTC2-20260801-playability-p1-game-domain-contract
base_branch: main
created: 2026-08-01T22:26:00+02:00
completed: 2026-08-02T19:33:21+02:00
archived: 2026-08-02T19:34:00+02:00
implementation_head: "52fb1f0d18dea35fb693a20992592c5a3e0b6759"
required_base_commit: "bfa694c988e19b1af427e25c3f97bbac1f2800d7"
merge_commit: "41a37e34660e2f0d6d2f41f0b480d2c5c9c5aa8a"
risk: high
related_pr: 155
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: github-only
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - protocol-canary gameplay producers
  - simulation and snapshots
  - renderer and UI consumers
  - app composition and real staging E2E
shared_path_lease:
  state: released
  released_by_merge: "41a37e34660e2f0d6d2f41f0b480d2c5c9c5aa8a"
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
    - oteryn-client/tools/architecture-check/**
    - oteryn-client/tests/architecture-fixtures/**
    - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
    - oteryn-client/docs/operations/RUST_WORKSPACE.md
---

# Goal

Implement the sole protocol-neutral P1 game-domain public-contract producer.

# Final acceptance

- [x] canonical generation-scoped gameplay IDs and handles exist;
- [x] closed/versioned `GameEvent` and `GameCommand` envelopes cover the minimum shared M2 spine;
- [x] external identifiers, text, counts, capacities, coordinates and resources are bounded and stale generations fail deterministically;
- [x] no Canary, socket, simulation, renderer, UI, platform or app dependency leaks into the public API;
- [x] locked metadata, pinned rustfmt, strict Clippy, complete workspace tests and architecture policy pass on the final restacked head;
- [x] supply-chain advisories, licenses, bans and sources pass;
- [x] exact changed-path, minimal lockfile, public API, trust-boundary and review audits have no open material finding;
- [x] implementation PR #155 merged through protected auto-merge;
- [x] serialized shared-path lease is released;
- [x] lifecycle record moved from `active` to `archive` in a separate closeout PR.

## Delivery classification

The delivered crate is an intentionally partial public-contract producer, not a complete playable user-facing feature. The remaining gameplay producer and consumer layers stay assigned to later playability waves.

## Final evidence

```yaml
implementation:
  pr: 155
  head: 52fb1f0d18dea35fb693a20992592c5a3e0b6759
  exact_base: bfa694c988e19b1af427e25c3f97bbac1f2800d7
  merge: 41a37e34660e2f0d6d2f41f0b480d2c5c9c5aa8a
validation:
  rust_client:
    run: 30758941404
    windows_job: 91525927591
    supply_chain_job: 91525927551
    result: PASS
  repository_ci:
    run: 30758941532
    required_job: 91526031004
    result: PASS
  ready_for_review_ci:
    run: 30759083301
    required_job: 91526401752
    result: PASS
  coordinator_audit:
    changed_paths: 14 authorized implementation and lifecycle paths
    cargo_lock: only local oteryn-game-domain package added
    comments_reviews_threads: clean
    material_findings: none
remote_execution_cleanup:
  temporary_pr: 174
  state: closed_without_merge
  final_changed_files: 0
blockers: []
next_action: Coordinator may grant the next serialized shared integration lease to P1 asset-pack-runtime PR #156 after this archive PR merges and current main is re-read.
```
