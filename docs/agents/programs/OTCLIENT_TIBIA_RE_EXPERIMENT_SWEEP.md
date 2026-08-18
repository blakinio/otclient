# OTCLIENT-TIBIA-RE official-client capability experiment sweep

```yaml
programme: OTCLIENT-TIBIA-RE
track: official-client-re
subject: official native Linux Tibia client only
repository: blakinio/otclient
run_scope: autonomous_program
decomposition_decision: discovery_first
persistence_required: true
ocr_role: bootstrap_or_visual_cross_check_only
```

## Purpose

This document is the durable research design for broad capability discovery in the official native Linux Tibia client. It extends, but does not replace, the canonical programme contracts under `docs/agents/prompts/OTCLIENT_TIBIA_RE_*.md`.

The objective is to determine experimentally what useful game state, server/world information, UI model state and semantic actions can be observed, correlated or invoked without OCR and without screen-coordinate clicking, and to turn proven findings into a normalized future Agent Game API.

All live-state, authorization, repository, safety, runner and track-isolation rules from the canonical Track A programme remain authoritative. Never use Windows/Wine/Proton/macOS/mobile/browser clients as evidence.

## Mandatory startup and login gate

Before any capability experiment, the worker must read the current trusted Track A contracts, inspect live `main`, active tasks, open/closed/superseded Track A PRs, runner ownership and current client identity, then resolve the current approved login/recovery path from repository evidence.

Login is phase `-1` and a hard precondition:

1. Use the current repository-approved official native-Linux login/recovery path; do not invent a second flow if an existing one can be recovered or reused.
2. Historical PR/workflow paths are evidence leads only unless they are current/live.
3. Start the official client normally. GDB-from-start is not the preferred world-entry path.
4. Use authorized account secrets only through the existing approved workflow/runtime mechanism. Never print, persist, copy or expose secret values.
5. Verify the required WARP/proxy/tunnel confinement when the active task requires it before secret use.
6. UI/image differencing may be used only to bootstrap login or character activation. It is not semantic proof.
7. Do not start capability experiments until `IN_GAME` is proven structurally from decoded GameState/worldmap/session evidence.
8. After every restart/relogin reacquire PID, PIE base and runtime object instances; never reuse transient addresses.
9. A disconnect is a recovery event, not a programme stop condition. Persist the current experiment result, recover through the approved path, reacquire runtime state and continue.

## Research model

For each feature, attempt to correlate four layers:

```text
USER / WORLD / SERVER EVENT
        |
        v
UI/controller/runtime method
        |
        v
runtime model/state mutation
        |
        v
protocol message / handler
```

For inbound information reverse the direction:

```text
protocol message
    -> deserializer/handler
    -> runtime model/event
    -> UI/chat/status representation
```

A hit in one layer is a lead, not automatically semantic proof.

## Experimental method

Prefer differential experiments:

```text
baseline A
-> exactly one bounded operation or server/world stimulus
-> observation B
-> structural delta
-> reverse operation or natural recovery
-> observation C
-> repeat
-> negative control
-> restart/ASLR control when appropriate
```

Whenever practical use:

- control 0: no action, prove candidate does not change randomly;
- control 1: repeat same action at least three times;
- control 2: perform inverse action, e.g. east/west, open/close, attack/cancel;
- control 3: change unrelated state and prove candidate remains stable;
- control 4: restart client and rediscover candidate dynamically;
- control 5: logout/relogin and revalidate semantic identity;
- control 6: use another instance of the same semantic object, e.g. second creature/container.

Preferred discovery tools where supported by evidence and repository policy include RTTI, vtables, Qt metaobjects, protobuf descriptors/type names, stable strings/xrefs, relocations, call relationships, semantic signatures, heap-object correlation, differential memory observation, passive tracing, syscall/socket correlation, watchpoints/breakpoints, the stable LD_PRELOAD bridge, protocol ingress/egress tracing and object lifetime analysis.

Do not bypass security controls or attack server infrastructure.

## Evidence gates

```text
G0 STRUCTURAL OBSERVATION
  deterministic state read without causing a gameplay action

G1 PASSIVE CORRELATION
  runtime object/event correlated with protocol/handler or known state transition

G2 REVERSIBLE ACTION PROOF
  harmless semantic action produces expected structural client/server result

G3 BOUNDED MUTATING ACTION PROOF
  safe state-mutating action produces server/client-confirmed result

G4 STABLE BRIDGE/API
  repeatable capability without OCR, pixel clicking or ad-hoc debugger injection,
  with dynamic rediscovery after restart/ASLR
```

