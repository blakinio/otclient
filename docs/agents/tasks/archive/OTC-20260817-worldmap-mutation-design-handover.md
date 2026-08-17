---
task_id: OTC-20260817-worldmap-mutation-design-handover
status: validating_merge
agent: ChatGPT
project_lane: otclient
lane: DOCUMENTATION-PROMPTING
task_kind: documentation_and_prompt_handover
phase: close
branch: docs/OTC-20260817-worldmap-mutation-design-handover
base_branch: main
base_main: f8e628a255a18ec92839bbb45ef0e3b40bef8605
live_main_observed: ec75e2606f7f4ad834e4b6be968fb03bdbff55df
pr: 468
risk: low
owned_paths_released_after_merge: true
modules_touched: []
reuses:
  - merged PR #367 worldmap extent static dependency graph
  - merged producer PR #437 exact static evidence
  - merged producer PR #446 downstream exact static evidence
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
policy_version: 2
prompting_standard_version: 2.1
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
client_byte_mutation_authorized: false
owner_funded_ai_api_authorized: false
prompt_eval:
  path: docs/agents/evidence/OTC-20260817-worldmap-mutation-design-handover/PROMPT_EVAL.md
  mode: documented_manual_scenario_matrix
  result: PASS_CONTRACT_INSPECTION
  automated_trials: NOT_AVAILABLE_NOT_CLAIMED
e2e: NOT_APPLICABLE_WITH_REASON_DOCUMENTATION_ONLY
next_action: require exact-final-head CI/governance success and merge PR #468; if a check fails, restore active ownership only if material remediation is needed
---

# Worldmap mutation-design handover closeout

## Delivered

- repository-owned worker prompt: `docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN.md`;
- owner alias: `OTCLIENT-TIBIA-RE-WORLDMAP-MUTATION-DESIGN`;
- alias contract: `docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN_ALIAS.md`;
- durable research-to-design handover: `docs/agents/evidence/OTC-20260817-worldmap-mutation-design-handover/20260817-handover.md`;
- prompt-as-code manual evaluation: `docs/agents/evidence/OTC-20260817-worldmap-mutation-design-handover/PROMPT_EVAL.md`.

## Acceptance state before final merge gate

- full prompt carries accepted #367 facts and explicit UNKNOWNs: PASS;
- alias resolves live state and reuses an existing correct task instead of duplicating: PASS;
- actual client-byte mutation remains separately authorized: PASS;
- no owner-funded AI/API authority added: PASS;
- prompt evaluation record exists and does not mislabel manual scenarios as automated trials: PASS;
- changed paths are task-owned documentation/prompting surfaces only: PASS;
- review submissions/threads at pre-close audit: 0/0;
- runtime E2E: NOT_APPLICABLE_WITH_REASON — this task changes no executable client/runtime behavior;
- exact-final-head required CI/governance: PENDING at archive creation;
- PR merge: PENDING at archive creation.

The task is archived before merge to avoid a stale active-task record. `status: validating_merge` is intentionally not a completion claim. GitHub exact-head CI and PR terminal state remain authoritative for final completion.
