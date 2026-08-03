---
task_id: OTC2-20260803-playability-p2-input-platform
status: implementing
agent: "P2 Windows/winit physical-input adapter producer"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-input-platform
phase: restack-and-workspace-integration
branch: feat/OTC2-20260803-playability-p2-input-platform
base_branch: main
created: 2026-08-03T10:15:00+02:00
updated: 2026-08-03T13:20:00+02:00
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
last_progress_at: 2026-08-03T13:20:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: integration-bootstrap
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 2
stall_warnings: 0
---

# Goal

Implement the sole bounded Windows/winit adapter into the merged `oteryn-input-actions` physical-event contract without product bindings, gameplay commands, application composition, global hooks, background capture, device fingerprinting or secret input logging.

# Live state

- exact current `main`: `8a3ce18f8fe98c5654ac3ce36c098404bdfc3343`;
- Asset Decode implementation/archive PRs #194/#199 are merged;
- Renderer Resource implementation/archive PRs #200/#201 are merged and all of their ownership and shared leases are released;
- Canary protocol remains independently provenance-blocked without a shared lease;
- this existing task and PR #195 are the sole Input Platform owner;
- no competing shared-path lease exists;
- Input Platform is fifth in the accepted P2 serialized integration order and now holds the workspace/category/lockfile lease.

# Exclusive implementation candidate

```yaml
crate: oteryn-input-platform
implementation_code_head: 0e4578dc9c1f8e2a083e18407a2c968cf5c0be1a
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
```

# Source audit before integration

- all numeric normalization rejects non-finite and out-of-range values before integer conversion;
- text errors expose lengths only; merged `TextCommit` debug output is payload-redacted;
- unsupported controls reset merged held state instead of aliasing or stranding releases;
- focus loss emits capture loss first when required and clears modifiers/pointer/IME state;
- relative motion requires focus, capture and a validated absolute baseline;
- winit output/native identifiers do not cross the public boundary;
- no product binding or command mapping is present.

# Acceptance

- [x] exclusive implementation and 13 focused/component tests are authored;
- [x] physical identity is explicit and logical identity is not substituted;
- [x] modifiers, pointer, wheel and text values are deterministic and bounded;
- [x] unsupported controls and lifecycle losses clear merged router state;
- [x] no raw secret logging, global hook, background capture or device fingerprinting exists;
- [ ] restack on exact current main;
- [ ] replace the standalone nested workspace marker with parent workspace inheritance;
- [ ] add the crate to the parent workspace and exact lockfile without registry drift;
- [ ] add narrow `input -> input` architecture policy and repository-layout documentation;
- [ ] pinned format, focused/component tests and strict package Clippy pass;
- [ ] exact-head Windows workspace, architecture, Supply Chain and repository CI pass;
- [ ] fresh independent audit has zero open critical, high or material-medium findings;
- [ ] PR #195 protected-merges;
- [ ] task archives separately and all ownership/leases release.

# Claim boundary

This is a physical-input `partial_producer`. It owns no product keymap, gameplay command, UI action, app composition, interactive Windows journey, global OS hook or background capture. E2E is `NOT_APPLICABLE`; product bindings and the interactive Windows path belong to downstream visible-world integration and controlled acceptance.

# Durable checkpoint

```yaml
checkpoint_version: 5
status: implementing
phase: restack-and-workspace-integration
observed_main: 8a3ce18f8fe98c5654ac3ce36c098404bdfc3343
branch: feat/OTC2-20260803-playability-p2-input-platform
implementation_code_head: 0e4578dc9c1f8e2a083e18407a2c968cf5c0be1a
checkpoint_head_before_resume: 16f9df4ec7df98bde61dc9c9c65ec2f2a9be55c6
implementation_pr: 195_open_draft
renderer_resource:
  implementation_pr: 200_merged
  archive_pr: 201_merged
  archive_merge: 8a3ce18f8fe98c5654ac3ce36c098404bdfc3343
shared_path_lease:
  state: held
  paths: [oteryn-client/Cargo.toml, oteryn-client/Cargo.lock, oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md, oteryn-client/tools/architecture-check/src/lib.rs]
blockers: []
next_action: Merge exact main into the branch, integrate the crate minimally, run focused/component validation, then retain exact-head CI and a fresh independent audit before protected merge and separate archive.
```
