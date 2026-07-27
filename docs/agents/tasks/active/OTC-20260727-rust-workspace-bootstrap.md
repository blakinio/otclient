---
task_id: OTC-20260727-rust-workspace-bootstrap
status: awaiting_final_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R01
branch: ci/OTC-20260727-rust-workspace-bootstrap
base_branch: main
created: 2026-07-27T01:20:00+02:00
updated: 2026-07-27T10:00:00+02:00
last_verified_commit: "6522ded9049ed3a3de8fe7f3d7bcb2a966cf252a"
risk: medium
related_pr: "#50"
depends_on:
  - merged PR #47 foundation audit
  - merged PR #49 audit task archival
blocks:
  - Rust foundation primitives crate
  - renderer/domain/asset/protocol workstreams
owned_paths:
  - oteryn-client/Cargo.toml
  - oteryn-client/Cargo.lock
  - oteryn-client/rust-toolchain.toml
  - oteryn-client/rustfmt.toml
  - oteryn-client/deny.toml
  - oteryn-client/tools/architecture-check/**
  - oteryn-client/tests/architecture-fixtures/**
  - oteryn-client/docs/operations/RUST_WORKSPACE.md
  - oteryn-client/docs/agents/prompts/NEXT_FOUNDATION_AGENT.md
  - .github/workflows/rust-client.yml
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260727-rust-workspace-bootstrap.md
crates_touched:
  - oteryn-architecture-check
features_touched: []
contracts_touched: []
modules_touched: []
reuses:
  - foundation audit bootstrap recommendation
  - existing repository required-check and Windows-only compilation policy
  - pinned repository action policy
public_interfaces:
  - Rust workspace metadata and lint policy
  - architecture category and dependency-edge policy
  - stable architecture violation codes
  - path-scoped Rust Windows and supply-chain CI entry point
cross_repo_tasks: []
---

# Goal

Create the smallest production-quality Rust workspace foundation for the greenfield Oteryn client: one architecture-policy tool, synthetic dependency-graph fixtures, pinned stable toolchain, lint/supply-chain policy and additive CI. Do not add any product application or engine crate.

# Acceptance criteria

- [x] Rust `1.94.0` is pinned and successfully installed on the required Windows x86-64 MSVC runner.
- [x] Workspace contains exactly one member: `oteryn-architecture-check`.
- [x] No placeholder application, renderer, protocol, domain, UI, asset, audio or feature crate exists.
- [x] Generated `Cargo.lock` is committed and required Cargo commands use `--locked` where supported.
- [x] Unsafe Rust is forbidden by workspace policy.
- [x] Architecture checker validates the real workspace and synthetic policy graphs.
- [x] Valid fixture passes and every required invalid fixture reports the expected stable rule family.
- [x] Dependencies escaping into legacy `src/`, `modules` or `mods` paths are rejected.
- [x] Dependency cycles, forbidden category edges, unresolved path dependencies and unapproved sources are rejected with actionable errors.
- [x] Dependency/license/advisory policy is documented and uses an immutable official cargo-deny action pin.
- [x] Rust CI is additive and path-scoped; no legacy workflow file or required check was weakened.
- [x] The Windows job covers locked metadata, formatting, Clippy, tests and real architecture validation.
- [x] Supply-chain policy is a separate job and does not substitute for Windows compilation/testing.
- [x] Workspace operations, module catalogue, validation matrix and changelog are current.
- [x] A copy-ready prompt for the next bounded foundation agent is committed.
- [x] Complete 23-file changed-path and full-patch review is recorded on the final implementation head.
- [ ] Exact-head Rust Windows, Rust supply-chain and repository required checks pass.
- [ ] Autonomous merge gate is satisfied.

# Confirmed context

- Foundation audit and lifecycle archive are merged.
- The audit authorized this package only; product implementation remains out of scope.
- Rust `1.94.0` dated 2026-07-02 was selected from current stable metadata and has installed successfully in Windows CI.
- Current official cargo-deny action commit `3c6349835b2b7b196a839186cb8b78e02f7b5f25` contains cargo-deny `0.20.2` and is pinned immutably.
- PR #48 is a separate draft operational analysis and does not overlap implementation paths.
- PR #36 and its archive #51 merged while this PR was open; their option behavior and changelog entry were preserved.
- This task adds one new workflow and does not modify the existing legacy CI workflow graph.

# Delivered implementation

## Workspace policy

- one workspace member under `tools/architecture-check`;
- Rust edition 2024 and minimum/pinned Rust `1.94`/`1.94.0`;
- committed generated lockfile;
- unsafe forbidden and strict Rust/Clippy workspace lints;
- narrow explicit dependency and license policy;
- only `serde_json` as the application-workspace external dependency.

## Architecture checker

The checker consumes locked Cargo metadata or schema-versioned synthetic JSON and validates:

- `oteryn-` package-name prefix;
- recognized category metadata;
- package and path dependency containment inside `oteryn-client/`;
- approved crates.io source forms;
- forbidden architecture-category edges;
- unresolved workspace path dependencies;
- dependency cycles;
- duplicate package names.

Stable codes: `E001`, `E002`, `E003`, `E004`, `E005`, `E006`, `E008`, `E009`.

Synthetic fixtures cover a valid minimal workspace plus legacy path, domain-to-Canary, renderer-to-feature, UI-core-to-feature, feature cycle and unapproved-source failures.

## CI and operations

- `Rust Client / Windows`: pinned toolchain, locked metadata, format, Clippy, tests and real workspace policy.
- `Rust Client / Supply Chain`: immutable official cargo-deny action, advisories, licenses, bans and sources.
- existing legacy workflows remain unchanged.
- `RUST_WORKSPACE.md` documents commands, categories, rule codes, adding crates and rollback.

## Next-agent prompt

`oteryn-client/docs/agents/prompts/NEXT_FOUNDATION_AGENT.md` is a standalone prompt for one standard-library-first `oteryn-foundation` primitives package. It explicitly excludes protocol identifiers, application/runtime systems and additional placeholder crates.

# Work log

## 2026-07-27T01:20:00+02:00

- Created the bounded WS-R01 task, branch and draft PR #50 after audit/archive merge and overlap inspection.
- Claimed only the one-member workspace, architecture policy, one additive workflow and required governance docs.

## Workspace implementation

- Added the pinned workspace/toolchain/lint/deny configuration.
- Implemented the architecture checker CLI/library and seven synthetic graph fixtures.
- Added Windows Rust CI and workspace operations documentation.
- Added no product crate, runtime behavior, protocol constant, asset, credential or external-repository write.

## CI repair evidence

- Initial manually written lockfile was rejected by locked metadata; CI was used to generate the authoritative lockfile, which was then committed.
- Pinned `rustfmt` identified formatting differences; generated formatting was inspected and committed, after which formatting passed.
- Strict Clippy identified two collapsible nested conditions; diagnostics were captured, the conditions were converted to let-chains and Clippy passed.
- Windows metadata, Clippy, unit/integration fixture tests and real architecture validation have all passed on repair heads.
- Temporary repair artifact/log steps were removed from the final workflow.
- Slow source compilation of an older cargo-deny release was replaced with the current immutable official action in a separate Ubuntu supply-chain job; Windows remains the required compiled job.
- The next-agent prompt was added at the user's request.

## Final review

- Reviewed the complete 23-file PR path list and full patch against current `main` after options PR #36/#51 merged.
- Preserved the merged deterministic-options changelog entry.
- Confirmed the diff contains one workflow, one tool crate, seven metadata-only fixtures, workspace policy files, operations/prompt/governance documentation and this task only.
- Confirmed no client/launcher executable, renderer, protocol, domain, UI, asset, audio, feature or placeholder crate is present.
- Confirmed no legacy source/runtime dependency, protocol constant, game asset, credential, private capture, generated build output or external-repository write is present.
- Confirmed temporary lock/format/Clippy diagnostic artifact steps are absent from the final workflow.
- Confirmed the official supply-chain action and checkout action use immutable commit pins.

# Validation and CI

| Commit/run | Check | Result | Evidence |
|---|---|---|---|
| `a10c6c7620d5b28b7d68060dd8427e4766f63cc2` | base/preflight | PASS | audit/archive merged; no overlapping owned paths |
| run `30224914936` | first Windows bootstrap | expected failure | exposed invalid hand-authored lockfile |
| run `30244788743` | generated lock + format discovery | partial PASS | locked metadata passed after generation; formatting delta captured |
| run `30245288403` | strict Clippy discovery | expected failure | two actionable `collapsible_if` findings captured |
| run `30245617416` | repaired Rust source | PASS through architecture validation | metadata, format, Clippy, tests and real checker passed; old cargo-deny install superseded |
| `6522ded9049ed3a3de8fe7f3d7bcb2a966cf252a` | complete changed-file/full-patch review | PASS | 23 declared files; merged-main changelog preserved; no out-of-scope runtime/content |
| final task-record head | Windows + supply-chain + repository required checks | pending | run after ready transition |

# Rejected approaches

- creating the complete planned crate tree as placeholders;
- adding `wgpu`, windowing, async, network, text, audio or WASM dependencies during bootstrap;
- linking legacy C++/Lua/OTUI runtime code;
- hand-maintaining a guessed lockfile after Cargo rejected it;
- relaxing formatting or Clippy policy instead of repairing source;
- retaining temporary CI artifact/debug steps;
- compiling stale cargo-deny from source in the Windows product job;
- weakening license/source policy to obtain green CI;
- expanding the architecture checker into a source parser or second build system.

# Risks and compatibility

- Runtime: no client runtime or user-data migration exists.
- Legacy compatibility: legacy source/build/workflows are unchanged.
- Rust compatibility: only Windows x86-64 MSVC compilation is claimed.
- Security: unsafe is forbidden; unknown registries/git sources and unapproved licenses are denied; no secrets are present.
- Architecture: metadata rules are a guardrail, not a substitute for ADR/source review.
- Rollback: normal squash revert removes the workspace/tooling/CI foundation.

# Remaining work

1. Update PR #50 body with final implementation/review state.
2. Mark ready and pass exact-head Windows, supply-chain and repository required checks.
3. Recheck mergeability, comments, reviews and unresolved threads; squash-merge only under the autonomous gate.
4. Archive this task in a separate lifecycle PR.
5. Do not start the next crate; hand off using `NEXT_FOUNDATION_AGENT.md`.

# Handoff

## Start here

- `oteryn-client/docs/operations/RUST_WORKSPACE.md`
- `oteryn-client/docs/agents/prompts/NEXT_FOUNDATION_AGENT.md`
- `oteryn-client/docs/audits/foundation/10-bootstrap-recommendation.md`

## Do not repeat

Do not add product placeholder crates, application dependencies or unresolved Platform/Canary identifiers to the foundation package.

## First next action

After this PR and its archive merge, give a fresh agent the committed `NEXT_FOUNDATION_AGENT.md` prompt for one bounded standard-library-first foundation primitives crate.

# Completion

- Final status: awaiting final CI
- PR: #50
- Merge commit: pending
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: pending
