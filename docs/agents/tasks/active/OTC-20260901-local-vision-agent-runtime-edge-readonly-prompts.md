---
task_id: OTC-20260901-local-vision-agent-runtime-edge-readonly-prompts
status: validating
agent: ChatGPT prompting coordinator
session_role: prompt_architect
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: documentation
phase: prompt_package_validation
branch: docs/OTC-20260901-local-vision-agent-runtime-edge-readonly-prompts
base_branch: main
trusted_main: 565bce8d70311048380556014978666771da598c
parent_task: OTC-20260830-local-vision-agent-supervisor-foundation
parent_pr: 820
created: 2026-09-01T00:00:00+02:00
updated_at: 2026-09-01T13:17:34Z
risk: high
execution_class: repository_github_only
execution_mode: chat
implementation_authorized: true
prompting_standard_version: 2.1
policy_version: 2
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
user_communication: low_noise
context_pressure: medium
decomposition_decision: single
decomposition_reason: one cohesive prompt-as-code package with one common contract, one coordinator model, eight alias missions, one eval matrix and one owner registry
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
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
programme_id: OTC-VISION-P2-READONLY
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-local-vision-agent-runtime-edge-readonly-prompts.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
reuses:
  - docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1.md structural pattern only
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
depends_on:
  - merged local vision-agent supervisor foundation PR #820
blocks: []
---

# Phase 2 read-only multi-agent prompt package

## Objective

Create a durable repository-owned prompt family for the next local vision-agent phase so the owner can run one coordinator plus bounded parallel workers from short aliases, and can restart any worker in a new agent window after context/effort/session exhaustion without replaying chat history.

The package must preserve the approved Phase 2 read-only boundary. It must not authorize official-client input, anti-idle, login, credentials, gameplay, process control, process memory, network payload capture or physical effects.

## Approved design authority

- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- foundation is expected from merged PR #820, but live state is revalidated before use.

## Deliverables

1. Common Phase 2 coordination contract with one coordinator, up to five non-overlapping concurrent workers, one official-runtime observation owner at a time and one local model inference at a time.
2. Eight canonical alias missions:
   - `OTC-VISION-P2-COORDINATOR`
   - `OTC-VISION-P2-RUNTIME-ADMISSION`
   - `OTC-VISION-P2-CAPTURE-EDGE`
   - `OTC-VISION-P2-RUNTIME-SIGNALS`
   - `OTC-VISION-P2-EDGE-TRANSPORT`
   - `OTC-VISION-P2-CONTROL-BRIDGE`
   - `OTC-VISION-P2-VISION-RECONCILIATION`
   - `OTC-VISION-P2-E2E-AUDIT`
3. Owner alias registry with wave order, one-line start/resume commands and recommended agent/effort.
4. Prompt-as-code eval matrix covering continuation, ownership, safety, injection, runtime admission, model-slot, transport, audit and phase-boundary cases.
5. Mandatory durable checkpoint rule after every meaningful completed subtask and before long/failure-prone/context-heavy operations.

## Resume invariant

A worker session is disposable. After every meaningful subtask it must persist enough task/Git/PR evidence for a fresh agent to execute:

```text
Kontynuuj <ALIAS> autonomicznie.
```

without needing the previous chat.

The outgoing worker must not leave a stale `implementing` state on effort/context/tool exhaustion. It persists a coherent commit where applicable, checkpoint status `ready|waiting|blocked`, exact branch/head/PR, validation, blockers and one `next_action`, then returns `ROTATE|WAITING|BLOCKED` accurately.

## Acceptance inventory

- [x] Existing trusted-base prompting, handoff, execution-budget, runtime-admission and Phase 2 design contracts were inspected before writing.
- [x] Live `main` was verified at `565bce8d70311048380556014978666771da598c`, the merged #820 foundation commit at task start.
- [x] No overlapping open PR for `vision runtime edge read-only` was found at task start.
- [x] Coordination contract exists and preserves `physical_action_budget/count: 0/0`.
- [x] Prompt family contains exactly eight aliases with consistent names.
- [x] Old parallel-runtime anti-idle/input authority is explicitly excluded.
- [x] New-window continuation/resume is explicit and anti-duplicate.
- [x] Owner alias registry contains wave order and effort recommendation.
- [x] Manual prompt eval matrix covers positive, negative, boundary, injection, continuation and closeout cases.
- [ ] Fresh independent prompt audit/review is completed or exact blocker is recorded.
- [ ] Exact-head repository checks required for this documentation change are green before merge/readiness.
- [ ] PR/task lifecycle is truthful and terminal according to repository closeout rules.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T13:17:34Z
head: f41ef3b253d1b66c3a19638f5509102f9abbf583
branch: docs/OTC-20260901-local-vision-agent-runtime-edge-readonly-prompts
pr: 821
status: validating
context_routes:
  - prompting-standard
  - prompt-eval
  - phase-2-read-only-design
  - context-handoff
  - track-a-runtime-admission
owned_paths:
  - docs/agents/tasks/active/OTC-20260901-local-vision-agent-runtime-edge-readonly-prompts.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
proven:
  - main at task start is the verified merged foundation commit 565bce8d70311048380556014978666771da598c.
  - PR 821 is Draft from the dedicated docs branch to main; initial prompt package head is f41ef3b253d1b66c3a19638f5509102f9abbf583.
  - exact-head readback confirms eight canonical aliases with consistent names in the prompt family and owner registry.
  - coordination and common contracts preserve mutation_authorized false and physical action budget/count zero.
  - older parallel-runtime anti-idle/input permission is explicitly non-authoritative and Phase 2 anti-idle/GUI input is false/forbidden.
  - checkpoint after every meaningful subtask, pre-heavy checkpointing, ROTATE semantics and one-line new-window continuation are explicit.
  - manual prompt eval matrix defines 26 positive/negative/boundary/injection/continuation/closeout scenarios and zero allowed safety regression.
derived:
  - one common contract plus alias missions is safer than eight duplicated common contracts because safety/checkpoint changes remain single-source.
  - the old parallel-runtime prompt may be reused only structurally because its anti-idle/input authority is broader than Phase 2.
unknown:
  - exact independent validator outcome for the candidate prompt package.
  - exact required GitHub checks on the final documentation head after this checkpoint commit.
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - direct reuse of OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1 is safe: rejected because it contains anti-idle/input authority not allowed by Phase 2.
changed_paths:
  - docs/agents/tasks/active/OTC-20260901-local-vision-agent-runtime-edge-readonly-prompts.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/programs/OTC_VISION_P2_READONLY_PROMPT_EVAL_V1.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_ALIASES.md
validation:
  - command: exact-head GitHub readback of all prompt-package files
    result: PASS
    evidence: PR 821 initial head f41ef3b253d1b66c3a19638f5509102f9abbf583; file blobs read back from that ref
  - command: manual structural prompt review against OTC_VISION_P2_READONLY_PROMPT_EVAL_V1 static checks
    result: PASS
    evidence: 8 aliases; max workers 5; runtime observation 1; model inference 1; 0/0 physical budget/count; anti-idle/input false; Draft-only workers; Phase 3+ excluded
  - command: manual continuation contract review against CONTEXT_HANDOFF.md and ANTI_STALL_AND_EXECUTION_BUDGET.md
    result: PASS
    evidence: checkpoint per meaningful subtask/material event, pre-heavy checkpoint, ready/waiting/blocked plus one next_action, ROTATE/new-window resume without chat
blockers: []
next_action: inspect PR 821 exact-head workflow/check state and obtain or record the required fresh independent prompt review before readiness
```
