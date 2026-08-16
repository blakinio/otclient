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
closeout_pr: 341
reconciliation_pr: 344
updated: 2026-08-16T12:06:00+02:00
owned_paths: []
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
audit:
  result: PASS
  basis: fresh live GitHub repository/Actions reinspection independent of implementation narrative
  material_findings_open: 0
e2e:
  result: PASS
  journey: linux-client-startup-smoke
  physical_synology_gameplay: NOT_APPLICABLE_WITH_REASON
  reason: physical login/input/gameplay belongs to the separate Synology runtime lane
final_heavy_ci:
  head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
  run: 31935503532
  result: PASS
  merge_tree_equivalent: true
  merge_tree: 6a51b91962c61b72a97a308d07292779ac7c3407
closeout_main_ci:
  head: 6c06d4daf83c03f2f9d22b4e2631caef0bb489c2
  run: 31940357773
  result: PASS
  scope: docs_only
ownership_released: true
next_action: none
---

# Final result

The OTClient CI hybrid is complete.

- Ordinary deterministic validation is Linux-only on GitHub-hosted runners.
- Windows general-CI workflow support is removed.
- Compile-relevant CI runs Linux test/release builds and a required real-client startup smoke under `Xvfb`.
- Synology/self-hosted remains reserved for persistent physical runtime evidence: real display/input ownership, login, walking/clicking, LAN integration and long-lived game sessions.
- A hosted headless startup smoke must not be cited as physical gameplay E2E.

## Verified implementation outcome

PR #331 was merged from exact head `4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe` as `c4b1919e16fb2931c74f32cb310229703dbf893c`.

Both commits resolve to the same repository tree:

```text
6a51b91962c61b72a97a308d07292779ac7c3407
```

Therefore exact-head CI run `31935503532` (`CI #3409`) validated the same content that was merged. It passed:

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
  Download real linux-release artifact                  PASS
  Verify dependencies with ldd                          PASS
  Launch real otclient under Xvfb                       PASS
  Upload startup evidence                               PASS
CI / Required                                           PASS
```

Startup evidence artifact:

```text
id: 9260979303
name: linux-client-startup-smoke
digest: sha256:cd13a4851684cd9e3a8ce71f1d1fb3e543160edb92586dddd048255dc32d5c4d
head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
```

## Post-merge 504 classification

The first heavy push attempt on merge SHA `c4b1919e...` failed while vcpkg fetched `freetype 2.14.3` from `gitlab.freedesktop.org`. The direct job log records repeated HTTP `504` responses through all built-in download attempts; no OTClient compile diagnostic preceded the failure.

This is classified as external dependency infrastructure rather than a code regression because the exact implementation tree completed all Linux builds/tests/smoke successfully and is tree-identical to the squash merge.

A later same-SHA retry was superseded/cancelled by newer `main` activity under the intended concurrency policy.

## Current workflow outcome

Fresh live reinspection at closeout confirms:

- `.github/workflows/ci.yml` routes compile scope to `reusable-build-linux.yml`;
- `Client Startup Smoke - Linux` uses GitHub-hosted `ubuntu-24.04` and the real release artifact;
- `.github/workflows/reusable-build-windows.yml` is absent;
- repository search finds no `reusable-build-windows.yml` or `windows-2025` general-CI reference;
- `.github/workflows/infrastructure-retry.yml` does not retry intentional `cancelled` runs;
- closeout merge SHA `6c06d4daf83c03f2f9d22b4e2631caef0bb489c2` passed docs-scoped push CI `31940357773` with `Detect Build Scope = PASS` and `CI / Required = PASS`, while Fast/Lua/Linux-build/smoke jobs were correctly skipped;
- later `main` also contains the separate Track A hybrid execution-routing contract from PR #343 and its archived closeout #345, reinforcing the same hosted-versus-Synology boundary without changing this task's implementation evidence.

## Follow-up PR #339 disposition

PR #339 (`ci: harden Linux dependency fetch resilience`) was created after the transient freetype 504. It proposed a vcpkg source-download cache, one bounded CMake retry, reopening this task record, and simultaneously archiving the unrelated historical `OTC-20260712-client-test-foundation` record.

Fresh closeout review found no evidence that those additions were required to deliver or validate the requested runner hybrid. Adding retry behavior and unrelated historical-task cleanup would broaden the completed task. PR #339 was therefore closed unmerged as `closed_obsolete`; its cache/retry idea may be evaluated later as a separate CI-resilience task.

No owner decision or review thread required #339 to remain open. Its Codex review bot only reported exhausted Codex review quota; no owner-funded quota was used to complete this task.

## Audit findings

### AUDIT-INFRA-001

```yaml
severity: informational
confidence: high
evidence: CI #3415 direct vcpkg job log
impact: external freetype source returned HTTP 504
disposition: false_positive_for_code_regression
verification: exact implementation/merge tree identity plus heavy exact-head CI PASS
```

### AUDIT-PR-001

```yaml
severity: material_during_closeout
confidence: high
evidence: open PR #339 explicitly referenced this task_id
impact: terminal archive initially omitted an open related follow-up PR
disposition: fixed
verification: PR #339 closed unmerged as obsolete; final reconciliation records it explicitly
```

### AUDIT-HYGIENE-001

```yaml
severity: informational
confidence: high
evidence:
  - ci/OTC-20260816-linux-ci-hybrid-check
  - ci/OTC-20260816-linux-ci-hybrid-task
  - ci/OTC-20260816-linux-ci-hybrid-temp
