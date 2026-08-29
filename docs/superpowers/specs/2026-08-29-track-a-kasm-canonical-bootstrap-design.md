# Track A Kasm Canonical Bootstrap — Design

## Status and scope

This design defines a KasmVNC-aware `create_new` path for the Track A canonical official-client runtime in `blakinio/otclient`.

It exists to recover the persistent physical runtime after the Synology restart without bypassing the canonical lease/flock/bootstrap boundary. It does not authorize login, credentials, character selection, gameplay, semantic promotion, or process-memory observation.

Current evidence at design time:

- trusted `main`: `b5c7d0fbb0e9667abe6fea7bbaea8834c1c654b5`;
- `synology-otclient-01` is restored and its runner container now uses Docker restart policy `always`;
- stale/deleted organization runner restart loops were stopped and disabled;
- `oteryn-organization-recovery` was recovered from a proven stale empty `.backup.lock` and is stable;
- fresh gameWindowState preflight `33258891050 / 99117302494` reaches exact-client inventory and fails memory-free with `OFFICIAL_CLIENT_CANDIDATE_COUNT=0`;
- `otclient-track-a-kasmvnc` is running, `DISPLAY=:1` is the owner-designated physical desktop, and no Tibia `client` process is running;
- the exact executable remains at `/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client`, fenced to `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

`OTC-20260828-game-window-state-qualification` remains repository `runtime_access: none`; it must not gain process-control authority merely to manufacture a target.

## Problem

The promoted canonical transition has a reviewed initial-creation path, but its legacy bootstrap launches a host-visible process group and requires local PID/process-group ownership. The physical runtime is now Docker/Kasm based: the official client PID lives inside `otclient-track-a-kasmvnc`, while the self-hosted GitHub runner is a separate container/PID namespace.

The legacy bootstrap therefore cannot safely create the Docker/Kasm target expected by current registration, Kasm proof and gameWindowState read-only consumers.

An ad-hoc manual start or raw `docker exec` before bootstrap is rejected. Client start is process control, and the accepted ADR requires creation inside one current lease + continuously held canonical flock + zero-client inventory + exact launch proof + registration commit + safe-detach transaction.

## Goals

1. Create at most one exact current official Tibia client in the existing owner-designated Kasm container.
2. Hold `coordination.lock` continuously from final absence proof through launch, repeated runtime proof, registration commit, post-commit proof and safe detach.
3. Reuse the existing Kasm exact-runtime proof and registration shape rather than create a second Docker identity model.
4. Make rollback target only the exact process created by this transaction.
5. Keep implementation repository-only and execute physical bootstrap only from trusted `main` under a separate one-shot runtime admission.
6. Preserve zero credentials/login/character/world/gameplay/UI input/packet capture/debugger attach/memory observation and zero semantic `IN_GAME` claims.

## Non-goals

- no account authentication or credential handling;
- no automatic character/world entry or gameplay keepalive;
- no Kasm container restart/recreation;
- no package download/update/copy or client-byte mutation;
- no change to gameWindowState reader semantics;
- no weakening of bootstrap/adoption/rebind/recovery/Gate B/self-hosted security policy;
- no edit to PR #795-owned lease/self-hosted-security paths unless a later current-main restack proves unavoidable.

## Architecture

### 1. Kasm bootstrap worker

Add `.github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py` with three bounded operations:

- `preflight <record>`
- `launch <record>`
- `rollback <record>`

The worker has no lease authority. The canonical transition invokes it only while holding the canonical flock.

`preflight` is read-only and proves:

- exactly one running `otclient-track-a-kasmvnc` container and its full Docker ID;
- `DISPLAY=:1` reachable as `kasm-user`;
- exact package client is executable, regular/non-symlink and exact size/SHA;
- complete inventory across all running Docker containers has zero exact, mismatched or unverifiable official-client candidates;
- no existing Tibia main window is present on the target display.

The secret-free preflight record binds container name/full ID, display, exact client path, size/SHA and a deterministic snapshot fingerprint. The transition rejects container or target drift before launch.

### 2. Kasm-specific create-new transition

Do not modify the semantics of legacy host bootstrap. Add a separate `kasm-bootstrap` operation to `.github/scripts/tibia-official-client-re-canonical-live-transition.py`.

Under the continuously held canonical flock it performs:

1. validate current authoritative lease generation;
2. require canonical registration absent;
3. run Kasm `preflight` and require zero candidates;
4. revalidate lease and registration absence;
5. run Kasm `launch`;
6. validate the launch record;
7. run the existing Kasm exact-runtime probe before commit;
8. require the probe identity to match the launch record and prove exactly one current exact target;
9. stage and atomically commit canonical registration;
10. repeat the same Kasm exact-runtime proof after commit;
11. revalidate lease and exact committed registration;
12. prove no bootstrap helper remains in the target container besides the official client;
13. return success and release the transaction flock, leaving the exact client persistent.

Any failure enters exact rollback; no owner interaction is requested during this transaction.

### 3. Registration compatibility

The post-launch Kasm probe continues to emit `proof_kind: existing_runtime_adoption_v1`. In this design, that value denotes the already-established **Kasm Docker runtime proof shape** consumed by current Gate B/recovery logic; it does not alone claim that the process pre-dated the transaction.

The bootstrap registration uses that proven shape and adds one optional provenance field:

`creation_kind: kasm_bootstrap_v1`

Existing readers already permit additive registration fields. The canonical transition tests must prove that this field does not alter existing adoption/rebind/recovery/Gate-B behavior.

Required Docker proof fields remain:

- `runtime_locator: docker:<container-name>:<full-container-id>`;
- `inventory_scope: all_running_docker_containers`;
- `inventory_complete: true`;
- `candidate_count: 1`;
- `candidate_fingerprint`;
- current container PID/start/fence/display/window evidence;
- `state: UNKNOWN`.

The bootstrap never claims `IN_GAME`, including when structural helper objects happen to exist.

### 4. Launch boundary

`launch` starts only the exact already-present binary; it does not modify the package.

Required mechanism:

- `docker exec -d` against the exact full container ID proven by preflight;
- user `kasm-user`;
- working directory equal to the exact package directory;
- explicit `HOME=/home/kasm-user` and `DISPLAY=:1`;
- direct execution of the exact client binary so no shell/helper remains resident;
- no `TIBIA_TEST_*`, lease/capability token, GitHub credential or task secret passed to the client.

The worker records the new PID/start only after proving exactly one exact client exists in the same container and that preflight proved zero clients immediately before launch.

### 5. Rollback

The launch record is stored outside the client environment and binds exactly:

- target container name/full ID;
- client PID and process start ticks;
- exact executable path, size and SHA;
- display;
- bootstrap run/transaction identifier in the record only.

No bootstrap marker is injected into the client environment.

Before sending a signal, rollback re-proves every bound identity field against the live process. Any container/PID/start/path/fence mismatch causes rollback to refuse signalling rather than risk another process.

If the transaction committed its own registration and later fails, it removes only that exact registration under the existing commit-conflict rules, then rolls back only the exact bootstrap-created process. It never overwrites or removes concurrent replacement registration.

Forbidden cleanup: `pkill`, `killall`, container stop/restart, display cleanup, volume cleanup or any process-name-only kill.

### 6. Safe detach

Success requires all of:

- exact client alive in `otclient-track-a-kasmvnc`;
- repeated Kasm proof stable;
- registration committed and re-read successfully;
- lease valid through final proof;
- no launch wrapper/helper/debugger/credential ingress/mutation helper remains inside target container;
- client has no canonical flock descriptor or lease capability;
- releasing the transaction flock does not terminate or mutate the client.

## Physical execution workflow

Implementation remains `runtime_access: none` and does not execute the official client.

After trusted-main merge, a dedicated owner-only `workflow_dispatch` physical workflow performs exactly one bootstrap attempt. It must:

- require repository owner actor;
- require `github.ref == 'refs/heads/main'`;
- checkout `main` and verify exact current SHA against `git ls-remote`;
- run on `[otclient, synology]`;
- have no `pull_request` path to the physical job;
- expose no secrets/credentials;
- require a durable task checkpoint with `runtime_access: canonical_bootstrap`, `bootstrap_mode: create_new`, `bootstrap: PASS`, `bootstrap_attempt_limit: 1`, `mutation_authorized: true`, `credentials_allowed: false`, `login_allowed: false`, `character_selection_allowed: false`, `gameplay_allowed: false`, plus explicit `live_runtime_authorization_source` bound to the owner's current approval;
- reject `GITHUB_RUN_ATTEMPT != 1` so UI rerun cannot become a second bootstrap attempt;
- persist a consumed one-shot authorization record before launch;
- record run/job, main SHA, lease/registration generations, container full ID, PID/start, exact fence and rollback/detach outcome without raw client data.

Do not edit PR #795-owned lease/self-hosted security files to enable this. If #795 merges first, restack and satisfy its current self-hosted checks.

## Interaction with gameWindowState

Bootstrap and causal validation remain separate.

After successful bootstrap and release of temporary canonical authority:

1. fresh-check current `main`;
2. run new memory-free `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION`;
3. require Docker registration + exact singleton + memory-free `READY`;
4. run fresh `START_GAME_WINDOW_STATE_QUALIFICATION`;
5. only after the one continuous read-only logger is active ask the owner for `LOGIN_SCREEN -> CHARACTER_SELECT -> WORLD -> WORLD_EXIT`;
6. correlate owner phase markers to that single artifact;
7. preserve `IN_GAME_CLAIMED=false` and `semantic_promotion_performed=false`;
8. only causal PASS may lead to a separate semantic-promotion PR with independent exact-head review.

The historical all-`EMPTY` session cannot be spliced into the new run.

## TDD and validation

### Worker RED/GREEN coverage

- target container missing/multiple/not running;
- display unavailable;
- exact client missing/symlinked/wrong size/wrong SHA;
- zero-client preflight success;
- existing exact client blocks create-new;
- mismatched/unverifiable official client blocks create-new;
- launch creates exactly one new exact PID/start in the preflight-bound container;
- container drift before launch fails closed;
- client exit before proof fails closed;
- exact rollback success;
- PID/start reuse, container-ID drift or fence drift refuses signal;
- static assertion forbids broad process-control commands.

### Canonical transition coverage

- registration must be absent;
- final absence inventory occurs while lease/flock are current;
- launch occurs only after zero-candidate proof;
- Kasm proof runs before and after commit;
- launch record and probe identity must match;
- registration carries Docker locator/provenance, `creation_kind: kasm_bootstrap_v1` and `state: UNKNOWN`;
- lease/registration drift aborts before commit;
- post-commit proof failure removes only own registration and performs exact rollback;
- success leaves client alive only after safe-detach proof;
- legacy host bootstrap remains unchanged;
- adoption/rebind/recovery/boot-epoch-recovery/Gate-B suites remain green.

### Workflow/governance coverage

- YAML parse and `git diff --check`;
- deterministic Track A admission validation;
- no PR event can schedule physical bootstrap;
- owner + exact-main ref gate before self-hosted scheduling;
- no credential/secret environment;
- `GITHUB_RUN_ATTEMPT == 1` and one consumed authorization;
- implementation task remains `runtime_access: none`, physical action budget/count `0/0`;
- full changed-path scope review;
- current self-hosted security policy PASS after any required restack.

## Expected implementation paths

- `.github/scripts/tibia-official-client-re-kasm-bootstrap-worker.py`
- `.github/scripts/test_tibia_official_client_re_kasm_bootstrap_worker.py`
- `.github/scripts/tibia-official-client-re-canonical-live-transition.py`
- `.github/scripts/test_tibia_official_client_re-canonical-live-transition.py`
- `.github/scripts/tibia-official-client-re-kasm-existing-runtime-probe.py` only if a strictly necessary reusable proof hook is missing;
- a hosted contract workflow for the new worker/transition;
- a dedicated main-only physical bootstrap workflow;
- `docs/agents/tasks/active/OTC-20260829-track-a-kasm-canonical-bootstrap.md`;
- focused evidence under `docs/agents/evidence/OTC-20260829-track-a-kasm-canonical-bootstrap/`;
- `docs/agents/MODULE_CATALOG.md`, `docs/agents/CHANGELOG.md` and canonical contracts/ADR only when public behavior actually changes.

Avoid `.github/workflows/tibia-official-client-re-canonical-live-lease.yml` while PR #795 owns it.

## Acceptance

Repository implementation is complete only when:

1. RED proves current transition cannot legally create the Docker/Kasm target.
2. GREEN proves Kasm create-new and exact rollback semantics.
3. Existing canonical/adoption/rebind/recovery/boot-epoch/Gate-B suites remain green.
4. Exact-head checks and current self-hosted security checks pass.
5. Full diff review finds no unrelated paths or weakened guard.
6. Independent audit has zero material findings.
7. Implementation merges to current `main` without consuming runtime authority.

Physical recovery is complete only when a later one-shot main run proves zero candidates immediately before launch, one exact client in `otclient-track-a-kasmvnc`, stable pre/post-commit Kasm proof, current Docker-locator registration, safe detach, authority release, no credential/login/gameplay action, and a fresh downstream gameWindowState preflight reaches memory-free `READY`.

## Failure policy

Any uncertainty in container identity, executable fence, candidate inventory, launch identity, X11 ownership, registration race, lease generation, rollback identity or safe detach is terminal for that bootstrap attempt and remains fail-closed.

A failed attempt may not be converted to success by manual registration edits, manual client start, broad cleanup, weakened inventory/hash gates, ignored current-main drift, workflow rerun, or owner interaction before the downstream logger is genuinely READY.
