# Local Track A Vision Agent Supervisor — Design

## Status and authority

This design formalizes the owner-approved architecture direction for `OTC-20260830-local-vision-agent-supervisor-discovery` in `blakinio/otclient`.

The owner approved the architectural direction on 2026-08-30. This written specification still requires separate owner review and approval before implementation planning.

This document grants no runtime or mutation authority. Until a separately authorized later phase says otherwise:

```yaml
runtime_access: none
implementation_authorized: false
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
```

No implementation step may weaken current Track A admission, exact-client fencing, canonical lease/registration/rebind/recovery, Gate A, Gate B, whole-lifetime supervision, `input.lock`, Kasm runtime-access, or single-local-model-residency policy.

## Problem

The owner already has the pieces required for a local visual research assistant, but they are not yet one coherent observable agent session:

- Molehill-PC has the existing local supervisor, Ollama, bounded local-worker MCP, pinned Hermes isolation and a disabled CUA registration;
- merged PR #790 provides the bounded `VisualEvidence` harness semantics and the leading tested Qwen3-VL profile;
- Track A already has canonical runtime governance, Kasm capture locators, guarded dispatch, `input.lock`, exact-current runtime-state observers and stronger world-state anchors;
- existing secret-bearing Track A work demonstrates secret environment scrubbing, but there is no generic credential broker for this future agent;
- there is no persistent owner-visible agent session tying task intake, heartbeat, screenshots, visual observations, runtime signals, action proposals, physical authority, evidence and owner controls together.

The missing subsystem must not become a second authority model or a generic autonomous desktop controller. It must preserve the existing supervisor and Track A boundaries while adding a thin persistent control/session layer.

## Decision

Adopt a **thin persistent Molehill session/control service plus a narrow Track A physical runtime edge**.

Qwen3-VL is a visual/OCR sensor, not an authority source. Deterministic policy and existing Track A runtime governance remain outside the model. CUA and Hermes are not on the primary physical-action path.

```text
OWNER dashboard/chat                 SUPERVISING ChatGPT/Codex
        |                                      |
        +------------- task/control -----------+
                           |
                 Molehill agent session service
                    /        |         \
            event/evidence  model      supervisor bridge
                ledger      scheduler
                              |
                    deterministic prefilter
                              |
                         Qwen3-VL
                              |
                        VisualEvidence
                              |
                       state reconciler
                         /          \
                  visual state    runtime evidence
                                      |
                              Track A runtime edge
                                      |
                           authority adapter
                                      |
                       bounded named executor
                                      |
                         before/after evidence
```

## Rejected primary approaches

### CUA-centric operator

The disabled `cua_repl` could reduce bespoke GUI code, but its authority surface is broader than the required Track A action vocabulary. Binding every low-level click or key event to the exact canonical lease/Gates/`input.lock`/budget/evidence transaction would be indirect and harder to audit. CUA remains disabled and may be reconsidered only as an optional diagnostic adapter after a separately reviewed need is demonstrated.

### Hermes-centric persistent agent

The pinned Hermes container provides useful isolation and safe-mode plumbing, but its current integration is batch/audit oriented. Making it the primary persistent Track A planner would add a second autonomous decision layer while the session state, owner controls, provenance, evidence and runtime-authority adapters would still need to be built. Hermes remains a bounded optional subworker, not the agent runtime.

## Design principles

1. **Authority outside models.** Model output is untrusted candidate analysis and never grants runtime, credential, action, semantic or merge authority.
2. **Visual evidence is additive.** OCR/vision may classify visible state but cannot independently promote `IN_GAME` or equivalent semantic runtime state.
3. **Reuse canonical Track A control.** The new runtime edge wraps existing guard/transition/lock/state mechanisms; it does not fork them.
4. **Named actions only.** The model never receives arbitrary shell, process-control, coordinate click or arbitrary text-entry tools.
5. **Owner controls dominate.** `STOP` and `PAUSE` are control-plane state, not prompts, and dominate supervisor/model requests.
6. **Fail closed on ambiguity.** Conflicting sensors, stale authority, uncertain effect outcome, model-slot conflict or lost heartbeat blocks new physical effects.
7. **One local model at a time.** Inference is serialized across the local supervisor. The service never evicts an unexpected foreign resident model merely to continue.
8. **Evidence before claims.** Every effect-capable run has an append-only event sequence and content-addressed evidence manifest.
9. **No credential propagation.** Tibia credentials never enter model inputs, session chat payloads, screenshots sent to vision, evidence records or logs.
10. **No unrestricted gameplay.** The architecture covers bounded research transitions only.

