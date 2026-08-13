---
task_id: OTC-20260813-tibia-re-canonical-runtime
status: validating
agent: ChatGPT
project_lane: otclient
lane: otclient
track: official-client-analysis
task_kind: documentation_infrastructure
phase: consolidation
branch: docs/OTC-20260813-tibia-re-canonical-runtime
base_branch: main
created: 2026-08-13T09:41:00+02:00
updated: 2026-08-13T09:56:00+02:00
risk: medium
related_pr: "#285"
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-tibia-re-canonical-runtime.md
  - docs/agents/SHORT_COMMANDS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-prompt-eval.md
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

# Owner persistence directive

All new material work for this programme must be persisted or indexed in `blakinio/otclient` before return/rotation. Nothing required for continuation may live only in chat, local scratch space, transient runner state, an external repository or an unreferenced workflow artifact/log. Large artifacts may remain outside Git when required, but their exact provenance and semantic result must be indexed from this repository.

# Acceptance inventory

- [x] A repository-owned short-command registry resolves `OTCLIENT-TIBIA-RE` without relying on chat memory.
- [x] The canonical wrapper prompt loads the original programme prompt but overrides runtime ownership to `blakinio/otclient` and the dedicated OTClient runner.
- [x] The wrapper explicitly forbids treating `oteryn-staging`, `oteryn-synology-staging`, or `oteryn-tibia-client-analysis` as active execution targets for new programme work.
- [x] The wrapper explicitly requires every material finding/result/checkpoint/next action to be persisted or indexed in `blakinio/otclient` before return/rotation.
- [x] A consolidated report records material external Oteryn evidence required for continuation, including exact run/job/commit identifiers and claim boundaries.
- [x] Current OTClient work inventory is recorded: PR #48 runtime, #279 OTBM pipeline, #280 runner infrastructure, #283 stable bridge.
- [x] Current unknowns and canonical continuation order are recorded.
- [x] Prompt routing was evaluated against positive, negative, boundary, stale-state, persistence and injection-style cases: 13/13 PASS.
- [x] No external repository is mutated.
- [x] No Codex, OpenAI API quota, user token or owner-funded AI service is used.
- [ ] Exact-head repository CI and PR diff/review hygiene are terminal before merge.

# Coordination

This task does not edit PR #48 workflow/task paths, PR #280 `infra/ot-runners/**`, PR #279 tooling, or PR #283 bridge paths. Those owners continue their own implementation. This task only creates the canonical routing/coordination layer on top of current `main`.

Runtime migration itself is being executed in the owning lanes:

- PR #48: bootstrap workflow changed from `[self-hosted, oteryn-staging]` + Docker container recreation to `[self-hosted, otclient, synology]` + direct persistent runner state at `/home/runner/_work/_otclient_tibia_re_state`.
- PR #280: OTClient runner gets a separate `otclient-tibia-re` build target, the `tibia-re` label, and baked X11/Vulkan/GDB/Qt/proxychains/pyelftools dependencies without Docker socket or runtime privilege escalation.

# Evidence boundary

PROVEN:
- `blakinio/otclient` `main` at task creation is `05450748daca8344d9555638b638e98b6dc3abc7`.
- master programme prompt is already on `main` at `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md`.
- PR #48, #279, #280 and #283 are all in `blakinio/otclient` and contain the active implementation/runtime work.
- historical Oteryn worldmap/action evidence was read from `blakinio/Oteryn-Platform` and consolidated without mutating the external repository.
- canonical wrapper evaluation passed 13/13 documented cases.
- owner explicitly requires all future material programme work to be saved in `blakinio/otclient`; this requirement is now encoded in the canonical wrapper and task.

DERIVED:
- after #280 deployment and #48 runner acceptance proof, future workers no longer need to query Oteryn-Platform merely to recover normal programme state.

UNKNOWN:
- exact result of the current PR #280 Docker target validation until its workflow becomes terminal;
- whether the updated PR #280 runner image is deployed on Synology;
- whether the dedicated runner currently carries the new `tibia-re` label;
- whether the PR #48 canonical bootstrap job is accepted by `synology-otclient-01`;
- current upstream official-client SHA;
- current structural `IN_GAME` state.

# Prompt evaluation

`docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-prompt-eval.md` compares the canonical wrapper against the unchanged base programme prompt and records 13/13 passing routing/safety/persistence/continuation cases. The candidate removes active-runtime ambiguity and requires repository persistence without weakening structural evidence, SHA fencing, recovery, OTBM or owner-funded-AI constraints.

# Checkpoint

```yaml
checkpoint_version: 3
status: validating
branch: docs/OTC-20260813-tibia-re-canonical-runtime
pr: 285
head_before_checkpoint: 9fe7ad92a769ea6cbf033b603678fc7e461c622a
base_head: 05450748daca8344d9555638b638e98b6dc3abc7
related_prs:
  runtime: 48
  otbm: 279
  runner: 280
  bridge: 283
prompt_eval:
  cases: 13
  passed: 13
blockers: []
next_action: verify PR #285 full diff and exact-head CI; merge the documentation routing layer if clean, while runner deployment/runtime acceptance continues in #280/#48
```
