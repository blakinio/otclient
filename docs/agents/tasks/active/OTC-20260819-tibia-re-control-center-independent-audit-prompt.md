---
task_id: OTC-20260819-tibia-re-control-center-independent-audit-prompt
status: in_progress
agent: ChatGPT
project_lane: otclient
lane: P0-AUDIT-PROMPT
track_id: official-client-re
task_kind: research_infrastructure_audit_prompt
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
branch: docs/OTC-20260819-tibia-re-control-center-independent-audit-prompt
base_branch: main
base_sha: 5817f1ad699c2d68dfb1a03886dc8c20dace67e7
risk: low
owned_paths:
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT.md
  - docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-independent-audit-prompt.md
modules_touched: []
reuses:
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
depends_on:
  - merged design PR #600
  - merged lifecycle closeout PR #601
blocks: []
cross_repository_task_ids: []
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
owner_current_instruction: save the prepared independent audit prompt for the TIBIA RE Control Center project to blakinio/otclient and merge it under repository governance
invocation_started_at: 2026-08-19T15:34:00+02:00
last_progress_at: 2026-08-19T15:34:00+02:00
current_blocker: null
next_action: add the canonical read-only independent audit prompt, open a draft PR, validate exact head, self-review, and merge if all gates pass
---

# Control Center independent audit prompt publication

## Objective

Persist a canonical, standalone prompt for a fresh independent read-only audit of the merged `TIBIA RE Control Center / E2E Lab` architecture before Package A implementation begins.

The prompt must be executable from repository state alone, must require live verification of current repository facts rather than trust historical chat, and must deeply falsify authority, concurrency, STOP ALL, scenario, recorder, privacy, browser/CLI, official-adapter, Oteryn-v2 and differential-E2E boundaries.

## Scope

Documentation only. No runtime observation, no client execution, no GUI input, no login, no credential access, no gameplay, no Oteryn-v2 writes and no implementation change.

## Acceptance criteria

- canonical prompt added under `docs/agents/prompts/`;
- audit is explicitly independent and read-only;
- current repository state must be revalidated before conclusions;
- design #600/#601, Surveyor #592, Track A governance and current Oteryn-v2 architecture are included in scope;
- P0-P3 severity criteria and exact structured output are defined;
- at least 18 concrete falsification scenarios are required;
- Package A implementation-readiness is a mandatory verdict;
- exact-head CI/governance and full changed-file self-review pass before merge.
