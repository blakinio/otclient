---
task_id: OTC2-20260801-complete-architecture-policy
status: completed
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: architecture
phase: archived
branch: fix/OTC2-20260801-complete-architecture-policy
base_branch: main
created: 2026-08-01T11:50:00+02:00
updated: 2026-08-01T13:55:00+02:00
last_verified_commit: "68f712a8bd3787d0b469c64cd2655d21de799725"
required_base_commit: "f6e7fedfe32b1ee0712a2b5d97cdf11a98362d63"
implementation_merge: "abe0c8c6a96026ba874f3fc58fa84eae3444b699"
related_pr: 129
risk: high
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: codex
blocks:
  - OTC2-20260801-safe-asset-open-remediation
---

# Result

`OTC2-AUD-004` is remediated and merged through PR #129.

The architecture checker now retains Cargo dependency kind and applies one complete allow policy across all 29 known categories for normal, build and dev edges. Normal product-to-tool dependencies are denied; dev dependencies may target tool packages; build dependencies are denied except the explicit `tool -> foundation` and `tool -> asset-types` pairs. `E005_FORBIDDEN_EDGE` remains the stable violation code.

Fixture schema v2 requires dependency kind while archived schema v1 remains readable with missing kind interpreted as normal. Exhaustive tests compare the policy decision with parsed fixture output for all `29 x 29 x 3 = 2523` combinations. The unchanged 19-member workspace graph passes.

# Durable artifacts

- `oteryn-client/tools/architecture-check/src/lib.rs`
- `oteryn-client/tools/architecture-check/tests/policy_fixtures.rs`
- `oteryn-client/docs/architecture/decisions/2026-08-01-complete-dependency-allow-policy.md`
- implementation PR #129
- implementation merge `abe0c8c6a96026ba874f3fc58fa84eae3444b699`

# Validation

Exact head `68f712a8bd3787d0b469c64cd2655d21de799725`:

- Rust Client run `30698432805` — PASS;
- Windows job `91365129660` — PASS: locked metadata, rustfmt, strict Clippy, full workspace tests and real-workspace architecture validation;
- Supply Chain job `91365129677` — PASS;
- CI run `30698432863` — PASS;
- required job `91365225623` — PASS;
- exact changed-file review — four declared paths only;
- comments, reviews and unresolved threads — none.

# Boundaries

No manifest, lockfile, workspace-member, dependency, workflow, R3 asset-open or external-repository path changed.

# Next action

Run a fresh ownership, overlap and primitive-discovery preflight for `R3-ASSET-OPEN` against current `main` before authorizing implementation.
