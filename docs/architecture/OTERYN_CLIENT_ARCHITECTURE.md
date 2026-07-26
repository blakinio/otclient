# Oteryn Client Architecture Routing

Status: routing document  
Last reviewed: 2026-07-27

## Target product

The normative target architecture for the new Oteryn client is:

- `oteryn-client/docs/architecture/ARCHITECTURE.md`
- `oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md`
- `oteryn-client/docs/architecture/CLIENT_LIFECYCLE.md`
- `oteryn-client/docs/architecture/MODULE_MODEL.md`
- `oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md`
- `oteryn-client/docs/architecture/SECURITY_MODEL.md`
- `oteryn-client/docs/architecture/PERFORMANCE_AND_TESTING.md`
- `oteryn-client/docs/architecture/ASSET_PIPELINE.md`

The target product is a greenfield Rust client under `oteryn-client/`. Canary is its first compatibility adapter and Oteryn is the long-term target ecosystem.

## Existing client

The maintained architecture needed to finish and support existing C++/Lua/OTUI work is preserved in:

- `docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md`
- `docs/agents/LEGACY_OTCLIENT_WORKSTREAMS.md`

The existing implementation under `src/`, `modules/`, `mods/` and related legacy paths remains buildable during migration. It is legacy/reference evidence for the Rust track and is not its architectural template or runtime dependency.

Existing legacy-client tasks and PRs continue to follow root repository safety, ownership, protocol and validation rules for their owned paths. They must not claim that incremental C++/Lua work implements the greenfield architecture.

New Rust-client work reads the root `AGENTS.md`, then `oteryn-client/AGENTS.md`, and must pass the foundation audit gate before production workspace bootstrap.
