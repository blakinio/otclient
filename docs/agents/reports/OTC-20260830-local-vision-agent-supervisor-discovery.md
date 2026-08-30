# OTC-20260830 local vision-agent supervisor discovery

## Purpose and authority

This checkpoint records the architecture design for reusing the owner's existing local Ollama/supervisor stack as the foundation for a future observable Track A vision/OCR research agent.

This report is discovery/design evidence only. It does **not** authorize implementation, official-client observation, credentials, login, character selection, GUI input, process control, process-memory access, gameplay or semantic promotion. The current task remains `runtime_access: none`, `implementation_authorized: false`, `physical_action_budget: 0`.

## Verified current state

Live GitHub state was revalidated before design. `main` remains `18ff83053f5c5d85c9bce6debab0f7fef6b79ecd`, the merge of PR #801 (`feat(track-a): add Kasm canonical bootstrap`). PR #808 remains an open Draft on `docs/OTC-20260830-local-vision-agent-supervisor-discovery`; no overlapping open local-vision/CUA agent PR was found.

Trusted-main Track A contracts still require explicit task authority and the applicable exact-client fence, canonical admission/lease/rebind/recovery, Gate A/Gate B, whole-lifetime supervisor and `input.lock` boundaries before a future physical effect. `runtime_access: none` cannot be silently expanded into observation or mutation authority.

Additional trusted-main components discovered during architecture reconciliation materially reduce the amount of new code required:

- `.github/scripts/tibia-official-client-re-control-center-bridge-transport.py` already constrains Control Center dispatch to the canonical `guarded-dispatch` transition process, exact repo-owned probe/worker paths, no shell and private stdin/stdout pipes; its test also verifies that the transport never reads token-file contents;
- `.github/scripts/tibia-official-client-re-input-lock.py` already provides fail-closed cross-process GUI/input serialization with cancellation and bounded acquisition;
- `.github/scripts/track_a_game_window_state_qualification.py` already provides exact-client, read-only `gameWindowState` qualification with change events, heartbeat, identity revalidation and fail-closed behavior while explicitly refusing semantic promotion;
- `.github/scripts/track_a_current_world_entered_anchor.py` and related durable-state logic already provide exact-current stronger causal anchors for world entry;
- `.github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh` and its helper already demonstrate a secret-handling pattern where credential variables are scrubbed from external child environments and the client/observer processes are checked for leakage.

These mechanisms remain governed by their own runtime authority. Their existence is reuse evidence, not permission to invoke them from this task.

## Existing local supervisor state

A fresh read-only inspection of `C:/Users/barte/Documents/ChatGPT/llm/supervisor` on Molehill-PC confirmed:

- `supervisor.ps1`, `mcp/local_worker_server.py`, `mcp/README.md`, `policies/LOCAL_MODEL_ROUTING.yaml`, `policies/SECURITY_POLICY.md`, benchmark/evidence directories and the pinned Hermes integration are present;
- `local_worker_server.py --self-test` still returns `local_worker_server self-test passed`;
- `mcp_servers.local_workers` remains registered in the local Codex configuration;
- `mcp_servers.cua_repl` remains present but `enabled = false`;
- Ollama API is ready on `0.32.14`; Docker is ready; `muse-ollama-proxy` remains `Exited (255)` and was not started or modified;
- `ollama ps` was empty, so no local model was resident at readback;
- `qwen3-vl:4b-instruct-q4_K_M`, `gemma4:12b`, `qwen3.5:9b`, `qwen2.5-coder:14b`, `gpt-oss:20b` and `muse-glimmer:latest` remain installed.

The local worker is intentionally a bounded, mostly stateless low-risk text/file delegation surface. Its policy explicitly reserves architecture, security and authentication/credential decisions for the stronger coordinator and treats every local-model output as untrusted. It is therefore a reusable subworker, not the correct place to embed persistent agent session state or Track A authority.

Hermes is currently integrated as a pinned, isolated batch audit/tool-loop container behind a fixed Ollama proxy. It is useful isolation plumbing but is not currently a persistent session/control/dashboard service. Making it the primary Track A agent runtime would add a second planning/authority layer without solving the required owner-control and evidence semantics.

