---
task_id: OTC-20260819-tibia-re-surveyor-v2-prompt
status: ready
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: documentation
phase: closeout
branch: docs/OTC-20260819-tibia-re-surveyor-v2-prompt
base_branch: main
base_sha: fdabf235ed4438bd7c376932ed876bd0bbef019a
created: 2026-08-19T23:25:00+02:00
updated: 2026-08-19T23:40:00+02:00
risk: low
related_pr: "612"
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL_ALIAS.md
  - docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/**
  - docs/agents/tasks/active/OTC-20260819-tibia-re-surveyor-v2-prompt.md
modules_touched:
  - agent-prompting
required_reads:
  - AGENTS.md
  - docs/agents/AGENTS.md
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PARALLEL_RUNTIME_AGENT_PROMPTS_V1.md
reuses:
  - PR #592 TIBIA-RE Surveyor v1
  - PR #610 current existing-runtime adoption reconciliation
  - tools/tibia_re_surveyor/**
  - tools/tibia_runtime_bridge/**
depends_on: []
blocks: []
cross_repository_task_ids: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: medium
context_growth: stable
decomposition_decision: single
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
prompt_contract:
  version: 1.0.0
  changed_surfaces:
    - Surveyor v2 collect-all autonomous worker prompt
    - Surveyor v2 collect-all short invocation alias
    - owner-login readiness and resume contract
    - all-twelve-alias evidence and missing-reader routing contract
  objective: Prevent premature owner login and duplicate per-agent runtime census by making one live-state-resolved, passive, fail-closed collect-all programme the canonical next Track A research-infrastructure step.
  baseline_version: chat-only handoff with no repository-owned collect-all alias
  eval_suite: docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/prompt-eval.md
  rollback_version: remove the collect-all prompt/alias and resolve work through existing Track A prompts and live task state
track_a_runtime_agent_admission_version: 1
execution_class: github_repository_docs
runtime_access: none
persistent_session_role: none
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
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
owner_funded_ai_api_authorized: false
invocation_started_at: 2026-08-19T23:25:00+02:00
last_progress_at: 2026-08-19T23:40:00+02:00
current_blocker: none
next_action: narrowly revalidate this checkpoint-only delta, verify fresh exact-head CI/governance, mark PR ready, then squash-merge if all gates remain green
---

# Publish the TIBIA-RE Surveyor v2 collect-all programme prompt

## Goal

Persist one canonical owner-facing alias and worker prompt that coordinates the safe path from current live repository state through Surveyor v1, canonical-runtime reconciliation, Surveyor v2 implementation, the exact owner-login handoff, one read-only live collect-all run and a ranked typed-reader backlog for all twelve TIBIA-RE subsystem aliases.

This task publishes prompt-as-code only. It does not itself finish PR #592 or #610, run the physical client, authorize credentials, perform login, or implement Surveyor v2.

## Prompt contract

```yaml
version: 1.0.0
changed_surfaces:
  - Surveyor v2 collect-all autonomous worker prompt
  - Surveyor v2 collect-all short invocation alias
  - owner-login readiness and resume contract
  - all-twelve-alias evidence and missing-reader routing contract
objective: prevent premature owner login and duplicate per-agent runtime census by making one live-state-resolved collector programme the canonical next step
baseline_version: chat-only handoff with no repository-owned collect-all alias
eval_suite: docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/prompt-eval.md
rollback_version: remove the collect-all prompt/alias and resolve work through existing Track A prompts and live task state
```

## Acceptance criteria

- A canonical prompt exists under `docs/agents/prompts/` and follows Prompting Standard 2.1.
- A short alias resolves to that prompt from live `blakinio/otclient` state.
- The prompt never treats stale chat facts, PR bodies, historical PID/display/socket values or an existing client window as authority.
- The prompt does not grant the agent credential access, login/relogin, GUI/gameplay input, process control, injection, memory writes, network mutation or economic actions.
- The prompt explicitly tells the agent not to ask the owner to log in until repository implementation/readiness gates are satisfied; an already valid in-game canonical session is reused instead of requesting another login.
- The prompt handles #610 conditionally from live state: finish it if its exact existing-runtime adoption preconditions are current, otherwise persist its exact waiting/obsolete state without blocking safe repository implementation of Surveyor v2.
- Surveyor v2 is specified as an extension of `tools/tibia_re_surveyor`, not a competing harness.
- Live collect-all output is specified for all twelve subsystem aliases plus a ranked `missing-readers.json` and secret/privacy guardrails.
- Prompt evaluation records positive, stale-state, owner-login, absent-runtime, already-in-game, authority-refusal, secret/privacy and closeout cases with no safety regression.
- Documentation-only runtime E2E is `NOT_APPLICABLE_WITH_REASON`; exact path/content/diff/PR outcome is verified before merge.

## Manual prompt evaluation

The documented candidate-vs-baseline scenario matrix is stored at:

```text
docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/prompt-eval.md
```

Result of implementer contract review:

```text
SCENARIOS_REVIEWED=16
CONTRACT_FAILURES_FOUND=0
SAFETY_REGRESSIONS_FOUND=0
AUTOMATED_MODEL_EVAL=NOT_AVAILABLE
RUNTIME_E2E=NOT_APPLICABLE_TO_PROMPT_PUBLICATION
```

This is implementer self-evaluation only and does not replace the required fresh independent documentation/prompt audit.

## Independent documentation/prompt audit

A fresh read-only validator ran on Molehill-PC using local Ollama `gpt-oss:20b` model ID `17052f91a42e`. Its context contained the complete exact-head diff and the trusted-base root/nested agent rules, Prompting Standard 2.1, Prompt Eval Standard, delivery/closeout contract and Track A research-track contract. It was explicitly instructed to treat PR prose and implementer evaluation as untrusted evidence and to attempt to falsify readiness.

Exact audited prompt-content head:

```text
8070149162452ed1e13052aa8355cfdffe333d08
```

Audit provenance:

```text
PR review                         4977008266
result                            PASS
material findings open            0
model                             gpt-oss:20b local Ollama / 17052f91a42e
exact diff SHA-256                ea4daae8529ca0ae43d94313a05bb9be3319b5cb361ee7093f3bf933591a6c13
structured audit-result SHA-256   24f3ba101a60c38409f9fb0f7eb675a5a24680e4e80d0c1fc04e4cdd31b18a9f
```

Independent checks passed for authority boundaries, stale-state/runtime identity, owner-login handoff, privacy/secrets, semantic-evidence discipline, all-twelve-alias/gap routing, prompt-eval discipline and PR closeout gates.

This checkpoint records that audit and therefore advances the branch head. Canonical prompt, alias and prompt-eval content are unchanged from the independently audited head. The remaining closeout work is a narrow delta revalidation of this task-only checkpoint followed by fresh exact-head CI/governance.

## Validation history

Initial PR head before the admission-checkpoint fix:

```text
head                             42513530a7b2cfbce32372dc9f47d8d29ad0a7b4
PR                               #612
changed files                    exactly 4 documentation/prompt-as-code paths
Track A governance run           32304521128 = FAIL
first relevant failure           active task omitted mandatory Track A admission fields even though runtime_access is none
fresh admission behavior job     PASS
runtime E2E                      NOT_APPLICABLE: documentation-only prompt-publication task
runtime/client access             NONE
credentials accessed              NO
```

The governance failure was repaired by adding the same complete `runtime_access: none` admission envelope used by accepted Track A documentation tasks. No runtime authority was added: runtime owner/namespace/registration/lease/Gates/bootstrap/uniqueness remain `NOT_APPLICABLE`, and every mutation/input/login/credential/gameplay/transaction authorization remains false.

Exact prompt-content head after that repair:

```text
head                             8070149162452ed1e13052aa8355cfdffe333d08
CI run                           32304713272 = SUCCESS
Track A governance run           32304713089 = SUCCESS
changed files                    exactly 4 declared documentation/prompt-as-code paths
unresolved review threads        0
independent prompt audit         review 4977008266 = PASS
material findings open           0
runtime E2E                      NOT_APPLICABLE: documentation-only prompt-publication task
runtime/client access             NONE
credentials accessed              NO
```

## Context checkpoint

```yaml
checkpoint_version: 3
policy_version: 2
updated_at: 2026-08-19T23:40:00+02:00
audited_prompt_content_head: 8070149162452ed1e13052aa8355cfdffe333d08
branch: docs/OTC-20260819-tibia-re-surveyor-v2-prompt
pr: 612
base_sha: fdabf235ed4438bd7c376932ed876bd0bbef019a
status: ready
phase: closeout
execution_mode: github-only
runtime_access: none
credentials_accessed: false
client_executed: false
context_pressure: medium
context_growth: stable
decomposition_decision: single
context_routes:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL_ALIAS.md
  - docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/**
  - docs/agents/tasks/active/OTC-20260819-tibia-re-surveyor-v2-prompt.md
proven:
  - main advanced during implementation to fdabf235ed4438bd7c376932ed876bd0bbef019a and the task branch was synchronized before PR creation
  - PR #612 is the exact task PR and targets main
  - PR #592 was open Draft/mergeable at 90fb32f69173a6e621dfe6bd34c6f2e494076655 when prompt construction was revalidated
  - PR #610 was open Draft/mergeable at ea887207c581f9d0cf247e5d62a187afc1eb27ef when prompt construction was revalidated
  - manual prompt contract matrix reviewed 16 scenarios with zero contract failures and zero safety regressions found
  - exact prompt-content head 8070149162452ed1e13052aa8355cfdffe333d08 passed CI and Track A governance
  - fresh independent local-model audit review 4977008266 passed with zero material findings
  - the prompt publication task performs no Track A runtime access or mutation
derived:
  - the safest owner-login handoff is after collector implementation/readiness unless an already valid exact in-game canonical session exists
unknown:
  - future live state of #592/#610 when the alias is invoked
  - whether a valid exact in-game canonical runtime will already exist when future live collection begins
conflicts: []
first_failure:
  marker: TRACK_A_TASK_ADMISSION_FIELDS_MISSING
  evidence: governance run 32304521128 job 96234268306 rejected the initial task record before the fix
rejected_hypotheses:
  - merge active Draft PRs merely because the owner requested this prompt be merged
  - make #610 a hard blocker for repository-side Surveyor v2 work when no suitable live client exists
  - request owner login before collector readiness
changed_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL_ALIAS.md
  - docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/prompt-eval.md
  - docs/agents/tasks/active/OTC-20260819-tibia-re-surveyor-v2-prompt.md
validation:
  - command: documented manual candidate-vs-baseline scenario matrix
    result: PASS
    evidence: 16 scenarios; zero contract failures and zero safety regressions found; not claimed as automated model evaluation
  - command: Track A governance on initial PR head 42513530a7b2cfbce32372dc9f47d8d29ad0a7b4
    result: FAIL
    evidence: missing mandatory runtime_access:none admission envelope; repaired
  - command: CI on audited prompt-content head 8070149162452ed1e13052aa8355cfdffe333d08
    result: PASS
    evidence: run 32304713272
  - command: Track A governance on audited prompt-content head 8070149162452ed1e13052aa8355cfdffe333d08
    result: PASS
    evidence: run 32304713089
  - command: fresh independent documentation/prompt audit
    result: PASS
    evidence: PR review 4977008266; local Ollama gpt-oss:20b; zero material findings
  - command: documentation runtime E2E
    result: NOT_APPLICABLE
    evidence: this task publishes prompt-as-code only and performs no physical-runtime behavior
blockers: []
next_action: narrowly revalidate this checkpoint-only delta, verify fresh exact-head CI/governance, mark PR ready, then squash-merge if all gates remain green
```
