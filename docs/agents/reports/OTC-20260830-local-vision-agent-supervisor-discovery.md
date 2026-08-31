# OTC-20260830 local vision-agent supervisor discovery

## Current checkpoint

The owner approved both architectural direction **Approach C** and the formal written design on 2026-08-30.

Formal design:

`docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`

Implementation plan:

`docs/superpowers/plans/2026-08-30-local-track-a-vision-agent-supervisor.md`

The plan has completed self-review for scope, cross-task type consistency, API/MCP route semantics, authority boundaries, reuse and deferred trust-boundary work. No implementation has started.

## Verified repository and local state used by the design

Trusted design base remains `main@18ff83053f5c5d85c9bce6debab0f7fef6b79ecd`, the merge of PR #801. PR #808 remains the Draft architecture/planning checkpoint.

Merged PR #790 remains the Tibia vision benchmark authority. Its result is `PARTIAL`, not a formal production model promotion, but the leading tested profile remains:

```text
qwen3-vl:4b-instruct-q4_K_M
sha256: ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
num_ctx: 4096
num_predict: 256
temperature: 0
```

Bounded evidence remains login classification `3/3`, expected-text recall `1.0`, black/no-text false text `0/3`, false `IN_GAME_VISUAL` `0/3`, hard gates PASS. OvisOCR2 remains unpromoted after fabricated text on black controls `3/3` under both tested prompt profiles.

Fresh read-only Molehill inspection established:

- Ollama `0.32.14` ready;
- Docker ready;
- `muse-ollama-proxy` still `Exited (255)` and not changed;
- no resident local model at readback;
- Qwen3-VL and existing text models installed;
- `local_worker_server.py --self-test` PASS;
- `mcp_servers.local_workers` present;
- `mcp_servers.cua_repl` present but `enabled=false`;
- local worker policy keeps architecture/security/authentication/credential decisions outside local-model authority.

No supervisor/proxy state, CUA state, credentials or Official Tibia runtime was changed by this task.

## Approved architecture

The approved design is a **thin persistent control/session plane plus a narrow Track A physical edge**.

- Qwen3-VL is a visual/OCR sensor only.
- Deterministic policy, owner controls and Track A authority remain outside the model.
- CUA remains disabled and is not the primary executor.
- Hermes remains existing bounded isolation/batch tooling, not the persistent planner/runtime.
- Owner `STOP`/`PAUSE` dominates supervisor/model proposals.
- Model-facing operations are named semantic actions, never raw click/type/shell/process-control.
- Raw Tibia credentials never enter model/session/dashboard/evidence channels.
- Visual evidence never independently promotes `IN_GAME`; stronger reviewed runtime evidence is required.
- No unrestricted gameplay action family is designed.

## Planning reconciliation: reuse existing Control Center

A deeper current-main mapping during implementation planning found that the approved Molehill session/control service does not need a second backend. The repository already contains the correct foundation under:

`tools/tibia_re_control_center/`

Reusable merged capabilities include:

- `SQLitePersistentStore` with one SQLite/WAL durable store;
- request idempotency and event/artifact persistence;
- `ControlDomainService` and `MutationCoordinator`;
- durable STOP/reset/recovery semantics;
- loopback-only Control API, UI and CLI with nonce/CSP/no-cookie/no-CORS boundary;
- Package D `OfficialTibiaAdapter` transaction semantics;
- `CanonicalTrackAAuthorityBridge` and guarded-dispatch transport.

Therefore the implementation plan extends Control Center with agent protocol/session/provenance/vision/reconciliation/dashboard/MCP features instead of creating another process model, state store or authority path.

This is an implementation mapping refinement, not a change to the owner-approved architecture.

## Package D current-client safety boundary

The merged `OfficialTibiaAdapter` still carries an older promotion fence than current trusted Track A `15.32.75d4a0 / 52105824 / d1a16819...` governance.

The plan explicitly forbids changing that fence merely to make the future agent actionable. The repository foundation will keep its production action executor unbound. Current-client physical action binding requires a separate reviewed task and fresh Track A runtime authorization.

## PR #615 overlap

Open Draft PR #615 is an older bounded local Ollama PoC. Its branch is not treated as trusted implementation authority and will not be merged or cherry-picked wholesale.

Potentially reusable invariants are independently revalidated in the new plan:

1. loopback-only Ollama transport;
2. exact model digest verification;
3. strict model-output schema validation;
4. secret rejection;
5. single-model residency;
6. deterministic unload/release.

PR #615 may be closed as superseded only after the replacement foundation is merged and final evidence proves all six invariants. Otherwise it remains open with the exact remaining gap recorded.

## Implementation-plan structure

The plan contains ten repository-only tasks:

1. extract PR #790 reusable vision/Ollama safety core;
2. add strict `TaskEnvelope` / `AgentEvent` / `ResultEnvelope` protocol and provenance types;
3. extend the existing SQLite store with durable agent sessions/tasks/results;
4. add the deterministic session coordinator with Null production executor and owner-control precedence;
5. add exact Qwen3-VL model-slot scheduler and visual sensor;
6. add visual/runtime reconciliation with no visual-only world promotion;
7. extend existing Control API/UI/CLI for agent task/chat/control/evidence views;
8. add a separate narrow supervisor MCP surface over Control API only;
9. run fake/offline vertical-slice E2E and security falsification;
10. perform docs, exact-head validation, fresh independent audit and related-PR disposition.

The plan uses TDD and preserves existing Package A/B/C/D and PR #790 regressions.

## Explicitly deferred trust boundaries

The following are **not** hidden implementation steps in this plan:

- Molehill deployment/registration of the new MCP/service integration;
- authenticated production Synology↔Molehill transport and key provisioning;
- live Track A read-only Kasm capture/runtime-signal binding;
- credential broker implementation;
- current-client physical actions for login/character/world transitions.

Each requires a later, separately authorized task. The repository foundation cannot be called an autonomous Tibia operator merely because its control-plane code exists.

## Current authority and requested decision

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

Current gate: choose and explicitly authorize the repository-only implementation workflow.

Recommended execution mode: **Subagent-Driven Development**, because Tasks 1–8 are mostly independently reviewable module/test slices while one coordinator can preserve the shared Control Center contracts and exact safety boundary. **Inline Execution** remains a valid serial alternative.
