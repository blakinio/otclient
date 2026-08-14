# Track A continuation handover for ChatGPT

Date: 2026-08-14
Repository: `blakinio/otclient`
Track: Track A / `official-client-re` / `OTCLIENT-TIBIA-RE`
Active task: `OTC-20260813-official-client-re-continuation`
PR: #289
Branch at handover creation: `ci/OTC-20260813-official-client-re-continuation`
Verified head before this handover write: `92df22f6dbcfed8108b8c5f33ec3d58b80de317a`

This record is a continuation checkpoint, not a completion claim. Revalidate the live head, runner, client SHA, runtime PIDs, PIE bases and workflow state before executing further work.

## Exact client boundary

```yaml
official_client_version: 15.32.df7b29
official_client_size: 51965216
official_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
runner: synology-otclient-01
state: /home/runner/_work/_otclient_tibia_re_state
legacy_state: /work/_otclient_tibia_re_state
display: :98
warp_socks_port: 25354
process_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
```

All exact addresses below are exact-build evidence only and must be rediscovered if the client SHA changes.

## Promoted facts

### Static protocol and QMeta census

- Exact binary census recovered 47 `ProtocolMessageHandler` classes, 146 `handleMessage` names, 189 inbound `GameserverMessage` names and 160 outbound `GameclientMessage` names.
- The embedded serialized descriptor set contains seven valid `FileDescriptorProto` records. The recovered `Coordinate` schema is `x=1`, `y=2`, `z=3`, all `uint32`.
- Selected high-value Gameserver/Gameclient schemas are not present in those seven embedded descriptors, so their field/layout recovery must use generated C++ metadata/accessors/disassembly/runtime objects rather than assuming embedded descriptors exist.
- The stripped client exposes no useful `qt_static_metacall` / `staticMetaObject` / handler symbols through the normal GDB symbol table; raw QMeta reconstruction remains the productive path.

Primary references:

- `20260814-official-client-protocol-surface-inventory.md`
- `20260814-protocol-handler-qmeta-neighborhoods.md`
- `20260814-protobuf-descriptor-census-and-xref-gate.md`

### Qt connection graph

Repaired direct callsite census proved:

```yaml
QObject_connectImpl: 2078
QObject_connect_legacy_string_api: 41
QObject_disconnectImpl: 65
total_direct_calls: 2184
```

Further bounded reconstruction established:

- all 41 legacy connect callsites were disassembled;
- 40 were classified into UI/controller edges and one remains explicitly `UNCLASSIFIED`;
- 31 high-information GameAction/connectImpl candidate sites were isolated across the selected GameAction families;
- for 29/31 sites the nearby GameAction QMeta object was proven to be the sender metaobject;
- QSlotObject invoke addresses were resolved for all 29 proven sender sites;
- those invoke addresses are generic Qt member-pointer/slot dispatch machinery, not receiver serializers;
- the shared receiver at `0x8332d0` is `tibia::game::TInternalGameActionRouter`, an internal action router/re-emitter, not the network serializer.

Primary references:

- `20260814-qt-connect-callsite-census.md`
- `20260814-gameaction-connectimpl-arguments.md`
- `20260814-gameaction-slot-provenance.md`
- `20260814-receiver-serializer-handover.md`

### Outbound semantic action builders

Concrete `TProtocolMessageQueue` QMeta/dispatch work recovered action-builder bodies and internal `GameclientMessage` discriminators for at least:

- directional movement / movement family;
- `MoveObject`;
- `Talk`;
- `Attack`;
- `Follow`;
- `TradeObject`.

Important exact-build convergence points:

```yaml
TProtocolMessageQueue_sendMessage_entry: 0xdf7930
TProtocolMessageQueue_sendMessage_body: 0xde6de0
prepareAndEnqueueGameclientMessage_entry: 0xdf6b99
prepareAndEnqueueGameclientMessage_body: 0xbc6e20
queue_processing_helpers:
  - 0xde91b0
  - 0xbc6f00
  - 0xbc6750
```

