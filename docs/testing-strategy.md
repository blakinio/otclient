# OTClient Redemption testing strategy

## Purpose

This document defines the first testing foundation for the OTClient Redemption
fork. The foundation favours deterministic, process-local tests and small test
seams over changes to game behaviour. It is intentionally narrower than the
Canary server suite because the client owns graphics, audio, Lua, global
managers, and protocol presentation concerns that are not present in the
server.

Every bug fix should include a regression test when technically possible. A
test that demonstrates an existing defect must not be enabled as a failing CI
test before the production fix is intentionally reviewed.

## Current state before this foundation

Tests are opt-in through `OTCLIENT_BUILD_TESTS=ON`. Configuration fails early
unless the vcpkg manifest feature `tests` is enabled, and that feature supplies
GoogleTest. `tests/CMakeLists.txt` provides `otclient_add_gtest`, which links a
test executable to `otclient_core` and discovers individual GoogleTest cases
for CTest.

The initial suite contains 23 discovered GoogleTest cases in three targets:

| Target | Cases | Coverage |
| --- | ---: | --- |
| `otclient_map_spectator_tests` | 9 | tile creature spans and deterministic map spectator queries |
| `otclient_string_encoding_tests` | 5 | UTF-8, Latin-1, and UTF-16 conversion |
| `otml_tests` | 9 | root and scoped aliases plus malformed/circular references |

The existing source directories are `tests/map`, `tests/stdext`, and
`tests/otml`. They remain in place in this PR to keep target names and history
stable.

`linux-debug` enables tests and the vcpkg feature. CI builds that preset and
runs unfiltered CTest on Linux Debug. Windows has `windows-tests` and ASAN test
presets, and macOS Debug enables tests, but the ordinary Windows and macOS CI
jobs build release client configurations without executing CTest. The separate
Lua job compiles runtime Lua files with LuaJIT; it does not execute behavioural
Lua tests.

## Testability constraints

- `InputMessage` and `OutputMessage` use an absolute buffer cursor after a
  reserved network-header prefix. Body size and absolute cursor position are
  deliberately different concepts.
- `InputMessage`, `OutputMessage`, `ProtocolGame`, `Tile`, and `ThingType`
  consult process-global client state. Even constructors can depend on
  `g_game` client version.
- Protocol parsing writes directly to `g_game`, `g_map`, `g_lua`, and a local
  player. Parser methods are private and the opcode loop combines dispatch,
  error reporting, and cursor progress.
- Tile classification depends on `ThingType` metadata normally loaded from
  licensed runtime data. Tests must construct synthetic metadata and must not
  copy proprietary assets.
- Resource, texture, dispatcher, application, Lua, sound, and game managers
  have lifecycle ordering requirements. A process-wide environment can prepare
  them, while per-test cleanup must remove mutable state.
- Runtime Lua modules assume globals such as `g_game`, `g_ui`, `g_resources`,
  `g_logger`, and `modules`. Only modules whose dependency surface can be
  represented by small explicit stubs are suitable for the first suite.
- A true startup currently creates platform, rendering, sound, and module
  infrastructure together. A GPU-free startup test needs a small future
  application bootstrap seam rather than preprocessor-heavy test code.

## Target architecture

The first PR uses the additive migration option: existing directories and
target names remain stable, while new tests use the following structure.

```text
tests/
  unit/
    client/
    framework/
    protocol/
    map/
    items/
    resources/
    ui/
  integration/
    protocol/
    modules/
    startup/
  lua/
    unit/
    contracts/
    helpers/
  fixtures/
    packets/
    configs/
    otml/
    resources/
  support/
    mocks/
    builders/
    test_environment/
```

Empty conceptual directories are documented but are not committed. A directory
is added only with a real test or fixture. This avoids a mechanical move of the
existing suite and keeps the diff reviewable.

Shared helpers must be small and used by at least one test in the same PR.
Message builders describe packet fields in code; output inspectors compare
wire bytes; synthetic thing builders avoid runtime assets; and a test
environment owns only the global lifecycle actually required by its target.

