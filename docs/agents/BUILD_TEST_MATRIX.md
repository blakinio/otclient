# OTClient Build and Test Matrix

Always read current `CMakePresets.json`; active PR #3 may add/rename test presets. Validation must be proportional to changed paths, risk and the current milestone; a commit or small task step does not by itself justify compilation.

## Validation timing and escalation

- During a multi-step task, run cheap focused checks after each step: syntax, formatting, load/parse checks, generated-file consistency and directly affected tests.
- Defer compilation and other heavy validation until the end of a coherent milestone, phase or implementation package. A five-step client feature should normally compile once after the five steps form one reviewable result, not after every step.
- Compile earlier only when a step changes CMake/build manifests, source registration, dependencies, toolchains, generated compile inputs, public headers/ABI, platform abstractions, or when later work requires a verified binary.
- Documentation, task-checkpoint, comment, metadata, Lua-only, OTUI-only and other clearly non-build-affecting commits do not require a C++ build; use their focused validators instead.
- Run the full applicable final validation once on the exact final head before merge. A later build-affecting commit invalidates it; a later docs-only commit needs only the checks selected by repository policy.
- Record why a heavy build was run early or skipped when the choice is not obvious from changed paths.

| Change | Minimum local validation | Additional validation |
|---|---|---|
| Documentation/task records | Markdown/path review, `git diff --check` | Fast/docs checks; no compilation |
| Lua module/mod | Runtime-root syntax/static checks and focused module test | Client runtime load/interaction; no C++ build unless compiled integration changed |
| OTUI/style | Load/parse and interaction at relevant resolutions | Scaling evidence when useful; no C++ build unless compiled integration changed |
| C++ implementation | Focused compile and CTest at coherent milestone completion | Required Linux plus affected Windows/macOS |
| CMake/dependency/toolchain/public header | Configure/build immediately enough to protect subsequent work | Clean or full affected-platform validation at milestone completion |
| Protocol | Parser/output tests and linked Canary version | Loopback or real integration |
| Test infrastructure | Existing support tests and affected labels | Full test preset/CTest when infrastructure affects broad coverage |
| Asset installer | Hash/path/fallback/extraction tests | Clean install/runtime load on affected platforms |
| Android/browser/platform | Platform-specific build | Do not infer from desktop validation |
| CI workflow | YAML and required-check/path-filter review | Observe emitted checks on PR; build only when selected by the workflow |

## Known release command

```bat
cmake --preset windows-release
cmake --build --preset windows-release
```

Use current testing strategy/presets after PR #3 state is resolved.