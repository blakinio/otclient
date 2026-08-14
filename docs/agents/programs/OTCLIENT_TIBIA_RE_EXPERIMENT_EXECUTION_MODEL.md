# OTCLIENT-TIBIA-RE experiment execution model

```yaml
programme: OTCLIENT-TIBIA-RE
track: official-client-re
subject: official native Linux Tibia client only
contract_version: 1.0
status: normative_execution_contract
applies_to:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_CENSUS_EXTENSION.md
priority_when_conflicting: this_file
```

## Purpose

This file hardens the broad capability sweep into an executable research methodology. The sweep and census extension define **what** to investigate; this file defines **how, in what order, and with what evidence** the work is promoted.

The goal is to prevent three failure modes:

1. treating a large symbol inventory as proof of a live capability;
2. confusing temporal correlation with causality in a noisy live game session;
3. turning a 75-family research programme into one unbounded worker/task context.

The canonical `OTCLIENT_TIBIA_RE_PROGRAMME.md` remains programme-level authority. Execute bounded hypotheses and rotate worker context while preserving one durable programme state.

## Lifecycle boundary

The PR that introduces this research design is a **research-design deliverable**, not execution of the whole capability sweep.

After the design PR is merged and its task is archived, the canonical `OTCLIENT-TIBIA-RE` coordinator must execute the programme through bounded experiment phases/tasks or continuation checkpoints. Do not keep the design task permanently active as the owner of all future experiments.

A future worker must not claim that the capability sweep was executed merely because these documents exist.

## Required execution order

Static discovery must precede live account/session work whenever the experiment does not require `IN_GAME`.

```text
S0  current official-client binary identity
    -> resolve exact current version/SHA and provenance

S1  exhaustive static census
    -> all generated protocol messages
    -> all Tibia-owned QMeta classes/methods/signals/properties/enums
    -> protocol queue methods
    -> relevant RTTI/vtable/generated descriptor families

S2  static graph + probe planning
    -> classify every census object
    -> build message/handler/storage/controller dependency graph
    -> rank hypotheses by information gain
    -> prepare exact passive probes

---------- LIVE ACCOUNT / WORLD BOUNDARY ----------

L0  login/recovery
    -> use current approved login path
    -> structural IN_GAME proof
    -> create new session_epoch

L1  common spines + causal recorder
    -> inbound dispatcher hypotheses
    -> outbound action dispatcher hypotheses
    -> background-noise baseline

L2  core read correlations
    -> player position
    -> HP/mana/player state
    -> map/tiles
    -> CreatureStorage
    -> inventory/containers
    -> chat/world events

L3  core semantic actions
    -> movement/turn/stop/path
    -> attack/follow/cancel
    -> use/use-with/use-on-creature/move-object
    -> container navigation
    -> talk/chat
    -> reference-path parity + server-confirmed result

L4  interaction systems
    -> party/shared experience
    -> player trade
    -> NPC conversation/trade
    -> cooldowns
    -> quick loot
    -> analyzers
    -> context/action-bar semantics

L5  rich model systems
    -> Bestiary/Bosstiary/bonus effects
    -> Wheel/gems/presets
    -> Forge
    -> Prey/Tasks/Soul Seals
    -> Imbuements/Weapon Proficiency
    -> Market/Houses/Quest/Rewards/etc.
    -> read/preview first

L6  stability
    -> fresh PID/ASLR validation
    -> logout/relogin/recovery
    -> stable bridge
    -> second-version update-resilience validation when another version is available
```

Do not spend live-session time performing S1/S2 work that can be completed against the exact binary offline.

## Competing dispatcher hypotheses

Do not assume the architecture that the experiment is trying to discover.

For inbound processing explicitly test competing hypotheses:

```text
H-IN-1
TProtocolMessageQueue is the central semantic event spine.

H-IN-2
TProtocolMessageQueue is primarily a fan-out surface and feature-family handlers/storage
objects are the real semantic event boundaries.

H-IN-3
Multiple independent inbound lanes exist and no single complete semantic dispatcher exists.
```

