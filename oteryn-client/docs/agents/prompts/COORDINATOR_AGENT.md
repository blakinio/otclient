# Parallel Wave Coordinator Agent Prompt

W1-W6 are completed and closed. No implementation wave is currently accepted. Copy the block below only to prepare the next planning package; do not create or implement worker packages from this closed-wave prompt.

```text
Work autonomously in repository:

blakinio/otclient

Role: coordinator preparing one bounded future Rust-client wave plan. Do not implement worker packages and do not launch workers before the planning PR and its separate archive merge.

Current Git/main, root and nested AGENTS.md files, live task records, open PRs, reviews and exact CI results are authoritative. Do not rely on chat history or copied hashes.

Repository safety:

- routine writes only to blakinio/otclient;
- external repositories are read-only evidence;
- never push directly to main;
- one task, branch and worktree per change;
- create an early draft PR;
- never bypass CI, review, branch protection or lifecycle rules;
- never commit credentials, private captures, tokens or proprietary assets;
- do not claim production compatibility from repository tests.

Mandatory reads:

1. AGENTS.md
2. docs/agents/README.md
3. docs/agents/CONTEXT_HANDOFF.md
4. oteryn-client/AGENTS.md
5. oteryn-client/docs/agents/PROGRAM.md
6. oteryn-client/docs/agents/WORKSTREAMS.md
7. oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md
8. oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
9. relevant architecture, lifecycle, audit, research and operations documents
10. every active Rust task and open PR
11. exact current external producer contracts needed by the proposed wave

Preflight:

- verify W1-W6 are merged, archived and not launchable;
- verify PR #93 merged and its task archive merged through PR #95;
- verify PR #23 remains legacy UI-only, PR #48 remains isolated operational non-merge work and PR #97 remains legacy asset rehearsal only;
- verify no active task or open PR owns the proposed paths or public contracts;
- verify every prior Cargo, lockfile, dependency-policy and shared-document lease is released;
- record exact current main in the planning task;
- stop or split the plan wherever an exact external contract is missing.

The next bounded recommendation is to plan OTERYN-W7-TECHNICAL-LOGIN with at most one coordinator and four workers:

- W7-ENTRY-CONTRACT: sole producer of typed account/session/directory/game-entry lifecycle contracts;
- W7-IDENTITY: consumer for Authorization Code + PKCE, callback validation, account session and one fresh game-entry request;
- W7-CANARY-ENTRY: consumer and sole producer of the initial transport/Current-profile admission interface;
- W7-LOGIN-E2E: final consumer/composition owner for the existing Rust window, fake-service E2E and executable integration.

Planning requirements:

- exact dependency graph and merge order;
- exact owned paths;
- exact producer/consumer declarations;
- one active shared-path lease at a time;
- no manual Cargo.lock conflict resolution;
- automated versus interactive evidence matrix;
- explicit blocked items and exact missing-contract evidence;
- exact first-milestone acceptance criteria;
- exact coordinator prompt and one exact prompt per worker;
- no worker task, branch, PR or lease before the plan and separate plan archive merge.

The first milestone may target only one explicitly configured world/issuer and one selected character. It excludes map rendering, broad world decoding, inventory, chat, combat, general native UI, channel switching, production assets and production deployment claims.

Do not infer general multi-world/channel routing from the current one-exact-issuer Gateway v1 path. Do not define speculative production APIs. An affected lane remains blocked while unaffected planning can continue.

Merge the planning package only after complete changed-file review, exact-head required checks, no unresolved threads, current main reconciliation and the root autonomous merge gate. Archive the planning task separately before any worker launch.
```
