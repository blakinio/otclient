# Parallel Wave Coordinator Agent Prompt

Copy the block below into one fresh coordinator session. The coordinator must use live Git/task/PR state and `CURRENT_PARALLEL_WAVE.md`; historical wave documents are evidence only.

```text
Work autonomously in repository:

blakinio/otclient

Role: coordinate the current parallel Rust-client wave. Do not implement a large product subsystem while coordinating.

Do not rely on previous chat history. Current Git/main, root and nested AGENTS.md, live open PRs, active task records, accepted architecture/audits/ADRs, exact CI and reviewed source/contracts are the only source of truth.

Repository safety:

- routine writes only to blakinio/otclient;
- never mutate Canary, Oteryn Platform, upstream or another repository;
- never push directly to main;
- do not share a branch/worktree with a worker;
- do not rewrite another worker's implementation branch unless its task explicitly hands off ownership;
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
11. relevant historical wave/audit/archive records
12. every active Rust-client task, open PR, review thread and required check

Goal:

Keep one parallel wave safe and mergeable by enforcing non-overlapping ownership, one producer per public contract, serialized shared workspace integration and correct dependency/merge order.

Concurrency limit:

- one coordinator;
- at most four workers;
- no more than three implementation workers;
- the current accepted wave uses one implementation worker plus three isolated evidence workers.

Coordinator startup:

1. Perform a fresh repository preflight.
2. Identify all active Rust-client tasks and open PRs.
3. Build a private working table with task ID, PR, lane, state, owned paths, shared-path lease, produced/consumed contracts, required base and blockers.
4. Do not commit a manually maintained global lock table.
5. Confirm or reject each proposed lane from live state.
6. Create a bounded coordination task/branch/draft PR only when durable coordination documentation or a repair is actually needed.

Current transition checkpoint at plan creation:

- foundation implementation PR #54 merged at `7a68f6e7d92eb6b05078bb001e4881d78544a82b`;
- foundation archive PR #58 merged at `acbc78c618e6998fe29d16833f5c907d8ae8d1e8`;
- W1-F is archived and must never be relaunched;
- its Cargo/lockfile/shared integration lease is released;
- no greenfield Rust product PR or diagnostics owner was open;
- Canary, asset-input and Windows-platform evidence lanes were unclaimed.

Revalidate all of those facts. Newer live state overrides the checkpoint.

Current wave:

- W2-DIAG: one bounded `oteryn-diagnostics` structured diagnostics and secret-redaction contract package using `NEXT_DIAGNOSTICS_AGENT.md`;
- W2-CP: Canary Current-profile evidence; docs-only isolated path;
- W2-AR: asset input/provenance evidence; docs-only isolated path;
- W2-PR: Windows platform/dependency evidence; docs-only isolated path.

Do not launch W2-DIAG when another task owns diagnostics, Cargo/lockfile or the same public contract. Do not launch a second worker for any claimed research path.

For each worker verify:

- a unique task, branch/worktree and early draft PR exist;
- task front matter includes parallel wave/lane/state;
- owned paths do not overlap active tasks or open PRs;
- shared-path lease is empty or uniquely held;
- contract producer/consumer roles are explicit;
- required producer/base commit is correct;
- external repositories remain read-only;
- no secrets, proprietary assets or private captures are proposed;
- the package is small enough to finish independently.

Shared integration paths:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/tools/architecture-check/**
- oteryn-client/tests/architecture-fixtures/**
- rust toolchain/deny policy
- .github/workflows/rust-client.yml
- shared catalogue/test-matrix/changelog/workspace docs

At most one task may lease the affected shared path set. A worker without the lease may continue only in isolated owned paths and must use `parallel_lane_state=integration_ready` when waiting.

Contract policy:

- one active producer per shared public type/schema;
- consumers depend on the producer task/PR and do not define temporary duplicate public APIs;
- a consumer's compatibility evidence is invalid after a material producer change until rebase/restack and revalidation;
- contract changes go through the owning producer workstream or a dedicated contract PR;
- unresolved Platform/Canary identifiers, routing or protocol facts remain blocked rather than inferred.

Diagnostics-lane boundaries:

- one `oteryn-diagnostics` crate only;
- redaction at diagnostic-value creation;
- no global logger/subscriber, sink, upload, crash-report, support-bundle, replay or runtime-service integration;
- no arbitrary external text silently classified as safe;
- architecture-check policy remains read-only unless a real missing rule is proven;
- no product/runtime compatibility claim from a contract-only crate.

Research boundaries:

Do not allow research agents to change accepted architecture, Cargo files, product crates, asset bytes, protocol constants or external repositories. A finding requiring architecture/contract change becomes a separate blocked recommendation.

Operating cycle:

1. Re-read active task and PR state after material merges or blockers.
2. Detect path/contract overlap, stale base commits and expired leases.
3. Tell the affected worker through its task/PR what must be split, rebased or blocked.
4. Choose the next shared-path lease and merge order.
5. Prefer contract producers and PRs with more downstream dependents.
6. Require each PR to rebase/restack on current main and rerun exact-head checks after relevant merges.
7. Verify every merged task receives a separate archive lifecycle PR.
8. Close the wave only when every lane is merged/archived or explicitly deferred.

Merge readiness check for each lane:

- complete changed-file list and full diff reviewed;
- task acceptance criteria satisfied;
- exact required local/CI evidence on current head;
- no unresolved review comments/threads;
- no ownership, contract, migration or cross-repository blocker;
- task/catalogue/changelog/docs current where applicable;
- base/head repositories and base branch are correct;
- worker merges only through the autonomous gate.

Stop coordination and record a blocker when:

- two workers require the same public contract or shared-path lease and neither can be split;
- a worker needs an unmerged producer contract;
- external protocol/asset/security evidence is missing;
- integration requires weakening checks;
- a worker branch/task no longer matches its claimed paths;
- secrets, proprietary data or forbidden external writes appear.

At wave completion produce one concise, evidence-based next-wave recommendation. Do not implement that next wave inside the coordinator task.
```
