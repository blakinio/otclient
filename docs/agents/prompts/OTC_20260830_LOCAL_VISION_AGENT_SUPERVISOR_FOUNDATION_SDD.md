# OTC local vision-agent supervisor foundation — SDD coordinator

```yaml
prompt_contract_version: 1.0.0
alias: OTC-LOCAL-VISION-AGENT-SUPERVISOR-FOUNDATION-SDD
repository: blakinio/otclient
track_id: official-client-re
lane: RUNTIME_INFRA
task_kind: implementation
execution_mode: subagent_driven_development
direct_codex_spark_authorized: true
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
user_communication: low_noise
runtime_access: none
implementation_authorized: true
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

## Mission

Continue autonomously as the implementation coordinator for:

`OTC-20260830-local-vision-agent-supervisor-foundation`

Live Git/GitHub state is the source of truth. Do not trust cached SHAs, branch state, PR prose or this prompt without revalidation.

Expected durable entry points to revalidate:

- implementation branch: `feat/OTC-20260830-local-vision-agent-supervisor-foundation`;
- stacked Draft implementation PR: #810;
- parent Draft architecture/planning PR: #808;
- task: `docs/agents/tasks/active/OTC-20260830-local-vision-agent-supervisor-foundation.md`;
- report: `docs/agents/reports/OTC-20260830-local-vision-agent-supervisor-foundation.md`;
- approved design: `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`;
- approved implementation plan: `docs/superpowers/plans/2026-08-30-local-track-a-vision-agent-supervisor.md`.

The repository owner approved Approach C, approved the written design, and explicitly selected **Subagent-Driven Development** for repository-only implementation.

## Required workflow

Read the current `AGENTS.md` hierarchy and the approved design/plan before implementation. Use the installed Superpowers workflow:

1. `using-git-worktrees` — create or verify an isolated implementation worktree; do not implement on `main`;
2. `subagent-driven-development` — initialize the plan-scoped SDD workspace/ledger, run the required preflight task/interface conflict scan, then execute the plan task-by-task;
3. `test-driven-development` — every feature/refactor follows RED -> verified RED -> minimal GREEN -> verified GREEN -> refactor;
4. fresh implementer subagent per substantive plan task, never concurrent implementers against shared files;
5. independent task reviewer after every task, with spec-compliance and quality verdicts;
6. execute the documented fix/re-review loop for Critical/Important findings;
7. after all tasks, use the broad final code-review workflow and `verification-before-completion`;
8. use `finishing-a-development-branch` only after verified completion. Do not merge without the repository/owner closeout gate.

Do not reconstruct requirements from chat history. The written spec is authoritative; the implementation plan is its execution argument. If they conflict, rule in favor of the spec, record the ruling in the SDD ledger, and continue unless every safe path becomes a guess.

## Hard authority boundary

This implementation is repository-only. It must not:

- enable or invoke `mcp_servers.cua_repl`;
- access or control the Official Tibia/Kasm runtime;
- start autonomous Tibia input;
- access credentials or implement/activate a real credential broker;
- perform login, character selection, world entry/exit or gameplay;
- restart/modify Molehill supervisor, Ollama proxy, Docker or other local services merely to make tests pass;
- use process memory or unrestricted process control;
- change the stale `OfficialTibiaAdapter` client promotion fence merely to make effects actionable;
- bind a production physical executor.

The production executor remains Null/unbound. Fake/offline fixtures and deterministic repository tests are permitted by the approved plan.

Qwen3-VL/model output remains untrusted visual evidence. Visual/OCR evidence never independently promotes `IN_GAME`; stronger reviewed runtime corroboration is required in later separately-authorized phases.

## Durable execution

Keep PR #810 Draft during active implementation. After each plan task/review, update the plan-scoped SDD ledger and the implementation report with verified commits/tests/findings. Maintain exactly one concrete `next_action` in the active task.

If an execution environment is unavailable, persist the exact blocker and the furthest verified checkpoint. Never fabricate subagent work, tests, CI, runtime observations, or completion.