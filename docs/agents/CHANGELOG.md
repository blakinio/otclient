# Agent-Facing Change Log

Curated behavior/architecture log for discovery; not a replacement for Git history/release notes.

## Unreleased

- Added persistent multi-agent coordination, autonomous PR/CI/merge rules, active-work discovery, module catalogue, task/handoff templates, ADRs, and cross-repository contracts.
- Protocol-game error callbacks now validate the exact source `ProtocolGame` before entering global `Game`, preventing delayed callbacks from obsolete sessions from disconnecting a replacement login.
- Deferred proxy and packet-player callbacks now retain explicit shared protocol ownership instead of asynchronously capturing raw `this`.
- Game connection-error, game-end and explicit logout paths now retain the exact source `ProtocolGame` through cleanup and revalidate identity after Lua-reentrant boundaries, so an obsolete session cannot disconnect its replacement.
- Deterministic game-lifecycle regression tests use a dedicated friend access seam instead of preprocessor access remapping, preserving MSVC link compatibility.
- Outbound protocol sends now serialize recording, framing, client sequence allocation and transport enqueue per protocol instance, preventing duplicate/gapped or wire-reordered sequenced packets when messages are emitted concurrently.

## 2026-07-12 bootstrap inventory

- Runtime Lua syntax checks are scoped to `data`, `modules`, and `mods` after merged PR #2.
- Reusable client unit/integration/Lua test foundation is active in PR #3: message builders, fake resources/state, test environment, tile/thing builders, Lua runner/contracts, OTML fixtures, and protocol loopback.
- Standalone agent handoff is active in PR #4 and must be reconciled with this system.
- Client-assets auto-install retains strict hashes and OTC-standard final paths.