## Test levels

### Unit

Unit tests exercise one C++ class or one pure Lua module in-process. They must
not open sockets, initialize a window, use real time, or depend on execution
order. CTest label: `unit`; additional domain labels such as `protocol` are
allowed.

### Integration

Integration tests exercise two or more real components, for example protocol
framing over a loopback mock server or module loading in an isolated Lua
process. They use random loopback ports, bounded waits, explicit teardown, and
no external service. CTest label: `integration`.

### Contract

Contract tests compare public data shared across language or subsystem
boundaries: resource identifiers, selected protocol codes, and feature names.
They parse the authoritative representation instead of duplicating entire
files. Contract tests are normally fast and carry `unit` plus a domain label.

### End-to-end

OTClient-to-Canary tests are optional and separate. A future manual
`workflow_dispatch` job may start a pinned local Canary process/container and a
disposable database, use non-production credentials, cap total runtime, collect
both logs, and always terminate processes. It must never become an implicit
dependency of unit or integration tests.

## Regression-test policy

Each bug fix should add a test that fails for the original reason and passes
after the fix, when a deterministic test seam exists. The test name describes
the preserved rule, the fixture contains the smallest reproducer, and the PR
links the issue or failure report. Timing retries, external services, private
assets, order dependencies, ignored CTest failures, and unconditional CI
disables are prohibited.

When an existing defect is found during foundation work:

1. record the reproducer in `docs/regression-test-backlog.md`;
2. do not merge a failing test;
3. identify the smallest production fix or test seam separately;
4. implement it in a focused regression PR after architectural review.

The currently observed singular/plural `ResourceTypes` mismatch in Wheel Lua
code is handled this way rather than changing game behaviour in this PR.

## First-PR boundaries

This foundation does not attempt full coverage of Forge, Wheel of Destiny, Gem
Atelier, Prey, Market, login, rendering, sound, or Canary E2E. It also does not
introduce pixel-perfect UI tests, proprietary item/sprite data, a complete fake
client, a complete Lua global model, or a mandatory real server.

A headless startup executable is deferred. The minimum future production seam
is a bootstrap object with explicit `initCore`, `loadConfiguration`,
`registerModules`, and `terminate` phases, plus injected platform/render/audio
adapters. That is a production refactor and requires an architectural
checkpoint before implementation.

The first loopback protocol test is also limited to framing and one message.
Full login/crypto negotiation remains out of scope.

## Roadmap

1. Establish labels, deterministic message helpers, message serialization
   tests, resource contracts, fixtures, and the Lua runner.
2. Add small parser entry points or callback receivers for stable opcodes after
   reviewing their API impact.
3. Expand synthetic Tile/Item/ThingType coverage without runtime assets.
4. Add isolated configuration/OTML fixtures and module-load tests with minimal
   Lua stubs.
5. Introduce a bounded loopback protocol harness and one-packet integration
   smoke test.
6. Design the headless bootstrap seam and add a no-GPU startup test.
7. Add manual Canary E2E, optional coverage reporting, and scheduled/manual
   sanitizer execution as their stability is demonstrated.

## Local commands

```sh
cmake --preset linux-tests
cmake --build --preset linux-tests
ctest --preset linux-tests
ctest --test-dir build/linux-tests -L unit --output-on-failure
ctest --test-dir build/linux-tests -L lua --output-on-failure
ctest --test-dir build/linux-tests -L integration --output-on-failure
```

Tests that own global managers must be executed at least twice and in parallel
before release. CTest uses explicit timeouts and `noTestsAction: error`.

## Client-assets safety

The test foundation does not change client-assets installation or runtime
loading. If later tests cover that subsystem, final test assertions must retain
the OTC-standard `data/things/<version>/` and `data/sounds/<version>/` paths,
strict manifest SHA-256 verification, no raw mismatch fallback, and Android
builds without unsupported libarchive linkage.
