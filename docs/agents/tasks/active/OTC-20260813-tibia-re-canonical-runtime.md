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
updated: 2026-08-13T10:20:00+02:00
risk: medium
related_pr: "#285"
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-tibia-re-canonical-runtime.md
  - docs/agents/SHORT_COMMANDS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-external-evidence-manifest.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-prompt-eval.md
modules_touched: []
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - PR #48 runtime evidence/task
  - PR #279 worldmap reconstruction tooling
  - PR #280 dedicated runner infrastructure
  - PR #283 runtime bridge
  - historical Oteryn-Platform reports/task as read-only evidence only
depends_on: []
blocks: []
cross_repository_tasks: []
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
- [x] A consolidated report records material external Oteryn worldmap/native-action evidence with exact run/job/commit identifiers and claim boundaries.
- [x] The proven historical non-OCR login/world-entry recovery recipe is imported with exact-version/layout gates, failed-hypothesis exclusions and semantic claim boundaries.
- [x] An external-evidence manifest maps the relevant Oteryn Tibia reports to imported/superseded/not-copied OTClient state and preserves missing worldmap runtime details without duplicating large evidence corpora.
- [x] Current OTClient work inventory is recorded: PR #48 runtime, #279 OTBM pipeline, #280 runner infrastructure, #283 stable bridge.
- [x] Current unknowns and canonical continuation order are recorded.
- [x] A 14-case **manual scenario matrix** was reviewed for static contract consistency; behavioral agent trials were explicitly not run and no behavioral 14/14 pass is claimed.
- [x] Deterministic repository outcome verification confirms the alias, wrapper, OTClient-only persistence/runtime routing and imported evidence exist in the resulting Git state.
- [x] Mandatory task coordination fields are explicitly declared, including empty lists where no dependency/block/cross-repo task applies.
- [x] No external repository is mutated.
- [x] No Codex, OpenAI API quota, user token or owner-funded AI service is used.
- [ ] Exact-head repository CI and final PR diff/review hygiene are terminal before merge.

# Coordination

This task does not edit PR #48 workflow/task paths, PR #280 `infra/ot-runners/**`, PR #279 tooling, or PR #283 bridge paths. Those owners continue their own implementation. This task creates the canonical routing/coordination layer on top of `main`.

Runtime migration itself is being executed in the owning lanes:

- PR #48: bootstrap workflow changed from `[self-hosted, oteryn-staging]` + Docker container recreation to `[self-hosted, otclient, synology]` + direct persistent runner state at `/home/runner/_work/_otclient_tibia_re_state`.
- PR #280: OTClient runner gets a separate `otclient-tibia-re` build target, the `tibia-re` label, and baked X11/Vulkan/GDB/Qt/proxychains/pyelftools dependencies without Docker socket or runtime privilege escalation.

# Evidence boundary

PROVEN:
- `blakinio/otclient` `main` at task creation was `05450748daca8344d9555638b638e98b6dc3abc7`.
- master programme prompt is already on `main` at `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md`.
- PR #48, #279, #280 and #283 are all in `blakinio/otclient` and contain the active implementation/runtime work.
- historical Oteryn worldmap/action/login evidence was read from `blakinio/Oteryn-Platform` and consolidated/indexed without mutating the external repository.
- the manual scenario matrix contains 14 representative static routing/safety/continuation cases; all 14 are represented consistently in candidate text, but behavioral pass rate is **NOT_MEASURED**.
- deterministic repository outcome verification passes for the actual routing/persistence files and related PR/runtime migration state.
- owner explicitly requires all future material programme work to be saved in `blakinio/otclient`; this requirement is encoded in the canonical wrapper/task/registry.
- PR #280 exact implementation Docker proof run `31679256871`, job `94380701487`, passed both image builds and dependency inspection; final workflow-free head `5f76d213d859c2a8838ac5b8740865ef6afaf1ab` passed repository CI run `31679760916`, including `CI / Required` job `94383401816`.

DERIVED:
- after #280 deployment and #48 runner acceptance proof, future workers no longer need to query Oteryn-Platform merely to recover normal programme state, the known historical login recipe or the important worldmap/action evidence.

UNKNOWN:
- measured future agent behavioral compatibility with the canonical wrapper, because no executable fresh-agent eval harness exists and no behavioral trials are claimed;
- whether the updated PR #280 runner image is deployed on Synology;
- whether the dedicated runner currently carries the new `tibia-re` label;
- whether the PR #48 canonical bootstrap job is accepted by `synology-otclient-01`;
- current upstream official-client SHA;
- current structural `IN_GAME` state.

# Review findings

Two P1 review findings were addressed:

1. Prompt eval overclaim: the former `14/14 PASS` wording was corrected to a manual scenario matrix with `behavioral_agent_trials: NOT_RUN`, while deterministic repository outcome evidence is reported separately.
2. Task coordination metadata: `modules_touched`, `depends_on`, `blocks` and `cross_repository_tasks` are now explicitly declared.

These fixes move the PR head; final exact-head CI and review-thread resolution are still required after the changes.

# Validation

- earlier exact-head canonical-routing CI run `31680504103` passed on head `289fa706b3edd5547ac9d561731cb9400776053d`, including `CI / Required` job `94385013470`;
- that run predates the review-finding repairs and is supporting evidence only;
- final exact-head CI must pass after the eval/task corrections;
- changed-file inventory remains confined to the seven canonical-routing/evidence documentation paths.

# Checkpoint

```yaml
checkpoint_version: 6
status: validating
branch: docs/OTC-20260813-tibia-re-canonical-runtime
pr: 285
head_before_checkpoint: 20d950cf7c6f2c924d90a96a129b8bc3459b2003
base_head_at_task_start: 05450748daca8344d9555638b638e98b6dc3abc7
related_prs:
  runtime: 48
  otbm: 279
  runner: 280
  bridge: 283
prompt_eval:
  mode: manual_scenario_matrix
  cases_reviewed: 14
  static_contract_consistency: 14_of_14
  behavioral_trials: NOT_RUN
  repository_outcome_verification: PASS
review_findings:
  prompt_eval_overclaim: fixed
  missing_coordination_fields: fixed
blockers: []
next_action: run final exact-head CI and recheck/resolve PR #285 review threads; merge only when all required checks pass on the exact final head
```
