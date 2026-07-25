---
task_id: OTC-20260725-windows-only
coordination_id: ""
status: implementation
agent: "GPT-5.6 Thinking"
branch: ci/OTC-20260725-windows-only
base_branch: main
created: 2026-07-25T11:00:00+02:00
updated: 2026-07-25T11:00:00+02:00
last_verified_commit: ""
risk: medium
related_issue: ""
related_pr: ""
depends_on: []
blocks: []
owned_paths:
  - .github/workflows/ci.yml
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260725-windows-only.md
modules_touched:
  - continuous integration
reuses:
  - .github/workflows/reusable-checks.yml
  - .github/workflows/reusable-tests-lua.yml
  - .github/workflows/reusable-build-windows.yml
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Temporarily make Windows the only compiled OTClient target in required CI while retaining non-compiling syntax and static validation.

# Acceptance criteria

- [ ] Required CI compiles and tests only Windows targets.
- [ ] Linux, macOS, Android, browser and Docker build jobs are not emitted by the primary CI workflow.
- [ ] Fast checks and Lua syntax checks remain required.
- [ ] Required-job evaluation matches the Windows-only workflow graph.
- [ ] Build/test documentation records the temporary Windows-only policy.
- [ ] Workflow validation and an observed PR run succeed.

# Confirmed context

- The repository owner explicitly requested Windows-only compilation for the current phase.
- The current primary workflow compiles Linux and Windows and can also emit macOS, Android, Docker and browser builds.
- Ubuntu-hosted lightweight coordination/check jobs may remain; they do not compile the client.
- External repositories remain read-only.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Primary CI | Required-check orchestration | `.github/workflows/ci.yml` | Narrow the active graph rather than replacing CI. |
| Windows reusable build | Windows compile/test matrix | `.github/workflows/reusable-build-windows.yml` | Remains the only compiled target. |
| Fast/Lua checks | Non-compiling validation | reusable checks and Lua workflows | Preserve cheap safety checks. |

# Ownership and overlap check

- Open PRs inspected: #25 and #26 affect audit/upstream synchronization, not the primary CI workflow.
- Overlaps: changing `.github/workflows/ci.yml` will cause workflow reruns for open implementation PRs after base updates.
- Resolution: deliver this as a separate narrow CI PR and do not modify feature branches.

# Current state

Implementation started on a dedicated branch.

# Plan

1. Reduce `.github/workflows/ci.yml` to fast checks, Lua syntax and Windows build/test.
2. Update build/test policy and changelog.
3. Validate emitted jobs on the PR and merge when required checks pass.

# Work log

## 2026-07-25T11:00:00+02:00

- Changed: created the dedicated Windows-only CI branch and task record.
- Learned: the current required gate models six build scopes; all non-Windows scopes must be removed consistently.
- Failed/blocked: none.
- Result: implementation can proceed without touching client source or external repositories.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep fast checks and Lua syntax on Ubuntu runners | They do not compile a Linux client and preserve inexpensive validation. | none |
| Leave reusable non-Windows workflows in the repository but uncalled | Makes the policy easy to reverse without running those builds now. | none |
| Remove non-Windows jobs from the required graph instead of forcing successful skips | Avoids misleading checks and keeps the required gate aligned with actual policy. | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `.github/workflows/ci.yml` | Windows-only required CI graph | planned |
| `docs/agents/BUILD_TEST_MATRIX.md` | Temporary platform validation policy | planned |
| `docs/agents/CHANGELOG.md` | Discoverable CI policy change | planned |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| pending | PR workflow emission and required gate | not-run | Must show only Windows compilation. |

# Failed approaches and dead ends

None.

# Risks and compatibility

- Runtime: none; no shipped client code changes.
- Data/migration: none.
- Security: fast/static checks remain active.
- Backward compatibility: non-Windows build definitions remain available but dormant.
- Cross-repo rollout: none.
- Rollback: restore the removed CI job calls and required-gate mappings.

# Remaining work

1. Update the primary workflow and documentation.

# Handoff

## Start here

Read this task and `.github/workflows/ci.yml`.

## Do not repeat

Do not delete reusable non-Windows workflows; only remove them from the active primary graph.

## Required reads

- `AGENTS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `.github/workflows/ci.yml`

## Open questions

None.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not applicable
- Changelog updated: pending
- Archived at: pending
