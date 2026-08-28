# Track A Canonical Client-Fence Reconciliation v1

```yaml
contract: TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1
status: proposed_until_merged
runtime_id: track-a-canonical-live
state_root: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime
registration: /home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json
runtime_access_class: canonical_recovery
mutation_authorized: false
```

## Purpose

This contract defines one narrow canonical-registration recovery subtype for either a governance-driven exact-client fence advance from the immediately superseded approved build or a same-fence runtime-identity refresh when the durable canonical registration is already exact-current but its container/PID/start identity is stale.

It exists to close the fail-closed gap exposed by the gameWindowState memory-free preflight: ordinary rebind cannot repair a changed client fence, same-boot stale-registration recovery and boot-epoch recovery intentionally require the previously accepted exact fence, adoption requires registration absence, and bootstrap must not run while a canonical registration exists.

This contract does **not** weaken those transitions. `rebind`, `stale-registration-recovery`, `boot-epoch-registration-recovery`, adoption and bootstrap retain their existing contracts unchanged. Client-fence reconciliation is a separately reviewed metadata-only recovery subtype executed through the existing cancellation-safe canonical `guard-run` authority boundary.

## Closed source and target fences

v1 accepts exactly two closed source modes: the approved predecessor-to-current fence transition and an exact-current-to-exact-current runtime-identity refresh. No other source fence is admitted.

Approved superseded source registration:

```yaml
client_version: 15.32
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

Approved exact-current source for identity refresh, and required current target:

```yaml
client_version: 15.32.75d4a0
client_size: 52105824
client_sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
runtime_platform: official_native_linux_only
```

No family match, prefix match, arbitrary predecessor, mixed old/new tuple, alternative SHA/size, or future build is accepted. Any future fence migration requires a new reviewed trusted-base contract/change rather than widening v1.

## Admission and authority

The repository implementation PR is `runtime_access: none` and cannot execute its own unmerged recovery implementation.

A later trusted-main live invocation may temporarily classify the transaction as the existing `canonical_recovery` metadata-reconciliation access class with this contract as `recovery_mode: client_fence_reconciliation_v1`. The transaction itself keeps `mutation_authorized: false` because it changes canonical metadata only, never client state.

Before the registration can be replaced:

1. the task/session must acquire a current authoritative canonical lease;
2. the reconciliation worker must execute only as the finite child of `.github/scripts/tibia-official-client-re-canonical-live-lease guard-run`, so the final reviewed cancellation-safe supervisor continuously owns `coordination.lock` for the whole transaction;
3. the worker must prove the active lease record still names the same task/session and a generation newer than the old registration lease generation;
4. the authoritative registration file must be a current-UID-owned regular mode-0600 file at the canonical path;
5. the source record must be schema v1, `runtime_id: track-a-canonical-live`, `proof_kind: existing_runtime_adoption_v1`, `state: UNKNOWN`, and carry only fail-closed adoption state evidence;
6. the source record must contain either the exact approved superseded fence or the exact approved current fence above, complete all-running-Docker inventory evidence, exactly one candidate, a self-consistent candidate fingerprint and an X11 window identity bound to its recorded PID.

An exact-current source may be rewritten only by this same guarded transaction to refresh runtime identity from repeated fresh exact-current singleton proof under a strictly newer canonical controller generation. The refresh does not change the client fence or semantic state. An unapproved/mixed/corrupt source fence fails closed and requires separate investigation.

## Fresh current-target proof

The worker may consume only the reviewed current Kasm existing-runtime adoption probe:

`.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py`

Each fresh probe must prove:

- `proof_kind: existing_runtime_adoption_v1`;
- current exact version/size/SHA equal to the required target fence;
- `inventory_scope: all_running_docker_containers`;
- `inventory_complete: true`;
- `candidate_count: 1`;
- a valid self-consistent candidate fingerprint;
- `state: UNKNOWN` with only `BRIDGE_3_OF_3_SEMANTICS_UNPROVEN` or `NO_STRUCTURAL_BRIDGE`;
- X11 window identity bound to the freshly observed PID;
- the same canonical Docker container **name** as the source registration, while container instance id may differ;
- the same display, remote-view endpoint and remote-view mapping as the source registration.

Boot identity, PID, process-start ticks and container instance id are replaced from fresh proof and are not treated as continuity anchors across either an exact-client build transition or an exact-current identity refresh. Their old values are historical evidence only. Target authority comes from the repeated fresh exact-current singleton proof, not from numeric PID continuity.

## Transaction

Inside one continuously supervised `guard-run` critical section the worker must:

1. validate the exact approved predecessor-or-current source registration and current controller generation;
2. perform fresh current-target probe A and validate the full closed contract;
3. stage a mode-0600 candidate registration derived from probe A;
4. perform probe B and require the complete fresh adoption signature to equal probe A;
5. re-read the authoritative registration and require it still equals the exact source record;
6. revalidate the same active task/session and lease generation;
7. atomically replace `runtime-registration.json`, fsync the canonical state directory, increment `registration_generation` by exactly one and bind `lease_generation` to the current controller;
8. re-read the committed record through the current exact fence;
9. perform probe C and require the complete fresh adoption signature to remain identical;
10. revalidate the committed current record, current task/session and lease generation before success.

The committed registration must take current runtime identity only from the fresh proof and force `state: UNKNOWN`. It must not retain or promote any previous `IN_GAME` semantics.

If any post-commit check fails, rollback may restore the exact source record only when the current registration is still exactly the transaction's own committed record. A concurrent or unexpected record fails closed without overwrite.

## Forbidden operations

This transition MUST NOT:

- launch, stop, restart, signal, attach to, inject into or otherwise control the Tibia process;
- read or write process memory;
- use ptrace, uprobes, input injection, xdotool, GUI automation or gameplay input;
- access credentials, login, logout, relog or select a character;
- infer `IN_GAME` from title, bridge presence, stale registration state or historical evidence;
- delete the registration and fall through to adoption/bootstrap;
- accept an arbitrary predecessor build or any source fence other than the two closed v1 source modes;
- edit `runtime-registration.json` outside the reviewed atomic transaction.

## Postcondition

Success means only:

```yaml
canonical_registration_fence: CURRENT_EXACT
registration_state: UNKNOWN
client_process_mutation_performed: false
process_memory_observation_performed: false
semantic_promotion_performed: false
```

It is not Gate B and does not authorize ordinary mutation. The gameWindowState lane must run its memory-free read-only readiness preflight again from trusted `main`; only a later READY result may engage the owner for the manual LOGIN_SCREEN -> CHARACTER_SELECT -> WORLD -> WORLD_EXIT causal sequence.
