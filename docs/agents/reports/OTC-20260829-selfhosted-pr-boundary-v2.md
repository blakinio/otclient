# OTC-20260829 self-hosted PR boundary v2 evidence

## Historical causal RED

The original hosted RED remains run `33236883246`, job `99059301992`: the trusted-main canonical lease workflow exposed a PR-triggered Synology job. PR #788 then received two P1 and one P2 review findings and is superseded by this fresh-main continuation.

## Review-regression RED

On fresh base `b5c7d0fbb0e9667abe6fea7bbaea8834c1c654b5`, the carried-forward #788 implementation passed its old checker, then the new regression failed with all three review defects:

```text
TRACK_A_SELFHOSTED_PR_REVIEW_REGRESSION_RED:
  mixed workflow_dispatch OR pull_request predicate was incorrectly accepted;
  mixed pull_request OR issue_comment predicate was incorrectly accepted;
  canonical lease self-hosted job does not require refs/heads/main before scheduling
```

## GREEN

The event predicate checker now recursively evaluates top-level boolean structure for `github.event_name`. It rejects an OR branch that can admit `pull_request` but correctly accepts an `issue_comment` gate whose nested OR only selects comment bodies. The canonical lease physical job requires all three before scheduling: owner, `workflow_dispatch`, and `github.ref == 'refs/heads/main'`.

Local focused results:

```text
TRACK_A_SELFHOSTED_PR_REVIEW_REGRESSION=PASS
TRACK_A_SELFHOSTED_PR_BOUNDARY=PASS
python -m py_compile boundary + regressions = PASS
git diff --check = PASS
```

## Security architecture disposition

The PR-head checker is explicitly not treated as the primary hostile-code boundary. `TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md` requires the physical selector offline by default and a fresh disposable one-job runner, queued only for one exact trusted-main job, before any secrets. This addresses historical same-UID/workspace residue as a separate problem from workflow predicate validation.

No physical runner, credentials, official client, login, or network payload was used for this v2 evidence. Pre-restack hosted validation was GREEN: boundary/audit run `33259495831` (`AUDIT_RESULT=PASS`), canonical lease `33259495743` with physical job skipped, governance `33259495742`, and required CI `33259495833`. Final restacked exact-head rerun remains mandatory before merge.

## Independent validator role

A separate hosted `fresh-audit` job runs `.github/scripts/audit_track_a_selfhosted_pr_boundary.py` from a fresh exact-head checkout with full base history. It does not trust the task narrative: it inventories the complete PR diff, exercises independent predicate counterexamples, directly inspects the canonical pre-scheduling gate, and verifies the no-runtime task/secret-runner fences. Stable failures are emitted as `AUDIT-F001`..`AUDIT-F011`.
