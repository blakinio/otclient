# Track A — ChatGPT framing recovery handover v2

Date: 2026-08-14  
Track: `official-client-re` / `OTCLIENT-TIBIA-RE`  
Repository: `blakinio/otclient`  
Primary PR: `#289`

## Purpose

This handover preserves the reconciled state of the official native Linux Tibia client reverse-engineering programme after correcting a major false outbound model and recovering the real Qt handoff / transport-owner structure. It is intended to be sufficient for a new autonomous agent to resume without relying on conversation memory.

Do not trust summaries blindly. Repository evidence, exact GitHub Actions artifacts/logs and exact-build ELF observations remain the source of truth.

## Mandatory exact-client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: native_linux_only
```

No client-specific FACT may be promoted without this fence.

## Branch state at handover

```yaml
primary_pr: 289
primary_branch: ci/OTC-20260813-official-client-re-continuation
primary_head_observed: 4ac4a7546b182fcc11aaac3893c2a0116304f3e2
recovery_branch: ci/OTC-20260814-track-a-chatgpt-framing-recovery
recovery_head_before_handover_commits: 7e9db4a04aa914ea209f68eeaf39181120e230ba
task_refresh_commit: 8e42f226c3c07e5b0b3995e713ca2e7e06ab1acc
```

The primary branch advanced independently. Do not push blindly to it while another writer may own it. Reconcile primary and recovery evidence first; continue on an isolated branch when ownership is not explicit.

## Current active external operation

```yaml
workflow: Track A final socket write resolution
run_id: 31825417040
job_id: 94848268697
last_observed_status: queued
recovery_experiment_head: 2f7e322b8da5139351e8b8faf91605795a117483
```

Do not repeatedly redispatch the same semantic operation while it remains queued/active. Inspect it after a state change. If the self-hosted runner remains unavailable, use existing exact-build artifacts/evidence or create a non-conflicting fallback rather than touching Track B runtime.

## Correct outbound handoff — FACT

The previous primary-owner `+0x90` model was false. The current exact-build handoff is:

```text
semantic action
  -> TInternalGameActionRouter
  -> TProtocolMessageQueue builder
  -> clientMessageReadyToProcess
  -> Qt connection callsite 0x19716a3
  -> heap QSlotObject invoker 0x7dd630
  -> TProtocolClientMessageProcessor
  -> TGameserverNetworkPacketRawDataProcessor
  -> TGameserverDualConnection
```

Concrete owner shared-pointer pairs and virtuals:

```yaml
'+0x9f0/+0x9f8':
  class: tibia::protocol::TProtocolServerPacketProcessor
'+0xa00/+0xa08':
  class: tibia::protocol::TProtocolClientMessageProcessor
  virtual_plus_0x10: '0xc2df80'
'+0xa10/+0xa18':
  class: tibia::network::TGameserverNetworkPacketRawDataProcessor
  virtual_plus_0x10: '0xb47130'
'+0xc18/+0xc20':
  class: tibia::network::TGameserverDualConnection
  virtual_plus_0x80: '0xb56d60'
  virtual_plus_0x78: '0xb56970'
  precondition_plus_0x90: '0xb40370'
```

Exact queue convergence already retained:

```yaml
sendMessage_entry: '0xdf7930'
sendMessage_body: '0xde6de0'
prepareAndEnqueueGameclientMessage_entry: '0xdf6b99'
prepareAndEnqueueGameclientMessage_body: '0xbc6e20'
queue_helpers: ['0xde91b0', '0xbc6f00', '0xbc6750']
```

## Major correction — old `+0x90 -> 0xb5b880` model is DISPROVEN

Never use this as the current root:

```text
clientMessageReadyToProcess
  -> owner virtual +0x90 = 0x8409d0
  -> owner+0x88
  -> vtable 0x2f66288 +0xb8
  -> 0xb5b880
```

Why it is invalid:

- the real `clientMessageReadyToProcess` connection uses heap QSlotObject invoker `0x7dd630`;
- PMF value `0x91` belonged to the preceding Qt connection and was mis-associated;
- exact ELF gives `0x2f66288 + 0xb8 = 0x313cce0`, which is non-executable;
- `0xb5b880` lies inside an instruction beginning at `0xb5b87c`;
- the workflow that promoted `0xb5b880` hardcoded the value instead of deriving it from ELF.

Classification: **DISPROVEN / SUPERSEDED**.

A fresh primary-branch evidence document still contains a sentence referring to `0xb5b880` as a canonical outbound subobject target. That sentence conflicts with stronger exact-build recovery evidence and must be treated as stale unless independently re-proven.

## `TUnencryptedRawMessageStream` — FACT

```yaml
class: tibia::network::TUnencryptedRawMessageStream
rtti_mangled: N5tibia7network28TUnencryptedRawMessageStreamE
vtable_address_point: '0x3084c58'
rtti: '0x3080660'
base_class: QBuffer
local_virtuals:
  '+0xe8': '0xb40630'
  '+0xf0': '0xb40690'
  '+0xf8': '0xb40710'
