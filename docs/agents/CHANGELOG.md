# Agent-Facing Change Log

Curated behavior/architecture log for discovery; not a replacement for Git history/release notes.

## Unreleased

- The target Oteryn client is now a greenfield Rust product isolated under `oteryn-client/`; Canary is the first protocol adapter, Oteryn is the target ecosystem, gameplay channels are selected through login/relog, and production workspace bootstrap is gated by a documented foundation audit. The existing C++/Lua/OTUI client remains legacy/reference evidence and is not a Rust runtime dependency.
- Forge now tracks every module-owned scheduled handle, cancels pending events before hide/game-end/terminate cleanup, releases callback references and uses generation guards so a raced stale callback cannot touch a reopened controller.
- Wheel of Destiny conviction summaries now use one named parser-order contract so skill, life leech, mana leech and five spell perks read slots 5-12 instead of the shifted legacy 3-10 assumptions.
- Action-bar cooldown protocol state is retained independently from visual options, subscribed for the module lifetime, reset at session boundaries and restored after relog/rebuild using the longest individual or spell-group remaining time for spells, runes and multi-actions.
- Character-list lifecycle now retains an absolute module-local OTUI path, safely recreates a destroyed legacy or Oteryn list from the existing login response, and returns to EnterGame instead of dereferencing a nil window when layout loading fails.
- The reviewed `opentibiabr/otclient` synchronization retains bounded unknown-opcode recovery, pre-780 inventory use-with lookup, ground-border multi-use targeting, animator-driven always-animated creature phases, NPC trade imbuement accounting/lifecycle cleanup, `--user-dir`, Stats pause/resume, manual-walk/bot coordination, browser Lua/UIGraph/shader compatibility and Cocoa mouse delta handling.
- Three reviewed upstream effects remain deliberately deferred: asset release-archive selection pending installer fixtures/path/runtime-load proof, Reward Wall source-byte semantics pending an exact Canary `OTS-*` contract, and rendering/preload ordering pending a framework-safe implementation without a framework-to-client dependency.
- Required CI compilation is temporarily Windows-only; Linux, macOS, Android, browser and Docker reusable workflows remain available but are not called by the primary workflow. Fast/static checks and Lua syntax remain required.
- Unix desktop browser URLs are now launched as exact process arguments instead of shell commands, preserving complete OAuth query strings and preventing shell metacharacter interpretation.
- Added persistent multi-agent coordination, autonomous PR/CI/merge rules, active-work discovery, module catalogue, task/handoff templates, ADRs, and cross-repository contracts.
- Protocol-game error callbacks now validate the exact source `ProtocolGame` before entering global `Game`, preventing delayed callbacks from obsolete sessions from disconnecting a replacement login.
- Deferred proxy and packet-player callbacks now retain explicit shared protocol ownership instead of asynchronously capturing raw `this`.
- Game connection-error, game-end and explicit logout paths now retain the exact source `ProtocolGame` through cleanup and revalidate identity after Lua-reentrant boundaries, so an obsolete session cannot disconnect its replacement.
- Deterministic game-lifecycle regression tests use a dedicated friend access seam instead of preprocessor access remapping, preserving MSVC link compatibility.
- Oteryn native authentication is active in PR #17: system-browser Authorization Code + PKCE, OS-assigned loopback callback, separate Platform Game Login Ticket issuance, standalone Game Gateway `/v1/login` consumption, server-authoritative world routing, and a one-shot `GameSessionKey` handoff consumed only after the actual `g_game.loginWorld` transfer without an Oteryn password fallback.
- The Oteryn login profile is disabled by default and production enablement remains blocked on the separately selected/proven Canary Game Session adapter and exact-version cross-repository E2E.

## 2026-07-12 bootstrap inventory

- Runtime Lua syntax checks are scoped to `data`, `modules`, and `mods` after merged PR #2.
- Reusable client unit/integration/Lua test foundation was merged in PR #3: message builders, fake resources/state, test environment, tile/thing builders, Lua runner/contracts, OTML fixtures, protocol loopback.
- Standalone agent handoff is active in PR #4 and must be reconciled with this system.
- Client-assets auto-install retains strict hashes and OTC-standard final paths.
