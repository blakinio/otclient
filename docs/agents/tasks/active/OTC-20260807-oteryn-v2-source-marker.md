---
task_id: OTC-20260807-oteryn-v2-source-marker
status: active
branch: docs/OTC-20260807-oteryn-v2-source-marker
base_branch: main
created: 2026-08-07
updated: 2026-08-07
related_pr: null
merge_commit: null
owned_paths:
  - docs/agents/tasks/active/OTC-20260807-oteryn-v2-source-marker.md
  - oteryn-client/README.md
  - oteryn-client/AGENTS.md
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

## Purpose

Complete the source-only closeout required by the accepted Oteryn v2 client cutover. The canonical Rust client moved from `blakinio/otclient/oteryn-client` to `blakinio/Oteryn-v2/apps/client` in destination merge `78988f72a80cc904aa9176ae850c50d4efa0b0f0` (`feat(rust): perform atomic client cutover (#50)`).

## Scope

- mark `oteryn-client/**` in this repository as historical migration/reference evidence;
- direct all new Oteryn v2 Rust-client work to `blakinio/Oteryn-v2`;
- pin the exact destination merge `78988f72a80cc904aa9176ae850c50d4efa0b0f0`;
- preserve the source tree and Git history as migration/provenance evidence;
- prevent future agents from treating this path as a second canonical Oteryn v2 product line;
- change no Rust/C++/Lua runtime, protocol, assets, workflows, dependencies, production systems or external repositories.

## Dependencies and evidence

- source repository current main at task start: `c923ad8a1dff17b4933a6110931b0823cec2c590`;
- canonical destination repository: `blakinio/Oteryn-v2`;
- atomic destination cutover: PR #50;
- destination merge: `78988f72a80cc904aa9176ae850c50d4efa0b0f0`;
- destination path: `apps/client`;
- no open PR in `blakinio/otclient` changes `oteryn-client/**` at task start;
- open PRs #23, #48 and #97 have non-overlapping paths.

## Acceptance criteria

- [ ] `oteryn-client/README.md` clearly marks the subtree moved/non-canonical and points to the exact destination.
- [ ] `oteryn-client/AGENTS.md` blocks new Oteryn v2 implementation in this repository and redirects future agents to the canonical destination.
- [ ] Historical source and provenance remain available in this repository history.
- [ ] Full changed-file review contains only the declared documentation/task paths.
- [ ] Required exact-head GitHub checks pass.
- [ ] No unresolved review threads or requested changes remain.
- [ ] PR is squash-merged through normal branch protection.
- [ ] Task is archived in the required post-merge lifecycle change.

## Claim boundary

This task is source-only cutover closeout. It does not change the canonical Oteryn-v2 architecture, implement `protocol-oteryn`, modify the migrated destination client, alter legacy OTClient runtime behavior or authorize production deployment.

## Next action

Open the draft PR, replace the old Rust-client README/AGENTS entry points with explicit historical/non-canonical markers, then validate the exact PR head.
