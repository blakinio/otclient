---
task_id: OTC-20260813-official-client-re-continuation
status: active
track_id: official-client-re
alias: OTCLIENT-TIBIA-RE
owner: chatgpt
branch: ci/OTC-20260813-official-client-re-continuation
base_branch: main
pr: 289
task_kind: runtime-research
phase: static-outbound-framing-convergence
risk: medium
runtime_platform: native_linux_only
safe_to_resume: true
recovery_generation: 2
recovery_attempts: 2
ai_owner_billing_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - .github/scripts/tibia-official-client-re-*
  - tests/tools/test_tibia_official_client_re_*.py
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
---

# OTC-20260813 — Official Linux client RE continuation

## Objective

Continue Track A against the **official native Linux Tibia client only**. Recover and validate structural world/player/creature/inventory/protocol/action state without OCR assumptions, preserve runtime isolation from Track B, and promote only exact-version evidence with explicit confidence boundaries.

This task is intentionally kept compact. Historical experiment details remain canonical in `docs/agents/evidence/OTC-20260813-official-client-re/` and are not duplicated here.

## Hard scope and safety

```yaml
repository: blakinio/otclient
runner: synology-otclient-01
subject: official native Linux Tibia client only
state_directory: /home/runner/_work/_otclient_tibia_re_state
legacy_compatibility_state_directory: /work/_otclient_tibia_re_state
display: ':98'
warp_socks_port: 25354
process_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
default_live_effect: READ_ONLY_OR_REVERSIBLE_NO_COST
track_b_runtime: OUT_OF_SCOPE
owner_funded_ai: FORBIDDEN_WITHOUT_EXPLICIT_CURRENT_PERMISSION
```

Do not read, stop, attach to, reconfigure or clean Track B runtime/process/display/ports/state. Do not spend Tibia Coins or gold and do not perform irreversible Market/Forge/trade effects.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: native_linux_only
```

Every binary experiment that can promote a client-specific conclusion must re-check this fence.

## Acceptance inventory

- [x] Track A namespace/runtime isolation proven on the dedicated runner.
- [x] Exact official Linux client version/size/SHA fenced.
- [x] Official client reconstruction and owned launch proven historically for this exact build.
- [x] Protocol surface census persisted: 47 handler classes, 146 handle-message names, 189 inbound and 160 outbound named messages.
- [x] Embedded protobuf `Coordinate` recovered as x=1/y=2/z=3, all `uint32`.
- [x] Qt direct call census persisted: 2078 `connectImpl`, 41 legacy connect, 65 `disconnectImpl`; legacy subset 40 classified + 1 explicit unclassified.
- [x] `TInternalGameActionRouter @ 0x8332d0` proven router/re-emitter and disproven as serializer.
- [x] Outbound builders recovered for movement, `MoveObject`, `Talk`, `Attack`, `Follow`, `TradeObject`.
- [x] Structural live-world map state and one forward/inverse reversible movement transition proven for the exact build.
- [x] Primary network-owner vtable and delegation edge recovered through concrete contained-subobject target `0xb5b880`.
- [ ] Exact serializer semantics downstream of `0xb5b880` proven.
- [ ] Exact framing and final `QIODevice`/`QTcpSocket` network-write site proven.
- [ ] Bridge `session-status` correlated with decoded structural world state using the official bundled Qt 6.9 runtime.
- [ ] Direct standalone player-position member proven; viewport-center position remains `DERIVED` only.
- [ ] P0 live reads proven for HP/maxHP, mana/maxMana, identity/state, CreatureStorage/lifecycle, battle target, inventory/equipment, containers, structured chat/world events.
- [ ] One safest reversible semantic action promoted through server-confirmed A3 and bridge/reference A4 parity.
- [ ] Generated-message and Tibia-owned QMeta/runtime classification registries reconciled to quantitative coverage target or documented terminal blockers.
- [ ] Fresh final audit, exact-head CI, PR hygiene, acceptance reconciliation and archive/merge gate completed.

## Proven outbound convergence

```text
semantic action
  -> TInternalGameActionRouter
  -> TProtocolMessageQueue builder
  -> clientMessageReadyToProcess
  -> containing network owner
  -> primary owner vtable address point 0x308c408
  -> primary slot +0x90 = 0x8409d0
  -> contained subobject at owner +0x88
  -> contained subobject vtable address point 0x2f66288
  -> contained subobject slot +0xb8 = 0xb5b880
```

Exact queue convergence retained from earlier evidence:

```yaml
TProtocolMessageQueue_sendMessage_entry: '0xdf7930'
TProtocolMessageQueue_sendMessage_body: '0xde6de0'
prepareAndEnqueueGameclientMessage_entry: '0xdf6b99'
prepareAndEnqueueGameclientMessage_body: '0xbc6e20'
queue_helpers: ['0xde91b0', '0xbc6f00', '0xbc6750']
primary_owner_vtable: '0x308c408'
primary_slot_0x90: '0x8409d0'
primary_slot_classification: delegating_thunk
contained_subobject_offset: '+0x88'
contained_subobject_vtable: '0x2f66288'
contained_subobject_slot_0xb8: '0xb5b880'
source_run: 31812572191
source_job: 94806473825
source_result: SUCCESS
```

Do **not** name `0x8409d0` or `0xb5b880` as the final serializer/write routine until their downstream semantics are proven. Do **not** call internal builder discriminators final wire opcodes until framing is proven.

## Structural live-world state

```yaml
reversible_path:
  - [32546, 32510, 7]
  - [32546, 32509, 7]
  - [32546, 32510, 7]