## Placement and trust zones

### Molehill control plane

The persistent session service runs alongside the existing local supervisor on Molehill-PC.

Responsibilities:

- persistent `session_id`, task/run state and heartbeat;
- owner/supervisor/system/model message provenance;
- task-envelope validation and idempotency;
- state reconciliation across vision and stronger runtime signals;
- local model-slot scheduling;
- event/evidence ledger;
- dashboard and owner chat;
- supervisor bridge;
- no direct Track A authority and no raw Tibia credentials.

The existing `mcp/local_worker_server.py` remains a separate bounded low-risk subworker. Do not add high-risk Track A actions, architecture decisions or credential operations to that MCP server.

### Track A physical runtime edge

A thin runtime-edge adapter runs in the existing Track A physical environment on Synology/Kasm or immediately adjacent to it.

Responsibilities:

- read-only screenshot/crop production when separately admitted;
- exact runtime-state signal access through reviewed producers;
- current Track A authority reconciliation before any future mutation;
- bounded semantic-action execution through existing canonical guard paths;
- secret injection only inside a separately authorized credential-broker transaction;
- before/after evidence production;
- no autonomous planning.

The runtime edge must not expose a generic remote shell or generic GUI-control API.

## Session and transport architecture

The session contract is transport-independent and versioned. The initial implementation should keep the owner UI loopback-only and use one dedicated authenticated local-network channel between the Synology runtime edge and Molehill control plane.

Preferred edge transport:

- Synology initiates an outbound persistent connection to the Molehill edge endpoint so no general inbound control listener is required on Synology;
- transport uses mutually authenticated device identity with explicit pairing and certificate/key material unavailable to models and normal evidence logs;
- messages carry versioned JSON metadata; screenshot/artifact bytes are content-addressed and transferred separately from control metadata;
- transport reconnect never implies action resume;
- transport authentication proves endpoint identity only and grants no Track A mutation authority.

The exact library and port are implementation details. The security invariants above are part of the contract.

The owner dashboard remains bound to loopback by default. Optional LAN dashboard exposure is a separate configuration choice and requires explicit owner authentication; it must not reuse Tibia credentials or runtime capability tokens.

## Stable supervisor handoff protocol

### `TaskEnvelope.v1`

Required fields:

```yaml
schema: otclient.local-agent.task.v1
session_id: <id>
task_id: <id>
run_id: <id>
idempotency_key: <unique effect-safe key>
trusted_main_sha: <exact SHA>
client_identity:
  version: <exact version or NOT_APPLICABLE>
  size: <exact size or NOT_APPLICABLE>
  sha256: <exact sha or NOT_APPLICABLE>
objective: <bounded objective>
allowed_actions: [<named actions>]
physical_action_budget: <integer>
max_attempts: <integer>
deadline_epoch_ms: <bounded deadline>
runtime_access: <declared class>
required_evidence: [<evidence kinds>]
secret_capability_ref: <opaque ref or null>
```

Raw credentials are forbidden. Duplicate `idempotency_key` values must never repeat a physical effect.

### `AgentEvent.v1`

Required fields:

```yaml
schema: otclient.local-agent.event.v1
session_id: <id>
run_id: <id>
seq: <strictly increasing integer>
observed_epoch_ms: <time>
provenance: OWNER | SUPERVISOR | SYSTEM | MODEL | SENSOR | RUNTIME
kind: <event kind>
state_before: <state>
state_after: <state>
artifact_refs: [<hash/ref>]
action_id: <id or null>
```

Events are append-only. A later correction is another event, not an in-place history rewrite.

### `ResultEnvelope.v1`

Required fields:

```yaml
schema: otclient.local-agent.result.v1
session_id: <id>
run_id: <id>
status: PASS | FAIL | INCONCLUSIVE
trusted_main_sha: <exact SHA>
final_state: <reconciled state>
action_count: <integer>
physical_action_budget: <integer>
evidence_manifest_sha256: <sha256>
unresolved_conflicts: [<items>]
```

## State model

Keep operational state separate from semantic Tibia state.

### Operational session state

```text
OFFLINE
IDLE
OBSERVING
RUNNING
WAITING_MODEL_SLOT
PAUSED
PAUSED_AUTHORITY
DEGRADED
STOPPED
TERMINAL
```

`STOPPED` is latched. Service restart preserves the latch. No effect is allowed until an explicit owner `RESUME` is accepted and current authority is freshly reconciled.

### Visual state

The vision sensor may report:

```text
UNKNOWN
LOGIN_SCREEN
CHARACTER_SELECT
WORLD_VISUAL
WORLD_EXIT_VISUAL
ERROR_SCREEN
```

