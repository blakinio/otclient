---
task_id: OTC-20260728-rust-diagnostics-foundation
coordination_id: ""
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R14
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-DIAG
parallel_lane_state: validating
coordinator_task: none
branch: feat/OTC-20260728-rust-diagnostics-foundation
base_branch: main
created: 2026-07-28T22:45:50+02:00
updated: 2026-07-28T23:01:30+02:00
last_verified_commit: "01de42984e72f9bb7c71853d030b68b2411ddbff"
required_base_commit: "c26e2df6888b70c7120760c88bcff4f3fcc0ac97"
risk: medium
related_issue: ""
related_pr: "#61"
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
  - CorrelationId
  - DiagnosticBuildError
  - DiagnosticCategory
  - DiagnosticCode
  - DiagnosticEvent
  - DiagnosticField
  - DiagnosticValue
  - FieldKey
  - SafeText
  - SensitiveKind
  - SensitiveValue
  - Severity
  - StaticTextError
  - TechnicalContext
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - redaction occurs at value creation and does not retain source text
  - sensitive values cannot expose contents through Debug or Display
  - arbitrary runtime strings have no implicit conversion to safe diagnostic values
---

# Goal

Add exactly one standard-library-first `oteryn-diagnostics` crate that provides bounded structured diagnostic events and redaction-at-creation contracts without installing logging, sinks, uploaders or runtime services.

# Acceptance criteria

- [x] Exactly one new production crate exists under `oteryn-client/crates/diagnostics/`.
- [x] Severity, category, code, technical context and fields are structured and bounded.
- [x] Arbitrary external text cannot silently become a safe field.
- [x] Sensitive values are irreversibly redacted when entering the diagnostic representation.
- [x] Public `Debug` and `Display` output cannot reveal sensitive marker values.
- [x] Synthetic regression tests cover token-, authorization-code-, PKCE-, ticket-, cookie-, private-chat- and personal-path-shaped values.
- [x] No global logger/subscriber, tracing integration, sink, upload, crash-report, support-bundle, replay, async runtime, thread, protocol, auth, asset, renderer, UI or legacy implementation is added.
- [ ] Workspace metadata, formatting, Clippy, tests, architecture validation, cargo-deny and exact-head required CI pass on this final task-record head.
- [x] Complete changed-file and full-diff review passes with no unrelated paths.
- [x] Module catalogue, build/test matrix and changelog are current.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- Required base and current `main` remain identical at `c26e2df6888b70c7120760c88bcff4f3fcc0ac97` after implementation validation.
- Foundation PR #54 is merged and archived by PR #58.
- The accepted W2 plan authorizes W2-DIAG as the sole diagnostics contract producer and shared Cargo integration lease holder.
- Open PRs #23, #37 and #48 do not own the Rust diagnostics crate, contract, Cargo workspace or this task path.
- The architecture checker already recognizes category `diagnostics`; checker, fixtures, Rust CI, toolchain and deny policy remain unchanged.
- Local Cargo execution is unavailable because the sandbox cannot resolve GitHub; exact GitHub Actions Windows and supply-chain runs provide required compiled evidence.

# Delivered contract

- Added exactly one package, `oteryn-diagnostics`, with an exact local dependency on merged `oteryn-foundation` `=0.1.0`.
- Added closed `Severity`, `DiagnosticCategory`, numeric `DiagnosticCode` and non-secret `CorrelationId` types.
- Added reviewed static `SafeText` and `FieldKey` constructors with fixed UTF-8 byte limits and closed errors that never retain rejected text.
- Added `SensitiveKind` and `SensitiveValue::redacted`; source text is accepted only for explicit classification and is not stored.
- Added `DiagnosticValue` without an arbitrary owned-string variant or implicit runtime-string conversion.
- Added generation-aware `TechnicalContext`, deterministic `DiagnosticField` formatting and `DiagnosticEvent` with at most 16 uniquely keyed fields.
- Added compile-fail evidence for arbitrary `String` conversion plus deterministic unit/doctests using clearly synthetic secret-shaped marker values.
- Registered the crate in the workspace and updated the generated lockfile, catalogue, validation matrix and changelog.

# Ownership and overlap review

- PR #61 changes exactly eight declared paths: the crate, Cargo workspace/lockfile, three shared agent documents and this task record.
- No architecture-check, fixture, workflow, toolchain, deny-policy, protocol, authentication, asset, renderer, UI, legacy-runtime or external-repository path changed.
- One incidental documentation-format change found during full diff review was removed before final validation.
- PR #37 and #23 remain responsible for restacking their stale shared-document changes after this producer merge if they remain active.

# Security review

- Sensitive source strings are not fields of `SensitiveValue` and are discarded at construction.
- `Debug` and `Display` expose only `<redacted:<classification>>` markers.
- Safe textual values require explicit reviewed `'static` construction and are bounded; runtime `String` has no implicit safe conversion.
- Event field count and key length are bounded; duplicate field keys are rejected with closed non-secret errors.
- Tests use only clearly synthetic marker strings and one synthetic Windows path; no real token, endpoint, capture, private chat or personal path is present.
- Diagnostics remain optional for correctness and own no authoritative state or background activity.

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `c26e2df6888b70c7120760c88bcff4f3fcc0ac97` | live preflight and overlap review | PASS | W2-DIAG unclaimed; exact required base |
| `44e9aee19044461519ce86c1a415a30dc6ca6c29` | Rust Client run `30398275457` | FAIL, fixed | cargo-deny rejected an unversioned path dependency; Windows rustfmt also reported deterministic formatting changes |
| `45648cf04eb66c05253c95bedc7c0f00c8e07d48` | Rust Client run `30398564142` | FAIL, fixed | supply-chain issue resolved; one remaining rustfmt line reported and corrected |
| `1bdeb1eb729d8758d7aca35328a88da819a021d7` | Rust Client run `30398757545` | PASS | locked metadata, rustfmt, Clippy, workspace tests, doctests, architecture policy and supply-chain all passed |
| `1bdeb1eb729d8758d7aca35328a88da819a021d7` | repository CI run `30398758094` | PASS | scope, syntax/workflow, Lua syntax, informational analysis and `CI / Required` passed; legacy Windows build skipped correctly |
| `01de42984e72f9bb7c71853d030b68b2411ddbff` | final implementation/diff review | PASS | secret-shaped synthetic cases strengthened; unrelated documentation wording restored; exact eight-file scope retained |
| final task-record head | exact-head Rust Client and repository CI | pending | required after this durable validation update |
| unavailable locally | Cargo commands | documented unavailable | local sandbox cannot resolve GitHub; no local success claim |

# Risks and compatibility

- Runtime: contract-only crate; no logger, sink, upload, crash-report, replay or product runtime compatibility claim.
- Data/migration: none.
- Performance: no product performance claim; event count and textual inputs are bounded.
- Backward compatibility: additive workspace member only.
- Cross-repository rollout: none.
- Rollback: a normal squash revert removes the crate and workspace registration.

# Remaining work

1. Pass exact-head Rust Client and repository required CI on this final task-record commit.
2. Mark PR #61 ready, inspect all comments/reviews/threads and current mergeability, then squash-merge through the autonomous gate.
3. Archive this task in a separate lifecycle PR and release the shared-path lease.

# Completion

- Final status: awaiting exact-head CI
- PR: #61
- Merge commit: pending
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: pending
