# Native-login canonical generation rebind and Gate B

Task: `OTC-20260818-native-login-to-ingame-e2e`

This checkpoint records the current-generation controller acquisition and the promoted canonical registration rebind required after the persistent runtime remained registered against released lease generation 9.

## Pre-acquire configuration discriminator

The first rebind workflow head was:

```text
HEAD=294f4f01f0ca122e47df98e67486bae05dba6285
RUN=32125796858
JOB=95675952044
RESULT=FAIL_PRE_ACQUIRE
DISCRIMINATOR=TRACK_A_CANONICAL_LEASE_ERROR=invalid_ttl
```

That run passed current-main admission, governance and XRes helper tests, and proved the expected released-generation-9 / registration-1-on-generation-9 controller state. It then failed at `lease acquire --ttl-seconds 3600` because the promoted lease implementation permits at most 2700 seconds. No lease generation was acquired, no rebind was invoked, and no client/auth/login/gameplay action occurred.

The repository source of truth `.github/scripts/tibia-official-client-re-canonical-live-lease.py` defines:

```text
DEFAULT_TTL_SECONDS=2700
MIN_TTL_SECONDS=60
MAX_TTL_SECONDS=2700
```

The only repair was therefore to bound the requested lease TTL to 2700 seconds; the runtime hypothesis and registration identity were unchanged.

## Successful current-generation transition

Corrected exact workflow head:

```text
HEAD=f9ccc6f1d0aa60c188534c1e83f25cd915323b72
RUN=32125924194
JOB=95676341318
RUNNER=synology-otclient-01
RESULT=SUCCESS
```

Immediately before lease acquisition the workflow re-proved:

```text
TRACK_A_AGENT_RUNTIME_CHANGED_TASKS=1
TRACK_A_AGENT_RUNTIME_BRANCH_BOUND_TASKS=1
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
NATIVE_LOGIN_REBIND_ADMISSION_POLICY=PASS
NATIVE_LOGIN_REBIND_PRECHECK=RELEASED_GEN9_REG1_9
```

The adapted raw-XRes worker and retained tests passed before crossing the transition boundary:

```text
canonical XRes worker-adapter tests = PASS
raw XRes owner tests = PASS
raw XRes wire tests = PASS
TRACK_A_CANONICAL_XRES_ADAPTER=PASS
NATIVE_LOGIN_REBIND_XRES_WORKER=PASS
```

## Lease acquisition

The one admitted acquire produced exactly the expected next controller generation:

```text
TRACK_A_CANONICAL_LEASE_ACQUIRE=true
TRACK_A_CANONICAL_LEASE_GENERATION=10
TRACK_A_CANONICAL_LEASE_EXPIRES_AT_EPOCH=1787050906
TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER=false
TRACK_A_CANONICAL_LEASE_IDEMPOTENT=false
NATIVE_LOGIN_REBIND_ACQUIRED_GENERATION=10
```

Controller identity:

```text
controller_task=OTC-20260818-native-login-to-ingame-e2e
controller_session=chatgpt-native-login-e2e-20260818
```

The raw lease capability remains only in the task-local protected Synology runtime path and was never emitted to logs or committed.

## Rebind and same-generation Gate B

The promoted transition controller then directly reported:

```text
TRACK_A_CANONICAL_REBIND=PASS
TRACK_A_CANONICAL_LEASE_GENERATION=10
TRACK_A_CANONICAL_GATE_B=PASS
TRACK_A_CANONICAL_LEASE_GENERATION=10
NATIVE_LOGIN_REBIND_RESULT=REBIND_GATE_B_PASS_ACTIVE_GEN10
```

Authoritative registration after the transition:

```json
{
  "boot_id_sha256": "a7395225814c9a850ff7663d0bce2dd289cf300c37d78e286d5c7d31043653f9",
  "client_sha256": "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe",
  "client_size": 51965216,
  "client_version": "15.32.df7b29",
  "display": ":99",
  "lease_generation": 10,
  "pid": 2658,
  "process_start_ticks": 66643010,
  "registration_generation": 2,
  "remote_view_endpoint": "127.0.0.1:6082",
  "remote_view_mapping": "PROVEN",
  "runtime_id": "track-a-canonical-live",
  "schema_version": 1,
  "source_run": "32125924194",
  "source_task": "OTC-20260818-native-login-to-ingame-e2e",
  "state": "UNKNOWN",
  "window_identity": "x11-window:12582929"
}
```

The boot identity, exact client fence, PID/start identity, display, window and remote-view mapping remained the same physical runtime that bootstrap generation 9 had registered; only the controller binding advanced to lease generation 10 and registration generation 2 after fresh revalidation.

## Current authority and negative boundary

The successful workflow intentionally kept the proven generation-10 controller lease active for the same task/session rather than releasing and gratuitously forcing another generation transition:

```text
NATIVE_LOGIN_REBIND_LEASE_LEFT_ACTIVE=true
NATIVE_LOGIN_REBIND_CREDENTIAL_ACCESS=false
NATIVE_LOGIN_REBIND_LOGIN_PERFORMED=false
NATIVE_LOGIN_REBIND_GAMEPLAY_PERFORMED=false
```

This checkpoint therefore proves current controller authority and Gate B, not authentication or `IN_GAME`.

## One-shot cleanup

The completed rebind workflow was removed after the successful run so later task-document updates cannot replay the acquire/rebind transaction:

```text
WORKFLOW_REMOVAL_COMMIT=87ad54f282cf695f5b44503f766a0b93302d22cf
```

## Classification

```text
FACT: released lease generation 9 advanced exactly once to active generation 10 for this task/session.
FACT: no stale takeover or idempotent reuse occurred.
FACT: canonical rebind advanced registration generation 1/lease 9 to registration generation 2/lease 10.
FACT: immediate same-generation Gate B passed for the exact registered official client.
FACT: generation-10 controller authority was intentionally retained after success.
FACT: no credentials, account login or gameplay occurred.
NEXT_LEGAL_STEP: while the same generation-10 lease remains fresh, renew/validate it without acquiring a new generation, rerun same-generation Gate B, and perform a bounded no-secret retained-native-session/auth-state discriminator before any credential request.
```