`WORLD_VISUAL` is deliberately not `IN_GAME`.

### Runtime/semantic state

Runtime adapters may report only the semantics their reviewed source can establish. A confirmed world state requires the separately reviewed stronger current signal set, such as exact-current `gameWindowState` and/or world-entry causal evidence. Visual/runtime disagreement produces `CONFLICT` or `INCONCLUSIVE` and blocks state-dependent mutation.

## Capture and vision pipeline

1. Runtime edge captures the exact admitted Kasm/X11 target using the existing read-only capture mechanism or a reviewed equivalent.
2. Capture metadata binds current runtime identity, geometry, monotonic time and full-frame SHA-256.
3. Deterministic preprocessing runs before model inference where useful: crop selection, black/blank detection, perceptual/change hash, fixed template/icon matching and secret-region masking.
4. The model scheduler admits exactly `qwen3-vl:4b-instruct-q4_K_M` at the benchmarked bounded profile first unless a later reviewed benchmark changes the choice.
5. Qwen emits strict `VisualEvidence`; model-authored authority/provenance fields are rejected.
6. The reconciler combines visual evidence with current runtime evidence according to deterministic rules.
7. OCR strings remain observation data and are never executed as instructions.

Do not rerun the whole PR #790 model bake-off merely to implement this design. Reuse its frozen fixtures and hard gates, then add representative secret-safe captures only when a later runtime task is legally admitted.

## Local model scheduler

The session service owns a single logical model slot for work it starts.

Rules:

- inspect current residency before every inference;
- zero resident models -> load exact target;
- exact owned target resident -> reuse within bounded keep-alive;
- another or unowned model resident -> `WAITING_MODEL_SLOT`, no inference and no forced eviction;
- switching from an owned model -> unload, verify empty, then load next exact model;
- release task-loaded models on terminal/idle boundaries when practical;
- Qwen3-VL is the visual loop model; Gemma/local-worker text work is optional and queued rather than run concurrently.

The persistent agent identity is the `session_id`, not a permanently resident model. Owner chat can therefore remain one agent session while model calls are serialized.

## Owner dashboard and chat

The dashboard is served by the session service and must show:

- session ID, heartbeat, operational state and current task/run;
- trusted `main` SHA and exact-client identity when applicable;
- latest secret-safe frame/crop plus SHA-256;
- visual class/confidence/OCR explicitly labeled visual-only/untrusted;
- stronger runtime signals and visual/runtime agreement status;
- requested, authorized, performed and reconciled action states;
- physical action budget and count;
- ordered event timeline with provenance;
- final result and evidence-manifest reference.

Owner chat messages are recorded with `OWNER` provenance. Natural-language content may be supplied to a bounded model when appropriate, but control tokens are parsed by deterministic control-plane code before any model sees them.

Required controls:

```text
PAUSE
STOP
RESUME
SCREENSHOT
```

Precedence:

1. SYSTEM safety/authority faults block effects.
2. OWNER `STOP`/`PAUSE` blocks effects.
3. SUPERVISOR tasks apply only inside system/owner constraints.
4. MODEL output is observation/proposal only.

`SCREENSHOT` is read-only. `RESUME` cannot bypass current runtime admission or authority checks.

## Named action contract

The initial mutation vocabulary is deliberately small and versioned. Candidate future actions are:

```text
SUBMIT_AUTHORIZED_LOGIN
SELECT_CHARACTER
ENTER_WORLD
EXIT_WORLD
```

`SCREENSHOT` is read-only and outside the physical mutation budget.

Each mutating action definition contains:

- action schema/version;
- allowed source state(s);
- expected terminal state(s);
- required current runtime authority class;
- required Track A gates and locks;
- maximum low-level input event count;
- maximum attempts;
- deadline;
- reconciliation rule;
- whether a credential capability is required.

The model may propose a named action but cannot approve it. The deterministic orchestrator checks the current task's allowed action set and remaining budget. The runtime edge then independently rechecks current Track A authority before effect.

Every actual low-level key/mouse event consumes budget. A failed attempt still consumes the events already sent. The design provides no unrestricted gameplay action family.

## Track A authority adapter

The adapter is a consumer of trusted-main governance, not a replacement authority system.

Before every future mutating transaction it must independently prove all requirements applicable to that transaction, including:

- current exact client fence;
- current runtime target uniqueness;
- current canonical registration/lease state;
- Gate A and any required rebind/recovery/bootstrap transition;
- Gate B when applicable;
- whole-lifetime cancellation-safe supervisor semantics;
- `input.lock` held from final target validation through physical effect and immediate reconciliation;
- current task-specific action authorization and budget.

