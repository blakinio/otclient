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
archived: 2026-08-13T10:36:00+02:00
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

The canonical wrapper requires every material programme finding, experiment result, failure, artifact reference, runtime identity, checkpoint and `next_action` to be persisted or indexed in `blakinio/otclient` before return/rotation. Large external artifacts may remain outside Git only when exact provenance and semantic consequences are indexed in this repository.

## Canonical runtime contract

```yaml
repository: blakinio/otclient
runner_name: synology-otclient-01
migration_selector: [self-hosted, otclient, synology]
post_deploy_selector: [self-hosted, Linux, X64, otclient, tibia-re, synology]
persistent_state: /home/runner/_work/_otclient_tibia_re_state
```

New programme work must not use the historical Oteryn runner/container/state paths as active execution dependencies.

## Independent post-implementation audit

A fresh-context validator role was executed after implementation PR #285 merged. The validator intentionally ignored the implementer summary and read only:

```text
trusted-base governance:
  docs/agents/AGENTS.md
  docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
acceptance/task contract from merged main
exact PR #285 changed-file set and final diff
merged main files at 89f62b00859f614a9adc1f2fbaf418f61f6950c2
final exact-head CI evidence
live related PR inventory
```

Validator identity:

```yaml
role: ChatGPT fresh-context closeout validator
invocation: same owner invocation, separate validator role with isolated evidence set
implementer_summary_used_as_evidence: false
```

Audit result:

```yaml
result: PASS
material_findings_open: 0
findings:
  - id: OTC-CANON-AUD-001
    severity: P1
    finding: prompt evaluation originally overstated a 14/14 behavioral pass
    disposition: fixed before implementation merge; report now says manual scenario matrix and behavioral trials NOT_RUN
    verification: merged prompt-eval report on main
  - id: OTC-CANON-AUD-002
    severity: P1
    finding: mandatory task coordination fields were missing
    disposition: fixed before implementation merge
    verification: merged active task contains modules_touched/depends_on/blocks/cross_repository_tasks
  - id: OTC-CANON-AUD-003
    severity: P1
    finding: first archive attempt lacked explicit independent-audit PASS and E2E result/reason
    disposition: fixed in archive PR #286 by this audit/E2E closeout block
    verification: this terminal archive record plus exact archive diff
```

The validator also confirmed:

- the alias resolves to a repository-owned canonical wrapper;
- the wrapper retains the unchanged base programme prompt rather than silently replacing its acceptance criteria;
- the merged wrapper routes new active execution to `blakinio/otclient`/dedicated OTClient runner and treats historical Oteryn runtime as evidence only;
- owner-funded Codex/API use is not authorized by the merged contract;
- imported evidence preserves claim boundaries and does not copy proprietary client binaries/assets;
- the implementation PR contains only the seven intended documentation/routing/evidence paths;
- related implementation lanes #48/#279/#280/#283 remain intentionally separate and are not falsely claimed completed by this task.

## E2E result

```yaml
result: NOT_APPLICABLE
reason: this task is documentation/routing/evidence consolidation only; it introduces no executable product/runtime behavior. The observable system outcome is repository resolution/persistence state on main, which was verified directly after merge. Live Tibia runner/session E2E belongs to independently owned runtime tasks #280/#48 and is explicitly not a completion criterion for this documentation task.
```

Deterministic outcome verification on merged `main` confirmed:

- `docs/agents/SHORT_COMMANDS.md` exists and maps `OTCLIENT-TIBIA-RE` to the canonical wrapper;
- the canonical wrapper and all imported evidence reports exist in `blakinio/otclient`;
- the persistence directive is encoded in the wrapper;
- external Oteryn runtime paths are explicitly non-canonical for new active work;
- implementation merge `89f62b00859f614a9adc1f2fbaf418f61f6950c2` is the current canonical source for this routing package.

## Implementation validation and review

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

All PR #285 review threads were resolved before its merge.

## Archive-PR validation

Archive PR #286 exact pre-remediation head `8514efe359ae743bb661008b46b9ec2ecc8c8e51` passed CI run `31682022891`, including `CI / Required` job `94389645880`. That run is supporting evidence only because this audit/E2E remediation changes the archive head; final required CI must pass again on the exact final archive head before merge.

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
closeout:
  implementation_complete: true
  vertical_slice_complete: true
  audit:
    result: PASS
    independent_validator: ChatGPT fresh-context closeout validator role
    material_findings_open: 0
  e2e:
    result: NOT_APPLICABLE
    reason: documentation/routing/evidence consolidation only; no executable product/runtime behavior introduced
    journeys: []
  implementation_ci:
    head: b2089d6f1fb9dcdd78acd67f2c9cb132fa42738f
    run: 31681473851
    result: PASS
  archive_ci:
    final_head: PENDING_THIS_REMEDIATION
    result: PENDING
  pull_requests:
    implementation_pr: blakinio/otclient#285 merged
    archive_pr: blakinio/otclient#286 pending exact-head CI and final review-thread cleanup
    intentionally_open_programme_prs:
      - blakinio/otclient#48
      - blakinio/otclient#279
      - blakinio/otclient#280
      - blakinio/otclient#283
  external_repository_writes: none
  owner_funded_ai_usage_by_task_implementation: none
  behavioral_prompt_trials: NOT_RUN
  manual_prompt_scenario_matrix: 14_cases_reviewed
  repository_outcome_verification: PASS
  task_status_after_archive_merge: completed
  task_archived_after_archive_merge: true
  ownership_released_after_archive_merge: true
```

## Next archive action

Wait only for final exact-head archive CI after this audit/E2E remediation, resolve the existing archive review thread if the final diff satisfies it, and merge PR #286. After that this archive has no remaining action; programme continuation stays with #48/#279/#280/#283.
