---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: implementing
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: isolated-finalizer
branch: feat/OTC2-20260803-playability-p2-canary-world-protocol
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T08:24:00+02:00
required_base_commit: "f1a5a1873dbb9ce164aefed7537d5c3004eeb696"
risk: high
related_pr: 188
owned_paths:
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
  - oteryn-client/crates/protocol-canary/**
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - oteryn-client/tests/integration/canary-world-protocol/**
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
user_communication: low_noise
context_pressure: high
decomposition_decision: phased
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - exact provenance-safe M2 gameplay field layouts and bounded fixtures
  - asset decode and renderer resources
  - platform input adapter and product binding map
  - visible-world app composition and controlled M2 E2E
invocation_started_at: 2026-08-03T08:24:00+02:00
last_progress_at: 2026-08-03T08:24:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: isolated-finalizer
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

# Proven launch state

- P1 aggregation implementation #184 and archive #185 are merged;
- P2 simulation/snapshot implementation #186 and archive #187 are merged;
- current exact base is `main@f1a5a1873dbb9ce164aefed7537d5c3004eeb696`;
- all prior shared integration leases were released before this task;
- current open PR inventory has no other Rust Client PR touching `oteryn-client/Cargo.lock`;
- this task exclusively leases `oteryn-client/Cargo.lock` for the bounded finalizer;
- architecture category `protocol-canary` permits the `game-domain` dependency;
- generated P1 index is pinned to `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`, release 3.6.1, client 1525, profile `current`;
- real wire admission is intentionally fail-closed and must remain so.

# Acceptance

## Phase 1 — baseline alignment

- [ ] development runtime metadata mechanically agrees with the generated `current-index.json` revision, release, client version, profile and enabled-feature/source-hash evidence;
- [ ] historical cuts remain explicit historical evidence and are not silently called current;
- [ ] descriptor/debug output remains non-secret and bounded;
- [ ] tests consume the generated index as read-only evidence and fail on drift;
- [ ] real admission remains `RealAdmissionUnavailable` and no credential/network lifecycle is weakened;
- [ ] evidence document distinguishes inspected development baseline from deployed runtime equality;
- [ ] focused format, strict Clippy and complete package tests pass;
- [ ] fresh source-provenance/trust/API audit has zero open material finding.

## Phase 2 — bounded gameplay wire mapping

- [ ] exact provenance-safe source/fixture evidence is classified per required M2 family;
- [ ] unsupported field layouts remain explicit `UNKNOWN` and are not guessed;
- [ ] only exactly supported bootstrap/map/entity/movement/logout decode/encode families enter the package;
- [ ] malformed/truncated/trailing/oversized/invalid-order/stale-session input fails closed;
- [ ] merged `GameEvent`/`GameCommand` remain the only semantic envelopes;
- [ ] parser owns no simulation, renderer, asset, input, UI or app state;
- [ ] component/fuzz-style negative evidence passes for every implemented layout;
- [ ] any `game-domain` dependency and lockfile delta occur only after exclusive validation under a serialized shared lease;
- [ ] exact-head Windows workspace, architecture, Supply Chain and repository CI pass;
- [ ] implementation protected-merges and the shared lease releases at the phase boundary.

## Claim boundary

Source declarations, opcodes and dispatch phases prove source shape only. They do not prove deployed revision, configuration, ordering, field layout or compatibility. Missing exact layout evidence blocks that subfamily; it never authorizes inference from neighboring handlers.

## Context checkpoint

```yaml
checkpoint_version: 3
updated_at: 2026-08-03T08:24:00+02:00
head_before_lease_commit: ff6e962c0a43e12bd87cc220e1b7fdeed86dc730
branch: feat/OTC2-20260803-playability-p2-canary-world-protocol
pr: 188
status: implementing
phase: isolated-finalizer
proven:
  - PR 188 contains development metadata alignment to generated source index bc0068ab80bbf003e128fce0589b4cc89d2682d3.
  - PR 188 contains a bounded single-byte encoder for eight step directions, stop movement and logout.
  - Unsupported semantic commands and stale session envelopes have explicit negative tests.
  - Real Canary admission remains fail-closed before network I/O.
  - No review comments, requested changes or unresolved review threads exist.
  - No other open Rust Client PR owns the shared Cargo lockfile path.
material_findings:
  - id: P2-CANARY-FINALIZER-001
    severity: high
    disposition: repair_pending
  - id: P2-CANARY-FINALIZER-002
    severity: high
    disposition: repair_pending
  - id: P2-CANARY-DRIFT-001
    severity: medium
    disposition: repair_pending
shared_path_lease:
  path: oteryn-client/Cargo.lock
  holder: OTC2-20260803-playability-p2-canary-world-protocol
  scope: regenerate only the protocol-canary dependency edge and validate the exact delta
validation:
  - open-PR overlap preflight: PASS
  - task/branch/PR continuity preflight: PASS
blockers: []
next_action: Add one self-contained push-triggered isolated finalizer, generate Cargo.lock with Cargo, export command.rs, repair the direction-scoped drift assertion, run focused validation, remove all temporary workflows, and push the coherent exact-head commit to PR 188.
```