The adapter must extend/reuse the existing Control Center guarded-dispatch transport. It must not create a parallel raw process-control path.

A stale or missing gate produces `PAUSED_AUTHORITY`. It never causes an implicit bootstrap, rebind, recovery or authority expansion unless the later task explicitly authorizes that exact transition.

## Credential broker boundary

Credential implementation is deferred to a separately authorized phase, but its interface is fixed now.

The model and session service use only an opaque `secret_capability_ref`. A request such as `SUBMIT_AUTHORIZED_LOGIN` is delivered to the runtime edge without secret values.

The future broker must:

- resolve the capability only at the physical effect edge;
- keep raw values out of model prompts, dashboard/chat, event metadata, evidence and logs;
- scrub secret environment variables before any external helper/client/observer process as demonstrated by the existing Track A secret-wrapper pattern;
- expose no generic `get_secret` API to the model or supervisor;
- zero/delete transient material as soon as practical after the one bounded action;
- never persist secret values in the canonical registration or agent session database.

During secret entry, capture to the vision model is suspended or deterministic secret-field regions are masked before transfer. Raw frames showing populated credential fields must not be persisted.

## Evidence model

Each run has one append-only event ledger and one terminal content-addressed manifest.

The manifest records at minimum:

```yaml
run_id: <id>
trusted_main_sha: <sha>
client_identity:
  version: <value>
  size: <value>
  sha256: <value>
captures:
  - full_sha256: <sha>
    crop_sha256: <sha or null>
    secret_safe: true
visual_observations:
  - class: <value>
    confidence: <value or null>
    model_profile: <exact id>
runtime_signals: [<typed refs>]
actions:
  - requested: <named action>
    authorized: <bool>
    performed: <bool>
    low_level_event_count: <count>
    before_state: <state>
    after_state: <state>
timings: <bounded timing data>
terminal_status: PASS | FAIL | INCONCLUSIVE
```

Evidence retains hashes and typed metadata rather than raw secret material. Artifact/hash mismatch invalidates the affected evidence; the recorder never silently rewrites provenance.

## Failure and recovery

- **Session heartbeat lost:** transition to `DEGRADED`/`PAUSED`; no new effect.
- **Runtime edge disconnected:** preserve state and evidence; no automatic replay after reconnect.
- **Capture failure:** bounded sensor retry only; then `INCONCLUSIVE`.
- **Qwen/model failure:** bounded inference retry only; never compensate with GUI input.
- **Unexpected model residency:** `WAITING_MODEL_SLOT`; no parallel inference and no unowned eviction.
- **Visual/runtime disagreement:** `CONFLICT`; no state-dependent action.
- **Authority/lease/Gate/lock failure:** `PAUSED_AUTHORITY`; no effect.
- **Effect was sent but outcome is unknown:** record `PERFORMED_UNKNOWN`; reconcile from observations and never automatically replay the same action.
- **Owner PAUSE/STOP:** latch control immediately; cancellation cannot be treated as success.
- **Service restart:** restore ledger and control latch; require fresh edge/runtime/authority reconciliation before later effects.
- **Evidence integrity failure:** terminal `FAIL` or `INCONCLUSIVE` according to the missing evidence requirement; do not repair hashes in place.

## Delivery matrix

| Layer | Decision | Design |
|---|---|---|
| capture producer | EXTEND/REUSE | Kasm X11/ffmpeg read-only capture behind runtime admission |
| vision/OCR sensor | REUSE/EXTEND | PR #790 `VisualEvidence`, Qwen3-VL bounded profile, representative fixtures later |
| deterministic classifiers | NEW/EXTEND | blank/change/template/masking before model inference |
| runtime signal adapters | REUSE | exact-current `gameWindowState`, world-entered and other reviewed Track A signals |
| agent state machine | NEW | persistent Molehill operational and reconciled state |
| decision/orchestration layer | NEW | deterministic policy around untrusted model proposals |
| bounded action executor | NEW | named-action executor behind Track A authority adapter |
| credential abstraction | NEW, DEFERRED EFFECT | opaque capability interface now; secret implementation later |
| Track A authority adapter | EXTEND/REUSE | canonical lease/Gates/rebind/recovery/guarded-dispatch/`input.lock` |
| evidence recorder | NEW | append-only events + content-addressed manifest |
| supervisor handoff | NEW THIN BRIDGE | versioned Task/Event/Result envelopes, preferably separate MCP surface |
| dashboard | NEW | same session-service backend; loopback default |
| owner chat/control | NEW | provenance-aware timeline plus deterministic PAUSE/STOP/RESUME/SCREENSHOT |
| local worker MCP | REUSE | low-risk text/extraction only; no high-risk expansion |
| CUA REPL | DEFERRED / NOT PRIMARY | remain disabled |
| Hermes tool loop | REUSE EXISTING ONLY | batch/isolation use; not persistent agent runtime |
| unrestricted gameplay | NOT NEEDED | explicitly outside scope |

