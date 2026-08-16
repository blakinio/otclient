---
task_id: OTC-20260816-linux-ci-hybrid
status: completed
owner: current-agent
session_role: closeout
feature_scope: infrastructure
completion_claim: internal_only
base_branch: main
implementation_pr: 331
implementation_head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
implementation_merge_commit: c4b1919e16fb2931c74f32cb310229703dbf893c
implementation_tree: 6a51b91962c61b72a97a308d07292779ac7c3407
closeout_branch: docs/OTC-20260816-linux-ci-hybrid-closeout
closeout_pr: pending
updated: 2026-08-16T11:48:00+02:00
owned_paths: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
audit:
  result: PASS
  basis: fresh live repository reinspection plus exact-head GitHub Actions evidence, without trusting implementation narrative
  material_findings_open: 0
e2e:
  result: PASS
  journey: linux-client-startup-smoke
  physical_synology_gameplay: NOT_APPLICABLE_WITH_REASON
  reason: this infrastructure task owns disposable hosted build/test/startup validation; physical login/input/gameplay evidence belongs to the separate Synology runtime lane
final_ci:
  head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
  run: 31935503532
  result: PASS
  merge_tree_equivalent: true
  merge_tree: 6a51b91962c61b72a97a308d07292779ac7c3407
current_main_observation:
  head: 9008bb7933db9e96119a61280941e695744e8408
  ci_run: 31939801096
  ci_result: PASS
  note: docs-scoped push; heavy build jobs correctly skipped by path scope
ownership_released: true
next_action: none
---

# Final result

Ordinary OTClient CI is Linux-only and uses disposable GitHub-hosted runners. Synology/self-hosted capacity remains reserved for work that genuinely requires the controlled physical runtime environment.

## Delivered runner boundary

### GitHub-hosted

- workflow/static validation;
- Lua syntax validation;
- Linux test and release builds;
- C++ unit, Lua and bounded integration tests;
- release-artifact dependency validation with `ldd`;
- bounded real-client startup under `Xvfb` with isolated persisted state;
- startup evidence artifact collection.

### Synology/self-hosted

- persistent OTClient/game sessions;
- canonical physical display/input ownership;
- real login, walking, clicking and gameplay control;
- LAN/runtime integration tied to the Synology environment;
- long-lived observations and direct physical runtime evidence.

A GitHub-hosted headless startup smoke is explicitly not physical gameplay E2E and must never be cited as such.

## Implementation evidence

PR #331 was merged from exact head `4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe` as squash commit `c4b1919e16fb2931c74f32cb310229703dbf893c`.

The exact PR head and the squash merge commit both resolve to tree:

```text
6a51b91962c61b72a97a308d07292779ac7c3407
```

Therefore the full successful exact-head validation exercised the same repository content that was merged.

Exact-head CI `31935503532` (`CI #3409`) passed all required compile-scope gates:

```text
Detect Build Scope                                      PASS
Fast Checks / Informational static analysis             PASS
Fast Checks / Syntax and workflow validation            PASS
Lua Syntax / Check Lua Syntax                           PASS
Build - Linux / Compile (linux-tests)                   PASS
  Run CMake                                             PASS
  Run C++ unit tests                                    PASS
  Run Lua tests                                         PASS
  Run integration tests                                 PASS
Build - Linux / Compile (linux-release)                 PASS
  Run CMake                                             PASS
  Upload artifacts                                      PASS
Client Startup Smoke - Linux                            PASS
  Download Linux release artifact                       PASS
  Verify client artifact dependencies                   PASS
  Launch client under virtual display                   PASS
  Upload startup smoke evidence                         PASS
CI / Required                                           PASS
```

Startup evidence artifact:

```text
id: 9260979303
name: linux-client-startup-smoke
digest: sha256:cd13a4851684cd9e3a8ce71f1d1fb3e543160edb92586dddd048255dc32d5c4d
head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
expired: false
```

## Post-merge infrastructure event

The first heavy push CI for merge SHA `c4b1919e16fb2931c74f32cb310229703dbf893c` did not expose a code regression. Its vcpkg source fetch for `freetype 2.14.3` received repeated HTTP `504` responses from `gitlab.freedesktop.org`; GitHub Packages did not yet contain that binary-cache entry, so source installation halted on the external download.

