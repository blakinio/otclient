---
task_id: OTC-20260822-control-center-parallel-prompts-postmerge-repair
status: validating
agent: ChatGPT
project_lane: otclient
lane: CONTROL-CENTER-PARALLEL-PROMPTS
track_id: official-client-re
task_kind: postmerge_remediation
phase: validation
risk: medium
branch: fix/control-center-parallel-prompts-postmerge-20260822
base_branch: main
created: 2026-08-22T16:20:00+02:00
updated: 2026-08-22T16:27:00+02:00
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
gameplay_allowed: false
transaction_authorized: false
network_listener_allowed: false
official_client_access: false
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: checkpoint_only
owned_paths:
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_B_ALIAS.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_B_PARALLEL_AGENT.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_C_ALIAS.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_C_PARALLEL_AGENT.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_D_PREP_ALIAS.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_D_PREP_PARALLEL_AGENT.md
  - docs/agents/tasks/active/OTC-20260821-control-center-parallel-agent-prompts.md
  - docs/agents/tasks/active/OTC-20260822-control-center-parallel-prompts-postmerge-repair.md
  - docs/agents/tasks/archive/OTC-20260822-control-center-parallel-prompts-postmerge-repair.md
depends_on:
  - PR #650 merged as 9c54c1a4e22db974109298a23be39d9b04305e76
blocks:
  - Package B/C/D-prep launch until this repair is merged
ownership_released: false
prompt_contract:
  version: 1.0.1
  changed_surfaces:
    - routing or continuation rule
    - canonical worker prompt headers
    - alias prompt headers
  objective: repair unsupported completion-policy enum while preserving single-task stop-at-boundary semantics
  baseline_version: control-center-parallel-prompts@1.0.0#9c54c1a4e22db974109298a23be39d9b04305e76
  eval_suite: docs/agents/evidence/OTC-20260821-control-center-parallel-agent-prompts/prompt-eval.md
  rollback_version: docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md@9dee1f97694a591b1f9a784556f1357f966c2e57
---

# Control Center parallel prompt post-merge repair

## Finding

The synchronized independent audit of PR #650 found P1 `PRRT_kwDOTVmdjs6bZQvw`: all six new worker/alias headers used undeclared Prompting Standard 2.1 value `finalize_archive_and_stop`.

PR #650 auto-merged before that audit result arrived. This task repairs trusted main immediately without expanding authority.

## Repair

Use supported `task_completion_policy: finalize_archive_and_continue` while retaining `run_scope: single_task` and `continuation_policy: stop_at_task_boundary`. The latter two fields prohibit follow-on task selection; the supported completion policy preserves archive semantics.

## Acceptance

- [x] six worker/alias headers use only declared Prompting Standard 2.1 values
- [x] `single_task` / `stop_at_task_boundary` remains intact
- [x] no runtime/credential/login/mutation authority changes
- [x] exact-head CI/governance PASS on pre-version-bump head `f0ceff3ff32273ae1d70e365e28e9bc4b86c7126`; rerun required on successor
- [ ] fresh independent exact-head audit has no P0/P1 (prior audit found versioning P1, now repaired)
- [ ] repair PR merged
- [ ] this task archived and ownership released

## Next action

Open the narrow repair PR, validate exact head, obtain fresh independent review, merge, then archive both the repair task and the original prompt-publication lifecycle before launching Package C.
