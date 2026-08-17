---
task_id: OTC-20260817-worldmap-mutation-design-handover
status: implementing
agent: ChatGPT
project_lane: otclient
lane: DOCUMENTATION-PROMPTING
task_kind: documentation_and_prompt_handover
phase: implement
branch: docs/OTC-20260817-worldmap-mutation-design-handover
base_branch: main
base_main: f8e628a255a18ec92839bbb45ef0e3b40bef8605
pr: null
risk: low
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN_ALIAS.md
  - docs/agents/evidence/OTC-20260817-worldmap-mutation-design-handover/**
  - docs/agents/tasks/active/OTC-20260817-worldmap-mutation-design-handover.md
  - docs/agents/tasks/archive/OTC-20260817-worldmap-mutation-design-handover.md
modules_touched: []
reuses:
  - merged PR #367 worldmap extent static dependency graph
  - merged producer PR #437 exact static evidence
  - merged producer PR #446 downstream exact static evidence
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
depends_on: []
blocks: []
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
implementation_authorized: true
client_byte_mutation_authorized: false
owner_funded_ai_api_authorized: false
next_action: persist handover and prompt evaluation, open Draft PR, validate exact head, archive task, then merge if repository gates pass
---

# Worldmap mutation-design handover

## Objective

Persist the completed #367 research outcome and provide one repository-owned autonomous alias and worker prompt for the next mutation-design phase, without authorizing official-client byte mutation.

## Acceptance

- full worker prompt exists and carries every material accepted fact/UNKNOWN from #367;
- short alias resolves the worker prompt and requires live-state reuse rather than duplicate tasks;
- prompt-as-code evaluation record exists per `PROMPT_EVAL_STANDARD.md`;
- durable handover records what was proven, what it enables, what remains and the exact next phase;
- documentation-only validation and exact-head CI pass;
- final diff is scoped, review threads are clear, task is archived and PR is merged under normal repository policy.
