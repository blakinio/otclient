---
task_id: OTC-20260821-surveyor-next-gap-alias
status: implementing
phase: prompt_audit_remediation
agent: ChatGPT
project_lane: otclient
lane: P0-ACTION
track_id: official-client-re
task_kind: documentation
risk: low
policy_version: 2
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
gui_input_authorized: false
process_control_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
branch: docs/OTC-20260821-surveyor-next-gap-alias
base_main: e4ad8d915378826d6cdf77d0943e8adbfa4847a1
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_NEXT_NONOVERLAP_GAP_CONTINUE.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_SURVEYOR_V2_NEXT_NONOVERLAP_GAP_CONTINUE_ALIAS.md
  - docs/agents/evidence/OTC-20260821-surveyor-next-gap-alias/prompt-eval.md
  - docs/agents/tasks/active/OTC-20260821-surveyor-next-gap-alias.md
modules_touched: []
reuses:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
depends_on:
  - OTC-20260821-surveyor-action-protocol-reader
blocks: []
feature_scope:
  type: internal_only
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
prompt_contract:
  version: 1.1.0
  changed_surfaces:
    - worker continuation rule
    - Track A admission ordering
    - Surveyor gap-selection routing
    - alias resolution
  objective: continue Surveyor across safe non-overlapping reader slices while requiring admission before substantial or live work
  baseline_version: OTCLIENT-TIBIA-RE canonical wrapper 1.2.0 plus no dedicated next-gap alias on main@e4ad8d915378826d6cdf77d0943e8adbfa4847a1
  eval_suite: docs/agents/evidence/OTC-20260821-surveyor-next-gap-alias/prompt-eval.md
  rollback_version: remove the dedicated next-gap prompt and alias and fall back to OTCLIENT_TIBIA_RE_CANONICAL.md v1.2.0
invocation_started_at: 2026-08-21T18:55:00Z
last_progress_at: 2026-08-21T19:08:00Z
---

# Surveyor v2 next non-overlap gap alias publication

## Objective

Publish one canonical autonomous-program continuation prompt and one short alias for Surveyor v2 after terminal closeout of `OTC-20260821-surveyor-action-protocol-reader`.

The prompt must recompute live state, avoid overlapping work, establish Track A admission before substantial collection, and continue across safe READY slices until a real programme stop rather than stopping after one reader.

## Acceptance

- alias resolves to one canonical prompt;
- prompt begins with current `main`, governance, explicit Track A coordinator/task admission, active/open ownership state and a collection mode legal under the current admission class;
- historical reader counts are checkpoint evidence only and are recomputed before selection;
- selection uses P0/P1 impact, downstream rows, evidence strength, read-only E2E feasibility, implementation surface and overlap avoidance;
- world/minimap is excluded while live ownership/PR overlap persists;
- completion of one reader slice loops back to live-state recomputation and does not terminate `autonomous_program`;
- no runtime/login/gameplay/process-control/memory-write/credential authority is granted by this prompt publication;
- material prompt-as-code change has a durable baseline/candidate/rollback record and representative manual eval matrix;
- documentation-only outcome receives fresh independent audit, exact-head CI/governance and terminal lifecycle closeout.

## Current coordination facts

- `main` at task start: `e4ad8d915378826d6cdf77d0943e8adbfa4847a1`;
- archived action-protocol slice reports historical 8 remaining typed-reader gaps;
- Draft PR #475 and Draft PR #593 still represent overlapping world/minimap work at the last verified selection checkpoint.

## Validation and audit history

Initial Track A governance run `32516182956` failed because the new no-runtime task omitted mandatory admission metadata. The task was repaired; exact-head `922179cc870931a3c4334e093ee300ad2eaca439` then passed CI `32516307070` and Track A governance `32516306717`.

Fresh independent audit review `PRR_kwDOTVmdjs8AAAABKdDqYg` on that exact head returned three material findings:

- `AUD-656-001`: autonomous-program metadata contradicted a one-slice stop condition;
- `AUD-656-002`: material prompt change lacked the required prompt-as-code eval/baseline/rollback record;
- `AUD-656-003`: `--collect-all` was ordered before mandatory Track A admission.

Candidate v1.1.0 repairs all three findings. It requires a new exact-head validation and fresh independent re-audit before readiness.

## E2E classification

`NOT_APPLICABLE_WITH_REASON`: this task publishes documentation/prompt contracts only and does not execute or change an official-client runtime. Behavioural prompt regression is covered by the durable manual scenario matrix plus fresh independent audit; actual reader E2E remains mandatory for every future selected reader task.

## Next action

Complete the manual prompt eval record, validate the new exact head, obtain fresh independent audit with zero material findings, merge #656, then perform a separate lifecycle archive closeout.
