# Oteryn Client Agent Instructions — moved/non-canonical

These instructions apply to every path under `oteryn-client/**` and override historical instructions retained in this repository.

## Mandatory cutover rule

The Rust Oteryn client has moved to the canonical repository `blakinio/Oteryn-v2`.

Canonical cutover evidence:

- destination repository: `blakinio/Oteryn-v2`;
- destination client path: `apps/client`;
- destination PR: `blakinio/Oteryn-v2#50`;
- destination merge: `78988f72a80cc904aa9176ae850c50d4efa0b0f0`;
- frozen source snapshot: `blakinio/otclient@c923ad8a1dff17b4933a6110931b0823cec2c590`.

## Required behavior for every agent

1. Do not implement, continue, fix, refactor, extend or otherwise develop Oteryn v2 Rust-client product work under `blakinio/otclient/oteryn-client/**`.
2. Route all new Oteryn v2 Rust-client, protocol, shared-domain, runtime, content and tooling work to `blakinio/Oteryn-v2` and read that repository's current `AGENTS.md`, ADRs, contracts, active tasks and live PR state before acting.
3. Treat this subtree as read-only historical source, migration/provenance evidence and bounded behavioral reference unless an explicitly authorized source-history or cutover-correction task requires a documentation-only change here.
4. Do not revive historical Canary compatibility, dual-protocol selection, old workspace plans or pre-cutover architecture as a second canonical Oteryn product line. Current architecture in `blakinio/Oteryn-v2` supersedes those historical directions.
5. Do not backport new Oteryn-v2 implementation into this subtree, create new Rust-client feature branches here, or open new implementation PRs targeting this path.
6. Preserve Git history and provenance. Do not delete or rewrite historical source merely to make the old subtree resemble the destination.
7. Legacy OTClient work outside `oteryn-client/**` remains governed by the repository-root `AGENTS.md` and its own active tasks; this marker does not freeze unrelated legacy maintenance.

## Historical inspection

When historical evidence from the pre-cutover Rust client is required, inspect the pinned source snapshot `c923ad8a1dff17b4933a6110931b0823cec2c590` and repository history. Historical documents may be useful as evidence, but they are not authoritative for current Oteryn v2 architecture.

If a request says to "continue Oteryn v2", "continue the Rust client", implement `protocol-oteryn`, or otherwise advance the migrated product, stop work in this repository and continue from `blakinio/Oteryn-v2` instead.
