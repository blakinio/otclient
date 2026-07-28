---
task_id: OTC-20260728-rust-diagnostics-foundation
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R14
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-DIAG
parallel_lane_state: active
coordinator_task: none
branch: feat/OTC-20260728-rust-diagnostics-foundation
base_branch: main
created: 2026-07-28T22:45:50+02:00
updated: 2026-07-28T22:45:50+02:00
last_verified_commit: "c26e2df6888b70c7120760c88bcff4f3fcc0ac97"
required_base_commit: "c26e2df6888b70c7120760c88bcff4f3fcc0ac97"
risk: medium
related_issue: ""
related_pr: pending
depends_on:
  - merged PR #54 foundation primitives
  - merged PR #58 foundation task archive
integration_after:
  - "c26e2df6888b70c7120760c88bcff4f3fcc0ac97"
blocks:
  - later diagnostics sinks and support tooling
owned_paths:
  - oteryn-client/crates/diagnostics/**
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260728-rust-diagnostics-foundation.md
shared_path_lease:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
contract_role: producer
contracts_produced:
  - oteryn-diagnostics structured event and redaction-at-creation contract
contracts_consumed:
  - merged oteryn-foundation technical time and generation primitives
crates_touched:
  - oteryn-diagnostics
features_touched: []
contracts_touched:
  - structured diagnostic event contract
  - safe and sensitive diagnostic value construction
modules_touched: []
reuses:
  - oteryn-foundation Moment and technical generation primitives
  - existing diagnostics architecture category
  - existing Rust workspace lint and supply-chain policy
public_interfaces:
  - DiagnosticEvent
  - DiagnosticField
  - DiagnosticValue
  - SafeText
  - SensitiveValue
  - Severity
  - DiagnosticCategory
  - DiagnosticCode
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - redaction occurs at value creation
  - sensitive values cannot expose contents through Debug or Display
---

# Goal

Add exactly one standard-library-first `oteryn-diagnostics` crate that provides bounded structured diagnostic events and redaction-at-creation contracts without installing logging, sinks, uploaders or runtime services.

# Acceptance criteria

- [ ] Exactly one new production crate exists under `oteryn-client/crates/diagnostics/`.
- [ ] Severity, category, code, technical context and fields are structured and bounded.
- [ ] Arbitrary external text cannot silently become a safe field.
- [ ] Sensitive values are irreversibly redacted when entering the diagnostic representation.
- [ ] Public `Debug` and `Display` output cannot reveal sensitive marker values.
- [ ] Synthetic regression tests cover token-, authorization-code-, PKCE-, ticket-, cookie-, private-chat- and personal-path-shaped values.
- [ ] No global logger/subscriber, tracing integration, sink, upload, crash-report, support-bundle, replay, async runtime, thread, protocol, auth, asset, renderer, UI or legacy implementation is added.
- [ ] Workspace metadata, formatting, Clippy, tests, architecture validation, cargo-deny and exact-head required CI pass.
- [ ] Complete changed-file and full-diff review passes with no unrelated paths.
- [ ] Module catalogue, build/test matrix and changelog are current.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- Current `main` is `c26e2df6888b70c7120760c88bcff4f3fcc0ac97`.
- Foundation PR #54 is merged and archived by PR #58.
- The accepted W2 plan authorizes W2-DIAG as the sole diagnostics contract producer and shared Cargo integration lease holder.
- Open PRs #23, #37 and #48 do not own the Rust diagnostics crate, contract, Cargo workspace or this task path.
- The architecture checker already recognizes category `diagnostics`; checker and fixture changes are read-only by default.
- Local sandbox GitHub DNS is unavailable, so local Cargo execution is unavailable; exact GitHub Actions results are required before merge.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Oteryn foundation primitives, PR #54 | technical `Moment` and generation types only where useful | `oteryn-client/crates/foundation/**` | generic, merged, standard-library-only lower layer |
| Rust workspace policy, PR #50 | manifests, lints, architecture category and CI | `oteryn-client/Cargo.toml`, `deny.toml`, `rust-client.yml` | current integration contract |
| Current parallel wave, PR #59 | exact W2-DIAG scope and lease | `oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md` | accepted launch plan |

# Ownership and overlap check

- Open PRs inspected: #23, #37, #48.
- Active tasks inspected: their matching task records plus current Rust coordination/archive evidence.
- Overlaps: PR #37 and #23 also touch shared catalogue/changelog files, but neither owns Rust Cargo or diagnostics; their branches are stale and must restack after this producer merge if still active.
- Resolution: this task holds the W2 shared-path lease; shared documentation edits remain narrow and later legacy branches must preserve current `main`.

# Parallel-lane safety

- Safe concurrency: the exclusive crate path is new and the three W2 evidence paths remain docs-only and disjoint.
- Exclusive paths/contracts: `crates/diagnostics/**`, the diagnostics public contract and the declared shared integration paths.
- Read-only shared paths: architecture checker/fixtures, Rust CI, toolchain and deny policy unless a proven defect appears.
- Contract role: producer; no consumer compatibility is claimed before merge.
- Validation invalidation: any newer `main` change to Cargo, lockfile, workspace policy or produced contract requires restack and full revalidation.
- `integration_ready`: crate implementation complete but shared integration unavailable; not expected because this task currently holds the lease.
- `blocked`: competing diagnostics producer, missing required base, security boundary violation or CI requiring weakened checks.
- Merge independence: may merge independently of W2 evidence lanes because it consumes only merged foundation contracts.
- Lease release: the separate archive lifecycle PR records release after implementation merge.

# Current state

Task and branch claimed. Draft PR will be opened before broad implementation.

# Plan

1. Open an early draft PR.
2. Implement one bounded crate with closed enums, typed safe/sensitive values and deterministic bounded events.
3. Integrate the crate into Cargo and update shared documentation.
4. Review the complete diff and drive exact-head CI to green.
5. Mark ready, squash-merge, then archive this task in a separate PR.

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `c26e2df6888b70c7120760c88bcff4f3fcc0ac97` | live preflight and overlap review | PASS | W2-DIAG unclaimed; exact current main |
| pending | local Cargo commands | unavailable | sandbox cannot resolve github.com; GitHub Actions required |

# Risks and compatibility

- Runtime: contract-only crate; no runtime service or compatibility claim.
- Data/migration: none.
- Security: primary risk is accidental printable sensitive data; constructors and formatting tests must fail closed.
- Backward compatibility: new crate only.
- Cross-repo rollout: none.
- Rollback: normal squash revert removes the crate and workspace registration.

# Remaining work

1. Open the early draft PR.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: pending
- Changelog updated: pending
- Archived at: pending
