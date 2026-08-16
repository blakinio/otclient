# Track A xkbcomp support inventory — 2026-08-16

## Scope

One bounded read-only support-path observation on `synology-otclient-01`. The job inspected only the two fixed xkbcomp paths and package metadata. It did not execute xkbcomp/Xvfb or inspect official-client/canonical runtime/process/display/VNC/network/login/credential state.

## Exact execution

- run: `31955054478`
- job: `95184310959`
- runner: `synology-otclient-01`
- result: `SUCCESS`

## Proven helper layout

Contained helper:

```text
path=/work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
kind=FILE
real=/work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
mode=755
uid=0
executable=true
sha256=0967e7e7b03b077327cea74567726b265bd304b4fdf59f87bf7fdfe1074e7591
current-container dpkg owner=UNOWNED
```

System helper:

```text
/usr/bin/xkbcomp = ABSENT
```

Current container package database:

```text
x11-xkb-utils = NOT_INSTALLED
xkbcomp = NOT_INSTALLED
```

Classification:

`PROVEN_CONTAINED_XKBCOMP_SYSTEM_ABSOLUTE_PATH_MISSING`

This explains the isolated Xvfb error without another Xvfb/bootstrap run: the exact helper binary needed by Xvfb already exists in the trusted persistent support root, but this packaged Xvfb invokes the compile-time absolute `/usr/bin/xkbcomp`, which is absent in the current runner container.

## Safe repair boundary

No network/package download is necessary to test the immediate environment. A bounded runner-support repair may use only the already proven contained source above and may materialize an exact bit-identical `/usr/bin/xkbcomp` **only if** preflight proves the dedicated runner job has authority to create that path safely. It must:

- require the source exact realpath, uid/mode and SHA above;
- require `/usr/bin/xkbcomp` to be absent or already bit-identical;
- fail closed if `/usr/bin` is not writable by the job identity;
- publish atomically without changing any other `/usr/bin` path;
- verify exact source/target SHA equality;
- run only an isolated Xvfb startup discriminator afterward, not the canonical client bootstrap;
- remove the newly created system helper on any post-publication validation failure.

Because `/usr/bin` is container-local rather than the persistent `/work` support volume, even a successful bounded repair is an immediate unblocking mechanism, not a substitute for declarative runner-image provisioning. Durable runner image configuration should eventually include the required xkbcomp package/helper.
