# Track A recovery checkpoint — generation 2

Timestamp: 2026-08-14T17:34:00+02:00
Last operation update: 2026-08-14T17:42:34+02:00

## Scope

Official native Linux Tibia client reverse engineering only (`official-client-re` / `OTCLIENT-TIBIA-RE`). Track B runtime/state remains out of scope.

## Revalidated repository state

- PR: `#289`, open draft.
- Branch: `ci/OTC-20260813-official-client-re-continuation`.
- Takeover source head: `60323a1e5ea252f22ee0fcc47a14ae62c9575792`.
- Source-head commit: `test(track-a): resolve derived network owner vtable`.
- Source-head Track A run: `31812572191`, job `94806473825`, `SUCCESS` on runner `synology-otclient-01`.
- Recent branch-run inspection at takeover found no queued or in-progress Track A run.
- Source-head generic CI run `31812575746` is `FAILURE`; this is not treated as a failure of the successful exact-head Track A research job and must be diagnosed separately before closeout.
- Recovery checkpoint commit: `2f4591f32f3f9fdbdb313757f9b6eb9114b36cba`.
- New static experiment head: `c15899ebef7cadb7ce6f4a302a28dff064f6b537`.
- New static experiment run: `31815819731`, initially observed `queued`.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Proven outbound-network convergence carried into this recovery

The current durable chain is:

```text
TProtocolMessageQueue semantic builder
  -> clientMessageReadyToProcess
  -> containing network owner
  -> primary owner vtable address point 0x308c408
  -> primary slot +0x90 = 0x8409d0
  -> subobject at owner +0x88
  -> subobject vtable address point 0x2f66288
  -> subobject slot +0xb8 = 0xb5b880
```

`0x8409d0` is a delegating thunk, not by itself the serializer. `0xb5b880` is the next concrete downstream target. Final serializer/framing/socket-write semantics remain `UNKNOWN` until directly proven.

## Recovery state

```yaml
recovery_generation: 2
recovery_attempts: 2
continuation_mode: bounded_slice
observed_state: active_external_operation
safe_to_resume: true
active_operation:
  type: static_exact_sha_experiment
  id: outgoing-payload-consumer-provenance
  run_id: 31815819731
  job_id: null
  workflow_name: Track A outgoing payload consumer provenance
  head_sha: c15899ebef7cadb7ce6f4a302a28dff064f6b537
  operation_started_at: 2026-08-14T17:42:34+02:00
  terminal_status: queued
  wait_deadline_at: 2026-08-14T18:27:34+02:00
check_generation:
  branch_head_checks_used: 1
  commit_log_checks_used: 1
  actions_runs_checks_used: 2
resume_condition: >-
  run 31815819731 reaches a terminal state or the persisted wait deadline expires;
  do not redispatch the same semantic operation while the recorded run is active
next_action: >-
  inspect run 31815819731 exactly once after a state change; if terminal, download
  its provenance artifact, classify the path from 0xb5b880 toward final framing/write,
  persist the result, and choose the next unresolved edge without live-client effect
```

## Confidence boundary

No new `OutGoingMessagePayload` claim is promoted by this checkpoint. Any such type/envelope relationship must be independently reproduced by the exact-SHA experiment or remain `UNKNOWN`.