Internal message discriminators are proven internal `GameclientMessage` selectors only. They are NOT yet promoted to final wire opcodes/bytes.

Primary reference:

- `20260814-protocol-queue-action-builders.md`

### Queue to transport-owner handoff

Static/Qt reconstruction currently closes the high-level outbound chain to:

```text
semantic GameAction
-> internal action router / receiver chain
-> TProtocolMessageQueue builder
-> clientMessageReadyToProcess
-> containing network owner
-> containing owner virtual slot +0x90
-> QTcpSocket-bearing setup path
```

Additional exact-build evidence:

- `clientMessageReadyToProcess` hands queue owner `+0x88` to the containing owner's virtual slot `+0x90`;
- the setup path constructs a `QTcpSocket` at `+0x196fee0`;
- `0x3085ba0` was identified as `TCreatureStorage` and explicitly rejected as the transport owner.

Still UNKNOWN:

- the concrete function behind containing-owner virtual slot `+0x90`;
- the exact serializer/framing function;
- whether internal discriminators are preserved as final wire bytes.

Primary reference:

- `20260814-protocol-queue-network-handoff.md`

### Live structural world and reversible movement

A real official-client live world session has now produced structural map evidence, not merely a visible window or connected socket.

Persistent structural observer plus reversible movement produced the derived path:

```text
(32546, 32510, 7)
-> (32546, 32509, 7)
-> (32546, 32510, 7)
```

Promoted boundary:

- FACT: exact live client produced coherent floor-7 map strips for forward and inverse movement and returned to the initial derived coordinate;
- FACT: the post-login map-description hook yields structural `x/y/z`, stack order and exact-build object-field candidates;
- FACT: current-floor aware-range directional strips measure `18 x 14`;
- DERIVED: the player coordinate is the fixed viewport center calculated from authoritative decoded strips;
- UNKNOWN: a direct standalone player-object position member address remains unpromoted.

Primary references:

- `20260814-live-structural-world-and-reversible-movement.md`
- `20260814-map-observation-and-dynamic-provenance-checkpoint.md`
- `experiments/EXP-20260814-live-reversible-movement.yaml`

### Read-only runtime bridge continuation

The PR #283 read-only bridge source was rebuilt successfully in run `31809994339`, but the live correlation step then failed because extracted Ubuntu Qt 6.4 libraries shadowed the official client's required bundled Qt 6.9 runtime.

Exact observed runtime error:

```text
libQt6Core.so.6: version Qt_6.9 not found
```

This is an environment/library-path failure, not evidence against the bridge design.

Current deterministic bridge recovery action:

```text
Keep extracted build tools/libraries out of the client LD_LIBRARY_PATH, launch the client against its bundled Qt 6.9 runtime, then repeat semantic world login and query bridge session-status against the already proven decoded world/map state.
```

### Controlled single-item drag experiment

A separate bounded branch `ci/OTC-20260814-track-a-single-item-drag` ran exact head `b4eab37373b6ef5901caaa0a59a42b07eb5e96b8` as run `31806475888`, job `94786521265`, and completed `SUCCESS` on `synology-otclient-01`.

Before stimulus it proved network confinement:

```yaml
local_socks_established: 2
direct_established: 0
udp_socket_count: 0
connected_world_gate: true
```

It sent one adjacent-tile drag from window coordinate `526,397` to `526,365` and observed:

```yaml
changed_pixels: 35335
events_delta: 0
strips_delta: 0
session_left_running: true
```

Classification:

- FACT: the controlled UI drag stimulus was delivered in a connected, confined live world session;
- FACT: no new map-provenance event or strip record was produced by the current observer in that bounded observation window;
- NOT PROVEN: `MoveObject` semantic success;
- NOT PROVEN: server-confirmed object relocation;
- therefore DO NOT promote this experiment to A3 or A4.

