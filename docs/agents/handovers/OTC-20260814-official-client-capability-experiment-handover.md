# Track A official-client capability experiment handover

```yaml
programme: OTCLIENT-TIBIA-RE
track: official-client-re
repository: blakinio/otclient
status: RESEARCH_DESIGN_READY_FOR_VALIDATION
source_of_truth: live repository + retained GitHub Actions evidence
execution_contract: docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
```

## Purpose

This handover preserves the current Track A design and exact evidence boundary for extracting useful semantic state, events and actions from the official native Linux Tibia client without OCR or screen-coordinate clicking as the normal interface.

It is a continuation aid, not proof that the runtime capabilities already work. Static binary evidence remains `STATIC_PRESENT` until the current exact client version is revalidated and promoted through the read/action evidence gates.

## Normative document set

Read together:

```text
docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
docs/agents/reports/OTCLIENT-20260814-official-client-experiment-design-review.md
```

Where execution order/evidence methodology differs, the execution model controls. Repository safety/authorization and the canonical programme remain more authoritative.

## Lifecycle

PR #293 is a **research-design deliverable**. It does not execute the entire capability sweep.

After PR #293 is merged:

1. archive the design task;
2. resume the canonical `OTCLIENT-TIBIA-RE` programme;
3. execute bounded hypotheses/phases with durable experiment records;
4. rotate worker context rather than turning the design task into a permanent catch-all owner.

## Exact researched binary evidence

Retained successful inventory evidence for the historical exact official Linux client:

```text
client version: 15.32.df7b29
client SHA256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

Important retained runs:

```text
protocol inventory
  run: 31651220862
  job: 94295767215
  total generated message symbols: 349
  client -> server: 160
  server -> client: 189
  old capability-regex matches: 98
  unclassified-by-old-regex: 251

capability QMeta inventory
  run: 31651155741
  job: 94295569820
  capability method hits: 494
  direct QMeta dispatch targets: 460

high-level action inventory
  run: 31651684700
  job: 94297172395
  HIGHLEVEL_ACTION_METHOD_COUNT=612

state/update inventory
  run: 31652393473
  job: 94299386259
  targeted hits: 121

action signature inventory
  run: 31651501473
  job: 94296624884
```

The older value `1004` for high-level action methods is not the direct marker from run `31651684700`; treat it as a different historical filter/count definition unless its provenance is reconstructed.

## Static surfaces already evidenced

The exact researched binary exposes named leads for, among others:

- session/authentication/world-entered/disconnect/death/server modal state;
- player data, HP/max HP, mana/max mana, skills, capacity, soul, resting/player state and cooldowns;
- all cardinal/diagonal movement, path, stop/cancel and rotation;
- CreatureStorage, creature health/outfit/speed/skull/party/type/light/marks and HUD status;
- battle lists, selected targets, attack and follow;
- inventory, object counts and semantic appearance metadata;
- containers, pagination, stash, depot search, managed containers and Quick Loot;
- chat/channel/private/NPC channel state and talk actions;
- player-to-player trade models/controllers;
- NPC trade storage/controller;
- party/shared-experience lead (`sendShareExperience` + inbound creature-party state);
- Cyclopedia/Bestiary/Bosstiary/monster bonus effects;
- Skill Wheel/gems/presets;
- Exaltation Forge fusion/transfer preview surfaces;
- Prey, Taskboard/Bounty/Weekly/Soul Seals;
- Imbuements and Weapon Proficiency;
- Market, Houses, Quest Log, Reward Wall/Daily Reward;
- Friends/VIP/Social;
- action bars/hotkeys/passive abilities/multi-actions;
- analyzers: Loot, Waste, Impact, Damage Input, Hunting Session, Progress, Analytics Selector, Party Hunt;
- network dual-connection state and FPS/latency controller;
- sound/event cue storages;
- minimap/world-map transforms and markers;
- generic dialog/sidebar/modal/controller state;
- `tibia::sessiondump::*` as a passive replay-feasibility lead only.

Static presence is not a live API and is not permission to invoke mutating actions.

## High-value semantic item metadata lead

The exact binary exposes `TAppearanceTypeHelperQmlService` methods equivalent to:

```text
appearance ID -> item name
appearance ID -> item description
item name -> appearance ID
```

This should be tested early because it may allow structural object naming without OCR or external item tables.

## Required execution order

Do not log in before static work that does not need a session.

```text
S0
resolve current official Linux client version/SHA and binary provenance

S1
exhaustively enumerate all generated messages and all Tibia-owned QMeta/runtime types
without feature-name filters

S2
classify and graph:
GeneratedMessage -> ProtocolMessageQueue -> handler -> storage -> controller/model
and the outbound inverse; rank high-information probes

--------- LIVE BOUNDARY ---------

L0
resolve current approved Track A login/recovery path
login through the authorized mechanism
structurally prove IN_GAME
create a new session_epoch

L1
instrument competing inbound/outbound dispatcher hypotheses
establish no-stimulus background baseline
start causal recorder

L2
promote core reads: position, HP/mana/player state, map, creatures,
inventory/containers, chat/world events

L3
promote core actions with normal-client reference parity and server-confirmed results

L4
party/player trade/NPC trade/cooldowns/quick loot/analyzers/context/action bars

L5
rich read/preview systems: Bestiary/Wheel/Forge/Prey/Market/etc.

