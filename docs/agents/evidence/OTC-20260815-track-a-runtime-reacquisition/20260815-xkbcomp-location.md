# Track A RUNTIME exact `xkbcomp` location

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Read-only diagnostic head: `d4a376bfa9ba24db1e3fe02bb69fd0709bdd1a6f`
Run: `31885075194`
Job: `95013088148`
Runner: `synology-otclient-01`, id `21`
Conclusion: `SUCCESS`
Artifact id: `9247041394`
Artifact ZIP SHA-256: `d207b9bfb568f68491efc5c47b8d9dc63b2b0ad51dcc43442d76d0d739c57059`

## Scope

The diagnostic was read-only. It did not start, stop or signal any Xvfb, relay, client, GDB or shared upstream process and did not access credentials.

## FACT

The proven runner source state remains:

```text
/work/_otclient_tibia_re_state
```

The source Xvfb binary exists. Under that same exact source toolroot, the diagnostic checked candidate compiler locations and found exactly:

```text
/work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp
```

with:

```text
exists=true
executable=true
size=221288
```

The other checked candidates were absent:

```text
/work/_otclient_tibia_re_state/toolroot/bin/xkbcomp
/work/_otclient_tibia_re_state/toolroot/usr/libexec/xkbcomp
/work/_otclient_tibia_re_state/runtime/xkbcomp
```

A bounded `find` under the source toolroot returned the same single path.

## Relation to the direct Xvfb stderr

The previous read-only diagnostic proved Xvfb fails with:

```text
sh: 1: ./xkbcomp: not found
XKB: Failed to compile keymap
Keyboard initialization failed.
```

Therefore the relative command `./xkbcomp` can be satisfied without copying/installing any dependency by starting the already exact source Xvfb with working directory:

```text
/work/_otclient_tibia_re_state/toolroot/usr/bin
```

while retaining `XKB_CONFIG_ROOT` and `-xkbdir` against the existing source toolroot XKB data.

## Classification

### FACT

- exact `xkbcomp` dependency is present and executable;
- no package installation, network download, binary replacement or shared-state mutation is required;
- the narrow repair is a process working-directory correction only.

### RECOMMENDATION

Restore the fenced RUNTIME workflow and change only the effective Xvfb launcher so it executes from `$toolroot/usr/bin`, where `./xkbcomp` is proven. Keep the existing exact source/client/WARP, task-role, credential, `setsid`, X11, cleanup and transport gates unchanged. Recover only exact failed run `31884912160` residue before the next bootstrap.