For outbound processing likewise test:

```text
H-OUT-1
Most semantic user actions converge on one common GameAction/generated-message dispatch path.

H-OUT-2
A small number of family dispatchers exist: movement, creature, generic use, chat,
containers, feature-specific actions.

H-OUT-3
Important action families have materially independent paths and require separate bridges.
```

Record falsification evidence. Do not force all evidence into a preferred common-bus design.

## Causal recorder

Live experiments operate in a noisy environment: regeneration, creature movement, timers, chat, map updates and connection traffic occur without the controlled stimulus. Timestamp-only before/after observations are insufficient for high-confidence promotion.

Every live instrumentation run should produce or derive a causal record with at least:

```yaml
session_epoch: <new identifier after each login/relogin/restart>
monotonic_ns: <monotonic timestamp>
stimulus_id: <controlled action id or BACKGROUND>
message_direction: CLIENT_TO_SERVER | SERVER_TO_CLIENT | LOCAL
message_sequence: <sequence/counter if structurally available>
message_type: <generated type or UNKNOWN>
connection_lane: <lane/socket/session identity if available>
thread_id: <runtime thread when observable>
handler: <resolved handler or UNKNOWN>
runtime_object: <semantic object/resolver identity>
object_instance_epoch: <process/session scoped identity>
before_state_hash: <normalized state hash when applicable>
after_state_hash: <normalized state hash when applicable>
semantic_delta: <normalized changed fields>
evidence_ref: <run/artifact/repository ref>
```

The recorder may store additional fields but must not store secrets or unnecessary personal chat content.

### Noise baseline

Before promoting a new live correlation, capture a bounded `NO_STIMULUS` baseline for the same probe set. Determine which candidates change naturally. A candidate that also changes in the negative-control baseline must not be promoted solely because it changed after the stimulus.

## Experiment contract additions

Every live experiment must retain all fields from the canonical programme experiment contract, including fields that were omitted from the first sweep draft:

```yaml
experiment_id:
objective:
hypothesis:
client_version:
binary_sha256:
preconditions:
  session_state:
  runner:
  container:
pid:
pie_base:
relevant_runtime_objects:
authorized_effects:
side_effect_budget:
  max_gold: 0
  max_tibia_coins: 0
  max_items_at_risk: 0
  max_irreversible_changes: 0
allowed_targets:
action:
expected_structural_evidence:
abort_conditions:
rollback_or_recovery:
observed_structural_evidence:
negative_control:
repeatability:
restart_test:
result: PROVEN | DERIVED | DISPROVEN | INCONCLUSIVE
artifacts:
privacy_redactions:
next_action:
```

Any experiment needing a larger effect budget must record `BLOCKED_REQUIRES_OWNER_AUTHORIZATION` unless explicit current authorization exists.

## Independent read and action evidence gates

The original G0-G4 ladder remains useful as a summary, but reads and actions must be tracked independently because a subsystem can be fully readable while its mutating actions remain unproven.

### Read gates

```text
R0 STATIC_PRESENT
  named static symbol/QMeta/generated type/storage/controller/field only

R1 LIVE_READ
  deterministic value/state read from a live current-version runtime

R2 CAUSAL_READ
  value/event changes with a controlled stimulus and survives negative controls

R3 RESTART_STABLE_READ
  resolver rediscovered on a fresh PID/PIE/session and same semantic read is reproduced

R4 BRIDGE_READ
  stable reusable non-OCR API exposes the read without ad-hoc debugger injection
```

### Action gates

```text
A0 STATIC_PRESENT
  action/message/handler surface exists statically

A1 REFERENCE_TRACE
  normal official-client UI/input action is traced through the intended semantic path

A2 ABI_MESSAGE_PROVEN
  action ABI/arguments and generated outbound semantic message are understood

A3 SERVER_CONFIRMED_ACTION
  programmatic semantic invocation produces the same intended server/client structural result

A4 BRIDGE_ACTION
  stable reusable non-pixel API repeats the action after runtime rediscovery/restart
```

