---
task_id: OTC-20260725-windows-only
coordination_id: ""
status: complete
agent: "GPT-5.6 Thinking"
branch: ci/OTC-20260725-windows-only
base_branch: main
created: 2026-07-25T11:00:00+02:00
updated: 2026-07-25T20:32:35+02:00
last_verified_commit: fd283c1a6d99dd870f09ee45fdf591541a6f71e9
risk: medium
related_issue: ""
related_pr: "#27"
depends_on: []
blocks: []
owned_paths:
  - .github/workflows/ci.yml
  - docs/agents/BUILD_TEST_MATRIX.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/archive/OTC-20260725-windows-only.md
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
- [x] Full changed-file and diff review completed.
- [x] Current-head CI and `CI / Required` succeeded.
- [x] PR #27 squash-merged through branch protection.

# Delivered

| Path | Result |
|---|---|
| `.github/workflows/ci.yml` | Primary CI emits fast/static checks, Lua syntax and the five-job Windows matrix only. |
| `docs/agents/BUILD_TEST_MATRIX.md` | Records Windows as the sole compiled and required target for the current phase. |
| `docs/agents/CHANGELOG.md` | Records the temporary Windows-only CI policy. |

Reusable Linux, macOS, Android, browser and Docker workflows remain present but dormant. Ubuntu runners continue to execute inexpensive orchestration and syntax/static validation without compiling a Linux client.

# Validation

| Commit/run | Check | Result |
|---|---|---|
| `336b2c659c54c75ba917a0bc3cab0d0b7e586776` | Full net diff review against current `main` before merge | passed; only four declared CI/docs/task paths |
| same | PR comments, reviews and inline threads | passed; none present |
| run `30167318524` / CI #210 | Fast checks and Lua syntax | success |
| same | Windows CMake Release | success |
| same | Windows CMake Tests and CTest | success |
| same | Windows Solution Debug | success |
| same | Windows Solution OpenGL | success |
| same | Windows Solution DirectX | success |
| same | `CI / Required` | success |
| `fd283c1a6d99dd870f09ee45fdf591541a6f71e9` | Squash merge of PR #27 | complete |

# Decisions

- Lightweight Ubuntu jobs remain because they do not compile a non-Windows client and preserve inexpensive validation.
- Reusable non-Windows workflows remain in the repository so a future explicit policy change can re-enable them.
- Non-Windows jobs were removed from the required graph instead of being represented as misleading successful skips.
- No required failure was bypassed; merge occurred only after the current branch was updated to `main` and CI #210 was fully green.

# Failed approaches and recovery

- A direct merge attempt was rejected even after an earlier green run because the PR branch was six commits behind `main` under strict branch protection.
- The branch was updated by a non-forced fast-forward through the current synthetic merge state, preserving its four-file net diff. CI #210 then ran on the exact current head and passed.
- No checks, tests or branch protections were disabled.

# Risks and compatibility

- Runtime: none; shipped client code was not changed.
- Security: fast/static checks and Lua syntax remain required.
- Compatibility: no compatibility claim is made for dormant non-Windows targets.
- Rollback: restore the removed CI job calls, path scopes and required-gate mappings in a focused policy PR.

# Handoff

The Windows-only policy is active on `main` at `fd283c1a6d99dd870f09ee45fdf591541a6f71e9`.

Future client source changes must pass the current five-job Windows matrix. Re-enabling another compiled platform requires an explicit repository-owner decision and a focused CI policy change.

# Completion

- Final status: complete
- PR: #27
- Merge commit: `fd283c1a6d99dd870f09ee45fdf591541a6f71e9`
- Catalogue updated: not applicable
- Changelog updated: yes
- Archived at: 2026-07-25T20:32:35+02:00
