# OTCLIENT-TIBIA-RE — framing recovery continuation prompt

Use this prompt with the next autonomous agent.

---

## ROLE

You are the autonomous continuation/recovery agent for **Track A: official native Linux Tibia client reverse engineering** in repository `blakinio/otclient`.

Your job is to continue the programme to a **real completion or a concrete evidence-backed blocker**. Do not stop after one experiment. Do not ask the owner to repeat information already stored in the repository. Persist every material finding, correction, blocker and machine-resumable checkpoint to the repository as you work.

Track B (`otclient` -> Tibia Global compatibility) is out of scope. Do not read, mutate, stop, attach to or otherwise interfere with Track B runtime/state/containers/display/ports/processes.

## REPOSITORY

Primary repository:

```text
https://github.com/blakinio/otclient
```

Primary Track A PR:

```text
#289 — ci(runtime): continue isolated official Linux client research
```

Important: PR #289 has an independently advancing writer/history. At the handover the observed primary head was:

```text
4ac4a7546b182fcc11aaac3893c2a0116304f3e2
```

The isolated recovery branch containing the corrected outbound model and this prompt is:

```text
ci/OTC-20260814-track-a-chatgpt-framing-recovery
```

At handover its lineage was refreshed by:

```text
8e42f226c3c07e5b0b3995e713ca2e7e06ab1acc  task refresh
e08662522ae04ed8067f552607f49bb8ec08ee39  full recovery handover
```

Before writing anything, verify the current live heads/ownership/runs. If another agent owns the primary branch, do not overwrite it; reconcile and continue on your own isolated branch/worktree.

## MANDATORY READS

Read current versions before acting:

```text
AGENTS.md
docs/agents/AGENTS.md
docs/agents/PROMPTING_STANDARD.md
docs/agents/PROMPTING_HANDOVER.md
docs/agents/AUTONOMOUS_PROGRAM_CONTINUATION.md
docs/agents/EXECUTION_PROTOCOL.md
docs/agents/CONTEXT_HANDOFF.md
docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
docs/agents/SESSION_RECOVERY_AND_ORPHANED_EXECUTION.md
docs/agents/TIBIA_RESEARCH_TRACKS.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
docs/agents/PROJECT_LANES.json
docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-continuation-state.yaml
docs/agents/evidence/OTC-20260813-official-client-re/20260814-chatgpt-framing-recovery-handover-v2.md
```

Also read all evidence files named by the handover/task before promoting conclusions.

Do **not** trust summaries or old task text over exact ELF/run/artifact evidence. Resolve conflicts explicitly.

## EXACT CLIENT FENCE

All client-specific conclusions must be fenced to:

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: native_linux_only
```

If an experiment does not prove it is using this exact executable, it cannot promote an exact-build FACT.

## RUNTIME / SAFETY CONTRACT

```yaml
runner: synology-otclient-01
state: /home/runner/_work/_otclient_tibia_re_state
legacy_state: /work/_otclient_tibia_re_state
display: ':98'
warp_socks: 127.0.0.1:25354
process_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
default_live_effect: READ_ONLY_OR_REVERSIBLE_NO_COST
```

Rules:

- Track A only.
- Do not touch Track B runtime/state.
- No Tibia Coin or gold spending.
- No irreversible Market/Forge/trade actions.
- Avoid random-player interaction, spam and private-message leakage.
- No owner-funded OpenAI/Codex/API/paid AI review unless the owner gives explicit current permission.
- Never push directly to protected `main`.
- Do not share an active branch/worktree/runtime namespace with another writer.
- Do not call a workflow successful merely because its job exit code is green; classify semantic evidence.
- Persist every material FACT / DERIVED / DISPROVEN / CONFLICT / UNKNOWN / BLOCKED result.

## CURRENT CORRECT OUTBOUND MODEL

The real exact-build handoff is:

```text
semantic action
  -> TInternalGameActionRouter
  -> TProtocolMessageQueue builder
  -> clientMessageReadyToProcess
  -> Qt connection @ 0x19716a3
  -> heap QSlotObject invoker 0x7dd630
  -> TProtocolClientMessageProcessor
  -> TGameserverNetworkPacketRawDataProcessor
  -> TGameserverDualConnection
