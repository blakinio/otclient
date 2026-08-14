---
task_id: OTC-20260813-official-client-re-continuation
status: active
track_id: official-client-re
alias: OTCLIENT-TIBIA-RE
owner: chatgpt-recovery
branch: ci/OTC-20260813-official-client-re-continuation
recovery_branch: ci/OTC-20260814-track-a-chatgpt-framing-recovery
base_branch: main
pr: 289
task_kind: runtime-research
phase: static-outbound-framing-convergence
risk: medium
runtime_platform: native_linux_only
safe_to_resume: true
recovery_generation: 4
recovery_attempts: 4
ai_owner_billing_authorized: false
---

# OTC-20260813 — Official Linux client RE continuation

## Objective

Continue Track A against the **official native Linux Tibia client only** until the programme reaches a real completion or an evidence-backed blocker. Recover and validate protocol/framing/final-write, structural live state, direct P0 reads and reversible actions without OCR assumptions. Persist every material result under the Track A evidence root.

## Hard scope and safety

```yaml
repository: blakinio/otclient
runner: synology-otclient-01
subject: official native Linux Tibia client only
state_directory: /home/runner/_work/_otclient_tibia_re_state
legacy_state_directory: /work/_otclient_tibia_re_state
display: ':98'
warp_socks_port: 25354
process_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
default_live_effect: READ_ONLY_OR_REVERSIBLE_NO_COST
track_b_runtime: OUT_OF_SCOPE
owner_funded_ai: FORBIDDEN_WITHOUT_EXPLICIT_CURRENT_PERMISSION
```

Never read, stop, attach to, reconfigure or clean Track B runtime/process/display/ports/state. Do not spend Tibia Coins/gold or perform irreversible Market/Forge/trade effects.

## Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: native_linux_only
```

Every binary conclusion must be fenced to this exact build.

## Branch/reconciliation state

As of 2026-08-14 evening Europe/Warsaw:

```yaml
primary_pr: 289
primary_branch: ci/OTC-20260813-official-client-re-continuation
primary_head_observed: 4ac4a7546b182fcc11aaac3893c2a0116304f3e2
recovery_branch: ci/OTC-20260814-track-a-chatgpt-framing-recovery
recovery_head_before_generation_4: 7e9db4a04aa914ea209f68eeaf39181120e230ba
active_recovery_run: 31825417040
active_recovery_job: 94848268697
active_recovery_status_observed: queued
```

The primary branch has an independent active writer/history. Do **not** overwrite it blindly. Reconcile primary evidence with recovery evidence first. If ownership is unclear, continue on a new isolated branch.

## Correct outbound model — current truth

```text
semantic action
  -> TInternalGameActionRouter
  -> TProtocolMessageQueue builder
  -> clientMessageReadyToProcess
  -> Qt connection @ 0x19716a3
  -> heap QSlotObject invoker 0x7dd630
  -> TProtocolClientMessageProcessor (owner +0xa00/+0xa08)
       virtual +0x10 -> 0xc2df80
  -> TGameserverNetworkPacketRawDataProcessor (owner +0xa10/+0xa18)
       virtual +0x10 -> 0xb47130
  -> TGameserverDualConnection (owner +0xc18/+0xc20)
       virtual +0x80 -> 0xb56d60
       virtual +0x78 -> 0xb56970
```

Related owner field:

```yaml
'+0x9f0/+0x9f8': tibia::protocol::TProtocolServerPacketProcessor
'+0xa00/+0xa08': tibia::protocol::TProtocolClientMessageProcessor
'+0xa10/+0xa18': tibia::network::TGameserverNetworkPacketRawDataProcessor
'+0xc18/+0xc20': tibia::network::TGameserverDualConnection
```

Exact queue convergence:

```yaml
sendMessage_entry: '0xdf7930'
sendMessage_body: '0xde6de0'
prepareAndEnqueueGameclientMessage_entry: '0xdf6b99'
prepareAndEnqueueGameclientMessage_body: '0xbc6e20'
queue_helpers: ['0xde91b0', '0xbc6f00', '0xbc6750']
```

## Raw stream / QIODevice facts

`TUnencryptedRawMessageStream` is structurally proven:

```yaml
class: tibia::network::TUnencryptedRawMessageStream
vtable_address_point: '0x3084c58'
rtti: '0x3080660'
base: QBuffer
local_virtual_plus_e8: '0xb40630'
qiodevice_write_inside_plus_e8: '0xb4066b'
```

Direct `QIODevice::write(QByteArray const&)` callsite census for the exact executable:

```yaml
count: 5
callsites: ['0x7dd563', '0xb4066b', '0xb46c75', '0xc4a848', '0xd08642']
file_io_excluded: ['0xc4a848', '0xd08642']
server_read_side: '0x7dd563'
raw_qbuffer_internal: '0xb4066b'
high_priority_unresolved: '0xb46c75'
```

Fresh primary-branch evidence commit `4ac4a7546b182fcc11aaac3893c2a0116304f3e2` upgrades `0xb46bd0/0xb46c75` back to a **high-priority gameserver TCP candidate**. Run `31827951737` proves a QObject-derived QMetaObject at `0x30b7d00`, static metacall `0xdd1cc0`, gameserver/TCP/QAbstractSocket vocabulary in its bounded stringdata region, and a QIODevice pointer at `[this+0x10]` used by `QIODevice::write` at `0xb46c75`.

This does **not** yet prove that the newline-terminated payload is the Tibia gameplay frame. The concrete `[this+0x10]` type and binary gameplay-frame write remain UNKNOWN.

## Critical disproven model — never resurrect

The following chain is **DISPROVEN / SUPERSEDED**:

```text
clientMessageReadyToProcess
  -> owner virtual +0x90 = 0x8409d0
  -> owner+0x88
  -> vtable 0x2f66288 +0xb8
  -> 0xb5b880
