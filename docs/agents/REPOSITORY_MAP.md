# OTClient Repository Map

Navigation map, not exhaustive inventory. Confirm manifests/paths before editing.

| Area | Typical paths | Responsibility/cautions |
|---|---|---|
| Framework/engine | `src/framework/**` | Application, graphics, networking, Lua/OTML, resources, platform abstractions. |
| Game client/protocol | `src/client/**` | Protocol, messages, game state, map/things, services. Coordinate with Canary. |
| Shipped modules | `modules/**` | Core feature modules, Lua, OTUI/OTML/styles, manifests. Preserve lifecycle/dependencies. |
| Optional mods | `mods/**` | Optional/custom behavior; not a substitute for core fixes. |
| Runtime data/assets | `data/**`, `bin/**` | Things, sounds, UI assets, setup/runtime files. Observe licensing/path gates. |
| Tests | `tests/**` | C++ unit/integration/OTML, Lua runner/contracts, fixtures/support. Inspect PR #3 while active. |
| Build | CMake files, `CMakePresets.json`, `cmake/**`, `vcpkg.json` | Use presets/platform configuration. |
| CI | `.github/workflows/**` | Fast checks, Lua syntax, builds, test/analysis. Runtime Lua roots are `data`, `modules`, `mods`. |
| Docs | `docs/**` | Asset, testing, platform, behavior, architecture docs. |
| Agent memory | `AGENTS.md`, `docs/agents/**` | Coordination, catalogue, tasks, ADRs, changelog. |

## Discovery commands

```sh
find . -name AGENTS.md -print
find modules mods -name '*.otmod' -o -name '*.lua' -o -name '*.otui' -o -name '*.otml'
rg -n "<module|controller|opcode|feature|message|widget>" src modules mods tests docs
rg -n "add_(executable|library)|target_sources|OTCLIENT_BUILD_TESTS" CMakeLists.txt src tests cmake
find docs/agents/tasks/active -maxdepth 1 -type f -print
```
