# OTC-20260814 — official-client capability experiment research design

```yaml
task_id: OTC-20260814-official-client-capability-experiment-sweep
programme: OTCLIENT-TIBIA-RE
track: official-client-re
status: in_progress
repository: blakinio/otclient
base_branch: main
branch: docs/OTC-20260814-official-client-capability-experiment-sweep
pr: 293
task_kind: research_design
owned_paths:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
  - docs/agents/reports/OTCLIENT-20260814-official-client-experiment-design-review.md
  - docs/agents/handovers/OTC-20260814-official-client-capability-experiment-handover.md
  - docs/agents/tasks/active/OTC-20260814-official-client-capability-experiment-sweep.md
modules_touched: []
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - existing Track A stable runtime bridge and relocation resolver as live state permits
depends_on: []
blocks: []
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
decomposition_decision: single
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
```

## Lifecycle clarification

This task owns the **research-design deliverable in PR #293**. It does **not** own execution of the whole 75-family capability programme after this design is merged.

The canonical programme remains:

```text
docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
```

After this design PR is merged and this task is archived, the `OTCLIENT-TIBIA-RE` coordinator executes bounded hypotheses/phases, persists evidence and rotates worker context according to the canonical programme and the execution model below.

Do not keep this design task permanently active as the catch-all owner for future runtime research.

## Objective

Finalize, validate and merge a durable, evidence-driven experimental design for extracting every useful semantic capability from the exact official native Linux Tibia client without OCR or screen-coordinate clicking as the normal semantic interface.

The design must let a fresh Track A worker determine:

- what can be read structurally;
- what server/world events can be captured structurally;
- what semantic actions can be invoked through proven client paths;
- how static evidence is promoted to live/restart-stable evidence;
- how the resulting capability set is represented as a future Agent Game API;
- how every material result is persisted and queried from Git/evidence state rather than chat.

## Normative design set

The research design consists of:

```text
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
```

Evidence and rationale:

```text
docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
docs/agents/reports/OTCLIENT-20260814-official-client-experiment-design-review.md
docs/agents/handovers/OTC-20260814-official-client-capability-experiment-handover.md
```

Where execution-order/evidence-method details conflict, `OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` controls. Repository/canonical programme safety, authorization and governance remain more authoritative.

## Design scope

The design covers at minimum:

- session/login/recovery and structural `IN_GAME`;
- player identity, position, HP/mana, skills, status, conditions, cooldowns;
- map/tile/cache/minimap and OTBM-relevant extraction;
- creatures, battle list, target, attack/follow and combat/PvP state;
- inventory, equipment, containers, stash/depot, object metadata and item manipulation;
- chat, channels, private/NPC/system messages;
- first-class World/Server Event Intelligence including warnings, events, action errors, connection/death/session-loss state and unknown inbound families;
- NPC conversation/trade, player-to-player trade and party/shared experience;
- context menus, action bars/hotkeys and semantic UI/modal state;
- Cyclopedia, Bestiary, Charms/bonus effects, Bosstiary, Wheel/gems/presets, Forge, Prey, tasks/Soul Seals, Imbuements, Weapon Proficiency, Market, Houses, Quest, rewards and other discovered current-client systems;
- analyzers/loot/gain-waste telemetry;
- Friends/VIP/Social read-only discovery;
- generated protocol/QMeta/runtime census and dependency graph;
- inbound/outbound common-spine discovery;
- restart/ASLR/update resilience and stable bridge/API promotion;
- creative recovery of all unclassified feature families.

## Execution architecture required by the design

Static discovery must precede live account/session work whenever possible:

```text
S0 current exact official-client binary identity
-> S1 exhaustive static generated-message/QMeta/runtime census
-> S2 classification graph + information-gain probe planning

LIVE BOUNDARY

-> L0 approved login/recovery + structural IN_GAME
-> L1 inbound/outbound topology + causal recorder/noise baseline
-> L2 core reads
-> L3 core actions + normal-client reference-path parity
-> L4 interaction systems
-> L5 rich read/preview systems
-> L6 restart/relogin/stable bridge/update-resilience validation
```

Do not require login for E51/E52-style static census work.

## Evidence quality requirements

The design must preserve the canonical experiment fields, including:

- exact client SHA/version;
- session/runtime identity;
- one falsifiable hypothesis;
- expected structural evidence;
- `abort_conditions`;
- `rollback_or_recovery`;
- authorized effects and explicit side-effect budget;
- negative/no-stimulus controls;
- repeatability/restart validation;
- privacy redactions;
- exact evidence refs;
- one executable `next_action`.

Reads and actions are tracked independently:

```text
READ:   R0 STATIC_PRESENT -> R1 LIVE_READ -> R2 CAUSAL_READ
        -> R3 RESTART_STABLE_READ -> R4 BRIDGE_READ

ACTION: A0 STATIC_PRESENT -> A1 REFERENCE_TRACE -> A2 ABI_MESSAGE_PROVEN
        -> A3 SERVER_CONFIRMED_ACTION -> A4 BRIDGE_ACTION
```

The older G0-G4 ladder remains a summary only.