## Existing Tibia vision evidence

Merged PR #790 remains the vision benchmark authority. Its terminal result is `PARTIAL`, not a formal `PRIMARY_MODEL`, because representative selection-quality Tibia/Track B screenshots were unavailable. The leading tested profile remains:

```text
qwen3-vl:4b-instruct-q4_K_M
sha256: ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
num_ctx: 4096
num_predict: 256
temperature: 0
```

Verified bounded smoke evidence remains login classification `3/3`, expected-text recall `1.0`, black no-text false-text `0/3`, false `IN_GAME_VISUAL` `0/3`, all hard gates PASS and final model residency empty. OvisOCR2 matched positive text recall but fabricated non-empty text on black controls `3/3` under both tested prompt profiles and remains unpromoted.

Architecture consequence: Qwen3-VL is the first local visual sensor to use for representative evidence, but its output remains `visual_only` and `structural_authority: false`. The full benchmark should not be re-run merely to design this system.

## Architectural approaches compared

### Approach A - CUA-centric local operator

Use the disabled `cua_repl` as the primary capture/action surface and let the local agent drive desktop interaction through broad computer-use primitives.

Advantages: fastest route to a generic GUI operator and least bespoke executor code.

Costs: authority is much broader than the required Track A action vocabulary; binding every click/keypress to canonical lease/Gate A/Gate B/`input.lock`/exact-client state is harder; evidence and action budgets become indirect; the currently disabled CUA surface is not a tested Track A primitive. This is rejected as the primary physical-effect path.

### Approach B - Hermes-centric persistent tool-loop

Turn the existing pinned Hermes container into the persistent local planner and expose capture, vision, runtime and action tools to it.

Advantages: existing container isolation, safe-mode conventions and fixed Ollama proxy can be reused.

Costs: the current Hermes integration is batch/audit oriented; it introduces an extra autonomous planning layer between the owner/supervisor and Track A authority; persistent state/dashboard/control provenance still has to be built; model-residency and authority boundaries become more complex. This is rejected as the primary runtime. Hermes may remain a deferred bounded subworker if a future concrete use case justifies it.

### Approach C - thin persistent session service + narrow Track A runtime edge

Keep ChatGPT/Codex as the architectural/supervising coordinator. Add one small persistent local agent-session service on Molehill that owns session state, dashboard/chat, event/evidence recording, model scheduling and the supervisor protocol. It consumes sensors and proposes only named high-level actions. Physical Track A capture/signals/effects stay behind a narrow runtime-edge adapter that reuses canonical trusted-main guard/transition/lock mechanisms.

Advantages: smallest coherent extension of what already exists; explicit owner control; no second agent platform; deterministic authority remains outside the model; clean separation of visual evidence from semantic promotion; direct reuse of existing Track A infrastructure.

Cost: one new persistent service and a small set of adapters/schemas must be built and tested.

**Recommendation: Approach C.**

## Recommended component boundaries

The future system should have two trust/placement zones.

### Molehill local control plane

1. **Existing supervisor lifecycle / Ollama** - reuse and minimally extend for one-model-at-a-time admission and health reporting. A model-residency conflict must fail closed; the agent must not evict an unexpected foreign resident model merely to continue.
2. **New agent session service** - persistent session ID, task/run state machine, heartbeat, owner/supervisor/model/system provenance, control precedence, bounded orchestration and restart recovery.
3. **Vision sensor adapter** - reuse PR #790 `VisualEvidence` semantics and exact Qwen3-VL profile. Deterministic crop/hash/change/template checks run before model inference where cheaper. Qwen produces observations only.
4. **Existing local worker MCP** - reuse only for low-risk bounded text/extraction tasks. It is not the session runtime and never gains architecture/security/credential authority.
5. **New evidence recorder** - append-only event ledger plus content-addressed artifact manifest; terminal export is a portable evidence bundle.
6. **New dashboard/chat surface** - served by the same session service to avoid a second backend. Loopback is the default exposure; LAN exposure is opt-in and must have explicit authentication/session protection.
7. **New thin supervisor bridge** - versioned task/result/event protocol exposed to ChatGPT/Codex, preferably by a separate narrow MCP adapter rather than adding high-risk capabilities to `local_worker_server.py`.

