# Track A P0 direct player-position passive probe checkpoint

## Scope

Task: `OTC-20260815-track-a-p0-direct-position`

Draft PR: #302

Base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`

The task is draft-only P0 research. Canonical promotion remains with coordinator PR #300.

## Exact client fence

- version mapping: `15.32.df7b29`
- size: `51965216`
- SHA-256: `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`
- platform: official native Linux client only

## Starting evidence

### FACT

- The exact-build runtime bridge/profile accepted as reference-only in PR #283 identifies `tibia::game::TPlayerData` with primary vptr offset `0x308ca70`.
- The accepted structural movement evidence retained by coordinator PR #300 supports the viewport-geometry-derived sequence `(32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)`.
- That coordinate remains `DERIVED`; it is not evidence of a standalone authoritative player-position member.
- Historical `cecf40` position-probe output did not establish `ref + 0x18` or another scanned triple as authoritative XYZ.

### UNKNOWN

- A direct standalone authoritative player-position member/reference in `TPlayerData` or a justified owner graph has not been proven.

## Passive reproducer

Code-bearing head: `7493983ca230c789f2d423cb073e036f4e29570e`

Files:

- `.github/scripts/tibia-official-client-re-p0-direct-position.py`
- `.github/workflows/tibia-official-client-re-p0-direct-position.yml`

The workflow is fail-closed on:

- repository/branch identity;
- `synology-otclient-01` runner identity once a runner is assigned;
- exact client size and SHA-256;
- live PID existence;
- `OTCLIENT_TIBIA_RE_TRACK=official-client-re` environment marker;
- `/proc/PID/exe` resolving to the exact fenced client.

The Python probe:

1. derives the live `TPlayerData` vptr as PIE main base plus `0x308ca70`;
2. scans readable+writable regions for that exact typed vptr using the same structural candidate model as the accepted PR #283 bridge;
3. inspects only the typed object and one justified pointer hop for plausible compact/32-bit XYZ-shaped fields;
4. reports recent structural map-strip geometry separately as a semantic oracle;
5. performs process reads only.

## Negative controls and side effects

### FACT

- There is no global process scan for known player XYZ triples.
- QMeta/generated message names are not treated as proof of persistent state.
- Structural viewport geometry is reported as an independent oracle, not promoted as direct state.
- The passive attempt issues no gameplay input and performs no process-memory writes.

### SIDE EFFECTS

None from the P0 probe itself. No movement, attack, use, trade, object movement, market, forge or currency action was issued.

## Execution state

### FACT

GitHub Actions run `31880617510` was created from code-bearing head `7493983ca230c789f2d423cb073e036f4e29570e`.

The required self-hosted job is:

- job: `95002559098`
- name: `passive-probe`
- labels: `[self-hosted, otclient, synology]`
- status at checkpoint: `queued`
- `runner_id`: `0`
- runner name: empty

The check suite also reports completed `luacheck` and `cppcheck` checks with `success`.

A separate stale self-hosted workflow job, `94887915796`, has also remained queued with `runner_id=0` using the older label set `[self-hosted, linux, x64, synology-otclient]`. This is evidence that the queue symptom is not unique to the new P0 label set, but it does not by itself prove why no runner is being assigned.

The last independently inspected successful runtime job used `synology-otclient-01` as runner id `21`: run `31806312967`, job `94785974126`, completed successfully on 2026-08-14.

Direct repository-runner inventory could not be inspected through the available GitHub connector because the Actions runners endpoint returned HTTP 403. Therefore current runner online/offline state is `UNKNOWN`.

## Result classification

### FACT

The passive runtime experiment has **not executed**. No live `TPlayerData` object address, candidate field, semantic correlation or no-hit result exists from this task yet.

### UNKNOWN

Direct authoritative player XYZ remains `UNKNOWN`.

No candidate can be promoted to `PROVEN` or `DERIVED` from this attempt because the runtime job has not run.

Repeatability is untested. Fresh-PID/relogin stability is untested. No causal movement test was attempted.

## Validation

- Draft PR #302 remained limited to owned P0 paths at the checkpoint.
- Standard exact-head PR CI for documentation checkpoint head `180e4a12e7016a6bea0dc8bbfe34b59aa8204dd9` completed with `success` in run `31880797651`.
- Runtime semantic validation is blocked on execution of job `95002559098`.

## Next action

Do not create a duplicate runtime experiment and do not infer a result from the queue state.

When a matching self-hosted runner is available, allow run `31880617510` / job `95002559098` to execute and inspect its exact logs. If typed `TPlayerData` resolution succeeds but passive observations do not discriminate a position field, only then consider one bounded reversible adjacent move plus inverse, after rechecking RUNTIME-lane ownership and using the shared runtime concurrency fence.
