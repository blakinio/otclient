---
task_id: OTC2-20260803-playability-p2-renderer-resource
status: implementing
agent: "P2 renderer resource producer"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-renderer-resource
phase: focused-repair-and-validation
branch: feat/OTC2-20260803-playability-p2-renderer-resource
base_branch: main
created: 2026-08-03T12:24:00+02:00
updated: 2026-08-03T12:40:00+02:00
required_base_commit: "1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2"
risk: medium
related_prs:
  - 200
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
temporary_validation_path:
  - .github/workflows/otc2-renderer-resource-atomic-repair.yml
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
depends_on:
  - OTC2-20260803-playability-p2-asset-decode
blocks:
  - OTC2-20260803-playability-p2-input-platform
  - OTC2-20260803-playability-p2-visible-world-integration
invocation_started_at: 2026-08-03T12:20:00+02:00
last_progress_at: 2026-08-03T12:40:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: atomic-repair
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 2
stall_warnings: 0
---

# Objective

Produce the smallest bounded renderer-resource contract for P2: immutable checked RGBA8 upload plans, generation-fenced logical handles and deterministic bounded cache/device-loss lifecycle. The crate owns no world state, draw policy, protocol, input, UI, filesystem acquisition or CPU media decode.

# Live preflight

- `main@1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2` archives the completed Asset Decode producer.
- Asset Decode implementation PR #194 and archive PR #199 are merged; its shared lease and ownership are released.
- Canary protocol remains independently blocked and holds no shared path.
- Input Platform PR #195 is draft, owns only `crates/input-platform/**` plus its task, and has not requested the shared lease.
- No renderer-resource task or PR existed before this producer was claimed.
- This task is fourth in the accepted P2 shared integration order and therefore holds the serialized workspace/category/lockfile lease.
- Draft implementation PR #200 owns this task branch.

# Current implementation

- backend-neutral `TextureUploadPlan` revalidates immutable `DecodedRgba8` layout and owns zero-padded 256-byte-aligned upload bytes;
- hard limits bound entries, logical device bytes, one texture and one upload plan;
- `TextureHandle` fences process, device and asset-pack generations plus opaque slot/serial identity;
- caller-visible acquisition coalesces duplicate generation-fenced assets and uses deterministic least-recently-used eviction;
- resource resolution performs no allocation, decode, filesystem, network or blocking I/O;
- device/pack replacement and sink failure are explicit and payload-redacted;
- fake-sink component tests exercise padding, coalescing, eviction, generation fencing, failure, reset and accounting.

# Repair checkpoint

The first focused Clippy generation exposed only bounded source mechanics: prohibited constant `expect` calls and one test initializer. These were repaired. A fresh audit then identified a post-upload counter-failure window that could leave a sink-owned texture outside cache accounting. The temporary push workflow preflights all fallible counters before upload, adds an atomicity fixture, restores unrelated lockfile drift, runs format/tests/strict Clippy, self-removes and commits only the bounded repair.

# Acceptance

- [x] stable handles fence process, device and asset-pack generations;
- [x] RGBA8 descriptors and immutable upload plans validate dimensions, row pitch, 256-byte alignment, byte counts and checked arithmetic;
- [x] configured upload/device memory limits are explicit and bounded;
- [x] duplicate asset requests coalesce deterministically;
- [x] cache entry/memory accounting and deterministic least-recently-used eviction are bounded;
- [x] unknown/stale handles, stale assets, device loss/recreation and sink failure have stable results;
- [x] frame lookup performs no filesystem access, decode, allocation or blocking I/O;
- [x] fake-sink tests cover upload, coalescing, eviction, stale generations and device loss;
- [x] workspace/lockfile/layout integration is minimal and lease-scoped;
- [ ] focused formatting, strict Clippy and package/component tests pass after atomic repair;
- [ ] architecture dependency direction is accepted without a broad policy exception;
- [ ] exact-head Windows, Supply Chain and repository CI pass;
- [ ] fresh independent API/hot-path/resource-lifecycle audit has zero material findings;
- [ ] implementation merges, task archives separately and all ownership/leases release.

# Claim boundary

This is a synthetic-v1 partial producer. It creates no real GPU device, draw pass, world renderer, production appearance importer, visible-world or M2 completion claim. E2E is `NOT_APPLICABLE` because the public package is a backend-neutral resource lifecycle producer validated with a deterministic fake upload sink.

# Checkpoint

```yaml
checkpoint_version: 2
status: implementing
phase: focused-repair-and-validation
base: 1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2
branch: feat/OTC2-20260803-playability-p2-renderer-resource
pr: 200
shared_path_lease:
  state: held
  paths: [oteryn-client/Cargo.toml, oteryn-client/Cargo.lock, oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md]
temporary_validation_path: .github/workflows/otc2-renderer-resource-atomic-repair.yml
blockers: []
next_action: Complete the self-removing atomic repair, then prove the narrow architecture edge and run exact-head validation.
```
