# 2026-08-28 — V3 field6 live checkpoint

Classification: **FACT / in-progress checkpoint / no retry**.

## Trusted repository state

```text
fresh main                         32146659213cba71910cbe8d46aa4c2f6ded607c
merged exact-current package fix  #764 -> 658715b3709b0290cdbb43fe44fce03ce5ef7060
merged direct package-source fix  #769 -> eb316cd4ce4b9926ade8b170babe2b3d7053b531
merged V3 live admission          #771 -> 32146659213cba71910cbe8d46aa4c2f6ded607c
V3 owner admission comment        5456573590
V3 exact trigger comment          5456601015
V3 workflow run                   33202129157
V3 live job                       98953921602
workflow                          Track A current login field6 runtime observation
workflow id                       344784595
```

## State at checkpoint

The V3 job is running on exact trusted `main@32146659213cba71910cbe8d46aa4c2f6ded607c`.

Observed step state at this checkpoint:

```text
Checkout exact trusted main                         SUCCESS
Prove trusted-main live admission and boundaries    SUCCESS
Materialize exact current package through WARP      IN_PROGRESS
Consume exact owner authorization once              PENDING
Capture field6 with protected login inputs          PENDING
Validate scalar-only evidence                       PENDING
Upload sanitized field6 evidence                    PENDING
Clean exact current package preflight state          PENDING
```

Therefore, at the time this checkpoint was written:

```text
physical_action_count=0
login_submit_count=0
owner_trigger_consumed=false
credentials_exposed_to_wrapper=false
official_client_started=false
FIELD6_VALUE=UNKNOWN
FIELD6_VALUE_PROVEN=false
```

No second V3 trigger is permitted. Do not rerun or replay comment `5456601015`.

## Exact evidence boundary

The only admissible official client remains:

```text
version=15.32.75d4a0
unpacked_size=52105824
unpacked_sha256=d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
packed_bin_client_sha256=075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
producer_entry=PIE+0xe25620
observed_scalar=uint32(edx)
```

Static promoted evidence already proves that this producer input is copied into outer protobuf field 6 at write site `0xe25ccc`. Track B PR #284 currently omits outer field 6 entirely. No Track B mutation is authorized until a sanitized runtime artifact proves the exact scalar value.

## Next action

1. Inspect only run `33202129157` until it reaches a terminal state; do not create another live trigger.
2. If package materialization fails before authorization consumption, classify the new pre-action failure and keep `physical_action_count=0`.
3. If materialization passes, the workflow may consume the V3 trigger and perform its one admitted account-login submission. No character selection, world entry, gameplay or packet capture is allowed.
4. Accept a value only if the terminal evidence proves `FIELD6_VALUE_PROVEN=true` with the exact client fence above.
5. Independently promote the scalar to trusted `main` before Track B #284 adds outer field 6 or spends another official-service game E2E.
6. After promotion, restack Track B #284 cleanly on fresh `main`, use TDD for field 6, run contracts/build, then perform only the newly justified bounded game E2E toward `GAME_START` / `IN_GAME`.

This checkpoint intentionally does not modify or merge into trusted `main` while the V3 live run is still executing.