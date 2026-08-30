# OTC-20260830 local vision-agent supervisor discovery

## Current checkpoint

The owner approved the recommended architecture direction (`Approach C`) on 2026-08-30.

The formal written design is committed at:

`docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`

The written spec has been self-reviewed for placeholders, internal contradictions, ambiguity, scope expansion and authority leakage. No material defect was found. The task now stops at the required second gate: explicit owner approval of the written spec before implementation planning.

This report and spec remain design evidence only. They do not authorize implementation, official-client observation, credentials, login, character selection, GUI input, process control, process-memory access, gameplay, CUA enablement or semantic promotion.

## Verified repository state at design

- trusted `main`: `18ff83053f5c5d85c9bce6debab0f7fef6b79ecd` (merged PR #801);
- PR #808: open Draft on `docs/OTC-20260830-local-vision-agent-supervisor-discovery`;
- PR #790: merged vision benchmark authority;
- current Track A admission/Kasm/hybrid-routing contracts remain authoritative and fail closed;
- `input.lock`, guarded Control Center dispatch, exact-current `gameWindowState` qualification and world-entry anchors already exist on trusted main and are reuse targets rather than new authority implementations.

Current task boundary remains:

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

## Verified Molehill supervisor state

Fresh read-only inspection confirmed the existing supervisor root at:

`C:/Users/barte/Documents/ChatGPT/llm/supervisor`

Relevant reusable surfaces:

- `supervisor.ps1`;
- `mcp/local_worker_server.py` and its tests/README;
- `policies/LOCAL_MODEL_ROUTING.yaml`;
- `policies/SECURITY_POLICY.md`;
- local Ollama runtime and benchmark/evidence directories;
- pinned Hermes container integration and fixed-target Ollama proxy design.

Observed state at design time:

```text
Ollama API: ready
Ollama version: 0.32.14
Docker: ready
muse-ollama-proxy: Exited (255)
local_worker_server --self-test: PASS
cua_repl: present, enabled=false
ollama resident models: none
```

Installed models included `qwen3-vl:4b-instruct-q4_K_M`, `gemma4:12b`, `qwen3.5:9b`, `qwen2.5-coder:14b`, `gpt-oss:20b` and `muse-glimmer:latest`.

No supervisor/proxy service was started or modified by this task.

## Vision authority

Merged PR #790 remains the benchmark source of truth.

Leading tested profile:

```text
qwen3-vl:4b-instruct-q4_K_M
sha256: ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
num_ctx: 4096
num_predict: 256
temperature: 0
```

Bounded evidence:

- login classification `3/3`;
- expected-text recall `1.0`;
- black no-text false text `0/3`;
- false `IN_GAME_VISUAL` `0/3`;
- all hard gates PASS;
- final model residency empty.

OvisOCR2 matched expected-text recall but fabricated non-empty text on black negative controls `3/3` under both tested prompt profiles and remains unpromoted.

Architecture consequence: Qwen3-VL is the first sensor to integrate, not a semantic authority. OCR/vision can never independently promote `IN_GAME`.

## Approved architecture direction

Use a thin persistent Molehill session/control service plus a narrow Track A runtime edge.

The Molehill control plane owns persistent session/heartbeat, owner chat/control, provenance, model scheduling, deterministic reconciliation, evidence and the supervisor protocol. It owns no Track A mutation authority and sees no raw Tibia credentials.

The Synology/Kasm runtime edge owns only bounded physical adapters: capture, stronger runtime signals, authority reconciliation, named-action execution and a future separately authorized credential injection boundary. It does not contain an autonomous planner.

Primary control flow:

```text
owner / supervising ChatGPT-Codex
        -> persistent session service
        -> deterministic prefilter + Qwen3-VL VisualEvidence
        -> state reconciler + stronger runtime signals
        -> current Track A authority adapter
        -> bounded named action
        -> before/after evidence
        -> ResultEnvelope + evidence manifest
```

CUA remains disabled and is not the primary executor. Hermes remains an existing bounded isolation/batch tool, not the persistent agent runtime.

## Important written-spec decisions

The formal design fixes these boundaries:

- versioned `TaskEnvelope.v1`, `AgentEvent.v1`, `ResultEnvelope.v1`;
- append-only event provenance (`OWNER`, `SUPERVISOR`, `SYSTEM`, `MODEL`, `SENSOR`, `RUNTIME`);
- owner `STOP`/`PAUSE` dominance and restart-persistent latch;
- operational state kept separate from visual and runtime semantic state;
- `WORLD_VISUAL` explicitly distinct from semantic `IN_GAME`;
- one-local-model-slot scheduler with no forced eviction of an unexpected resident model;
- named model-facing actions only, with no raw coordinate click, arbitrary type, shell or process-control tool;
- explicit action budgets, bounded attempts and idempotency to prevent duplicate physical effects;
- Track A authority adapter reusing canonical guarded-dispatch/Gates/registration/lease/rebind/recovery/`input.lock` semantics;
- opaque credential capability interface; exact secret implementation deferred and separately authorized;
- screenshot suppression/masking during future secret entry;
- append-only evidence plus content-addressed manifest;
- loopback owner dashboard by default and authenticated local-network edge transport;
- no unrestricted gameplay action family.

## Delivery matrix summary

| Layer | Decision |
|---|---|
| capture producer | reuse/extend existing Kasm capture |
| vision/OCR | reuse PR #790 Qwen3-VL semantics |
| deterministic classifiers | new/extend |
| runtime signals | reuse reviewed Track A sources |
| persistent agent state machine | new |
| deterministic orchestration | new |
| bounded action executor | new |
| credential abstraction | new interface, secret effect deferred |
| Track A authority adapter | reuse/extend existing canonical control |
| evidence recorder | new |
| supervisor handoff | new thin bridge |
| dashboard/chat/control | new in same session backend |
| existing local-worker MCP | reuse unchanged high-risk boundary |
| CUA | deferred, disabled |
| Hermes persistent planner | not needed |
| unrestricted gameplay | out of scope |

## Self-review result

`PASS_BOUNDED` for the design document.

Checks performed:

- no `TODO`/`TBD` or unresolved placeholder requirement;
- no contradiction with approved Approach C;
- no model authority or OCR semantic-promotion path;
- no credential exposure path;
- no implicit runtime/login/input authority;
- no bypass around existing Track A canonical guards;
- no simultaneous-model design;
- no unrestricted gameplay scope;
- implementation sequence stops before credential implementation and official-client physical effects unless a later task explicitly authorizes them.

## Next gate

Current blocker:

`OWNER_WRITTEN_SPEC_APPROVAL_REQUIRED`

Exactly one next action is durable in the task record: the owner reviews and explicitly approves or requests changes to `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`. Only after written-spec approval may the repository planning workflow be invoked.