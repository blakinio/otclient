# OTC-20260829 V4 field6 admission v2 evidence

Replacement PR: #796 (supersedes stale #786).

## Scope

Repository-only admission repair on fresh protected main after merged PR #795. This package itself performs no Synology job, official-client execution, credential access, GUI input, login submit, packet capture, or physical action. `physical_action_count` remains `0` and `FIELD6_VALUE=UNKNOWN`.

## Causal RED

The clean-runner design deliberately removes persistent authorization state, so a GitHub rerun could otherwise replay the same comment. Before changing the workflow, the security regression failed exactly:

```text
FIELD6_SECURITY_CONTRACT_RED: live workflow missing GITHUB_RUN_ATTEMPT == 1 guard
```

## GREEN implementation

The first trusted-main live-admission step now requires `GITHUB_RUN_ATTEMPT == 1` and emits `TRACK_A_FIELD6_RUN_ATTEMPT=1` before authorization consumption or secret exposure. Credential strings continue to enter `xdotool type` only through stdin (`--file -`), not argv.

Local focused GREEN before publication:

```text
TRACK_A_CURRENT_LOGIN_FIELD6_SECURITY_CONTRACT=PASS
TRACK_A_CURRENT_LOGIN_FIELD6_RUNTIME_CONTRACT=PASS
git diff --check = PASS
```

## Independent audit

`.github/scripts/audit_track_a_current_login_field6_admission.py` is a separate deterministic validator role. On a fresh hosted checkout it inventories the complete PR diff, verifies trusted #795 clean-runner contract presence, exact task admission/no-relogin/no-gameplay fences, exact V4 owner trigger, fail-closed run-attempt/auth/secret ordering, single-step secret references, and stdin-only xdotool credential transport. Stable findings use `FIELD6-AUDIT-F001`..`FIELD6-AUDIT-F020`. Exact-head hosted evidence remains required before merge.

## Remaining physical gate

Merge of this admission does not itself prove a safe credential environment. The exact V4 trigger remains forbidden until a fresh one-job runner satisfying `TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md` is actually provisioned and its queued-job uniqueness/provenance is verified.

## Boundary-audit blocker repair

The first #796 hosted generation exposed a merged-#795 audit reuse defect: run `33260012616`, job `99120220924`, failed `AUDIT-F003` solely because the audit hardcoded #795 paths. Separate PR #798 repaired that validator and squash-merged as `0c9c4e1021b09eb0c2de6fe426ad0688e4539173`; #796 is restacked on that trusted base before final validation.

Final local pre-restack after #798: admission independent audit PASS, security contract PASS, field6 runtime contract PASS, reusable self-hosted boundary PASS, `git diff --check` PASS. Final hosted exact-head evidence after one-commit restack remains authoritative for merge.
