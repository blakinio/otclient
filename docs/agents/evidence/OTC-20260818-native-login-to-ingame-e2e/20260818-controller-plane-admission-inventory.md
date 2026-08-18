# Native-login controller-plane admission inventory

Task: `OTC-20260818-native-login-to-ingame-e2e`

This checkpoint records the single fresh no-client controller-plane inventory required before physical `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` execution.

## Provenance

```text
BASE_MAIN=a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
SEMANTIC_HEAD=82d27d97fce047dbad648212428e0b3cdb7f6211
RUN=32124348434
JOB=95671496871
RUNNER=synology-otclient-01
WORKFLOW=Track A native-login admission inventory
RESULT=SUCCESS
```

Immediately before reading controller metadata, the physical job revalidated that the live `main` ref still equalled the PR base and that the current Track A admission passed deterministic governance:

```text
NATIVE_LOGIN_CURRENT_MAIN=PASS
TRACK_A_AGENT_RUNTIME_CHANGED_TASKS=1
TRACK_A_AGENT_RUNTIME_BRANCH_BOUND_TASKS=1
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
NATIVE_LOGIN_ADMISSION_POLICY=PASS
```

## Direct controller-plane facts

The read occurred under a nonblocking shared flock on the already-existing canonical coordination lock and used only whitelisted non-secret lease/registration fields.

```text
NATIVE_LOGIN_CANONICAL_LEASE=PRESENT
NATIVE_LOGIN_CANONICAL_LEASE_SCHEMA_VERSION=1
NATIVE_LOGIN_CANONICAL_LEASE_RUNTIME_ID=track-a-canonical-live
NATIVE_LOGIN_CANONICAL_LEASE_STATUS=released
NATIVE_LOGIN_CANONICAL_LEASE_GENERATION=8
NATIVE_LOGIN_CANONICAL_LEASE_CONTROLLER_TASK=null
NATIVE_LOGIN_CANONICAL_LEASE_CONTROLLER_SESSION=null
NATIVE_LOGIN_CANONICAL_LEASE_EXPIRED=false
NATIVE_LOGIN_CANONICAL_REGISTRATION=ABSENT
NATIVE_LOGIN_ADMISSION_RESULT=REGISTRATION_ABSENT
NATIVE_LOGIN_CANONICAL_CONTROL_METADATA_UNCHANGED=true
NATIVE_LOGIN_ADMISSION_INVENTORY=COMPLETE
```

The job explicitly recorded that this discovery phase did not cross any client or secret boundary:

```text
NATIVE_LOGIN_CLIENT_PROCESS_OBSERVATION=false
NATIVE_LOGIN_X11_OBSERVATION=false
NATIVE_LOGIN_VNC_RFB_OBSERVATION=false
NATIVE_LOGIN_NETWORK_SESSION_OBSERVATION=false
NATIVE_LOGIN_CREDENTIAL_ACCESS=false
NATIVE_LOGIN_LOGIN_PERFORMED=false
NATIVE_LOGIN_GAMEPLAY_PERFORMED=false
NATIVE_LOGIN_CONTROLLER_MUTATION=false
```

## Classification

```text
FACT: authoritative canonical registration was absent at this fresh inventory.
FACT: canonical lease generation 8 existed in released state with no controller task/session.
FACT: controller metadata was unchanged across the read-only probe.
FACT: no client/process/X11/VNC/network/session observation and no credential/login/gameplay/controller mutation occurred.
INFERENCE: ordinary canonical reuse/rebind is unavailable from this checkpoint because there is no authoritative registration.
NEXT_LEGAL_TRANSITION: one separately admitted canonical bootstrap transaction using the current promoted implementation, subject to current-main freshness and deterministic admission immediately before execution.
```

No historical PID, XID, display, registration, session, lease authority or login budget is inherited by that transition.

## One-shot cleanup

The temporary inventory workflow was removed immediately after the semantic run so it cannot be replayed from later task updates:

```text
WORKFLOW_REMOVAL_COMMIT=271d84bbe3ead2d5689f9c4a445eff193113c421
```