Every capability records the highest achieved gate.

## Experiment record schema

Every material experiment must be indexed durably with at least:

```yaml
experiment_id:
date:
objective:
hypothesis:
client:
  version:
  sha256:
runtime:
  runner:
  process:
  pid:
  pie_base:
preconditions:
baseline_state:
action_or_stimulus:
candidate_runtime_objects:
candidate_functions:
candidate_messages:
expected_structural_delta:
observed_structural_delta:
negative_control:
repeatability:
restart_test:
evidence:
  repository_paths:
  run_ids:
  artifact_ids:
  signatures:
  addresses_as_version_fenced_leads:
result: PROVEN | DERIVED | DISPROVEN | INCONCLUSIVE
confidence_boundary:
new_capabilities:
rejected_hypotheses:
next_action:
```

## Capability matrix

Maintain or extend the canonical Track A capability matrix rather than creating duplicate registries. At minimum track:

| Capability | Feature group | Read source | Runtime owner | Inbound message | Outbound action | Semantic fields | Authority | Resolver | Restart proven | Evidence gate | Experiment IDs | Status | Current client SHA | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Statuses: `PROVEN`, `DERIVED`, `UNKNOWN`, `CONFLICT`, `DISPROVEN`, `BLOCKED`.

Authority classification should use: `SERVER_AUTHORITATIVE`, `CLIENT_DERIVED`, `CLIENT_ONLY`, `STATIC_METADATA`, `UNKNOWN`.

# Experiment groups

## P0 — runtime/session/player/world/combat core

### 0. Exact runtime identity

Establish exact client version/SHA256, ELF metadata, PID, PIE base, loaded libraries, current bridge compatibility, session/protocol objects and structural `IN_GAME` state before current-version claims.

### 1. Session state machine

Attempt to distinguish structurally: process started, login screen, authenticating, character selection, connecting game server, pending game, entering world, `IN_GAME`, connection lost, logout and recovery. Seek semantic events such as `LoginStarted`, `LoginSucceeded`, `CharacterSelected`, `WorldSessionStarted`, `WorldSessionEnded`, `ConnectionLost` and a non-OCR `session.is_in_game()`.

### 2. Player core state

Find and correlate where safely possible: character ID, name, vocation, level, experience, XP progress, HP/max HP/%, mana/max mana/%, capacity, soul, speed/base speed, position X/Y/Z, direction, outfit, mount state, stamina, premium/account state when exposed, blessings information and other current-client state.

HP/mana candidates require controlled changes rather than visual matching alone: baseline -> harmless damage/heal or safe mana expenditure/regeneration -> structural delta -> repeat/control.

### 3. Skills and combat statistics

Investigate magic level and all current vocation/weapon/support skills, base vs effective values, loyalty-modified values if separately represented, progress percentages and client-exposed combat statistics.

### 4. Conditions, buffs and debuffs

Map condition IDs and lifetimes where available for haste, paralyze, poison, fire, energy, bleeding, drunk, PZ lock, logout block, invisibility, mana shield and current-client equivalents. Find collection ownership, source messages, icons and expiry information if the client knows it.

### 5. Cooldowns and exhaustion

Map spell cooldowns, cooldown groups, item/rune cooldowns where represented, action exhaustion, attack delay, start/end events and remaining time. Use safe ready -> cast/use -> cooldown starts -> countdown -> cooldown ends experiments.

### 6. Map/tile model

Expand the existing worldmap work to identify X/Y/Z, stack order, ground, items, creatures, effects/projectiles, appearance/type identifiers, count/subtype, elevation, blocking, pathability/walkability, usable/movable/pickupable/container flags, doors, stairs/ramps/floor transitions, magic fields and relevant zone flags where stored.

### 7. Viewport, cache and minimap

Separate currently rendered viewport from decoded known world, neighboring/floor cache and minimap/cache persistence. Measure exact coordinate coverage and test persistence after leaving area, relog and restart. Determine whether the runtime knows more than the visible viewport.

### 8. Creature registry

Seek a central `CreatureStorage`/registry. Correlate creature ID, name, position/floor, direction, HP%, player/monster/NPC class, outfit/mount/light, speed, skull/shield/party state, targetability, visibility, summon/master relationship when present, and appear/move/update/disappear lifecycle.