The later retry attempt was superseded/cancelled by newer `main` activity through the repository concurrency policy. This event is classified as external dependency infrastructure, not a material implementation finding, because:

1. the exact implementation tree had already completed both Linux builds and all required tests successfully;
2. the exact implementation tree equals the squash-merge tree;
3. later current-main CI is green and continues to reference the Linux reusable build, not a Windows build.

## Current repository outcome

Fresh live inspection at closeout confirms:

- `.github/workflows/ci.yml` routes compile scope to `Build - Linux` through `reusable-build-linux.yml`;
- `Client Startup Smoke - Linux` runs on GitHub-hosted `ubuntu-24.04` and consumes the real release artifact;
- `.github/workflows/reusable-build-windows.yml` is absent from `main`;
- repository search finds no `reusable-build-windows.yml` or `windows-2025` references;
- `.github/workflows/infrastructure-retry.yml` does not retry intentionally cancelled/superseded runs;
- current `main` head observed during closeout is `9008bb7933db9e96119a61280941e695744e8408` and its scoped CI run `31939801096` is `PASS`;
- documentation-only changes correctly avoid allocating Linux build/startup jobs when compile scope is false.

## Audit

### AUDIT-INFRA-001

```yaml
severity: informational
confidence: high
evidence: post-merge vcpkg log for CI #3415
impact: external freetype source download returned HTTP 504; no code defect identified
disposition: false_positive_for_code_regression
verification: exact implementation/merge tree identity plus exact-head heavy CI PASS
```

### AUDIT-HYGIENE-001

```yaml
severity: informational
confidence: high
evidence:
  - ci/OTC-20260816-linux-ci-hybrid-check
  - ci/OTC-20260816-linux-ci-hybrid-task
  - ci/OTC-20260816-linux-ci-hybrid-temp
impact: three stale helper refs remain; none is the merged implementation branch, owns no live task path and has no required PR
disposition: accepted_tooling_limitation
verification: implementation branch is gone; helper refs inventoried and ownership released; the exposed GitHub connector has no delete-ref action
```

No critical, high or material medium findings remain.

## E2E classification

The applicable end-to-end journey for this infrastructure task is:

```text
real linux-release artifact
→ fresh GitHub-hosted Ubuntu runtime
→ dynamic dependency resolution
→ virtual X display
→ real otclient process startup
→ bounded 20-second liveness
→ persisted startup/dependency evidence artifact
```

Result: `PASS` in `31935503532`.

Physical login/input/walking/clicking is intentionally outside this task and remains owned by the separate Synology/Track A runtime lane. No claim about physical gameplay runtime state is made here.

## Related PR terminal inventory

```yaml
related_prs:
  - repository: blakinio/otclient
    number: 331
    purpose: implementation
    final_head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
    terminal_state: merged
    merge_commit: c4b1919e16fb2931c74f32cb310229703dbf893c
    unresolved_threads: 0
  - repository: blakinio/otclient
    number: 328
    purpose: superseded_attempt
    final_head: b082c62fdd13896e27321a86e2bccf2d46c41abc
    terminal_state: closed_superseded
```

PR #280 is not a related implementation/closeout PR for this task. It remains the separate specialized Synology/runtime lane and is intentionally untouched.

## Closeout

```yaml
implementation_complete: true
complete_feature_or_declared_partial: true
outcome_verified: true
audit:
  result: PASS
  findings_open_material: 0
e2e:
  result: PASS
  journey: linux-client-startup-smoke
final_ci:
  head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
  run: 31935503532
  result: PASS
  merge_tree_equivalent: true
pull_requests:
  open_related_prs: 0
  unresolved_review_threads: 0
  terminal_prs:
    - blakinio/otclient#331 merged
    - blakinio/otclient#328 closed_superseded
task_archived_or_terminal: true
ownership_released: true
stale_branches_reconciled: true
stale_branch_note: helper refs inventoried and unowned; deletion unavailable through the exposed connector
```
