---
task_id: OTC-20260819-track-a-parallel-runtime-prompts
status: blocked
agent: ChatGPT
session_role: prompt-author
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: documentation
phase: fresh-independent-prompt-audit-required
execution_mode: github_only
branch: docs/OTC-20260819-track-a-parallel-runtime-prompts
base_branch: main
base_main: a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
related_pr: 543
created: 2026-08-19
updated: 2026-08-19
risk: medium
implementation_authorized: true
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
  - docs/agents/tasks/active/OTC-20260819-track-a-parallel-runtime-prompts.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPT_EVAL_V1.md
modules_touched:
  - official-client-re-prompting
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
  - docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
depends_on:
  - main@a1368bbecd5b6a6bc2447d2c7debb1141efc2dcb
blocks: []
non_overlap:
  - PR #536 owns the full-client coverage checklist/matrix and is not modified.
  - PR #539 owns S10 action-protocol research and is not modified.
  - PR #528 owns native-login continuation and is not modified.
  - PR #475 owns worldmap physical runtime research and is not modified.
  - PR #302 owns direct-player-position research and is not modified.
policy_version: 2
context_pressure: medium
context_growth: stable
estimate_confidence: high
decomposition_decision: single
decomposition_reason: one canonical alias/prompt package plus its prompt-as-code evaluation
validation_level: focused
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
---

# Objective

Persist the owner's complete ready-to-invoke parallel Track A agent prompt package so the owner can use short aliases while workers resolve the full instructions from Git.

The package binds every runtime-capable worker to the current canonical KasmVNC locator contract, live PID/start/exe/XID revalidation, shared GUI coordination, and the owner's current campaign authorization for minimal anti-idle input. It preserves stricter repository rules for login, credentials, process control, client mutation, irreversible economy operations and canonical promotion.

# Prompt contract

```yaml
prompt_contract:
  version: 1.0.0
  changed_surfaces:
    - worker alias registry
    - common Track A shared-runtime worker contract
    - subsystem worker prompts
    - coordinator prompt
    - shared anti-idle/input coordination rule
  objective: short aliases deterministically resolve to complete, safe, non-overlapping parallel research prompts that know the current KasmVNC runtime locator and keep an already-running logged-in session active without duplicate input
  baseline_version: OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION prompt_contract_version 1.0.0 without subsystem runtime aliases
  eval_suite: docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPT_EVAL_V1.md
  rollback_version: docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md@main
```

# Owner authorization captured by this task

Current owner instruction authorizes workers in this prompt family to use the owner-designated shared Track A environment for their bounded research and requires an anti-idle action approximately every ten minutes so the already-running session is not logged out.

This is narrowly encoded as:

- shared read-only observation may run concurrently after live identity/admission checks;
- minimal anti-idle input may be sent only to the freshly proven intended in-game client, using the shared input lock/heartbeat contract;
- preferred anti-idle stimulus is one safe rotation in place; otherwise one safe adjacent step with restoration when practical;
- mission-scoped reversible input may be used only where the worker's task and current Track A admission authorize it;
- this does **not** create standing login, credential, 2FA, character-selection, process-control, debugger/injection, client-byte mutation, purchase/transfer, or irreversible gameplay authority.

# Acceptance

- [x] canonical prompt file contains the common runtime contract and all requested aliases;
- [x] every alias has one bounded subsystem mission and explicit coverage ownership;
- [x] all workers point to `otclient-track-a-kasmvnc`, `DISPLAY=:1`, KasmVNC, and `TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`;
- [x] live process identity requires PID + start ticks + executable + build fence where relevant + XID ownership; historical PID/XID are forbidden as authority;
- [x] shared anti-idle uses one heartbeat and serialized input so many agents do not all move the character independently;
- [x] current owner authorization is bounded and does not silently broaden credentials/login/process-control/irreversible effects;
- [x] researcher outputs remain Draft-only and coordinator-only promotion is preserved;
- [x] prompt eval includes positive, negative, boundary, stale-target, concurrency, injection, authorization and closeout cases;
- [x] full diff is documentation-only and does not touch #528/#539/#475/#302/#536 owned paths;
- [x] complete prompt/eval content passed exact-head CI/governance before this checkpoint-only task update;
- [ ] final unchanged checkpoint head exact-head CI/governance green;
- [ ] fresh independent documentation/prompt audit with material findings `0`;
- [ ] mark Ready, squash merge, archive task and release ownership.

# Validation checkpoint

First complete prompt/eval head:

```text
62b65f9b975f0282ee0acf386210b218bb814e94
CI 32192910735 = SUCCESS
Track A agent runtime governance 32192910601 = FAILURE
```

That governance failure was metadata-only: this task record lacked universal Track A admission fields. No prompt/eval content failure was reported.

After adding the required `none/NOT_APPLICABLE` admission values, exact head:

```text
c50d8984ce6b1a75b2b7b6dd35219c8c5d95b15b
CI 32193038317 = SUCCESS
Track A agent runtime governance 32193038190 = SUCCESS
```

Full changed-file inventory is exactly three declared documentation/task paths. All three complete patches were self-reviewed. Manual eval contains 25 representative positive/negative/boundary cases. Material prompt findings from self-review: `0`.

This checkpoint-only task update changes the head, so final exact-head checks must be observed once more before any Ready transition.

# Independent-audit blocker

`PROMPT_EVAL_STANDARD.md` and task closeout require a fresh independent prompt/documentation validator for this material prompting change. The authoring worker's self-review cannot be represented as independent validation.

```yaml
status: blocked
blocker: REQUIRED_FRESH_INDEPENDENT_PROMPT_DOCUMENTATION_AUDIT
material_findings_open_from_self_review: 0
last_completed_step: full 12-alias prompt package, shared KasmVNC/anti-idle contract, 25-case manual eval, exact three-path self-review, green pre-checkpoint CI/governance
next_action: fresh validator audits exact final diff against PROMPTING_STANDARD, PROMPT_EVAL_STANDARD, parallel coordination and KasmVNC runtime contract; if material findings are 0 and final exact-head checks remain green, mark Ready and squash-merge/archive
```
