# ADR-0004: Static First-Party Modules and Sandboxed WebAssembly Extensions

Status: accepted  
Date: 2026-07-26

## Context

The client needs clear modular ownership and possible future extensibility without placing dynamic dispatch, arbitrary native code or scripting hooks in performance/security-critical paths.

## Decision

Compile engine and first-party gameplay features as Rust crates with explicit dependency direction and typed contracts.

Optional third-party extensions, when introduced, run as WebAssembly guests with versioned capability-limited host APIs, memory/execution quotas and isolated storage.

Do not retain Lua/OTUI compatibility and do not support native dynamic plugins by default.

## Consequences

- first-party behavior is optimized and statically reviewable;
- feature boundaries are enforced through crates and architecture tests;
- extension crashes and abuse can be contained;
- extension APIs require deliberate versioning and host implementation work;
- extension delivery is deferred until after the playable core.

## Rejected

- Lua as the primary first-party feature language;
- arbitrary script access to game globals;
- DLL/native plugin loading;
- making every engine subsystem dynamically unloadable;
- a single global event bus as the only module contract.
