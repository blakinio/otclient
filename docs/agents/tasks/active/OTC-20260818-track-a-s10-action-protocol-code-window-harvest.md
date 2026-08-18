---
task_id: OTC-20260818-track-a-s10-action-protocol-code-window-harvest
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P1-BRIDGE
track_id: official-client-re
task_kind: discovery
phase: retained-exact-sha-code-window-harvest
execution_mode: github_only
branch: docs/OTC-20260818-track-a-s10-action-protocol-code-window-harvest
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
live_main_observed: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
related_pr: 539
created: 2026-08-18
updated: 2026-08-19
risk: low
implementation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-track-a-s10-action-protocol-code-window-harvest.md
  - docs/agents/reports/OTCLIENT-20260818-track-a-s10-action-protocol-code-window-harvest.md
modules_touched:
  - official-client-re-documentation
  - track-a-action-protocol-boundary
reuses:
  - docs/agents/reports/OTCLIENT-20260818-track-a-s9-action-control-static-census.md
  - docs/agents/tasks/archive/OTC-20260818-track-a-s9-action-control-static-census.md
  - ci/OTC-20260814-track-a-single-item-drag
  - ci/OTC-20260814-track-a-final-write-continuation
  - ci/OTC-20260814-official-client-re-receiver-recovery
  - ci/OTC-20260814-track-a-verified-merge-slice
depends_on: []
blocks: []
non_overlap:
  - PR #528 owns current official-client package/runtime/login continuation; this task does not acquire, update, execute, observe or mutate that runtime or package lane.
  - PR #475 worldmap physical runtime is not observed or mutated.
  - PR #302 direct-player-position Draft is not modified or observed live.
  - PR #536 owns only its coverage-audit task/checklist/matrix paths; this task does not edit them.
  - no new official-client bytes are acquired and no old runtime offsets are promoted as current-build facts.
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 6
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one bounded retained-evidence harvest for the first causal action-to-protocol edge
validation_level: focused
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
invocation_started_at: 2026-08-18
last_progress_at: 2026-08-19
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
last_completed_step: all four bounded retained historical branches inspected for the sendMoveObject action-to-protocol discriminator
terminal_classification: PARTIAL_ACTION_TO_PROTOCOL_EDGE
current_result: BLOCKED_MISSING_RETAINED_CODE_WINDOW
next_action: run proportionate independent documentation audit and exact-head repository checks; if accepted, promote/archive this bounded result without weakening the missing-edge boundary
---

# Objective

Continue Track A after the promoted S1-S9 static wave by harvesting already-retained exact-SHA code/disassembly/connect evidence for the first causal action-layer to protocol-layer edge, without repeating exhausted QMeta/name scans and without touching the current physical/runtime package lane owned by PR #528.

Primary discriminator:

```text
TContainerGameActionHandler / TGenericGameActionHandler
  -> sendMoveObject
  -> exact protocol owner
  -> exact message producer
```

A matching method name, adjacent type name, QMeta presence, or protocol-surface proximity is insufficient. Promotion requires direct retained disassembly, dataflow, or connection evidence that causally links the action sender to the protocol owner/producer.

# Terminal S10 result

```yaml
terminal_classification: PARTIAL_ACTION_TO_PROTOCOL_EDGE
current_result: BLOCKED_MISSING_RETAINED_CODE_WINDOW
ACTION_LAYER_TO_PROTOCOL_CONNECTION: UNKNOWN_FOR_THE_SPECIFIC_SENDMOVEOBJECT_EDGE
EXACT_PROTOCOL_OWNER: PROVEN_HISTORICAL_EXACT_BUILD
EXACT_MOVEOBJECT_MESSAGE_PRODUCER: PROVEN_HISTORICAL_EXACT_BUILD
PER_ACTION_RUNTIME_EFFECT: NOT_OBSERVED_BY_S10
CURRENT_BUILD_OFFSETS: UNKNOWN
```

This blocker is terminal for the retained-evidence discriminator. It is not evidence that the action/protocol connection does not exist.

# Historical exact-build fence

All executable addresses below are historical evidence for exactly:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

They must not be reused as current-client offsets. PR #528 owns the current official-client package/runtime lane.

# H1 — historical move-object sender: PROVEN

Retained evidence:

`docs/agents/evidence/OTC-20260813-official-client-re/20260814-high-value-outbound-signal-disassembly.md`
from `ci/OTC-20260814-track-a-single-item-drag`.

Direct exact-build facts:

```text
TContainerGameActionHandler static metaobject 0x30850a0
qt_static_metacall 0xd1dac0
sendMoveObject QMeta case 0xd1df30
QMeta signal index 1
wrapper -> QMetaObject::activate
```

The wrapper loads the QMeta argument pointer and emits a Qt signal. It is not a serializer or protocol builder.

Historical successful workflow provenance recorded by the retained evidence:

```text
run 31793188185
job 94744455372
head 1c4ef6b612220e24cb312dfa6fce032b5c13d484
```

