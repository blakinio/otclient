---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: validating
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: post-merge-windows-repair-ci
branch: fix/OTC2-20260803-canary-index-lf
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T09:07:00+02:00
required_base_commit: "9db7ad54d636ec5fefbfc40515c66343cc2786f5"
risk: high
related_pr: 188
repair_pr: 190
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - oteryn-client/tests/integration/canary-world-protocol/**
  - .gitattributes
shared_path_lease:
  - oteryn-client/Cargo.lock
implementation_authorized: true
policy_version: 2.1
prompting_standard_version: 2.1
task_kind: implementation
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
context_pressure: high
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - exact provenance-safe M2 inbound gameplay field layouts and bounded fixtures
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
invocation_started_at: 2026-08-03T08:24:00+02:00
last_progress_at: 2026-08-03T09:07:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: windows-newline-repair
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Reconcile the Canary Current development runtime descriptor with the merged generated P1 source index, preserving fail-closed real admission, then implement only those bounded M2 bootstrap/map/entity/movement/logout mappings whose exact field layouts can be established from provenance-safe evidence.

# Proven launch and current state

- P1 aggregation implementation #184 and archive #185 are merged;
- P2 simulation/snapshot implementation #186 and archive #187 are merged;
- outbound implementation PR #188 merged as `9db7ad54d636ec5fefbfc40515c66343cc2786f5`;
- repository CI and Supply Chain passed for PR #188;
- Windows metadata, formatting and workspace Clippy passed for PR #188;
- Windows workspace tests exposed one cross-platform fixture failure after merge because Git checkout converted generated JSON line endings to CRLF;
- the failure is isolated to test fixture line-ending normalization and does not change command encoding or admission behavior;
- repair PR #190 adds an explicit LF checkout rule for generated Canary JSON evidence;
- the Cargo.lock lease remains held until repair PR #190 passes, merges and the continuation checkpoint releases it;
- real wire admission remains fail-closed before network I/O.

# Acceptance

## Phase 1 — baseline alignment

- [x] development runtime metadata mechanically agrees with the generated `current-index.json` revision, release, client version, profile and enabled-feature/source-hash evidence;
- [x] historical cuts remain explicit historical evidence and are not silently called current;
- [x] descriptor/debug output remains non-secret and bounded;
- [x] tests consume the generated index as read-only evidence and fail on drift;
- [x] real admission remains `RealAdmissionUnavailable` and no credential/network lifecycle is weakened;
- [x] evidence document distinguishes inspected development baseline from deployed runtime equality;
- [x] focused Linux format, strict Clippy and package tests pass;
- [x] fresh source-provenance/trust/API audit has zero open product-code finding;
- [ ] Windows line-ending normalization repair passes exact-head workspace tests.

## Phase 2 — bounded gameplay wire mapping

- [x] exact provenance-safe source/fixture evidence is classified per required M2 family;
- [x] unsupported field layouts remain explicit `UNKNOWN` and are not guessed;
- [x] only the exactly supported outbound movement, stop and logout encoding family enters this phase;
- [x] stale-session and unsupported semantic command inputs fail closed for the implemented outbound family;
- [x] merged `GameCommandEnvelope` remains the only outbound semantic envelope;
- [x] the encoder owns no simulation, renderer, asset, input, UI or app state;
- [x] focused negative tests pass for every implemented single-byte outbound layout;
- [x] the `game-domain` dependency and Cargo.lock delta were generated under the exclusive task lease;
- [ ] exact-head Windows workspace, architecture, Supply Chain and repository CI pass after repair;
- [ ] repair protected-merges and the shared lease releases at the phase boundary.

## Claim boundary

Source declarations, opcodes and dispatch phases prove source shape only. They do not prove deployed revision, configuration, ordering, inbound field layout or compatibility. Missing exact layout evidence blocks that subfamily; it never authorizes inference from neighboring handlers.

## Context checkpoint

```yaml
checkpoint_version: 7
updated_at: 2026-08-03T09:07:00+02:00
base: 9db7ad54d636ec5fefbfc40515c66343cc2786f5
branch: fix/OTC2-20260803-canary-index-lf
implementation_pr:
  number: 188
  state: merged
  merge_commit: 9db7ad54d636ec5fefbfc40515c66343cc2786f5
repair_pr:
  number: 190
  state: open
status: validating
phase: post-merge-windows-repair-ci
validated_before_merge:
  focused_run_id: 30791628885
  focused_job_id: 91616196561
  cargo_fmt: PASS
  strict_clippy: PASS
  package_tests: PASS_18_OF_18
  architecture: PASS
  repository_ci_run: 30791877998
  repository_ci: PASS
  supply_chain: PASS
post_merge_failure:
  run_id: 30791877711
  job_id: 91616943625
  gate: Rust Client / Windows workspace tests
  signature: generated source index has no producer metadata
  cause: generated JSON was checked out with CRLF while the drift test intentionally used canonical LF section delimiters
  unaffected_gates:
    - cargo metadata --locked
    - cargo fmt --all --check
    - cargo clippy --workspace --all-targets --locked -- -D warnings
    - Supply Chain
repair:
  path: .gitattributes
  change: enforce LF for oteryn-client/tools/canary-protocol-index/generated/*.json
  product_behavior_changed: false
  credentials_or_private_data_changed: false
  pr: 190
fresh_audit:
  result: PASS_WITH_REPAIR_VALIDATION_PENDING
  validator: fresh_connector_audit_role
  material_product_findings_open: 0
  ci_portability_findings_open: 1
  finding:
    id: P2-CANARY-WINDOWS-EOL-001
    severity: high
    disposition: repair_implemented_validation_pending
  repair_diff:
    expected_paths:
      - .gitattributes
      - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
    product_code_changed: false
e2e:
  result: NOT_APPLICABLE
  reason: This bounded producer phase performs no network transmission and has no reachable application consumer; controlled visible-world E2E belongs to the later P2 integration task.
shared_path_lease:
  path: oteryn-client/Cargo.lock
  holder: OTC2-20260803-playability-p2-canary-world-protocol
  release_condition: repair PR 190 merge followed by immediate continuation checkpoint on current main
repair_cycles_for_current_gate: 1
blockers: []
next_action: Observe exact-head Windows workspace, Supply Chain and repository CI for repair PR 190, complete the final two-file audit, protected-merge it, then release the Cargo.lock lease and continue the parent task at inbound layout normalization.
```
