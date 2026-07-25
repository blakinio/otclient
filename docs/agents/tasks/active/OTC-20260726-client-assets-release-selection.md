---
task_id: OTC-20260726-client-assets-release-selection
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-client-assets-release-selection
base_branch: main
created: 2026-07-26T01:55:00+02:00
updated: 2026-07-26T01:55:00+02:00
last_verified_commit: "ff36aa74324eddbe6a64a79b23bd42d6a185fb7f"
risk: high
related_issue: "opentibiabr/otclient#1766"
related_pr: ""
depends_on: []
blocks:
  - production asset auto-install enablement for release archives
owned_paths:
  - modules/client_assets/client_assets.otmod
  - modules/client_assets/client_assets_release_selector.lua
  - modules/client_assets/client_assets_release_adapter.lua
  - tests/lua/fixtures/client_assets/releases.json
  - tests/lua/unit/client_assets_release_selector_test.lua
  - tests/lua/CMakeLists.txt
  - docs/client-assets-auto-install.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260726-client-assets-release-selection.md
modules_touched:
  - client_assets
reuses:
  - existing release resolver and codeload fallback
  - existing strict manifest SHA-256 checks
  - existing standard final paths and runtime completeness checks
  - existing Lua test runner
public_interfaces: []
cross_repo_tasks: []
---

# Goal

Prevent unrelated legacy or macOS release archives from being selected for a requested client version while preserving the existing codeload fallback, strict hashes and standard final installation paths.

# Acceptance criteria

- [ ] Release assets are prepared cache-stably from each release's own tag/name, not a transient requested version.
- [ ] A matching non-macOS archive is placed first for the existing resolver.
- [ ] macOS `.app.zip`, `macos` and standalone `mac` variants are excluded.
- [ ] An unrelated legacy archive is never accepted only because it is the first ZIP/RAR.
- [ ] A release with no matching archive contains no archive candidates, forcing the existing codeload fallback.
- [ ] Release fixtures cover matching tag, matching version label, client preference, legacy, Linux and macOS variants.
- [ ] Tests verify final things/sounds/extras path contracts and required runtime file locations.
- [ ] No proprietary or downloaded game assets are committed.
- [ ] Exact-head Lua Syntax, focused CTest and required CI pass.
- [ ] Real release rehearsal or an exact documented blocker remains before claiming production runtime archive compatibility.

# Confirmed context

- Current resolver `findReleaseArchive` returns the first non-mac archive and can fall back to an unrelated first archive.
- Upstream commit `465b7a217e87502bb7f9980bf6e099718d0a9a49` scores tag/version matches and falls back to codeload when no match exists.
- Directly replacing the 1559-line installer is unnecessary; the sandboxed module can prepare GitHub release JSON before the existing private resolver caches it.
- Preparation must be stable across later client-version requests because `releasesCache` stores the transformed response.
- Existing installer code already targets `data/things/<version>`, `data/sounds/<version>` and `bin`, and checks modern catalog/hash completeness before writing the completion marker.

# Plan

1. Add a pure release selector/preparer with synthetic fixtures.
2. Add a narrowly conditional GitHub releases JSON adapter before the existing resolver caches data.
3. Prove the old private selection semantics choose the prepared best archive or codeload fallback.
4. Record path/runtime completeness contracts without committing assets.
5. Validate and retain a real-release rehearsal blocker if no network/runtime artifact environment is available.

# Work log

## 2026-07-26T01:55:00+02:00

- Claimed the focused installer task on current `main` independently from the lifecycle/options stack.
- Confirmed that request-specific destructive reordering would poison the release cache; selection is therefore derived per release.
- External repositories remain read-only and no archive bytes are imported.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| pending | synthetic release selector fixtures | not-run |
| pending | final-path/runtime-file contract tests | not-run |
| pending | Lua Syntax | not-run |
| pending | Windows CMake Tests / CTest | not-run |
| pending | `CI / Required` | not-run |
| pending | real release rehearsal | blocker until a networked runtime/artifact environment exists |

# Risks and compatibility

- The adapter mutates only successful GitHub releases-array responses while the client-assets module is loaded.
- Other HTTP JSON requests pass through unchanged.
- Existing private resolver, strict hashes, extraction, paths and codeload fallback remain authoritative.
- Rollback is a normal squash revert.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Catalogue updated: not required; internal installer policy
- Changelog updated: pending
- Archived at: pending
