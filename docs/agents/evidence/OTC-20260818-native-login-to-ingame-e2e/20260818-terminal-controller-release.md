# Native-login terminal controller release

Task: `OTC-20260818-native-login-to-ingame-e2e`

After the protected cold-auth capability probe established `EXTERNAL_ACTION_REQUIRED`, the task released its current canonical controller authority without mutating the official client.

## Provenance

```text
HEAD=edd52adabb6a4e5dd1b77a6710f20cd01bdccc7b
RUN=32127353047
JOB=95680752008
RUNNER=synology-otclient-01
RESULT=SUCCESS
```

The release workflow first revalidated current-main admission and directly required that the live lease still belonged to this exact task/session at active generation 10:

```text
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
NATIVE_LOGIN_TERMINAL_RELEASE_PRECHECK=ACTIVE_GEN10_CURRENT_TASK
```

It then performed the canonical lease release:

```text
TRACK_A_CANONICAL_LEASE_RELEASE=true
TRACK_A_CANONICAL_LEASE_GENERATION=10
NATIVE_LOGIN_TERMINAL_RELEASE_RESULT=RELEASED_GEN10
```

The task-local lease token was deleted after release. The released controller state was rechecked as generation 10 with null controller task/session.

Negative boundary:

```text
NATIVE_LOGIN_TERMINAL_CLIENT_MUTATION=false
NATIVE_LOGIN_TERMINAL_CREDENTIAL_ACCESS=false
NATIVE_LOGIN_TERMINAL_LOGIN_PERFORMED=false
```

The registered physical client was deliberately left idle. Its historical PID/display/window values remain evidence only and do not transfer authority to a future continuation. Any continuation after the external secret-input boundary must start with a fresh controller-plane inventory/admission and may not reuse this released lease capability.

## One-shot cleanup

The terminal-release workflow was removed after the successful run:

```text
WORKFLOW_REMOVAL_COMMIT=43ade26425dbbb800b3f0e7eabc532b815eb925e
```
