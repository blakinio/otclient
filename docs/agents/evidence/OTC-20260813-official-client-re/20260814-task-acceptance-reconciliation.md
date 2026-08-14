# Track A active-task acceptance reconciliation — 2026-08-14

Repository: `blakinio/otclient`
Track: Track A / `official-client-re` / `OTCLIENT-TIBIA-RE`
Task: `OTC-20260813-official-client-re-continuation`
PR: #289

This record reconciles the older acceptance checklist in the active task against newer evidence. It does not weaken the original acceptance criteria and it does not itself mark the task complete.

## Reconciliation

### Structural login / `IN_GAME`

**Current state: PROVEN for the exact live session used by the structural map experiments.**

Evidence now exceeds a visible-window/socket-only claim:

- semantic accessible world login was executed on the owned Track A runtime;
- the exact official client subsequently produced decoded floor-7 map-strip records;
- forward and inverse movement generated coherent structural world transitions;
- the client returned to the initial derived coordinate.

Therefore the older unchecked wording that structural `IN_GAME` still needed to be re-proven is stale for that exact session. Fresh sessions still require the same structural gate before mutation.

Primary evidence:

- `20260814-live-structural-world-and-reversible-movement.md`
- `experiments/EXP-20260814-live-reversible-movement.yaml`

### Bridge session-status correlation

**Current state: UNKNOWN / NOT COMPLETE.**

The PR #283 read-only bridge source builds, but the latest live correlation attempt failed before semantic correlation because extracted Ubuntu Qt 6.4 libraries shadowed the official client bundled Qt 6.9 runtime.

Exact error:

```text
libQt6Core.so.6: version Qt_6.9 not found
```

This is an environment/library-path failure. The deterministic recovery is to keep extracted build/sysroot libraries out of the official client's runtime `LD_LIBRARY_PATH`, launch with bundled Qt 6.9, then query `session-status` against already decoded structural world state.

### Authoritative player position and reversible movement

**Current state: PARTIALLY SATISFIED WITH AN IMPORTANT BOUNDARY.**

PROVEN:

```text
(32546,32510,7)
-> (32546,32509,7)
-> (32546,32510,7)
```

The decoded map-strip geometry is authoritative structural world evidence and the reversible transition is proven.

However the player coordinate is currently **DERIVED** as the fixed viewport center from authoritative strip geometry. A direct standalone player-object position member remains `UNKNOWN`. Do not silently promote the derived coordinate to a direct-member ABI claim.

### Creature/player handler offsets and selected field layouts

**Current state: PARTIAL / NOT TERMINAL.**

PROVEN:

- relocation-backed QMeta census covers all 47 protocol-handler records;
- `TPlayerProtocolMessageHandler static_metacall=+0xd1a920` and its 22 own QMeta methods are recovered;
- `TCreatureProtocolMessageHandler` has a valid QMeta record but zero own QMeta methods, so creature routing must be recovered through the real upstream/base/direct path rather than invented local cases;
- selected Chat/Container/GameAction dispatch entries are recovered.

Still incomplete:

- deterministic field layouts for the remaining selected player/creature messages;
- complete runtime routing for creature lifecycle and P0 live state.

### Outbound builder/serializer entry points

**Current state: BUILDERS PROVEN; SERIALIZER/FRAMING NOT YET PROVEN.**

Concrete `TProtocolMessageQueue` builder bodies/internal discriminators are recovered for at least:

- movement;
- `MoveObject`;
- `Talk`;
- `Attack`;
- `Follow`;
- `TradeObject`.

Current exact-build convergence leads:

```yaml
sendMessage_entry: 0xdf7930
sendMessage_body: 0xde6de0
prepareAndEnqueueGameclientMessage_entry: 0xdf6b99
prepareAndEnqueueGameclientMessage_body: 0xbc6e20
queue_helpers:
  - 0xde91b0
  - 0xbc6f00
  - 0xbc6750
```

The queue-to-network-owner handoff is also proven through containing-owner virtual slot `+0x90`, with a `QTcpSocket`-bearing setup path.

Still `UNKNOWN`:

- concrete function behind virtual slot `+0x90`;
- exact serializer;
- exact framing;
- final network write;
- whether internal `GameclientMessage` discriminators are preserved as final wire bytes.

Therefore the original combined builder/serializer acceptance item is not yet terminal even though its builder half is now satisfied.

### Controlled `MoveObject`/item drag

**Current state: NOT A3 / NOT A4.**

Run `31806475888`, job `94786521265` successfully delivered one adjacent-tile UI drag in a confined connected world session, but the current structural observer recorded:

```yaml
changed_pixels: 35335
events_delta: 0
strips_delta: 0
```

This proves stimulus delivery only. It does not prove server-confirmed object relocation. A future `MoveObject` promotion must compare authoritative source/destination object state and inverse restoration or capture the outbound semantic message plus server-confirmed structural result.

## Current completion boundary

The task is **not complete**.

Highest-value remaining gates, in order:

1. recover live read-only bridge correlation with bundled Qt 6.9 runtime;
2. resolve concrete network-owner `+0x90` function and close serializer/framing/final-write chain;
3. promote one safest reversible semantic action, preferably movement, through reference parity to A3 and bridge A4;
4. recover P0 live reads: HP/maxHP, mana/maxMana, identity/state, CreatureStorage/lifecycle, target, inventory/equipment, containers, chat, world/server events;
5. complete generated-message and Tibia-owned QMeta/runtime classification registries with quantitative coverage;
6. reconcile the active task checklist on the final exact head, run audit/CI/PR hygiene, merge/archive only when all applicable acceptance is terminal and policy permits.

## Canonical continuation references

- `20260814-chatgpt-continuation-handover.md`
- `experiments/EXP-20260814-continuation-state.yaml`
- `20260814-protocol-queue-action-builders.md`
- `20260814-protocol-queue-network-handoff.md`
- `20260814-live-structural-world-and-reversible-movement.md`
- `README.md`
