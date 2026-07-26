# OTClient Known Risks

## Repository-wide

- `opentibiabr/otclient` is read-only; verify repository before mutation.
- Open PR and active task state is authoritative; indexes can be stale.
- Proprietary assets, credentials, private captures and personal data must not be committed.
- Cross-repository protocol/login/identifier/asset facts require exact producer and consumer evidence.
- Greenfield routing must not erase the detailed legacy architecture/workstream knowledge still required by active existing-client work.

## Greenfield Rust client

- The foundation audit is mandatory. Premature Cargo bootstrap would freeze speculative protocol, asset and dependency assumptions.
- The existing C++/Lua/OTUI client is evidence only; linking or structurally porting it would undermine the greenfield architecture.
- Gameplay world channels can be confused with network streams. `WorldChannelId` means a parallel gameplay instance selected at login/relog.
- Canary compatibility can leak into the domain unless protocol-adapter boundaries and architecture checks are enforced.
- Oteryn native transport is not yet a client-only decision; premature QUIC/schema choices would create cross-repository debt.
- A broad global mutex/event bus or reflection-heavy ECS can recreate legacy coupling in a new language.
- High average FPS can hide frame-time spikes; performance requires reproducible scenes and percentile evidence.
- Asset pack/importer work is high risk for licensing, path traversal, decompression and unbounded allocation.
- Identity and game-ticket flows are vulnerable to stale callbacks, ticket replay and accidental password fallback.
- Reconnect and gameplay-channel relog are distinct lifecycles; mixing them can replay credentials or retain old session state.
- WebAssembly extensions require real quotas/capabilities; enabling them before the playable core increases security scope.
- Windows is the only initial required platform; portability architecture is not evidence of runtime compatibility.
- Parallel agents can conflict on shared `GameEvent`, `GameCommand`, render snapshot, asset schema and UI registry contracts.
- Dependency supply-chain, unsafe/FFI surface and license policy must be audited before adoption.

## Legacy client

- Module lifecycle leaks occur when events, keys, timers, widgets or callbacks are not cleaned up.
- Load-order bugs occur when modules capture globals too early or omit dependencies.
- Protocol field order, widths, signedness, opcode reuse and feature gates must match Canary.
- UI may work at one resolution while clipping or mis-scaling at another.
- Runtime Lua syntax CI intentionally scans `data`, `modules` and `mods`.
- Asset installation must retain strict hashes and standard final paths.
- Active legacy test/CI infrastructure should be reused rather than duplicated.

A legacy risk fix must not opportunistically change the greenfield architecture, and a Rust-client task must not modify legacy behavior unless separately owned.
