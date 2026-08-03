---
task_id: OTC2-20260803-playability-p2-renderer-resource
status: implementing
agent: "P2 renderer resource producer"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-renderer-resource
phase: exclusive-implementation-and-integration
branch: feat/OTC2-20260803-playability-p2-renderer-resource
base_branch: main
created: 2026-08-03T12:24:00+02:00
updated: 2026-08-03T12:24:00+02:00
required_base_commit: "1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2"
risk: medium
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
last_progress_at: 2026-08-03T12:24:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: implementation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Produce the smallest bounded renderer-resource contract for P2: immutable checked RGBA8 upload plans, generation-fenced logical handles and deterministic bounded cache/device-loss lifecycle. The crate owns no world state, draw policy, protocol, input, UI, filesystem acquisition or CPU media decode.

# Live preflight

- `main@1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2` archives the completed Asset Decode producer.
- Asset Decode implementation PR #194 and archive PR #199 are merged; its shared lease and ownership are released.
- Canary protocol remains independently blocked and holds no shared path.
- Input Platform PR #195 is draft, owns only `crates/input-platform/**` plus its task, and has not requested the shared lease.
- No renderer-resource task, branch or PR existed.
- This task is fourth in the accepted P2 shared integration order and therefore holds the serialized workspace/category/lockfile lease.

# Acceptance

- [ ] stable handles fence process, device and asset-pack generations;
- [ ] RGBA8 descriptors and immutable upload plans validate dimensions, row pitch, 256-byte alignment, byte counts and checked arithmetic;
- [ ] configured upload/device memory limits are explicit and bounded;
- [ ] duplicate asset requests coalesce deterministically;
- [ ] cache entry/memory accounting and deterministic least-recently-used eviction are bounded;
- [ ] unknown/stale handles, stale assets, device loss/recreation and sink failure have stable results;
- [ ] frame lookup performs no filesystem access, decode, allocation or blocking I/O;
- [ ] fake-sink tests cover upload, coalescing, eviction, stale generations and device loss;
- [ ] workspace/category/lockfile integration is minimal and lease-scoped;
- [ ] exact-head formatting, Clippy, tests, architecture, Supply Chain and repository CI pass;
- [ ] fresh independent API/hot-path/resource-lifecycle audit has zero material findings;
- [ ] implementation merges, task archives separately and all ownership/leases release.

# Claim boundary

This is a synthetic-v1 partial producer. It creates no real GPU device, draw pass, world renderer, production appearance importer, visible-world or M2 completion claim. E2E is `NOT_APPLICABLE` because the public package is a backend-neutral resource lifecycle producer validated with a deterministic fake upload sink.

# Checkpoint

```yaml
checkpoint_version: 1
status: implementing
base: 1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2
branch: feat/OTC2-20260803-playability-p2-renderer-resource
shared_path_lease:
  state: held
  paths: [oteryn-client/Cargo.toml, oteryn-client/Cargo.lock, oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md]
blockers: []
next_action: Implement the bounded crate and minimal workspace/category/lockfile integration, then run exact-head validation and fresh audit.
```
