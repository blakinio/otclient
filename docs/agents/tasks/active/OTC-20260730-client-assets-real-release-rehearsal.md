---
task_id: OTC-20260730-client-assets-real-release-rehearsal
status: in_progress
agent: "GPT-5.6 Thinking"
track: legacy-client
branch: ci/OTC-20260730-client-assets-real-release-rehearsal
base_branch: main
created: 2026-07-30T11:05:00+02:00
updated: 2026-08-01T10:16:00+02:00
last_verified_commit: "73ddebdec4a1873373e6f05451454f9b233db2d8"
required_base_commit: "43ed867910907cd4ebcf9f14e64977105d08ab7e"
risk: high
related_pr: "#97"
depends_on:
  - merged PR #37 and archive PR #83
blocks:
  - production runtime archive compatibility claim until exact rehearsal evidence is complete
owned_paths:
  - .github/workflows/client-assets-real-release-rehearsal.yml
  - docs/agents/tasks/active/OTC-20260730-client-assets-real-release-rehearsal.md
  - modules/client_assets/client_assets_release_selector.lua
  - modules/client_assets/client_assets_release_adapter.lua
  - tests/lua/fixtures/client_assets_releases.lua
  - tests/lua/unit/client_assets_release_selector_test.lua
  - docs/client-assets-auto-install.md
modules_touched:
  - client_assets
reuses:
  - existing GitHub release selector and conditional adapter
  - existing HTTP download cache path
  - existing g_crypt SHA-256 implementation
  - existing Lua unit runner and release fixtures
  - existing strict manifest SHA-256 checks
public_interfaces:
  - configured GitHub release-asset SHA-256 verification before installer extraction
cross_repo_tasks: []
---

# Goal

Complete the mandatory networked real-release rehearsal left by PR #37 and fix the exact integrity gap exposed by the first run, without weakening hashes, changing final runtime paths or committing downloaded game bytes.

# Scope

- resolve the release and archive exactly as the shipped selector does for client version `1525`;
- preserve the selected GitHub release asset `digest` and bind it to the exact selected download URL;
- verify downloaded selected-release archive bytes before the installer callback can begin extraction;
- leave unrelated downloads and codeload fallback behavior unchanged;
- build the current Linux client on a clean hosted runner and launch it under Xvfb without account or world login;
- install into `data/things/1525`, `data/sounds/1525` and configured extras paths;
- prove appearances and static data load for exact client version `1525`;
- remove the operational workflow before final merge and retain text-only evidence in this task.

# Safety boundaries

- no proprietary asset, archive, binary, log or runtime directory is committed or uploaded as a workflow artifact;
- downloaded bytes exist only on the ephemeral GitHub-hosted runner;
- no credentials, account login, character login, server connection or production deployment;
- `strictManifestSha256 = true` and `allowRawFallbackHashMismatch = false` remain unchanged;
- final runtime paths remain `data/things/<version>/`, `data/sounds/<version>/` and expected extras;
- a runtime pass without independent archive/content SHA-256 verification remains a blocker.

# First rehearsal evidence and failure

Run `30530600485`, job `90831765205`, head `73ddebdec4a1873373e6f05451454f9b233db2d8`:

- configured real release endpoint resolution passed;
- upstream `assets.json` and `assets.json.sha256` verification passed;
- Linux build, clean runtime preparation, installer flow and fresh runtime load passed;
- final runtime/path checks reached the last gate;
- only `Enforce runtime and integrity gates` failed because the client emitted no independent archive/content SHA-256 verification evidence.

Root cause: release preparation retained the selected asset table and GitHub `digest`, but the existing resolver reduced the selected release archive to its URL. The installer therefore called its existing archive verifier without an expected digest, which is a no-op.

# Implementation decision

The conditional configured-release adapter now owns the missing bridge:

1. normalize only valid SHA-256 release digests (`sha256:<64 hex>` or a bare 64-hex compatibility value);
2. remember a digest only for the exact selected `browser_download_url` returned from the configured GitHub Releases response;
3. wrap `HTTP.download` only for those exact mapped URLs;
4. read the completed archive from the existing `/downloads/` cache and verify it with `g_crypt.sha256` before forwarding success to the installer;
5. fail closed on read or digest mismatch;
6. restore both HTTP functions and clear URL/digest state on module unload.

No digest is inferred for codeload fallback and unrelated HTTP downloads are passed through unchanged.

# Coordination

PR #23 owns shared `docs/agents/MODULE_CATALOG.md` and `docs/agents/CHANGELOG.md`. This task does not edit those files without an explicit narrow lease. Behavior and validation evidence are recorded in the owning asset documentation and this task record.

# Acceptance criteria

- [ ] Actual configured release endpoint is queried and selected tag/archive URL/digest are recorded on the final head.
- [ ] Upstream `assets.json` matches its separately fetched `assets.json.sha256` on the final head.
- [ ] Focused Lua tests prove digest normalization, exact-URL verification, mismatch rejection, unrelated-download passthrough and unload restoration.
- [ ] Current Linux client builds and starts under Xvfb from a clean runtime directory.
- [ ] Shipped missing-assets prompt starts the unmodified installer flow.
- [ ] Final things, sounds, marker and required catalog files are present.
- [ ] `modules.client_assets.isClientVersionInstalled(1525)` returns true.
- [ ] `modules.game_things.isLoaded()` returns true after `g_game.setClientVersion(1525)`.
- [ ] Installed manifest identifier matches the independently fetched release-tag identifier.
- [ ] Client log records successful SHA-256 verification of the exact downloaded selected release archive.
- [ ] No downloaded game bytes are committed or uploaded.
- [ ] Operational rehearsal workflow is removed before merge.
- [ ] Final exact-head required CI, review-thread gate and complete changed-file review pass.
- [ ] Exact run, job, release, URL, digest, hashes and conclusion are recorded before archival.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T10:16:00+02:00
branch: ci/OTC-20260730-client-assets-real-release-rehearsal
pr: 97
status: implementing
required_base: 43ed867910907cd4ebcf9f14e64977105d08ab7e
proven:
  - first rehearsal completed real release resolution, build, install and fresh runtime load
  - final failure was isolated to missing independent archive/content integrity evidence
  - selected release asset retains a GitHub digest before the legacy resolver reduces it to a URL
  - existing selector, adapter, SHA-256 implementation and Lua runner are sufficient for a bounded fix
unknown:
  - exact final release metadata and digest until the restacked rehearsal runs
  - final exact-head CI outcome
conflicts:
  - shared changelog and module catalogue remain owned by PR #23 and are intentionally untouched
first_failure:
  marker: missing-runtime-archive-sha256-evidence
  evidence: run 30530600485 job 90831765205 step Enforce runtime and integrity gates
next_action: Restack PR #97 on current main, run focused and required CI, then repeat the real-release rehearsal.
```