### Track A physical runtime edge

1. **Capture adapter** - extend/reuse the existing Kasm X11/`ffmpeg x11grab` observation path. Capture is read-only and separately admitted when a later task allows it.
2. **Runtime signal adapters** - reuse exact-client and `gameWindowState`/world-entered/current-runtime evidence producers. They remain stronger corroboration than OCR and keep their existing fail-closed semantics.
3. **Track A authority adapter** - a thin adapter over the canonical registration/lease/rebind/recovery/Gate A/Gate B/live-guard/whole-lifetime supervisor/`input.lock` mechanisms. It must not reimplement or fork those contracts.
4. **Bounded action executor** - new narrow executor behind the authority adapter. Its model-facing vocabulary is named semantic actions, never arbitrary shell, unrestricted coordinate clicking or arbitrary typed text.
5. **Credential broker boundary** - future separately-authorized secret injection at the effect edge. The model, dashboard chat, task envelopes and evidence must never contain raw credential values.

The runtime-edge transport should extend the existing Control Center guarded-dispatch path rather than inventing a parallel bypass. The persistent Molehill service sends capability-bounded requests; the edge independently revalidates current authority before every physical-effect transaction.

## End-to-end data and control flow

```text
OWNER dashboard/chat                     SUPERVISING ChatGPT/Codex
        |                                           |
        +-------------- control/task ---------------+
                            |
                  agent session service
                   /       |        \
          event/evidence  model      supervisor bridge
              ledger      scheduler
                           |
                  deterministic vision prefilter
                           |
                     Qwen3-VL sensor
                           |
                     VisualEvidence
                           |
                    state reconciler
                     /           \
             visual state      runtime signals
                                   |
                           Track A runtime edge
                                   |
                    authority adapter / input.lock
                                   |
                       bounded named executor
                                   |
                      before/after observation
                                   |
                  terminal evidence/result bundle
```

A state such as `WORLD`/`IN_GAME` may be visually suggested, but semantic promotion requires the applicable reviewed stronger runtime evidence. Visual/runtime disagreement produces `CONFLICT`/`INCONCLUSIVE`, never an optimistic promotion.

## Supervisor handoff protocol

Use stable versioned envelopes independent of transport.

`TaskEnvelope.v1` should carry: `session_id`, `task_id`, `run_id`, `trusted_main_sha`, exact-client identity/fence, bounded objective, allowed named actions, physical action budget, retry/time limits, required evidence, runtime-authority class, idempotency key and optional opaque secret capability reference. It must contain no raw credentials.

`AgentEvent.v1` should carry: monotonically increasing sequence, timestamp, provenance (`OWNER`, `SUPERVISOR`, `SYSTEM`, `MODEL`), state transition, sensor/runtime observation references, action proposal/approval/performance state and artifact hashes.

`ResultEnvelope.v1` should carry: `run_id`, terminal `PASS | FAIL | INCONCLUSIVE`, final reconciled state, evidence-manifest hash/reference, action counts/budget consumption and unresolved conflicts.

The transport can be a narrow local MCP/HTTP bridge, but the envelope is the contract. Duplicate `TaskEnvelope` idempotency keys must not repeat physical effects.

## Dashboard and owner chat behavior

The dashboard should show one live session with:

- session/heartbeat and current deterministic state;
- latest secret-safe screenshot/crop and its SHA;
- latest visual classification/confidence and OCR text marked untrusted/visual-only;
- stronger runtime signals and whether they agree with visual evidence;
- requested, approved and performed named action with before/after states;
- current physical action budget/count;
- event timeline with explicit provenance;
- terminal result/evidence bundle link.

Owner chat and supervisor messages share the session timeline but never collapse provenance. `OWNER` control commands are parsed as control-plane commands, not prompts for the model.

Control precedence is fail-closed:

