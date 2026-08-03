---
task_id: OTC2-20260803-playability-p2-input-platform
status: waiting
agent: "P2 Windows/winit physical-input adapter producer"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-input-platform
phase: exclusive-implementation-complete-awaiting-renderer-resource-archive
branch: feat/OTC2-20260803-playability-p2-input-platform
base_branch: main
created: 2026-08-03T10:15:00+02:00
updated: 2026-08-03T12:51:00+02:00
required_base_commit: "d18b618fc68c0e67598be10dee6f1d0119bc8aa8"
risk: medium
related_prs: [195, 200]
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-input-platform.md
  - oteryn-client/crates/input-platform/**
shared_path_lease: []
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
validation_level: component-before-integration
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
dependent_downstream_package: playability-p2-visible-world-integration
invocation_started_at: 2026-08-03T10:15:00+02:00
last_progress_at: 2026-08-03T12:51:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: renderer-dependency-wait
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 1
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Implement the sole bounded Windows/winit adapter into the merged `oteryn-input-actions`
physical-event contract without product bindings, gameplay commands, application composition,
global hooks, background capture, device fingerprinting or secret input logging.

# Verified live state

```yaml
base_at_claim: d18b618fc68c0e67598be10dee6f1d0119bc8aa8
observed_main: 1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2
p1_aggregation: merged_and_archived
input_actions:
  implementation_pr: 157
  archive_pr: 183
  state: merged_and_archived
winit: 0.30.13
p2_order:
  - simulation-snapshot
  - canary-world-protocol
  - asset-decode
  - renderer-resource
  - input-platform
  - visible-world-integration
simulation_snapshot: merged_and_archived
canary_world_protocol:
  latest_implementation_pr: 196
  latest_closeout_pr: 198
  state: provenance_blocked_without_shared_lease
asset_decode:
  implementation_pr: 194
  implementation_merge: cbd263f382ce333ee113f71ebeb359c7f573d744
  archive_pr: 199
  archive_merge: 1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2
  state: merged_and_archived
renderer_resource:
  task: OTC2-20260803-playability-p2-renderer-resource
  implementation_pr: 200
  branch: feat/OTC2-20260803-playability-p2-renderer-resource
  observed_head: 1615249a9781db2d253f57ce568a9e481fe59e47
  state: active_implementing
  phase: focused-repair-and-architecture-integration
  shared_path_lease: held
  exact_head_rust_client: 30807323424_action_required
  exact_head_repository_ci: 30807323553_action_required
input_platform:
  implementation_pr: 195
  state: open_draft_waiting
shared_path_lease_holder: OTC2-20260803-playability-p2-renderer-resource
unrelated_open_prs: [23, 48, 97]
```

Renderer Resource is now active and holds the serialized workspace/category/lockfile lease. Input
Platform remains fifth in the accepted sequence. No root workspace, lockfile, architecture policy,
workflow or `apps/client/**` mutation is authorized for this task until Renderer Resource merges,
archives separately and releases its lease.

# Exclusive implementation

```yaml
crate: oteryn-input-platform
implementation_code_head: 0e4578dc9c1f8e2a083e18407a2c968cf5c0be1a
public_success_output: Vec<oteryn_input_actions::NormalizedInputEvent>
public_error: InputPlatformError
public_winit_or_win32_output: none
physical_identity: explicit_usb_hid_keyboard_usage_subset
logical_key_identity: ignored
keyboard_groups:
  - letters_A_to_Z
  - digits_0_to_9
  - editing_and_punctuation
  - F1_to_F24
  - navigation
  - numpad
  - left_and_right_modifiers
mouse_buttons: [primary, secondary, middle, back, forward]
pointer_position: rounded_bounded
pointer_large_jump: rebase_zero_motion
relative_motion: focused_captured_and_absolute_baseline_only
wheel_line_scale: 120
wheel_pixel_scale: 1
text_limit_utf8_bytes: 4096
ime_policy: suppress_key_text_while_enabled_and_emit_commit_separately
focus_duplicate: no_output
capture_duplicate: no_output
capture_gain_unfocused: rejected
focus_loss: capture_loss_if_needed_then_focus_loss
capture_loss: clear_pointer_baseline
winit_device_removed: DeviceLost
unknown_key_or_button: DeviceLost_reset
lifecycle_order: event_loop_receipt_order
background_input: ignored
raw_text_logging: false
native_key_or_device_identifier_retention: false
global_state: none
global_hook: none
```

# Changed paths

- `docs/agents/tasks/active/OTC2-20260803-playability-p2-input-platform.md`
- `oteryn-client/crates/input-platform/Cargo.toml`
- `oteryn-client/crates/input-platform/src/adapter.rs`
- `oteryn-client/crates/input-platform/src/error.rs`
- `oteryn-client/crates/input-platform/src/lib.rs`
- `oteryn-client/crates/input-platform/src/tests.rs`
- `oteryn-client/crates/input-platform/src/winit_adapter.rs`

# Acceptance state

- [x] no winit or Win32 type crosses the public output boundary;
- [x] physical identity is explicit and logical identity is not substituted;
- [x] modifiers, buttons, pointer, wheel and text values are deterministic and bounded;
- [x] IME commits remain distinct from key transitions;
- [x] focus, capture and device loss emit merged cleanup events;
- [x] duplicate lifecycle transitions are deterministic;
- [x] unsupported controls reset through `DeviceLost`, never alias and cannot strand held state;
- [x] no raw secret text logging, global hook, background capture or device fingerprinting exists;
- [x] synthetic adapter and `InputRouter` component test source is present;
- [x] adapter event matches rechecked against the pinned winit API surface by source inspection;
- [ ] pinned rustfmt executed for this package;
- [ ] strict package Clippy executed;
- [ ] focused and component package tests executed;
- [ ] fresh independent validator executed;
- [ ] serialized workspace/category/lockfile integration completed;
- [ ] exact-head Windows workspace, architecture, Supply Chain and repository CI passed after integration.

`integration_ready` remains false. The source and test implementation are a coherent integration
candidate, but required executable proof has not run and is not inferred from parent-workspace CI.

# Test inventory

```yaml
adapter_and_router_tests_authored: 11
windows_winit_mapping_tests_authored: 2
total: 13
coverage:
  - keyboard_and_non_ime_text
  - synthetic_and_background_input
  - unsupported_key_button_reset
  - side_specific_modifiers
  - pointer_bounds_rebase_and_relative_capture
  - wheel_units_zero_and_bounds
  - ime_bounds_and_privacy
  - focus_loss_and_duplicate
  - capture_loss_and_order
  - device_loss
  - wheel_router_impulse
  - stable_winit_keyboard_subset
  - stable_winit_mouse_buttons
```

# Validation

```yaml
focused:
  result: NOT_RUN
  blocker: no authorized GitHub Actions entry point compiles the non-member standalone crate
component:
  result: NOT_RUN
  blocker: same; InputRouter component tests are authored but unexecuted
static_api_recheck:
  result: PASS_BY_SOURCE_INSPECTION
  scope:
    - winit_0_30_13_keyboard_input_fields
    - physical_key_identity
    - synthetic_key_filter
    - modifier_state
    - mouse_button_variants
    - cursor_and_wheel_events
    - ime_events
    - device_removed_and_relative_motion
  new_material_findings: 0
intermediate_repository_ci:
  run: 30798555174
  head: 8741c6b06b7ad1e788070c0316294f3d9ac0594f
  result: CANCELLED_AFTER_HEAD_MOVED
  supply_chain: PASS
  parent_workspace_format: PASS
  parent_workspace_clippy: PASS
  parent_workspace_tests: CANCELLED
  architecture: SKIPPED
  proves_input_platform: false
exact_head_workspace:
  result: NOT_PERMITTED_WHILE_RENDERER_RESOURCE_HOLDS_SERIALIZED_LEASE
```

# Audit

```yaml
validator: implementing_session_self_falsification
independent_validator: NOT_RUN
full_pr_diff_inspected: true
pinned_winit_api_surface_rechecked: true
public_type_leakage: none_observed
stuck_input_risk: remediated
unsupported_event_policy: explicit_DeviceLost_reset
privacy_and_logging: pass_by_source_inspection
hidden_global_state: none_observed
background_capture_or_global_hooks: none
panic_unwrap_todo_unimplemented: none_observed
new_material_findings_after_dependency_recheck: 0
open_material_code_findings: 0
resolved_findings:
  - id: P2-INPUT-STUCK-001
    severity: medium
    issue: unsupported release originally returned only an error and could strand router state
    disposition: fixed_with_DeviceLost_reset_and_InputRouter_fixture
  - id: P2-INPUT-DOC-001
    severity: low
    issue: public winit docs described the superseded error policy
    disposition: fixed
open_evidence_gates:
  - focused_component_execution
  - pinned_rustfmt_and_strict_clippy
  - fresh_independent_validation
```

# Exact waiting boundary

Asset Decode is merged and separately archived. Renderer Resource is now the active fourth producer,
owns PR #200 and holds the serialized shared-path lease. Its implementation, exact-head validation,
fresh audit, protected merge and separate archive are not owned by this task. This Input Platform
producer may not modify that branch, its exclusive crate, shared Cargo/category paths or its CI
repair workflow, and may not request the lease before it is explicitly released.

Input Platform cannot execute its required workspace integration or authoritative package gates
until that release. Repeated polling is not authorized; this checkpoint records the exact dependency
and leaves the branch coherent for immediate continuation once the barrier becomes terminal.

# Durable checkpoint

```yaml
checkpoint_version: 4
updated_at: 2026-08-03T12:51:00+02:00
base_at_claim: d18b618fc68c0e67598be10dee6f1d0119bc8aa8
observed_main: 1d7f80e3dadc8c71ad06dab2f7cfad5c7ad361b2
branch: feat/OTC2-20260803-playability-p2-input-platform
implementation_code_head: 0e4578dc9c1f8e2a083e18407a2c968cf5c0be1a
previous_checkpoint_head: ccf007d7272b202d389512e574abed4285904f5f
status: waiting
phase: exclusive-implementation-complete-awaiting-renderer-resource-archive
implementation_pr: 195_open_draft
exclusive_implementation_complete: true
integration_candidate_ready: true
integration_ready: false
focused_validation: NOT_RUN
component_validation: NOT_RUN
static_api_recheck: PASS_BY_SOURCE_INSPECTION
fresh_independent_audit: NOT_RUN
material_code_findings_open: 0
e2e: NOT_APPLICABLE_application_bindings_and_interactive_Windows_journey_are_downstream
unresolved_review_threads_at_last_read: 0
asset_decode: merged_and_archived
renderer_resource:
  pr: 200_open_draft
  head: 1615249a9781db2d253f57ce568a9e481fe59e47
  state: active_holding_serialized_lease
archive_pr: not_created_before_implementation_merge
shared_path_lease: []
blockers:
  - P2-INPUT-RENDERER-LEASE
next_action: After Renderer Resource merges and separately archives, obtain the Input Platform serialized lease, restack on exact main, integrate minimally and execute rustfmt, strict Clippy, focused/component tests, exact-head CI and fresh independent validation before merge.
```