impact: three stale helper refs remain without live ownership or required PRs
disposition: accepted_tooling_limitation
verification: implementation branch is gone; helper refs are inventoried and unowned; exposed connector has no delete-ref action
```

No critical, high or material medium finding remains open.

## Applicable E2E

```text
real linux-release artifact
→ fresh GitHub-hosted Ubuntu runtime
→ ldd dependency check
→ virtual X display
→ real otclient process startup
→ bounded 20-second liveness
→ persisted startup/dependency evidence
```

Result: `PASS` in run `31935503532`.

Physical gameplay/runtime validation remains explicitly outside this infrastructure task and belongs to the separate Synology/Track A lane.

## Related PR terminal inventory

```yaml
related_prs:
  - repository: blakinio/otclient
    number: 328
    purpose: superseded_attempt
    terminal_state: closed_superseded
  - repository: blakinio/otclient
    number: 331
    purpose: implementation
    final_head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
    terminal_state: merged
    merge_commit: c4b1919e16fb2931c74f32cb310229703dbf893c
    unresolved_threads: 0
  - repository: blakinio/otclient
    number: 339
    purpose: obsolete_resilience_followup
    final_head: ffe103ec61772e73e978f11a83f4f4a0dc5d83b1
    terminal_state: closed_obsolete
    unresolved_threads: 0
  - repository: blakinio/otclient
    number: 341
    purpose: archive
    final_head: dd2de1a8a99995ed023f33a388c1689430286aa6
    terminal_state: merged
    merge_commit: 6c06d4daf83c03f2f9d22b4e2631caef0bb489c2
    unresolved_threads: 0
  - repository: blakinio/otclient
    number: 344
    purpose: terminal_reconciliation
    terminal_state: merged
    unresolved_threads: 0
```

PR #280 is a separate specialized Synology/runtime lane and is intentionally not classified as a related implementation/closeout PR for this task.

The historical `OTC-20260712-client-test-foundation` active record remains a separate stale-governance cleanup item; it is not silently modified as part of this task.

## Closeout

```yaml
implementation_complete: true
outcome_verified: true
audit:
  result: PASS
  findings_open_material: 0
e2e:
  result: PASS
  journey: linux-client-startup-smoke
final_heavy_ci:
  head: 4c50f1d5843bfe067cca19519e25e4fa9dc7ccfe
  run: 31935503532
  result: PASS
  merge_tree_equivalent: true
closeout_main_ci:
  head: 6c06d4daf83c03f2f9d22b4e2631caef0bb489c2
  run: 31940357773
  result: PASS
pull_requests:
  open_related_prs: 0
  unresolved_review_threads: 0
  terminal_prs:
    - blakinio/otclient#328 closed_superseded
    - blakinio/otclient#331 merged
    - blakinio/otclient#339 closed_obsolete
    - blakinio/otclient#341 merged
    - blakinio/otclient#344 merged
task_archived_or_terminal: true
ownership_released: true
stale_branches_reconciled: true
stale_branch_note: helper refs inventoried/unowned; deletion unavailable through exposed connector
```
