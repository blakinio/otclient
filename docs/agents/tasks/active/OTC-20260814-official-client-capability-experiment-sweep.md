# OTC-20260814 — official-client capability experiment sweep

```yaml
task_id: OTC-20260814-official-client-capability-experiment-sweep
programme: OTCLIENT-TIBIA-RE
track: official-client-re
status: ready
repository: blakinio/otclient
base_branch: main
branch: docs/OTC-20260814-official-client-capability-experiment-sweep
owned_paths:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
  - docs/agents/tasks/active/OTC-20260814-official-client-capability-experiment-sweep.md
modules_touched: []
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - existing Track A stable runtime bridge and relocation resolver as live state permits
depends_on:
  - current approved Track A native-Linux runner/runtime/login path resolved from live repository state
blocks: []
run_scope: autonomous_program
decomposition_decision: discovery_first
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: internal_only
```

## Objective

Execute a broad, evidence-driven capability discovery sweep against the exact current official native Linux Tibia client and determine what game state, server/world events, UI model state and semantic actions can be exposed structurally without OCR or screen-coordinate clicking.

The normative experimental design for this task is:

```text
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
```

This task extends the canonical `OTCLIENT-TIBIA-RE` programme. It does not replace Track A governance or create a second reverse-engineering lane.

## Why this task exists

The existing Track A programme already covers session state, map, creatures, inventory/containers, movement, attack/follow, use/move-object, chat, protocol mapping, OTBM feasibility and a stable bridge. The new sweep broadens that work into a systematic whole-client experiment programme, including:

- player HP/mana/stats/skills/conditions/cooldowns;
- battle list and combat modes;
- equipment, inventory, containers, item manipulation and quick loot;
- chat/channel/NPC interaction and NPC trade;
- semantic context menus, action bars and useful UI model state;
- Cyclopedia, Bestiary, Charms, Bosstiary, Wheel of Destiny and Exaltation Forge;
- imbuements, Prey, rewards, Market, Store, Quest Log and character information;
- VIP/party/social state and analyzer telemetry;
- protocol descriptor census, cache/lifetime studies and update-resilient resolvers;
- central inbound event-dispatch and outbound action-dispatch discovery;
- a first-class World/Server Event Intelligence layer for announcements, events, server-save/restart/logout warnings, connection state, action errors, combat/loot/XP notifications, private messages and other information reaching the client.

## Hard login precondition

No capability experiment may start until the worker has obtained and structurally proven a real official native-Linux world session through the current repository-approved Track A login/recovery path.

The worker must:

1. resolve current `main`, Track A task/PR ownership, runner state and approved login/recovery implementation;
2. treat historical closed/unmerged PR workflows as leads rather than current authority;
3. start the official client normally rather than using GDB-from-start as the preferred login path;
4. use authorized secrets only through the approved workflow/runtime secret mechanism and never expose them;
5. verify required WARP/proxy confinement when applicable;
6. use UI/image differencing only as login/bootstrap assistance;
7. require decoded GameState/worldmap/session evidence for `IN_GAME`;
8. reacquire PID/PIE/runtime objects after every restart/relog;
9. recover and continue after disconnect instead of treating it as completion.

## High-value hypotheses

Prioritize falsifying/proving these hypotheses early:

1. A common inbound dispatcher can expose a large fraction of player/world/chat/system/server events as one event stream.
2. A common outbound action dispatcher can expose movement, attack/follow, use, chat and container actions through one semantic action layer.
3. HP/mana/player/creature/container/cooldown state is already maintained in runtime models and can be read without OCR.
4. Battle List is a filtered/sorted view over a central creature registry rather than a separate truth source.
5. Bestiary/Wheel/Forge/Market and other rich interfaces have structured model/controller or protocol-response state that can be captured before rendering.
6. Server/world announcements and warnings carry structured event/message identity beyond the final displayed text for at least some families.
7. Current runtime state contains more map/cache information than the currently rendered viewport.
8. Existing exact-version semantic resolvers can be generalized enough to survive PID/ASLR changes and provide leads across client updates without claiming unproven cross-version support.

