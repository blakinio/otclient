---
task_id: OTC-20260813-official-client-re-continuation
status: waiting
track_id: official-client-re
alias: OTCLIENT-TIBIA-RE
branch: ci/OTC-20260813-official-client-re-continuation
base_branch: main
pr: 289
task_kind: runtime-research
phase: static-protocol-metadata-mapping
risk: medium
runtime_platform: native_linux_only
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - .github/scripts/tibia-official-client-re-*
  - tests/tools/test_tibia_official_client_re_*.py
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
modules_touched:
  - official-client-re workflow and evidence only
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md
  - PR 283 runtime bridge after exact-SHA validation
depends_on:
  - synology-otclient-01 availability
blocks: []
cross_repository_tasks: []
---

# OTC-20260813 — Official Linux client RE continuation

## Objective

Continue Track A against the official native Linux Tibia client only. Recover and
validate structural world/player/creature/inventory/protocol/action state without
OCR assumptions, preserve runtime isolation from Track B, and promote only
exact-version evidence with explicit confidence boundaries.

## Runtime ownership

```yaml
runner: synology-otclient-01
subject: official native Linux Tibia client only
state_directory: /home/runner/_work/_otclient_tibia_re_state
legacy_compatibility_state_directory: /work/_otclient_tibia_re_state
display: :98
warp_socks_port: 25354
bridge_socket: <state_directory>/runtime/otclient-tibia-re.sock
process_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
container_names: none
```

Track B runtime/process/display/ports/state remain out of scope and must not be
read, stopped, attached to, reconfigured or cleaned by this task.

## Acceptance inventory

- [x] Track A namespace isolation is proven on the dedicated runner.
- [x] Exact official Linux client version/size/SHA are version-fenced.
- [x] Official client reconstruction and normal owned launch have been proven.
- [x] Protocol surface inventory is persisted from the exact binary.
- [x] High-confidence QMeta/string clusters are persisted for Chat, Container, Effect, Market, NPC Trade, Player Trade, Quest and Game Event.
- [x] Capability/observation matrix is persisted with `FACT` versus `UNKNOWN` boundaries.
- [ ] Login recovery / structural `IN_GAME` acceptance is re-proven for the current live session when a live-world experiment becomes necessary.
- [ ] Bridge session status is correlated with decoded world state.
- [ ] Authoritative player position and one reversible movement transition are proven structurally.
- [ ] Creature/player handler offsets and selected message field layouts are deterministically recovered.
- [ ] Outbound builder/serializer entry points are recovered for movement, `MoveObject`, `Attack`, `Follow`, `Talk` and `TradeObject`.

## Current exact-version facts

```yaml
official_client_version: 15.32.df7b29
official_client_size: 51965216
official_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
protocol_inventory:
  run: 31787489302
  job: 94726575137
  head: c63dec6c1329bfb1494de17715956a6815786d66
  result: PASS
  totals:
    protocol_handler_classes: 47
    handle_message_names: 146
    inbound_gameserver_messages: 189
    outbound_gameclient_messages: 160
qmeta_neighborhoods:
  run: 31787757301
  job: 94727417973
  head: 797c8079b6280644cbbd9ce0641846c6fa0fb21e
  result: PASS
symbol_surface:
  run: 31787886977
  job: 94727824870
  head: 923d297ecc49129130b530a9ea6c333de549598f
  result: PASS
  finding: stripped binary exposes no usable qt_static_metacall/staticMetaObject/handler function symbols through GDB
```

## Promoted static conclusions

- World map snapshot/strip/floor and dynamic create/change/delete paths are separate named inbound protocol surfaces.
- `MoveCreature` and explicit creature-state messages are present in the exact binary.
- Player basic/current/skills/state/inventory/goods/XP/death surfaces are present.
- Inventory/container create/change/delete, stash and depot-search surfaces are present; the main container group is class-locally clustered.
- Chat/channel/player-NPC speech surfaces are present; `handleTalkMessage` and channel lifecycle handlers form a compact Chat cluster.
- NPC trade, player trade, market, quest, game-event and graphical-effect groups have compact class-local method-name clusters.
- Outbound named surfaces include directional movement, `GoPath`, `MoveObject`, object use/look, `Attack`, `Follow`, party actions, `Talk`, NPC/player trade, market, container, stash/depot and buddy/friend actions.
- These names do **not** establish wire opcodes, message field layouts, executable handler offsets or safe callable builder offsets by themselves.

## Evidence index

Canonical evidence for the current phase:

- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-official-client-protocol-surface-inventory.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-handler-qmeta-neighborhoods.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-capability-observation-matrix.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/README.md`

Earlier login/reconstruction/runtime failures and their exact run/job evidence remain
preserved in Git history and the earlier evidence/checkpoint documents. They are
not re-expanded here because the current durable task checkpoint is intentionally
compact.

## Current experiment

```yaml
experiment: protocol metadata string -> absolute pointer -> executable RIP xref graph
workflow_source_head: 55dc75c830e571490be30a5c83a922a528c5931f
run: 31788735824
job: 94730524231
runner: synology-otclient-01
subject_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
scope:
  inbound:
    - Chat/Talk
    - Container
    - Creature/MoveCreature
    - PlayerDataBasic
    - Effect
    - Market
    - NPC Trade
    - Player Trade
    - Quest
    - GameEvent
  outbound:
    - MoveObject
    - Attack
    - Follow
    - Talk
    - TradeObject
    - GoPath
state_at_checkpoint: in_progress
result_claimed: false
```

The standalone first version of the xref workflow was removed from the branch
after its run started; the maintained xref step is folded into
`.github/workflows/tibia-official-client-re-qmeta-handler-neighborhood.yml`.
Do not treat deletion of the source workflow as invalidating run `31788735824`:
the run is pinned to its exact source head and exact official-client SHA.

## Anti-stall checkpoint

```yaml
checkpoint_version: 3
updated_at: 2026-08-14T11:37:00+02:00
owner_resume: explicit in current conversation
branch: ci/OTC-20260813-official-client-re-continuation
pr: 289
pr_state: open_draft_mergeable
status: waiting
invocation_started_at: 2026-08-14T11:34:00+02:00
last_progress_at: 2026-08-14T11:37:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: other
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 2
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
last_progress:
  - persisted exact-binary xref experiment
  - persisted capability/observation matrix
  - updated evidence index
  - removed redundant standalone workflow after folding probe into maintained qmeta workflow
blockers: []
```

## Rejected interpretations

- Pixels, socket counts or a visible window are not structural `IN_GAME` proof.
- String offsets are not function offsets.
- Protocol/message names are not wire opcodes.
- QMeta string proximity is not sufficient where class ownership is ambiguous.
- VIP functionality is not absent merely because literal `Vip` message names are sparse; Buddy/FriendSystem vocabulary is used.
- Pre-world GDB attach must not be reintroduced as a normal login diagnostic because prior evidence shows it changes Qt/UI timing.

## Next action

```text
After run 31788735824 reaches a terminal state, inspect job 94730524231 once,
persist the exact xref findings (or exact failure) into Track A evidence, then use
that result to choose the narrowest next deterministic target: QMeta metadata
reconstruction if metadata xrefs are useful, otherwise selected protobuf/wrapper
layout recovery for MoveCreature/PlayerDataCurrent/Container/Talk.
```
