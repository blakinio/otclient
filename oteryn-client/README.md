# Oteryn Client

Status: architecture and audit phase  
Primary implementation language: Rust  
Initial desktop target: Windows  
First game-server compatibility target: Canary  
Long-term game-server target: Oteryn

`oteryn-client/` is the isolated home of the new first-party Oteryn game client. It is a greenfield product, not a line-by-line rewrite of the current C++/Lua/OTUI client.

The existing repository roots `src/`, `modules/`, `mods/`, `data/` and the existing CMake build remain the legacy client. They may be inspected for verified behavior, protocol evidence, asset metadata and regression scenarios, but the Rust client must not link them, execute their Lua/OTUI modules, include their headers or inherit their global-state architecture.

## Product contract

The client must provide:

- Oteryn Identity login through Authorization Code + PKCE in the system browser;
- no collection or transmission of the user's main Oteryn password to a game server;
- account, character, world and gameplay-channel selection;
- a one-shot game-session handoff scoped to the selected character, world and channel;
- login to Canary through a compatibility adapter during the migration period;
- later login to native Oteryn game services through a separate adapter;
- relog from one gameplay channel to another by closing the current game session and creating a new one;
- a high-performance data-oriented runtime, modern GPU renderer and native Rust UI;
- signed and verified updates and asset packs;
- deterministic testing, replay and profiling support.

A gameplay channel means a parallel instance of one world, such as `Channel 1`, `Channel 2` and `Channel 3`. It is selected during login or relog. It is not a network multiplexing stream.

## Start here

1. Read the repository root `AGENTS.md`.
2. Read `oteryn-client/AGENTS.md`.
3. Read `docs/architecture/ARCHITECTURE.md`.
4. Read `docs/architecture/REPOSITORY_LAYOUT.md`.
5. Read `docs/agents/PROGRAM.md` and `docs/agents/WORKSTREAMS.md`.
6. Inspect the live task records and open pull requests before claiming work.

The first implementation work is blocked by the foundation audit defined in `docs/agents/AUDIT_PLAN.md`. The audit may create documentation, fixtures inventories and benchmark plans, but it must not bootstrap production crates or choose protocol facts without evidence.

## Planned top-level structure

```text
oteryn-client/
├── AGENTS.md
├── README.md
├── Cargo.toml                    # created after the audit gate
├── Cargo.lock
├── rust-toolchain.toml
├── apps/
├── crates/
├── features/
├── tools/
├── contracts/
├── assets/
├── tests/
├── benches/
└── docs/
```

The complete planned tree and dependency rules are normative in `docs/architecture/REPOSITORY_LAYOUT.md`.

## Current phase

This directory initially contains architecture and agent-operating documents only. Creating placeholder crates before the audit is intentionally prohibited: empty abstractions would appear authoritative before the Canary protocol, asset legality, target hardware and feature inventory are verified.
