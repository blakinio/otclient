# Independent Spark audit - managed-auth blocker

Date: 2026-08-19
Task: `OTC-20260818-native-login-to-ingame-e2e`
PR: #528
Audit target attempted: `0a839f5d6a01690b8600057eae9532516055d251`
Model required/selected: `gpt-5.3-codex-spark`
Managed path: `spark-review-runner` / `codex-cli 0.147.0`

## Preconditions

The branch had just merged `main@aaf6706cfcd02e70511e5fa7e9ef9b0d7e1f0d12` cleanly and was zero commits behind at audit dispatch. Exact-head checks on `0a839f5d6a01690b8600057eae9532516055d251` all passed:

```text
CI run 32242937598: PASS
Track A agent runtime governance run 32242937431: PASS
Track A native auth bridge validation run 32242937489: PASS
```

The repository-approved runner contained Codex CLI and `codex login status` reported ChatGPT-managed login configuration. No API key or owner AI credential was read, exported, printed, copied or committed.

## Audit invocation result

A read-only, ephemeral independent falsification audit was dispatched with exactly `gpt-5.3-codex-spark`. The audit prompt required review of object provenance/rebasing, Qt thread correctness, selected-character identity, false login-success and false IN_GAME alternatives, secret leakage, runtime admission, helper/socket peer identity, process-handoff interpretation, and separation of historical proof from current session state.

The model did not execute. The managed authentication failed before any model response with HTTP 401 conditions classified by Codex as:

```text
token_invalidated
refresh_token_invalidated
```

CLI exit code: `1`. No final audit message was produced.

## Controlling disposition

```yaml
INDEPENDENT_AUDIT: NOT_RUN
MATERIAL_FINDINGS: UNKNOWN
HISTORICAL_E2E_PROOF_WITHDRAWN: false
MERGE_READINESS: BLOCKED
BLOCKER: OWNER_REAUTH_REQUIRED_FOR_REPOSITORY_APPROVED_SPARK_RUNNER
```

This authentication failure is not evidence for or against the native-login implementation. It only means the required independent audit remains outstanding. Do not substitute self-review, another model/provider, OpenAI API credentials, hosted Codex review, or a repeated credential-bearing Tibia login.

## Next action

The owner must reauthenticate ChatGPT Codex on `spark-review-runner`. After that, rerun the exact `gpt-5.3-codex-spark` falsification audit on the then-current exact PR head, repair any material finding, rerun exact-head required checks, and only then reconsider readiness/merge.
