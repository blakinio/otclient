# Repository governance

This document records the repository-governance and CI baseline for the
`blakinio/otclient` fork. The snapshot was taken on 2026-07-11 before the
governance changes were implemented.

## Initial state

- The default branch is `main`. The fork initially has only that remote branch.
- `origin/main` and `opentibiabr/otclient:main` both point to
  `bdea0b23b4a738809d698cb7e4f88a299dd6bffc`, so the fork starts without an
  upstream delta.
- Repository merge settings are: auto-merge disabled, update-branch disabled,
  merge commits enabled, squash merge enabled, rebase merge enabled, and
  automatic head-branch deletion disabled.
- Secret scanning and push protection are enabled. Dependabot security updates
  are disabled.
- The repository has no repository Rulesets. Classic protection is active on
  `main`, with pull requests required and zero approvals, linear history
  required, administrator enforcement disabled, signed commits not required,
  and force pushes and deletions blocked.
- The existing classic protection has no required status checks, does not
  require branches to be up to date, and does not require conversation
  resolution.
- GitHub Actions is enabled for all actions. Full-SHA pinning is not enforced by
  the repository setting. The default `GITHUB_TOKEN` permission is read-only,
  workflows cannot approve pull requests, and first-time external contributors
  require approval before workflows run.
- The main `CI` workflow uses workflow-level path filters. A pull request that
  changes only documentation or repository metadata can therefore have no CI
  check at all.
- CI has no stable aggregate job suitable for branch protection. Platform jobs
  are conditional and draft pull requests skip most work.
- The Docker build is called by CI with `packages: write`, including pull
  request runs. Publishing and validation share a reusable workflow.
- External actions use a mixture of full commit SHAs and mutable version tags.
- There is no Dependabot configuration, CODEOWNERS file, contribution policy,
  or security policy. Existing pull request and issue templates do not capture
  all Canary and protocol compatibility information.

## Risks found

1. A required check cannot be selected reliably when GitHub skips the entire
   workflow because of a top-level path filter.
2. Conditional jobs do not provide one stable pass/fail decision, and an
   incautious aggregate job could hide a failed prerequisite behind a skipped
   downstream build.
3. Pull request code receives broader package permissions than a validation
   build needs. The Docker build also receives a token as a BuildKit secret.
4. Mutable action tags allow upstream action content to change without a pull
   request in this repository.
5. Syntax validation through reviewdog is unavailable to fork pull requests,
   so XML and Lua errors need direct blocking checks as well as optional PR
   annotations.
6. Native Dependabot auto-merge would be unsafe before both repository
   auto-merge and the `CI / Required` branch-protection check are enabled.
7. Retrying ordinary `failure` conclusions would conceal code, test, or lint
   defects. A retry must be restricted to a single infrastructure retry.
8. The cache-cleanup workflow installs a moving GitHub CLI extension at run
   time, adding avoidable supply-chain drift.

## Implementation decisions

- Run `CI` for every pull request to `main`, every merge queue group, and every
  push to `main`. Detect paths inside the workflow and skip only expensive
  platform builds.
- Add the always-running aggregate job named `Required`. It depends on every
  relevant CI job, accepts only `success` and justified `skipped` results, and
  rejects `failure`, `cancelled`, and every other conclusion. Its stable check
  context is `CI / Required`.
- Keep fast syntax checks active for all pull requests, including drafts. Skip
  expensive platform builds while a pull request is a draft; the
  `ready_for_review` event starts them.
- Treat YAML, workflow, XML, Lua syntax, compilation, and CTest failures as
  blocking. Keep luacheck and cppcheck informational because the inherited code
  has historical findings.
- Run actionlint from source pinned to an exact upstream commit. This avoids a
  mutable or unchecked downloaded executable.
- Make pull request Docker validation read-only and do not pass repository
  tokens into the untrusted build. Publish GHCR images only in a separate,
  trusted push-to-`main` workflow.
- Remove the preset-level vcpkg `--binarysource=clear` override that masked the
  CI-provided cache. Linux and Windows consume the GitHub Packages vcpkg cache
  read-only; only the trusted Docker publication path may write it. Android
  uses its Actions cache read-only outside trusted pushes.
- Pin every third-party `uses:` reference to a full commit SHA and let
  Dependabot propose later SHA updates.
