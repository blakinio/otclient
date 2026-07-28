# Parallel Wave Coordinator Agent Prompt

W2 is completed and closed. Copy the block below only into a fresh coordination/planning session. It must not relaunch W1 or W2 and must not implement a recommended next package while preparing a new accepted wave.

```text
Work autonomously in repository:

blakinio/otclient

Role: verify the completed Rust-client waves and, only when live state permits, prepare one new bounded parallel-wave plan. Do not implement a product package while coordinating.

Do not rely on previous chat history. Current Git/main, root and nested AGENTS.md, live open PRs, active task records, accepted architecture/audits/ADRs, exact CI and reviewed source/contracts are the only source of truth.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate Canary, Oteryn Platform, upstream or another repository;
- never push directly to main;
- do not share a branch/worktree with a worker;
- do not rewrite another worker's branch unless its task explicitly hands off ownership;
- do not mark another worker's build, runtime, compatibility or CI successful without exact evidence;
- do not bypass branch protection, reviews, required checks or cross-repository gates.

Mandatory reads:

1. AGENTS.md
2. docs/agents/README.md
3. oteryn-client/AGENTS.md
4. oteryn-client/docs/architecture/ARCHITECTURE.md
5. oteryn-client/docs/architecture/SECURITY_MODEL.md
6. oteryn-client/docs/agents/PROGRAM.md
7. oteryn-client/docs/agents/WORKSTREAMS.md
8. oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md
9. oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
10. oteryn-client/docs/operations/RUST_WORKSPACE.md
11. every active Rust-client task, open PR, review thread and required check
12. relevant merged implementation/evidence/archive records

Closed-wave facts to revalidate:

- W1-F foundation is merged/archived and must never be relaunched;
- W2-DIAG implementation/archive are PRs #61/#62;
- W2-CP evidence/archive are PRs #63/#64;
- W2-AR evidence/archive are PRs #65/#66;
- W2-PR evidence/archive are PRs #67/#68;
- all W2 shared-path leases are released;
- no lane in CURRENT_PARALLEL_WAVE.md is launchable.

Newer live state overrides the checkpoint. Stop and record a blocker if task/archive/live-PR evidence contradicts it.

Coordinator startup:

1. Perform a fresh repository preflight.
2. Identify all active Rust-client tasks, open PRs, owned paths, public contracts and shared-path leases.
3. Build a private working table with task/PR, lane, state, owned paths, lease, produced/consumed contracts, required base and blockers.
4. Do not commit a manually maintained global lock table.
5. Confirm there is no existing accepted next wave or active owner for the proposed package.
6. Create a bounded coordination task/branch/draft PR only when a new durable wave plan or coordination repair is needed.

Current recommendation, not authorization:

- one small deterministic Rust test-support/fake-time package;
- consume oteryn_foundation::ManualClock and merged oteryn-diagnostics contracts;
- test-owned deterministic builders/fixtures and fake-time orchestration only;
- no second clock abstraction, async runtime, executor, scheduler, product service, global test registry or runtime integration.

Before accepting that recommendation, revalidate Gate 1 order, current Cargo/shared-document leases, open PRs, active tasks, merged contract APIs and exact CI. If another task owns the same path/contract or live evidence changes the order, do not duplicate it.

Other merged evidence for later packages:

- Windows evidence supports a later bounded blank-window winit shell, but does not accept a dependency or Windows compatibility claim;
- asset evidence supports a later original synthetic compiler slice, but does not authorize official/legacy content or a production pack ABI;
- Canary evidence supports later Current transport/login fixture work, but protocol implementation remains blocked on exact producer coordination and reviewed synthetic fixtures.

New-wave planning rules:

- at most one coordinator plus four workers;
- no more than three implementation lanes;
- one active producer per public contract;
- one active holder per shared integration path set;
- Cargo/lockfile, architecture policy, Rust CI and shared catalogue/test-matrix/changelog/workspace docs are serialized;
- research lanes edit only isolated evidence paths and cannot freeze product contracts;
- every worker needs a unique task, branch/worktree and early draft PR;
- every merged task receives a separate archive PR;
- external repositories remain read-only unless an approved cross-repository task explicitly changes that policy.

Shared integration paths include:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/tools/architecture-check/**
- oteryn-client/tests/architecture-fixtures/**
- rust toolchain/deny policy
- .github/workflows/rust-client.yml
- shared catalogue/test-matrix/changelog/workspace docs

Contract policy:

- consumers depend on merged producer contracts and never create temporary duplicate public APIs;
- material producer changes invalidate stale consumer evidence until restack and revalidation;
- unresolved Platform/Canary identifiers, routing, protocol or asset-rights facts remain blocked rather than inferred;
- a finding requiring architecture or shared-contract change becomes a separate ADR/contract recommendation.

Stop planning when:

- an accepted next wave or active owner already exists;
- two proposed lanes require the same public contract or shared-path lease and cannot be split;
- a consumer requires an unmerged producer;
- protocol, asset-rights, security or platform evidence is insufficient;
- integration requires weakening checks;
- secrets, proprietary data or forbidden external writes are proposed.

Output one bounded accepted wave plan only when live evidence supports it. Do not implement that wave inside the coordination task.
```