### 9. Battle list

Determine whether battle list is a view/filter over CreatureStorage or a separate/server-derived model. Test sorting/filtering without changing world state. Map entries, sort keys, selected/attacked/followed creature, health, distance/floor filtering and hidden/offscreen behavior.

### 10. Combat targeting

With safe targets only, correlate select/attack/switch/cancel/follow/cancel-follow and target disappearance/death/offscreen/floor changes across semantic action, outbound message, runtime state and server-confirmed structural result.

### 11. Combat modes

Map stand/chase, offensive/balanced/defensive if present, secure mode and PvP options. Determine local-only vs protocol-mutating behavior.

### 12. Equipment

Discover current slots and item state: slot ID, item/appearance/type IDs, count/subtype, tier, imbuement, duration/expiry and charges. Prefer harmless reversible swaps and generic equipment-change events.

### 13. Containers

Map open-container registry, IDs, names/types, parents, slots, capacity, page/index, pagination, nested containers, insertion/removal/stack updates, close/up/seek and multiple simultaneous containers. Determine ID lifetime across reopen/relog.

### 14. Item manipulation

Using nonvaluable reversible targets only, map move within/between containers/inventory, stack split/merge, use, use-with, use-on-creature, rotate/open/browse-field where supported. Never guess a mutating ABI.

### 15. Quick loot and loot state

Read-only first: quick-loot configuration, assigned loot containers, corpse interaction state, loot messages and item-transfer events. Do not interfere with another player's loot.

## P0/P1 — inbound world/server event intelligence

### 16. Central inbound event intelligence

This is a first-class objective, not merely a chat subtask.

Determine whether all or many server-originating events converge on a common inbound dispatcher. Build a passive logger, where safe, that correlates:

```text
timestamp
message type / protobuf type / opcode family
message size when available
handler
runtime object/model changed
semantic event classification
UI/chat/status representation
```

Unknown incoming messages must not be dropped. Record them as `UnknownIncomingEvent` with enough version-fenced evidence to classify later.

Target a normalized event stream equivalent to:

```text
PlayerHealthChanged
PlayerManaChanged
PlayerPositionChanged
CreatureAppeared
CreatureMoved
CreatureHealthChanged
CreatureDisappeared
TileChanged
ItemAdded
ItemRemoved
ContainerOpened
ContainerChanged
ContainerClosed
ChatMessageReceived
TargetChanged
CooldownStarted
CooldownFinished
SystemNotification
WorldEventStarted
WorldEventUpdated
WorldEventEnded
ConnectionStateChanged
ActionRejected
UiModelUpdated
```

### 17. Server/system/world announcements

Capture and classify all information that reaches the client from the world/server even when it does not immediately mutate map state, including where current-client evidence permits:

- server/system messages;
- server-save warnings;
- restart/shutdown/maintenance warnings;
- forced-logout or session-expiry warnings;
- connection lost/reconnecting/kicked state;
- world/raid/event start, update and end announcements;
- boss/event announcements;
- quest/progress notifications;
- reward/prey/bestiary/forge notifications;
- PvP/skull/PZ/status notifications;
- action errors such as not possible, exhausted, out of range/reach;
- combat/loot/XP/damage/healing notifications;
- social/party/guild/VIP notifications when structurally exposed.

Classify into a durable taxonomy, e.g. `CHAT`, `SYSTEM`, `WARNING`, `WORLD_EVENT`, `RAID`, `SERVER_SAVE`, `MAINTENANCE`, `CONNECTION`, `COMBAT`, `LOOT`, `QUEST`, `SOCIAL`, `PARTY`, `GUILD`, `NPC`, `TRADE`, `MARKET`, `CYCLOPEDIA`, `REWARD`, `ERROR`, `ACTION_REJECTED`, `OTHER`.

Do not assume every event is text-only. For each important message determine whether the client receives structured IDs, timers, severity, start/end times, actor/target IDs, positions, reason codes or other fields before formatting text.

Target normalized structures such as:

```text
SystemNotification {
  type,
  severity,
  remaining_seconds,
  text,
  source_message
}

WorldEvent {
  category,
  event_id,
  state,
  starts_at,
  ends_at,
  text,
  source_message
}
```

Only fields proven to exist should be promoted to the API.