qiodevice_write_inside_0xb40630: '0xb4066b'
qiodevice_readall_wrapper: '0xb40710'
source_run: 31824001391
source_job: 94843696871
result: SUCCESS
```

Two instances are constructed in the owner setup; evidence indicates read/server-side and write/client-side uses. Do not conflate them.

## Direct `QIODevice::write(QByteArray const&)` census

Exact callsites:

```text
0x7dd563
0xb4066b
0xb46c75
0xc4a848
0xd08642
```

Current classification:

- `0xc4a848`, `0xd08642`: file I/O, excluded from gameplay socket path.
- `0x7dd563`: tied to server/read-side transport cluster; not outbound final gameplay write.
- `0xb4066b`: internal `TUnencryptedRawMessageStream` / QBuffer write; not yet final socket.
- `0xb46c75`: **high-priority unresolved gameserver TCP candidate**.

Earlier recovery inference treated `0xb46bd0/0xb46c75` as a likely generic text/log writer because it does `QString -> local8bit -> append('\n') -> QIODevice::write`. Fresh primary-branch evidence makes that elimination unsafe.

### Fresh primary-branch candidate evidence

Commit:

```text
4ac4a7546b182fcc11aaac3893c2a0116304f3e2
```

Evidence file:

```text
docs/agents/evidence/OTC-20260813-official-client-re/20260814-direct-writer-gameserver-tcp-candidate.md
```

Exact experiment:

```yaml
workflow: .github/workflows/tibia-official-client-re-text-writer-provenance.yml
run_id: 31827951737
job_id: 94856503248
head: 9e11f3a7f7712df7f9de28221b84437ee1b4def1
result: SUCCESS
artifact_id: 9229547119
```

FACTS from that evidence:

- local QObject-derived QMetaObject at `0x30b7d00`;
- stringdata `0x1d4d2b0`, metadata `0x1d4d1a0`, static metacall `0xdd1cc0`;
- bounded QMeta/stringdata neighborhood contains `TGameserverNetworkPacketConnection`, `TGameserverTCPConnection`, `QAbstractSocket::SocketError`, `readyRead`, `onReadyRead`, connection/error signals/slots;
- function FDE `0xb46bd0..0xb46cce` obtains device from `[this+0x10]`, emits a Qt signal, converts a member QString to local8bit, appends newline, and calls `QIODevice::write(QByteArray const&)` at `0xb46c75` through that member.

UNKNOWN:

- exact semantic class identity of QMetaObject `0x30b7d00`;
- concrete type of `[this+0x10]` (`QTcpSocket*`, another QAbstractSocket/QIODevice, or wrapper);
- whether the newline payload is connection-control/proxy/handshake text or Tibia gameplay data;
- where the actual binary gameplay frame crosses into the final socket.

## Transport RTTI inventory

```yaml
TGameserverTCPConnection: '0x3080630'
TGameserverNetworkPacketConnection: '0x3080648'
TUnencryptedRawMessageStream: '0x3080660'
TGameserverNetworkPacketSequenceFlowProcessor: '0x3080678'
TGameserverDualConnection: '0x30b7628'
TIODeviceWriter: '0x3080718'
TProtocolWriter: '0x3080728'
TProtobufClientMessageTranslator: '0x3080748'
TProtocolClientMessageProcessor: '0x3080758'
TGameserverNetworkPacketRawDataProcessor: '0x3080768'
```

Immediate missing proof is the concrete vtable/member graph for `TIODeviceWriter` and `TGameserverTCPConnection`, and its connection to the real binary gameplay write.

## Live structural world proof

```yaml
reversible_path:
  - [32546, 32510, 7]
  - [32546, 32509, 7]
  - [32546, 32510, 7]
aware_range: [18, 14]
map_callback_has_xyz_and_stack_order: true
player_coordinate:
  classification: DERIVED
  derivation: fixed viewport center from authoritative decoded map strips
  direct_member: UNKNOWN
