# OTClient Build and Test Matrix

Validation is proportional to changed paths, risk and current milestone. Exact live workflow/preset state is authoritative.

## 1. Greenfield Rust client policy

The Rust client lives under `oteryn-client/` and is currently in architecture/audit phase.

### Before workspace bootstrap

| Change | Minimum validation | Additional evidence |
|---|---|---|
| Architecture/ADR | Markdown, link/path and complete diff review | repository fast/docs checks |
| Audit documents | evidence labels, citations/paths, consistency and provenance review | exact external/runtime blockers documented |
| Synthetic fixture inventory | schema/provenance/secret/license review | parser not claimed until implemented |

No Rust build is required before `Cargo.toml` exists. Do not create placeholder code merely to produce a build check.

### After audit-approved bootstrap

Planned required stages are defined by `oteryn-client/docs/architecture/PERFORMANCE_AND_TESTING.md` and include:

- format/workspace metadata;
- architecture dependency checks;
- clippy/workspace lints;
- unit/property tests;
- protocol golden/malformed/fuzz-smoke tests;
- dependency advisory/license checks;
- Windows build and headless integration tests;
- renderer/UI GPU checks when runner support exists;
- packaging/update clean-install tests at release milestones.

Windows is the first required compiled target. Portability design does not justify Linux/macOS compatibility claims.

## 2. Legacy C++/Lua client policy

Always inspect current `CMakePresets.json`; live PRs may change test presets. Existing policy remains Windows-only for required compilation.

- Primary CI may use Ubuntu for path detection, YAML/static checks, Lua syntax and required-job evaluation, but not to claim Linux client compatibility.
- Required compilation and CTest coverage use the current Windows workflow/presets.
- Linux, macOS, Android, browser and Docker workflows are dormant unless explicitly re-enabled.

Known release command:

```bat
cmake --preset windows-release
cmake --build --preset windows-release
```

| Legacy change | Minimum local validation | Additional validation |
|---|---|---|
| Documentation/task records | Markdown/path/full-diff review | fast/docs checks; no compilation |
| Lua module/mod | runtime-root syntax/static checks and focused tests | runtime interaction; C++ build only if compiled integration changed |
| OTUI/style | load/parse and interaction | relevant resolution/DPI evidence |
| C++ implementation | focused Windows compile and affected CTest | full required Windows matrix on final head |
| CMake/dependency/public header | configure/build early enough to protect later work | clean Windows final validation |
| Protocol | parser/output tests and exact Canary pair | Windows loopback or real integration |
| Test infrastructure | existing support tests and labels | full affected Windows preset/CTest |
| Asset installer | hash/path/fallback/extraction tests | clean Windows install/runtime load |
| CI workflow | YAML/required-check/path-filter review | observe emitted checks on PR |

## 3. Cross-track changes

A PR should not normally change both legacy runtime code and Rust-client implementation. Shared documentation/contract changes must clearly identify which behavior is proven for which track.

- Legacy build success does not validate the Rust architecture.
- Future Rust tests do not validate legacy C++ behavior.
- Protocol and Identity claims require exact producer/consumer evidence for the affected client implementation.
- Documentation-only changes require no speculative build.

## 4. Validation timing

- Run cheap focused checks after coherent edits.
- Run heavy compilation at the end of a coherent implementation package, or earlier when build manifests/toolchains/public interfaces change.
- A later build-affecting commit invalidates prior build evidence.
- Never mark a check passed without exact evidence.