## Causality requirement

A live correlation must not rely only on temporal before/after proximity. The design requires a causal recorder or equivalent evidence with, where available:

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

Important correlations require a no-stimulus baseline to detect naturally changing candidates.

## Action parity requirement

A stable semantic action must be compared against normal official-client behaviour:

```text
normal client action -> normalized outbound semantic message/result
programmatic action   -> normalized outbound semantic message/result
```

Transport-only metadata may differ. Semantic fields and authoritative result must match or the discrepancy must be explicitly explained before A3/A4 promotion.

## Machine-readable persistence requirement

High-cardinality research state cannot live only in Markdown.

Future execution must create/reuse one canonical Track A evidence root with logical datasets equivalent to:

```text
capabilities.jsonl
protocol_messages.jsonl
runtime_types.jsonl
experiments/<experiment_id>.yaml
```

Do not create parallel evidence roots when equivalent canonical files already exist.

Markdown remains the human-readable synthesis; raw traces/dumps remain artifacts when repository/privacy/licensing rules require it.

## Quantitative coverage requirement

The future programme must measure at least:

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

Census-level acceptance requires:

1. every generated message has direction and family/status or explicit `UNCLASSIFIED`;
2. every recovered Tibia-owned runtime/QMeta census entry has family/status or ignored-with-reason;
3. every P0 capability has an experiment ID or explicit `BLOCKED/UNSUPPORTED` rationale;
4. no P0 `STATIC_PRESENT` capability is silently abandoned;
5. every R4/A4 capability has fresh restart/rediscovery validation.

These coverage gates do not replace canonical programme completion acceptance.

## Rare event and privacy requirements

Rare world/server events use explicit evidence states:

```text
STATIC_REACHABLE
LIVE_OBSERVED
REPLAY_CONFIRMED
NOT_OBSERVED
```

Do not keep a worker alive waiting for a raid, maintenance warning or rare disconnect. Sessiondump/replay is a passive research lead only and must not become a normal Agent Game API dependency without evidence and a safe need.

For chat/social research, do not commit raw unrelated-player private content. Persist normalized type/channel/length/flags and anonymized identity where possible. Plain text is allowed only for owner/test/NPC-generated evidence or after explicit redaction. Never persist credentials, session secrets or secret-bearing captures.

## Safety boundary

Default to read-only or reversible/no-cost experiments. Do not:

- destroy valuable items/equipment;
- spend Tibia Coins;
- materially spend gold/Forge/Charm/Prey/other resources;
- reset valuable character configuration;
- create real Market purchases/offers merely for proof;
- disturb unrelated players;
- bypass anti-cheat/client checks;
- expose secrets/private account state;
- consume owner-funded Codex/OpenAI/paid AI quota without explicit permission for that exact use.

Any experiment requiring a larger effect budget is `BLOCKED_REQUIRES_OWNER_AUTHORIZATION` unless current explicit authorization exists.

## Acceptance inventory for this design task

This **design task** is complete only when:

- all seven owned paths exist in PR #293 and the changed-file list matches the task ownership declaration;
- the broad experiment sweep is durable;
- the evidence-derived E51-E75 extension is durable;
- the hardened execution model is durable;
- the exact-binary census and design review are durable;
- the handover points to the current design and next programme action;
- login remains a hard boundary for live experimentation but not for offline static census;
- World/Server Event Intelligence remains first-class;
- causal/noise controls, independent read/action gates, reference-path parity, machine-readable persistence, measurable coverage, rare-event states and privacy minimization are explicit;
- no runtime capability is falsely promoted by this documentation-only task;
- the full PR diff contains no unrelated files, binaries, assets, secrets or private data;
- required documentation CI/checks pass on the exact final PR head;
- PR #293 is mergeable with no unresolved blocking review state;
- PR #293 is merged through the repository merge gate;
- this design task is archived after merge according to repository lifecycle policy.

Runtime E2E for this documentation-only design task is `NOT_APPLICABLE_WITH_REASON`: runtime proof belongs to subsequent bounded OTCLIENT-TIBIA-RE execution work, not to the design PR.

## Current checkpoint

```yaml
checkpoint_version: 3
updated_at: 2026-08-14T10:05:00+02:00
base_main: 005158b5b9bf25fe77bd5fc10813a6388a072836
pr: 293
status: in_progress
runtime_claims_by_this_task: none
durable_design:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
durable_evidence:
  - docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
  - docs/agents/reports/OTCLIENT-20260814-official-client-experiment-design-review.md
validation_notes:
  - changed-file ownership must remain exactly aligned with the seven research-design paths
  - documentation-only runtime E2E is not applicable; exact-head CI and PR hygiene remain required
safe_to_resume: true
post_merge_programme_action: resolve exact current official Linux client version/SHA, execute S1/S2 exhaustive static census and graph/probe planning before login, then recover/login and structurally prove IN_GAME for L1 live correlation
next_action: review the exact PR #293 changed-file set and diff, verify exact-head documentation CI and mergeability, fix any design/CI findings, then mark ready and merge when the repository merge gate is satisfied
```
