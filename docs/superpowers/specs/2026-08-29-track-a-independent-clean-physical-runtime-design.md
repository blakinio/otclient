# Track A Independent Clean Physical Runtime — Design

## Status and scope

This design adds one narrow fallback execution class for the already-admitted V4 current-login field6 observation. Canonical Track A bootstrap/reuse/rebind/recovery, retained Kasm state, ordinary physical gameplay, and the persistent programme session remain Synology-only.

Trusted-main probe run `33261106292`, job `99123092884`, proved `synology-otclient-01` was inside a container with read/write access to the Synology host Docker socket. Historical PR-controlled code therefore had a host-equivalent mutation path. Under `TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md`, neither that runner nor another container on the same unverified host is admissible for Tibia credentials.

V4 has not run. `FIELD6_VALUE=UNKNOWN`; physical action count remains `0`.

## Decision

Introduce `execution_class: independent_ephemeral_physical_runtime` for a one-job Linux guest on a physically separate trusted owner workstation, but only when:

1. the normal Synology secret-bearing path is explicitly disqualified by durable evidence;
2. the task is ephemeral and does not depend on canonical/Kasm/Synology-local retained state;
3. `physical_e2e_required: true` remains true;
4. the guest is created from a hash-verified official Ubuntu image after task-specific governance is merged;
5. the runner is repository-scoped, one-job ephemeral, and has no Docker socket, privileged mode, persistent work volume, host filesystem mount, or prior repository state;
6. no secret is reachable before exact trusted-main, exact-run-attempt, runner-identity, and guest-provenance checks pass.

The first and only consumer is `OTC-20260828-current-login-field6-runtime` V4. This class is not a new default and may not be used for canonical operations.

## Alternatives rejected

### GitHub-hosted

It is clean and disposable, but the current routing contract classifies hosted Xvfb below physical E2E. Moving V4 there would silently downgrade the admitted evidence class.

### Fresh Synology container

Rejected because the historical runner had host Docker-socket RW. New container identity cannot prove host cleanliness.

### Full Synology reset

Potentially safe but outside this task and risky to unrelated NAS/Kasm state.

## Independent guest provenance

The initial implementation targets `Molehill-PC` using a newly imported WSL2 guest named `OTClientV4Clean`. The source is Canonical Ubuntu 24.04 Noble amd64 rootfs `noble-server-cloudimg-amd64-root.tar.xz`; the exact SHA256 fetched from Canonical's matching `SHA256SUMS` is recorded before import.

Before GitHub runner registration:

- `/etc/wsl.conf` disables Windows-drive automount and Windows interop/path injection;
- the guest is restarted after that policy change;
- `/mnt/c` is absent and Windows executable interop does not work;
- `/var/run/docker.sock` and other Docker/Podman host sockets are absent;
- no repository checkout, runner `_work`, task state, or prior GitHub runner state exists;
- a dedicated unprivileged `runner` user exists;
- required runtime dependencies are installed from Ubuntu repositories;
- `/etc/otclient-field6-runner-provenance` is root-owned, non-secret and not writable by `runner`;
- the provenance record binds rootfs SHA256, guest name, clean generation nonce, no-automount/no-interop/no-Docker-socket assertions, exact runner name, and the eventual one-time label.

The Windows host is control plane only. No Tibia credential, Actions registration token, or GitHub credential is written into repository files or the provenance record.

## Runner identity and scheduling

Use exact runner name `molehill-otclient-v4-01`. Configure it with `--ephemeral --disableupdate --no-default-labels`. The only custom scheduling label is `field6-v4-<comment_id>`, where `<comment_id>` is the numeric ID of the exact owner V4 trigger comment created on PR #758. The workflow computes the same required label from `github.event.comment.id`.

The V4 comment is created while no matching runner is online, so the exact job queues. Before configuration/start, the coordinator must prove:

- exactly one V4 workflow run exists for that comment and `GITHUB_RUN_ATTEMPT == 1`;
- exactly one queued live job requires `field6-v4-<comment_id>`;
- no other queued job requests that one-time label;
- the guest provenance marker already binds the same comment-derived label and runner name.

Only then is the runner registered and started. Because default labels are disabled, unrelated jobs targeting generic `self-hosted`, `Linux`, `X64`, `otclient`, or `synology` are ineligible.

