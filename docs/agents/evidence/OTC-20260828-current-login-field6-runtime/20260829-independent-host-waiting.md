# 2026-08-29 independent V4 host waiting checkpoint

Checkpoint time: `2026-08-29T19:25:29+02:00`
Track: `official-client-re`
Task: `OTC-20260828-current-login-field6-runtime`

## Trusted repository state

Protected `main` was freshly verified at:

```text
517f96beaeb3b49188f15316a565dd0fb89450ae
fix(track-a): route field6 V4 to independent runner (#806)
```

PR #806 is merged. The trusted V4 workflow now routes only to the independent one-time comment-derived label and no longer targets the disqualified Synology secret boundary.

Current Track A facts remain:

```text
FIELD6_VALUE=UNKNOWN
physical_action_count=0
V4_live_trigger_posted=false
V4_runner_registered=false
Tibia_credentials_exposed=false
V4_login_submit_performed=false
```

The exact live trigger `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true` has not been posted.

## Current external host gate

Fresh Remote Desktop Commander status at this checkpoint:

```text
host=Molehill-PC
status=offline
last_seen=2026-08-29T16:27:12.049+00:00
expected_guest=OTClientV4Clean
expected_runner=molehill-otclient-v4-01
```

This status is point-in-time evidence only. It does not claim the workstation is powered off; it proves the authorized host-control channel is currently unavailable. No attempt is permitted to fall back to Synology for V4 credentials.

## Why Synology remains forbidden

Trusted-main read-only host probe `33261106292 / 99123092884` proved the historical Synology repository runner had read/write access to the host Docker socket. PR #802 persisted that sanitized result. A new runner container on the same unverified Synology host therefore cannot establish clean credential provenance.

## Prepared immutable guest inputs

No runner has been registered. The next host session must freshly verify these public inputs before import/use:

```text
Ubuntu_rootfs_url=https://cloud-images.ubuntu.com/releases/noble/release-20260801/ubuntu-24.04-server-cloudimg-amd64-root.tar.xz
Ubuntu_rootfs_sha256=915b4be62933475c3fb5f5031aa2e159294db95fb32aaa9e8b317aadcb6c065d
GitHub_Actions_runner_version=2.337.0
GitHub_Actions_runner_linux_x64_sha256=70920811a4f8ad4328818682bca5c6469c1c942fab52448868071d0063816613
```

The fresh guest must explicitly provide `/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so` (Ubuntu package `libgl1-mesa-dri`) in addition to the other V4 runtime prerequisites.

## Required next action

When `Molehill-PC` is online again through the authorized control channel:

1. freshly verify protected `main` and this task state;
2. prove `OTClientV4Clean` is absent, or destroy only that exact stale target if a prior incomplete import is found and its ownership is unambiguous;
3. verify/download the exact Canonical rootfs SHA before import;
4. import a new WSL2 `OTClientV4Clean`, disable host automount/interop, restart only that guest, and prove host mounts/Docker/Podman sockets/prior repository and runner state are absent;
5. install/verify the exact system-toolroot dependencies and GitHub Actions runner archive checksum;
6. create the root-owned non-secret provenance record, but do not bind a one-time label or register/start the runner yet;
7. only then post exactly one V4 owner trigger, prove exact attempt-1 queued-job uniqueness, bind `field6-v4-<comment_id>` to provenance, register the one-job `--ephemeral --no-default-labels` runner, and execute the single V4 job;
8. destroy `OTClientV4Clean` after the terminal result.

If one login submit occurs without scalar proof, an identical V4 retry is forbidden. Track B must not consume field6 until the sanitized scalar is separately promoted to trusted `main`.
