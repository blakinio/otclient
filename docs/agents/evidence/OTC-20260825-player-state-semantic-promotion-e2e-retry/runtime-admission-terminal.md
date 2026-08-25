# Player-state semantic promotion E2E retry — terminal admission evidence

## Verdict

- terminal result: `BLOCKED_WITH_REASON`
- blocker: `RECOVERY_CONTRACT_NOT_PROVEN:recovery_boot_identity_changed`
- stale-registration recovery: **NOT_APPLIED**
- Gate B: `NOT_REACHED`
- target uniqueness after canonical mutation admission: `NOT_REACHED`
- semantic preconditions: `NOT_REACHED`
- `READY=false`
- `COMMIT=false`
- `POSSIBLY_DISPATCHED=false`
- `PHYSICAL_ACTION_COUNT=0`
- semantic promotion: **NOT_PERFORMED**
- retry after this terminal blocker: **FORBIDDEN for this task**

The owner authorized one one-tile movement only if the full admission chain passed. It did not. No movement or other gameplay/client mutation was dispatched.

## Source of truth

The run was fenced to current `main` `f4b92d88e9623d8c10b349803fbd7d797bd588d7`, the squash merge of PR #693. PR #692 was already terminally merged and its durable result established the stale authoritative adoption registration. PR #693 was terminally merged with the distinct canonical stale-registration recovery lifecycle.

Runtime candidate head: `3c7a2c10862d79090eaa08b8efbf9d5aa6a3be83`.

Physical admission workflow: GitHub Actions run `32814985641`, job `97701351494`, runner `synology-otclient-01`. The job conclusion is `success` because the fail-closed controller completed correctly; the E2E semantic result is `BLOCKED_WITH_REASON`, not semantic success.

## Pre-runtime verification

Before any runtime access the Synology/Linux job passed:

- Track A agent runtime governance: `PASS`;
- canonical live transition suite: `37/37 PASS`;
- Kasm existing-runtime probe suite: `10/10 PASS`;
- task-specific one-shot causal worker suite: `11/11 PASS`;
- typed player-state reader suite: `7/7 PASS`;
- trusted-main check: `PASS`;
- `git diff --check`: `PASS`.

The one-shot causal worker and physical workflow were task instrumentation only. They are removed from the final merge candidate because no semantic promotion occurred.

## Fresh Track A admission

The fresh controller-plane prestate was:

```text
canonical_registration=PRESENT
lease_generation=26
registration_generation=2
registration_lease_generation=19
registration_pid=19590
registration_process_start_ticks=76611792
registration_proof_kind=existing_runtime_adoption_v1
registration_state=UNKNOWN
registration_state_evidence=BRIDGE_3_OF_3_SEMANTICS_UNPROVEN
runtime_access=none
mutation_authorized=false
```

Canonical lease acquisition and validation succeeded without stale takeover:

```text
TRACK_A_CANONICAL_LEASE_ACQUIRE=true
TRACK_A_CANONICAL_LEASE_GENERATION=27
TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER=false
TRACK_A_CANONICAL_LEASE_IDEMPOTENT=false
TRACK_A_CANONICAL_LEASE_VALIDATE=true
PLAYER_STATE_E2E_GATE_A=PASS
```

A fresh read-only Kasm existing-runtime probe returned:

```text
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS
```

## Recovery contract decision

The fresh evidence did **not** satisfy the reviewed PR #693 stale-registration recovery contract. The exact decision was:

```text
PLAYER_STATE_E2E_AUTHORITY_TRANSITION_DECISION=BLOCK:RECOVERY_CONTRACT_NOT_PROVEN:recovery_boot_identity_changed
```

The recovery validator requires boot identity continuity while allowing only the stale runtime PID/start pair to be replaced. Current evidence proves that continuity anchor changed. Therefore invoking `stale-registration-recovery` would have violated the reviewed contract and was correctly refused before any registration mutation.

Consequences:

```text
PLAYER_STATE_E2E_RESULT=BLOCKED_WITH_REASON:BLOCK:RECOVERY_CONTRACT_NOT_PROVEN:recovery_boot_identity_changed
PLAYER_STATE_E2E_READY=false
PLAYER_STATE_E2E_COMMIT=false
PLAYER_STATE_E2E_POSSIBLY_DISPATCHED=false
PLAYER_STATE_E2E_PHYSICAL_ACTION_COUNT=0
PLAYER_STATE_E2E_SEMANTIC_PROMOTION=false
```

No canonical recovery was applied. No ordinary rebind was attempted as a substitute. Gate B, post-admission target uniqueness and semantic preconditions were not reached. The one-shot movement request was never created or committed to the guarded-dispatch boundary.

## Forbidden paths remained unused

The task performed no login, credential access, relog, restart, character selection, process-control shortcut, memory write, injection, transaction, gameplay action or movement. The runtime was observed only through the reviewed read-only probe before the recovery-contract refusal.

The post-run lease release succeeded:

```text
TRACK_A_CANONICAL_LEASE_RELEASE=true
TRACK_A_CANONICAL_LEASE_GENERATION=27
PLAYER_STATE_E2E_RELEASE=PASS
```

Authority returned to `runtime_access:none` with no task controller retained.

## Closeout implication

This task cannot legally manufacture boot-identity continuity or reinterpret the reviewed recovery contract. A future runtime attempt would require a separately reviewed lifecycle that can establish a fresh canonical registration across a proven boot-epoch discontinuity, plus fresh owner authorization. This task must not retry the movement and must not carry its movement authorization forward.

## Closeout restack

The evidence-only closeout was later restacked onto current main 5b098eb6034ed42cf25283a0911b73078009db9 after PR #695. This does not alter or rerun runtime evidence.