The capability matrix must record both `read_gate` and `action_gate` when applicable.

Example:

```text
Forge state        R4 / A0
Movement           R4 / A4
Bestiary read      R3 / NOT_APPLICABLE
Player trade       R2 / A1
```

Do not collapse a strong read proof into an implied action proof.

## Reference-path parity for semantic actions

For every action that is intended for the stable Agent Game API, compare the normal client path with the programmatic path.

```text
REFERENCE
normal official-client input/action
-> capture normalized outbound message M_ref
-> capture resulting structural state R_ref

CANDIDATE
programmatic semantic invocation
-> capture normalized outbound message M_agent
-> capture resulting structural state R_agent

PARITY
compare semantic fields(M_ref, M_agent)
compare result(R_ref, R_agent)
```

Expected transport-only differences such as sequence, encryption framing, socket timing or correlation counters may differ. Semantic action fields and resulting authoritative state must match or the discrepancy must be explained before A3/A4 promotion.

A function call returning successfully is never sufficient evidence for action parity.

## Exhaustive protocol schema requirement

The exhaustive protocol census must extract more than message names whenever generated metadata makes it possible.

For every generated message record:

```yaml
name:
direction:
namespace:
fields:
  - number:
    name:
    type:
    cardinality:
    oneof:
    enum_values:
nested_messages:
serializer:
deserializer:
queue_method:
handler:
feature_family:
classification_status:
current_client_sha:
first_live_experiment:
```

`UNCLASSIFIED` is a valid temporary state. Silently omitting an unknown message is not.

## Runtime/QMeta graph requirement

The static and live census should build a graph rather than only a flat name list.

Target relationships such as:

```text
GeneratedMessage
  -> TProtocolMessageQueue::received/send method
  -> feature ProtocolMessageHandler
  -> Storage / domain object
  -> signal / model mutation
  -> Controller
  -> QML/UI representation
```

Where Qt object relationships exist and can be observed safely, record QObject instance ownership and signal/slot relationships. Do not assume every discovered type is a QObject.

For outbound actions build the inverse graph from normal user intent to generated message.

## Machine-readable durable registries

Markdown reports remain human-facing summaries. High-cardinality research state must additionally be machine-readable so later agents can query coverage without rereading long prose.

The execution worker must create/reuse canonical files under a single Track A evidence root selected after checking existing repository conventions. Required logical datasets are:

```text
capabilities.jsonl
protocol_messages.jsonl
runtime_types.jsonl
experiments/<experiment_id>.yaml
```

Do not create duplicate roots if equivalent canonical files already exist.

### Capability record minimum

```yaml
capability_id:
feature_family:
status:
authority:
read_gate:
action_gate:
current_client_sha:
read_source:
action_source:
resolver:
restart_proven:
experiment_ids:
evidence_refs:
notes:
```

### Runtime type record minimum

```yaml
type_name:
namespace:
kind: QMETA | RTTI | GENERATED_MESSAGE | STORAGE | CONTROLLER | HANDLER | OTHER
feature_family:
methods:
signals:
properties:
relationships:
classification_status:
current_client_sha:
```

Large raw traces/dumps remain Actions artifacts or approved evidence artifacts; Git stores indices, hashes and normalized non-sensitive results.

## Quantitative coverage gates

Programme coverage must be measurable rather than described only as "broad" or "material".

For the current exact client version track at minimum:

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

Required census completion conditions:

