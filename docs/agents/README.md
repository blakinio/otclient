# Agent Coordination Documentation

Persistent operating memory for autonomous agents.

## Read order

1. `../../AGENTS.md`
2. `OTERYN_CLIENT_ARCHITECTURE.md` through `../architecture/OTERYN_CLIENT_ARCHITECTURE.md`
3. `OTERYN_WORKSTREAM_MAP.md`
4. `ACTIVE_WORK.md` as a coordination snapshot only
5. all records under `tasks/active/`
6. all live open pull requests and their checks/review threads
7. `MODULE_CATALOG.md`
8. `REPOSITORY_MAP.md`
9. `KNOWN_RISKS.md`
10. `BUILD_TEST_MATRIX.md`
11. `CROSS_REPO_CONTRACTS.md` when Canary, Oteryn Platform, protocol, identifiers, payloads, login or assets may be affected
12. relevant tasks, ADRs, capability audits and source/tests

A completely new agent should start from the copy-ready prompt in `prompts/OTCLIENT_NEW_AGENT_PROMPT.md`, but must still perform the full live preflight above.

## Core documents

| Document | Purpose |
|---|---|
| `../architecture/OTERYN_CLIENT_ARCHITECTURE.md` | Stable target architecture, trust boundaries, dependency direction and definition of done. |
| `OTERYN_WORKSTREAM_MAP.md` | Repository structure, workstream routing, path ownership, package sizing and acceptance gates. |
| `prompts/OTCLIENT_NEW_AGENT_PROMPT.md` | Standalone startup prompt for a fresh autonomous agent. |
| `MODULE_CATALOG.md` | Existing reusable modules, services and test infrastructure. |
| `REPOSITORY_MAP.md` | Fast path-to-responsibility navigation. |
| `KNOWN_RISKS.md` | Cross-cutting failure modes and safety risks. |
| `BUILD_TEST_MATRIX.md` | Current platform and validation policy. |
| `CROSS_REPO_CONTRACTS.md` | Durable Canary ↔ OTClient and Oteryn integration contracts. |

## Sources of truth

- Git, current `main`, open PRs and checks are authoritative for branches, commits, merge state and live changes.
- Active task files are authoritative for progress, ownership, failures, decisions and handoff.
- `ACTIVE_WORK.md` is a convenience index and can become stale.
- The architecture defines stable boundaries; it does not prove that a planned module is already implemented.
- The workstream map routes changes; source and manifests confirm the actual owner.
- `MODULE_CATALOG.md` is a reusable-system discovery index, not a substitute for source/tests.
- Capability audits describe current gaps and evidence levels; revalidate volatile issue/PR status.
- `CHANGELOG.md` records completed behavior/architecture changes.
- ADRs preserve durable decisions.

## Lifecycle

### Start

- inspect current `main`, open PRs, review threads and active tasks;
- read the architecture and route the task through the workstream map;
- search catalogue/repository for reusable work;
- create a task from `templates/TASK.md`;
- claim narrow paths/modules and declare overlaps/dependencies;
- publish a branch and draft PR early.

### During

- update the task after discoveries, failures, decisions, tests and review feedback;
- keep the PR body current;
- update the catalogue with new/changed reusable interfaces;
- link dependencies and cross-repository tasks;
- preserve Windows-only validation and Oteryn security boundaries unless a separate authorized architecture decision changes them.

### Finish

- review the full diff and changed-file list;
- satisfy the autonomous merge gate;
- update changelog/catalogue/contracts when applicable;
- archive the task when final state is known;
- merge through PR, never push to `main`.

## Avoiding duplicate work

Search by responsibility, paths, symbols, protocol fields, option keys, configuration, widgets, tests, active task ownership and recent PRs. Reuse similar work or record why it cannot be reused.

Do not create a second architecture, repository map, test harness, authentication flow, protocol model or feature controller when an existing owner can be safely extended.
