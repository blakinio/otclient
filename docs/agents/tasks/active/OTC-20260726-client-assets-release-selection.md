---
task_id: OTC-20260726-client-assets-release-selection
coordination_id: ""
status: in_progress
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-client-assets-release-selection
base_branch: main
created: 2026-07-26T01:55:00+02:00
updated: 2026-07-29T12:25:00+02:00
last_verified_commit: "a26efb7af14afe39e310cb393b130d4270fc1673"
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
- [ ] Final current-base exact-head Lua Syntax, focused CTest, required Windows matrix and `CI / Required` pass.
- [x] A real release rehearsal requirement and the current environment blocker are documented before any production runtime archive compatibility claim.

# Confirmed context

- The legacy resolver returns the first non-mac archive and can otherwise accept an unrelated first archive.
- Upstream commit `465b7a217e87502bb7f9980bf6e099718d0a9a49` scores tag/version matches and falls back to codeload when no best archive exists.
- The sandboxed module prepares GitHub release JSON before the existing private resolver caches it; the installer itself is not replaced.
- Preparation is derived independently from each release's tag/name and is idempotently marked, so later client-version requests do not poison cached data.
- Existing installer code remains authoritative for strict hashes, extraction, `data/things/<version>`, `data/sounds/<version>`, runtime extras, catalog/runtime checks and completion-marker timing.
- The adapter recognizes only the exactly configured GitHub releases repository/path after normalization; unrelated repositories, paths, errors and non-table responses pass through unchanged.

# Implementation

- `client_assets_release_selector.lua` scores matching archives, excludes macOS variants, removes unrelated archives and retains non-archive metadata.
- `client_assets_release_adapter.lua` wraps only the configured GitHub releases JSON response while loaded and restores the original HTTP function on unload.
- `client_assets_releases.lua` supplies synthetic matching, no-match, legacy, Linux, original, macOS and generic-tag fixtures without archive bytes.
- `client_assets_release_selector_test.lua` exercises resolver semantics after preparation, cache idempotence, URL scoping, HTTP restoration, final paths and runtime completeness.
- `tests/lua/CMakeLists.txt` registers only the focused test and leaves the shared suite labels unchanged.
- `docs/client-assets-auto-install.md` records the selection policy and mandatory networked clean-directory rehearsal before a production runtime claim.

# Work log

## 2026-07-26 implementation

- Claimed the focused installer task independently from the lifecycle/options stack.
- Confirmed request-specific destructive reordering would poison the release cache, so selection is derived per release.
- Added the selector, conditional HTTP adapter, synthetic fixtures, focused tests, path/runtime contracts and documentation.
- Preserved the existing private resolver and codeload fallback; no archive bytes or proprietary assets were imported.
- The environment lacked a networked archive rehearsal and runnable graphical client, so production runtime compatibility remained explicitly rehearsal-gated.

## 2026-07-27 restack and required-check history

- Preserved the original head `070a1d842e0276e5db67a27eee6943304543445e` before the first force-restack.
- Rebuilt only the intended nine files on each fresh `main`; all newer shared Lua registrations were retained and adding `assets` to the common suite labels was explicitly rejected.
- Run `30244985640` on `2ae0aa80d8448b43b81a5951fe1402ed0a440be3` passed Lua Syntax, Fast Checks, all required Windows jobs, CMake Tests/CTest and `CI / Required`, but branch protection initially kept the required check in `expected` state.
- A clean synchronize event was produced without changing the nine-file scope; subsequent heads and runs were preserved as backups whenever `main` advanced.
- Runs `30249989537`, `30252961648`, `30255867747` and their associated heads became superseded because unrelated Rust/orchestration lifecycle PRs advanced `main` while Windows CI was running.
- Every restack was preceded by a backup branch and every base comparison confirmed that only the changelog overlapped; the seven implementation/test/docs files and the CMake registration remained untouched upstream.

## 2026-07-29 current-base reconciliation

