# OTClient Module and System Catalogue

Last reviewed: 2026-07-12

This catalogue makes reusable client work visible. Verify source, manifests, tests, and open PR state before use.

## Maintenance contract

Update this file in the same PR that adds/changes a reusable module, controller, widget infrastructure, protocol helper, message/test utility, platform abstraction, asset installer, public configuration, or integration contract. Include active PR work early so another agent does not duplicate it.

## Core client/module areas

| Module/system | Status | Responsibility/public surface | Primary paths | Reuse/safety notes |
|---|---|---|---|---|
| Shipped game modules | maintained | Feature UI/controllers and interaction loaded through manifests | `modules/**` | Extend owning module; preserve dependencies, lifecycle cleanup, events, keys, widgets, localization. |
| Optional/custom mods | maintained | Optional behavior outside shipped core | `mods/**` | Do not hide a required core fix here. Runtime Lua syntax CI covers this root. |
| Protocol and features | maintained | Packet parsing/output, feature flags, game state | `src/client/**`, `modules/game_features/**`, affected modules | Check Canary payloads/opcodes/version gates and contracts. |
| Client assets auto-install | maintained | Secure things/sounds/runtime-extra installation | installer sources and `docs/client-assets-auto-install.md` | Final paths remain `data/things/<version>/`, `data/sounds/<version>/`, expected `bin/*`; strict hashes stay enabled. |

## Reusable test infrastructure

| Module/tool | Status | Responsibility/public surface | Source/docs | Reuse notes |
|---|---|---|---|---|
| Client test foundation | active PR #3 | Deterministic C++ builders/assertions/fakes/environment, OTML fixtures, protocol loopback, Lua runner/contracts | `tests/support/**`, `tests/unit/**`, `tests/integration/**`, `tests/lua/**`, `tests/fixtures/**`, testing docs | Reuse support, labels, fixtures, and presets; do not create a second harness. |
| InputMessageBuilder | active #3 | Deterministic framed parser inputs | `tests/support/builders/input_message_builder.{h,cpp}` | Reuse for parser/protocol tests. |
| OutputMessageInspector | active #3 | Inspects encoded output bytes in tests | `tests/support/builders/output_message_inspector.h` | Reuse instead of ad hoc internals. |
| Thing/Tile builders/assertions | active #3 | Synthetic things/items/creatures and tile assertions | `tests/support/builders/thing_builders.*`, `tests/support/assertions/tile_assertions.h` | Reuse for map/tile/module tests. |
| TestEnvironment/fakes | active #3 | Deterministic lifecycle and substitutes for global resources/game state | `tests/support/test_environment/**`, `tests/support/mocks/**` | Prefer over new global mocking layers. |
| Lua runner/stubs | active #3 | Named assertions, deterministic failure, minimal globals | `tests/lua/helpers/**` | Add focused tests to existing runner/contracts. |
| Protocol loopback | active #3 | Bounded local socket integration for framed packets | `tests/integration/protocol/loopback_packet_test.cpp` | Extend for protocol regression cases. |

## Current governance work

| Item | Status | Paths | Note |
|---|---|---|---|
| Existing agent handoff | active PR #4 | `AGENT_HANDOFF.md` | Reconcile with `docs/agents/**`; avoid contradictory systems. |

## Entry template

```md
### Module name
- Status:
- Responsibility/public surface:
- Source paths:
- Manifest/startup/dependencies:
- Tests:
- Documentation:
- Used by:
- Task/PR:
- Last verified commit:
```
