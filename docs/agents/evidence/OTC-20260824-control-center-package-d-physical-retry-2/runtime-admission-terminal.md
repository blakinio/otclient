# Package D physical retry 2 — terminal runtime-admission evidence

```yaml
task: OTC-20260824-control-center-package-d-physical-retry-2
pull_request: 686
branch: runtime/OTC-20260824-control-center-package-d-physical-retry-2
trusted_main_at_admission: 2cc9adf1bd301e0a03808e2249aa6ee78862edce
physical_preflight_head: 83557cb92b89dcc505398602e6ddb6dea0eefa92
runtime_admission: BLOCKED
target_uniqueness: BLOCKED
gate_a: NOT_APPLICABLE
rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
action: NOT_ATTEMPTED
physical_action_count: 0
authoritative_confirmation: NOT_APPLICABLE
no_retry: true
blocker: BLOCKED_TRACK_A_RUNTIME_EXECUTOR_NOT_ACQUIRED
```

## Fresh admission boundary

The task started from `runtime_access: none`. No historical PID, process-start value, display, XID, registration, controller lease, workflow run, session, KasmVNC observation, or previous Package D evidence was accepted as current runtime authority.

The exact current client fence was bound from trusted `main` before any physical work:

```text
version=15.32
size=52109920
sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
platform=official_native_linux_only
```

Open-PR/ownership preflight found no overlap on this task's declared unique repository paths. PR #475's current-head task record had released current runtime authority and owned paths. PR #528 was already terminal closed/superseded. PR #541 remained a stale Draft whose branch record owns its Kasm desktop surface; this task therefore did not mutate that surface without fresh canonical admission.

## Fresh physical transport evidence

Fresh Remote Desktop Commander inventory reported both devices named `Synology` offline. `Molehill-PC` was online and was used only for non-invasive infrastructure diagnosis.

From that authorized PC path, the NAS hostname resolved and the host answered on SSH and SMB. The SSH endpoint returned an OpenSSH banner, and the existing Windows-authenticated SMB connection succeeded. This proves the NAS host itself was reachable; it does not prove Track A runtime authority.

The already-present local Synology SSH public key fingerprint was compared with the user's existing remote `authorized_keys` using public fingerprints only; a match was proven. Non-interactive SSH with the existing local private key still failed closed. No password, passphrase, private-key content, DSM credential, token, cookie, or other secret was read or printed. No `authorized_keys`, SSH, DSM, Docker, runner, or authentication configuration was modified.

## Canonical self-hosted executor attempt

A task-specific controller-plane-only workflow used the trusted current selector:

```text
runs-on: [otclient, synology]
```

Run `32698858788`, job `97346162472`, was inspected twice on exact head `83557cb92b89dcc505398602e6ddb6dea0eefa92`. The job remained `queued` and never started. Anti-stall policy forbids further unchanged polling on that exact head.

Because the job never acquired `synology-otclient-01`:

- the required isolated task worktree was not created on the physical executor;
- current canonical lease status was not read;
- current `runtime-registration.json` presence/contents were not read;
- no current registration or lease generation was established;
- no live Official Tibia process/window/display/container observation was performed;
- no Gate A, rebind, Gate B, input lock, guarded-dispatch READY or COMMIT was reached.

Therefore the runtime class could not lawfully advance beyond `none`. Required identity and uniqueness facts remain unknown, and `UNKNOWN => REFUSE` applies.

## Effect and privacy accounting

```yaml
effect_budget:
  max_actions: 1
  max_movement_tiles: 0
  max_spells: 0
  max_consumables: 0
  max_items_moved: 0
  max_gold: 0
  max_tibia_coins: 0
  max_irreversible_changes: 0
consumed:
  actions: 0
  movement_tiles: 0
  spells: 0
  consumables: 0
  items_moved: 0
  gold: 0
  tibia_coins: 0
  irreversible_changes: 0
ready_emitted: false
commit_emitted: false
possibly_dispatched: false
official_client_access: NONE
credentials_accessed: false
login_attempted: false
privacy_scan: PASS
```

No action request hash or adapter execution generation is synthesized because no action reached dispatch. STOP/control generations were not mutated. There is no post-COMMIT uncertainty: dispatch never began.

## Terminal disposition

This retry is terminal `BLOCKED_WITH_REASON` with `PHYSICAL_ACTION_COUNT=0` and blocker `BLOCKED_TRACK_A_RUNTIME_EXECUTOR_NOT_ACQUIRED`. It must not be resumed or retried under this task identity. Any future physical attempt requires a new task and a completely fresh admission from then-current `main` and runtime state.

The task-specific workflow and active task record are removed from the final PR diff during closeout. Final exact-head hosted CI/governance and PR review hygiene are required after that seal; those checks do not retroactively provide physical runtime admission.