- Exact-head run `30257714952` on `b04c6d3dc69797268f03af9823db4a7c99e0ee38` completed successfully: Lua Syntax, both Fast Checks, all five Windows build variants, CMake Tests/CTest and `CI / Required` were green.
- Before merge, `main` advanced through additional Rust diagnostics and evidence-wave lifecycle work to `0b1cd7914c04efd6b41a4a1b975234df715e6104`, making that otherwise successful run superseded as final merge evidence.
- Preserved the verified head as `backup/OTC-20260726-client-assets-release-selection-pre-20260729-restack`.
- Compared all thirteen intervening commits: only `docs/agents/CHANGELOG.md` overlaps the nine owned paths.
- Reconciled the current diagnostics/foundation changelog entries, converted assets selection from deferred to implemented, retained the two unrelated deferred effects, and rebuilt the exact same nine-file scope on current `main`.
- Real-release rehearsal is still not performed and remains an explicit blocker to any production runtime archive compatibility claim.

## 2026-07-29 final Windows validation and W4 restack

- Exact-head run `30438208569` on `a26efb7af14afe39e310cb393b130d4270fc1673` passed Lua Syntax, both Fast Checks, all five Windows build variants, CMake Tests with `Run CTest`, and `CI / Required` job `90547397445`.
- Before auto-merge could execute, docs-only W4 planning PRs #77 and #78 advanced `main` to `b16e0a8c17cf1ce7b0808ef577cce0d5bc76f0b3`; neither PR overlaps any of the nine owned paths.
- Preserved the fully verified head as `backup/OTC-20260726-client-assets-release-selection-pre-20260729-restack-6` and rebuilt the same nine-file scope on the new base.
- The synchronized current-base head requires one final exact-head CI graph before squash merge. The real-release rehearsal remains unperformed and production runtime archive compatibility is still not claimed.

# Validation and CI

| Commit | Check | Result |
|---|---|---|
| `070a1d842e0276e5db67a27eee6943304543445e` | original draft head | superseded by restack |
| `2ae0aa80d8448b43b81a5951fe1402ed0a440be3` | run `30244985640`: Lua, Windows matrix, CTest, `CI / Required` | PASS; superseded after required-check attachment refresh |
| `c2157fe77169a08ca9f8a263fe69c313ff6a4fd2` | run `30249989537` | superseded because `main` advanced |
| `e9d420c90a9b291c79b122a5a0198db67a538ed2` | run `30252961648` | superseded because `main` advanced |
| `ef4814cbc9f54774a27f11acbfb426b1e4c76cd3` | run `30255867747` | superseded because `main` advanced |
| `b04c6d3dc69797268f03af9823db4a7c99e0ee38` | run `30257714952`: Lua, full Windows matrix, CMake Tests/CTest, `CI / Required` | PASS; superseded because `main` advanced to `0b1cd7914c04efd6b41a4a1b975234df715e6104` |
| `a26efb7af14afe39e310cb393b130d4270fc1673` | run `30438208569`: Lua, full Windows matrix, CMake Tests/CTest, `CI / Required` job `90547397445` | PASS; superseded because docs-only #77/#78 advanced `main` to `b16e0a8c17cf1ce7b0808ef577cce0d5bc76f0b3` |
| pending synchronized current-base head | final exact-head Windows CI and `CI / Required` | pending |
| unavailable in this environment | real release rehearsal | explicit blocker: clean real-release download, strict integrity validation and exact-client startup evidence required |

# Risks and compatibility

- The adapter transforms only successful table responses from the configured GitHub releases endpoint while the client-assets module is loaded.
- Other HTTP JSON requests and failures pass through unchanged.
- Existing private resolver, strict hashes, extraction, paths and codeload fallback remain authoritative.
- Synthetic fixtures and compiled CI do not replace a real release download/startup rehearsal.
- Rollback is a normal squash revert.

# Remaining work

1. Pass the current-base restack head's exact-head Windows CMake Tests/CTest, required Windows matrix and `CI / Required`.
2. Re-check the exact nine-file diff, reviews and current `main`, then squash-merge.
3. Archive this task in a separate docs-only PR with final head, CI run, squash merge SHA and the unresolved rehearsal requirement.

# Completion

- Final status: in progress
- PR: #37
- Merge commit: pending
- Catalogue updated: not required; internal installer policy
- Changelog updated: yes
- Archived at: pending
