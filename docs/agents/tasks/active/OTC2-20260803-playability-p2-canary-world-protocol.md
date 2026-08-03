---
task_id: OTC2-20260803-playability-p2-canary-world-protocol
status: ready
agent: "P2 Canary world protocol worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p2-canary-world-protocol
phase: finalizer-isolation-required
branch: feat/OTC2-20260803-playability-p2-canary-world-protocol
base_branch: main
created: 2026-08-03T02:04:00+02:00
updated: 2026-08-03T08:08:59+02:00
required_base_commit: "f1a5a1873dbb9ce164aefed7537d5c3004eeb696"
risk: high
related_pr: 188
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
invocation_started_at: 2026-08-03T07:57:00+02:00
last_progress_at: 2026-08-03T08:08:59+02:00
ci_checks_for_current_head: 1
ci_check_generation: finalizer-isolation
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Goal

Reconcile the Canary Current development runtime descriptor with the merged generated P1 source index, preserving fail-closed real admission, then implement only those bounded M2 bootstrap/map/entity/movement/logout mappings whose exact field layouts can be established from provenance-safe evidence.

# Proven launch state

- P1 aggregation implementation #184 and archive #185 are merged;
- P2 simulation/snapshot implementation #186 and archive #187 are merged;
- current exact base is `main@f1a5a1873dbb9ce164aefed7537d5c3004eeb696`;
- all prior shared integration leases are released;
- no open PR owns `protocol-canary`, its P2 evidence path or integration-test path;
- architecture category `protocol-canary` already permits the later `game-domain` dependency;
- generated P1 index is pinned to `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`, release 3.6.1, client 1525, profile `current`;
- current runtime descriptor still names source revisions `95b276db311cf6e9acd58b847f1fb0ca6697b137` and `4b2d6f432d92628c42bde1d95daed6ae0d0eb88f`;
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
- [ ] implementation protected-merges, task archives separately and lease releases.

## Claim boundary

Source declarations, opcodes and dispatch phases prove source shape only. They do not prove deployed revision, configuration, ordering, field layout or compatibility. Missing exact layout evidence blocks that subfamily; it never authorizes inference from neighboring handlers.

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-03T08:08:59+02:00
head_before_checkpoint: fc4e1740362e4a8e00e7088d7c2156bef34fbb08
branch: feat/OTC2-20260803-playability-p2-canary-world-protocol
pr: 188
status: ready
phase: finalizer-isolation-required
proven:
  - PR 188 contains development metadata alignment to generated source index bc0068ab80bbf003e128fce0589b4cc89d2682d3.
  - PR 188 contains a bounded single-byte encoder for eight step directions, stop movement and logout.
  - Unsupported semantic commands and stale session envelopes have explicit negative tests.
  - Real Canary admission remains fail-closed before network I/O.
  - No review comments, requested changes or unresolved review threads exist.
material_findings:
  - id: P2-CANARY-FINALIZER-001
    severity: high
    evidence: oteryn-client/crates/protocol-canary/Cargo.toml adds oteryn-game-domain while oteryn-client/Cargo.lock lacks the corresponding package dependency entry.
    impact: cargo metadata --locked and required Rust Client CI fail.
    disposition: open
  - id: P2-CANARY-FINALIZER-002
    severity: high
    evidence: command.rs exists but lib.rs does not yet declare and re-export the command module.
    impact: the bounded encoder is not part of the public package build and its unit tests are not compiled by the crate.
    disposition: open
  - id: P2-CANARY-DRIFT-001
    severity: medium
    evidence: generated-index command test selects the first matching opcode before constraining direction and dispatch phase.
    impact: a duplicate server-to-client opcode could satisfy or invalidate the assertion incorrectly.
    disposition: repair prepared in the reviewed finalizer but not committed
execution_history:
  - cycle: 1
    head: 820ec0dab017898d3c19a7a27a6efff3f609c5b5
    result: finalizer rejected a stale trigger-parent race
  - cycle: 2
    head: b8f347bdd98c51f5dc638833ac008554a58a1708
    result: trigger bootstrap repaired, but no executable finalizer check was created for the new head
  - cycle: 3
    head: fc4e1740362e4a8e00e7088d7c2156bef34fbb08
    result: direct self-finalizer workflow was prepared, but no executable finalizer check was created for the new head
validation:
  - required Windows CI on 0dd5397624dab678591a9bc1c526a3df501b32e6: FAIL at cargo metadata --locked due to Cargo.lock drift
  - independent static provenance/trust/API audit: FAIL with two open high findings and one open medium finding above
  - E2E: NOT_APPLICABLE for this isolated non-network contract-producer phase; controlled playable-client E2E belongs to later P2 integration and acceptance tasks
repair_cycles_for_current_gate: 3
blocker: Current invocation exhausted the maximum three repair cycles for the finalizer gate; repository policy requires a fresh isolation phase rather than another trigger variation.
next_action: In a fresh session, execute one new bounded finalizer isolation path that does not reuse the pull_request synchronize trigger chain, generates Cargo.lock with Cargo, exports command.rs from lib.rs, applies the direction-scoped drift test, runs fmt/Clippy/tests/architecture, removes all temporary workflows, and commits the coherent result to PR 188.
```