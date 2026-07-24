---
task_id: OTC-20260724-shell-safe-open-url
coordination_id: OTS-20260721-oteryn-identity-auth
status: completed
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260724-shell-safe-open-url
base_branch: main
created: 2026-07-24T12:40:00+02:00
completed: 2026-07-24T17:08:34+02:00
related_pr: "20"
merge_commit: 4435a8fa67622d5770a9a7cc4c15af3480d8feb1
risk: medium
---

# OTC-20260724-shell-safe-open-url

## Outcome

Unix desktop browser URLs are launched as exact process arguments instead of shell commands. OAuth Authorization Code + PKCE query strings therefore reach the browser unchanged, and shell metacharacters are no longer interpreted.

## Delivered

- Linux uses `Platform::spawnProcess("/usr/bin/env", {"xdg-open", url})`.
- Apple uses `Platform::spawnProcess("/usr/bin/open", {url})`.
- Focused Linux regression coverage verifies a URL containing multiple `&` separators is received as exactly one unchanged argument.
- Module catalogue and changelog were updated.

## Validation

- Implementation source: `9189d1063e968a0c2ffab11c5069db192e753397`.
- Linux release workflow: `30087461815`.
- Linux artifact: `8595332324`.
- Artifact digest: `sha256:396e0e1fed38c14f43c88cba4e578997ecbd56c2f211ee8b398c712a10c44850`.
- Executable digest: `sha256:9c95ca6e3c26b387f61fcaeb99596d877c1db1bd85a8df1dac310f4a9af03c22`.
- Production-like rehearsal: `30095854266` — PASS.
- Retained evidence: `8597730728`, digest `sha256:e7e908e9129658654054a96adf641757edc2c904fc2b01a5b9fc97e393d18009`.
- Evidence classification: `PRODUCTION_LIKE_PROVEN`.
- Final OTClient CI: `30098690336` — PASS.

## Cross-repository gate

Platform rehearsal PR `blakinio/Oteryn-Platform#126` was merged as `b520cf78ac1b488a289b156b492539b2a047f299` after the physical OAuth PKCE, world entry, logout, replay rejection, credential rotation, rollback and final smoke scenarios passed.

## Completion

- Final status: completed
- PR: `blakinio/otclient#20`
- Merge commit: `4435a8fa67622d5770a9a7cc4c15af3480d8feb1`
- Catalogue updated: yes
- Changelog updated: yes
- Archived at: 2026-07-24T17:42:00+02:00