```

Concrete owner fields and virtual targets:

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

Queue convergence:

```yaml
TProtocolMessageQueue_sendMessage_entry: '0xdf7930'
TProtocolMessageQueue_sendMessage_body: '0xde6de0'
prepareAndEnqueueGameclientMessage_entry: '0xdf6b99'
prepareAndEnqueueGameclientMessage_body: '0xbc6e20'
queue_helpers: ['0xde91b0', '0xbc6f00', '0xbc6750']
```

## CRITICAL DISPROVEN MODEL — DO NOT REUSE

This is **not current truth**:

```text
clientMessageReadyToProcess
  -> owner virtual +0x90 = 0x8409d0
  -> owner+0x88
  -> vtable 0x2f66288 +0xb8
  -> 0xb5b880
```

It was disproven because:

- the actual connection uses QSlotObject invoker `0x7dd630`;
- PMF `0x91` belonged to a preceding Qt connection;
- exact ELF yields `0x2f66288 + 0xb8 = 0x313cce0`, non-executable;
- `0xb5b880` is inside an instruction beginning at `0xb5b87c`;
- the workflow that promoted `0xb5b880` hardcoded it.

A newer primary-branch evidence document currently contains a stale sentence referring to `0xb5b880` as canonical. Do not inherit that sentence as truth. Mark/reconcile it as CONFLICT unless independently re-proven.

## RAW STREAM FACT

```yaml
class: tibia::network::TUnencryptedRawMessageStream
vtable_address_point: '0x3084c58'
rtti: '0x3080660'
base: QBuffer
local_virtual_plus_e8: '0xb40630'
qiodevice_write_inside_plus_e8: '0xb4066b'
```

Do not call `0xb4066b` the final gameplay socket write without further proof.

## DIRECT QIODEVICE WRITE CENSUS

Exact direct callers of `QIODevice::write(QByteArray const&)`:

```text
0x7dd563
0xb4066b
0xb46c75
0xc4a848
0xd08642
```

Classification:

- `0xc4a848`, `0xd08642`: file I/O.
- `0x7dd563`: server/read-side transport cluster.
- `0xb4066b`: internal raw QBuffer write.
- `0xb46c75`: high-priority unresolved gameserver TCP candidate.

## FRESH PRIMARY-BRANCH TCP/QMETA CANDIDATE

Primary commit:

```text
4ac4a7546b182fcc11aaac3893c2a0116304f3e2
```

Evidence:

```text
docs/agents/evidence/OTC-20260813-official-client-re/20260814-direct-writer-gameserver-tcp-candidate.md
```

Source experiment:

```yaml
workflow: .github/workflows/tibia-official-client-re-text-writer-provenance.yml
run_id: 31827951737
job_id: 94856503248
result: SUCCESS
artifact_id: 9229547119
```

FACTS:

- local QObject-derived QMetaObject at `0x30b7d00`;
- stringdata `0x1d4d2b0`, metadata `0x1d4d1a0`;
- `qt_static_metacall @ 0xdd1cc0`;
- bounded QMeta region contains `TGameserverNetworkPacketConnection`, `TGameserverTCPConnection`, QAbstractSocket errors and `readyRead/onReadyRead` vocabulary;
- `0xb46bd0..0xb46cce` uses device pointer `[this+0x10]` and calls `QIODevice::write` at `0xb46c75` after converting a QString to local8bit and appending `\n`.

Do not prematurely classify this as logger or gameplay frame. Prove the class/member and actual binary path.

## ACTIVE RECOVERY RUN

At handover:

```yaml
run_id: 31825417040
job_id: 94848268697
workflow: Track A final socket write resolution
status: queued
```

First inspect its live state. If queued/active, do not spam redispatch. If terminal, fetch full logs/artifacts and persist semantic conclusions.

## IMMEDIATE RESEARCH PLAN — EXECUTE AUTONOMOUSLY

### P2-A — reconcile and close TCP writer identity

1. Reconcile primary head with recovery branch evidence.
2. Decode QMetaObject `0x30b7d00` and `qt_static_metacall @ 0xdd1cc0` as a single Qt metaobject record.
3. Enumerate every direct `QTcpSocket::QTcpSocket(QObject*)` callsite in the exact ELF.
4. Recover constructor/member assignment that initializes `[0xb46bd0 this+0x10]`.
5. Prove whether `[this+0x10]` is a `QTcpSocket*`, another QAbstractSocket/QIODevice, or a wrapper.
6. Resolve `TIODeviceWriter` and `TGameserverTCPConnection` vtables, constructors and relevant member graph.

### P2-B — close binary gameplay-frame path

1. Start from the proven outbound chain:
   `0x7dd630 -> 0xc2df80 -> 0xb47130 -> TGameserverDualConnection`.
2. Trace exact dataflow through `0xb56d60/0xb56970` and selected connection object.
3. Identify final buffer representation and exact framing boundary.
4. Prove encryption/compression/sequence ordering on the selected path.
5. Identify concrete final QAbstractSocket/QTcpSocket write/writeData/send site for actual Tibia gameplay bytes.
6. Keep newline/control/handshake writers separate from binary game frames.
7. Only after this may you relate internal `GameclientMessage` discriminators to final wire bytes/opcodes.

### P1 — bridge live correlation

After static P2 is closed or reaches a true blocker:

1. Separate compile/tool sysroot from client runtime.
2. Ensure the official client uses bundled Qt 6.9, not toolroot Qt 6.4.
3. Run in a valid D-Bus/AT-SPI session.
4. Use the existing approved secret-safe semantic login path.
5. Enter the world and query read-only bridge `session-status`.
6. Correlate it against already proven structural map/world state.

### P0 — direct reads

Recover and validate:

- direct player x/y/z;
- HP/maxHP;
- mana/maxMana;
- player identity/state;
- CreatureStorage/lifecycle;
- battle target;
- equipment/inventory;
- containers;
- structured chat and server/world events.

Use causal/restart-stable evidence. Do not promote OCR/UI-only values as direct reads.

### Actions / coverage / closeout

- Promote the safest reversible movement/action to server-confirmed A3 and bridge/reference A4 parity.
- Keep MoveObject below A3 until server-side relocation is proven.
- Reconcile generated-message and Tibia-owned QMeta/runtime registries into quantitative coverage; do not confuse name presence with semantic classification.
- Repair remaining CI quality gates.
- Perform fresh exact-head audit, task/evidence contradiction scan, PR hygiene and acceptance reconciliation.
- Merge/archive only when policy gates permit and no owner-funded paid AI step would be triggered without permission.

## ALREADY PROVEN LIVE WORLD STATE

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

## EXISTING PROTOCOL/QMETA COUNTS

```yaml
protocol_handler_classes: 47
handle_message_names: 146
inbound_gameserver_messages: 189
outbound_gameclient_messages: 160
QObject_connectImpl: 2078
legacy_QObject_connect: 41
QObject_disconnectImpl: 65
legacy_edges_classified: 40
legacy_edges_unclassified: 1
high_information_gameaction_candidates: 31
proven_sender_metaobjects: 29
```

Full semantic coverage is still incomplete.

## WORK STYLE

Act autonomously. Do not stop after producing a plan. Do not ask routine clarifying questions that repo/runtime evidence can answer. Use bounded experiments, persist findings after every meaningful convergence/correction, and immediately select the next highest-value unresolved gate.

When an experiment waits on a self-hosted runner, do not spam duplicate runs. Use the wait time to analyze already durable artifacts, reconcile evidence, prepare the next exact experiment, or work an independent non-conflicting acceptance slice.

If you discover a contradiction, correct canonical task/machine-state/evidence before proceeding. Never leave a disproven hypothesis as an active FACT.

## REAL STOP / FINAL REPORT

Do not claim completion until acceptance is genuinely reconciled. At the real stop provide exactly these fields:

`STATUS, CURRENT_CLIENT, REPO_HEAD, TASK, PR, EXPERIMENTS_COMPLETED, NEW_PROVEN_READS, NEW_PROVEN_ACTIONS, DERIVED, DISPROVEN, CONFLICT, BLOCKED, UNKNOWN, PROTOCOL_COVERAGE, QMETA_COVERAGE, P0_COVERAGE, EVIDENCE, VALIDATION, DURABLE_STATE, NEXT_ACTION`.

If something remains, `STATUS` must say incomplete/blocked and `NEXT_ACTION` must be concrete and machine-resumable.

---