The next item-move experiment must observe the authoritative source/destination object state or outbound semantic message plus server-confirmed inverse state, not rely on changed pixels.

## Current unresolved high-value boundaries

1. Concrete function behind network-owner virtual slot `+0x90`.
2. Exact serializer/framing and final network-send path after `TProtocolMessageQueue`.
3. Final wire-byte relationship of internal `GameclientMessage` discriminators.
4. Read-only bridge `session-status` correlated with already decoded structural world state.
5. Direct standalone player position member (current position remains structurally DERIVED from map strips).
6. P0 live reads still needing causal/restart-stable promotion: HP/maxHP, mana/maxMana, player identity/state, CreatureStorage/lifecycle, target, inventory/equipment, containers, chat, world/server events.
7. Server-confirmed semantic actions and eventual A4 bridge parity.
8. Complete quantitative S1/S2 classification/coverage must be rechecked before any 100% claim.

## Recommended continuation order

### P1 — repair bridge/runtime library separation

- use build sysroot/toolchain only for compilation;
- do not expose extracted Qt 6.4 libraries to the official client process;
- launch using bundled Qt 6.9;
- semantic login through the repository-approved non-secret path;
- correlate bridge `session-status` with decoded map/world structural state;
- record live PID/PIE/session epoch and exact evidence.

### P2 — finish outbound serializer/framing convergence

Follow:

```text
TProtocolMessageQueue::sendMessage body 0xde6de0
queue helpers 0xbc6750 / 0xbc6f00 / 0xde91b0
containing network owner virtual slot +0x90
QTcpSocket-bearing path
```

Recover the exact slot and serializer/framing transition. Do not infer wire bytes from internal discriminators without capture/structural proof.

### P3 — promote one semantic action causally

Use the safest reversible action first, preferably movement or another zero-cost action whose reference path is already structurally observable.

Required parity:

```text
official semantic reference action
-> outbound semantic message
-> server-confirmed structural result

agent semantic invocation
-> same semantic fields
-> server-confirmed structural result
-> inverse/recovery
```

Only then promote A3; A4 requires the stable bridge invocation path.

### P4 — complete P0 live read gates

Priority:

1. HP/maxHP;
2. mana/maxMana;
3. player identity/state;
4. CreatureStorage and lifecycle;
5. target;
6. inventory/equipment;
7. containers;
8. chat;
9. world/server events.

Use no-stimulus baseline, controlled stimulus, inverse/recovery, repeat x3 where practical, negative control and restart validation before R3/R4 promotion.

### P5 — reconcile registries and coverage

Before closing the research task:

- ensure every recovered generated message is `CLASSIFIED` or explicitly `UNCLASSIFIED`;
- ensure every recovered Tibia-owned QMeta/runtime entry is classified, ignored-with-reason or unclassified;
- reconcile machine-readable canonical registries rather than creating duplicates;
- publish quantitative protocol/QMeta/P0/action coverage;
- run fresh audit, exact-head CI, PR hygiene and task closeout only when acceptance is truly terminal.

## Safety and claim boundaries

- Native Linux only.
- Track A only; do not read or mutate Track B runtime/state.
- No OCR as structural proof path.
- No credentials, tokens, cookies, private chat content or proprietary client bytes committed.
- Default live actions must be reversible and no-cost.
- No Tibia Coin/gold spending, Forge/Market/irreversible mutations, random-player trade/party/social tests or anti-cheat bypass work.
- Do not consume Codex/OpenAI API/other owner-funded AI quota unless separately authorized for that exact use.
- Never promote STATIC_PRESENT to live read/action without the required R/A gate evidence.

## Next agent bootstrap

Start by re-reading live repository policy and this active task, then verify current PR #289 head and runtime state. Treat this file as a recovery map only. The first preferred live action is bridge/runtime Qt separation and `session-status` correlation; in parallel, if live execution is blocked, continue the static network-owner `+0x90` / serializer/framing convergence instead of waiting.