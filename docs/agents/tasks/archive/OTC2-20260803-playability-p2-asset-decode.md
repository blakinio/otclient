---
task_id: OTC2-20260803-playability-p2-asset-decode
status: completed
agent: "P2 CPU asset-decode and normalization producer"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-asset-decode
phase: archived
branch: feat/OTC2-20260803-playability-p2-asset-decode
base_branch: main
created: 2026-08-03T10:16:00+02:00
completed: 2026-08-03T11:24:14+02:00
archived: 2026-08-03T11:25:00+02:00
required_base_commit: "c5270fccce2e56cde408f80857d95422e759cc4f"
implementation_head: "dbda420eeb0de617d0e3b523b655a82b67caaeb6"
merge_commit: "cbd263f382ce333ee113f71ebeb359c7f573d744"
related_prs:
  - 194
  - 197
policy_version: 2
prompting_standard_version: 2.1
task_kind: implementation
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
feature_scope:
  type: data_pipeline
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
shared_path_lease:
  state: released
  released_by_merge: cbd263f382ce333ee113f71ebeb359c7f573d744
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
    - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
ownership:
  state: released
---

# Result

Implemented and protected-merged the bounded synthetic-v1 CPU RGBA8 decode and normalization producer.

The public contract:

- accepts only an immutable verified `AssetRuntime`, a generation-fenced `AssetHandle` and bounded `DecodeLimits`;
- accepts only synthetic-v1 `AssetKind::Rgba8` for image normalization;
- rejects opaque `Blob`, stale generation, unsupported schema, invalid dimensions, arithmetic overflow, configured/absolute bounds and non-exact payload length deterministically;
- returns immutable owned boxed tightly packed RGBA8 bytes that do not alias runtime payload storage;
- exposes no filesystem path, loose-file importer, network, GPU, renderer-cache or application concept;
- performs all layout/allocation checks before output allocation and contains no production blocking I/O or hidden global cache.

# Bounds

- maximum width: `16384`;
- maximum height: `16384`;
- maximum decoded bytes: `16777216`;
- maximum decoded pixels: `4194304`;
- bytes per pixel: `4`;
- pixel count, row pitch and expected byte length: checked arithmetic;
- payload length: exact equality required before copy.

# Deterministic coverage

Nine package/component tests cover:

1. byte-identical owned output and ownership after runtime drop;
2. opaque Blob rejection;
3. stale-generation rejection;
4. unsupported-schema rejection before decode;
5. limit validation and pre-copy enforcement;
6. zero, overflow, truncated and trailing layouts;
7. exact synthetic-v1 16 MiB maximum;
8. payload-redacted Debug/Display output;
9. synthetic compiler -> runtime -> decode component round trip.

# Integration delta

- added workspace member `crates/asset-decode`;
- added one local lockfile package `oteryn-asset-decode`;
- production dependencies: existing local `oteryn-asset-runtime` and `oteryn-asset-types` only;
- test-only dependency: existing local `oteryn-asset-compiler`;
- new registry dependencies: none;
- architecture category: existing `runtime`;
- implementation diff: six expected paths;
- temporary validation workflow retained: false.

# Validation

## Focused/component

- run `30798884308`, job `91638642610`: PASS;
- pinned Rust 1.94 formatting;
- strict Clippy with `-D warnings`;
- 9 package/component tests;
- compiler -> runtime -> decode round trip;
- architecture and bounded lock generation.

## Exact current-main implementation

Final implementation head `dbda420eeb0de617d0e3b523b655a82b67caaeb6` was directly based on `main@c5270fccce2e56cde408f80857d95422e759cc4f` and passed:

- Rust Client run `30800946849`;
- Windows workspace job `91645129521`: PASS;
- Supply Chain job `91645129589`: PASS;
- repository CI run `30800947305`;
- required job `91645654801`: PASS.

Historical exact generations also passed at `f594acbde5cf5a1335e37cbd356ddca8825eb52c` and `fc7aaeefcb570cd634341a56e2685c3fc74ebe32` before later non-overlapping Canary documentation commits advanced `main`.

# Audit

Fresh exact-final-diff validator review `4842447042`: PASS.

Checked:

- public trust/API boundary;
- schema, kind and generation fences;
- checked arithmetic and allocation timing;
- exact byte length and payload ownership;
- Debug/Display redaction;
- no production filesystem/network/GPU/global-cache behavior;
- changed-path inventory, architecture category and dependency direction;
- lockfile delta and absence of new registry dependencies.

Open material findings: 0.

# PR hygiene

- implementation PR #194: merged as `cbd263f382ce333ee113f71ebeb359c7f573d744`;
- temporary restack PR #197: merged terminal;
- temporary validation workflow: removed before implementation merge;
- implementation review threads: 0 unresolved;
- requested changes: 0.

# Claim boundary

This completed task is a partial producer only. It does not claim production asset import, production appearance support, GPU upload, renderer resources, visible-world completion or M2 acceptance.

# Closeout

```yaml
checkpoint_version: 8
status: completed
phase: archived
implementation_pr:
  number: 194
  state: merged
  head: dbda420eeb0de617d0e3b523b655a82b67caaeb6
  merge_commit: cbd263f382ce333ee113f71ebeb359c7f573d744
temporary_restack_pr:
  number: 197
  state: merged
focused_validation:
  run: 30798884308
  job: 91638642610
  tests: 9
  result: PASS
exact_head_validation:
  rust_client_run: 30800946849
  windows_job: 91645129521
  supply_chain_job: 91645129589
  repository_ci_run: 30800947305
  repository_required_job: 91645654801
  result: PASS
fresh_audit:
  validator_review: 4842447042
  material_findings_open: 0
  result: PASS
e2e:
  result: NOT_APPLICABLE
  reason: Producer has no executable or GPU consumer.
shared_path_lease:
  state: released
ownership:
  state: released
blockers: []
next_action: Open Renderer Resource only from exact current main after confirming this lifecycle archive merge; do not begin it in this task.
```
