# Agent Coordination Documentation

Persistent operating memory for autonomous agents across the legacy client and the greenfield Rust client.

## Read order

1. `../../AGENTS.md`.
2. Determine the track from the changed paths.
3. For new Rust-client work, read `../../oteryn-client/AGENTS.md`, its architecture and agent program.
4. For legacy C++/Lua client work, read the legacy architecture/workstream owner and inspect source/module/test conventions.
5. Read `ACTIVE_WORK.md` only as a coordination snapshot.
6. Inspect all records under `tasks/active/` and all live open PRs/checks/review threads.
7. Read `MODULE_CATALOG.md`, `REPOSITORY_MAP.md`, `KNOWN_RISKS.md` and `BUILD_TEST_MATRIX.md`.
8. Read `CROSS_REPO_CONTRACTS.md` for protocol, identifiers, login, routing, gameplay channels or assets.
9. Read relevant tasks, ADRs, audits, source and tests.

## Product tracks

### Greenfield Oteryn Rust client

Normative entry point: `../../oteryn-client/README.md`.

| Document | Purpose |
|---|---|
| `../../oteryn-client/docs/architecture/ARCHITECTURE.md` | Stable target architecture and runtime boundaries. |
| `../../oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md` | Planned workspace, crates and dependency direction. |
| `../../oteryn-client/docs/architecture/CLIENT_LIFECYCLE.md` | Account/game sessions, gameplay-channel login and relog. |
| `../../oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md` | Canary/Oteryn adapter isolation. |
| `../../oteryn-client/docs/architecture/SECURITY_MODEL.md` | Trust boundaries and invariants. |
| `../../oteryn-client/docs/agents/PROGRAM.md` | Ordered audit-first implementation gates. |
| `../../oteryn-client/docs/agents/WORKSTREAMS.md` | Agent ownership and package routing. |
| `../../oteryn-client/docs/agents/AUDIT_PLAN.md` | Mandatory foundation audit. |
| `../../oteryn-client/docs/agents/prompts/FIRST_AUDIT_AGENT.md` | Standalone prompt for the first audit agent. |

The current C++/Lua/OTUI code is evidence only for this track and must not become a Rust runtime dependency.

### Legacy OTClient

The existing roots `src/`, `modules/`, `mods/`, `data/`, CMake and legacy tests remain operational during migration.

| Document | Purpose |
|---|---|
| `../architecture/LEGACY_OTCLIENT_ARCHITECTURE.md` | Maintained architecture needed for legacy work. |
| `LEGACY_OTCLIENT_WORKSTREAMS.md` | Detailed legacy ownership and acceptance routing. |
| `programs/OTCLIENT_UPSTREAM_INTELLIGENCE.md` | Durable read-only upstream/fork audit program. |
| `prompts/OTCLIENT_NEW_AGENT_PROMPT.md` | Standalone startup prompt for a fresh legacy-client agent. |

Legacy work follows exact path owners, existing lifecycle/protocol/security rules and live PR/task state. It must not create a second target architecture or claim to be the greenfield Rust implementation.

## Shared documents

| Document | Purpose |
|---|---|
| `OTERYN_WORKSTREAM_MAP.md` | Top-level track router. |
| `MODULE_CATALOG.md` | Existing/planned reusable systems and interfaces. |
| `REPOSITORY_MAP.md` | Fast path-to-responsibility navigation. |
| `KNOWN_RISKS.md` | Cross-cutting and track-specific risks. |
| `BUILD_TEST_MATRIX.md` | Current validation policy for both tracks. |
| `CROSS_REPO_CONTRACTS.md` | Canary/Oteryn integration contract registry. |
| `CHANGELOG.md` | Curated completed behavior/architecture changes. |

## Sources of truth

- Git, current `main`, open PRs and checks are authoritative for branch/merge/live state.
- Active task files are authoritative for ownership, progress, failures and handoff.
- `ACTIVE_WORK.md` can be stale.
- `oteryn-client/docs/architecture/**` is authoritative for the new client.
- The legacy source, exact tests and `LEGACY_OTCLIENT_*` documents govern only existing-client maintenance and audit evidence.
- Upstream intelligence records are durable memory but volatile issue/PR/source status must be revalidated.
- Cross-repository facts require current producer/consumer evidence.
- ADRs preserve durable decisions.

## Lifecycle

### Start

- inspect current `main`, open PRs, review threads and active tasks;
- route the task to greenfield or legacy paths;
- read the nearest nested `AGENTS.md`;
- search for existing owners and reusable work;
- create a bounded task, branch and draft PR;
- declare ownership, dependencies and cross-repository tasks.

### During

- update the task after discoveries, failures, decisions, tests and reviews;
- keep the PR body current;
- update catalogues/contracts/ADRs when public boundaries change;
- do not cross from legacy to Rust paths opportunistically;
- preserve security, licensing and exact-version gates.

### Finish

- inspect the full changed-file list and diff;
- run proportional focused checks and exact-head required CI;
- update task/docs/contracts/catalogue as applicable;
- merge only through the root autonomous merge gate;
- leave one concrete next action.

## Avoiding duplicate work

Search by responsibility, path, crate/module, protocol field, identifier, feature capability, asset schema, test fixture, task ownership and open PR. Extend the owning architecture or interface rather than creating a parallel framework.