## World/Server Event Intelligence acceptance

This area is P0/P1 and must not be treated as merely a chat subfeature.

The worker must attempt to capture and classify, when naturally/safely observable:

```text
SYSTEM
WARNING
WORLD_EVENT
RAID
SERVER_SAVE
MAINTENANCE
CONNECTION
COMBAT
LOOT
QUEST
SOCIAL
PARTY
GUILD
NPC
TRADE
MARKET
CYCLOPEDIA
REWARD
ERROR
ACTION_REJECTED
CHAT
OTHER
```

Target observations include:

- event/raid/boss announcements;
- server-save/restart/shutdown/maintenance warnings;
- imminent/forced logout and session invalidation;
- connection lost/reconnect/kick state;
- private/channel/NPC/system messages;
- combat, damage, healing, XP and loot notifications;
- quest/progress/reward notifications;
- VIP/party/guild/social notifications;
- action rejection reasons such as exhausted, impossible, unreachable/out of range;
- unknown incoming message families preserved for later classification.

For each important family, determine whether the runtime/protocol exposes structured type/ID, reason, severity, timer, position, actor/target, start/end or similar semantic fields before text formatting. Do not invent fields that cannot be proven.

## Persistence requirements

All material work must be recoverable from `blakinio/otclient` plus explicitly referenced evidence. The worker must update/reuse, not duplicate, the canonical Track A durable state for:

- exact current client version/SHA;
- experiment IDs and results;
- capability matrix;
- rejected/disproven hypotheses;
- protocol catalogue;
- action catalogue;
- event-intelligence catalogue/taxonomy;
- resolvers/signatures and version fences;
- run/job/artifact evidence references;
- blockers/UNKNOWN/CONFLICT state;
- exactly one executable `next_action` while work remains.

No material finding may remain only in chat, terminal output, a transient runner filesystem or an unindexed Actions artifact.

## Safety boundary

Default to read-only or reversible/no-cost experiments. Do not destroy valuable items/equipment, spend Tibia Coins, spend substantial gold or character resources, reset valuable Wheel/Charm/Prey/Forge configuration, create Market transactions, spam/message unrelated players or perform account-risking actions merely for proof.

If a capability requires a costly/irreversible mutation, record `BLOCKED_REQUIRES_OWNER_AUTHORIZATION` and continue other READY work.

No owner-funded Codex/OpenAI API/paid AI quota may be consumed without separate explicit authorization for that exact use.

## Acceptance inventory

This task is not complete merely because the research design exists. A later execution/continuation agent must use it to drive experiments and persist evidence. Programme-level completion remains governed by the canonical Track A prompt.

For this task record itself, acceptance is:

- the broad experiment design is persisted under `docs/agents/programs/`;
- login/recovery is an explicit hard precondition;
- World/Server Event Intelligence is an explicit first-class experiment family;
- the design covers player/world/combat/inventory/chat/NPC/UI/Cyclopedia/Wheel/Forge/Market/social/analytics and cross-cutting protocol/event/action/cache/resilience discovery;
- evidence gates, differential controls, non-destructive boundaries, capability matrix schema and durable persistence rules are explicit;
- a fresh Track A worker can discover this task from `tasks/active/` and continue without this chat.

## Current checkpoint

```yaml
checkpoint_version: 1
created_at: 2026-08-14T09:26:00+02:00
base_main: 005158b5b9bf25fe77bd5fc10813a6388a072836
status: ready
durable_design: docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
proven_by_this_task:
  - research design persisted in repository
  - World/Server Event Intelligence included as first-class target
  - login/recovery hard gate included
runtime_claims_by_this_task: none
unknown:
  - current exact live official-client version/SHA at next experiment
  - current authoritative Track A runtime/login owner at next experiment
  - which listed capabilities will prove structurally extractable on the current client
safe_to_resume: true
next_action: fresh Track A worker must resolve current live repository/runtime/login state, structurally prove IN_GAME on the exact current official Linux client, then start the P0 differential sweep with central inbound dispatcher plus player position/HP/mana/world/creature correlations and persist each experiment result
```
