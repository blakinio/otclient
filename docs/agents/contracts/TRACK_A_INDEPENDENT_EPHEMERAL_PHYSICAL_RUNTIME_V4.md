# Track A independent ephemeral physical runtime contract v4

Status: proposed until independently validated and merged to protected `main`. This contract grants no runtime, credential, login, mutation or runner-registration authority to the branch that introduces it.

## Purpose

Define a narrow security fallback when the normal Synology physical host is durably disqualified for a secret-bearing ephemeral experiment. The fallback is `execution_class: independent_ephemeral_physical_runtime` and requires a physically separate owner-controlled Linux guest whose lifetime is one task-owned job.

It is not a second canonical runtime. All canonical registration, bootstrap, reuse/mutation, rebind, recovery, boot-epoch recovery, retained Kasm state and persistent-session work remain `execution_class: synology_physical_runtime` under the existing canonical contracts.

## Admission boundary

A task may use this execution class only when all of the following are true on trusted `main`:

- durable evidence explicitly disqualifies the Synology secret-bearing path;
- `runtime_access: ephemeral_isolated`;
- `physical_e2e_required: true`;
- `persistent_session_role: none`;
- the task owns a unique runtime namespace and `target_uniqueness: PROVEN` before mutation;
- canonical registration, Gate A, generation rebind, Gate B and bootstrap are `NOT_APPLICABLE`;
- the task does not require Synology-local storage, a Kasm/canonical process, LAN-only state or retained runtime identity;
- a task-specific workflow/contract names the exact independent host and proves its clean provenance before any secret.

`canonical_bootstrap`, `canonical_reuse_or_mutation`, `canonical_rebind`, `canonical_recovery`, and `canonical_boot_epoch_recovery` may never route through `independent_ephemeral_physical_runtime`.

## Clean guest provenance

Before the runner is configured, a newly created Linux guest must prove:

1. official source image and exact SHA256 are recorded and verified before import/boot;
2. the guest is physically separate from the disqualified Synology host;
3. no previous repository checkout, runner `_work`, runner credentials/state, task state or prior-job home survives in the guest;
4. host filesystem automount/interop is disabled where the guest platform supports it;
5. no host Docker socket, Podman socket, privileged container interface, unrelated host-home mount or persistent job volume is available;
6. required runtime binaries/libraries are installed before GitHub runner registration;
7. a non-secret provenance record is root-owned and not writable by the unprivileged runner user;
8. that record binds the guest generation, image SHA256, expected runner name and exact one-time scheduling label.

A clean guest cannot attest itself merely by repository-controlled prose. Host-control creation plus direct pre-registration checks are required and their sanitized results become durable evidence after the experiment.

## One-job GitHub runner boundary

The repository job is queued while no matching runner is online. The one-time scheduling label is exactly:

```text
field6-v7-<comment_id>
```

where `<comment_id>` is the numeric GitHub ID of the exact owner V7 trigger comment. Before runner configuration, the coordinator must prove exactly one attempt-1 queued job requires that label and no other queued job requests it.

Runner registration must use the exact task-approved name and:

```text
--ephemeral
--disableupdate
--no-default-labels
--labels field6-v7-<comment_id>
```

The registration credential is short-lived control-plane data. It must not be committed, logged, stored in the guest image/provenance, or placed in a process argv when a pipe/stdin path is available.

Because default labels are disabled, generic `self-hosted`, `Linux`, `X64`, `otclient` and `synology` jobs are ineligible for this runner. If exact queued-job uniqueness is not proven immediately before registration/start, the runner stays offline and the operation fails closed.

## Secret and mutation boundary

Before any application secret is reachable, the job must independently prove trusted protected `main`, `GITHUB_RUN_ATTEMPT == 1`, exact runner name, exact comment-derived label, task admission fields, and the root-owned clean guest provenance record.

Secrets remain scoped to the smallest reviewed step and may not enter workflow inputs, comments, repository files, argv, logs, artifacts, persistent guest state, process-environment evidence or raw-memory evidence.

