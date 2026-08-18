---
task_id: OTC-20260818-track-a-s10-action-protocol-code-window-harvest
status: investigating
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
related_pr: PENDING
created: 2026-08-18
updated: 2026-08-18
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
estimate_confidence: medium
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
last_progress_at: 2026-08-18
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Continue Track A after the promoted S1-S9 static wave by harvesting already-retained exact-SHA code/disassembly/connect evidence for the **first causal action-layer to protocol-layer edge**, without repeating exhausted QMeta/name scans and without touching the current physical/runtime package lane owned by PR #528.

Primary discriminator:

```text
TContainerGameActionHandler / TGenericGameActionHandler
  -> sendMoveObject
  -> exact protocol owner
  -> exact message producer
```

A matching method name, adjacent type name, QMeta presence, or protocol-surface proximity is insufficient. Promotion requires direct retained disassembly, dataflow, or connection evidence that causally links the action sender to the protocol owner/producer.

# Current trusted boundary

Current trusted base is:

```text
main@ebbb36f50076ff4072c7218e302614c1dfea00b1
```

That base promoted S9 and formally closed the independent repo-only S1-S9 QMeta/static catalogue wave. The retained S9 boundary is:

```yaml
ACTION_LAYER_TO_PROTOCOL_CONNECTION: UNKNOWN
PER_ACTION_PROTOCOL_TO_SERIALIZED_MESSAGE: UNKNOWN
PER_ACTION_RUNTIME_EFFECT: NOT_OBSERVED
STATIC_ACTION_CONTROL_CATALOGUE: EXHAUSTED_FOR_RETAINED_QMETA
```

S10 therefore does **not** run another broad QMeta/name census.

# Historical retained-evidence sources

Read-only historical branch sources verified to exist in `blakinio/otclient`:

```text
ci/OTC-20260814-track-a-single-item-drag
ci/OTC-20260814-track-a-final-write-continuation
ci/OTC-20260814-official-client-re-receiver-recovery
ci/OTC-20260814-track-a-verified-merge-slice
```

Start with `single-item-drag`, because its retained workflow set includes move-object/game-action/protocol-queue investigations and is the most direct candidate for a `sendMoveObject` causal edge. The other branches are fallback retained-evidence sources, not authority to reuse stale runtime addresses on a current client.

# Exact-build safety boundary

Historical retained evidence may remain fenced to the previously researched official native Linux client:

```text
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

PR #528 has separately produced runtime evidence that this old build is now refused as too old. Therefore historical exact-SHA code windows can prove historical client semantics only; they do not prove current-build offsets, helper compatibility, or runtime identity.

This task does not independently acquire the current official client because PR #528 is the active owner of current package/runtime/login continuation.

# Evidence standard

Accept only a directly evidenced causal chain such as:

```text
GameActionHandler sender/callsite
 -> concrete receiver/connect/direct-call edge
 -> protocol owner/handler
 -> concrete message producer/builder
```

Required classification:

```text
PROVEN     direct retained code/disassembly/dataflow/connect evidence closes the claimed edge
DERIVED    inference from PROVEN facts, explicitly weaker than direct proof
UNKNOWN    retained evidence does not close the edge
DISPROVEN  bounded candidate is directly falsified
```

Never promote name similarity or QMeta adjacency to `PROVEN`.

# Planned harvest order

1. Inspect retained `single-item-drag` workflow definitions and any referenced artifact/evidence indexes for `sendMoveObject`, `GameActionHandler`, protocol queue/handler and high-value send disassembly.
2. Reconstruct only the smallest bounded code windows needed to connect sender -> receiver/owner -> producer.
3. If that branch is insufficient, repeat the same bounded search over `final-write-continuation`, `receiver-recovery`, then `verified-merge-slice`.
4. If `sendMoveObject` cannot be closed, do not widen into another general census; record the exact missing retained code window before considering another principal action family.

# Stop / blocker contract

If the retained historical exact-SHA evidence does not contain a direct causal code/dataflow/connect window sufficient to close the edge, persist exactly:

```text
BLOCKED_MISSING_RETAINED_CODE_WINDOW
```

That is a terminal result for this retained-evidence discriminator, not negative proof that the action/protocol connection does not exist.

The next meaningful proof would then require one of:

```text
- an admissible exact code window for the legitimate current official client after current-build provenance is established; or
- a separately legal non-conflicting runtime evidence path under current Track A admission/ownership.
```

Do not guess or reuse stale offsets to avoid this blocker.

# Validation / E2E

This is documentation plus read-only retained-repository evidence analysis.

```yaml
E2E: NOT_APPLICABLE
reason: no client execution, login, gameplay, runtime observation or mutation occurs in S10 retained-evidence harvest
```

Final documentation changes require Markdown/path/full-diff review and repository fast/docs or equivalent exact-head checks. Completion still requires the repository's proportionate fresh independent documentation audit and normal closeout gates.

# Current checkpoint

```yaml
status: investigating
last_completed_step: S10 scope, ownership, retained historical branch set and fail-closed evidence standard established from current main
current_result: UNKNOWN
next_action: inspect the retained exact-SHA single-item-drag workflow/evidence chain for a direct sendMoveObject GameActionHandler -> protocol owner -> message producer code window
```
