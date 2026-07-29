# Next Deterministic Test Support Agent Prompt

Copy the block below into one fresh worker session only after the W3 plan and its lifecycle archive have merged.

```text
Work autonomously in repository:

blakinio/otclient

Task: implement lane `W3-TEST` from `OTERYN-W3-TEST-SUPPORT` as one small deterministic Rust test-support package.

Do not rely on chat history. Current Git/main, root and nested AGENTS.md, live open PRs, active tasks, accepted architecture, merged foundation/diagnostics source and exact CI are authoritative.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate upstream, Canary, Oteryn Platform or another repository;
- never push directly to main;
- create one task, one branch/worktree and an early draft PR;
- stop for unresolved ownership overlap, secrets/proprietary data, required external writes or a stable-boundary conflict needing an ADR.

Fresh preflight:

1. Read AGENTS.md, docs/agents/README.md and oteryn-client/AGENTS.md.
2. Read ARCHITECTURE.md, REPOSITORY_LAYOUT.md, PROGRAM.md, WORKSTREAMS.md, MULTI_AGENT_EXECUTION.md, CURRENT_PARALLEL_WAVE.md and RUST_WORKSPACE.md.
3. Inspect all active Rust tasks, open PRs, review threads and current main.
4. Read `crates/foundation` clock/generation APIs and the complete `crates/diagnostics` public contract/tests.
5. Confirm no owner holds `crates/test-support`, Cargo/lockfile or W3 shared docs.
6. Record exact producer/base commits in the task.

Required package:

- add exactly one library crate at `oteryn-client/crates/test-support/`;
- package name `oteryn-test-support`;
- category `tool`;
- dependencies only on workspace-local `oteryn-foundation` and `oteryn-diagnostics`;
- no external dependency.

Required public behavior:

- deterministic test-owned timeline/context orchestration that owns or clones the existing `ManualClock` and exposes it directly;
- technical-context construction from the timeline's current `Moment` and explicit process/session/task/correlation values;
- a deterministic diagnostic-event fixture builder accepting only reviewed static message/key text and already-classified `DiagnosticValue` values;
- insertion-order preservation and propagation of diagnostics field bounds/duplicate-key failures;
- closed, secret-free errors only where composition needs one;
- APIs usable without window, filesystem, network, wall-clock time, background work or application startup.

Hard boundaries:

- do not define another clock trait/type implementing `MonotonicClock`;
- do not add sleep, polling, timer wheel, async runtime, executor, scheduler or hidden thread;
- do not add global mutable fixture registries, environment mutation or singletons;
- do not install logging/tracing subscribers or sinks;
- do not add telemetry, crash-report, support-bundle, recorder or replay-runner behavior;
- do not add protocol packets/constants, authentication data, endpoints, private paths, user data or proprietary assets;
- do not integrate the crate into product/runtime services;
- do not edit architecture checker/fixtures, Rust CI/toolchain or deny policy unless live evidence proves a separate blocker; record that blocker rather than broadening scope.

Owned path:

- `oteryn-client/crates/test-support/**`
- the worker task record

Unique shared lease:

- `oteryn-client/Cargo.toml`
- `oteryn-client/Cargo.lock`
- `oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md`
- `oteryn-client/docs/operations/RUST_WORKSPACE.md`
- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `docs/agents/CHANGELOG.md`

Required tests:

- deterministic start/advance/current moment;
- shared clock observation across clones and threads without sleeps;
- backwards and overflow failures are propagated without partial mutation;
- context uses exact current time and explicit typed generations/correlation;
- event builder preserves field insertion order;
- duplicate keys and maximum field bound remain enforced;
- sensitive synthetic runtime text is redacted and absent from Display/Debug;
- arbitrary owned/runtime strings cannot become safe message/key/value through implicit conversion (compile-fail doctest or equivalent);
- no test contains a real credential, endpoint, personal path or proprietary byte.

Validation from `oteryn-client/` on the exact final head:

- `cargo metadata --locked --format-version 1`
- `cargo fmt --all --check`
- `cargo clippy --workspace --all-targets --locked -- -D warnings`
- `cargo test --workspace --all-targets --locked`
- `cargo run --locked -p oteryn-architecture-check -- workspace .`
- `cargo deny check`
- required GitHub Rust Client Windows/Supply Chain and repository `CI / Required`

Before merge:

- review the complete changed-file list and full diff;
- update task, module catalogue, build/test matrix, changelog, repository layout and workspace operations;
- keep the PR body current with exact validation SHA and no runtime compatibility claim;
- verify comments/reviews/threads and unchanged current base;
- mark ready, pass any ready-for-review exact-head run and squash-merge with expected head SHA;
- archive the task in a separate lifecycle PR and release the lease.
```
