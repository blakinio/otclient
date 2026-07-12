# OTClient Build and Test Matrix

Always read current `CMakePresets.json`; active PR #3 may add/rename test presets.

| Change | Minimum local validation | Additional validation |
|---|---|---|
| Documentation | Markdown/path review, `git diff --check` | Fast/docs checks |
| Lua module/mod | Runtime-root syntax/static checks and focused module test | Client runtime load/interaction |
| OTUI/style | Load/parse and interaction at relevant resolutions | Scaling evidence when useful |
| C++ | Appropriate preset build and focused CTest | Required Linux plus affected Windows/macOS |
| Protocol | Parser/output tests and linked Canary version | Loopback or real integration |
| Test infrastructure | Existing support tests and affected labels | Full test preset/CTest |
| Asset installer | Hash/path/fallback/extraction tests | Clean install/runtime load on affected platforms |
| Android/browser/platform | Platform-specific build | Do not infer from desktop validation |
| CI workflow | YAML and required-check/path-filter review | Observe emitted checks on PR |

## Known release command

```bat
cmake --preset windows-release
cmake --build --preset windows-release
```

Use current testing strategy/presets after PR #3 state is resolved.
