# OTClient Module and System Catalogue

Last reviewed: 2026-07-27

This catalogue makes reusable work visible across the greenfield Rust client and existing OTClient. Verify source, manifests, tasks, tests and open PR state before use.

## Maintenance contract

Update this file in the same PR that adds or changes a reusable module/crate, controller, widget infrastructure, protocol helper, test utility, platform abstraction, asset installer/format, public configuration or integration contract. Include active PR work early so another agent does not duplicate it.

## Greenfield Rust client

| Module/system | Status | Responsibility/public surface | Primary paths | Reuse/safety notes |
|---|---|---|---|---|
| Greenfield architecture package | merged PR #45 | Normative Rust client architecture, workspace plan, lifecycle, protocol boundary, module/security/performance/asset models and agent program | `oteryn-client/docs/architecture/**`, `oteryn-client/docs/agents/**` | Target architecture. Legacy code is evidence only and is not a Rust runtime dependency. |
| Rust foundation audit | merged PR #47 | Verified product/Canary/Oteryn/assets/performance/platform/test inputs, risks/gaps and first implementation recommendation | `oteryn-client/docs/audits/foundation/**` | Authorizes narrow packages only. Channel-aware native routing, real asset rights and numeric performance/hardware evidence remain separate gates. |
| Rust workspace policy | active PR #50 | One-member Rust workspace, pinned toolchain, lockfile, workspace lints, dependency policy and additive Rust CI | `oteryn-client/Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `rustfmt.toml`, `deny.toml`, `.github/workflows/rust-client.yml` | Contains no product application or engine crate. Windows is required compiled proof; cargo-deny runs as a separate supply-chain job. |
| Oteryn architecture checker | active PR #50 | Validates workspace package names/categories, path containment, dependency sources, forbidden category edges, unresolved path dependencies and cycles | `oteryn-client/tools/architecture-check/**`, `oteryn-client/tests/architecture-fixtures/**` | Metadata/graph policy only. It does not replace Cargo, source review, security review, protocol tests or runtime validation. |
| Rust workspace operations | active PR #50 | Commands, category metadata, rule codes, CI/supply-chain policy and procedure for adding the next crate | `oteryn-client/docs/operations/RUST_WORKSPACE.md` | Read before editing workspace manifests or adding a category/crate. |
| Next foundation agent prompt | active PR #50 | Copy-ready bounded prompt for one standard-library-first foundation primitives crate | `oteryn-client/docs/agents/prompts/NEXT_FOUNDATION_AGENT.md` | Use only after PR #50 is merged and archived; fresh preflight remains mandatory. |

## Existing legacy client/module areas

Detailed maintenance boundaries are in `docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md` and `docs/agents/LEGACY_OTCLIENT_WORKSTREAMS.md`.

| Module/system | Status | Responsibility/public surface | Primary paths | Reuse/safety notes |
|---|---|---|---|---|
| Shipped game modules | maintained legacy | Feature UI/controllers and interaction loaded through manifests | `modules/**` | Extend owning module; preserve dependencies, lifecycle cleanup, events, keys, widgets and localization. Do not structurally port into Rust. |
| Optional/custom mods | maintained legacy | Optional behavior outside shipped core | `mods/**` | Do not hide a required core fix here. Runtime Lua syntax CI covers this root. This is not the Rust extension model. |
| Protocol and features | maintained legacy | Packet parsing/output, feature flags and game state | `src/client/**`, `modules/game_features/**`, affected modules | Check Canary payloads/opcodes/version gates and contracts. Rust consumes only audited evidence. |
| Protocol game callback guard | maintained legacy; hardening PR #9 | Carries an exact source `ProtocolGame` through connection-error, game-end and disconnect cleanup; supports before/after callback identity checks | `src/client/protocolgamecallbackguard.h`, `src/client/protocolgame.cpp`, `src/client/game.{h,cpp}` | Reuse for legacy lifecycle callbacks entering global `Game`; capture once and revalidate after Lua/callback boundaries. Rust uses generation-owned sessions independently. |
| Oteryn native identity login | maintained legacy; PR #17 evidence | System-browser Authorization Code + PKCE, loopback callback, Platform Game Login Ticket, Game Gateway response normalization and one-shot Game Session handoff | `modules/client_entergame/oteryn_identity*.lua`, `modules/client_entergame/oteryn_session_guard.lua`, `src/framework/net/server.*`, `src/framework/util/crypt.cpp`, `init.lua` | First-party Oteryn profile only; disabled by default; no password fallback; routing from Gateway. Security/contract evidence for the independent Rust implementation. |
| Unix external URL launch | maintained legacy; PR #20 | Launches browser URLs as exact argv values without shell parsing on Unix desktop | `src/framework/platform/unixplatform.cpp`, `tests/unit/framework/platform_open_url_test.cpp` | Reuse `Platform::spawnProcess` in legacy; never interpolate external URLs into a shell command. Not proof of Rust platform support. |
| Client assets auto-install | maintained legacy | Secure things/sounds/runtime-extra installation | installer sources and `docs/client-assets-auto-install.md` | Final paths remain `data/things/<version>/`, `data/sounds/<version>/`, expected `bin/*`; strict hashes stay enabled. Rust uses a separate signed pack pipeline. |
| Runtime Stats collection controls | maintained legacy; merged PR #26 | Lua-visible `g_stats.pause()`/`resume()` suspend or resume new performance-stat samples | `src/framework/util/stats.{h,cpp}`, `src/framework/luafunctions.cpp` | Treat as diagnostics policy, not correctness/security. Useful only as legacy baseline evidence for Rust audit. |
| User-directory override | maintained legacy; merged PR #26 | `--user-dir=<path>` redirects persisted legacy state | `src/main.cpp`, `src/framework/core/resourcemanager.{h,cpp}` | Apply before `init.lua` resolves write directory. Do not infer greenfield settings/security policy from it. |
| Bot/manual-walk coordination | maintained legacy; merged PR #26 | `TargetBot.Danger()` and `modules.game_interface.lastManualWalk` expose optional runtime coordination | bot mod and `modules/game_interface/gameinterface.lua`, `modules/game_walk/walk.lua` | Consumers tolerate missing/offline optional modules. Runtime-only and never authoritative movement/combat state. |