L6
fresh PID/ASLR/relogin rediscovery, stable bridge and update-resilience validation
```

## Dispatcher hypotheses

Do not assume one common dispatcher merely because it would simplify the bridge.

Inbound candidates to falsify:

```text
H-IN-1 TProtocolMessageQueue is the central semantic spine
H-IN-2 queue fans out; family handlers/storages are the real semantic boundaries
H-IN-3 multiple materially independent lanes exist
```

Outbound candidates:

```text
H-OUT-1 one common action spine
H-OUT-2 several family action spines
H-OUT-3 important features require independent paths
```

Preserve negative results.

## Causal evidence requirement

Live before/after proximity is not enough in a continuously changing game session.

Use evidence equivalent to:

```text
session_epoch
monotonic timestamp
stimulus_id
message direction/type/sequence
connection lane
thread
handler/runtime object
before_state_hash
after_state_hash
normalized semantic delta
```

Capture a bounded no-stimulus baseline for important new probes so natural regen/movement/timer/chat traffic does not become a false correlation.

## Read/action maturity

Track independently:

```text
R0 STATIC_PRESENT
R1 LIVE_READ
R2 CAUSAL_READ
R3 RESTART_STABLE_READ
R4 BRIDGE_READ

A0 STATIC_PRESENT
A1 REFERENCE_TRACE
A2 ABI_MESSAGE_PROVEN
A3 SERVER_CONFIRMED_ACTION
A4 BRIDGE_ACTION
```

A readable feature may remain action-unsupported. Do not imply action support from read maturity.

## Action reference-path parity

Before A3/A4 promotion:

```text
normal official-client action
-> normalized outbound semantic message
-> authoritative result

programmatic candidate action
-> normalized outbound semantic message
-> authoritative result
```

Semantic message fields/results must match or differences must be explained. Transport sequence/timing/framing may differ.

## Exhaustive census expectations

For every generated protocol message extract where resolvable:

- name/direction/namespace;
- field numbers, names and types;
- cardinality/oneof/enum values;
- nested messages;
- serializer/deserializer;
- protocol queue method;
- handler;
- feature family or explicit `UNCLASSIFIED`;
- first live experiment;
- current-client SHA.

For runtime/QMeta census preserve methods/signals/properties and dependency relationships rather than only a flat list.

## Machine-readable durable state

Future execution must create/reuse one canonical Track A evidence root containing logical datasets equivalent to:

```text
capabilities.jsonl
protocol_messages.jsonl
runtime_types.jsonl
experiments/<experiment_id>.yaml
```

Search existing conventions first; do not create duplicate evidence roots.

Human-readable Markdown summarizes the result. Large/raw traces remain referenced artifacts when policy requires.

## Quantitative coverage

Track at least:

```text
protocol_message_classification_pct
qmeta_type_classification_pct
p0_capabilities_with_experiment_pct
p0_reads_terminal_pct
p0_actions_terminal_pct
unknown_inbound_count
unclassified_runtime_type_count
restart_validated_capability_count
```

Every generated message/runtime census entry must be classified or explicitly unclassified/ignored-with-reason. Every P0 capability needs an experiment or explicit blocker/unsupported rationale.

## World/Server Event Intelligence

Treat incoming information as first-class state, not a chat footnote.

Target families include:

- server/system messages;
- server-save/restart/shutdown/maintenance warnings;
- forced logout/session invalidation;
- disconnect/reconnect/kick/death/modal state;
- raid/world-event/boss announcements;
- action rejection/errors;
- private/channel/NPC messages;
- combat/damage/heal/XP/loot notifications;
- quest/reward/prey/bestiary/forge notifications;
- social/party/guild/VIP notifications;
- every unknown inbound family.

For rare events use:

```text
STATIC_REACHABLE
LIVE_OBSERVED
REPLAY_CONFIRMED
NOT_OBSERVED
```

Do not keep workers waiting for a naturally rare event. Investigate sessiondump only as a safe deterministic replay lead.

## Privacy boundary

Do not commit raw unrelated-player private messages or unnecessary player identity data.

Prefer normalized/redacted evidence:

```text
message type
channel/type ID
length
flags
hashed/anonymized actor when needed
sequence/time metadata
semantic fields
```

Plain text is limited to owner/test/NPC-generated experiment content or explicitly redacted evidence. Never commit credentials, auth/session tokens, cookies or secret-bearing traces/screenshots.

## Safety boundary

Default live tests to read-only/reversible/no-cost.

Do not for proof alone:

- spend Tibia Coins or substantial gold;
- destroy/fuse/transfer valuable equipment;
- spend/reset Forge/Charm/Prey/Wheel resources;
- create Market purchases/offers;
- risk valuable items in trade;
- disturb unrelated players;
- bypass anti-cheat/client checks;
- consume owner-funded AI quota without explicit permission for that exact use.

Use `BLOCKED_REQUIRES_OWNER_AUTHORIZATION` when an otherwise useful proof requires a larger irreversible/cost budget.

## Exact next programme action after design merge

```text
1. Resolve the current official Linux client binary/version/SHA.
2. Execute S1 exhaustive generated-message census without regex filtering.
3. Execute S1 exhaustive Tibia-owned QMeta/runtime census.
4. Build S2 dependency graph and machine-readable registries; classify all entries.
5. Rank P0 probes by information gain.
6. Only then resolve live runner/login ownership, enter the world through the approved path and structurally prove IN_GAME.
7. Start L1 with competing inbound/outbound topology hypotheses plus the causal/noise recorder.
8. Promote player position + HP/mana + map + CreatureStorage + inventory/containers + chat/world events first.
9. Persist every material experiment and exactly one continuation action.
```
