# Parallel Wave Coordinator Agent Prompt

W4 is the current accepted wave. Copy the block below only into a fresh coordinator session after the W4 planning lifecycle merges. W1, W2 and W3 are historical and must not be relaunched.

```text
Work autonomously in repository:

blakinio/otclient

Role: coordinate `OTERYN-W4-WINDOWS-SHELL`. Do not implement the worker package while coordinating.

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
11. every active Rust task, open PR, review thread and required check
12. merged foundation/diagnostics/test-support source and Windows platform evidence

Revalidate before launch:

- W1, W2 and W3 are completed/archived and not launchable;
- the W4 plan lifecycle is merged;
- no active task or PR owns `apps/client`, Cargo/lockfile or the same public surface;
- primary evidence still supports exact `winit 0.30.13`, Apache-2.0 and MSRV 1.70, or the plan is amended before launch;
- open legacy/operational PRs do not overlap W4 paths.

Current wave:

- one coordinator;
- one implementation lane `W4-SHELL` using `NEXT_WINDOWS_SHELL_AGENT.md`;
- no secondary implementation or research lane.

W4-SHELL boundaries:

- exactly one package under `oteryn-client/apps/client/`, package name `oteryn-client`, category `app`;
- exact direct dependency `winit = "=0.30.13"` unless fresh primary evidence changes;
- reuse workspace-local foundation, diagnostics and test-support contracts;
- one resizable blank Windows window, main-thread event-loop ownership and deterministic shutdown;
- deterministic unit-testable shell state machine and bounded structured lifecycle diagnostics;
- no renderer/GPU, direct raw-window-handle, direct Win32/windows-sys, unsafe, protocol, identity, networking, assets, audio, feature UI, persistence or async runtime;
- architecture checker/rules/fixtures, Rust CI/toolchain remain read-only unless a separate blocker is recorded.

Unique shared-path lease for W4-SHELL:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/deny.toml
- oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
- oteryn-client/docs/operations/RUST_WORKSPACE.md
- docs/agents/MODULE_CATALOG.md
- docs/agents/BUILD_TEST_MATRIX.md
- docs/agents/CHANGELOG.md

For the worker verify:

- unique task, branch/worktree and early draft PR;
- exact owned paths and unique lease in task front matter;
- exact dependency source/version/license/MSRV/advisory evidence;
- one package only and independently mergeable scope;
- task/PR remain current after failures, fixes and validation;
- interactive Windows evidence is never inferred from compilation.

Merge readiness:

- full changed-file list and diff reviewed;
- automated acceptance and explicit runtime evidence blockers are documented;
- exact-head locked metadata, fmt, Clippy, all-target tests, architecture check, cargo-deny and repository CI pass;
- no unresolved comments/reviews/threads, overlap or migration/cross-repository blocker;
- base is current main and PR is mergeable;
- squash merge followed by a separate lifecycle archive PR.

After the worker archive merges, close W4 durably, release every lease and recommend exactly one next bounded package from live evidence. Do not implement that next package in the closure task.
```
