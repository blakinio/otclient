---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: ready
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: inbound-layout-normalization
branch: docs/OTC2-20260803-canary-outbound-phase-closeout
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T09:13:00+02:00
required_base_commit: "822c1fcd21ef34f2d4d13e90ce93c89e7e9953f1"
risk: high
related_prs:
  - 188
  - 190
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - oteryn-client/tests/integration/canary-world-protocol/**
shared_path_lease: []
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
last_progress_at: 2026-08-03T09:13:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: inbound-evidence-next
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Goal

Reconcile the Canary Current development runtime descriptor with the merged generated P1 source index, preserving fail-closed real admission, then implement only those bounded M2 bootstrap/map/entity/movement/logout mappings whose exact field layouts can be established from provenance-safe evidence.

# Current state

- P1 aggregation implementation #184 and archive #185 are merged;
- P2 simulation/snapshot implementation #186 and archive #187 are merged;
- outbound implementation PR #188 merged as `9db7ad54d636ec5fefbfc40515c66343cc2786f5`;
- Windows line-ending repair PR #190 merged as `822c1fcd21ef34f2d4d13e90ce93c89e7e9953f1`;
- exact-head repository CI, Windows workspace, architecture and Supply Chain passed for repair PR #190;
- the cross-platform generated-index finding is resolved;
- the exclusive Cargo.lock lease is released;
- real wire admission remains fail-closed before network I/O;
- inbound bootstrap, map, entity and reconciliation layouts remain explicit `UNKNOWN`.

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
- [x] Windows line-ending normalization repair passes exact-head workspace tests.

## Phase 2 — bounded gameplay wire mapping

- [x] exact provenance-safe source/fixture evidence is classified per required M2 family at the current evidence boundary;
- [x] unsupported field layouts remain explicit `UNKNOWN` and are not guessed;
- [x] only the exactly supported outbound movement, stop and logout encoding family enters the package;
- [x] stale-session and unsupported semantic command inputs fail closed for the implemented outbound family;
- [x] merged `GameCommandEnvelope` remains the only outbound semantic envelope;
- [x] the encoder owns no simulation, renderer, asset, input, UI or app state;
- [x] focused negative tests pass for every implemented single-byte outbound layout;
- [x] the `game-domain` dependency and Cargo.lock delta were generated under the exclusive task lease;
- [x] exact-head Windows workspace, architecture, Supply Chain and repository CI pass after repair;
- [x] implementation and repair protected-merged and the shared lease is released;
- [ ] complete provenance-safe inbound bootstrap/map/entity/reconciliation layouts are normalized;
- [ ] original sanitized positive and negative fixtures prove every implemented inbound family;
- [ ] inbound parser component and malformed/truncated/trailing/oversized/ordering tests pass;
- [ ] controlled visible-world integration consumes decoded `GameEvent` envelopes.

## Claim boundary

Source declarations, opcodes and dispatch phases prove source shape only. They do not prove deployed revision, configuration, ordering, inbound field layout or compatibility. Missing exact layout evidence blocks that subfamily; it never authorizes inference from neighboring handlers.

## Context checkpoint

```yaml
checkpoint_version: 8
updated_at: 2026-08-03T09:13:00+02:00
base: 822c1fcd21ef34f2d4d13e90ce93c89e7e9953f1
branch: docs/OTC2-20260803-canary-outbound-phase-closeout
status: ready
phase: inbound-layout-normalization
terminal_prs:
  - number: 188
    state: merged
    merge_commit: 9db7ad54d636ec5fefbfc40515c66343cc2786f5
    purpose: Current baseline alignment and bounded outbound command encoder
  - number: 190
    state: merged
    merge_commit: 822c1fcd21ef34f2d4d13e90ce93c89e7e9953f1
    purpose: deterministic generated-index LF checkout on Windows
final_validation:
  focused_run_id: 30791628885
  focused_job_id: 91616196561
  focused_package_tests: PASS_18_OF_18
  focused_architecture: PASS
  repair_repository_ci_run: 30792560570
  repair_repository_ci: PASS
  repair_rust_client_run: 30792560480
  windows_job_id: 91619004844
  windows_workspace: PASS
  windows_architecture: PASS
  supply_chain_job_id: 91619004911
  supply_chain: PASS
fresh_audit:
  result: PASS
  validator: fresh_connector_audit_role
  material_findings_open: 0
  resolved_findings:
    - id: P2-CANARY-WINDOWS-EOL-001
      disposition: resolved_and_verified_exact_head
  final_repair_paths:
    - .gitattributes
    - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
    - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
e2e:
  result: NOT_APPLICABLE
  reason: The completed outbound producer phase performs no network transmission and has no reachable application consumer; controlled visible-world E2E remains a later P2 integration gate.
shared_path_lease: []
unknown:
  - complete inbound bootstrap, map, entity and reconciliation field layouts
  - provenance-safe original positive and negative inbound fixtures
  - controlled post-admission packet ordering
blockers: []
next_action: Inspect the exact Canary source revision and generated index for one bounded inbound bootstrap family, normalize every field, gate and ordering prerequisite into provenance-safe evidence, and leave the family UNKNOWN unless the complete layout is proven without inference.
```
