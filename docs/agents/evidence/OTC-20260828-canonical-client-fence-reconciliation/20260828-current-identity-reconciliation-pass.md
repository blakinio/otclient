# Exact-current canonical runtime-identity reconciliation — PASS

Date: 2026-08-28

## Identity

- fresh owner trigger comment: `5457186114` on merged PR #760
- workflow run: `33206484746`
- job: `98968734937`
- runner: `synology-otclient-01`
- exact trusted main: `7edf5bc44c08b762be7ac34104e840b391747fd6`
- decision: `RECONCILE_CURRENT_IDENTITY`

## Guarded proof

The trusted-main workflow passed repository admission and deterministic pre-runtime verification, then acquired canonical lease generation `42`. The source exact-current registration was bound to lease generation `41`, satisfying the strictly-newer controller-generation requirement.

Three guarded existing-runtime probes independently returned `TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS`. Their stable exact-current singleton identity was committed through the canonical guard and the helper reported `target_uniqueness=PROVEN`, `mutation_authorized=false`, `state=UNKNOWN` and reconciliation PASS.

Terminal markers:

```text
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PENDING_ADMISSION=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_PRERUNTIME=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_DECISION=RECONCILE_CURRENT_IDENTITY
TRACK_A_CANONICAL_LEASE_GENERATION=42
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_GATE_A=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_CANONICAL_LEASE_GENERATION=42
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_REGISTRATION_LEASE_GENERATION=41
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

## Final fence and safety boundary

Final memory-free verification required the canonical registration to remain owner-owned, mode `0600`, exact-fenced to:

```yaml
client_version: 15.32.75d4a0
client_size: 52105824
client_sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
state: UNKNOWN
```

No client process mutation, process-memory observation, GUI/input, login, credential access, character selection, gameplay, packet/payload capture or semantic promotion occurred. The canonical lease was explicitly released after the guarded transaction.

## Downstream

The old gameWindowState preflight blocker `REGISTERED_TARGET_NOT_CURRENT_UNIQUE_CANDIDATE` has been repaired at the canonical metadata layer. This PASS itself does not grant gameWindowState process-memory access. After repository recovery authority is closed, a new memory-free `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION` must re-prove current registration/identity/uniqueness and create its own bounded read-only admission before any observation.
