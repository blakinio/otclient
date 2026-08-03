---
task_id: OTC2-20260803-playability-p2-renderer-resource
status: validating
agent: "P2 renderer resource producer"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-renderer-resource
phase: exact-head-validation-and-audit
branch: feat/OTC2-20260803-playability-p2-renderer-resource
base_branch: main
created: 2026-08-03T12:24:00+02:00
updated: 2026-08-03T13:03:00+02:00
required_base_commit: "1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2"
risk: medium
related_prs: [200]
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-renderer-resource.md
  - oteryn-client/crates/renderer-resource/**
shared_path_lease:
  holder: OTC2-20260803-playability-p2-renderer-resource
  state: held
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
    - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
    - oteryn-client/crates/asset-decode/Cargo.toml
    - oteryn-client/tools/architecture-check/src/lib.rs
temporary_validation_path: []
implementation_authorized: true
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: implementation
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
context_pressure: high
decomposition_decision: phased
validation_level: heavy
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
depends_on: [OTC2-20260803-playability-p2-asset-decode]
blocks:
  - OTC2-20260803-playability-p2-input-platform
  - OTC2-20260803-playability-p2-visible-world-integration
invocation_started_at: 2026-08-03T12:20:00+02:00
last_progress_at: 2026-08-03T13:03:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: exact-head-final
terminal_ci_wait_started_at: 2026-08-03T13:03:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 4
context_reconstruction_attempts: 2
stall_warnings: 0
---

# Objective

Produce the smallest bounded renderer-resource contract for P2: immutable checked RGBA8 upload plans, generation-fenced logical handles and deterministic bounded cache/device-loss lifecycle. The crate owns no world state, draw policy, protocol, input, UI, filesystem acquisition or CPU media decode.

# Live state

- `main@1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2` contains the merged and archived Asset Decode producer.
- PR #200 is the only Renderer Resource implementation PR.
- Canary protocol remains independently blocked and holds no shared path.
- Input Platform PR #195 remains draft and owns no shared path while this serialized lease is held.
- No temporary workflow or request-only script remains in the PR diff.

# Implemented contract

- `TextureUploadPlan` revalidates immutable `DecodedRgba8` layout and owns zero-filled, 256-byte-row-aligned upload bytes.
- `TextureFormat::Rgba8Unorm` preserves the accepted raw RGBA8 contract without inventing an unproven sRGB transfer function.
- Hard limits bound live entries, logical device bytes, one texture and one upload-plan allocation.
- `TextureHandle` fences process, monotonically increasing device and asset-pack generations plus opaque slot/serial identity.
- `ResourceCache` coalesces duplicate generation-fenced assets and performs deterministic least-recently-used eviction.
- All fallible counters and cache metadata reservation complete before sink upload; no uploaded resource can escape cache accounting.
- Capacity and memory pressure commit bounded evictions before upload; this documented behavior remains deterministic if the sink then fails.
- `resolve` performs no allocation, decode, filesystem, network or blocking I/O.
- Device/pack replacement, stale handles/assets, missing resources and sink failures return stable payload-redacted errors.
- Fake-sink tests cover row padding and format, coalescing, eviction, pressure-plus-upload-failure, generation fencing, pre-upload arithmetic failure, reset and memory accounting.

# Architecture integration

The previous coarse `runtime` category for `oteryn-asset-decode` would require unsafe `renderer -> runtime`. The lease-scoped repair introduces a closed `asset-decode` category, permits only `asset-decode -> asset-runtime|asset-types` and `renderer -> asset-decode`, keeps `app/runtime -> asset-decode` forbidden, and changes no Asset Decode API or behavior.

# Validation checkpoint

Four bounded repair cycles addressed Clippy mechanics, post-upload accounting atomicity, monotonic generation/failure semantics and the final unproven color-space assumption. Self-removing focused generations ran pinned formatting, package tests, strict package Clippy, architecture-check tests and workspace architecture validation before final product head `563507cb6af1afd6fb727bec8cd662e9c0a38a67`. This checkpoint commit starts the retained exact-head validation generation.

# Acceptance

- [x] stable handles fence process, device and asset-pack generations;
- [x] RGBA8 descriptors and immutable upload plans validate dimensions, row pitch, 256-byte alignment, byte counts and checked arithmetic;
- [x] raw RGBA8 color semantics remain neutral and explicit;
- [x] configured upload/device memory limits are explicit and bounded;
- [x] duplicate asset requests coalesce deterministically;
- [x] cache entry/memory accounting and deterministic least-recently-used eviction are bounded;
- [x] stale/unknown handles, stale assets, device loss/recreation and sink failure have stable results;
- [x] frame lookup performs no filesystem access, decode, allocation or blocking I/O;
- [x] fake-sink component tests cover required lifecycle and negative cases;
- [x] workspace/category/lockfile integration is minimal and lease-scoped;
- [x] lockfile diff contains only the new local package entry;
- [x] narrow architecture category and dependency direction are covered by policy tests;
- [ ] retained exact-head Windows metadata, formatting, workspace Clippy/tests, architecture and Supply Chain pass;
- [ ] retained exact-head repository CI passes;
- [ ] fresh independent API/hot-path/resource-lifecycle audit has zero open material finding;
- [ ] implementation PR merges;
- [ ] task archives separately and all ownership/leases release.

# Claim boundary

This is a synthetic-v1 partial producer. It creates no real GPU device, draw pass, world renderer, production appearance importer, visible-world or M2 completion claim. E2E is `NOT_APPLICABLE` because this backend-neutral resource-lifecycle producer has no reachable real device, application or world composition.

# Checkpoint

```yaml
checkpoint_version: 6
status: validating
phase: exact-head-validation-and-audit
base: 1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2
branch: feat/OTC2-20260803-playability-p2-renderer-resource
final_product_head: 563507cb6af1afd6fb727bec8cd662e9c0a38a67
pr: 200
changed_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-renderer-resource.md
  - oteryn-client/Cargo.lock
  - oteryn-client/Cargo.toml
  - oteryn-client/crates/asset-decode/Cargo.toml
  - oteryn-client/crates/renderer-resource/Cargo.toml
  - oteryn-client/crates/renderer-resource/src/lib.rs
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/tools/architecture-check/src/lib.rs
focused_validation:
  result: PASS
  final_product_commit: 563507cb6af1afd6fb727bec8cd662e9c0a38a67
  commands:
    - cargo fmt --all
    - cargo metadata --locked --format-version 1
    - cargo test -p oteryn-renderer-resource --all-targets
    - cargo clippy -p oteryn-renderer-resource --all-targets -- -D warnings
    - cargo test -p oteryn-architecture-check --all-targets
    - cargo run -p oteryn-architecture-check -- workspace .
resolved_audit_findings:
  - id: P2-RENDERER-RESOURCE-ATOMICITY-001
    result: counters and metadata reservation preflight before sink upload
  - id: P2-RENDERER-RESOURCE-GENERATION-001
    result: device and pack generations must advance monotonically
  - id: P2-RENDERER-RESOURCE-COLORSPACE-001
    result: raw RGBA8 remains unorm without an unproven sRGB claim
exact_head_validation: pending
fresh_audit: pending
e2e:
  result: NOT_APPLICABLE
  reason: Backend-neutral producer has no reachable real GPU device, application or world composition.
shared_path_lease:
  state: held_until_terminal_merge_and_archive
blockers: []
next_action: Complete retained exact-head validation, run a fresh falsification audit, then merge and archive this task before releasing the Input Platform integration lease.
```
