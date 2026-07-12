# OTClient Known Risks

- `opentibiabr/otclient` is read-only; verify repository before mutation.
- Module lifecycle leaks occur when events, keys, timers, widgets, or callbacks are not cleaned up.
- Load-order bugs occur when modules capture globals too early or omit dependencies.
- Protocol field order, widths, signedness, opcode reuse, and feature gates must match Canary.
- UI may work at one resolution while clipping or mis-scaling at another.
- Runtime Lua syntax CI intentionally scans `data`, `modules`, and `mods`; changing scope changes a required contract.
- Asset installation must retain strict hashes and standard final paths; Android cannot inherit unsupported desktop archive dependencies.
- Proprietary assets must not be committed without rights.
- PR #3 introduces reusable test harnesses/presets; parallel infrastructure would duplicate globals and fixtures.
- PR #4 overlaps governance docs; reconcile rather than preserve contradictions.
