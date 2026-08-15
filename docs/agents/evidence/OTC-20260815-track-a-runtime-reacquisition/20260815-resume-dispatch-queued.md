# Track A RUNTIME — resumed reacquisition dispatch remains queued

Date: 2026-08-15  
Task: `OTC-20260815-track-a-runtime-reacquisition`  
Track: `official-client-re`

## Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

## Why a new dispatch became valid

The previous RUNTIME waiting checkpoint named P0 run `31880617510` as the serialized runtime-lane blocker and could not verify runner availability. That prerequisite changed materially:

- the P0 owner fenced and cancelled stale run `31880617510`;
- P0 run `31883178675` executed on `synology-otclient-01`, proving the selector can reach the dedicated runner;
- P0 run `31883422477` / job `95009054487` executed on that runner and proved `TRACK_A_P0_DISCOVERED_EXACT_TRACK_CLIENTS=0`;
- P0 therefore remains semantically `INCONCLUSIVE/UNKNOWN` and explicitly waits for RUNTIME ownership to create a fresh exact-client world session.

The cancelled RUNTIME run `31882125124` could not be retried through the available GitHub action (`403 This workflow run cannot be retried`).

## Auditable resume request

A durable request was persisted at:

`docs/agents/evidence/OTC-20260815-track-a-runtime-reacquisition/runtime-run-request.json`

It records the released P0 prerequisite, exact main/client fence, original code-bearing head, allowed login/restart effects and forbidden economic/irreversible/Track-B effects.

The workflow was changed only to make that request an explicit push trigger and to fail closed unless:

- repository/branch/runner identity match;
- request schema/task/track/reason/base/main/P0 evidence match;
- client SHA/size/version/platform match;
- helper Git blob remains exactly `c1b88d4cc17edf2684b93d7e516f9c694e37966a` from code-bearing head `4bd5cbc47fbfd816a6ab5dd66b57c88b3ff981f4`;
- helper shell syntax passes.

Dispatch head: `950ce8f5f7cf22b457e82cdb20e9eec285438d9c`.

## Current external operation

```yaml
workflow: .github/workflows/tibia-official-client-re-runtime-reacquisition.yml
run: 31883846172
job: 95010096196
job_name: reacquire
head: 950ce8f5f7cf22b457e82cdb20e9eec285438d9c
first_observation: queued
second_observation: queued
semantic_execution_started: false
```

No semantic login/restart result exists from this run yet. No generation-1/2 claim may be made from queue state.

## Classification

### FACT

- the old P0 queue blocker is terminally released;
- the matching runner has executed later P0 jobs;
- a fresh RUNTIME dispatch was created successfully under the intended concurrency group;
- the exact self-hosted `reacquire` job exists but remained queued across the two unchanged external-state observations allowed by the anti-stall contract.

### UNKNOWN

- current runner online/busy assignment state; repository runner inventory remains unavailable to the GitHub integration;
- protected login-secret availability/acceptance;
- generation-1 structural `IN_GAME`;
- generation-2 fresh PID/PIE and structural read reacquisition;
- live transport confinement and credential-environment results;
- final cleanup outcome.

## Stop boundary

Per `ANTI_STALL_AND_EXECUTION_BUDGET.md` and `EXECUTION_PROTOCOL.md`, no worker session should stay alive merely to poll an unchanged queued external operation. The task must be `waiting` until run `31883846172` materially changes state. On resumption, inspect exact jobs/logs/artifacts first; do not create another conceptual duplicate or weaken the gate.
