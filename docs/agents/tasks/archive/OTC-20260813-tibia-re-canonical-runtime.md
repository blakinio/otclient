---
task_id: OTC-20260813-tibia-re-canonical-runtime
status: completed
agent: ChatGPT
project_lane: otclient
lane: otclient
track: official-client-analysis
task_kind: documentation_infrastructure
phase: closeout
branch: docs/OTC-20260813-tibia-re-canonical-runtime-archive
base_branch: main
created: 2026-08-13T09:41:00+02:00
completed: 2026-08-13T10:20:12+02:00
archived: 2026-08-13T10:28:00+02:00
risk: medium
implementation_pr: "#285"
implementation_merge: 89f62b00859f614a9adc1f2fbaf418f61f6950c2
owned_paths_released:
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
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
---

# OTC-20260813 — OTCLIENT-TIBIA-RE canonical runtime consolidation archive

## Completed objective

`blakinio/otclient` is now the canonical repository and coordination surface for `OTCLIENT-TIBIA-RE`. New live programme work is routed toward the dedicated OTClient runner model, and historical Oteryn Platform runtime/reports are retained only as read-only provenance/evidence.

## Delivered on main

Merged PR #285, commit `89f62b00859f614a9adc1f2fbaf418f61f6950c2`, added:

- `docs/agents/SHORT_COMMANDS.md` — repository-owned alias resolution for `OTCLIENT-TIBIA-RE`;
- `docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md` — additive canonical wrapper over the unchanged base programme prompt;
- `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md` — consolidated current state and imported worldmap/action evidence;
- `docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md` — proven historical non-OCR login/world-entry recipe plus failed-hypothesis exclusions;
- `docs/agents/reports/OTCLIENT-20260813-tibia-re-external-evidence-manifest.md` — explicit migration/disposition manifest for external Oteryn evidence;
- `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-prompt-eval.md` — manual scenario-matrix evaluation with deterministic repository-outcome verification and explicit `behavioral_agent_trials: NOT_RUN` boundary.

## Owner persistence directive

The canonical wrapper now requires every material programme finding, experiment result, failure, artifact reference, runtime identity, checkpoint and `next_action` to be persisted or indexed in `blakinio/otclient` before return/rotation. Large external artifacts may remain outside Git only when exact provenance and semantic consequences are indexed in this repository.

## Canonical runtime contract

```yaml
repository: blakinio/otclient
runner_name: synology-otclient-01
migration_selector: [self-hosted, otclient, synology]
post_deploy_selector: [self-hosted, Linux, X64, otclient, tibia-re, synology]
persistent_state: /home/runner/_work/_otclient_tibia_re_state
```

New programme work must not use the historical Oteryn runner/container/state paths as active execution dependencies.

## Validation and review

PR #285 final implementation head:

```text
b2089d6f1fb9dcdd78acd67f2c9cb132fa42738f
```

Exact-head CI:

```yaml
run: 31681473851
conclusion: success
```

Review findings addressed before merge:

1. Prompt-eval overclaim was corrected from an apparent behavioral `14/14 PASS` to a 14-case manual scenario matrix with `behavioral_agent_trials: NOT_RUN` and separate deterministic repository-outcome verification.
2. Mandatory task coordination metadata (`modules_touched`, `depends_on`, `blocks`, `cross_repository_tasks`) was added explicitly.

All review threads were resolved before the final merge gate.

## Related programme lanes after closeout

This consolidation task is complete, but the durable programme continues through independently owned work:

- PR #48 — runtime/login/live structural session recovery on the dedicated OTClient runner;
- PR #279 — fail-closed worldmap/OTBM reconstruction pipeline;
- PR #280 — dedicated Synology runner infrastructure and deployment gate;
- PR #283 — stable read-only non-GDB runtime bridge awaiting live structural correlation.

These are not blockers for this documentation/routing task and retain their own lifecycle/status.

## Remaining programme unknowns

- current upstream official-client SHA/version;
- whether the updated PR #280 image is deployed on Synology and the `tibia-re` label is live;
- whether the canonical PR #48 bootstrap is accepted by `synology-otclient-01`;
- current OTClient-owned structural `IN_GAME` state;
- bridge live session-marker correlation and authoritative player position;
- subsequent action/OTBM evidence required by the base programme.

## Completion evidence

```yaml
status: completed
implementation_pr: 285
implementation_merge: 89f62b00859f614a9adc1f2fbaf418f61f6950c2
final_ci_run: 31681473851
final_ci: success
changed_files: 7
external_repository_writes: none
owner_funded_ai_usage: none
behavioral_prompt_trials: NOT_RUN
manual_prompt_scenario_matrix: 14_cases_reviewed
repository_outcome_verification: PASS
ownership_released: true
```

## Next programme action

Continue `OTCLIENT-TIBIA-RE` from the live durable tasks on `main`: finish/deploy the dedicated runner path (#280/#48), reverify the current official-client identity, then recover structural `IN_GAME` and resume live bridge/state/action evidence. This archive itself has no remaining action.
