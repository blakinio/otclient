---
task_id: OTC-20260807-oteryn-v2-source-marker
status: completed
branch: docs/OTC-20260807-oteryn-v2-source-marker
base_branch: main
created: 2026-08-07
updated: 2026-08-07
related_pr: "274"
merge_commit: 8c56c45c6c25147470ce3ca23e639a31d9085e47
owned_paths: []
required_reads:
  - AGENTS.md
  - docs/agents/README.md
  - oteryn-client/README.md
  - oteryn-client/AGENTS.md
search_first:
  - Oteryn-v2
  - source marker
  - historical marker
optional_reads: []
---

# Mark migrated Rust client source as historical/non-canonical

## Terminal result

The required source-only closeout for the Oteryn v2 Rust-client migration is complete.

Canonical migration evidence:

- frozen source repository: `blakinio/otclient`;
- frozen source snapshot: `c923ad8a1dff17b4933a6110931b0823cec2c590`;
- canonical destination repository: `blakinio/Oteryn-v2`;
- canonical destination client path: `apps/client`;
- atomic destination cutover PR: `blakinio/Oteryn-v2#50`;
- canonical destination cutover merge: `78988f72a80cc904aa9176ae850c50d4efa0b0f0`;
- source-marker PR: `blakinio/otclient#274`;
- source-marker final head: `0bb7f92ae420fc3e81a4ade62a9b9b994c894f0c`;
- source-marker squash merge: `8c56c45c6c25147470ce3ca23e639a31d9085e47`.

## Delivered scope

- `oteryn-client/README.md` now marks the old Rust-client subtree as `HISTORICAL / NON-CANONICAL` and points to the exact destination repository, path and cutover merge;
- `oteryn-client/AGENTS.md` now prevents future agents from restarting Oteryn v2 Rust-client development in this repository and redirects product work to `blakinio/Oteryn-v2`;
- historical source, Git history and provenance remain available in `blakinio/otclient`;
- unrelated legacy OTClient work remains governed by the repository root and is not frozen by this marker;
- no runtime, protocol, dependency, workflow, asset, production or external-repository mutation was part of the source-marker PR.

## Validation

```yaml
implementation_complete: true
outcome_verified: true
changed_paths:
  - docs/agents/tasks/active/OTC-20260807-oteryn-v2-source-marker.md
  - oteryn-client/AGENTS.md
  - oteryn-client/README.md
full_diff_review: PASS
runtime_component_e2e:
  result: NOT_APPLICABLE
  reason: source-marker documentation only
final_ci:
  head: 0bb7f92ae420fc3e81a4ade62a9b9b994c894f0c
  result: PASS
  workflows:
    - Rust Client run 31155904330: PASS
    - CI run 31155910869: PASS
review:
  unresolved_threads: 0
  requested_changes: 0
merge:
  pr: 274
  method: squash
  commit: 8c56c45c6c25147470ce3ca23e639a31d9085e47
external_repository_writes: none
production_operations: none
```

## Programme consequence

`blakinio/otclient/oteryn-client/**` is now formally historical/non-canonical. New Oteryn v2 Rust-client development belongs only in `blakinio/Oteryn-v2`.

The source-marker blocker recorded by the Oteryn-v2 foundation programme is satisfied by merge `8c56c45c6c25147470ce3ca23e639a31d9085e47`. The Oteryn-v2 architecture programme may now proceed to its next ordered gate, `FND-ID-01`, subject to verification against current `Oteryn-v2/main`.

## Closeout

```yaml
task_status: completed
ownership_released: true
archive_required: satisfied by this lifecycle PR
next_action: Continue Oteryn-v2 architecture work from the canonical repository; do not resume Rust-client implementation in blakinio/otclient.
```