current_floor_aware_range: [18, 14]
map_callback_has_xyz_and_stack_order: true
player_coordinate:
  classification: DERIVED
  derivation: fixed viewport center from authoritative decoded map strips
  direct_member: UNKNOWN
```

The single adjacent ground-item drag experiment delivered its stimulus but did not produce server-confirmed `MoveObject`; it remains below A3.

## Bridge state

The bridge source builds. Historical run `31809994339` failed live correlation because the workflow exposed extracted Ubuntu Qt 6.4 in the official client runtime `LD_LIBRARY_PATH`, shadowing the client's required bundled Qt 6.9.

Deterministic recovery rule:

- extracted toolroot/sysroot libraries are compile/tool-only;
- official client runtime must use bundled Qt 6.9;
- after semantic world entry, query bridge `session-status` and correlate it with already decoded structural map/world state.

## Current recovery checkpoint — generation 2

```yaml
recovery_generation: 2
recovery_attempts: 2
continuation_mode: bounded_slice
observed_state: active_external_operation
safe_to_resume: true
takeover_source_head: 60323a1e5ea252f22ee0fcc47a14ae62c9575792
checkpoint_commit: 2f4591f32f3f9fdbdb313757f9b6eb9114b36cba
machine_state_commit: 09fa30c86b791062724aca0d251ed84e552d90e7
active_operation:
  type: static_exact_sha_experiment
  id: outgoing-payload-consumer-provenance
  workflow: Track A outgoing payload consumer provenance
  workflow_path: .github/workflows/tibia-official-client-re-outgoing-payload-consumers.yml
  experiment_head: c15899ebef7cadb7ce6f4a302a28dff064f6b537
  run_id: 31815819731
  job_id: null
  first_observed_status: queued
  operation_started_at: 2026-08-14T17:42:34+02:00
  wait_deadline_at: 2026-08-14T18:27:34+02:00
resume_condition: >-
  run 31815819731 reaches terminal state or the persisted wait deadline expires;
  do not redispatch the same semantic operation while it is active
```

The experiment starts from `0xb5b880`, independently searches bounded direct-call provenance, protobuf/envelope literals and Qt/network-write symbols, and uploads a durable report artifact. A previously mentioned `OutGoingMessagePayload` relationship is **not promoted** until this or later exact-SHA evidence independently reproduces it.

## CI state requiring closeout repair

For source head `60323a1e5ea252f22ee0fcc47a14ae62c9575792`:

```yaml
track_a_run: 31812572191
track_a_job: 94806473825
track_a_result: SUCCESS
generic_ci_run: 31812575746
generic_ci_result: FAILURE
first_failed_ci_job: 94807088316
first_failed_ci_step: Run yamllint
```

This is a repository quality-gate failure, not a contradiction of the successful Track A binary experiment. It must be repaired and revalidated before closeout.

## Current unknowns

- exact serializer semantics downstream of `0xb5b880`;
- exact framing and final network write;
- relationship between internal GameclientMessage discriminators and final wire bytes;
- independently reproduced outbound envelope/protobuf wrapper semantics;
- bridge session-status/live structural-world correlation;
- direct player-position member;
- HP/maxHP and mana/maxMana;
- player identity/state;
- CreatureStorage and creature lifecycle;
- battle target;
- inventory/equipment and containers;
- structured chat and server/world events;
- server-confirmed semantic `MoveObject`;
- complete quantitative protocol/QMeta/P0 coverage.

## Ordered continuation

1. Finish run `31815819731`; persist its artifact-derived framing/write provenance.
2. Continue static P2 edge-by-edge until serializer/framing/final-write is proven or a concrete evidence-backed blocker is reached.
3. Repair bridge Qt separation and correlate live read-only bridge `session-status` with structural world state.
4. Recover P0 reads with causal/restart-stable evidence.
5. Promote safest reversible movement through A3/A4 parity; avoid costly/irreversible effects.
6. Complete protocol/QMeta registries and quantitative coverage.
7. Repair workflow `yamllint`, perform fresh audit, exact-head CI, reviews/threads/PR hygiene, then merge/archive only when all policy gates permit.

## Durable evidence

- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-chatgpt-recovery-generation-2.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-continuation-state.yaml`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-network-owner-vtable-census.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-network-handoff.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-action-builders.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-live-structural-world-and-reversible-movement.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-qt-connect-callsite-census.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-gameaction-connectimpl-arguments.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-gameaction-slot-provenance.md`

## Next action

Inspect `31815819731` after a state change. If terminal, download its report artifact, classify the concrete path from `0xb5b880`, persist the result, and immediately select the next unresolved downstream edge. Do not launch the live client while this static P2 operation is still active.
