# Native-login retained-session discriminator

Task: `OTC-20260818-native-login-to-ingame-e2e`

This checkpoint records the single structural read-only discriminator used after canonical rebind/Gate B to decide whether the freshly registered official client exposed a reusable native character-selection model without requesting credentials.

## Non-runtime preflight failures

Two environmental/configuration failures occurred before the successful native-model read:

```text
RUN=32126542329 JOB=95678250579
DISCRIMINATOR=invalid_gate_a_enum
RUNTIME_OBSERVATION_STARTED=false

RUN=32126665668 JOB=95678628873
DISCRIMINATOR=GDB_UNAVAILABLE
GATE_B=PASS
PROCESS_IDENTITY=PASS
NATIVE_MODEL_MEMORY_READ_STARTED=false
```

The first was repaired by using the canonical governance enum `gate_a: PASS`. The second proved the Synology runner did not provide `gdb`; it was repaired without installing tooling or changing the client by replacing the debugger dependency with a bounded read-only `/proc/<pid>/mem` reader. The structural hypothesis, vptr discriminator and output restrictions were unchanged.

## Successful discriminator

```text
HEAD=683c6cb2909b60240e22b2ed344077928e14aaae
RUN=32126937957
JOB=95679477308
RUNNER=synology-otclient-01
RESULT=SUCCESS
```

Admission and current-generation fencing:

```text
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
NATIVE_LOGIN_RETAINED_ADMISSION_POLICY=PASS
TRACK_A_CANONICAL_LEASE_RENEW=true
TRACK_A_CANONICAL_LEASE_GENERATION=10
TRACK_A_CANONICAL_LEASE_EXPIRES_AT_EPOCH=1787051643
NATIVE_LOGIN_RETAINED_CONTROLLER_STATE=ACTIVE_GEN10_REG2_10
NATIVE_LOGIN_RETAINED_XRES_WORKER=PASS
TRACK_A_CANONICAL_GATE_B=PASS
TRACK_A_CANONICAL_LEASE_GENERATION=10
NATIVE_LOGIN_RETAINED_PROCESS_IDENTITY=PASS
```

The read-only scanner independently derived the current PIE load bias, found exactly one primary `TCharacterSelectionController` vptr using the previously static/historical address fence `0x308ed68`, and emitted only structural counts:

```text
NATIVE_LOGIN_RETAINED_LOAD_BIAS_PROVEN=true
NATIVE_LOGIN_RETAINED_CHARSEL_INSTANCE_COUNT=1
NATIVE_LOGIN_RETAINED_CHARSEL_VPTR_PROVEN=true
NATIVE_LOGIN_RETAINED_NATIVE_CHARACTER_LIST_COUNT=0
NATIVE_LOGIN_RETAINED_NATIVE_SELECTED_LOGIN_DATA_COUNT=0
NATIVE_LOGIN_RETAINED_SESSION=NOT_PROVEN_AVAILABLE
NATIVE_LOGIN_RETAINED_DISCRIMINATOR=PASS:CURRENT_NATIVE_CHARACTER_MODEL_EMPTY
```

No character names, worlds, account identifiers, tokens, strings, raw buffers or screenshots were read or emitted.

After the discriminator, the same lease was still valid at generation 10:

```text
TRACK_A_CANONICAL_LEASE_VALIDATE=true
TRACK_A_CANONICAL_LEASE_GENERATION=10
```

Negative boundary:

```text
NATIVE_LOGIN_RETAINED_METHOD_INVOCATION=false
NATIVE_LOGIN_RETAINED_MEMORY_WRITE=false
NATIVE_LOGIN_RETAINED_SECRET_VALUE_READ=false
NATIVE_LOGIN_RETAINED_GUI_INTERACTION=false
NATIVE_LOGIN_RETAINED_LOGIN_PERFORMED=false
NATIVE_LOGIN_RETAINED_GAMEPLAY_PERFORMED=false
```

## Classification

```text
FACT: current exact official-client runtime remained admitted and Gate-B-valid on active generation 10.
FACT: exactly one current TCharacterSelectionController object existed.
FACT: its native character list and selected login-data vector were both structurally empty.
FACT: no reusable current native character-selection model was therefore available in this freshly bootstrapped process.
FACT: no native shortcut/method was invoked and no credentials were requested.
INFERENCE: the programme cannot legitimately skip initial authentication on the basis of the current in-memory native model.
NEXT_LEGAL_STEP: classify cold-auth requirements and test only the availability of the already-promoted protected local secret-ingress boundary before requesting any secret or mutating the client.
```

This does not prove the absence of every possible persisted session store on disk; it proves that the running client does not currently expose the native character model required for the no-credential direct-to-character-selection path.

## One-shot cleanup

The retained-session workflow was deleted after the successful run:

```text
WORKFLOW_REMOVAL_COMMIT=7c1dd9a50de9c53402a1787516201860f6137a0f
```