1. 100% of generated protocol message types have a direction and `feature_family` or explicit `UNCLASSIFIED` status.
2. 100% of recovered Tibia-owned QMeta/runtime census entries have a family/status or explicit ignored-with-reason classification.
3. Every P0 capability has at least one experiment ID or an explicit `BLOCKED/UNSUPPORTED` rationale.
4. No P0 `STATIC_PRESENT` capability is silently left without a promotion/falsification experiment.
5. Every A4 action has fresh restart/rediscovery validation.
6. Every R4 read has fresh restart/rediscovery validation.

Programme completion still requires the canonical acceptance inventory; 100% census classification alone is not programme completion.

## Discovery versus independent validation

A discovery run and a promotion-validation run must be conceptually separate for important P0/G4 candidates.

```text
DISCOVERY
find candidate resolver/object/message/handler
-> persist hypothesis and rediscovery method

VALIDATION
fresh PID/PIE/session where practical
-> do not trust the old heap address
-> rediscover semantically
-> execute the same falsifiable test
-> compare outcome
```

For stable bridge/API promotion, use a fresh validator/worker context when repository execution policy calls for independent validation. The validator may receive the hypothesis and resolver strategy but must not treat the discoverer's conclusion as evidence.

## Rare-event evidence states

World/Server Event Intelligence contains naturally rare events such as specific raids, server maintenance/restart warnings or unusual disconnect reasons. Do not keep a worker alive merely waiting for them.

Record one of:

```text
STATIC_REACHABLE
  handler/type/path exists statically but event not observed live

LIVE_OBSERVED
  event observed in a real current-version session

REPLAY_CONFIRMED
  a repository-approved deterministic replay/session fixture reproduces the event path

NOT_OBSERVED
  no current evidence yet
```

Investigate `tibia::sessiondump::*` only as a passive research lead for deterministic replay feasibility. Do not make sessiondump support an Agent Game API dependency unless a safe product need and evidence justify it.

Synthetic/replay evidence does not replace a live observation where the programme acceptance explicitly requires live current-version evidence, but it may efficiently validate parsing/dispatch for rare inbound families.

## Privacy and sensitive-data minimization

Research covers private messages, player names, VIP/friends, party and social state. Raw personal communication from unrelated players must not be committed to Git.

Persist only the minimum evidence needed, for example:

```text
message type
channel/type ID
length
structural flags
anonymized or hashed actor identity when identity is relevant
timestamp/sequence metadata
normalized fields
```

Plain message text may be persisted only when it was deliberately generated by the owner/test participant/NPC for the experiment and contains no secret or unnecessary personal data, or after explicit redaction/anonymization.

Never commit account credentials, authentication/session tokens, private cookies, secret-bearing network traces or screenshots containing secrets.

## Information-gain scheduling

Within a priority tier, prefer experiments that can unlock many downstream capabilities.

High-information targets include:

1. exhaustive generated-message/QMeta graph;
2. inbound protocol queue/feature-handler topology;
3. outbound action topology;
4. semantic object metadata service;
5. central CreatureStorage/player/container storages;
6. generic UI modal/window state;
7. restart-stable resolver framework.

If a lower-priority feature reveals a common dispatcher/storage used by P0 features, investigate that common mechanism immediately.

## Stop and anti-stall semantics

A single uncertain offset, rare event or unavailable feature must not stall the programme.

For each bounded hypothesis:

1. record current result;
2. try one materially different discovery method if justified;
3. if still unresolved, classify `INCONCLUSIVE/BLOCKED`;
4. move to another READY high-information experiment;
5. return only when canonical real stop conditions are met.

Do not wait in the foreground for CI, a raid, a server-save warning or another naturally delayed condition when independent READY research exists.

## Desired terminal evidence

A stable Agent Game API capability is strongest when the repository can show:

```text
exact client SHA/version
+ static semantic resolver
+ live reference-path trace
+ causal state/message correlation
+ negative control
+ server-confirmed result when action
+ fresh PID/ASLR rediscovery
+ stable bridge invocation/read
+ machine-readable capability record
+ human-readable evidence summary
```

Anything less must be represented by the appropriate lower read/action gate rather than described as fully supported.
