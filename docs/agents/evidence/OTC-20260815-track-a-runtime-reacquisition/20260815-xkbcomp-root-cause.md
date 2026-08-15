# Track A RUNTIME XKB compiler root cause

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Read-only diagnostic execution head: `4999b050ff83b8734528949e53ae4abad2728b1c`
Diagnostic run: `31885018787`
Diagnostic job: `95012954293`
Runner: `synology-otclient-01`, id `21`
Conclusion: `SUCCESS`
Artifact: `track-a-runtime-xvfb-diagnostic-31885018787`
Artifact id: `9247024733`
Artifact ZIP SHA-256: `299cb6b7004213f1f726d336c3f2fafbb4eaa6e86b3e2b516cb8c02bc3dd88ce`

## Diagnostic scope

The diagnostic performed only read-only inspection of canonical task-owned residue from failed run `31884912160`. It did not start, stop or signal Xvfb, relay, client, GDB or the shared upstream process. It did not read or print credential values.

## FACT — task-owned residue state

At diagnostic time:

```text
root_exists=true
file=xvfb.log exists=true size=262
file=relay.log exists=true size=0
file=xvfb.pid exists=true size=6
file=socks-relay.pid exists=true size=6
role=xvfb pid=22489 alive=false
role=socks-relay pid=22453 alive=false
x11_lock_exists=false
x11_socket_exists=false
source_xvfb_exists=true
source_xvfb_size=2064864
```

Thus the failed bootstrap did not leave a live Xvfb/relay or active `:115` X11 endpoint. The task-owned residue is filesystem evidence only.

## FACT — direct Xvfb stderr root cause

The sanitized task-owned `runtime/xvfb.log` contains:

```text
sh: 1: ./xkbcomp: not found
sh: 1: ./xkbcomp: not found
XKB: Failed to compile keymap
Keyboard initialization failed. This could be a missing or incorrect setup of xkeyboard-config.
(EE)
Fatal server error:
(EE) Failed to activate virtual core keyboard: 2(EE)
```

This directly explains `TRACK_A_RUNTIME_ERROR=xvfb_exited` from run `31884912160`.

## Classification

### FACT

- the Xvfb binary exists and was executable from the proven source state;
- it exits because its keyboard initialization invokes relative `./xkbcomp`, which is not found from the launch working directory;
- the failure is not a runner-selector, upstream WARP, exact-client, task SOCKS relay, login-secret or gameplay failure;
- generation 1 was never started in the failed run.

### INFERENCE

A correct repair must satisfy the Xvfb binary's relative `./xkbcomp` expectation without weakening XKB config, display or ownership gates. The narrowest candidate is to launch Xvfb from the directory that actually contains the exact source-state `xkbcomp`, provided a read-only diagnostic proves that location and executable status.

### UNKNOWN pending dependency-location diagnostic

Read-only run `31885075194` / job `95013088148` is locating the exact `xkbcomp` dependency under the proven source toolroot. No runtime retry should be issued before that result is available.