Before the workflow exposes secrets it must additionally prove:

- protected `main` checkout still equals remote `refs/heads/main`;
- exact owner V4 trigger on PR #758;
- `GITHUB_RUN_ATTEMPT == 1`;
- `RUNNER_NAME == molehill-otclient-v4-01`;
- task `execution_class: independent_ephemeral_physical_runtime`;
- `runtime_access: ephemeral_isolated`, `physical_e2e_required: true`, and `persistent_session_role: none`;
- the comment-derived job label matches provenance;
- root-owned provenance file passes schema/ownership/mode/guest/rootfs/no-host-socket checks.

The repository workflow never provisions or registers the runner and never receives a runner-registration credential.

## Toolroot behavior

The existing field6 helper expects a persistent extracted toolroot. A fresh independent guest instead uses its system root, but only through an exact V4-only gate:

- default Synology behavior stays unchanged;
- only when `TRACK_A_FIELD6_SYSTEM_TOOLROOT=1`, the exact independent runner name is present, and the provenance check has passed may `resolve_toolroot` validate `/` with the same `toolroot_ok` requirements;
- missing Xvfb, xdotool, gdb, XKB data, Mesa `swrast`, or proxychains fails closed;
- a Synology runner or any other task cannot select `/` through this mode.

Runtime packages mirror the proven `otclient-tibia-re` dependency set needed by the V4 helper: Xvfb, xdotool, gdb, proxychains4, Mesa software rendering/X11/GTK runtime libraries, Python, curl, git, procps, iproute2, lsof, netcat, socat and required support libraries.

## Secret and physical-action boundary

No new application secret is introduced. Existing `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` GitHub Actions secrets remain scoped to the single capture step after every admission/provenance gate. Credential text continues into xdotool only through stdin/`--file -`, never argv.

V4 still permits at most one login submit and forbids relogin, restart, character selection, world entry, gameplay, network payload capture, packet retention, process-environment retention, and raw-memory retention. GDB remains the parent process and captures only `uint32(edx)` at `PIE+0xe25620`.

## Cleanup

After any terminal job result:

1. the ephemeral runner auto-deregisters/exits after its single job;
2. no UI rerun or second identical V4 trigger is permitted;
3. sanitized field6 artifact is retained only if schema validation passes;
4. the WSL guest is terminated and unregistered/destroyed from Windows;
5. no runner work/state or credential-bearing guest state remains.

A public hash-verified rootfs download may remain only as an inert image cache. If the single login submit occurred and the scalar was not proven, continuation requires a newly justified generation rather than an identical retry.

## Routing-contract change

`OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md` gains a third class:

```text
independent_ephemeral_physical_runtime
```

It is a security fallback requiring durable Synology disqualification evidence plus a task-specific independent-runtime contract. It does not alter `synology_physical_runtime` semantics or canonical ownership.

## TDD and validation

Repository RED/GREEN must prove:

- current routing lacks/rejects the new class before implementation;
- the new class is legal only for `ephemeral_isolated` physical work with explicit independent-host provenance requirements;
- canonical access classes cannot use the fallback;
- V4 consumer tests reject the old Synology selector after field6 is reclassified;
- independent selector/name/comment-derived label/attempt/main/owner/provenance ordering is exact;
- PR events cannot schedule the physical job;
- system-toolroot mode is impossible without exact independent-runner markers;
- secret references remain only in the capture step and after admission;
- old canonical/Synology behavior remains unchanged;
- reusable self-hosted boundary, Track A governance, field6 contract/security/audit, materializer and CI remain GREEN.

Host provenance before V4 is persisted as sanitized evidence: rootfs source + SHA256, guest name, WSL version, automount/interop disabled, Docker socket absent, exact runner name, one-time comment-derived label, ephemeral registration mode and queued-job uniqueness. Registration credentials and Tibia credentials are never retained.

## Acceptance

The fallback is ready only when the governance/contract PR is merged to protected `main`, the field6 consumer is separately restacked and merged on that trusted base, a newly imported guest passes all provenance checks, the matching runner is absent/offline before the exact V4 job is queued, and only that queued attempt can be accepted. Only then may the single V4 owner trigger be posted.