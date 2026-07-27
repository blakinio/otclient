---
task_id: OTC-20260726-client-assets-release-selection
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-client-assets-release-selection
base_branch: main
created: 2026-07-26T01:55:00+02:00
updated: 2026-07-27T09:05:00+02:00
last_verified_commit: "070a1d842e0276e5db67a27eee6943304543445e"
risk: high
related_issue: "opentibiabr/otclient#1766"
related_pr: "#37"
depends_on: []
blocks:
  - production asset auto-install enablement for release archives
owned_paths:
  - modules/client_assets/client_assets.otmod
  - modules/client_assets/client_assets_release_selector.lua
  - modules/client_assets/client_assets_release_adapter.lua
  - tests/lua/fixtures/client_assets_releases.lua
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

- [x] Release assets are prepared cache-stably from each release's own tag/name, not a transient requested version.
- [x] A matching non-macOS archive is placed first for the existing resolver.
- [x] macOS `.app.zip`, `macos` and standalone `mac` variants are excluded.
- [x] An unrelated legacy archive is never accepted only because it is the first ZIP/RAR.
- [x] A release with no matching archive contains no archive candidates, forcing the existing codeload fallback.
- [x] Release fixtures cover matching tag, matching version label, client preference, legacy, Linux and macOS variants.
- [x] Tests verify final things/sounds/extras path contracts and required runtime file locations.
- [x] Only the new test is registered; the shared Lua suite retains `LABELS "lua;unit"` without a global `assets` label.
- [x] No proprietary or downloaded game assets are committed.
- [ ] Exact-head Lua Syntax, focused CTest and required Windows CI pass.
- [x] A real release rehearsal requirement and the current environment blocker are documented before any production runtime archive compatibility claim.

# Confirmed context

- Current resolver `findReleaseArchive` returns the first non-mac archive and can fall back to an unrelated first archive.
- Upstream commit `465b7a217e87502bb7f9980bf6e099718d0a9a49` scores tag/version matches and falls back to codeload when no best archive exists.
- Directly replacing the installer is unnecessary; the sandboxed module prepares GitHub release JSON before the existing private resolver caches it.
- Preparation is stable across later client-version requests because each release is transformed only from its own tag/name and marked idempotently.
- Existing installer code remains authoritative for strict hashes, extraction, `data/things/<version>`, `data/sounds/<version>`, `bin`, catalog/hash checks and completion marker timing.
- The adapter recognizes only the exactly configured GitHub releases repository/path after normalization; other repositories, paths and non-GitHub endpoints pass through unchanged.

# Implementation

- `client_assets_release_selector.lua` scores matching archives, excludes macOS variants, removes unrelated archives and retains non-archive metadata.
- `client_assets_release_adapter.lua` conditionally wraps only the configured GitHub releases JSON response and restores the original HTTP function on unload.
- `client_assets_releases.lua` supplies synthetic matching, no-match, legacy, Linux, original, macOS and generic-tag fixtures without archive bytes.
- `client_assets_release_selector_test.lua` exercises existing private resolver semantics after preparation, cache idempotence, conditional HTTP wrapping, final paths and catalog/runtime-file completeness.
- `tests/lua/CMakeLists.txt` registers only the focused test and leaves the shared suite labels unchanged.
- `docs/client-assets-auto-install.md` records the selection policy and mandatory networked clean-directory rehearsal before a production runtime claim.

# Work log

## 2026-07-26T01:55:00+02:00

- Claimed the focused installer task on then-current `main` independently from the lifecycle/options stack.
- Confirmed that request-specific destructive reordering would poison the release cache; selection is therefore derived per release.
- External repositories remained read-only and no archive bytes were imported.

## 2026-07-26T02:08:00+02:00

- Added selector, HTTP adapter, synthetic fixtures, focused tests, path/runtime contracts and documentation.
- Preserved the existing private resolver and codeload fallback rather than copying the full upstream installer diff.
- No local Lua interpreter, networked archive rehearsal or runnable graphical client was available. Repository CI can validate code/tests, but production runtime archive compatibility remains explicitly rehearsal-gated.

## 2026-07-27T09:05:00+02:00

- Re-ran repository preflight after PR #36 and its archive lifecycle merged.
- Preserved old PR head `070a1d842e0276e5db67a27eee6943304543445e` as `backup/OTC-20260726-client-assets-release-selection-pre-20260727-restack`.
- Rebuilt only the intended nine files on fresh `main` `0ce30abc4e582eb05dce1471153d85b1152d4d5e`.
- Retained all newer shared Lua test registrations and explicitly rejected adding `assets` to the common suite labels.
- Real-release rehearsal remains not performed; no claim of production runtime archive compatibility is made.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| `070a1d842e0276e5db67a27eee6943304543445e` | original draft head | superseded by restack |
| pending final restack head | exact nine-file diff review | pending after ref update |
| pending final restack head | Lua Syntax | pending required CI |
| pending final restack head | Windows CMake Tests / CTest | pending required CI |
| pending final restack head | required Windows matrix and `CI / Required` | pending |
| unavailable in this environment | real release rehearsal | explicit blocker: clean real-release download, hash validation and client startup evidence required |

# Risks and compatibility

- The adapter transforms only successful responses from the configured GitHub releases endpoint while the client-assets module is loaded.
- Other HTTP JSON requests pass through unchanged.
- Existing private resolver, strict hashes, extraction, paths and codeload fallback remain authoritative.
- Synthetic fixtures and compiled CI do not replace a real release download/startup rehearsal.
- Rollback is a normal squash revert.

# Remaining work

1. Move the completed nine-file restack onto the PR branch and re-review the exact diff and review state.
2. Mark PR #37 ready and pass exact-head Windows CMake Tests/CTest, the required Windows matrix and `CI / Required`.
3. Squash-merge the code if green while retaining the real-release rehearsal blocker.
4. Archive this task in a separate docs-only PR with final head, CI run, squash merge SHA and the unresolved rehearsal requirement.

# Completion

- Final status: in progress
- PR: #37
- Merge commit: pending
- Catalogue updated: not required; internal installer policy
- Changelog updated: yes
- Archived at: pending