- Enable native auto-merge only for Dependabot patch and minor updates. A
  read-only `pull_request_target` workflow uses the pinned metadata action and
  uploads data without checking out PR code. After successful CI, a separate
  trusted `workflow_run` validates the artifact's workflow provenance, the live
  PR head, the successful `Required` job, repository auto-merge, and the
  protected `CI / Required` context before requesting squash auto-merge. It
  never executes artifact contents or pull request code.
- Permit at most one automatic rerun for unambiguous infrastructure conclusions
  (`cancelled`, `timed_out`, or `startup_failure`). Ordinary failures are never
  retried automatically.
- Keep the fork-specific governance work outside `src/`, `modules/`, `mods/`,
  and `data/` so upstream synchronization remains a normal fetch/rebase or
  merge operation.

## Blocking and informational controls

| Control | Policy |
| --- | --- |
| yamllint and YAML parsing | Blocking |
| actionlint | Blocking |
| Lua bytecode syntax compilation | Blocking |
| xmllint | Blocking |
| Linux, Windows, macOS, Android, browser, and Docker builds when selected | Blocking |
| CTest in the Linux debug build | Blocking |
| luacheck | Informational |
| cppcheck | Informational |

A skipped platform build is acceptable only when the path-scope detector says
that platform is unaffected, or while a pull request is a draft. The aggregate
job still observes failures in the detector and all prerequisite checks.

The intended scope behavior is:

- documentation, templates, and repository policy changes run blocking fast
  checks and Lua syntax, skip platform builds, and finish with `CI / Required`;
- Lua-only changes follow the same inexpensive path because they do not alter
  native compilation; the separate Docker publish workflow includes runtime
  assets when such a change reaches `main`;
- C++ source changes select every platform build;
- a draft runs blocking fast checks and Lua syntax but skips platform builds;
- `merge_group` and manual CI dispatch select every platform build; and
- a fork pull request receives no inherited repository secrets, persists no
  checkout credential, and can use only the explicitly read-only permissions.

## Recommended repository settings

After this pull request is merged, the repository-level settings should be:

```text
allow_auto_merge=true
allow_update_branch=true
allow_squash_merge=true
allow_merge_commit=false
allow_rebase_merge=false
delete_branch_on_merge=true
```

The helper at `scripts/configure-github-repository.sh` prints the proposed
change by default. Review its output, then run it explicitly with `--apply` only
after approval:

```bash
./scripts/configure-github-repository.sh
./scripts/configure-github-repository.sh --apply
```

The helper does not change repository visibility, the default branch, branch
protection, or Rulesets. It does not delete branches or force-push.

Dependabot is configured to request the `dependencies` and `ci` labels. Create
those labels before enabling scheduled updates if they are not already present;
GitHub otherwise creates the pull request without the missing labels.

## Main branch protection / Ruleset checkpoint

Do not apply this protection until a pull request has produced the check named
exactly `CI / Required`. After that first successful run, update either the
existing classic branch protection or an equivalent repository Ruleset for
`main` with all of the following:

- require changes through a pull request;
- require 0 approvals initially;
- do not require Code Owner review initially;
- require conversation resolution;
- require the status check `CI / Required`;
- require the branch to be up to date before merge;
- require linear history;
- block force pushes and branch deletion;
- do not require signed commits initially; and
- retain an emergency administrator bypass.

With GitHub CLI, inspect the registered contexts first:

```bash
gh api repos/blakinio/otclient/commits/HEAD/check-runs \
  --jq '.check_runs[].name' | sort -u
```

For classic branch protection, apply the checkpoint only after explicit
approval. Preserve the current 0-review and administrator-bypass posture while
adding strict status checks and conversation resolution. A minimal API payload
for the relevant fields is:

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["CI / Required"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 0,
    "require_last_push_approval": false
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
```

Re-read protection after applying it and confirm that the sole required CI
context is spelled exactly `CI / Required`. Signed commits are already disabled;
do not call the separate signatures endpoint. Do not enable mandatory Code
Owner approval while `@blakinio` is the only active maintainer.

## Upstream synchronization

Keep `origin` pointed at `blakinio/otclient` and `upstream` pointed at
`opentibiabr/otclient`. Governance changes are isolated on
`chore/repository-governance`; no client files are modified. A typical sync is:

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main
git push origin main
```

If the fork intentionally diverges later, use a reviewed merge or rebase on a
topic branch instead of force-pushing `main`.
