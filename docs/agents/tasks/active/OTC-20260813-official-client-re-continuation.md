---
task_id: OTC-20260813-official-client-re-continuation
status: active
track_id: official-client-re
alias: OTCLIENT-TIBIA-RE
owner: chatgpt
branch: ci/OTC-20260814-official-client-re-receiver-recovery
base_branch: ci/OTC-20260813-official-client-re-continuation
source_pr: 289
task_kind: runtime-research
phase: static-outbound-receiver-recovery
risk: medium
runtime_platform: native_linux_only
safe_to_resume: true
recovery_generation: 2
recovery_attempts: 2
ai_owner_billing_authorized: false
---

# OTC-20260813 — Official Linux client RE continuation

## Objective

Continue Track A against the **official native Linux Tibia client only**. Recover and validate structural world/player/creature/inventory/protocol/action state without OCR assumptions and promote only exact-version evidence.

## Hard scope

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

## Acceptance inventory

- [x] Track A namespace/runtime isolation proven.
- [x] Exact official Linux client version/size/SHA fenced.
- [x] Protocol inventory: 47 handler classes, 146 handle-message names, 189 inbound and 160 outbound named messages.
- [x] Qt direct call census: 2078 `connectImpl`, 41 legacy connect, 65 `disconnectImpl`.
- [x] `TInternalGameActionRouter @ 0x8332d0` proven router/re-emitter and disproven as serializer.
- [x] Outbound builders recovered for movement, `MoveObject`, `Talk`, `Attack`, `Follow`, `TradeObject`.
- [x] Structural live-world map state and reversible one-tile movement proven.
- [x] Queue-to-containing-owner handoff and receiver virtual slot offset `+0x90` proven.
- [ ] Concrete containing-owner vptr and concrete `+0x90` target re-derived after P2 conflict correction.
- [ ] Exact serializer, framing and final `QIODevice`/`QTcpSocket` network-write site proven.
- [ ] Bridge `session-status` correlated with decoded world state using bundled Qt 6.9 runtime.
- [ ] Direct standalone player-position member and P0 live reads proven.
- [ ] One safest reversible semantic action promoted through server-confirmed A3 and bridge/reference A4 parity.
- [ ] Item-level protocol/QMeta registries and quantitative coverage closed or terminally blocked.
- [ ] Fresh audit, exact-head CI, PR hygiene and archive/merge gate completed.

## Current proven outbound boundary

```text
semantic action
  -> TInternalGameActionRouter
  -> TProtocolMessageQueue builder
  -> clientMessageReadyToProcess
  -> QObject::connectImpl @ 0x7e7470
  -> receiver = containing owner
  -> pointer-to-member encoding 0x91
  -> receiver virtual slot offset +0x90
```

Queue convergence:

```yaml
TProtocolMessageQueue_sendMessage_entry: '0xdf7930'
TProtocolMessageQueue_sendMessage_body: '0xde6de0'
prepareAndEnqueueGameclientMessage_entry: '0xdf6b99'
prepareAndEnqueueGameclientMessage_body: '0xbc6e20'
queue_helpers: ['0xde91b0', '0xbc6f00', '0xbc6750']
```

The same setup family constructs a `QTcpSocket`.

## P2 conflict correction

Run `31815819731`, job `94817115581`, artifact `9225203231` (`sha256:e0ca5a278d7235e1755105775ed235a4f5ee501db2e5cb473b6d008e8f9831a3`) succeeded on the exact client.

It does **not** validate the inherited chain `0x308c408 -> 0x8409d0 -> owner+0x88 -> 0x2f66288:+0xb8 -> 0xb5b880`.

- exact `0x8409d0` is a non-trivial routine with normal prologue;
- it calls virtual slots `+0x60` and `+0x68` through `[owner+0x118]`;
- it is not the previously claimed simple forwarding thunk;
- under the captured stream, `0xb5b880` is not an instruction boundary;
- `OutGoingMessagePayload` and `OutgoingMessagePayload` literal counts are zero;
- workflow address labels were input hypotheses, not independent proof.

Concrete owner vptr and concrete receiver `+0x90` target are therefore `UNKNOWN` pending setup/constructor re-derivation.

## Structural live-world state

```yaml
reversible_path:
  - [32546, 32510, 7]
  - [32546, 32509, 7]
  - [32546, 32510, 7]
current_floor_aware_range: [18, 14]
player_coordinate: DERIVED_FROM_FIXED_VIEWPORT_CENTER
direct_player_member: UNKNOWN
```

Single adjacent ground-item drag delivered its stimulus but did not prove server-confirmed `MoveObject`; it remains below A3.

## Bridge state

Bridge source builds. Run `31809994339` failed live correlation because extracted Ubuntu Qt 6.4 shadowed the official client's bundled Qt 6.9. Recovery rule: toolroot libraries are build/tool-only; official client launch uses `$runtime/lib` bundled Qt 6.9, then bridge `session-status` is correlated with decoded world state.

## Recovery branch isolation

A concurrent Track A writer moved source branch `ci/OTC-20260813-official-client-re-continuation` to `8ac9c72ee16427a8d79526184cb525f6a2114e8e` and queued run `31816876078`. To avoid shared-writer force-push or branch mutation, this recovery continues on `ci/OTC-20260814-official-client-re-receiver-recovery`, forked from that exact source head. No Track B state is touched.

## Current unknowns

- containing-owner primary vptr and concrete virtual `+0x90` target;
- exact serializer/framing/final network write;
- relationship of internal GameclientMessage discriminators to final wire bytes;
- bridge live correlation; direct player position; HP/mana/identity/CreatureStorage/target/inventory/containers/chat/world events;
- server-confirmed semantic `MoveObject`;
- complete item-level protocol/QMeta/P0 coverage.

## Ordered continuation

1. Run exact receiver-target reconstruction from `0x7e7470` and setup/constructor provenance.
2. Continue serializer/framing/final-write convergence only from independently re-proven target.
3. Repair bridge Qt separation and correlate live `session-status`.
4. Recover P0 reads and safest reversible A3/A4 parity.
5. Complete item-level registries and quantitative coverage.
6. Repair remaining lint/CI, perform fresh audit/reviews/threads/PR hygiene, then reconcile recovery branch back to source Track A branch only after writer ownership is clear.

## Durable evidence

- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-network-handoff.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-outgoing-payload-consumer-provenance.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-chatgpt-recovery-generation-2.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-continuation-state.yaml`
- `docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-quantitative-coverage-baseline.yaml`

## Next action

Execute `.github/workflows/tibia-official-client-re-queue-receiver-exact-target.yml` on this isolated recovery branch and persist its run/job/artifact.