1. SYSTEM safety/authority fault blocks physical effects;
2. OWNER `STOP`/`PAUSE` dominates supervisor/model activity;
3. SUPERVISOR task/capability instructions apply only inside owner/system constraints;
4. MODEL output is a proposal/observation only.

`STOP` latches immediately and forbids new effects. `PAUSE` preserves state/evidence but forbids effects. A restart never auto-resumes a previously paused/stopped physical session. `SCREENSHOT` is an explicit read-only request and never carries effect authority. An owner-originated pause cannot be overridden by the model or supervisor.

## Credential boundary

Raw secrets must never be model inputs, chat payloads, dashboard events, OCR targets, task/result envelopes or logs.

The future model requests only an abstract named action such as `SUBMIT_AUTHORIZED_LOGIN`. The runtime edge resolves an opaque, separately-authorized credential capability locally and performs the secret-bearing keystrokes inside the smallest possible effect boundary. The existing Track A secret-wrapper pattern is reusable evidence for environment scrubbing, but the exact future credential store/provider remains **deferred and separately authorized**.

During secret entry, raw frames containing populated secret fields must not be sent to Qwen or persisted. The preferred design is to suppress capture during the injection interval and/or deterministically mask configured secret-field regions before any image leaves the runtime edge. Evidence records only the abstract action and its before/after state, not the secret values.

## Action authority and budgets

The model must never receive raw `click(x,y)`, arbitrary `type(text)`, shell or process-control tools. It may propose only a versioned allowlist such as future `SUBMIT_AUTHORIZED_LOGIN`, `SELECT_CHARACTER`, `ENTER_WORLD`, `EXIT_WORLD`, plus read-only `SCREENSHOT`.

Each mutating named action has an explicit expected source state, expected terminal state, maximum low-level input count, maximum attempts and deadline. The executor reserves/charges the physical budget before effect. Every actual low-level input event counts. Retries are bounded and consume budget.

Before each mutating transaction, the Track A authority adapter independently proves the applicable current exact-client fence, canonical target/lease/gates/rebind state, whole-lifetime supervisor and `input.lock`. Missing, stale or ambiguous authority returns a blocked state; it does not silently bootstrap, rebind or widen authority unless the later task explicitly authorizes that transition.

No unrestricted gameplay action family is part of this architecture.

## Failure and recovery behavior

- heartbeat loss, runtime-edge loss or stale session -> `PAUSED`/`DEGRADED`, no physical effect and no automatic resume;
- capture or Qwen failure -> bounded sensor-only retry; then `INCONCLUSIVE`, without compensating GUI input;
- visual/runtime disagreement or ambiguous screen -> `CONFLICT`/`UNKNOWN`, no action;
- exact-client/lease/Gate/input-lock/whole-lifetime-supervisor failure -> `PAUSED_AUTHORITY`, no action;
- unexpected local model residency -> `WAITING_MODEL_SLOT`, no parallel inference and no forced eviction of an unowned model;
- executor outcome unknown after an effect -> `PERFORMED_UNKNOWN` and reconciliation only; do not automatically replay a possibly already-delivered physical action;
- service restart -> restore event ledger, preserve owner STOP/PAUSE latch, require fresh runtime/authority reconciliation before any later effect;
- evidence hash mismatch -> invalidate the affected run/evidence instead of repairing provenance.

## Testing strategy for a later implementation

1. Schema/state-machine unit tests: versioned envelopes, provenance, precedence, idempotency, action budgets, STOP/PAUSE latching and restart recovery.
2. Offline replay tests: PR #790 frozen images plus synthetic runtime events; zero physical input.
3. Vision integration tests: exact Qwen3-VL profile against existing fixtures first, then separately admitted representative secret-safe captures; preserve PR #790 hard gates instead of re-running an unrelated model bake-off.
4. Security tests: prove raw credentials cannot enter prompts/events/logs/evidence; reject raw model click/type/shell requests; verify masking/suppression around credential injection.
5. Single-model residency tests: only one local model resident/inferencing at a time; foreign/unexpected residency fails closed.
6. Track A adapter contract tests: mock canonical lease/gates/exact-client/live-guard/`input.lock`; prove the new service cannot bypass existing authority.
7. Dashboard/reconnect tests: provenance, event replay, owner control precedence and heartbeat behavior.
8. Crash/ambiguity tests around request -> approval -> effect -> result; idempotency must prevent duplicate physical effects.
9. Only after separate owner/spec/runtime authorization: staged physical tests progressing from read-only capture to dummy X11 actions, then narrowly authorized official-client transition tests. No gameplay expansion.

