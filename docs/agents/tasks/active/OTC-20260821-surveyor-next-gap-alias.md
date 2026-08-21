---
task_id: OTC-20260821-surveyor-next-gap-alias
status: implementing
phase: prompt_publication
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
  - docs/agents/tasks/active/OTC-20260821-surveyor-next-gap-alias.md
modules_touched: []
reuses:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
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
invocation_started_at: 2026-08-21T18:55:00Z
last_progress_at: 2026-08-21T19:01:00Z
---

# Surveyor v2 next non-overlap gap alias publication

## Objective

Publish one canonical continuation prompt and one short alias for the next Surveyor v2 typed-reader slice after terminal closeout of `OTC-20260821-surveyor-action-protocol-reader`.

The prompt must force live-state recomputation and must not hard-code a next reader. It must reject overlapping candidates, especially world/minimap work while active PR/task ownership still overlaps that area.

## Acceptance

- alias resolves to one canonical prompt;
- prompt starts from live `main`, active tasks, open PRs, current Surveyor `--collect-all`, and current runtime admission rather than historical counts;
- next gap is selected by P0/P1 blocker impact, downstream rows, evidence strength, read-only E2E feasibility, implementation surface and overlap avoidance;
- historical `8` remaining readers is treated as checkpoint evidence only and recomputed before selection;
- no runtime, login, gameplay, process-control, memory-write or credential authority is granted by the prompt publication itself;
- documentation-only outcome receives proportionate audit, exact-head CI/governance and terminal lifecycle closeout.

## Current live coordination facts

- `main` at task start: `e4ad8d915378826d6cdf77d0943e8adbfa4847a1`;
- action-protocol reader slice is archived and reports 8 remaining typed-reader gaps;
- active world/minimap work remains represented by Draft PR #475 and Draft PR #593, so a fresh worker must treat that family as overlapping until live state proves otherwise.

## Validation history

Initial governance run `32516182956` failed only because the new Track A task record omitted mandatory no-runtime admission metadata. The fresh admission behavior audit job passed; the deterministic policy audit correctly rejected the incomplete front matter. The prompt and alias content were not implicated.

## Next action

Revalidate the exact new head, run proportionate prompt/content audit, merge after required CI/governance pass, then archive this documentation task.
