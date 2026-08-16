# Track A dedicated-runner system xkbcomp repair — 2026-08-16

## Scope

One bounded support-filesystem repair on `synology-otclient-01` followed by one isolated Xvfb startup validation. The operation did not launch the official Tibia client, VNC, WARP, canonical lease/registration/session, game network/login, credentials, `/proc` inventory or Track B surfaces.

## Exact execution

- PR: `#389`
- branch: `ci/OTC-20260816-track-a-runner-system-xkbcomp-repair`
- repair head: `ebd428390e13cec5b064602d37e8a2b2b76181ed`
- workflow run: `31955642775`
- job: `95185761723`
- runner: `synology-otclient-01`
- result: `SUCCESS`

Two older queued/pending runs created while the initial runner selector was being corrected were cancelled by task-local concurrency before execution. The successful run used the previously proven dedicated-runner selector `[otclient, synology]`.

## Source fence

The contained helper was re-proven exactly:

```text
source=/work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
sha256=0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
uid=0
mode=755
ldd_missing=0
```

Result marker:

```text
SOURCE_FENCE=PASS
```

## Publication

The system target was absent at preflight and the job had the required root/writable-path authority. The task staged the exact helper in `/usr/bin`, atomically published `/usr/bin/xkbcomp`, then re-verified the exact source/target digest.

```text
TARGET_PUBLICATION=ATOMIC_CREATED
TARGET_POST=PASS:sha256=0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
```

The target was intentionally retained because post-publication validation succeeded. This is an immediate repair of the current dedicated-runner container, not a claim of durable declarative runner-image provisioning.

## Isolated Xvfb validation

Using the contained Xvfb, contained library paths, contained XKB root and the same argument shape used by the trusted canonical worker, the isolated test selected free display `:199` and created its X11 socket successfully:

```text
XVFB_VALIDATION=PASS:display=:199:socket_created=true
RUNNER_SYSTEM_XKBCOMP_REPAIR=PASS
```

The task-owned Xvfb process was then cleaned up. No canonical runtime/client was created by this validation.

## Classification

`PASS / IMMEDIATE_RUNNER_CONTAINER_XKBCOMP_REPAIR_PROVEN`

The prior `xvfb_socket_missing` discriminator caused by absent compile-time absolute `/usr/bin/xkbcomp` is resolved for the current dedicated-runner container. A fresh RUNTIME bootstrap may now re-enter from current trusted `main`, re-run admission and either advance through canonical bootstrap/Gate B or stop on a new independently observed fail-closed discriminator.

## Remaining boundary

This evidence does **not** prove that a canonical official-client runtime currently exists. Until a fresh RUNTIME operation proves otherwise, current physical claims remain unregistered/unproven. The helper repair also does not replace eventual declarative runner-image provisioning of xkbcomp.