## Phased implementation sequence after owner approval

The current task stops before implementation. If the owner approves this direction, the next repository step is the required formal design spec under `docs/superpowers/specs/`, followed by self-review and a second owner approval of the written spec.

Only after that gate should planning/implementation be considered in this order:

1. control-plane schemas, persistent session state, evidence ledger and dashboard/chat using fake adapters; physical budget stays zero;
2. offline vision adapter and deterministic preprocessing using PR #790 fixtures under the single-model scheduler;
3. separately-authorized read-only Track A capture/runtime-signal integration through the canonical runtime edge; still no input;
4. narrow named-action executor and authority adapter tested against a dummy/emulated X11 target;
5. separately designed/approved credential broker tested only against a dummy login surface;
6. separately-authorized Track A login/character/world transition E2E with exact client/gates/locks/evidence and bounded action budget.

## Delivery matrix

| Layer | Decision | Reuse / build boundary |
|---|---|---|
| supervisor lifecycle | EXTEND EXISTING | reuse `supervisor.ps1`; add health/model-slot integration only |
| capture producer | EXTEND EXISTING | Kasm `ffmpeg x11grab`/runtime-edge adapter; no new desktop platform |
| vision/OCR sensor | EXTEND EXISTING | PR #790 `VisualEvidence` semantics + exact Qwen3-VL profile |
| deterministic classifiers | NEW | crop/hash/change/template/redaction/prefilter layer |
| runtime signal adapters | EXTEND EXISTING | `gameWindowState`, world-entered and exact-current runtime evidence |
| agent state machine | NEW | persistent deterministic session/recovery/control state |
| decision/orchestration | NEW | thin session service; model suggestions remain untrusted |
| bounded action executor | EXTEND + NEW NARROW ADAPTER | canonical Control Center guarded dispatch + named action implementation |
| credential abstraction | NEW, IMPLEMENTATION DEFERRED | opaque capability + edge broker; raw secrets never exposed |
| Track A authority adapter | REUSE + THIN ADAPTER | canonical lease/gates/rebind/live-guard/`input.lock`; do not duplicate logic |
| evidence recorder | NEW + EXTEND | append-only event ledger + PR #790 visual evidence/artifact hashes |
| supervisor handoff | NEW THIN BRIDGE | `TaskEnvelope` / `AgentEvent` / `ResultEnvelope`, transport-neutral |
| dashboard | NEW | same session-service backend; loopback default |
| owner chat/control | NEW | provenance-preserving OWNER/SUPERVISOR/SYSTEM/MODEL timeline |
| pause/stop/recovery lifecycle | NEW | deterministic control plane; no auto-resume |
| existing local worker MCP | REUSE | bounded low-risk text subworker only |
| CUA REPL | DEFERRED / NOT PRIMARY | remain disabled; optional future diagnostic adapter only if justified |
| Hermes tool-loop | DEFERRED / NOT NEEDED | retain existing isolation/audit use; not primary session runtime |
| unrestricted gameplay | NOT NEEDED / FORBIDDEN | outside this architecture |

## Owner approval hard gate

Recommended direction: **Approach C - persistent Molehill session/control service plus a narrow canonical Track A runtime edge, Qwen3-VL as visual sensor, deterministic policy/authority outside the model, CUA and Hermes excluded from the primary action path.**

No implementation code, formal design spec, CUA enablement, official-client runtime observation/input, login, credential access or PR merge is authorized by this report.

The single next repository action is owner approval or rejection of this architectural direction. If approved, the following task must write the formal design spec and stop again for owner approval of that written spec before implementation planning.