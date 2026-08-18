# Native-login canonical bootstrap and same-generation Gate B

Task: `OTC-20260818-native-login-to-ingame-e2e`

This checkpoint records the single authorized physical canonical bootstrap transaction after the fresh controller-plane inventory proved authoritative registration absent.

## Provenance

```text
BASE_MAIN=a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
WORKFLOW_HEAD=d1ab020f11365abeab7a0c2cbd7eeea3e99de38b
RUN=32125054251
JOB=95673637453
RUNNER=synology-otclient-01
WORKFLOW=Track A native-login canonical bootstrap
RESULT=SUCCESS
```

The physical job checked out the exact PR head, re-proved that live `main` still equalled the exact task base, and reran deterministic Track A admission immediately before crossing the runtime boundary:

```text
TRACK_A_AGENT_RUNTIME_CHANGED_TASKS=1
TRACK_A_AGENT_RUNTIME_BRANCH_BOUND_TASKS=1
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
NATIVE_LOGIN_BOOTSTRAP_ADMISSION_POLICY=PASS
```

The current raw-XRes worker adapter and its retained fixtures passed before launch:

```text
canonical XRes worker-adapter tests = PASS
raw XRes owner tests = PASS
raw XRes wire tests = PASS
TRACK_A_CANONICAL_XRES_ADAPTER=PASS
NATIVE_LOGIN_CANONICAL_XRES_WORKER=PASS
NATIVE_LOGIN_SUPPORT_ROOT_PREFLIGHT=PASS
NATIVE_LOGIN_SYSTEM_XKBCOMP_PREFLIGHT=PASS
```

System `xkbcomp` retained the promoted exact SHA:

```text
0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
```

## Controller transition

Immediately before acquisition, the canonical lease was still the released generation observed by the no-client inventory:

```text
status=released
generation=8
controller_task=null
controller_session=null
```

The task then acquired exactly one new lease generation without stale takeover or idempotent reuse:

```text
TRACK_A_CANONICAL_LEASE_ACQUIRE=true
TRACK_A_CANONICAL_LEASE_GENERATION=9
TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER=false
TRACK_A_CANONICAL_LEASE_IDEMPOTENT=false
```

## Physical bootstrap

The promoted worker completed the required physical stages in order:

```text
warp_start
wireproxy_configtest_start
wireproxy_configtest_pass
warp_egress_probe_start
warp_egress_probe_pass
warp_pass
xvfb_start
xvfb_pass
vnc_start
vnc_pass
client_start
client_window_wait_start
client_window_wait_pass
```

The cancellation-safe transition controller then reported:

```text
TRACK_A_CANONICAL_BOOTSTRAP=PASS
TRACK_A_CANONICAL_LEASE_GENERATION=9
TRACK_A_CANONICAL_GATE_B=PASS
TRACK_A_CANONICAL_LEASE_GENERATION=9
NATIVE_LOGIN_BOOTSTRAP_RESULT=REGISTERED_GATE_B_PASS
```

## Authoritative runtime registration

The sanitized registration committed by the transition was:

```json
{
  "boot_id_sha256": "a7395225814c9a850ff7663d0bce2dd289cf300c37d78e286d5c7d31043653f9",
  "client_sha256": "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe",
  "client_size": 51965216,
  "client_version": "15.32.df7b29",
  "display": ":99",
  "lease_generation": 9,
  "pid": 2658,
  "process_start_ticks": 66643010,
  "registration_generation": 1,
  "remote_view_endpoint": "127.0.0.1:6082",
  "remote_view_mapping": "PROVEN",
  "runtime_id": "track-a-canonical-live",
  "schema_version": 1,
  "source_run": "32125054251",
  "source_task": "OTC-20260818-native-login-to-ingame-e2e",
  "state": "UNKNOWN",
  "window_identity": "x11-window:12582929"
}
```

This is evidence for that exact bootstrap/Gate-B transaction. Subsequent runtime work must freshly revalidate process/display/session identity and current controller generation; it may not treat these values as transferable authority.

## Release and secret boundary

After Gate B and registration validation, the task explicitly released controller authority while leaving the registered physical runtime idle:

```text
TRACK_A_CANONICAL_LEASE_RELEASE=true
TRACK_A_CANONICAL_LEASE_GENERATION=9
status=released
generation=9
controller_task=null
controller_session=null
NATIVE_LOGIN_RUNTIME_CONTROLLER_RELEASED=true
NATIVE_LOGIN_PERSISTENT_RUNTIME_LEFT_IDLE=true
NATIVE_LOGIN_CREDENTIAL_ACCESS=false
NATIVE_LOGIN_LOGIN_PERFORMED=false
NATIVE_LOGIN_GAMEPLAY_PERFORMED=false
```

Therefore this checkpoint does **not** claim authentication, character selection, game-server acceptance, map entry or `IN_GAME`.

## One-shot cleanup

The bootstrap workflow was removed immediately after the successful physical run to prevent replay from later task updates:

```text
WORKFLOW_REMOVAL_COMMIT=933d1841cee25c2bb65fa236e854e342efc261c0
```

## Classification

```text
FACT: canonical bootstrap attempt 1/1 succeeded.
FACT: exact official client registration generation 1 was published against lease generation 9.
FACT: same-generation Gate B passed before the registration was accepted.
FACT: controller authority was then released at generation 9 while the registered runtime was deliberately left idle.
FACT: no credentials, account login or gameplay action occurred in this bootstrap transaction.
NEXT_LEGAL_STEP: fresh post-bootstrap admission from current controller-plane metadata, followed by current-generation rebind/Gate-B as required before any retained-session observation or native auth.
```
