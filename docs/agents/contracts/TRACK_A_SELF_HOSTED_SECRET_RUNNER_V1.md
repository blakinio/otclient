# Track A self-hosted secret-runner boundary v1

Status: proposed until merged to protected `main`; this document grants no runtime, credential, login, or mutation authority by itself.

## Purpose

Prevent pull-request or historical same-UID residue from observing credentials used by a Track A physical job in the public `blakinio/otclient` repository. Repository workflow checks are defense in depth only: a pull request can modify its own workflow and checker before scheduling, so a persistent online repository runner is not a secret boundary.

## Mandatory boundary for a secret-bearing physical job

Before any Track A job receives credentials, all of the following must be freshly true:

1. The repository self-hosted runner matching the physical selector is offline and not busy. PR/static validation must not require it online.
2. The physical job is created only from trusted protected `main`; a manual dispatch must additionally require `github.ref == 'refs/heads/main'`.
3. The exact intended run/job/event is queued before a physical runner is brought online, and `GITHUB_RUN_ATTEMPT` must be exactly `1` before authorization consumption or secret access.
4. No other queued job eligible for the same physical selector may race the intended job. Ambiguity fails closed.
5. The runner that is then exposed to credentials is a fresh one-job environment. It must not restore an earlier runner `_work`, runner state, task state, home directory, process namespace, or other writable residue controlled by prior PR jobs.
6. The fresh runner must not mount a host Docker socket, run privileged, or inherit unrelated host-home/state mounts unless a separately reviewed task proves that exact capability is required.
7. Runner registration uses a short-lived repository registration credential through the host control plane. Prefer GitHub ephemeral/one-job registration and disable self-update for the bounded execution.
8. After the one job terminates, the runner unregisters/stops and its disposable work/state is destroyed before any later secret-bearing job.

Secrets may enter only through GitHub Actions for the bounded secret step after trusted-main and task-admission checks pass. They must never be placed in repository files, workflow dispatch inputs, comments, argv, logs, artifacts, retained process environment, or persistent runner state.

## Rerun invariant

A clean one-job runner deliberately does not preserve the old local `COMMENT_ID.used` marker. Therefore any secret-bearing one-shot workflow that relies on such a marker must also reject `GITHUB_RUN_ATTEMPT != 1` before authorization consumption, credential exposure, client execution, or physical action. Historical V1/V2/V3 trigger revocation remains a separate required invariant.

## Failure behavior

If clean-runner provenance, offline-before-queue state, exact queued-job uniqueness, trusted-main workflow identity, run-attempt freshness, or post-job destruction cannot be proven, credentials/login remain forbidden and the task records `BLOCKED`/`WAITING` rather than reusing the persistent runner.
