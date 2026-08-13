---
task_id: OTC-20260813-tibia-re-canonical-runtime
status: implementing
agent: ChatGPT
project_lane: otclient
lane: otclient
track: official-client-analysis
task_kind: documentation_infrastructure
phase: consolidation
branch: docs/OTC-20260813-tibia-re-canonical-runtime
base_branch: main
created: 2026-08-13T09:41:00+02:00
updated: 2026-08-13T09:41:00+02:00
risk: medium
related_pr: none
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-tibia-re-canonical-runtime.md
  - docs/agents/SHORT_COMMANDS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - PR #48 runtime evidence/task
  - PR #279 worldmap reconstruction tooling
  - PR #280 dedicated runner infrastructure
  - PR #283 runtime bridge
  - historical Oteryn-Platform reports as read-only evidence only
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
---

# Objective

Make `blakinio/otclient` the single canonical repository and coordination surface for `OTCLIENT-TIBIA-RE`, with the dedicated repository runner (`synology-otclient-01`, selector `[self-hosted, otclient, synology]`) as the only active live-experiment target after migration. Preserve Oteryn-Platform work only as imported read-only historical evidence.

# Acceptance inventory

- [ ] A repository-owned short-command registry resolves `OTCLIENT-TIBIA-RE` without relying on chat memory.
- [ ] The canonical wrapper prompt loads the original programme prompt but overrides runtime ownership to `blakinio/otclient` and the dedicated OTClient runner.
- [ ] The wrapper explicitly forbids treating `oteryn-staging`, `oteryn-synology-staging`, or `oteryn-tibia-client-analysis` as active execution targets for new programme work.
- [ ] A consolidated report records all material external Oteryn evidence required for continuation, including exact run/job/commit identifiers and claim boundaries.
- [ ] Current OTClient work inventory is recorded: PR #48 runtime, #279 OTBM pipeline, #280 runner infrastructure, #283 stable bridge.
- [ ] Current unknowns and one canonical next action are recorded.
- [ ] No external repository is mutated.
- [ ] No Codex, OpenAI API quota, user token or owner-funded AI service is used.

# Coordination

This task does not edit PR #48 workflow/task paths, PR #280 `infra/ot-runners/**`, PR #279 tooling, or PR #283 bridge paths. Those owners continue their own implementation. This task only creates the canonical routing/coordination layer on top of current `main`.

# Evidence boundary

PROVEN:
- `blakinio/otclient` `main` at task creation is `05450748daca8344d9555638b638e98b6dc3abc7`.
- master programme prompt is already on `main` at `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md`.
- PR #48, #279, #280 and #283 are all in `blakinio/otclient` and contain the active implementation/runtime work.
- historical Oteryn worldmap/action evidence is readable through `blakinio/Oteryn-Platform` and can be summarized without mutating it.

UNKNOWN:
- whether the updated PR #280 runner image is already deployed on Synology;
- whether the dedicated runner currently carries the new `tibia-re` label;
- current upstream official-client SHA;
- current structural `IN_GAME` state.

# Checkpoint

```yaml
checkpoint_version: 1
status: implementing
branch: docs/OTC-20260813-tibia-re-canonical-runtime
base_head: 05450748daca8344d9555638b638e98b6dc3abc7
related_prs:
  runtime: 48
  otbm: 279
  runner: 280
  bridge: 283
blockers: []
next_action: create the short-command registry, canonical wrapper prompt and consolidated state report, then open a draft PR and validate exact references
```