```

Movement is structurally proven and reversible. Single ground-item drag delivered the stimulus but did not prove server-side `MoveObject`; it remains below A3.

## Protocol/QMeta census already established

```yaml
protocol_handler_classes: 47
handle_message_names: 146
inbound_gameserver_messages: 189
outbound_gameclient_messages: 160
QObject_connectImpl_direct_calls: 2078
QObject_connect_legacy_calls: 41
QObject_disconnectImpl_direct_calls: 65
legacy_edges_classified: 40
legacy_edges_unclassified: 1
gameaction_high_information_candidates: 31
proven_sender_metaobjects: 29
```

Do not convert name-presence counts into semantic 100% coverage. Full quantitative semantic coverage remains incomplete.

## Bridge state / P1

Bridge build is proven. Historical run `31809994339` failed client launch because extracted Ubuntu Qt 6.4 polluted the client runtime `LD_LIBRARY_PATH`, while the official client requires bundled Qt 6.9.

Recovery requirements:

1. Keep bridge build sysroot/toolroot separate from client runtime libraries.
2. Do not expose toolroot Qt 6.4 to the client.
3. Use official client bundled Qt 6.9 (`runtime/bin/lib` / bundled RUNPATH as appropriate).
4. Run inside a live D-Bus/AT-SPI session.
5. Enter the world through the already approved secret-safe semantic login path.
6. Query read-only bridge `session-status` and correlate with structural map/world evidence.

## P0 gaps still open

- direct standalone player position member;
- HP/maxHP;
- mana/maxMana;
- player identity/state;
- CreatureStorage/lifecycle;
- battle target;
- inventory/equipment;
- containers;
- structured chat and server/world events.

Evidence must be causal and restart-stable where possible; UI/OCR-only observations are insufficient for direct-read acceptance.

## Ordered autonomous continuation

1. Read mandatory agent/project standards and current task/state.
2. Verify PR #289, primary branch head, recovery branch head, active runs and ownership. Do not share a branch/worktree/runtime with an active writer.
3. Reconcile fresh primary `0xb46bd0/0xb46c75` TCP/QMeta evidence with recovery outbound evidence. Preserve the new candidate; reject stale `0xb5b880` references.
4. Inspect run `31825417040` after state change. If terminal, persist exact artifacts/results; if still queued, do not spam redispatch.
5. Decode QMetaObject `0x30b7d00` and `qt_static_metacall @ 0xdd1cc0` as one record.
6. Enumerate every direct `QTcpSocket::QTcpSocket(QObject*)` construction site and recover the constructor/store initializing `[0xb46bd0 this+0x10]`.
7. Resolve `TIODeviceWriter` and `TGameserverTCPConnection` vtables/constructors/member graph.
8. Follow exact dataflow from `TProtocolClientMessageProcessor@0xc2df80` through `TGameserverNetworkPacketRawDataProcessor@0xb47130` and `TGameserverDualConnection` (`0xb56d60/0xb56970`) to the concrete socket/device.
9. Distinguish connection-control/newline write from binary Tibia gameplay-frame write. Prove framing, encryption/compression, sequencing and final socket boundary before assigning wire semantics/opcodes.
10. Persist every FACT/DERIVED/DISPROVEN/UNKNOWN result under Track A evidence.
11. Then fix P1 bridge Qt/D-Bus runtime and correlate `session-status` live.
12. Recover P0 reads.
13. Promote safest reversible movement/action to A3/A4 parity.
14. Finish protocol/QMeta quantitative coverage.
15. Reconcile CI/PR/evidence, run exact-head audit, archive/merge only if policy gates allow.

## Safety and execution contract

- Track A only; Track B is out of scope.
- Default live effect: `READ_ONLY` or `REVERSIBLE_NO_COST`.
- No Tibia Coin/gold spending.
- No irreversible Market/Forge/trade actions.
- Avoid unsolicited/random-player interaction and private-message leakage.
- No owner-funded OpenAI/Codex/API/paid AI review without explicit current permission.
- Never push directly to protected `main`.
- One active task/branch/worktree per agent; if ownership is unclear, create a new isolated continuation branch.
- Do not declare success based on workflow exit code alone; classify the semantic evidence.
- Do not resurrect disproven hypotheses because a later document casually references them.

## Real completion gates

Track A is not complete until at least:

- final binary gameplay serializer/framing/final socket write is proven or a strong terminal blocker is documented;
- bridge live correlation succeeds on bundled Qt 6.9 or a terminal blocker is documented;
- P0 reads are covered to acceptance or individually documented as terminal blockers;
- safest reversible action reaches A3/A4 acceptance;
- protocol/QMeta quantitative coverage is reconciled;
- contradictions are removed/superseded in canonical evidence;
- exact-head CI/audit/PR hygiene is complete;
- task is archived only after acceptance reconciliation.

## Required final status block

At a real stop, report:

`STATUS, CURRENT_CLIENT, REPO_HEAD, TASK, PR, EXPERIMENTS_COMPLETED, NEW_PROVEN_READS, NEW_PROVEN_ACTIONS, DERIVED, DISPROVEN, CONFLICT, BLOCKED, UNKNOWN, PROTOCOL_COVERAGE, QMETA_COVERAGE, P0_COVERAGE, EVIDENCE, VALIDATION, DURABLE_STATE, NEXT_ACTION`.
