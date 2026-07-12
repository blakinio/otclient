# Agent Coordination Documentation

Persistent operating memory for autonomous agents.

## Read order

1. `../../AGENTS.md`
2. `ACTIVE_WORK.md`
3. `MODULE_CATALOG.md`
4. `REPOSITORY_MAP.md`
5. `KNOWN_RISKS.md`
6. `BUILD_TEST_MATRIX.md`
7. `CROSS_REPO_CONTRACTS.md` when Canary may be affected
8. relevant tasks and ADRs

## Sources of truth

- Git/open PRs are authoritative for branches, commits, checks, merge state.
- Active tasks are authoritative for progress, ownership, failures, decisions, handoff.
- `ACTIVE_WORK.md` is a convenience index and can become stale.
- `MODULE_CATALOG.md` is a reusable-system discovery index, not a substitute for source/tests.
- `CHANGELOG.md` records completed behavior/architecture changes.
- ADRs preserve durable decisions.

## Lifecycle

### Start

- inspect open PRs/tasks;
- search catalogue/repository for reusable work;
- create task from `templates/TASK.md`;
- claim paths/modules;
- publish branch and draft PR early.

### During

- update task after discoveries, failures, decisions, tests, review feedback;
- keep PR body current;
- update catalogue with new/changed reusable interfaces;
- link dependencies/cross-repo tasks.

### Finish

- satisfy autonomous merge gate;
- update changelog/catalogue;
- archive task when final state is known;
- merge through PR, never push to `main`.

## Avoiding duplicate work

Search by responsibility, paths, symbols, protocol fields, configuration keys, tests, and recent PRs. Reuse similar work or record why it cannot be reused.