### 18. Chat messages and channels

Map incoming/outgoing local say, NPC speech, whisper, yell, private messages, channel messages, system/status/loot/combat messages. Seek a structured `ChatMessage{type,author,text,channel,timestamp?,position?}`. Prefer self/NPC/system-safe tests and never message random players.

Map open channels, IDs/names, selected channel, unread markers, open/close actions and private-conversation state. Determine whether channel operations cause server requests.

### 19. Connection and imminent logout intelligence

Specifically test the client signals/models/messages that indicate imminent logout, forced logout, server restart/save, disconnect, reconnect and session invalidation. Determine whether a timer/reason code exists structurally or only formatted text is available.

This capability is high priority for an autonomous agent because it should be able to checkpoint, stop risky actions and recover before/after session loss.

## P1 — NPC, interaction and semantic UI/control

### 20. NPC conversation

Use safe NPC interactions. Correlate visible NPC -> talk -> response -> conversation window/model -> option selection. Determine whether modern dialog options carry semantic IDs/action IDs or are text-driven.

### 21. NPC trade

Read-only first. Extract NPC identity, offer rows, item IDs/names, buy/sell price, amount, weight/subtype, owned count, selected row, amount selector and available actions. Only consider a tiny harmless transaction after ABI and cost/reversibility are proven. Never buy valuable items for proof.

### 22. Depot/inbox/stash

Read-only first. Investigate depot, inbox, stash, store inbox and locker hierarchy, search and counts. Avoid destructive transfers.

### 23. General UI semantic model

Investigate whether the runtime can structurally query open windows, active modal, focused widget, active tab/page, selected row, list models, action/button IDs, enabled state and confirmation dialogs. Do not attempt to reproduce the GUI toolkit; expose only useful semantic UI state.

### 24. Context menus

For ground, item, container, NPC, monster, player and self, map available semantic actions such as Look, Use, Open, Browse Field, Attack, Follow, Trade With, Message To, Add To VIP and current equivalents. Goal: `context_actions(target) -> SemanticAction[]` without pixel coordinates.

### 25. Look/inspect

Correlate look-at tile/item/creature requests and replies; determine whether structured identifiers accompany displayed text.

### 26. Action bars/hotkeys

Map action bar entries, assigned spell/item, hotkey, target mode, amount/subtype, cooldown overlay and enabled state. Determine whether invocation converges on generic semantic use/cast methods.

### 27. Outbound action bus

High priority: determine whether movement, combat, item use, chat, container and other actions converge on one or a few common dispatch chains such as user intent -> game action -> generated `GameclientMessage` -> serializer -> transport. A common outbound dispatcher may collapse many separate action-RE tasks into one stable semantic layer.

## P2 — Cyclopedia and character systems

### 28. Cyclopedia shell

Map open/close, tab/page IDs, navigation, requests/responses and reusable controller/model objects before individual feature pages.

### 29. Bestiary

Investigate race/monster IDs, names/categories, kills/requirements/stages, difficulty/occurrence if received, charm points, loot unlock/entries, selected creature and search/filter state. Test closed -> open -> category -> creature A -> creature B -> close and determine local/static vs on-demand vs cached data.

### 30. Charms

Read-only first: available points, unlocked charms, assignment/target race, costs and active state. Do not spend/remove charms just for proof.

### 31. Bosstiary/boss systems

If current client supports them, map boss IDs, kills/progress, unlocks, slots, selected boss and bonuses/rewards with same cache/on-demand analysis.

### 32. Wheel of Destiny

High priority, read-only/preview first. Map vocation, available/spent points, node/slice IDs, node level/max/cost, prerequisites, unlocked state, perk/revelation IDs, stage, active configuration, presets/loadouts if present, selected node, preview state and apply/confirm message.

Perform closed -> open -> select A -> select B -> preview without commit -> close. Separate local static definitions, character-specific response data and server-committed configuration. Do not spend/reset points merely for research.

### 33. Exaltation Forge

High priority, read-only/preview first. Map dust/limit, slivers, cores, history, item classification/tier, fusion/transfer/convergence eligibility, costs/probabilities, selected source/target and preview/confirmation state. Determine request/response types per screen. Do not fuse/transfer/destroy valuable equipment for evidence.

### 34. Imbuements

Read-only first: slots, active imbuements, IDs/tiers, duration/remaining time, costs/materials, selected item/slot. Avoid consuming resources.