## Testing strategy

### Phase 0 — pure control plane

Unit/TDD coverage for schemas, state machine, provenance, action budgets, idempotency, owner-control precedence, crash recovery and append-only evidence. All adapters are fake. Physical action budget remains zero.

### Phase 1 — offline vision

Reuse PR #790 fixtures and hard gates. Test deterministic preprocessing, Qwen profile admission, strict `VisualEvidence`, negative controls and model-slot serialization. No official runtime access.

### Phase 2 — runtime-edge read-only integration

Only under a separately admitted task, test edge transport, exact runtime identity, screenshot hashing/masking and reviewed runtime-signal adapters. No GUI input, credentials or login.

### Phase 3 — bounded executor on non-Tibia dummy X11 target

Test named-action translation, budget accounting, timeout/cancellation, before/after reconciliation, PAUSE/STOP dominance and duplicate-effect prevention without touching the official client.

### Phase 4 — credential broker security validation

Separately authorized implementation and audit proving secrets cannot reach models/events/logs/client child environments outside the narrow injection boundary. Still no official-service login until another explicit runtime authorization.

### Phase 5 — staged official-client transitions

Each transition requires a separate current task/runtime admission and exact Track A authority. Progress narrowly from read-only capture to one authorized transition at a time. No gameplay expansion is implied.

## Implementation sequencing after written-spec approval

1. Create the repository implementation plan using the repository planning workflow.
2. Implement session schemas/state/evidence and fake adapters first.
3. Add the separate supervisor-facing bridge without modifying the risk boundary of `local_worker_server.py`.
4. Add deterministic vision adapter and exact Qwen model-slot handling.
5. Add the authenticated runtime-edge transport and read-only adapters.
6. Add dashboard/chat/control over the same session backend.
7. Add the Track A authority adapter by wrapping existing guarded mechanisms.
8. Add dummy-target named executor and exhaustive safety tests.
9. Stop again before any credential implementation or official-client physical effect unless the current task explicitly authorizes that phase.

Do not implement all later physical phases in one authorization merely because the control plane exists.

## Expected implementation ownership

The implementation plan should keep two narrow ownership domains:

- **local supervisor/control plane:** new agent-session, dashboard, model-scheduler and supervisor-bridge modules under the existing Molehill supervisor root, with tests and explicit local security policy updates;
- **repository Track A edge:** only the smallest new adapters/contracts needed to connect the session service to existing capture/runtime/guarded-dispatch primitives, plus deterministic tests and governance documentation.

Avoid unrelated refactors of existing supervisor, Control Center, canonical transition, Kasm bootstrap or vision benchmark code.

## Acceptance criteria

The architecture implementation cannot be called complete unless all applicable criteria are proven on the exact implementation head:

1. persistent session survives service reconnect/restart without silently resuming effects;
2. owner `STOP`/`PAUSE` dominates model/supervisor requests and remains latched across restart;
3. duplicate task/action idempotency never repeats a physical effect;
4. only one local model is resident/inferencing at a time and unexpected foreign residency fails closed;
5. Qwen output remains visual-only and cannot promote `IN_GAME`;
6. stronger reviewed runtime evidence is required for semantic world confirmation;
7. model-facing tools expose only named actions, never raw click/type/shell/process-control;
8. current Track A guard/Gate/lock semantics cannot be bypassed through the new bridge;
9. raw Tibia credentials cannot appear in model inputs, dashboard/chat, events, evidence or long-lived process environments;
10. evidence bundles bind run/main/client/capture/action/timing/outcome and detect hash tampering;
11. dashboard shows current heartbeat, provenance, sensors, authority, budget and before/after action status;
12. runtime ambiguity, effect uncertainty or transport loss fails closed without automatic replay;
13. focused/component/integration tests and fresh independent audit have no material finding;
14. any official-client E2E is separately authorized and proves only its bounded transition;
15. unrestricted gameplay remains absent.

## Written-spec approval gate

This specification intentionally stops before implementation planning.

After self-review, the owner must explicitly approve this written spec. Only then may the coordinator invoke the repository planning workflow. Approval of the earlier architectural direction does not by itself approve implementation or physical runtime effects.