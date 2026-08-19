# Native-login post-bootstrap controller inventory

Task: `OTC-20260818-native-login-to-ingame-e2e`

This checkpoint records the fresh controller-plane-only read performed after successful bootstrap/Gate B and controller release.

## Provenance

```text
BASE_MAIN=a518ceaef9135c05e36ffd7066b3acb2d81f8c4c
WORKFLOW_HEAD=4b02606b585c5f02f7f2293c5916f2a66ee6ad8a
RUN=32125504315
JOB=95675058329
RUNNER=synology-otclient-01
RESULT=SUCCESS
```

Immediately before metadata access:

```text
TRACK_A_AGENT_RUNTIME_CHANGED_TASKS=1
TRACK_A_AGENT_RUNTIME_BRANCH_BOUND_TASKS=1
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
NATIVE_LOGIN_POST_BOOTSTRAP_CURRENT_MAIN=PASS
NATIVE_LOGIN_POST_BOOTSTRAP_ADMISSION_POLICY=PASS
```

## Direct controller-plane facts

Every expected controller/registration fence evaluated true. The current state remained:

```text
NATIVE_LOGIN_POST_BOOTSTRAP_LEASE_STATUS="released"
NATIVE_LOGIN_POST_BOOTSTRAP_LEASE_GENERATION=9
NATIVE_LOGIN_POST_BOOTSTRAP_REGISTRATION_GENERATION=1
NATIVE_LOGIN_POST_BOOTSTRAP_REGISTRATION_LEASE_GENERATION=9
NATIVE_LOGIN_POST_BOOTSTRAP_REGISTRATION_STATE="UNKNOWN"
NATIVE_LOGIN_POST_BOOTSTRAP_REGISTRATION_PID=2658
NATIVE_LOGIN_POST_BOOTSTRAP_REGISTRATION_PROCESS_START_TICKS=66643010
NATIVE_LOGIN_POST_BOOTSTRAP_REGISTRATION_DISPLAY=":99"
NATIVE_LOGIN_POST_BOOTSTRAP_REGISTRATION_WINDOW_IDENTITY="x11-window:12582929"
NATIVE_LOGIN_POST_BOOTSTRAP_REGISTRATION_REMOTE_VIEW_ENDPOINT="127.0.0.1:6082"
NATIVE_LOGIN_POST_BOOTSTRAP_CONTROL_METADATA_UNCHANGED=true
NATIVE_LOGIN_POST_BOOTSTRAP_RESULT="REGISTERED_RELEASED_GEN9"
```

The registration exact-client fence and provenance were also rechecked as controller metadata:

```text
schema_version=1
runtime_id=track-a-canonical-live
client_version=15.32.df7b29
client_size=51965216
client_sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
source_task=OTC-20260818-native-login-to-ingame-e2e
source_run=32125054251
remote_view_mapping=PROVEN
```

## Negative boundary

This inventory explicitly recorded:

```text
NATIVE_LOGIN_POST_BOOTSTRAP_CLIENT_PROCESS_OBSERVATION=false
NATIVE_LOGIN_POST_BOOTSTRAP_X11_OBSERVATION=false
NATIVE_LOGIN_POST_BOOTSTRAP_NETWORK_OBSERVATION=false
NATIVE_LOGIN_POST_BOOTSTRAP_CREDENTIAL_ACCESS=false
NATIVE_LOGIN_POST_BOOTSTRAP_LOGIN_PERFORMED=false
NATIVE_LOGIN_POST_BOOTSTRAP_GAMEPLAY_PERFORMED=false
NATIVE_LOGIN_POST_BOOTSTRAP_CONTROLLER_MUTATION=false
```

Thus PID/display/window values above remain registration metadata only until a separately admitted current-runtime identity transition revalidates them directly.

## One-shot cleanup

The temporary post-bootstrap inventory workflow was removed immediately after the run:

```text
WORKFLOW_REMOVAL_COMMIT=f65fd28a68a18d6a57075b088b8df6baccc2db64
```

## Classification

```text
FACT: authoritative registration remains present and bound to released lease generation 9.
FACT: controller task/session remain null.
FACT: registration generation remains 1 and state remains UNKNOWN.
FACT: controller metadata did not change during the read-only probe.
INFERENCE: a new controller acquisition will advance the lease generation and therefore cannot authorize ordinary mutation against registration lease generation 9 without the promoted generation-rebind transition.
NEXT_LEGAL_TRANSITION: separately admitted canonical_rebind transaction after acquiring the new current controller lease, followed by current-generation Gate B before any retained-session observation/authentication.
```
