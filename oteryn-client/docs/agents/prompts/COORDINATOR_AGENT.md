# Parallel Wave Coordinator Agent Prompt

W3 is the current accepted wave. Copy the block below only into a fresh coordinator session. W1 and W2 are historical and must not be relaunched.

```text
Work autonomously in repository:

blakinio/otclient

Role: coordinate `OTERYN-W3-TEST-SUPPORT`. Do not implement the worker package while coordinating.

Current Git/main, root and nested AGENTS.md, live open PRs, active task records, accepted architecture, exact CI and reviewed source/contracts are authoritative. Do not rely on chat history.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate Canary, Oteryn Platform, upstream or another repository;
- never push directly to main;
- one branch/worktree per task;
- no branch-protection, review or CI bypass;
- no success claim without exact evidence.

Mandatory reads:

1. AGENTS.md
2. docs/agents/README.md
3. oteryn-client/AGENTS.md
4. oteryn-client/docs/architecture/ARCHITECTURE.md
5. oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
6. oteryn-client/docs/agents/PROGRAM.md
7. oteryn-client/docs/agents/WORKSTREAMS.md
8. oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md
9. oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
10. oteryn-client/docs/operations/RUST_WORKSPACE.md
11. every active Rust-client task, open PR, review thread and required check
12. merged foundation/diagnostics source and archived W2 records

Revalidate before launch:

- W1 and W2 are completed/archived and not launchable;
- the W3 plan lifecycle is merged;
- no active task or PR owns `crates/test-support`, Cargo/lockfile or the same public surface;
- merged producer APIs remain `oteryn_foundation::ManualClock` and `oteryn-diagnostics` contracts;
- open legacy/operational PRs do not overlap W3 paths.

Current wave:

- one coordinator;
- one implementation lane `W3-TEST` using `NEXT_TEST_SUPPORT_AGENT.md`;
- no secondary implementation or research lane.

W3-TEST boundaries:

- exactly one `oteryn-test-support` library crate under `oteryn-client/crates/test-support/`;
- architecture category `tool`;
- only workspace-local `oteryn-foundation` and `oteryn-diagnostics` dependencies;
- use `ManualClock` directly; no second clock trait/implementation;
- deterministic test-owned timeline/context and diagnostic-event fixture builders;
- no async runtime, executor, scheduler, sleep, hidden thread, global registry or product integration;
- no logger/sink/upload/replay implementation;
- no protocol/auth/user/private/proprietary fixture data;
- architecture checker/fixtures, Rust CI/toolchain and deny policy stay read-only.

Unique shared-path lease for W3-TEST:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
- oteryn-client/docs/operations/RUST_WORKSPACE.md
- docs/agents/MODULE_CATALOG.md
- docs/agents/BUILD_TEST_MATRIX.md
- docs/agents/CHANGELOG.md

For the worker verify:

- unique task, branch/worktree and early draft PR;
- exact owned paths and unique lease in task front matter;
- producer/consumer commits recorded;
- package is small, standard-library-first and independently mergeable;
- task/PR remain current after failures, fixes and validation.

Merge readiness:

- full changed-file list and diff reviewed;
- acceptance criteria and focused tests satisfied;
- exact-head locked metadata, fmt, Clippy, all-target tests, architecture check, cargo-deny and repository CI pass;
- no unresolved comments/reviews/threads, overlap or migration/cross-repository blocker;
- base is current main and PR is mergeable;
- squash merge followed by a separate lifecycle archive PR.

After the worker archive merges, close W3 durably, release every lease and recommend exactly one next bounded package from live evidence. Do not implement that next package in the closure task.
```
