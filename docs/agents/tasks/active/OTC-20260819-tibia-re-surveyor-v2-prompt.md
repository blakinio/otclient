---
task_id: OTC-20260819-tibia-re-surveyor-v2-prompt
status: implementing
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: documentation_prompt_as_code
branch: docs/OTC-20260819-tibia-re-surveyor-v2-prompt
base_branch: main
base_sha: 97593631cfdaae8c38fcb497adf156760068f19a
created: 2026-08-19
updated: 2026-08-19
related_pr: ""
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL_ALIAS.md
  - docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/**
  - docs/agents/tasks/active/OTC-20260819-tibia-re-surveyor-v2-prompt.md
  - docs/agents/tasks/archive/OTC-20260819-tibia-re-surveyor-v2-prompt.md
  - docs/agents/CHANGELOG.md
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
---

# Publish the TIBIA-RE Surveyor v2 collect-all programme prompt

## Goal

Persist one canonical owner-facing alias and worker prompt that coordinates the safe path from current live repository state through Surveyor v1, canonical-runtime reconciliation, Surveyor v2 implementation, the exact owner-login handoff, one read-only live collect-all run and a ranked typed-reader backlog for all twelve TIBIA-RE subsystem aliases.

This task publishes prompt-as-code only. It does not itself finish PR #592 or #610, run the physical client, authorize credentials, perform login, or implement Surveyor v2.

## Prompt contract

```yaml
version: 1.0.0
changed_surfaces:
  - worker template
  - alias routing
objective: prevent premature owner login and duplicate per-agent runtime census by making one live-state-resolved collector programme the canonical next step
baseline_version: chat-only handoff with no repository-owned collect-all alias
eval_suite: docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/prompt-eval.md
rollback_version: no collect-all alias; use existing Track A prompts and live PR/task state directly
```

## Acceptance criteria

- A canonical prompt exists under `docs/agents/prompts/` and follows prompting standard v2.1.
- A short alias resolves to that prompt from live `blakinio/otclient` state.
- The prompt never treats stale chat facts, PR bodies, historical PID/display/socket values or an existing client window as authority.
- The prompt does not grant the agent credential access, login/relogin, GUI/gameplay input, process control, injection, memory writes, network mutation or economic actions.
- The prompt explicitly tells the agent not to ask the owner to log in until repository implementation/readiness gates are satisfied; an already valid in-game canonical session is reused instead of requesting another login.
- The prompt handles #610 conditionally from live state: finish it if its exact existing-runtime adoption preconditions are current, otherwise persist its exact waiting/obsolete state without blocking safe repository implementation of Surveyor v2.
- Surveyor v2 is specified as an extension of `tools/tibia_re_surveyor`, not a competing harness.
- Live collect-all output is specified for all twelve subsystem aliases plus a ranked `missing-readers.json` and secret/privacy guardrails.
- Prompt evaluation records positive, stale-state, owner-login, absent-runtime, already-in-game, authority-refusal, secret/privacy and closeout cases with no safety regression.
- Documentation-only runtime E2E is `NOT_APPLICABLE_WITH_REASON`; exact path/content/diff/PR outcome is verified before merge.

## Context checkpoint

```yaml
checkpoint_version: 1
policy_version: 2
updated_at: 2026-08-19T21:25:00Z
head: 97593631cfdaae8c38fcb497adf156760068f19a
branch: docs/OTC-20260819-tibia-re-surveyor-v2-prompt
pr: none
status: implementing
phase: implement
execution_mode: chat_github
context_pressure: medium
context_growth: stable
decomposition_decision: single
context_routes:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL_ALIAS.md
  - docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/**
  - docs/agents/CHANGELOG.md
proven:
  - main resolved to 97593631cfdaae8c38fcb497adf156760068f19a at task start
  - PR #592 is open, mergeable and Draft at head 90fb32f69173a6e621dfe6bd34c6f2e494076655
  - PR #610 is open, mergeable and Draft at head ea887207c581f9d0cf247e5d62a187afc1eb27ef
  - current Track A policy requires exact live-state admission and separates metadata adoption from later mutation authority
derived:
  - the safest owner-login handoff is after collector implementation/readiness, unless an already valid exact in-game canonical session exists
unknown:
  - whether PR #592/#610 will still have the same heads when the future alias is invoked
  - whether a valid exact in-game canonical runtime will already exist when live collection begins
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - merge active Draft PRs merely because the owner requested this prompt be merged
changed_paths:
  - docs/agents/tasks/active/OTC-20260819-tibia-re-surveyor-v2-prompt.md
validation:
  - command: prompt evaluation manual scenario matrix
    result: NOT_RUN
    evidence: prompt not yet written
  - command: documentation runtime E2E
    result: NOT_APPLICABLE
    evidence: this task only publishes prompt-as-code and performs no physical-runtime behavior
blockers: []
next_action: create the canonical collect-all prompt and alias, then evaluate the candidate against the documented scenario matrix
```
