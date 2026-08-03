---
task_id: OTC2-20260803-playability-p2-asset-decode
status: ready
agent: "P2 CPU asset-decode and normalization producer"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-asset-decode
phase: protected-merge
branch: feat/OTC2-20260803-playability-p2-asset-decode
base_branch: main
created: 2026-08-03T10:16:00+02:00
updated: 2026-08-03T11:20:00+02:00
required_base_commit: "c5270fccce2e56cde408f80857d95422e759cc4f"
risk: medium
related_prs:
  - 194
  - 197
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-asset-decode.md
  - oteryn-client/crates/asset-decode/**
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
implementation_authorized: true
policy_version: 2
prompting_standard_version: 2.1
task_kind: implementation
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
context_pressure: medium
decomposition_decision: phased
feature_scope:
  type: data_pipeline
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
depends_on:
  - OTC2-20260801-playability-p1-asset-pack-runtime
  - OTC2-20260803-playability-p1-aggregation
blocks:
  - OTC2-20260803-playability-p2-renderer-resource
  - OTC2-20260803-playability-p2-visible-world-integration
  - OTC2-20260803-playability-p2-controlled-m2-acceptance
invocation_started_at: 2026-08-03T10:16:00+02:00
last_progress_at: 2026-08-03T11:20:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-current-main-checkpoint
terminal_ci_wait_started_at: 2026-08-03T11:20:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Consume verified, generation-fenced synthetic-v1 `asset-runtime` records and produce deterministic, immutable, bounded CPU RGBA8 image data for the later Renderer Resource producer.

# Final producer result

The `oteryn-asset-decode` runtime package provides:

- `decode_rgba8(&AssetRuntime, AssetHandle, DecodeLimits)` with no filesystem-path input;
- synthetic-v1 `AssetKind::Rgba8` normalization only, with explicit opaque `Blob` rejection;
- immutable owned boxed RGBA8 bytes that do not alias runtime payload storage;
- checked non-zero dimensions, pixel count, row pitch and expected byte length;
- absolute/configured dimension, pixel and allocation bounds before output allocation;
- deterministic exact-length rejection for truncated, oversized and trailing payloads;
- fail-closed stale generation, unsupported schema and kind mismatch behavior;
- payload-redacted Debug/Display behavior;
- no production filesystem, network, GPU, renderer cache, global cache or blocking I/O.

# Validation evidence

## Focused integration

Run `30798884308`, job `91638642610`: PASS.

- pinned Rust 1.94 formatting;
- strict package Clippy with `-D warnings`;
- 9 package/component tests;
- compiler -> runtime -> decode round trip;
- architecture dependency direction;
- bounded lockfile generation and temporary-workflow self-removal.

## Exact implementation validation

Head `f594acbde5cf5a1335e37cbd356ddca8825eb52c` passed:

- Rust Client run `30799757159`;
- Windows workspace job `91641423237`;
- Supply Chain job `91641423243`;
- repository CI run `30799757355`, required job `91642080158`.

The documentation checkpoint `fc7aaeefcb570cd634341a56e2685c3fc74ebe32` also passed Rust Client run `30800298386` and repository CI run `30800298580`. While those checks ran, `main` advanced only in Canary-owned documentation paths to `c5270fccce2e56cde408f80857d95422e759cc4f`. The producer was rebuilt as one exact six-path commit on that current base (`f72d776483b705683949b7afc899aa912ae227ab`). This final task checkpoint requires one retained exact-head generation before merge.

# Fresh final audit

A fresh exact-diff falsification audit checked public API trust boundaries, schema/kind/generation fences, checked arithmetic, allocation timing, exact byte length, owned output, formatting redaction, production dependency direction, lockfile delta, changed-path inventory and absence of production filesystem/network/GPU/global-cache behavior.

Result: PASS. Open material findings: 0. Durable validator review: PR #194 review `4842447042`.

# Acceptance inventory

- [x] stable public decoded-image API and error model;
- [x] non-zero bounded dimensions;
- [x] checked pixel count, row pitch and expected byte length;
- [x] allocation bound checked before copy/allocation;
- [x] exact payload length with deterministic truncated, oversized and trailing failure behavior;
- [x] stale generation, unsupported schema and asset-kind mismatches fail;
- [x] debug/display reveal no payload bytes;
- [x] no global cache or unbounded collection;
- [x] equal verified input yields byte-identical immutable output;
- [x] normal, zero, maximum, overflow, mismatch and stale-generation tests;
- [x] compiler -> runtime -> decode component round trip passes;
- [x] no filesystem/network/GPU dependency or blocking I/O in the public decode path;
- [x] focused rustfmt, strict Clippy, package tests and architecture pass;
- [x] shared integration occurred only under the recorded lease;
- [x] exact implementation-head Windows workspace, Supply Chain and repository CI pass;
- [x] fresh independent audit has zero open material findings;
- [ ] current-main final checkpoint required checks pass;
- [ ] implementation merge, separate archive merge and ownership release.

# Integration delta

- workspace member: `crates/asset-decode`;
- lockfile: one local package with `asset-compiler`, `asset-runtime` and `asset-types`; no registry delta;
- architecture category: existing `runtime`;
- exact implementation diff: six expected paths;
- temporary workflow retained: false;
- temporary restack PR #197: merged terminal.

# Claim boundary

This task delivers only a bounded synthetic-v1 CPU RGBA8 producer. It does not deliver production appearance import, renderer resources, visible-world composition, M2 acceptance, rights or redistribution decisions.

# Checkpoint

```yaml
checkpoint_version: 7
status: ready
phase: protected-merge
base: c5270fccce2e56cde408f80857d95422e759cc4f
branch: feat/OTC2-20260803-playability-p2-asset-decode
pr: 194
restack_pr:
  number: 197
  state: merged
current_main_restack_head: f72d776483b705683949b7afc899aa912ae227ab
focused_validation:
  run: 30798884308
  job: 91638642610
  result: PASS
  tests: 9
validated_implementation:
  head: f594acbde5cf5a1335e37cbd356ddca8825eb52c
  rust_client_run: 30799757159
  windows_job: 91641423237
  supply_chain_job: 91641423243
  repository_ci_run: 30799757355
  repository_required_job: 91642080158
  result: PASS
validated_checkpoint:
  head: fc7aaeefcb570cd634341a56e2685c3fc74ebe32
  rust_client_run: 30800298386
  repository_ci_run: 30800298580
  result: PASS
fresh_audit:
  validator_review: 4842447042
  result: PASS
  material_findings_open: 0
integration_ready: true
architecture_category: runtime
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
lease_holder: OTC2-20260803-playability-p2-asset-decode
temporary_workflow_retained: false
blockers: []
next_action: Merge PR #194 after the current-main final checkpoint required checks pass, then create and merge the separate lifecycle archive.
```
