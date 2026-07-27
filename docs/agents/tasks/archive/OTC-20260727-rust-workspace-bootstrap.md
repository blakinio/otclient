---
task_id: OTC-20260727-rust-workspace-bootstrap
status: completed
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R01
branch: ci/OTC-20260727-rust-workspace-bootstrap
base_branch: main
created: 2026-07-27T01:20:00+02:00
updated: 2026-07-27T10:25:00+02:00
last_verified_commit: "2903abc116b1523a9be62e689b715cd50eea28d8"
risk: medium
related_pr: "#50"
depends_on:
  - merged PR #47 foundation audit
  - merged PR #49 audit task archival
blocks: []
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
  - docs/agents/tasks/archive/OTC-20260727-rust-workspace-bootstrap.md
crates_touched:
  - oteryn-architecture-check
features_touched: []
contracts_touched: []
modules_touched: []
public_interfaces:
  - Rust workspace metadata and lint policy
  - architecture category and dependency-edge policy
  - stable architecture violation codes
  - path-scoped Rust Windows and supply-chain CI entry point
cross_repo_tasks: []
---

# Goal

Create the smallest production-quality Rust workspace foundation for the greenfield Oteryn client: one architecture-policy tool, synthetic dependency-graph fixtures, pinned stable toolchain, lint/supply-chain policy and additive CI, without adding product application or engine crates.

# Completion summary

PR #50 delivered the single WS-R01 package authorized by the foundation audit:

- exactly one workspace member, `oteryn-architecture-check`;
- Rust `1.94.0`, edition 2024 and Windows x86-64 MSVC target;
- Cargo-generated committed lockfile;
- unsafe-forbidden and strict Rust/Clippy workspace policy;
- explicit cargo-deny advisory/license/ban/source policy;
- metadata/graph architecture validation with stable rule codes;
- one valid and six focused invalid synthetic fixtures;
- additive Windows Rust and supply-chain CI;
- workspace operations documentation;
- copy-ready prompt for the next bounded foundation agent.

No client/launcher executable, renderer, protocol, game domain, UI, asset runtime, audio, feature or placeholder product crate was added. No legacy runtime dependency, protocol constant, proprietary asset, credential, private capture or external-repository write was introduced.

# Delivered architecture policy

The checker validates:

- `oteryn-` package names;
- recognized architecture categories;
- containment under `oteryn-client/`;
- approved crates.io source forms;
- forbidden category edges;
- unresolved workspace path dependencies;
- dependency cycles;
- duplicate package names.

Stable rule codes:

```text
E001_PACKAGE_NAME
E002_UNKNOWN_CATEGORY
E003_OUTSIDE_WORKSPACE
E004_UNAPPROVED_SOURCE
E005_FORBIDDEN_EDGE
E006_DEPENDENCY_CYCLE
E008_UNKNOWN_WORKSPACE_DEP
E009_DUPLICATE_PACKAGE
```

# Validation

| Evidence | Result |
|---|---|
| complete 23-file changed-path and full-patch review | PASS |
| final feature head | `2903abc116b1523a9be62e689b715cd50eea28d8` |
| Rust Client run `30248454243` | PASS |
| Rust Client / Windows | PASS: pinned toolchain, locked metadata, rustfmt, Clippy, tests and real architecture policy |
| Rust Client / Supply Chain | PASS: advisories, licenses, bans and sources |
| repository CI run `30248454375` | PASS |
| Detect Build Scope, both Fast Checks, Lua Syntax and `CI / Required` | PASS |
| legacy Windows build | correctly skipped because final PR diff did not enter legacy compile scope |
| PR comments/reviews/threads | none |
| mergeability | mergeable on current `main` |

# CI repair history

- an invalid hand-authored lockfile was rejected and replaced with Cargo-generated output;
- pinned rustfmt differences and Windows checkout newline behavior were corrected rather than bypassed;
- strict Clippy `collapsible_if` findings were repaired;
- temporary lock/format/diagnostic repair workflow steps and write permission were removed;
- stale source compilation of cargo-deny was replaced with the immutable official cargo-deny action;
- the feature branch was synchronized with current `main` while preserving the exact 23-file product diff.

# Merge

- PR: #50
- Method: squash
- Feature head: `2903abc116b1523a9be62e689b715cd50eea28d8`
- Squash merge commit: `4fb1d2d987a2975f800f6c08fb7a76f53a07abb7`
- Merged: 2026-07-27

# Rejected approaches

- creating the complete planned crate tree as placeholders;
- adding GPU, windowing, async, network, text, audio or WebAssembly dependencies during bootstrap;
- linking legacy C++/Lua/OTUI runtime code;
- weakening formatting, Clippy, license or source policy to obtain green CI;
- retaining temporary CI repair/debug behavior;
- expanding the checker into a source parser or second build system.

# Next action

Give a fresh agent the committed prompt:

```text
oteryn-client/docs/agents/prompts/NEXT_FOUNDATION_AGENT.md
```

The prompt authorizes exactly one standard-library-first crate:

```text
oteryn-client/crates/foundation/
oteryn-foundation
```

Its bounded scope is typed generation primitives, deterministic monotonic time, cancellation ownership and narrow non-secret errors. It explicitly excludes unresolved Platform/Canary identifiers, protocol/domain/UI/renderer/assets, async runtime and additional placeholder crates.

# Completion

- Final status: completed
- PR: #50
- Merge commit: `4fb1d2d987a2975f800f6c08fb7a76f53a07abb7`
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: `docs/agents/tasks/archive/OTC-20260727-rust-workspace-bootstrap.md`
