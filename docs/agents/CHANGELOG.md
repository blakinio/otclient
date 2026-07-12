# Agent-Facing Change Log

Curated behavior/architecture log for discovery; not a replacement for Git history/release notes.

## Unreleased

- Added persistent multi-agent coordination, autonomous PR/CI/merge rules, active-work discovery, module catalogue, task/handoff templates, ADRs, and cross-repository contracts.

## 2026-07-12 bootstrap inventory

- Runtime Lua syntax checks are scoped to `data`, `modules`, and `mods` after merged PR #2.
- Reusable client unit/integration/Lua test foundation is active in PR #3: message builders, fake resources/state, test environment, tile/thing builders, Lua runner/contracts, OTML fixtures, and protocol loopback.
- Standalone agent handoff is active in PR #4 and must be reconciled with this system.
- Client-assets auto-install retains strict hashes and OTC-standard final paths.
