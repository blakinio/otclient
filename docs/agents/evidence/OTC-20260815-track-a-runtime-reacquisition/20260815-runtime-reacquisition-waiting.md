# Track A runtime reacquisition — runner/concurrency waiting checkpoint

Task: `OTC-20260815-track-a-runtime-reacquisition`  
Draft PR: `#303`  
Base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`  
Code-bearing runtime head: `9d5734ced2155cf01ab6cbdfabfb2eb2707b7152`  
Checkpoint: `2026-08-15T13:12:53+02:00`  
Classification: `WAITING / NO_RUNTIME_SEMANTIC_RESULT`

## Exact client fence

The experiment is fenced to:

```text
version mapping: 15.32.df7b29
size: 51965216
SHA-256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official native Linux client only
runner: synology-otclient-01
```

The helper will recheck size/SHA on the runner before every build-specific observation. That runtime recheck has **not** executed in this task yet.

## Implemented bounded experiment

The Draft now contains only task-owned runtime tooling:

- `.github/workflows/tibia-official-client-re-runtime-reacquisition.yml`
- `.github/scripts/tibia-official-client-re-runtime-reacquisition.sh`

The experiment is designed to:

1. use task state under `/home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition`;
2. use display `:115` and task-local SOCKS relay port `25415` while treating shared Track A SOCKS `25354` as read-only dependency;
3. refuse a pre-existing display/port collision rather than delete or replace it;
4. launch persistent X/client/GDB/relay processes with `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` removed from their environments;
5. expose credentials only to the minimal login workflow step;
6. arm the exact-build structural Worldmap observer at static offset `0x19a8ea3` **before** login;
7. require a logged-out five-second `NO_STIMULUS` baseline with zero valid Worldmap records;
8. require at least eight validated structural `(x,y,z,order)` records after world activation with no direct client TCP and no client UDP;
9. cleanly stop generation 1, then start generation 2 and require a different PID and PIE base before accepting restart/relogin reacquisition;
10. perform zero gameplay movement/action unless a later explicit discriminator makes one bounded reversible action necessary.

No canonical capability status is modified by this Draft tooling.

## Static/exact-head validation

Standard PR CI for the code-bearing head `9d5734ced2155cf01ab6cbdfabfb2eb2707b7152` completed successfully in run `31881289268`.

Two earlier workflow generations were superseded before runtime execution became available:

- run `31880945751` — cancelled;
- run `31881193523` — cancelled.

Their GitHub jobs inventory exposed no task self-hosted runtime job, so they provide no client/session evidence.

Current runtime workflow run:

```text
run: 31881287155
head: 9d5734ced2155cf01ab6cbdfabfb2eb2707b7152
status at checkpoint: in_progress
self-hosted reacquire job: not yet materialized/assigned in GitHub jobs inventory
additional check-runs only: luacheck 95004188562, cppcheck 95004249306
```

Those additional checks are not runtime evidence.

## Blocking live state

A separately owned P0 task is ahead of this task in the same serialized Track A runtime lane:

```text
P0 task: OTC-20260815-track-a-p0-direct-position
P0 run: 31880617510
P0 job: 95002559098
job name: passive-probe
labels: self-hosted, otclient, synology
status: queued
runner_id: 0
concurrency group in both workflows: official-client-re-runtime
```

The P0 task record independently classifies itself `waiting` on this queued self-hosted job. Direct repository runner inventory cannot be queried through the current GitHub integration: `GET /repos/blakinio/otclient/actions/runners` returned HTTP `403 Resource not accessible by integration`.

The RUNTIME worker will not cancel, bypass or mutate the P0 task/run because it is separately owned.

## Claim matrix

| Claim | Result | Evidence boundary |
|---|---|---|
| current task exact-build runtime recheck | `NOT_EXECUTED` | helper is implemented; self-hosted job not assigned |
| logged-out negative control | `NOT_EXECUTED` | requires generation 1 runtime |
| generation 1 structural `IN_GAME` | `INCONCLUSIVE` | no runtime job/result |
| generation 2 fresh PID/PIE | `INCONCLUSIVE` | no restart/relogin execution |
| structural read-path reacquisition after restart/relogin | `INCONCLUSIVE` | no generation 2 evidence |
| persistent child credential-environment clearing | `IMPLEMENTED_NOT_RUNTIME_VALIDATED` | explicit `env -u` + runtime assertions exist in helper |
| task-owned namespace cleanup | `IMPLEMENTED_NOT_RUNTIME_VALIDATED` | ownership fences/refusal rules exist; runtime cleanup not executed |
| direct standalone P0 player XYZ | `NOT_CLAIMED` | separately owned by PR #302 |
| bridge `session_epoch` / R4 | `NOT_PROVEN` | this Draft does not claim bridge epoch semantics |
| action gate A3 | `NOT_PROVEN` | no programmatic/semantic action proof in this task |
| action gate A4 | `NOT_PROVEN` | no restart-stable action proof in this task |

Historical reversible GUI movement remains historical starting evidence only and is not promoted by this task.

## Side-effect and privacy report

- gameplay actions performed by this task at this checkpoint: `0`;
- gold / Tibia Coins / item / market / trade / forge effects: `0 observed`;
- no account identifiers, credentials, authenticated screenshots, OCR output or private chat were persisted;
- the protected login step has not executed in the current task run, so no runtime credential claim is inferred from static CI.

## Resume condition

Resume when the serialized self-hosted Track A runtime lane can assign the RUNTIME `reacquire` job on `synology-otclient-01` without displacing separately owned P0 work. Re-fetch `main`, PR/task overlaps and exact Draft head before execution. Then inspect the exact runtime job/artifact rather than treating workflow status or green static CI as semantic proof.