```

Exact correction:

- the real connection uses QSlotObject invoker `0x7dd630`;
- PMF value `0x91` belonged to the preceding Qt connection;
- `0x2f66288 + 0xb8 = 0x313cce0`, non-executable;
- `0xb5b880` lies inside an instruction beginning at `0xb5b87c`;
- the workflow that promoted `0xb5b880` hardcoded the value instead of recovering it.

If any newer document calls `0xb5b880` a canonical outbound target, classify that sentence as stale/conflicting until independently re-proven. Do not use it as a root.

## Acceptance inventory

- [x] Track A runtime namespace isolation.
- [x] Exact official client build fence.
- [x] Official-client reconstruction/launch proven historically.
- [x] Protocol census: 47 handler classes, 146 handle-message names, 189 inbound and 160 outbound names.
- [x] Qt direct-call census: 2078 connectImpl, 41 legacy connect, 65 disconnectImpl; legacy 40 classified + 1 explicit unknown.
- [x] Action router proven; not serializer.
- [x] Builders recovered for movement, MoveObject, Talk, Attack, Follow, TradeObject.
- [x] Live structural world/map state and reversible movement proven.
- [x] Correct QSlotObject handoff `0x7dd630` proven.
- [x] Owner stream-pair classes `+0x9f0/+0xa00/+0xa10/+0xc18` proven.
- [x] Outbound virtual targets `0xc2df80`, `0xb47130`, `0xb56d60`, `0xb56970` proven.
- [x] `TUnencryptedRawMessageStream` / QBuffer identity proven.
- [ ] `TIODeviceWriter` and `TGameserverTCPConnection` concrete vtables/member relations proven.
- [ ] Final gameplay framing/encryption/compression ordering proven.
- [ ] Concrete final `QTcpSocket`/QAbstractSocket gameplay write proven.
- [ ] Bridge `session-status` correlated with world state using bundled Qt 6.9.
- [ ] Direct player-position member proven.
- [ ] P0 reads: HP/maxHP, mana/maxMana, identity/state, CreatureStorage/lifecycle, target, inventory/equipment, containers, chat/world events.
- [ ] Safest reversible semantic action promoted to server-confirmed A3 and bridge/reference A4 parity.
- [ ] Quantitative protocol/QMeta/runtime coverage reconciled.
- [ ] Final audit, exact-head CI, PR hygiene, acceptance reconciliation, archive/merge gate.

## Bridge state

Bridge source builds. Historical run `31809994339` failed live correlation because extracted Ubuntu Qt 6.4 shadowed bundled official-client Qt 6.9.

Recovery rule:

- toolroot/sysroot libraries are compile/tool-only;
- official client runtime must use its bundled Qt 6.9;
- launch in a working D-Bus/AT-SPI session;
- after semantic world entry query read-only bridge `session-status` and correlate with decoded structural map/world state.

## Live world state

```yaml
reversible_path:
  - [32546, 32510, 7]
  - [32546, 32509, 7]
  - [32546, 32510, 7]
aware_range: [18, 14]
player_position:
  classification: DERIVED
  direct_member: UNKNOWN
```

Single-item drag delivered stimulus but has no server-confirmed MoveObject result; below A3.

## Ordered continuation

1. Reconcile primary head `4ac4a754...` with recovery evidence. Preserve fresh `0xb46bd0/0xb46c75` QMeta/TCP evidence but reject stale references to `0xb5b880`.
2. Inspect run `31825417040` after a state change; do not spam redispatch while queued/active.
3. Decode QMetaObject `0x30b7d00` + `qt_static_metacall 0xdd1cc0`; enumerate direct `QTcpSocket::QTcpSocket(QObject*)` callsites; prove constructor/member assignment for `[this+0x10]`.
4. Resolve exact `TIODeviceWriter` and `TGameserverTCPConnection` vtables and connect `0xc2df80 -> 0xb47130 -> TGameserverDualConnection` to the real gameplay socket writer.
5. Distinguish connection-control/newline writer from binary Tibia gameplay-frame write; prove final framing/encryption/compression/sequence ordering and wire boundary.
6. Repair bridge runtime isolation (bundled Qt 6.9 + live D-Bus/AT-SPI), then correlate bridge `session-status` with structural world state.
7. Recover direct P0 reads with causal/restart-stable evidence.
8. Promote safest reversible movement/action to A3/A4 parity.
9. Complete quantitative protocol/QMeta coverage.
10. Repair remaining CI quality issues and perform final audit/PR reconciliation/merge/archive only if all gates permit.

## Durable sources to read first

- `docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-continuation-state.yaml`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-chatgpt-network-handoff-correction.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-queue-qslot-consumer-success.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-derived-transport-field-provenance.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-unencrypted-raw-message-stream-proven.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-stream-owner-pair-mapping.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-outbound-owner-vtable-resolution.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-direct-qiodevice-write-classification.md`
- primary-branch `docs/agents/evidence/OTC-20260813-official-client-re/20260814-direct-writer-gameserver-tcp-candidate.md`

## Next action

Reconcile the fresh primary-branch TCP/QMeta candidate with the corrected recovery outbound model, then resolve `[0xb46bd0 this+0x10]` to a concrete socket/device class and find the binary gameplay-frame write. Persist every promoted/disproven result before moving to the next slice.
