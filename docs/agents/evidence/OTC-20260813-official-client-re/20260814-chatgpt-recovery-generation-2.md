# Track A recovery checkpoint — generation 2

Timestamp: 2026-08-14T17:34:00+02:00
Last operation update: 2026-08-14T18:02:00+02:00

## Scope

Official native Linux Tibia client reverse engineering only (`official-client-re` / `OTCLIENT-TIBIA-RE`). Track B runtime/state remains out of scope.

## Branch ownership recovery

Source PR #289 branch `ci/OTC-20260813-official-client-re-continuation` moved concurrently to `8ac9c72ee16427a8d79526184cb525f6a2114e8e` with a separate Track A workflow and queued run `31816876078`. A non-force update was rejected as non-fast-forward.

No force push was used. This invocation continues on isolated branch:

```text
ci/OTC-20260814-official-client-re-receiver-recovery
```

forked from source head `8ac9c72ee16427a8d79526184cb525f6a2114e8e`.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## P2 correction completed

- workflow: `Track A outgoing payload consumer provenance`
- head: `c15899ebef7cadb7ce6f4a302a28dff064f6b537`
- run: `31815819731`
- job: `94817115581`
- result: `SUCCESS`
- artifact: `9225203231`
- digest: `sha256:e0ca5a278d7235e1755105775ed235a4f5ee501db2e5cb473b6d008e8f9831a3`

The run contradicts the inherited `0x8409d0` simple-thunk / `0xb5b880` downstream-target interpretation. Exact `0x8409d0` is a non-trivial routine using `[owner+0x118]`; `0xb5b880` is not shown as an instruction boundary under the captured stream. No `OutGoingMessagePayload`/`OutgoingMessagePayload` literal was reproduced.

The proven outbound boundary is rolled back to:

```text
TProtocolMessageQueue::clientMessageReadyToProcess
  -> QObject::connectImpl @ 0x7e7470
  -> containing-owner receiver
  -> pointer-to-member encoding 0x91
  -> receiver virtual slot offset +0x90
```

Concrete owner vptr, concrete `+0x90` function, serializer, framing and final write are `UNKNOWN` pending re-derivation.

## Active operation

```yaml
recovery_generation: 2
recovery_attempts: 2
continuation_mode: bounded_slice
observed_state: active_external_operation
safe_to_resume: true
active_operation:
  id: queue-receiver-exact-target
  workflow: Track A queue receiver exact target
  workflow_path: .github/workflows/tibia-official-client-re-queue-receiver-exact-target.yml
  branch: ci/OTC-20260814-official-client-re-receiver-recovery
  head: 7be0c193d2b20cbb2c82b53884ecd2f5c439f344
  run_id: 31817347325
  first_observed_status: queued
  operation_started_at: 2026-08-14T18:01:26+02:00
  wait_deadline_at: 2026-08-14T18:46:26+02:00
resume_condition: >-
  run 31817347325 reaches terminal state or the persisted wait deadline expires;
  do not redispatch this semantic operation while the recorded run is active
next_action: >-
  artifact-first classify exact table reads/setup candidates/aligned disassembly;
  re-prove concrete receiver target before continuing serializer/framing recovery
```

Detailed P2 correction: `20260814-outgoing-payload-consumer-provenance.md`.
