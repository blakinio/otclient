# OTClient Build and Test Matrix

Always read current `CMakePresets.json`; active PR #3 may add/rename test presets. Validation must be proportional to changed paths, risk and the current milestone; a commit or small task step does not by itself justify compilation.

## Temporary platform policy

Windows is the only compiled and required client target for the current project phase.

- Primary CI may use Ubuntu runners for path detection, YAML/static checks, Lua syntax and the final required-job evaluator, but those jobs must not compile a Linux client.
- Required compilation and CTest coverage use `.github/workflows/reusable-build-windows.yml` only.
- Linux, macOS, Android, browser and Docker reusable workflows remain in the repository but are not called by the primary CI workflow.
- Do not claim compatibility with a dormant platform from Windows validation.
- Re-enabling another compiled target requires an explicit repository-owner decision and a focused CI policy change.

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
| C++ implementation | Focused Windows compile and affected CTest at coherent milestone completion | Full required Windows matrix on final head |
| CMake/dependency/toolchain/public header | Configure/build immediately enough to protect subsequent work | Clean Windows validation at milestone completion |
| Protocol | Parser/output tests and linked Canary version | Windows loopback or real integration |
| Test infrastructure | Existing support tests and affected labels | Full Windows test preset/CTest when infrastructure affects broad coverage |
| Asset installer | Hash/path/fallback/extraction tests | Clean Windows install/runtime load |
| Android/browser/non-Windows platform | Source review only while target is dormant | No compatibility claim; do not compile until policy changes |
| CI workflow | YAML and required-check/path-filter review | Observe emitted checks on PR; only Windows build may be selected |

## Known release command

```bat
cmake --preset windows-release
cmake --build --preset windows-release
```

Use current testing strategy and Windows presets after PR #3 state is resolved.
