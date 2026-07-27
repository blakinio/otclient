# Next Rust Foundation Agent Prompt

Copy the block below into a fresh agent session after the WS-R01 workspace bootstrap is merged and archived.

```text
Work autonomously in repository:

blakinio/otclient

Task: implement the next bounded Gate 1 package for the greenfield Rust Oteryn client: one small, standard-library-first foundation crate for typed generations/identities, deterministic monotonic time, cancellation ownership and narrowly scoped non-secret errors.

Do not rely on previous chat history. Current Git, current main, root and nested AGENTS.md files, open PRs, active task records, merged foundation audit, architecture documents, the live Rust workspace and exact CI are source of truth.

Repository safety:

- routine writes only to blakinio/otclient;
- do not mutate Canary, Oteryn Platform, upstream or external repositories;
- never push directly to main;
- create one bounded task record, dedicated branch/worktree and early draft PR;
- inspect all open PRs, review threads and active tasks before claiming paths;
- do not edit paths owned by another active task;
- do not weaken Rust, legacy or required CI checks;
- do not commit credentials, tickets, private logs, proprietary assets, packet captures or generated build output.

Mandatory reads:

1. AGENTS.md
2. oteryn-client/AGENTS.md
3. oteryn-client/README.md
4. oteryn-client/docs/architecture/ARCHITECTURE.md
5. oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
6. oteryn-client/docs/architecture/CLIENT_LIFECYCLE.md
7. oteryn-client/docs/architecture/SECURITY_MODEL.md
8. oteryn-client/docs/architecture/PERFORMANCE_AND_TESTING.md
9. oteryn-client/docs/agents/PROGRAM.md
10. oteryn-client/docs/agents/WORKSTREAMS.md
11. oteryn-client/docs/audits/foundation/README.md
12. oteryn-client/docs/audits/foundation/08-risk-register.md
13. oteryn-client/docs/audits/foundation/09-gap-and-decision-log.md
14. oteryn-client/docs/audits/foundation/10-bootstrap-recommendation.md
15. oteryn-client/docs/operations/RUST_WORKSPACE.md
16. the archived WS-R01 bootstrap task and merged PR
17. all live open PRs, active tasks and exact required checks

Goal:

Deliver exactly one reusable crate, expected path/package:

- directory: oteryn-client/crates/foundation/
- package: oteryn-foundation

The crate provides small deterministic primitives needed by later application/domain/platform work without defining game behavior or choosing protocol/server contracts.

Before creating the crate, verify whether `foundation` is already a recognized workspace category and listed in REPOSITORY_LAYOUT.md. If not, update the layout, responsibility table, architecture checker category policy and synthetic fixtures in this same focused PR. Do not silently classify the crate as an unrelated existing category.

Required crate scope:

1. Typed generation/identity primitives
   - non-interchangeable newtypes for process/session/task generations where the architecture already proves the concept;
   - checked construction/increment/ordering where applicable;
   - no implicit conversion between unrelated identifiers;
   - no protocol opcodes or assumptions about Platform world ID, Canary world-list ID or Canary channel_id;
   - do not define CharacterId, WorldId or WorldChannelId until their owning contract/task selects exact semantics.

2. Deterministic monotonic time
   - a narrow monotonic clock interface suitable for lifecycle/domain tests;
   - a production implementation backed by monotonic standard-library time;
   - a deterministic manual/fake implementation for tests;
   - explicit duration/deadline behavior;
   - no wall-clock use for timeout ordering;
   - no global mutable clock singleton.

3. Cancellation ownership
   - small cloneable observation token plus explicit cancellation owner/source;
   - cancellation is idempotent and observable across clones;
   - deterministic cleanup/drop semantics are documented;
   - no async runtime dependency, executor, task scheduler or global event bus;
   - no hidden thread creation.

4. Narrow error types
   - errors only for these foundation primitives, such as exhausted generation or invalid monotonic operation;
   - errors are typed, deterministic and safe to display/debug;
   - no universal application error framework, anyhow-style public API or user-facing recovery taxonomy in this package;
   - no secrets or arbitrary external strings stored in errors.

Dependency policy:

- prefer zero external runtime dependencies;
- use only the Rust standard library unless a concrete requirement cannot be met safely;
- any external dependency requires current primary documentation, exact version, license/maintenance/unsafe analysis, deny-policy compatibility and explicit task/PR rationale;
- unsafe Rust remains forbidden;
- no native/FFI dependency;
- no async, network, GPU, windowing, HTTP/TLS, serialization, tracing or WASM dependency.

Architecture boundaries:

- `oteryn-foundation` may not depend on product/application/domain/protocol/UI/renderer/asset/feature crates;
- later crates may depend on it only for genuinely generic primitives;
- do not put GameEvent, GameCommand, map/entity storage, Identity, account session, game ticket, gameplay-channel routing, UI, renderer or asset logic here;
- do not create additional placeholder crates or directories;
- do not link or execute legacy C++/Lua/OTUI code.

Expected owned paths, subject to live overlap check:

- oteryn-client/crates/foundation/**
- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/tools/architecture-check/** only for the new category/edge policy
- oteryn-client/tests/architecture-fixtures/** only for focused foundation fixtures
- oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md if the crate/category is not already normative
- oteryn-client/docs/operations/RUST_WORKSPACE.md
- docs/agents/MODULE_CATALOG.md
- docs/agents/BUILD_TEST_MATRIX.md when validation policy changes
- docs/agents/CHANGELOG.md
- one active task record

Required tests:

- unrelated newtypes cannot be interchanged through public APIs;
- generation ordering and checked increment;
- defined behavior at maximum value without wraparound;
- production monotonic clock never reports time before its origin;
- manual clock deterministic advance and deadline checks;
- invalid backwards manual-clock movement is rejected or impossible by API;
- cancellation source is idempotent;
- all cloned tokens observe cancellation;
- dropping observers does not cancel unrelated work;
- dropping/cancelling the owner follows the documented invariant;
- repeated create/cancel/drop cycles leave no retained resources;
- thread-race smoke test for cancellation observation when the implementation is thread-safe;
- architecture fixture proving foundation may have no upward product dependency;
- real workspace architecture check passes.

Acceptance criteria:

- one new crate only, with one explicit architecture category;
- standard-library-only implementation unless separately proven otherwise;
- public API is small, documented and free of speculative game/server concepts;
- no unsafe code, panic/unwrap/expect/todo/unimplemented/debug macros under workspace policy;
- deterministic unit tests pass;
- `cargo metadata --locked --format-version 1` passes;
- `cargo fmt --all --check` passes;
- `cargo clippy --workspace --all-targets --locked -- -D warnings` passes;
- `cargo test --workspace --all-targets --locked` passes;
- real and synthetic architecture checks pass/fail as expected;
- cargo-deny advisories/licenses/bans/sources pass;
- required Windows Rust CI passes on the exact final head;
- existing repository required checks remain green;
- complete changed-file and full-diff review finds no product implementation, protocol constants, assets, secrets or out-of-scope paths;
- task, catalogue, operations documentation and changelog are current;
- PR is merged only through the autonomous merge gate and the completed task is archived separately.

Explicit non-goals:

- no application/window shell;
- no renderer or wgpu dependency;
- no protocol adapter, packet bytes or Canary constants;
- no Oteryn Identity, account session, game ticket or gameplay-channel mapping;
- no GameEvent/GameCommand design;
- no world/entity/map storage;
- no async runtime or networking;
- no tracing/crash reporting package;
- no UI/input/audio/assets/features;
- no performance claim beyond focused primitive tests/build evidence;
- no additional Gate 1 package in the same PR.

Implementation approach:

1. Perform fresh preflight and record exact main/open-PR/task state.
2. Create the task, branch and draft PR before broad edits.
3. Decide and document the minimal `foundation` category/layout amendment if required.
4. Define the smallest public API and tests first.
5. Implement with the standard library and workspace lints.
6. Update architecture policy fixtures for the new category/forbidden upward edge.
7. Run focused checks after coherent edits and exact-head Windows/supply-chain/required CI at the end.
8. Inspect the complete diff, comments and review threads.
9. Merge only when every gate passes, archive the task separately and leave one concrete next package recommendation without implementing it.

Stop and record a blocker rather than guessing when:

- live work already owns the foundation crate/category/shared workspace paths;
- the proposed primitive would encode unresolved Platform/Canary identifiers;
- an external dependency is required but license/security/unsafe evidence is incomplete;
- the design needs a global runtime, executor or broad event bus;
- satisfying the task would require weakening workspace or repository checks;
- architecture documents contradict the proposed public dependency direction.
```
