# First Oteryn Rust Client Audit Agent Prompt

Copy the block below into a fresh agent session.

```text
Work autonomously in repository:

blakinio/otclient

Task: perform the mandatory foundation audit for the greenfield Rust Oteryn client.

Do not rely on previous chat history. Current Git, main, root/nested AGENTS.md, live open PRs, active task records, architecture documents and verified contracts are source of truth.

Repository safety:

- routine writes only to blakinio/otclient;
- do not mutate upstream or external repositories;
- never push directly to main;
- create one dedicated branch/worktree, task record and draft PR;
- do not edit paths owned by another active task;
- do not commit secrets, credentials, private logs, proprietary game assets or unlicensed captures.

Mandatory reads:

1. AGENTS.md
2. oteryn-client/AGENTS.md
3. oteryn-client/README.md
4. oteryn-client/docs/architecture/ARCHITECTURE.md
5. oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md
6. oteryn-client/docs/architecture/CLIENT_LIFECYCLE.md
7. oteryn-client/docs/architecture/MODULE_MODEL.md
8. oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md
9. oteryn-client/docs/architecture/SECURITY_MODEL.md
10. oteryn-client/docs/architecture/PERFORMANCE_AND_TESTING.md
11. oteryn-client/docs/architecture/ASSET_PIPELINE.md
12. oteryn-client/docs/agents/PROGRAM.md
13. oteryn-client/docs/agents/WORKSTREAMS.md
14. oteryn-client/docs/agents/AUDIT_PLAN.md
15. docs/agents/CROSS_REPO_CONTRACTS.md
16. all active tasks and live open PRs

Product constraints:

- this is a new Rust client, not a line-by-line OTClient port;
- current C++/Lua/OTUI code is legacy/reference evidence only;
- the Rust client must not link legacy code, execute legacy Lua/OTUI or inherit legacy globals;
- Canary is the first compatibility adapter;
- Oteryn is the long-term target ecosystem;
- protocol adapters translate to stable GameEvent/GameCommand domain contracts;
- a gameplay world channel is a parallel world instance selected at login or relog;
- changing Channel 1 to Channel 2 happens through relog, not seamless in-game transfer;
- Oteryn login uses system-browser Authorization Code + PKCE and one-shot game-session handoff;
- the main Oteryn password is never sent to Canary/game nodes;
- server implementation design is out of scope except for exact client-facing contracts;
- Windows is the first required platform;
- no production Rust workspace/bootstrap code may be added by this audit task.

Audit goal:

Create verified inputs for implementation. Do not let legacy structure dictate the architecture. Label every conclusion PROVEN, SUPPORTED, INFERRED, UNKNOWN, BLOCKED or REJECTED.

Required outputs under:

oteryn-client/docs/audits/foundation/

- README.md
- 01-product-and-feature-inventory.md
- 02-canary-compatibility.md
- 03-oteryn-identity-and-session.md
- 04-assets-and-licensing.md
- 05-performance-baseline.md
- 06-platform-and-hardware.md
- 07-test-and-fixture-inventory.md
- 08-risk-register.md
- 09-gap-and-decision-log.md
- 10-bootstrap-recommendation.md

Follow oteryn-client/docs/agents/AUDIT_PLAN.md exactly.

Search-first requirements:

- current main and all live open PRs/tasks;
- existing protocol/version/feature definitions and tests;
- login, character list, world routing and session lifecycle;
- asset formats, loaders, manifests, licenses and distribution rules;
- renderer/world/UI architecture and available performance diagnostics;
- current Oteryn Identity/game-session contracts;
- exact Canary producer evidence for any protocol fact;
- current primary documentation for candidate Rust dependencies when recommending them.

Audit rules:

- verify facts from exact source/contract/test/runtime evidence;
- distinguish current behavior from desired future behavior;
- do not copy protocol assumptions from third-party forks;
- do not import proprietary assets or raw private captures;
- do not invent target hardware, benchmarks or performance results;
- when runtime access is unavailable, document an executable measurement procedure and mark the evidence BLOCKED;
- record failed searches and rejected hypotheses;
- use tables/machine-readable artifacts where they improve agent continuation;
- propose an ADR amendment rather than silently changing a stable architecture boundary.

The final bootstrap recommendation must select one narrow first implementation package with:

- workstream;
- owned paths;
- exact artifacts;
- acceptance tests;
- prerequisites;
- non-goals;
- blockers and rollback.

Do not bootstrap Cargo crates, choose speculative protocol constants or implement product behavior.

Validation:

- complete changed-file and full-diff review;
- Markdown/link/path consistency;
- repository documentation/fast checks on exact head;
- no build claim unless a build was actually run;
- no server/runtime compatibility claim without exact evidence.

Finish end-to-end: update the task and PR, inspect CI, fix documentation issues, and merge only if the root autonomous merge gate is satisfied. Leave one concrete next action for the bootstrap agent.
```
