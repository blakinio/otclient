---
task_id: OTC2-20260801-playability-p1-asset-pack-runtime
status: validating
agent: "P1 asset pack runtime worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-asset-pack-runtime
phase: integration-and-validation
branch: feat/OTC2-20260801-playability-p1-asset-pack-runtime
base_branch: main
created: 2026-08-01T22:27:00+02:00
updated: 2026-08-02T21:12:00+02:00
last_verified_commit: "330fe1a5bc6d814883be4e4b5bd3c1e31983ca9b"
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
last_progress_at: 2026-08-02T21:12:00+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement the immutable synthetic-v1 asset pack open/verify/index/lookup runtime defined by `P1_ASSET_PACK_RUNTIME_AGENT.md`.

# Acceptance

- [x] runtime accepts only bytes or an already-opened `Read` object and exposes no path API;
- [x] schema-v1 decoding verifies magic/version/counts/text/dimensions/payload lengths/per-record SHA-256/canonical order/full consumption;
- [x] configured pack/record/payload limits may only narrow producer schema bounds;
- [x] immutable canonical index and generation-fenced logical handles exist;
- [x] malformed, truncated, trailing, duplicate, oversized, digest-corrupt, unsupported-version and stale-generation cases have focused tests;
- [x] no decode/GPU/import/signing/rights/app activation work entered the crate;
- [ ] package formatting, strict Clippy and focused tests pass;
- [ ] exact-head heavy gates pass after serialized workspace integration;
- [ ] independent audit has no open material findings;
- [ ] PR is merged and the task is separately archived.

## Trust boundary and schema decisions

- Acquisition remains caller-owned. `AssetRuntime` receives a complete byte slice or an already-opened reader and never receives a filesystem path.
- The current producer format is the project-original `OTASSET1` schema version 1 from `oteryn-asset-types`.
- Schema v1 declares one SHA-256 digest per inline payload. It does not declare a separate whole-pack digest, signature or caller-controlled offset table.
- Records and payloads are encoded inline through a monotonic decoder cursor. Caller-controlled overlapping ranges are therefore not representable in schema v1; malformed/truncated/trailing input fails through the producer decoder rather than a speculative offset-table error.
- The runtime reuses `AssetPack::decode` as the sole schema validator and adds only runtime-specific limits, immutable indexing and generation fencing.
- Debug output for runtime/view objects reports only generation, IDs, kinds and byte counts; metadata text and payload bytes are not emitted.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-02T21:12:00+02:00
head: 330fe1a5bc6d814883be4e4b5bd3c1e31983ca9b
branch: feat/OTC2-20260801-playability-p1-asset-pack-runtime
pr: 156
status: validating
phase: integration-and-validation
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
  reason: game-domain implementation PR 155 and archive PR 175 are merged; PR 157 remains exclusive to input-actions/task paths and no competing shared lease exists.
  expected_integration: add one workspace member and one local lockfile package; existing architecture category and asset-runtime -> asset-types edge already permit the crate.
proven:
  - Current main is fbbff443dc64f39ca6fa39c7ddefc9fef2d1ac3c.
  - PR 156 initially owned only its task path; asset-runtime crate paths were absent on main.
  - Open PR 157 owns only input-actions/task paths and does not hold shared integration paths.
  - Current asset-types schema bounds pack size, record count, payload size, text, dimensions, canonical order and per-payload SHA-256.
  - Architecture policy already knows category asset-runtime and permits its normal dependency on asset-types.
  - Exclusive crate implementation introduces no dependency except the read-only asset-types producer.
derived:
  - No architecture checker or fixture change is required unless real validation disproves the existing policy.
  - One deterministic remote integration run is required to restack, add the workspace member, regenerate Cargo.lock with Cargo 1.94 and apply pinned rustfmt.
unknown:
  - Compiler, strict Clippy, tests, architecture and supply-chain outcome on the integrated head.
conflicts: []
first_failure:
  marker: static test review before CI
  evidence: error assertions compared Result values whose success types intentionally do not implement PartialEq.
  causal_hypothesis: assertions should compare only `Result::err()` instead of adding artificial equality semantics to runtime/view objects.
  repair: scheduled in the deterministic integration run before first retained heavy gate.
rejected_hypotheses:
  - Add production schema, signatures, whole-pack hash or rights policy: rejected as later owner scope.
  - Duplicate schema-v1 parser in asset-runtime: rejected; asset-types remains the sole format validator.
  - Add offset/overlap errors to a sequential inline format: rejected as speculative and unrepresentable in schema v1.
  - Expose filesystem path opening: rejected by the capability boundary.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p1-asset-pack-runtime.md
  - oteryn-client/crates/asset-runtime/**
validation:
  - command: live main, PR and ownership reconciliation
    result: PASS
    evidence: main fbbff443; game-domain merged/archived; PR 157 disjoint; shared lease free before grant.
  - command: producer schema and architecture policy review
    result: PASS
    evidence: asset-types remains sole decoder; asset-runtime category and asset-types edge already exist.
  - command: exclusive changed-path and public trust-boundary review
    result: PASS_WITH_REPAIR
    evidence: all implementation paths are owned; one test-only PartialEq assertion defect identified for deterministic repair before CI.
blockers: []
next_action: Run the isolated exact-main integration harness to repair error assertions, merge current main, add the workspace member, regenerate Cargo.lock with pinned Cargo 1.94, apply rustfmt and trigger retained exact-head validation.
```
