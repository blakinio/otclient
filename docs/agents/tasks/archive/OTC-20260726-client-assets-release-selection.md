---
task_id: OTC-20260726-client-assets-release-selection
coordination_id: ""
status: completed
agent: "GPT-5.6 Thinking"
branch: fix/OTC-20260726-client-assets-release-selection
base_branch: main
created: 2026-07-26T01:55:00+02:00
updated: 2026-07-29T15:24:00+02:00
last_verified_commit: "e02ef6bfb806639dfb003b2dc5913327cddf2594"
risk: high
related_issue: "opentibiabr/otclient#1766"
related_pr: "#37"
depends_on: []
blocks:
  - production runtime archive compatibility claim until the real-release rehearsal is completed
owned_paths:
  - modules/client_assets/client_assets.otmod
  - modules/client_assets/client_assets_release_selector.lua
  - modules/client_assets/client_assets_release_adapter.lua
  - tests/lua/fixtures/client_assets_releases.lua
  - tests/lua/unit/client_assets_release_selector_test.lua
  - tests/lua/CMakeLists.txt
  - docs/client-assets-auto-install.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/archive/OTC-20260726-client-assets-release-selection.md
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

# Result

PR #37 was squash-merged after a stable-current-base exact-head CI graph. The client-assets GitHub release adapter now prevents unrelated legacy or macOS archives from being selected for a requested client version while preserving the existing resolver, codeload fallback, strict hashes, extraction behavior and standard final installation paths.

The merged implementation:

- derives archive ordering cache-stably from each release's own tag/name;
- prefers matching non-macOS client archives;
- excludes `.app.zip`, `macos` and standalone `mac` variants;
- removes unrelated legacy archives from resolver candidates;
- leaves no archive candidates when nothing matches, forcing the existing codeload fallback;
- adapts only the exactly configured GitHub releases repository/path;
- passes unrelated repositories, paths, errors and non-table HTTP responses through unchanged;
- retains existing strict hashes, extraction, final paths and completion-marker behavior as authoritative.

# Acceptance criteria

- [x] Release assets are prepared cache-stably from each release's own tag/name, not a transient requested version.
- [x] A matching non-macOS archive is placed first for the existing resolver.
- [x] macOS `.app.zip`, `macos` and standalone `mac` variants are excluded.
- [x] An unrelated legacy archive is never accepted only because it is the first ZIP/RAR.
- [x] A release with no matching archive contains no archive candidates, forcing the existing codeload fallback.
- [x] Release fixtures cover matching tag, matching version label, client preference, legacy, Linux and macOS variants.
- [x] Tests verify final things/sounds/extras path contracts and required runtime file locations.
- [x] Only the focused test is registered; the shared Lua suite retains `LABELS "lua;unit"` without a global `assets` label.
- [x] No proprietary or downloaded game assets are committed.
- [x] Stable-current-base exact-head Lua Syntax, focused CTest, required Windows matrix and `CI / Required` passed.
- [x] A real-release rehearsal requirement and the current environment blocker are documented before any production runtime archive compatibility claim.

# Implementation

- `client_assets_release_selector.lua` scores matching archives, excludes macOS variants, removes unrelated archives and retains non-archive metadata.
- `client_assets_release_adapter.lua` wraps only the configured GitHub releases JSON response while loaded and restores the original HTTP function on unload.
- `client_assets_releases.lua` supplies synthetic matching, no-match, legacy, Linux, original, macOS and generic-tag fixtures without archive bytes.
- `client_assets_release_selector_test.lua` exercises resolver semantics after preparation, cache idempotence, URL scoping, HTTP restoration, final paths and runtime completeness.
- `tests/lua/CMakeLists.txt` registers only the focused test and leaves the shared suite labels unchanged.
- `docs/client-assets-auto-install.md` records the selection policy and mandatory networked clean-directory rehearsal before a production runtime claim.

# Final diff

The merged feature PR changed exactly these nine paths:

1. `docs/agents/CHANGELOG.md`
2. `docs/agents/tasks/active/OTC-20260726-client-assets-release-selection.md`
3. `docs/client-assets-auto-install.md`
4. `modules/client_assets/client_assets.otmod`
5. `modules/client_assets/client_assets_release_adapter.lua`
6. `modules/client_assets/client_assets_release_selector.lua`
7. `tests/lua/CMakeLists.txt`
8. `tests/lua/fixtures/client_assets_releases.lua`
9. `tests/lua/unit/client_assets_release_selector_test.lua`

The final compare was ahead `1`, behind `0`; no historical stack or unrelated files were included. `tests/lua/CMakeLists.txt` added only `unit/client_assets_release_selector_test.lua` to the existing test invocation.

# Validation and merge evidence

| Evidence | Result |
|---|---|
| stable base | `e9bcc172f005fb9993178b17f630acf382656090` |
| final feature head | `e02ef6bfb806639dfb003b2dc5913327cddf2594` |
| exact-head CI run | `30445396206`: PASS |
| Lua Syntax | PASS |
| Fast Checks / static analysis | PASS |
| Fast Checks / syntax and workflow validation | PASS |
| CMake Tests job `90554706852` | PASS, including `Run CMake` and `Run CTest` |
| CMake Release job `90554706875` | PASS |
| Solution OpenGL job `90554706885` | PASS |
| Solution DirectX job `90554706887` | PASS |
| Solution Debug job `90554706900` | PASS |
| `CI / Required` job `90570852453` | PASS |
| comments, reviews and unresolved threads | none |
| feature PR | #37 |
| squash merge | `fbf3c77e291dad8950e5b3ecfe1e3d47ab7a7b6b` |

Earlier exact-head runs that passed or partially progressed were preserved on backup branches whenever unrelated lifecycle work advanced `main`. The final backup before the last force-restack is `backup/OTC-20260726-client-assets-release-selection-pre-20260729-restack-7`.

# Production compatibility boundary

The real-release rehearsal was not performed and remains mandatory before claiming production runtime archive compatibility or enabling release archives as production-proven.

The rehearsal must use:

- a clean writable directory;
- the actual configured GitHub release endpoint and an actual configured release;
- recorded selected release tag and archive URL;
- strict manifest/hash and downloaded-byte integrity verification;
- verification of final `data/things/<version>`, `data/sounds/<version>` and runtime extras paths;
- verification that the completion marker is written only after the required runtime files are complete;
- a fresh startup using the exact target client version.

Synthetic fixtures, Lua tests, hosted Windows compilation and CTest success do not satisfy this networked runtime rehearsal. No production runtime archive compatibility claim is made by this task.

# Boundaries preserved

- no game/archive bytes or proprietary assets were committed;
- no authentication, protocol, renderer, Canary or server behavior changed;
- unrelated HTTP endpoints and response types remain unchanged;
- the existing resolver, strict hashes, extraction and codeload fallback remain authoritative;
- rollback is a normal squash revert of PR #37.

# Completion

- Final status: completed
- PR: #37
- Merge commit: `fbf3c77e291dad8950e5b3ecfe1e3d47ab7a7b6b`
- Catalogue updated: not required; internal installer policy
- Changelog updated: yes
- Archived at: `docs/agents/tasks/archive/OTC-20260726-client-assets-release-selection.md`
- Remaining blocker: real-release rehearsal before any production runtime archive compatibility claim
