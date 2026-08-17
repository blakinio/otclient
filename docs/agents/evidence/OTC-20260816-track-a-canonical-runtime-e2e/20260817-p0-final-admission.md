# P0 final canonical admission — post-#465 physical controller-plane evidence

## Trusted base

- repository: `blakinio/otclient`
- trusted `main` at admission creation: `f8e628a255a18ec92839bbb45ef0e3b40bef8605`
- canonical XRes integration: PR #465, merge `f8e628a255a18ec92839bbb45ef0e3b40bef8605`
- consumer: `OTC-20260815-track-a-p0-direct-position`, Draft PR #302
- physical XID→PID producer already trusted: PR #457, merge `16c6fb695a85a6ba3a809fcf5b031ce4ac7e11fc`

## Fresh admission

- admission PR: #467
- physical admission head: `2e35d0666b9fe73812abce4b4c09073e31c45e82`
- workflow run: `32019313320`
- job: `95355423148`
- runner: `synology-otclient-01`
- job conclusion: `SUCCESS`

The admission governance revalidation on the physical job reported:

```text
TRACK_A_AGENT_RUNTIME_CHANGED_TASKS=1
TRACK_A_AGENT_RUNTIME_BRANCH_BOUND_TASKS=1
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
P0_FINAL_CANONICAL_ADMISSION_POLICY=PASS
```

## Controller-plane observation

The one-shot probe acquired only a nonblocking shared flock on the existing canonical coordination lock and read whitelisted controller metadata. It did not inspect the client or process state.

Observed result:

```text
P0_FINAL_CANONICAL_LEASE="PRESENT"
P0_FINAL_CANONICAL_LEASE_SCHEMA_VERSION=1
P0_FINAL_CANONICAL_LEASE_RUNTIME_ID="track-a-canonical-live"
P0_FINAL_CANONICAL_LEASE_STATUS="released"
P0_FINAL_CANONICAL_LEASE_GENERATION=7
P0_FINAL_CANONICAL_LEASE_CONTROLLER_TASK=null
P0_FINAL_CANONICAL_LEASE_CONTROLLER_SESSION=null
P0_FINAL_CANONICAL_LEASE_EXPIRED=false
P0_FINAL_CANONICAL_REGISTRATION="ABSENT"
P0_FINAL_CANONICAL_ADMISSION_RESULT="REGISTRATION_ABSENT"
P0_FINAL_CANONICAL_CONTROL_METADATA_UNCHANGED=true
P0_FINAL_CANONICAL_PROCESS_OBSERVATION=false
P0_FINAL_CANONICAL_X11_OBSERVATION=false
P0_FINAL_CANONICAL_CLIENT_MUTATION=false
P0_FINAL_CANONICAL_ADMISSION_INVENTORY="COMPLETE"
```

The before/after fingerprints of the existing coordination lock, lease and registration paths were identical. The probe made no lease/registration write, rebind, bootstrap, client launch/stop/signal/attach, `/proc` observation, X11/VNC observation, credential use, login or gameplay action.

The one-shot workflow was deleted immediately after the successful inventory so it cannot be reused accidentally.

## Disposition for P0 #302

`BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE`

`semantic_player_xyz=INCONCLUSIVE`

The authoritative canonical registration is absent and the lease is released. Therefore no current canonical runtime identity or structurally verified `IN_GAME` lifecycle exists that P0 may legally reuse. Historical XID/PID/display/session observations, including PID `13648` from #457, are not current runtime authority.

A P0-only bootstrap/login is explicitly outside this admission and is not permitted to manufacture semantic evidence. Consequently no process-memory discriminator run was executed and no direct player XYZ claim was promoted.

## Exact missing prerequisite

A separately authorized legitimate canonical lifecycle, created for an independent programme purpose, must first exist and reach structurally verified `IN_GAME`. Only then may RUNTIME refresh from trusted `main`, perform a fresh admission and required ownership/generation gates, establish fresh exact-client identity, and run the bounded P0 discriminator.

Until that prerequisite exists, Draft PR #302 must remain unpromoted with semantic position evidence inconclusive.

## Closeout audit

- physical admission policy: PASS
- physical controller-plane inventory: PASS
- authoritative registration: ABSENT
- control metadata unchanged: PASS
- process observation: NONE
- X11 observation: NONE
- client mutation: NONE
- bootstrap/login: NONE
- open material audit findings: 0
- final classification: `BLOCKED_NO_LEGAL_EXISTING_IN_GAME_LIFECYCLE`
