# Track A Kasm Canonical Bootstrap — Design

## Status and scope

This design defines a KasmVNC-aware `create_new` path for the Track A canonical official-client runtime in `blakinio/otclient`.

It exists to recover the persistent physical runtime after the Synology restart without bypassing the canonical lease/flock/bootstrap boundary. The design does not authorize login, credentials, character selection, gameplay, semantic promotion, or process-memory observation.

Current evidence at design time:

- trusted `main`: `b5c7d0fbb0e9667abe6fea7bbaea8834c1c654b5`;
- `synology-otclient-01` has been restored and now starts with Docker restart policy `always`;
- stale/deleted organization runner containers have been stopped and prevented from restart loops;
- `oteryn-organization-recovery` stale `.backup.lock` was removed only after proving no live backup cycle, and recovery is stable again;
- fresh gameWindowState preflight `33258891050 / 99117302494` reaches the global exact-client inventory and fails memory-free with `OFFICIAL_CLIENT_CANDIDATE_COUNT=0`;
- `otclient-track-a-kasmvnc` is running, `DISPLAY=:1` is the owner-designated physical desktop, and no Tibia `client` process is currently running;
- the exact current executable remains present at `/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client`, fenced to `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

The existing `OTC-20260828-game-window-state-qualification` task remains fail-closed at repository `runtime_access: none`; it must not gain process-control authority merely to manufacture a target.

## Problem

The promoted canonical transition has a reviewed initial-creation path, but its legacy bootstrap model launches a host-visible process group and requires local PID/process-group ownership. The current physical runtime is Docker/Kasm based. Its official client PID exists inside `otclient-track-a-kasmvnc`, while the self-hosted GitHub runner is a separate container with a separate PID namespace.

Therefore the legacy bootstrap cannot safely create the exact Docker/Kasm runtime expected by the current canonical registration, Kasm probe, and gameWindowState read-only workflow.

Starting Tibia manually or with an ad-hoc `docker exec` before canonical bootstrap is not acceptable. Client start is process control, and the accepted ADR requires initial creation to occur only inside the reviewed lease + continuously held canonical flock + absence inventory + registration commit + safe-detach transaction.

## Design goals

1. Create at most one exact current official Tibia client in the existing owner-designated Kasm container.
2. Keep the canonical `coordination.lock` continuously held from final absence proof through launch, repeated runtime proof, registration commit, post-commit proof, and safe detach.
3. Reuse the existing Kasm exact-runtime proof rather than inventing a second identity model.
4. Preserve compatibility with downstream Docker-aware canonical readers, including `runtime_locator` and candidate fingerprint evidence.
5. Make rollback target only the exact process created by this transaction.
6. Keep the implementation PR repository-only (`runtime_access: none`) and execute the physical bootstrap only after trusted-main promotion through a separate owner-only main workflow.
7. Avoid credentials, login, character selection, gameplay, GUI input, packet capture, debugger attach, memory observation, and semantic `IN_GAME` claims.

## Non-goals

- no Tibia account authentication;
- no owner credential handling;
- no automatic character/world entry;
- no gameplay keepalive;
- no Kasm container restart or recreation;
- no package download/update or client-byte mutation;
- no change to the gameWindowState reader semantics;
- no weakening of canonical bootstrap, adoption, rebind, recovery, Gate B, or self-hosted workflow security policy;
- no modification of PR #795-owned lease/self-hosted security paths unless later restacking proves unavoidable.

## Chosen architecture

### 1. Add a narrow Kasm bootstrap worker

Add a repository-owned worker dedicated to the existing physical container, for example:

` .github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py `

The worker has no lease authority of its own. It is invoked only by the canonical transition while that transition owns the canonical flock.

The worker exposes three bounded operations:

- `preflight <record>`
- `launch <record>`
- `rollback <record>`

`preflight` is read-only and must prove:

- exactly one running container named `otclient-track-a-kasmvnc`;
- the current full Docker container ID;
- `DISPLAY=:1` is reachable as `kasm-user`;
- the exact package client exists, is executable, regular/non-symlink, exact size/SHA;
- complete inventory across all running Docker containers contains zero official-client candidates, including no mismatched or unverifiable official-looking candidate;
- no existing Tibia main window is present on the target display.

The preflight record is secret-free and binds container name/full ID, display, client path, size/SHA, and an inventory nonce/fingerprint sufficient for the transition to reject stale or switched-target input.

### 2. Add a Kasm-specific create-new transition

Do not weaken or reinterpret the legacy host bootstrap. Add a separate operation in `.github/scripts/tibia-official-client-re-canonical-live-transition.py`, e.g. `kasm-bootstrap`.

The operation uses the existing canonical lease manager, task/session capability, cancellation-safe supervisor primitives, and `coordination.lock`.

Inside the continuously held flock it performs:

1. validate the current authoritative lease generation;
2. require authoritative registration absent;
3. call Kasm worker `preflight` and require zero official-client candidates;
4. revalidate lease/registration absence;
5. call Kasm worker `launch`;
6. validate the launch record;
7. call the existing `.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py` repeatedly around commit;
8. require exact singleton Docker/Kasm identity and prove it matches the launch record;
9. stage and atomically commit canonical registration;
10. repeat the exact Kasm proof after commit;
11. revalidate the lease and committed registration;
12. prove no bootstrap helper/process remains besides the exact official client;
13. release the transaction and leave the exact client persistent.

The existing Kasm probe remains the authoritative current-runtime proof for Docker container identity, current PID/start ticks, exact executable fence, `DISPLAY=:1`, X11 window ownership, remote-view metadata, all-running-container inventory completeness, candidate count and candidate fingerprint.

### 3. Registration compatibility

The new Kasm bootstrap must produce a registration that all existing Docker-aware canonical consumers can reproduce.

Use the same runtime-proof fields already emitted by the Kasm adoption probe:

- `runtime_locator: docker:<container-name>:<full-container-id>`;
- `inventory_scope: all_running_docker_containers`;
- `inventory_complete: true`;
- `candidate_count: 1`;
- `candidate_fingerprint`;
- current container PID/start/fence/display/window evidence;
- fail-closed semantic `state: UNKNOWN`.

The registration should retain the existing Kasm proof schema used by current Gate B/recovery readers rather than introduce a parallel Docker identity format. Add explicit bootstrap provenance only if it can be additive and does not make existing readers reinterpret the proof.

No bootstrap transaction may claim `IN_GAME`. A newly launched unauthenticated client is registered as `UNKNOWN` even if structural helpers unexpectedly exist.

### 4. Launch boundary

`launch` must start only the exact already-present binary. It must not update or copy the package.

Preferred mechanism:

- `docker exec -d` into the exact preflight-bound full container ID;
- user `kasm-user`;
- working directory equal to the exact package directory;
- `HOME=/home/kasm-user` and `DISPLAY=:1` set explicitly;
- direct `exec` of the exact client executable, with no shell left resident;
- no `TIBIA_TEST_*`, lease token, capability token, GitHub credential, or task secret passed into the client environment.

The worker must capture the newly created client PID and process start ticks only after proving exactly one exact client exists in the same container and that it did not pre-exist the transaction.

### 5. Rollback

Rollback is fail-closed and process-specific.

The launch record must bind at least:

- target container name and full ID;
- client PID;
- process start ticks;
- exact executable size/SHA;
- exact executable path;
- display;
- transaction/run marker retained outside the client secret environment if needed.

Before signalling anything, rollback must re-prove all of those fields against the live process. If any identity field differs, rollback refuses to signal rather than risk killing an unrelated process.

If the transaction committed its own registration and later fails, it removes only that exact registration record before/while rolling back the exact bootstrap-created client, following the existing atomic-registration conflict rules. It never deletes a concurrent replacement registration.

No broad `pkill`, `killall`, container stop/restart, display cleanup, or volume cleanup is allowed.

### 6. Safe detach

Successful safe detach means:

- the exact client remains alive in `otclient-track-a-kasmvnc`;
- repeated Kasm probe is stable;
- canonical registration is committed and re-read successfully;
- the current lease remains valid through the final proof;
- no launch wrapper, temporary helper, debugger, credential ingress, or mutation-capable bootstrap process remains inside the target container;
- the persistent client has no canonical flock descriptor or lease capability;
- release of the transition's flock cannot terminate or mutate the client.

## Physical execution workflow

The implementation PR remains repository-only and must not execute the official client.

After merge to trusted main, a separate main-only live workflow may invoke exactly one Kasm bootstrap transaction. It should be a dedicated `workflow_dispatch` workflow with these boundaries:

- actor must be repository owner;
- ref must be `refs/heads/main`;
- checkout exact current main and verify against `git ls-remote`;
- run on `[otclient, synology]`;
- no PR-triggered self-hosted physical job;
- no secrets or credential environment;
- durable task checkpoint must be `runtime_access: canonical_bootstrap`, `bootstrap_mode: create_new`, `bootstrap: PASS`, `bootstrap_attempt_limit: 1`, `mutation_authorized: true`, `credentials_allowed: false`, `login_allowed: false`, `character_selection_allowed: false`, `gameplay_allowed: false`;
- the workflow consumes the one authorization once and cannot be replayed blindly;
- physical result records exact run/job, main SHA, lease generation, registration generation, container full ID, PID/start, exact fence, and rollback/detach status without retaining raw client data.

The workflow must be designed to coexist with the self-hosted security hardening lane. In particular, do not edit PR #795-owned lease workflow or its security contract merely to get this bootstrap running. If PR #795 merges first, restack on it and satisfy its current self-hosted workflow checks before the bootstrap PR becomes ready.

## Interaction with gameWindowState qualification

The Kasm bootstrap does not perform the gameWindowState experiment.

After successful bootstrap and release of temporary canonical authority:

1. fresh-check current `main`;
2. run a new memory-free `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`;
3. require exact singleton candidate plus valid Docker canonical registration;
4. require memory-free `READY`;
5. run a fresh `START_GAME_WINDOW_STATE_QUALIFICATION`;
6. only after the continuous read-only logger is active ask the owner to perform `LOGIN_SCREEN -> CHARACTER_SELECT -> WORLD -> WORLD_EXIT`;
7. correlate owner phase markers to the one continuous artifact;
8. keep `IN_GAME_CLAIMED=false` and `semantic_promotion_performed=false` during qualification;
9. only a causal PASS can lead to a separate semantic-promotion PR with independent exact-head review.

No old all-`EMPTY` session may be spliced into the new causal session.

## Testing strategy

Implementation follows TDD.

### Worker tests

Deterministic tests must cover at least:

- target container missing/multiple/not running;
- display unavailable;
- exact client missing, symlinked, wrong size, wrong SHA;
- zero-client preflight success;
- existing exact client blocks create-new;
- mismatched/unverifiable official-looking client blocks create-new;
- launch returns exactly one new exact PID/start in the preflight-bound container;
- launch target/container drift fails closed;
- client exits before proof;
- rollback exact identity success;
- rollback PID reuse/start drift refuses signal;
- rollback container ID drift refuses signal;
- no broad process-control command exists in the worker.

### Canonical transition tests

Extend the existing canonical transition suite to prove:

- Kasm bootstrap requires registration absent;
- final absence inventory occurs while canonical flock/lease are current;
- launch occurs only after zero-candidate proof;
- existing Kasm probe is repeated before commit and after commit;
- launch record and probe identity must match;
- registration contains Docker locator/candidate provenance and `state: UNKNOWN`;
- lease or registration drift before commit aborts;
- post-commit proof failure removes only own registration and triggers exact rollback;
- success leaves the client alive and returns only after safe-detach proof;
- legacy host bootstrap behavior remains unchanged;
- adoption/rebind/recovery/boot-epoch recovery/Gate B regressions stay green.

### Workflow/governance tests

Require:

- YAML parse;
- deterministic Track A admission validation;
- no PR event can schedule the physical self-hosted bootstrap job;
- owner + main-ref gate before scheduling;
- no credential/secret environment in physical steps;
- exactly one bootstrap attempt;
- implementation PR task remains `runtime_access: none` and physical action budget `0`;
- exact changed-path and `git diff --check` validation;
- current self-hosted security policy passes after any required restack.

## Expected implementation paths

Primary implementation paths:

- `.github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py`
- `.github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py`
- `.github/scripts/tibia-official-client-re-canonical-live-transition.py`
- `.github/scripts/test_tibia_official_client_re_canonical_live_transition.py`
- `.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py` only if a strictly necessary reusable proof hook is missing;
- a focused repository-only contract workflow for the new worker/transition;
- a dedicated main-only live bootstrap workflow;
- `docs/agents/tasks/active/OTC-20260829-track-a-kasm-canonical-bootstrap.md`;
- focused evidence under `docs/agents/evidence/OTC-20260829-track-a-kasm-canonical-bootstrap/`;
- `docs/agents/MODULE_CATALOG.md`, `docs/agents/CHANGELOG.md`, and relevant canonical contracts/ADR only where public behavior actually changes.

Avoid changing `.github/workflows/tibia-official-client-re-canonical-live-lease.yml` while PR #795 owns it.

## Acceptance criteria

Repository implementation is complete only when:

1. RED tests demonstrate the current canonical transition cannot legally bootstrap the Kasm Docker target.
2. GREEN tests prove the new create-new Kasm path and exact rollback semantics.
3. Existing canonical transition, Kasm adoption, rebind, recovery, boot-epoch recovery and Gate B tests remain green.
4. Exact-head GitHub checks and current self-hosted workflow security checks pass.
5. Full diff review finds no unrelated paths or weakened guard.
6. Independent audit reports zero material findings.
7. Implementation merges to current `main` without silently consuming runtime authority.

Physical recovery is complete only when a later one-shot main run proves:

- zero official-client candidates immediately before launch;
- one exact current client launched in `otclient-track-a-kasmvnc`;
- exact singleton Kasm proof stable before and after registration commit;
- authoritative registration current and Docker-locator bound;
- safe detach PASS;
- lease/temporary authority released;
- no credentials/login/character/world/gameplay performed by bootstrap;
- fresh downstream gameWindowState preflight can reach memory-free `READY`.

## Failure policy

Any uncertainty in container identity, executable fence, candidate inventory, launch identity, X11 ownership, registration race, lease generation, rollback identity or safe detach is terminal for that bootstrap attempt and remains fail-closed.

A failed attempt must not be converted into success by manual registration edits, manual client start, broad process cleanup, disabling inventory checks, weakening hash/version gates, ignoring current-main drift, or asking the owner to interact with Tibia before the downstream logger is genuinely READY.
