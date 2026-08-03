---
task_id: OTC2-20260803-playability-p2-input-platform
status: validating
agent: "P2 Windows/winit physical-input adapter producer"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-input-platform
phase: protected-merge-and-archive
branch: feat/OTC2-20260803-playability-p2-input-platform
base_branch: main
created: 2026-08-03T10:15:00+02:00
updated: 2026-08-03T13:46:00+02:00
required_base_commit: "8a3ce18f8fe98c5654ac3ce36c098404bdfc3343"
risk: medium
related_prs: [195, 200, 201]
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-input-platform.md
  - oteryn-client/crates/input-platform/**
shared_path_lease:
  holder: OTC2-20260803-playability-p2-input-platform
  state: held
  paths:
    - oteryn-client/Cargo.toml
    - oteryn-client/Cargo.lock
    - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
    - oteryn-client/tools/architecture-check/src/lib.rs
temporary_validation_paths: []
implementation_authorized: true
policy_version: 2
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
dependent_downstream_package: playability-p2-visible-world-integration
invocation_started_at: 2026-08-03T10:15:00+02:00
last_progress_at: 2026-08-03T13:46:00+02:00
ci_checks_for_current_head: 1
ci_check_generation: protected-ready
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 2
stall_warnings: 0
---

# Goal

Implement the sole bounded Windows/winit adapter into the merged `oteryn-input-actions` physical-event contract without product bindings, gameplay commands, application composition, global hooks, background capture, device fingerprinting or secret input logging.

# Terminal implementation

```yaml
crate: oteryn-input-platform
exclusive_code_head: 0e4578dc9c1f8e2a083e18407a2c968cf5c0be1a
integrated_product_head: df8e8bd833f1a3b7395b03bda8dd13470754458a
validated_head: 7a6cbef1dcefb6910903c68720dc45234cf3edd6
base: 8a3ce18f8fe98c5654ac3ce36c098404bdfc3343
public_success_output: Vec<oteryn_input_actions::NormalizedInputEvent>
public_error: InputPlatformError
physical_identity: explicit_usb_hid_keyboard_usage_subset
logical_key_identity: ignored
mouse_buttons: [primary, secondary, middle, back, forward]
pointer_values: finite_rounded_bounded
relative_motion: focused_captured_with_absolute_baseline
wheel_line_scale: 120
wheel_pixel_scale: 1
text_limit_utf8_bytes: 4096
ime_policy: key_text_suppressed_while_ime_enabled_and_commit_emitted_separately
unsupported_key_or_button: DeviceLost_reset
focus_and_capture_cleanup: deterministic
background_input: ignored
raw_text_logging: false
native_device_identifier_retention: false
global_hook: none
architecture_category: input-platform
normal_dependency_edges: [input-platform_to_input]
```

# Completed integration

- branch is restacked on exact current main containing archived Asset Decode and Renderer Resource producers;
- parent workspace package and lint inheritance is active;
- the new package is a workspace member and `Cargo.lock` adds only its local entry;
- the dedicated `input-platform` category permits only `input-platform -> input` and prevents reverse, foundation, platform, runtime and renderer edges;
- repository layout records the native-adapter responsibility and one-way dependency;
- all temporary integration/validation workflows and scripts are removed;
- generated Rust target metadata is absent from the final diff.

# Verified lifecycle boundary

- numeric normalization rejects non-finite and out-of-range values before integer conversion;
- raw text and native identifiers are neither logged nor retained; error formatting is payload-redacted;
- unsupported controls produce deterministic `DeviceLost` cleanup instead of aliases or stranded releases;
- focus loss emits capture loss first when required and clears modifiers, pointer baseline and IME state;
- relative motion requires focus, confirmed capture and a validated absolute baseline;
- synthetic keyboard events and all unfocused background input are ignored;
- winit/Win32 output types, product bindings, commands, UI actions and application lifecycle do not cross the public boundary.

# Acceptance

- [x] exclusive implementation and 13 focused/component tests are authored;
- [x] physical identity is explicit and logical identity is not substituted;
- [x] modifiers, pointer, wheel and text values are deterministic and bounded;
- [x] unsupported controls and lifecycle losses clear merged router state;
- [x] no raw secret logging, global hook, background capture or device fingerprinting exists;
- [x] exact-main restack and parent-workspace integration are complete;
- [x] lockfile integration has no registry source/checksum drift;
- [x] dedicated one-way architecture category and policy tests are complete;
- [x] pinned focused/component validation passed;
- [x] exact-head Windows metadata, formatting, workspace Clippy/tests and architecture passed;
- [x] exact-head Supply Chain and repository CI passed;
- [x] fresh exact-final-diff audit has zero open critical, high or material-medium findings;
- [ ] PR #195 protected-merges after ready-state CI;
- [ ] task archives separately and all ownership/leases release.

# Claim boundary

This is a physical-input `partial_producer`. It owns no product keymap, gameplay command, UI action, app composition, interactive Windows journey, global OS hook or background capture. E2E is `NOT_APPLICABLE`; product bindings and the interactive Windows path belong to downstream visible-world integration and controlled acceptance.

# Durable checkpoint

```yaml
checkpoint_version: 7
status: validating
phase: protected-merge-and-archive
observed_main: 8a3ce18f8fe98c5654ac3ce36c098404bdfc3343
branch: feat/OTC2-20260803-playability-p2-input-platform
exclusive_code_head: 0e4578dc9c1f8e2a083e18407a2c968cf5c0be1a
integrated_product_head: df8e8bd833f1a3b7395b03bda8dd13470754458a
validated_head: 7a6cbef1dcefb6910903c68720dc45234cf3edd6
implementation_pr: 195_open_draft
changed_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-input-platform.md
  - oteryn-client/Cargo.lock
  - oteryn-client/Cargo.toml
  - oteryn-client/crates/input-platform/Cargo.toml
  - oteryn-client/crates/input-platform/src/adapter.rs
  - oteryn-client/crates/input-platform/src/error.rs
  - oteryn-client/crates/input-platform/src/lib.rs
  - oteryn-client/crates/input-platform/src/tests.rs
  - oteryn-client/crates/input-platform/src/winit_adapter.rs
  - oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
  - oteryn-client/tools/architecture-check/src/lib.rs
focused_validation:
  result: PASS
  producer_commit: df8e8bd833f1a3b7395b03bda8dd13470754458a
  commands:
    - cargo fmt --all
    - cargo metadata --locked --format-version 1
    - cargo clippy -p oteryn-input-platform --all-targets -- -D warnings
    - cargo test -p oteryn-input-platform --all-targets
    - cargo test -p oteryn-architecture-check --all-targets
    - cargo run -p oteryn-architecture-check -- workspace .
exact_head_validation:
  result: PASS
  rust_client_run: 30810506337
  windows_job: 91675884500
  locked_metadata: PASS
  formatting: PASS
  workspace_clippy: PASS
  workspace_tests: PASS
  architecture: PASS
  supply_chain_job: 91675884496
  supply_chain: PASS
  repository_ci_run: 30810506497
  repository_required_job: 91676092725
  repository_ci: PASS
fresh_audit:
  result: PASS
  validator: fresh_connector_audit_role
  review_id: 4843634196
  critical_open: 0
  high_open: 0
  material_medium_open: 0
e2e:
  result: NOT_APPLICABLE
  reason: Physical-input producer has no product bindings, application composition or reachable interactive Windows journey.
pr_hygiene:
  temporary_paths: []
  unresolved_review_threads: 0
  requested_changes: 0
shared_path_lease:
  state: held_until_terminal_merge_and_archive
blockers: []
next_action: Complete retained final-head CI, mark PR 195 ready, require ready-state CI, protected-merge, archive separately and release all Input Platform ownership and shared leases.
```
