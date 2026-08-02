---
task_id: OTC2-20260801-playability-p1-asset-pack-runtime
status: validating
agent: "P1 asset pack runtime worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-asset-pack-runtime
phase: exact-head-validation
branch: feat/OTC2-20260801-playability-p1-asset-pack-runtime
base_branch: main
created: 2026-08-01T22:27:00+02:00
updated: 2026-08-02T21:29:00+02:00
last_verified_commit: "516e9aa129e335691c312e7be88c4229f894cfaf"
required_base_commit: "fbbff443dc64f39ca6fa39c7ddefc9fef2d1ac3c"
risk: high
related_pr: 156
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
  - oteryn-client/crates/asset-runtime/**
shared_path_lease:
  holder: OTC2-20260801-playability-p1-asset-pack-runtime
  granted_at: 2026-08-02T21:12:00+02:00
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
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - asset decoding and renderer upload
  - production asset source/import/signing decisions
  - app composition and pack activation
invocation_started_at: 2026-08-02T21:12:00+02:00
last_progress_at: 2026-08-02T21:29:00+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement the immutable synthetic-v1 asset pack open/verify/index/lookup runtime defined by `P1_ASSET_PACK_RUNTIME_AGENT.md`.

# Acceptance

- [x] runtime accepts only bytes or an already-opened `Read` object and exposes no path API;
- [x] producer schema verifies magic/version/counts/text/dimensions/payload lengths/per-record SHA-256/canonical order/full consumption;
- [x] runtime limits only narrow producer schema bounds;
- [x] immutable canonical index and generation-fenced logical handles exist;
- [x] malformed, truncated, trailing, duplicate, oversized, digest-corrupt, unsupported-version and stale-generation cases fail closed;
- [x] no decode/GPU/import/signing/rights/app activation work entered the crate;
- [x] pinned package rustfmt, strict Clippy and focused tests pass;
- [x] deterministic existing-compiler -> runtime component round trip passes;
- [ ] exact-head heavy gates pass after serialized workspace integration;
- [x] independent API/trust-boundary/lockfile audit has no open material finding;
- [ ] PR is merged and the task is separately archived.

## Trust boundary and schema decisions

- Acquisition remains caller-owned. `AssetRuntime` receives a complete byte slice or an already-opened reader and never receives a filesystem path.
- The sole producer format is project-original `OTASSET1` schema version 1 from `oteryn-asset-types`.
- Schema v1 declares one SHA-256 digest per inline payload. It has no whole-pack digest, signature or caller-controlled offset table.
- Inline records are consumed through one monotonic decoder cursor, so overlapping caller ranges are not representable; malformed, partial and trailing data fail through the producer decoder.
- `AssetPack::decode` remains the sole schema parser. The runtime adds only runtime limits, immutable indexing, generation fencing and bounded lookup.
- Runtime/view Debug output omits metadata text and payload bytes.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-02T21:29:00+02:00
head: 516e9aa129e335691c312e7be88c4229f894cfaf
branch: feat/OTC2-20260801-playability-p1-asset-pack-runtime
pr: 156
status: validating
phase: exact-head-validation
context_routes:
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
  - docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
  - docs/agents/GITHUB_ONLY_EXECUTION.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/WAVE_P1_CONTRACT_SPINE.md
  - oteryn-client/docs/agents/prompts/P1_ASSET_PACK_RUNTIME_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
  - oteryn-client/crates/asset-runtime/**
shared_lease:
  state: granted
  reason: game-domain and its lifecycle archive are merged; PR 157 remains disjoint and no competing shared holder exists.
  integration: exact main fbbff443 is in branch history; workspace member and minimal local lockfile package are present; existing architecture category and asset-runtime -> asset-types/tool-dev edges cover the crate.
proven:
  - AssetRuntime opens bytes or an already-opened reader, fully delegates schema verification to asset-types and owns no arbitrary path traversal.
  - RuntimeLimits narrow pack/record/payload bounds; immutable binary-search index and generation-fenced handles reject stale or unknown lookups.
  - Focused negative corpus and debug-redaction tests pass.
  - Cargo.lock diff contains only local oteryn-asset-runtime with asset-types and test-only asset-compiler dependencies.
  - Temporary integration/component PR 176 is closed without merge with zero final changed files.
  - Pinned focused run 30763307527 job 91537593375 passed rustfmt, strict package Clippy and package tests.
  - Component run 30763398001 job 91537833564 passed deterministic compiler output, runtime open/index/lookup, package tests and strict Clippy.
derived:
  - No architecture checker or fixture mutation is required because the accepted category and dependency edges already exist.
  - A task-record commit is required to trigger retained PR workflows after GITHUB_TOKEN worker pushes.
unknown:
  - Locked workspace metadata, full workspace Clippy/tests, architecture, supply-chain and repository required CI outcome on the checkpoint head.
conflicts: []
first_failure:
  marker: focused test compilation
  evidence: Result assertions required PartialEq on AssetRuntime/AssetView instead of comparing stable errors.
  causal_hypothesis: test assertions accidentally compared complete Result values.
  repair: compare `Result::err()` only; package and component validation now pass.
rejected_hypotheses:
  - Add production schema, signatures, whole-pack hash or rights policy: rejected as later owner scope.
  - Duplicate schema-v1 parser in asset-runtime: rejected; asset-types remains the sole format validator.
  - Add offset/overlap errors to a sequential inline format: rejected as speculative and unrepresentable in schema v1.
  - Expose filesystem path opening: rejected by the capability boundary.
  - Keep incidental transitive lockfile upgrades: rejected; Cargo 1.94 restored ipnet 2.12.0 and libredox 0.1.18.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/crates/asset-runtime/**
validation:
  - command: live main, PR and ownership reconciliation
    result: PASS
    evidence: main fbbff443; game-domain merged/archived; PR 157 disjoint; serialized lease valid.
  - command: producer schema and architecture policy review
    result: PASS
    evidence: asset-types is the sole decoder; asset-runtime category and normal/dev edges already exist.
  - command: focused package run 30763307527 / job 91537593375
    result: PASS
    evidence: pinned rustfmt, strict package Clippy and all package tests passed.
  - command: component run 30763398001 / job 91537833564
    result: PASS
    evidence: two compiler outputs were byte-identical and opened/indexed identically; strict Clippy/tests passed.
  - command: exact changed-path, public API, trust-boundary and lockfile audit
    result: PASS
    evidence: eight authorized paths; no producer edits; minimal local lockfile graph; temporary PR 176 closed empty.
blockers: []
next_action: Inspect retained Rust Client and repository CI on this checkpoint head, isolate one actionable failure if present, otherwise mark ready, auto-merge and archive separately.
```