### 35. Prey

Read-only first: slots, creature/race ID, bonus type/strength, remaining time, reroll/free-reroll state, prices and cards if represented. Do not spend cards/gold for proof.

### 36. Daily reward/reward state

Map reward calendar/model, streak, next/claimable reward and request/response state. Do not consume strategically important rewards just for proof.

### 37. Market

Read-only. Map query request/response, item/category search, IDs, buy/sell offers, amount/price, history/statistics, pagination, filters/sort, selected offer and displayed balance if part of the model. Do not create or accept offers for proof.

### 38. Store

Read-only unless separately authorized. Map categories, products/product IDs, displayed coin balances and preview/selection. Never purchase anything for an experiment.

### 39. Quest log

Map quest IDs/names, missions, state/descriptions/completion, selected entry and cache/request-on-open behavior.

### 40. Achievements, titles and character info

Where exposed, map achievements, titles, character inspection, outfits, mounts, familiars and unlocked cosmetics. Separate static metadata from character-specific server state.

## P3 — social and analytics

### 41. VIP/contacts

Read-only preferred. Map player GUID/name, online state, groups, icons, descriptions, notifications and semantic add/remove/update handlers. Do not contact or modify unrelated users for proof.

### 42. Party/social state

Safely observe party membership, leader/member IDs, shared-exp state, invites and shield indicators. Do not invite random players.

### 43. Analyzers

Investigate Hunt/Loot/Supply/Damage/Input/Impact/XP/session analyzer models. Classify which totals are locally derived from game events vs received from server. These may expose already-normalized telemetry useful for agents.

## Cross-cutting discovery

### 44. Protocol descriptor census

Enumerate useful generated message/protobuf descriptors and cluster them by session, movement, map, creature, inventory, combat, chat, market, Cyclopedia, Bestiary, Wheel, Forge, prey, store, quest, social and unknown families. Descriptor presence is `DERIVED` until observed live.

### 45. Data lifetime/cache

For map, Bestiary, Wheel, Forge, Market and other rich features test before first open, after open, after close/reopen, after logout/relog and after restart. Classify static binary metadata, process cache, per-session data and per-request data.

### 46. Local vs server authority

For every important field classify authority experimentally. Examples include HP/mana, creature position, cooldown, battle ordering, analyzer totals, Wheel definitions, Bestiary metadata and UI filtering.

### 47. Stability and ASLR

Any important `PROVEN` capability should be rerun after client restart with changed PID/PIE base. No important capability should permanently depend on one heap address.

### 48. Client update resilience

For important discoveries create semantic resolvers using RTTI, vtable identity, descriptors, stable strings/xrefs, call patterns, relocations and structural invariants. Record exact-version proof separately from proposed rediscovery method. Never claim cross-version compatibility until a second version proves it.

### 49. Agent Game API candidate

Maintain a proposed normalized API, but never implement speculative methods. Candidate surface may include:

```text
session.state()
session.is_in_game()
player.state()
player.position()
player.conditions()
player.cooldowns()
world.visible_tiles()
world.tile(x,y,z)
world.creatures()
events.stream()
combat.target()
combat.attack(id)
combat.follow(id)
combat.cancel()
inventory.equipment()
containers.list()
containers.items(id)
chat.messages()
chat.say(text)
npc.trade_state()
cyclopedia.bestiary()
wheel.state()
forge.state()
ui.semantic_state()
```

Each API candidate must be tagged `PROVEN_READ`, `PROVEN_ACTION`, `DERIVED`, `UNKNOWN` or `UNSUPPORTED`.

### 50. Creative discovery pass

After obvious groups, perform a bounded sweep for high-value capabilities not listed here by inspecting descriptors, strings, handlers, model/controller classes and unknown message families. Examples worth checking when present include party/team finders, stash/supply management, reward systems, boss systems, inspection, combat statistics, imbuement timers, item tier/classification, zone/area flags, notifications, death/respawn state, modal decision state, latency/ping, pathfinder/auto-walk path, minimap marks, selected/hovered thing and client-side visibility calculations.

Do not treat this list as exhaustive.

# Prioritization

