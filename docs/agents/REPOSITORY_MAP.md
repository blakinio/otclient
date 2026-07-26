# OTClient Repository Map

Navigation map, not exhaustive inventory. Confirm live paths, manifests, tasks and PR ownership before editing.

| Area | Typical paths | Responsibility/cautions |
|---|---|---|
| Greenfield Oteryn client | `oteryn-client/**` | New Rust product, architecture, audits, future workspace/crates/features/tools. Read nested `AGENTS.md`; audit gate applies. |
| Greenfield architecture | `oteryn-client/docs/architecture/**` | Normative target design and ADRs. Do not create parallel architectures. |
| Greenfield agent program | `oteryn-client/docs/agents/**` | Audit, workstreams, prompts and implementation gates. |
| Legacy architecture/routing | `docs/architecture/LEGACY_OTCLIENT_ARCHITECTURE.md`, `docs/agents/LEGACY_OTCLIENT_WORKSTREAMS.md` | Maintained knowledge for existing C++/Lua tasks; not the target architecture. |
| Legacy framework/engine | `src/framework/**` | Existing C++ application, graphics, networking, Lua/OTML, resources and platform abstractions. Legacy/reference only for the Rust track. |
| Legacy game/protocol | `src/client/**` | Existing protocol, game state, map/things and services. Coordinate exact Canary facts. |
| Legacy shipped modules | `modules/**` | Existing Lua/OTUI functionality. Preserve lifecycle/dependencies for legacy tasks; do not port structurally into Rust. |
| Legacy optional mods | `mods/**` | Optional/custom legacy behavior; not a substitute for core fixes or a Rust extension model. |
| Legacy runtime assets | `data/**`, `bin/**` | Existing assets/runtime files. Observe licensing, provenance and strict path/hash gates. |
| Legacy tests | `tests/**` | Existing C++/Lua/OTML fixtures/support. Audit evidence only for Rust; do not link as Rust test infrastructure. |
| Legacy build | CMake files, `CMakePresets.json`, `cmake/**`, `vcpkg.json`, `vc18/**` | Existing client build policy. |
| CI | `.github/workflows/**` | Repository checks and future isolated Rust jobs. Dedicated CI ownership required. |
| Shared docs | `docs/**` | Repository-wide contracts, legacy behavior, routing and agent coordination. |
| Agent memory | `AGENTS.md`, `docs/agents/**`, `oteryn-client/AGENTS.md` | Root governance plus nearest-path rules. |

## Discovery commands

```sh
find . -name AGENTS.md -print
find docs/agents/tasks/active -maxdepth 1 -type f -print
find oteryn-client -maxdepth 4 -type f -print
rg -n "GameEvent|GameCommand|WorldChannelId|protocol-canary|protocol-oteryn" oteryn-client docs
rg -n "<module|controller|opcode|feature|message|widget>" src modules mods tests docs
rg -n "add_(executable|library)|target_sources|OTCLIENT_BUILD_TESTS" CMakeLists.txt src tests cmake
```

Before the Rust workspace exists, absence of planned crate directories is intentional and must not be treated as missing implementation to fill outside the audit/program sequence.
