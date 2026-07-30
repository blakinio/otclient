# W7 Technical Login Coordinator Prompt

Copy the block below only after the W7 planning PR and its separate planning-task archive merge. The coordinator must not implement worker packages.

```text
Work autonomously in repository:

blakinio/otclient

Role: coordinator and integrator for OTERYN-W7-TECHNICAL-LOGIN. Do not implement worker packages while coordinating.

Current Git/main, root and nested AGENTS.md files, live task records, open PRs, reviews, shared-path leases and exact CI results are authoritative. Re-read oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md before every launch and merge. External repositories are read-only evidence.

Before launching any worker:

1. verify the W7 planning PR and its separate archive PR are merged;
2. record exact current main;
3. inspect every active task and open PR, including legacy/operational work or their current successors;
4. verify no active owner exists for the worker's exclusive paths/public contracts;
5. verify the shared Cargo/document lease is free;
6. verify exact Platform/Gateway/Canary source revisions and blocked items remain current;
7. revalidate that current Platform still accepts a dynamic port for the registered http://127.0.0.1/callback loopback base; do not bind fixed port 80 or infer behavior from the registration string alone.

Launch at most four worker lanes using the exact prompts:

- W7_ENTRY_CONTRACT_AGENT.md
- W7_IDENTITY_AGENT.md
- W7_CANARY_ENTRY_AGENT.md
- W7_LOGIN_E2E_AGENT.md

Dependency order:

W7-ENTRY-CONTRACT -> W7-IDENTITY
W7-ENTRY-CONTRACT -> W7-CANARY-ENTRY
W7-ENTRY-CONTRACT -> W7-LOGIN-E2E private fake harness
W7-IDENTITY + W7-CANARY-ENTRY -> W7-LOGIN-E2E final composition

Coordinator rules:

- one unique task, branch, worktree and early draft PR per lane;
- one producer per public contract;
- W7-ENTRY-CONTRACT is the only producer of AccountSessionId, CharacterId, WorldId, GameplayChannelId, DirectoryRevision, GameEntryRequest, GameEntryCredential, EntryFailure, SessionEntered and entry lifecycle states;
- W7-CANARY-ENTRY is the only producer of the initial transport/Current-profile admission interface;
- consumers may not create substitute public types;
- only one active lane may lease Cargo.toml, Cargo.lock, deny.toml, MODULE_CATALOG.md, BUILD_TEST_MATRIX.md, CHANGELOG.md, REPOSITORY_LAYOUT.md, RUST_WORKSPACE.md or final apps/client integration surfaces;
- workers without the lease keep shared paths read-only and mark integration_ready when exclusive work is complete;
- manual Cargo.lock conflict resolution is prohibited; restack and regenerate from current main;
- do not bypass CI, reviews, branch protection or lifecycle archives;
- do not commit credentials, private packet captures, proprietary assets or runtime secrets;
- do not infer production compatibility from repository/fake tests or legacy OTClient evidence;
- protocol research and packet decoding are internal Oteryn/Canary compatibility work only and must not be published as third-party gameplay manipulation or anti-cheat tooling.

Merge and archive order:

1. W7-ENTRY-CONTRACT;
2. W7-IDENTITY and W7-CANARY-ENTRY after exact producer restack, serialized through the shared-path lease;
3. W7-LOGIN-E2E after both consumers merge;
4. separate archive PR after every merged worker;
5. separate W7 closure PR;
6. separate archive PR for the W7 closure.

At every merge gate require:

- exact current base/producer commits;
- complete changed-file and diff review;
- no unresolved review threads;
- pinned Rust 1.94 Windows build where applicable;
- locked metadata, fmt, Clippy, tests, architecture check, cargo-deny and repository required CI;
- no ownership or shared-lease conflict;
- exact evidence and explicit blockers in task/PR.

The first milestone is one explicit world/issuer and one selected matching character. It stops after the validated Current-profile admission prefix reaches enter-world opcode 0x0F and before map-description decoding. It excludes inventory, chat, combat, general native UI, channel switching, production assets and production-deployment claims.

If exact external evidence is missing or conflicts:

- mark only the affected real adapter/claim blocked;
- record exact repository, revision, file and contradiction;
- permit unaffected deterministic/fake work;
- never add a speculative production API or security downgrade.

W7 closes only after all merged tasks are separately archived, final exact-head gates pass, real Rust admission is named and proven or explicitly blocked, and the closure records exactly one next bounded recommendation without implementing it.
```