The initial consumer, current-login field6 V7, retains exactly one login-submit budget and forbids relogin, restart, character selection, world entry, gameplay and network payload capture. This contract does not itself grant that V7 action; the existing owner admission and later merged consumer workflow remain separately required.

## Cleanup and replay

The runner accepts at most one job and then deregisters/exits. After every terminal outcome the guest is destroyed, including its runner work directory and any credential-bearing transient state. UI rerun does not create a second permitted action; `GITHUB_RUN_ATTEMPT != 1` fails before authorization consumption, secret exposure, client execution or physical mutation.

If the one allowed physical action occurred but the intended evidence was not proven, an identical retry is forbidden. Persist the terminal sanitized evidence and require a newly justified generation.

## Failure behavior

Any unknown or mismatch in image hash, physically separate host provenance, host integration, Docker socket state, runner identity, one-time label, queue uniqueness, run attempt, task admission, trusted-main identity, provenance ownership/mode or post-job destruction keeps credentials/login forbidden.

This contract never weakens `TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md`; it supplies a separate safe executor when that contract proves the normal Synology host cannot be trusted for a secret-bearing ephemeral job.

## V7 exact consumer binding

For the current field6 V7 consumer, the only admitted clean guest is OTClientV7Clean and the only admitted GitHub runner name is molehill-otclient-v7-01. The one-time label is field6-v7-<comment_id> and default runner labels remain disabled.

The V7 guest contains a pre-registered, root-owned official-launcher package seed at /opt/otclient-v7-seed/seed.tar.gz. The seed must be a regular non-symlink file owned by root:root, mode 0400 or otherwise not writable by group/world, size 412272538, SHA256 64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016. Before any authorization consumption or secret exposure, workflow provenance must bind and re-prove that seed.

The current V7 package source must be the repository-reviewed official-launcher seed importer. Custom direct payload curl materialization is not an admissible V7 source. The importer must revalidate the archive hash, exact manifest version, exact file set, every manifest localfile size/hash, and the exact bin/client fence before publication.

No host Docker socket, Podman socket, host drive mount, Windows interop, prior repository checkout, prior runner credentials, or prior runner _work may be reachable inside the V7 guest. After the one job terminates, the guest and seed are destroyed together.


## V7 runner-readable immutable permission fence

The current V7 consumer requires exact root-owned permissions before runner registration and again in workflow provenance:

- provenance mode 0644 at `/etc/otclient-field6-runner-provenance`;
- seed directory mode 0555 at `/opt/otclient-v7-seed`;
- seed mode 0444 at `/opt/otclient-v7-seed/seed.tar.gz`.

These exact modes make provenance and seed bytes readable by the unprivileged runner while retaining no runner write path. Any mode mismatch fails before trusted-main checkout, authorization consumption, secret exposure or official-client execution.


## V7 local X11 socket namespace boundary

The V7 credential-bearing guest must remain in the **same boot** from the host-control repair through runner execution. WSLg's read-only `/tmp/.X11-unix` mount must be unmounted only inside `OTClientV7Clean`; global WSL/WSLg settings are not changed. A task-local host-control keeper may preserve that boot until the ephemeral Actions runner listener is active.

Before runner registration, `/tmp/.X11-unix` must be a local X11 socket directory owned by `root:root`, mode 1777, and **not a mountpoint**. The runner user must perform a secret-free Xvfb probe on a non-task display; a real Unix socket must appear and be cleaned completely.

Trusted workflow execution must independently re-prove the local X11 socket directory, mode 1777, not a mountpoint, and run its own secret-free Xvfb probe before authorization consumption or application secrets. Successful proof exports only `TRACK_A_FIELD6_X11_NAMESPACE_VERIFIED=1`; the field6 helper refuses the independent runner without that marker.

Provenance schema `otclient.track-a.independent-field6-runner.v4` binds `x11_socket_dir=/tmp/.X11-unix`, `x11_socket_dir_mode=1777`, `x11_socket_dir_mountpoint=false`, `x11_secret_free_probe=true`, and `same_boot_required=true`.