```text
P0: login/session, player position, HP/mana, map, creatures, battle target,
    combat actions, inventory/containers, inbound event intelligence, chat,
    common inbound/outbound dispatchers

P1: conditions, cooldowns, NPC/trade, context menu, skills, analyzers,
    action bars, semantic UI state

P2: Bestiary, Charms, Bosstiary, Wheel, Forge, Imbuements, Prey,
    Market, Quest Log

P3: social/store/cosmetic/nonessential UI
```

Exploit high-value common-dispatch discoveries opportunistically even if they arise from a lower-priority feature.

# Non-destructive/no-cost boundary

Default experiments must not lose valuable items, destroy equipment, spend Tibia Coins, spend substantial gold, spend charm/prey/forge resources, reset valuable character configuration, disturb unrelated players, create market transactions or cause account risk.

Use read-only/preview states wherever possible. If proof requires a costly or irreversible action, mark `BLOCKED_REQUIRES_OWNER_AUTHORIZATION` and continue with other READY work.

# Durable persistence contract

No material discovery may exist only in chat, terminal output, runner filesystem or an unindexed Actions artifact.

After every material result update/reuse the canonical durable state, including as applicable:

1. active Track A task checkpoint;
2. capability matrix;
3. experiment index with stable IDs;
4. rejected/disproven hypotheses;
5. exact current-version profile and resolvers;
6. protocol catalogue;
7. action catalogue;
8. World/Server Event Intelligence catalogue/taxonomy;
9. evidence/run/artifact index;
10. exactly one executable `next_action` while incomplete.

Large traces, binaries, screenshots or dumps should not be committed when policy/licensing/privacy forbids it; persist hashes, semantic results, run/job/artifact identifiers and provenance instead.

# Anti-stall rule

Do not spend an entire worker session perfecting one uncertain offset. After bounded failures, record the hypothesis/result, try one materially different method, then move to another READY capability and preserve the blocker. A disproven hypothesis is progress.

# Desired end state

A future agent should be able to consume a structural model conceptually equivalent to:

```text
GameState {
    session
    player
    world
    creatures
    combat
    inventory
    containers
    cooldowns
    chat
    server_world_events
    npc_trade
    bestiary
    wheel
    forge
    ui
}
```

receive an event stream conceptually equivalent to:

```text
PlayerHealthChanged
PlayerManaChanged
PlayerMoved
CreatureAppeared
CreatureMoved
CreatureHealthChanged
TargetChanged
ContainerChanged
ChatMessageReceived
SystemNotification
WorldEventStarted
ServerSaveWarning
ConnectionStateChanged
ActionRejected
CooldownChanged
UiModelChanged
```

and invoke proven semantic actions such as movement, turn, stop, attack, follow, use/use-with, move item, open/close/navigate container, talk and safe NPC trade operations without OCR or coordinate clicking.

## Specialized monster spawn/mechanics subprogramme

For P0 map/viewport/creature/battle/combat observations and related inbound events, use the specialized child programme when the research objective is monster spawn reconstruction, respawn timing or empirical monster mechanics:

```text
docs/agents/programs/OTCLIENT_TIBIA_RE_MONSTER_SPAWN_MECHANICS.md
docs/agents/contracts/MONSTER_OBSERVATION_V1.md
docs/agents/contracts/MONSTER_OBSERVATION_V1.schema.json
docs/agents/prompts/OTCLIENT_TIBIA_RE_MONSTER_SPAWN_MECHANICS_ALIAS.md
```

A raw creature-create/add event remains only an observed appearance until the child programme's continuous-coverage, epoch, terminal/death, repetition and negative-control gates are satisfied. The child programme keeps observed creation tiles, inferred spawn regions and unknown server-side spawn/home rules separate, and keeps empirical behavior distinct from unproven server algorithms.

Large observation streams remain sanitized artifacts with repository-indexed provenance. Physical evidence is serialized through current Track A RUNTIME ownership and at most the one legal canonical logged-in session by default; offline spawn/mechanics inference remains GitHub-hosted `runtime_access: none`.

# Final worker response

When a bounded invocation actually stops, return a compact status only after durable repository state is current:

```text
STATUS:
CURRENT_CLIENT:
REPOSITORY_HEAD:
TASK:
PR:
NEW_PROVEN:
NEW_DERIVED:
DISPROVEN:
BLOCKED:
UNKNOWN:
EXPERIMENTS_COMPLETED:
CAPABILITY_MATRIX:
EVIDENCE_INDEX:
VALIDATION:
DURABLE_STATE:
NEXT_ACTION:
```
