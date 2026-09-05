# P0 direct-position live runtime prerequisite — 2026-08-15

## Scope

Task: `OTC-20260815-track-a-p0-direct-position`

Branch: `research/OTC-20260815-track-a-p0-direct-position`

Draft PR: #302

Exact client fence:

- version mapping: `15.32.df7b29`
- size: `51965216`
- SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- platform: official native Linux client only

This checkpoint records runtime-prerequisite evidence only. It does not promote a direct player-position value.

## FACT — stale queue recovery

The original code-bearing run `31880617510` / job `95002559098` remained queued with `runner_id=0`. Direct runner inventory was unavailable to the GitHub integration with HTTP 403, so that queue state alone was not classified as an offline runner.

Historical successful job `94785974126` had executed on `synology-otclient-01` with labels `otclient` and `synology`. The P0 workflow had required the additional `self-hosted` label. Commit `6e1af63176b3451da0e82fb2751e5c5f50658c49` aligned the P0 selector to `[otclient, synology]`.

Because the original queued P0 run continued to occupy the serialized runtime lane, commit `ab22e9c495daea050f45e90b3e38b78062539d59` added an exact-fenced GitHub-hosted preflight that could cancel only run `31880617510` when all of its immutable P0 identity fields still matched. The stale run subsequently reached terminal `cancelled` state.

No RUNTIME task run, Track B run, or unrelated workflow was cancelled by this recovery.

## FACT — self-hosted runner execution recovered

Run `31883178675` on head `ab22e9c495daea050f45e90b3e38b78062539d59` created self-hosted job `95008500800`. GitHub assigned:

- runner id: `21`
- runner: `synology-otclient-01`
- labels: `otclient`, `synology`

The job therefore disproved the earlier operational hypothesis that the P0 semantic probe was blocked solely because no matching runner could execute it.

The first actionable runtime failure was a stale shared PID file. `runtime/client.pid` contained PID `18102`, and `kill -0 18102` failed with `No such process` before the memory probe ran.

## FACT — stale PID recovery discriminator

Commit `29973501a14aefd14ef887161014190d270d5c0c` added a read-only fallback for a stale PID file. It scans `/proc/[0-9]*` and accepts a candidate only when both are true:

1. `/proc/<pid>/exe` resolves to the exact fenced client executable;
2. `/proc/<pid>/environ` contains the exact marker `OTCLIENT_TIBIA_RE_TRACK=official-client-re`.

It requires exactly one matching live process. It does not start, stop, signal, inject into, or write to any candidate process.

Run `31883422477` executed this discriminator on `synology-otclient-01` at exact head `29973501a14aefd14ef887161014190d270d5c0c`. Self-hosted job `95009054487` reported:

```text
TRACK_A_P0_PIDFILE_STALE=true
TRACK_A_P0_DISCOVERED_EXACT_TRACK_CLIENTS=0
TRACK_A_P0_ERROR=expected_one_live_exact_track_client
```

The job exited with code `3` by design. `luacheck` and `cppcheck` companion checks in that run completed successfully.

## Classification

### FACT

- The exact fenced Linux client binary is present on the permitted Synology runtime environment; the workflow reached the process-selection stage after the executable, size, and SHA-256 checks.
- `synology-otclient-01` is capable of executing the P0 workflow.
- The historical shared `runtime/client.pid` is stale.
- At the time of run `31883422477`, zero live processes simultaneously matched the exact fenced executable and Track A process marker.
- No P0 gameplay stimulus was used in this continuation: zero movement, zero process-memory writes, zero gameplay actions.

### UNKNOWN

- Whether `TPlayerData` or a justified one-hop owner contains an authoritative direct player XYZ member in a live in-game session.
- The direct member offset/access path, lifetime, semantic change behavior, and fresh-PID/relogin stability.
- Negative discrimination against camera/map-origin/viewport copies for any direct candidate, because no live typed owner object was available for observation.

### INCONCLUSIVE

The direct-player-position hypothesis remains **INCONCLUSIVE/UNKNOWN**, not disproven. Absence of a live exact Track A process prevents the required typed-object observation; it does not establish that the field does not exist.

The historical viewport-center transition remains a separate **DERIVED** structural oracle and must not be promoted as a direct player-position member.

## Required cross-lane dependency

The P0 prompt permits live stimulus to be coordinated with RUNTIME but does not give this task ownership of RUNTIME login/restart paths. Draft PR #303 owns the restart/relogin reacquisition workflow and task-local runtime. Its current workflow cleans its task-owned client at the end, so a later P0 workflow cannot inspect that process after completion.

A future coordinated execution must provide a bounded live observation window in which the P0 read-only probe runs while an exact RUNTIME-owned in-game client is alive, or an integration task with explicit non-overlapping ownership must invoke the P0 probe inside that controlled RUNTIME window. No such cross-lane mutation is authorized from this P0 branch.

## Read-gate disposition

`RETURN_FOR_EVIDENCE / WAITING_ON_RUNTIME_PREREQUISITE`

Missing evidence is precise: at least one live exact Track A in-game process, under RUNTIME ownership, must be observable long enough to obtain typed `TPlayerData` reads; any candidate then still requires repeat observation and structural/causal discrimination according to the task acceptance gate.
