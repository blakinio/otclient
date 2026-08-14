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
recovery_generation: 3
recovery_attempts: 3
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

Historical experiment details remain canonical under `docs/agents/evidence/OTC-20260813-official-client-re/`; disproven hypotheses must not remain as current acceptance facts.

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

Every binary experiment that promotes a client-specific conclusion must re-check this fence.

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
- [x] Correct `clientMessageReadyToProcess` Qt handoff recovered: heap `QSlotObject`, invoker `0x7dd630`, owner saved at slot-object `+0x10`.
- [x] Neighbor transport cluster `0x7dd3f0` structurally linked to the same owner state and to a real `QIODevice::write` callsite `0x7dd563`.
- [x] `tibia::network::TUnencryptedRawMessageStream` uniquely recovered at vtable address point `0x3084c58`, RTTI `0x3080660`, deriving from `QBuffer`; local virtual `+0xe8 = 0xb40630` reaches `QIODevice::write` at `0xb4066b`.
- [ ] Concrete owner stream-pair mapping for `+0x9f0/+0xa00/+0xa10/+0xc18` proven.
- [ ] Exact ordering of raw stream, framing, encryption/compression and final `QTcpSocket` proven.
- [ ] Exact serializer semantics and final gameplay network-write site proven.
- [ ] Bridge `session-status` correlated with decoded structural world state using the official bundled Qt 6.9 runtime.
- [ ] Direct standalone player-position member proven; viewport-center position remains `DERIVED` only.
- [ ] P0 live reads proven for HP/maxHP, mana/maxMana, identity/state, CreatureStorage/lifecycle, battle target, inventory/equipment, containers, structured chat/world events.
- [ ] One safest reversible semantic action promoted through server-confirmed A3 and bridge/reference A4 parity.
- [ ] Generated-message and Tibia-owned QMeta/runtime classification registries reconciled to quantitative coverage target or documented terminal blockers.
- [ ] Fresh final audit, exact-head CI, PR hygiene, acceptance reconciliation and archive/merge gate completed.

## Corrected outbound convergence

```text
semantic action
  -> TInternalGameActionRouter
  -> TProtocolMessageQueue builder
  -> clientMessageReadyToProcess
  -> Qt QSlotObject connection @ 0x19716a3
  -> QSlotObject invoker 0x7dd630
  -> containing owner stream family (+0xc18 / +0xa00 / +0xa10)

neighboring transport path:
  owner stream family (+0xa10 / +0x9f0)
  -> function 0x7dd3f0
  -> devirtualized stream method check +0xe8 == 0xb40630
  -> tibia::network::TUnencryptedRawMessageStream
  -> QIODevice::write callsites 0x7dd563 and 0xb4066b in the recovered stream cluster
```

Exact queue convergence retained from earlier evidence:

```yaml
TProtocolMessageQueue_sendMessage_entry: '0xdf7930'
TProtocolMessageQueue_sendMessage_body: '0xde6de0'
prepareAndEnqueueGameclientMessage_entry: '0xdf6b99'
prepareAndEnqueueGameclientMessage_body: '0xbc6e20'
queue_helpers: ['0xde91b0', '0xbc6f00', '0xbc6750']
clientMessageReadyToProcess_connection: '0x19716a3'
qslot_invoker: '0x7dd630'
transport_cluster: '0x7dd3f0'
raw_stream_class: tibia::network::TUnencryptedRawMessageStream
raw_stream_vtable: '0x3084c58'
raw_stream_rtti: '0x3080660'
raw_stream_base: QBuffer
raw_stream_plus_e8: '0xb40630'
raw_stream_qiodevice_write: '0xb4066b'
```

Do **not** call `0x7dd563`, `0xb40630`, or `0xb4066b` the final gameplay socket write until downstream/layer ordering and the `QTcpSocket` object are proven. Do **not** call internal builder discriminators final wire opcodes until framing is proven.

## Superseded / disproven outbound model

The previous convergence below is **not current truth** and must not be reused:

```text
clientMessageReadyToProcess
  -> containing owner virtual +0x90 = 0x8409d0
  -> owner+0x88 subobject
  -> subobject +0xb8 = 0xb5b880
```

Exact-build correction:

- the connection uses a heap `QSlotObject` with invoker `0x7dd630`; the previously parsed PMF `0x91` belonged to the preceding connection;
- `0x2f66288 + 0xb8` resolves to `0x313cce0`, non-executable;
- `0xb5b880` lies inside an instruction beginning at `0xb5b87c`;
- the workflow that promoted `0xb5b880` had hardcoded that value rather than recovering it from ELF.

Classification: **DISPROVEN / SUPERSEDED**.

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

## Current recovery checkpoint — generation 3

```yaml
recovery_generation: 3
continuation_mode: autonomous_program
observed_state: active_external_operation
safe_to_resume: true
isolated_recovery_branch: ci/OTC-20260814-track-a-chatgpt-framing-recovery
latest_proven_evidence_commit: 7a3d2bcac9a32ab5c07043b4b43e4146e674aeaf
machine_state_correction_commit: 103969b467869f66cba07ae52a468d12943130d7
active_operation:
  type: static_exact_sha_experiment
  id: stream-owner-pair-mapping
  workflow: Track A stream owner pair mapping
  workflow_path: .github/workflows/tibia-official-client-re-stream-owner-pairs.yml
  experiment_head: 0a3c4fdb824c943e34b2c318ef41f41db733d132
  run_id: 31824297168
  first_observed_status: queued
```

This experiment is mapping the concrete classes/control blocks behind owner shared-pointer pairs `+0x9f0/+0x9f8`, `+0xa00/+0xa08`, `+0xa10/+0xa18`, `+0xc18/+0xc20` and ordering them against `TUnencryptedRawMessageStream`.

## Current unknowns

- concrete owner stream-pair class mapping for `+0x9f0/+0xa00/+0xa10/+0xc18`;
- exact layer ordering of `TUnencryptedRawMessageStream`, framing, encryption/compression and final socket;
- exact serializer semantics and final gameplay network write;
- final wire relationship of internal `GameclientMessage` discriminators;
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

1. Finish run `31824297168`; persist exact owner stream-pair mappings and class RTTI evidence.
2. Continue static P2 edge-by-edge until raw stream -> framing/encryption/compression -> `QTcpSocket` ordering and final write are proven or an evidence-backed blocker is reached.
3. Repair bridge Qt separation and correlate live read-only bridge `session-status` with structural world state.
4. Recover P0 reads with causal/restart-stable evidence.
5. Promote safest reversible movement through A3/A4 parity; avoid costly/irreversible effects.
6. Complete protocol/QMeta registries and quantitative coverage.
7. Repair remaining CI quality gates, perform fresh audit, exact-head CI, reviews/threads/PR hygiene, then merge/archive only when all policy gates permit.

## Durable evidence

- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-chatgpt-network-handoff-correction.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-queue-qslot-consumer-success.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-derived-transport-field-provenance.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-unencrypted-raw-message-stream-proven.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-continuation-state.yaml`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-action-builders.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-live-structural-world-and-reversible-movement.md`

## Next action

Inspect `31824297168` after a state change. If terminal, persist its artifact-derived owner-pair/class mapping and immediately continue to the next unresolved stream/framing/socket edge. Do not launch the live client while this static P2 operation is active.
