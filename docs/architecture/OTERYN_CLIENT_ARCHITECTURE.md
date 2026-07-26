# Oteryn Client Architecture Routing

Status: routing document  
Last reviewed: 2026-07-26

The normative target architecture for the new Oteryn client is now:

- `oteryn-client/docs/architecture/ARCHITECTURE.md`
- `oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md`
- `oteryn-client/docs/architecture/CLIENT_LIFECYCLE.md`
- `oteryn-client/docs/architecture/MODULE_MODEL.md`
- `oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md`
- `oteryn-client/docs/architecture/SECURITY_MODEL.md`
- `oteryn-client/docs/architecture/PERFORMANCE_AND_TESTING.md`
- `oteryn-client/docs/architecture/ASSET_PIPELINE.md`

The target product is a greenfield Rust client under `oteryn-client/`. Canary is its first compatibility adapter and Oteryn is the long-term target ecosystem.

The existing C++/Lua/OTUI implementation under `src/`, `modules/`, `mods/` and related legacy paths remains buildable during migration. It is classified as legacy/reference evidence and is not the architectural template or runtime dependency of the Rust client.

Existing legacy-client tasks and PRs must continue to follow the root repository safety, ownership, protocol and validation rules for the paths they own. They must not claim that incremental C++/Lua work implements the greenfield architecture.

New Rust-client work must read the root `AGENTS.md`, then `oteryn-client/AGENTS.md`, and must pass the foundation audit gate before production workspace bootstrap.