## Reusable existing-client test infrastructure

| Module/tool | Status | Responsibility/public surface | Source/docs | Reuse notes |
|---|---|---|---|---|
| Client test foundation | maintained legacy; merged PR #3 | Deterministic C++ builders/assertions/fakes/environment, OTML fixtures, protocol loopback and Lua runner/contracts | `tests/support/**`, `tests/unit/**`, `tests/integration/**`, `tests/lua/**`, testing docs | Reuse for legacy work. Rust audit may reuse behavior evidence but the Rust workspace receives native Cargo test support. |
| InputMessageBuilder | maintained legacy | Deterministic framed parser inputs | `tests/support/builders/input_message_builder.{h,cpp}` | Reuse instead of ad hoc legacy internals; audit semantics/provenance before Rust equivalents. |
| OutputMessageInspector | maintained legacy | Inspects encoded output bytes in tests | `tests/support/builders/output_message_inspector.h` | Reuse for legacy output tests; not a Rust dependency. |
| Thing/Tile builders/assertions | maintained legacy | Synthetic things/items/creatures and tile assertions | `tests/support/builders/thing_builders.*`, `tests/support/assertions/tile_assertions.h` | Reuse for legacy map/tile tests; audit behavior before recreation. |
| TestEnvironment/fakes | maintained legacy | Deterministic lifecycle and substitutes for global resources/game state | `tests/support/test_environment/**`, `tests/support/mocks/**` | Prefer over another legacy global mocking layer. Rust gets independent typed fakes. |
| Lua runner/stubs | maintained legacy | Named assertions, deterministic failure and minimal globals | `tests/lua/helpers/**` | Add focused legacy tests to the existing runner/contracts. |
| Protocol loopback | maintained legacy | Bounded local socket integration for framed packets | `tests/integration/protocol/loopback_packet_test.cpp` | Extend for legacy regressions. Does not prove Rust adapter compatibility. |

## Current governance work

| Item | Status | Paths | Note |
|---|---|---|---|
| Existing agent handoff | active PR #4 | `AGENT_HANDOFF.md` | Reconcile with root/nested agent docs; avoid contradictory rules. |
| Official Tibia Linux runner analysis | draft operational PR #48 | dedicated workflow and task record | One-off non-merge operational analysis; does not own Rust workspace/product paths. |
| Rust workspace bootstrap | active PR #50 | Rust workspace/tooling/CI/docs paths listed above | Single authorized WS-R01 package; product crates remain out of scope. |

## Entry template

```md
### Module name
- Track: greenfield-rust | legacy-client
- Status:
- Responsibility/public surface:
- Source paths:
- Manifest/startup/dependencies/lifecycle:
- Tests:
- Documentation:
- Used by:
- Task/PR:
- Last verified commit:
```
