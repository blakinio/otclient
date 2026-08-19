---
task_id: OTC-20260819-tibia-re-surveyor-v2-prompt
status: completed
agent: ChatGPT
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: documentation
risk: low
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
implementation_pr: 612
implementation_merge_commit: 3cb5d52c06b03f5db496d71e9b6945dbf9d3b0bd
validated_head: e2c2d1a1373d92cf782293b360663b5c68db7b0a
ci_run: 32305421521
ci_result: SUCCESS
track_a_governance_run: 32305420138
track_a_governance_result: SUCCESS
independent_prompt_audit_review: 4977008266
independent_prompt_audit_result: PASS
final_delta_revalidation_review: 4977030622
final_delta_revalidation_result: PASS
material_findings_open: 0
runtime_e2e: NOT_APPLICABLE
runtime_e2e_reason: documentation-only prompt publication; no official-client behavior was implemented or executed
ownership_released: true
completed_at: 2026-08-19T23:48:00+02:00
next_action: invoke TIBIA-RE-SURVEYOR-V2-COLLECT-ALL from current main; follow its live-state preflight and do not manually log in until it emits COLLECTOR_READY=YES and OWNER_LOGIN_REQUIRED=YES unless it proves an existing valid in-game canonical session can be reused
---

# TIBIA-RE Surveyor v2 collect-all programme prompt — completed

## Delivered

PR #612 published the repository-owned programme prompt and short alias:

- `docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL.md`
- `docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_COLLECT_ALL_ALIAS.md`
- `docs/agents/evidence/OTC-20260819-tibia-re-surveyor-v2-prompt/prompt-eval.md`

The prompt coordinates the safe path from current live repository state through Surveyor v1 resolution, conditional existing-runtime reconciliation, Surveyor v2 collect-all implementation, pre-login readiness, manual owner login only when genuinely required, post-login runtime revalidation, one passive read-only live collection, `missing-readers.json`, gap-driven typed-reader work, independent audit/E2E/CI and terminal closeout.

## Validation and audit

Final exact source head:

```text
e2c2d1a1373d92cf782293b360663b5c68db7b0a
```

Terminal evidence:

```text
CI                         32305421521 = SUCCESS
Track A runtime governance 32305420138 = SUCCESS
changed files              exactly 4 declared documentation/prompt-as-code paths
review threads             0
independent prompt audit   review 4977008266 = PASS; material findings 0
final delta revalidation   review 4977030622 = PASS; material findings 0
runtime E2E                NOT_APPLICABLE: documentation-only publication
runtime/client access      NONE
credentials accessed       NO
```

Squash merge:

```text
3cb5d52c06b03f5db496d71e9b6945dbf9d3b0bd
```

## Boundaries preserved

This publication task did not execute or observe the official client and performed no credential access, login/relogin, GUI/gameplay input, process control, attach/injection, process-memory/client-byte mutation, network mutation, item/economic transaction or owner-funded OpenAI/Codex invocation.

The published future programme is itself live-state-resolved and fail-closed. It does not ask the owner to log in while safe repository-side prerequisites remain; it reuses an already valid exact in-game canonical session when available; and its passive collect-all path may not promote canonical semantic coverage merely from collected structural evidence.

Ownership for the prompt-publication task is released. Future Surveyor v2 implementation/runtime work must claim its own current task, paths and Track A admission from then-current `main`.
