---
task_id: OTC-20260725-windows-only
coordination_id: ""
status: ready
agent: "GPT-5.6 Thinking"
branch: ci/OTC-20260725-windows-only
base_branch: main
created: 2026-07-25T11:00:00+02:00
updated: 2026-07-25T15:27:00+02:00
last_verified_commit: 13ed2a4b3814988c4a4d375baa68b6868679b5ca
risk: medium
related_issue: ""
related_pr: "#27"
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

- [x] Required CI graph contains only the Windows compiled target.
- [x] Linux, macOS, Android, browser and Docker build jobs are not emitted by the primary CI workflow definition.
- [x] Fast checks and Lua syntax checks remain required.
- [x] Required-job evaluation matches the Windows-only workflow graph.
- [x] Build/test documentation records the temporary Windows-only policy.
- [x] Workflow validation and an observed ready-for-review PR run succeed.

# Confirmed context

- The repository owner explicitly requested Windows-only compilation for the current phase.
- Ubuntu-hosted lightweight coordination/check jobs may remain; they do not compile the client.
- Reusable non-Windows workflows remain present but are no longer called from `.github/workflows/ci.yml`.
- External repositories remain read-only.

# Existing work to reuse

| Module/task/PR | Reuse | Evidence/path | Why it fits |
|---|---|---|---|
| Primary CI | Required-check orchestration | `.github/workflows/ci.yml` | Narrowed instead of replaced. |
| Windows reusable build | Windows compile/test matrix | `.github/workflows/reusable-build-windows.yml` | Sole compiled target. |
| Fast/Lua checks | Non-compiling validation | reusable checks and Lua workflows | Preserved unchanged. |

# Ownership and overlap check

- Open PRs inspected: #25 and #26 affect audit/upstream synchronization, not the primary CI workflow.
- Overlaps: changing `.github/workflows/ci.yml` will affect future workflow runs after this PR reaches `main`.
- Resolution: separate narrow PR #27; feature branches were not modified.

# Current state

Implementation and ready-for-review validation are complete on PR #27. Full changed-file and diff review found only the four declared paths. The observed workflow emitted fast checks, Lua syntax, the Windows build/test matrix and the required evaluator; it emitted no non-Windows client compilation.

# Plan

1. Confirm the task-record-only follow-up commit passes the current-head required gate.
2. Squash-merge PR #27 when the autonomous merge gate remains satisfied.
3. Archive the completed task in a focused post-merge documentation PR.

# Work log

## 2026-07-25T11:00:00+02:00

- Changed: created the dedicated Windows-only CI branch and task record.
- Learned: the prior required gate modeled six build scopes; all non-Windows scopes needed consistent removal.
- Failed/blocked: none.
- Result: implementation could proceed without client source or external repository changes.

## 2026-07-25T12:05:00+02:00

- Changed: removed Linux, macOS, Android, Docker and browser jobs/scopes from primary CI; retained Windows, fast checks and Lua syntax; updated policy and changelog.
- Learned: Ubuntu runners remain necessary for inexpensive orchestration and do not constitute Linux client compilation.
- Failed/blocked: none.
- Result: PR #27 has a four-file, policy-only diff and is ready for current-head CI validation.

## 2026-07-25T15:27:00+02:00

- Changed: reviewed the complete four-file diff, ready-for-review workflow run, PR metadata, comments, reviews and inline threads.
- Learned: workflow run `30153693814` emitted only fast checks, Lua syntax, five Windows compile/test jobs and `CI / Required`; every emitted job succeeded.
- Failed/blocked: none.
- Result: PR #27 satisfies its observable acceptance criteria and is ready for the final task-record commit check and squash merge.

# Decisions

| Decision | Reason/evidence | ADR |
|---|---|---|
| Keep fast checks and Lua syntax on Ubuntu runners | They do not compile a Linux client and preserve inexpensive validation. | none |
| Leave reusable non-Windows workflows in the repository but uncalled | The temporary policy remains easy to reverse without running those builds now. | none |
| Remove non-Windows jobs from the required graph instead of forcing successful skips | The required gate should represent actual policy, not misleading skipped targets. | none |

# Files and interfaces

| Path/interface/config/schema | Purpose | Status |
|---|---|---|
| `.github/workflows/ci.yml` | Windows-only required CI graph | implemented |
| `docs/agents/BUILD_TEST_MATRIX.md` | Temporary platform validation policy | implemented |
| `docs/agents/CHANGELOG.md` | Discoverable CI policy change | implemented |
| task record | Coordination and evidence | current |

# Validation and CI

| Commit | Command/check/workflow | Result | Evidence/notes |
|---|---|---|---|
| `134aace4c9ce2771b213323fcfbafaf480e5b5a4` | Full PR changed-file and diff review | passed | Only declared CI/docs/task paths; non-Windows reusable files are untouched. |
| `13ed2a4b3814988c4a4d375baa68b6868679b5ca` | GitHub Actions run `30153693814` | passed | Fast checks, Lua syntax, five Windows jobs and `CI / Required` succeeded; no Linux, macOS, Android, Docker or browser build job was emitted. |
| `13ed2a4b3814988c4a4d375baa68b6868679b5ca` | PR comments, reviews and review-thread inspection | passed | No comments, reviews or unresolved inline threads. |

# Failed approaches and dead ends

None.

# Risks and compatibility

- Runtime: none; no shipped client code changes.
- Data/migration: none.
- Security: fast/static checks remain active.
- Backward compatibility: non-Windows build definitions remain available but dormant.
- Cross-repo rollout: none.
- Rollback: restore the removed CI job calls, path scopes and required-gate mappings.

# Remaining work

1. Squash-merge PR #27 after the current-head required check succeeds.
2. Archive this record after the merge commit is known.

# Handoff

## Start here

Read PR #27, this task and `.github/workflows/ci.yml`.

## Do not repeat

Do not delete reusable non-Windows workflows; they are intentionally dormant.

## Required reads

- `AGENTS.md`
- `docs/agents/BUILD_TEST_MATRIX.md`
- `.github/workflows/ci.yml`

## Open questions

None.

# Completion

- Final status: ready for merge
- PR: #27
- Merge commit: pending
- Catalogue updated: not applicable
- Changelog updated: yes
- Archived at: pending
