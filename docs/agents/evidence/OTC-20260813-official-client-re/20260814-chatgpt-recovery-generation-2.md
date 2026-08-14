# Track A recovery checkpoint — generation 2

Timestamp: 2026-08-14T17:34:00+02:00

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
observed_state: active_takeover
safe_to_resume: true
active_operation:
  type: static_exact_sha_experiment
  id: outgoing-payload-consumer-provenance
  run_id: null
  job_id: null
  workflow_name: tibia-official-client-re-outgoing-payload-consumers
  source_head_sha: 60323a1e5ea252f22ee0fcc47a14ae62c9575792
  operation_started_at: 2026-08-14T17:34:00+02:00
  terminal_status: preparing
check_generation:
  branch_head_checks_used: 1
  commit_log_checks_used: 1
  actions_runs_checks_used: 1
resume_condition: >-
  no newer conflicting Track A writer and no active overlapping Track A run
next_action: >-
  add an exact-client-SHA-gated static workflow that starts at 0xb5b880 and
  reconstructs bounded direct-call, protobuf/string, Qt write and socket-write
  provenance; persist the resulting run/job/artifact before any live-client effect
```

## Confidence boundary

No new `OutGoingMessagePayload` claim is promoted by this checkpoint. Any such type/envelope relationship must be independently reproduced by the new exact-SHA experiment or remain `UNKNOWN`.
