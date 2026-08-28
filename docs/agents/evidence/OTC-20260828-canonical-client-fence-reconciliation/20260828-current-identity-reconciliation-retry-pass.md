# Exact-current canonical runtime-identity reconciliation retry — PASS

Date: 2026-08-28

## Trigger and trusted head

- fresh owner trigger comment: `5457630365` on merged PR #760
- workflow run: `33210019599`
- job: `98980682859`
- runner: `synology-otclient-01`
- exact trusted main: `fd7a47308581dceda6fd6aa3613f0614a816d150`
- decision: `RECONCILE_CURRENT_IDENTITY`

## Guarded result

The transaction acquired canonical lease generation `43`; the source exact-current registration was lease generation `42`, proving the required strictly newer controller generation (`43 > 42`). Three guarded existing-runtime probes independently returned `TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS`, target uniqueness was `PROVEN`, the guard command returned `0`, and the lease was explicitly released.

```text
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PENDING_ADMISSION=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PRERUNTIME=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_DECISION=RECONCILE_CURRENT_IDENTITY
TRACK_A_CANONICAL_LEASE_GENERATION=43
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_GATE_A=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CANONICAL_LEASE_GENERATION=43
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_LEASE_GENERATION=42
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_TARGET_UNIQUENESS=PROVEN
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_MUTATION_AUTHORIZED=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_STATE=UNKNOWN
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CLIENT_PROCESS_MUTATION=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PROCESS_MEMORY_OBSERVATION=false
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_SEMANTIC_PROMOTION=false
TRACK_A_CANONICAL_LEASE_GUARD_COMMAND_RC=0
TRACK_A_CANONICAL_LEASE_RELEASE=true
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_RELEASE=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_CURRENT=PASS
```

## Final safety state

Final memory-free verification retained the exact official-client fence:

```yaml
client_version: 15.32.75d4a0
client_size: 52105824
client_sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
state: UNKNOWN
```

No client process mutation, process-memory observation, GUI/input, login, credential access, character selection, gameplay, packet/payload capture or semantic promotion occurred. The temporary canonical recovery lease was released before the job ended.

## Downstream

After repository authority is returned to `runtime_access: none`, immediately run a new memory-free `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`. No owner UI is authorized unless that preflight explicitly returns `GAME_WINDOW_STATE_LOGGER_PREFLIGHT=READY`.