# H2 — sender-to-receiver binding: PARTIAL, insufficient for the target edge

Retained evidence:

- `20260814-gameaction-connectimpl-arguments.md`
- `20260814-gameaction-slot-provenance.md`
- `experiments/EXP-20260814-gameaction-connectimpl-correlation.yaml`

Direct exact-build facts:

```text
Container connect candidate 0x7ffb24:
  sender static metaobject = 0x30850a0 (TContainerGameActionHandler)
  recovered slot payload target = 0x8332d0
  adjustment = 0

0x8332d0:
  class = tibia::game::TInternalGameActionRouter
  behavior = Qt re-emitter / internal action router
  serializer = false
```

The retained connect reconstruction explicitly does not establish the pointer-to-member signal index for the proven sender-metaobject sites. Therefore `0x7ffb24` cannot be causally identified as the connection for `TContainerGameActionHandler::sendMoveObject` signal index `1` from the retained window alone.

The second nearby Container site, `0x7d7307`, also does not close the gap: within the bounded window the Container metaobject is loaded into the receiver-side register while the pushed sender metaobject remains unresolved.

Classification:

```yaml
TContainerGameActionHandler_some_signal_to_TInternalGameActionRouter: PROVEN_HISTORICAL_EXACT_BUILD
TContainerGameActionHandler_sendMoveObject_signal_1_to_that_connect_site: UNKNOWN
```

# H3 — exact protocol owner and MoveObject producer: PROVEN independently

Retained evidence:

`docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-action-builders.md`
from `ci/OTC-20260814-track-a-single-item-drag`.

Direct exact-build facts:

```text
static metaobject 0x3085b60 = tibia::protocol::TProtocolMessageQueue
QMeta index 218 = sendMoveObject
case entry 0xdf6d58
concrete builder body 0xbd3be0
internal GameclientMessage discriminator 0x78
```

The builder allocates/initialises the message object, prepares typed payload storage, copies action parameters and submits the owning message. The `0x78` value is only an internal message discriminator; it is not promoted to a final wire opcode/byte.

Historical successful workflow provenance:

```text
QMeta decode run 31802808290 / job 94774542787
dispatch run 31802935253 / job 94774953120
builder disassembly run 31803012968 / job 94775199763
convergence run 31803088165 / job 94775445667
```

# Fallback retained branches

The bounded fallback pool was also inspected:

```text
ci/OTC-20260814-track-a-final-write-continuation
ci/OTC-20260814-official-client-re-receiver-recovery
ci/OTC-20260814-track-a-verified-merge-slice
```

Later retained continuation state promotes the general historical model:

```text
semantic action
 -> TInternalGameActionRouter
 -> TProtocolMessageQueue builder
 -> clientMessageReadyToProcess
 -> transport processing
```

It also corrects older transport hypotheses and identifies the queue consumer QSlotObject at `0x7dd630` plus downstream transport classes. None of these retained additions supplies the missing action-specific pointer-to-member/connect proof binding `TContainerGameActionHandler::sendMoveObject` signal index `1` to the concrete router/queue path.

`ci/OTC-20260814-track-a-verified-merge-slice` adds final-write/TCP provenance but no new action-specific Container connection window.

# Exact missing retained window

To promote the full target to `PROVEN_ACTION_TO_PROTOCOL_EDGE`, one of the following would be required:

```text
1. exact connect construction proving:
   TContainerGameActionHandler::sendMoveObject signal index 1
   -> concrete receiver/member
   -> TInternalGameActionRouter / TProtocolMessageQueue action path

or

2. direct disassembly/dataflow proving that the sendMoveObject payload from the action handler
   reaches TProtocolMessageQueue::sendMoveObject / body 0xbd3be0 while preserving action identity.
```

The four bounded retained branches do not contain that proof window in the evidence inspected by S10.

Therefore the required fail-closed result is:

```text
BLOCKED_MISSING_RETAINED_CODE_WINDOW
```

# Safety / non-overlap

S10 performed repository-only retained-evidence analysis.

```yaml
runtime_access: none
client_executed: false
new_client_bytes_obtained: false
credentials_accessed: false
login_performed: false
gameplay_performed: false
pr528_runtime_touched: false
pr475_runtime_touched: false
pr302_runtime_touched: false
E2E: NOT_APPLICABLE
```

The Remote Desktop/Synology connector became unavailable during this invocation; no runtime claim depends on it and no runtime operation was attempted after the disconnect.

# Closeout gate

The research discriminator itself is exhausted. Remaining work on PR #539 is governance/validation only:

1. independent documentation audit;
2. exact-head path/Markdown/full-diff repository checks;
3. if accepted, promotion/archive of this bounded partial result without converting the missing edge to `PROVEN`.

Any future causal proof requires an admissible exact code window for the legitimate current official client or a separately legal non-conflicting Track A runtime path. It must not reuse the historical addresses above as current-build facts.
