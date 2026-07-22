# Agent-Facing Change Log

Curated behavior/architecture log for discovery; not a replacement for Git history/release notes.

## Unreleased

- Added persistent multi-agent coordination, autonomous PR/CI/merge rules, active-work discovery, module catalogue, task/handoff templates, ADRs, and cross-repository contracts.
- Protocol-game error callbacks now validate the exact source `ProtocolGame` before entering global `Game`, preventing delayed callbacks from obsolete sessions from disconnecting a replacement login.
- Deferred proxy and packet-player callbacks now retain explicit shared protocol ownership instead of asynchronously capturing raw `this`.
- Game connection-error, game-end and explicit logout paths now retain the exact source `ProtocolGame` through cleanup and revalidate identity after Lua-reentrant boundaries, so an obsolete session cannot disconnect its replacement.
- Deterministic game-lifecycle regression tests use a dedicated friend access seam instead of preprocessor access remapping, preserving MSVC link compatibility.
- Oteryn native authentication is active in PR #17: system-browser Authorization Code + PKCE, OS-assigned loopback callback, separate Platform Game Login Ticket issuance, standalone Game Gateway `/v1/login` consumption, server-authoritative world routing, and a one-shot `GameSessionKey` handoff consumed only after the actual `g_game.loginWorld` transfer without an Oteryn password fallback.
- The Oteryn login profile is disabled by default and production enablement remains blocked on the separately selected/proven Canary Game Session adapter and exact-version cross-repository E2E.

## 2026-07-12 bootstrap inventory

- Runtime Lua syntax checks are scoped to `data`, `modules`, and `mods` after merged PR #2.
- Reusable client unit/integration/Lua test foundation was merged in PR #3: message builders, fake resources/state, test environment, tile/thing builders, Lua runner/contracts, OTML fixtures, and protocol loopback.
- Standalone agent handoff is active in PR #4 and must be reconciled with this system.
- Client-assets auto-install retains strict hashes and OTC-standard final paths.
