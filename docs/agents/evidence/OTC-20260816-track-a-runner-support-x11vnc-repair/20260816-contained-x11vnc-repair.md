# Track A contained x11vnc support-root repair — 2026-08-16

## Scope

Bounded physical runner-support filesystem repair on `synology-otclient-01`. No official-client file/process, canonical registration/lease/session, X11/VNC runtime state, network/game/login state, credentials or Track B surface was inspected or mutated.

## First attempt — validation refusal before copy

- run: `31954234775`
- job: `95182280438`
- runner: `synology-otclient-01`
- result: `FAIL_CLOSED_BEFORE_COPY`
- refusal: `RUNNER_SUPPORT_REPAIR_REFUSED=DPKG_VERIFY`
- target created: `false`

`dpkg -V x11vnc` reported only four missing documentation/manpage files in the slim runner image:

- `/usr/share/doc/x11vnc/NEWS.gz`
- `/usr/share/doc/x11vnc/README.gz`
- `/usr/share/man/man1/x11vnc.1.gz`
- `/usr/share/man/man8/Xdummy.8.gz`

No mismatch of `/usr/bin/x11vnc` was reported. The validator was narrowed to permit only that exact known documentation-only absence set; any other package verification difference still fails closed.

## Successful repair

- run: `31954295453`
- job: `95182427755`
- runner: `synology-otclient-01`
- result: `SUCCESS`
- package: `x11vnc 0.9.16-10`
- source: `/usr/bin/x11vnc`
- target: `/work/_otclient_tibia_re_state/toolroot/usr/bin/x11vnc`
- target pre-state: `ABSENT`
- publication: atomic temporary-file -> rename inside contained toolroot

Package/source checks passed:

- source is a regular executable, non-symlink, exact realpath `/usr/bin/x11vnc`;
- source uid is root and mode is not group/world writable;
- dpkg status is installed, exact version `0.9.16-10`, and dpkg ownership maps the source to package `x11vnc`;
- `dpkg -V` differences were only the four known documentation/manpage omissions above.

Existing contained root prerequisites were revalidated before publication. Source and published target hashes are identical:

```text
4954921ae9c4e2bf7061603eb6a2d52c2292a0973eb2da5d6f48a9bd49570ffc
```

The trusted canonical worker's contract-test resolver then returned exactly:

```text
/work/_otclient_tibia_re_state/toolroot
```

and the workflow emitted:

```text
RUNNER_SUPPORT_REPAIR_RESULT=PASS_CONTAINED_TOOLROOT_COMPLETE
```

## Safety boundary

The repair completes the existing hardened one-root support contract; it does not relax the trusted worker to ambient system paths. The one-shot repair workflow was removed immediately after successful evidence capture. A later canonical runtime bootstrap must still use fresh admission and the trusted-main worker; this support repair alone grants no client/runtime mutation authority.
