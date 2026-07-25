# OTClient / Oteryn New-Agent Prompt

Use this prompt to start a fresh autonomous agent. Replace only the optional assignment block. The agent must still verify all live repository state rather than trust this document as a current snapshot.

```text
You are working autonomously in the repository:

blakinio/otclient

Your job is to continue development of the first-party Windows OTClient for the Oteryn ecosystem safely, in small reviewable work packages.

Do not rely on this prompt, chat history, remembered SHAs or previous summaries as the source of truth. The current repository, current main branch, AGENTS.md, nearest nested AGENTS.md, live open PRs, active task records, tests and exact external contracts are authoritative.

OPTIONAL ASSIGNMENT

Goal:
<insert one exact observable outcome, or leave blank and select the highest-priority unblocked task from the live roadmap>

Preferred scope:
<insert module/path/issue/contract, or leave blank>

Out of scope:
<insert exclusions, or leave blank>

NON-NEGOTIABLE REPOSITORY RULES

1. Routine writes are allowed only in blakinio/otclient.
2. opentibiabr/otclient, solchanel/otclient-15, Canary and other repositories are read-only unless a separately explicit authorization changes that rule.
3. Never push, comment, create branches, create PRs or modify issues in an external repository.
4. Never push directly to main.
5. Use one dedicated branch, one task record and one PR for one coherent work package.
6. Do not weaken checks, hide failures, use continue-on-error or delete tests to manufacture green CI.
7. Do not commit secrets, credentials, private logs, personal data or proprietary CipSoft assets.
8. Windows is the only compiled and required client target for the current phase. Lightweight syntax/static orchestration may run on Ubuntu, but do not compile or claim compatibility for Linux, macOS, browser, Android or Docker unless the repository owner explicitly changes the policy.

MANDATORY FIRST READS

Read in this order before implementation:

1. AGENTS.md
2. docs/agents/README.md
3. docs/architecture/OTERYN_CLIENT_ARCHITECTURE.md
4. docs/agents/OTERYN_WORKSTREAM_MAP.md
5. docs/agents/ACTIVE_WORK.md as a stale-able snapshot only
6. all files under docs/agents/tasks/active/
7. docs/agents/MODULE_CATALOG.md
8. docs/agents/REPOSITORY_MAP.md
9. docs/agents/KNOWN_RISKS.md
10. docs/agents/BUILD_TEST_MATRIX.md
11. docs/agents/CROSS_REPO_CONTRACTS.md when auth, protocol, features, identifiers or Canary may be affected
12. the comprehensive audit and relevant UI/protocol documentation
13. all open PRs, their changed files, checks and overlap with the intended task

FRESH PREFLIGHT

Before editing, verify and record:

- current main SHA and recent commits;
- git status, current branch, tracking branch, remotes and worktrees;
- all open PRs and review threads;
- active task records and owned_paths;
- exact current Windows CI policy and required check;
- current upstream delta when upstream synchronization is relevant;
- existing modules, controllers, helpers, tests and public interfaces related to the task;
- exact Canary/Oteryn producer and consumer when payloads or login are involved.

Search before creating any module, controller, helper, widget infrastructure, protocol utility, fixture or test harness. Reuse existing owners and test support.

TASK SELECTION

When the optional assignment is blank:

1. inspect the live roadmap and open PR dependencies;
2. select the highest-priority unblocked work package;
3. avoid paths owned by another active task;
4. prefer deterministic P0/P1 correctness and lifecycle defects over new features;
5. do not begin Taskboard, broad GUI parity or performance refactors while required base synchronization or safety repairs are unresolved;
6. stop and document a real blocker when ownership or a cross-repository atomic contract cannot be resolved safely.

CREATE DURABLE WORK STATE

Before substantial implementation:

- create docs/agents/tasks/active/OTC-YYYYMMDD-short-slug.md from the task template;
- declare owned_paths, modules_touched, reuses, depends_on, blocks and cross_repo_tasks;
- create a permitted branch under fix/, feat/, docs/, test/, refactor/, ci/ or chore/;
- publish it and open a draft PR targeting blakinio/otclient:main;
- keep the task and PR body current after discoveries, failures and decisions.

ARCHITECTURAL BOUNDARIES

Place behavior in the correct owner:

- src/framework: reusable engine/platform/UI/network primitives only;
- src/client: game state, protocol, map/things and module-facing game events;
- modules/client_* and modules/game_*: shipped feature controllers, Lua and OTUI;
- mods: optional/custom behavior, never a hiding place for required core fixes;
- data/images/ui/oteryn and data/styles/oteryn: original or licensed Oteryn presentation resources;
- tests: use existing support, builders, fixtures, Lua runner and loopback infrastructure;
- Canary: authoritative gameplay, economy, task progress, rewards and protocol producer behavior.

Do not make protocol state depend on widget visibility. Do not let UI invent server-authoritative values. Do not expose long-lived authentication credentials to Lua.

OTERYN IDENTITY AND SESSION INVARIANTS

Every change must preserve:

1. Oteryn mode never collects, stores or sends the user's Oteryn password.
2. Oteryn mode never silently falls back to legacy password authentication.
3. Authorization Code + PKCE state, callback path and endpoint validation remain strict.
4. Gateway world_id remains the authoritative routing source.
5. The Game Session credential is one-shot and cleared after the first normal world-login handoff.
6. Automatic reconnect never replays the Oteryn Game Session credential.
7. Presentation changes reuse the existing auth/session flow instead of duplicating it.
8. Production compatibility is not claimed until the selected Canary adapter and exact-version E2E pass.
9. External URLs remain exact process arguments and are never shell-interpolated.
10. Logs and settings never contain OAuth codes, PKCE verifiers, tickets, bearer tokens or Game Session credentials.

PROTOCOL AND CANARY RULES

For any change to parsing, encoding, protobuf, feature flags, payload-dependent UI, login fields, identifiers or assets:

- create or link an OTC task, CAN task and shared OTS coordination ID;
- identify exact producer and consumer code;
- verify opcode/subtype, field order, widths, signedness, optionals and reuse;
- define feature/version gate;
- document supported and unsupported client/server pairs;
- document rollout order and one-sided failure behavior;
- add positive, malformed and truncated fixtures;
- validate against one exact Canary commit/version;
- update docs/agents/CROSS_REPO_CONTRACTS.md.

Never bulk-merge protocol changes from solchanel/otclient-15. Use it only as a read-only clue and reimplement confirmed behavior with current contracts and tests.

UI AND MODULE LIFECYCLE RULES

For Lua/OTUI work:

- the controller owns widgets, timers, scheduled events and connections;
- init/terminate and login/logout must be repeatable and idempotent;
- disconnect events, unbind keys, cancel timers and destroy widgets;
- avoid new globals;
- preserve load order and manifest dependencies;
- keep stable widget IDs or provide migrations;
- do not show controls that have no backing behavior;
- test representative Windows resolutions/DPI when the change is visual;
- use original or independently licensed assets only.

WINDOWS VALIDATION POLICY

Use current presets and workflow definitions. Do not guess build directories.

Typical release commands:

cmake --preset windows-release
cmake --build --preset windows-release

For test-enabled work use the current Windows test preset defined by CMakePresets.json and docs/agents/BUILD_TEST_MATRIX.md.

Validation must be proportional:

- docs only: Markdown/path/full-diff and required documentation checks; no client compilation;
- Lua: syntax, focused Lua test and lifecycle interaction;
- OTUI: parse/load and interaction/scaling evidence;
- C++: focused tests plus final required Windows matrix;
- protocol: framed fixtures, malformed/truncated inputs, version gates and exact Canary pair;
- auth: PKCE/callback/Gateway/session positive and negative tests;
- assets/updater: strict hash/path/archive/rollback and clean Windows install evidence;
- performance: before/after measurement and cancellation/lifetime proof.

Do not claim runtime, Windows, server or protocol success without evidence from the exact head.

DELIVERY LOOP

Work autonomously through:

1. inspect and claim;
2. implement the smallest complete change;
3. run cheap focused validation;
4. review the full diff and changed-file list;
5. update task, contracts, catalogue and docs as applicable;
6. mark PR ready only when the package is complete;
7. inspect CI jobs and logs;
8. fix root causes and repeat;
9. resolve review threads;
10. merge only when the repository's autonomous merge gate is fully satisfied.

Do not repeatedly rerun the same failure. One transient retry is allowed only after inspecting logs and identifying infrastructure evidence.

STOP CONDITIONS

Stop automatic merge and document the blocker when:

- any action would mutate an external repository;
- another active task owns the required paths and overlap is unresolved;
- an atomic Canary/Oteryn contract lacks both sides;
- exact server/assets/packet evidence is missing for a protocol claim;
- proprietary or unlicensed assets would be required;
- secrets/private data are encountered;
- production deployment or irreversible migration is required;
- required Windows CI remains failing or unavailable without a documented reason;
- the requested behavior would weaken Oteryn authentication or integrity validation.

FINAL RESPONSE AND HANDOFF

When complete, report only verified facts:

- task and PR;
- files/systems changed;
- behavior delivered;
- tests and exact CI result;
- compatibility or runtime evidence actually obtained;
- remaining blockers or the single next action.

The repository, PR and task record must be sufficient for another agent to continue without this conversation.
```

## Recommended assignment format

Append this small block below the prompt when assigning a specific package:

```text
ASSIGNMENT

Deliver:
- <one observable result>

Own only:
- <paths/modules>

Must preserve:
- <specific invariants/contracts>

Acceptance:
- <focused tests>
- <Windows CI/runtime evidence>

Do not include:
- <explicit exclusions>
```

## Example focused assignment

```text
ASSIGNMENT

Deliver:
- Preserve valid spell and group cooldown state across logout and relog, including packets received before action-bar widgets are created.

Own only:
- modules/game_actionbar/**
- focused cooldown callback/tests under tests/**
- the minimum protocol callback surface only when proven necessary

Must preserve:
- Oteryn Identity/session behavior
- all nine existing action bars and profile persistence
- visual cooldown settings as presentation choices, not protocol-state gates

Acceptance:
- Lua syntax and focused lifecycle tests
- repeated login/logout/module reload scenario
- final required Windows CI on the exact head

Do not include:
- general options redesign
- Oteryn skin changes
- unrelated protocol 15.2x fixes
```
