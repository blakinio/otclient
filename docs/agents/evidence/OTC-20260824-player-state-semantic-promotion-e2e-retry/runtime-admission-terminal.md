# Player-state semantic-promotion E2E retry — terminal runtime evidence

Task: `OTC-20260824-player-state-semantic-promotion-e2e-retry`  
PR: `#692`  
Trusted main at runtime transaction: `e98545313a606d6bf4edfb43768e042d2242392c`  
Runtime workflow: `32770840660`  
Physical job: `97570588590` (`synology-otclient-01`)  
Exact workflow head: `f0393251ff711e58448fa682144a4cb9bd3ae041`

## Source-of-truth preflight

The retry was based on current trusted `main` and the terminal merged outcomes of PRs `#688`, `#689`, `#690`, and `#691`.

Fresh controller-plane admission before the transaction observed:

- canonical lease: `released`, generation `25`, no controller task/session;
- authoritative registration: present, registration generation `2`, lease generation `19`;
- registered PID/start ticks: `19590 / 76611792`;
- registered proof: `existing_runtime_adoption_v1`;
- registered semantic state: `UNKNOWN / BRIDGE_3_OF_3_SEMANTICS_UNPROVEN`;
- no lease capability, credentials, token material, login material, or session secret was read or retained.

A separate nonmutating locator observed the canonical Kasm container `otclient-track-a-kasmvnc`, display `:1`, one exact current client PID `646` / start ticks `1394843`, size `52109920`, SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`, and the owned Tibia X11 window. That locator did not itself claim all-container uniqueness; the reviewed Kasm probe later supplied that discriminator under the canonical transition.

## Fresh exact-main admission transaction

Run `32770840660` checked out exact head `f0393251ff711e58448fa682144a4cb9bd3ae041` and revalidated that live `main` was still `e98545313a606d6bf4edfb43768e042d2242392c`.

Before touching canonical controller state it passed:

- Track A task governance;
- canonical transition suite: `30` tests PASS;
- Kasm existing-runtime probe suite: `10` tests PASS.

It then acquired one fresh controller lease without stale takeover or idempotent reuse:

```text
TRACK_A_CANONICAL_LEASE_ACQUIRE=true
TRACK_A_CANONICAL_LEASE_GENERATION=26
TRACK_A_CANONICAL_LEASE_STALE_TAKEOVER=false
TRACK_A_CANONICAL_LEASE_IDEMPOTENT=false
TRACK_A_CANONICAL_LEASE_VALIDATE=true
PLAYER_STATE_RETRY_GATE_A=PASS
```

Classification: `Gate A = PASS`.

## Canonical adoption rebind result

The trusted-main Kasm adoption probe completed successfully under the reviewed transition:

```text
TRACK_A_KASM_EXISTING_RUNTIME_PROBE=PASS
```

That probe is fail-closed and inventories official-client candidates across all running Docker containers, requires exactly one exact current candidate in `otclient-track-a-kasmvnc`, validates the process fence and owned X11 window, and emits adoption identity/evidence for the transition.

The repaired canonical rebind from PR `#689` then refused the transaction:

```text
TRACK_A_CANONICAL_TRANSITION_ERROR=probe_registration_pid_mismatch
PLAYER_STATE_RETRY_REBIND=BLOCKED:probe_registration_pid_mismatch
```

This is not the evidence-only refresh case repaired by `#689`. The current exact client PID/start identity (`646 / 1394843`) is different from the authoritative registration PID/start identity (`19590 / 76611792`). The current implementation intentionally permits `BRIDGE_3_OF_3_SEMANTICS_UNPROVEN -> NO_STRUCTURAL_BRIDGE` only while stable adoption identity is unchanged. Stable identity drift remains fail-closed.

The workflow cryptographically compared `runtime-registration.json` before and after the failed rebind and reported:

```text
PLAYER_STATE_RETRY_FAILED_REBIND_REGISTRATION_UNCHANGED=true
```

A fresh post-run controller-plane read confirmed the registration is still generation `2` / lease `19`, PID/start `19590 / 76611792`, state `UNKNOWN / BRIDGE_3_OF_3_SEMANTICS_UNPROVEN`; current registration file SHA-256 is `a9cd1c53e6bf369f68b23ef9e381099d5c137295ff68fdad92908c57c267790b`.

Classification: `generation rebind = BLOCKED (probe_registration_pid_mismatch)`.

## Downstream gates and one-shot action budget

Because rebind was blocked, policy required immediate refusal before Gate B or semantic promotion preconditions:

```text
PLAYER_STATE_RETRY_GATE_B=NOT_REACHED
PLAYER_STATE_RETRY_SEMANTIC_PRECONDITIONS=NOT_REACHED
PLAYER_STATE_RETRY_READY=false
PLAYER_STATE_RETRY_COMMIT=false
PLAYER_STATE_RETRY_POSSIBLY_DISPATCHED=false
PLAYER_STATE_RETRY_PHYSICAL_ACTION_COUNT=0
```

The Kasm probe itself passed the exact-singleton/all-running-Docker candidate discriminator, so `target_uniqueness = PROVEN`; it does not override the blocked canonical rebind.

No `input.lock` guarded action path, no movement worker, and no gameplay input was invoked. The authorized one-tile effect budget remains unused. No automatic retry is legal or required because `COMMIT` was never reached; the authorization does not carry into a future task automatically.

No login, credentials, relog, restart, character selection, client signal/process-control shortcut, memory write, injection, transaction, or network/gameplay mutation occurred.

## Controller release and final runtime safety

The task released generation `26` after the fail-closed result:

```text
TRACK_A_CANONICAL_LEASE_RELEASE=true
TRACK_A_CANONICAL_LEASE_GENERATION=26
PLAYER_STATE_RETRY_RELEASE=PASS
```

A separate post-run read confirmed:

- lease status `released`;
- lease generation `26`;
- controller task/session `null`;
- registration unchanged at generation `2` / lease `19`.

## Terminal classification

```text
Gate A: PASS
rebind: BLOCKED_PROBE_REGISTRATION_PID_MISMATCH
Gate B: NOT_REACHED
target uniqueness: PROVEN
semantic preconditions: NOT_REACHED
READY: false
COMMIT: false
POSSIBLY_DISPATCHED: false
PHYSICAL_ACTION_COUNT: 0
runtime lease: released generation 26
semantic promotion: NOT_PERFORMED
repository product-code promotion: NOT_PERFORMED
```

The retry is terminally blocked by stale canonical registration identity, not by the PR `#689` evidence-refresh bug. A future attempt would require a separately reviewed and authorized canonical stale-registration recovery lifecycle that legally reconciles the authoritative registration with the current physical runtime before a new movement authorization is requested.
