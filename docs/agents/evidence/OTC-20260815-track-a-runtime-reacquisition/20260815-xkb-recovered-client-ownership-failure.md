# Track A RUNTIME post-XKB client ownership failure

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Execution head: `e5d73eb092968479782bd77061ca12c449b9f62f`
Run: `31885192604`
Job: `95013369670`
Runner: `synology-otclient-01`, id `21`
Conclusion: `FAILURE`
Artifact id: `9247072540`
Artifact ZIP SHA-256: `dacb6fe4ac20eece815003dcb409fc393b32e749883234f0d8edcb4986c12f46`

## FACT — XKB/Xvfb recovery succeeded

The exact `xkbcomp` dependency was verified at `/work/_otclient_tibia_re_state/toolroot/usr/bin/xkbcomp`. Xvfb was launched with that directory as working directory while retaining source XKB configuration and all Track/Task/Role/no-secret fences.

Bootstrap then completed successfully:

```text
TRACK_A_RUNTIME_SOURCE_STATE=/work/_otclient_tibia_re_state
TRACK_A_UPSTREAM_WARP_VERIFIED=true pid=16739 source_state=/work/_otclient_tibia_re_state
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=socks-relay pid=23997
TRACK_A_TASK_SOCKS_RELAY_VERIFIED=true port=25415 pid=23997
TRACK_A_CREDENTIAL_ENV_CLEAR role=xvfb pid=24032
TRACK_A_TASK_XVFB_VERIFIED=true display=:115 pid=24032
TRACK_A_RUNTIME_NAMESPACE_READY=true
```

The separate cross-step persistence gate also completed successfully:

```text
TRACK_A_RUNTIME_PERSISTENT_CHILD_VERIFIED role=socks-relay pid=23997
TRACK_A_RUNTIME_PERSISTENT_CHILD_VERIFIED role=xvfb pid=24032
TRACK_A_RUNTIME_PERSISTENT_RELAY_LISTENING=true
```

This closes the previous `./xkbcomp` / Xvfb bootstrap and immediate cross-step persistence failures.

## FACT — first generation now reaches exact-client launch

`Prepare generation 1` reverified the exact package client and then failed with:

```text
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_RUNTIME_ERROR=client_gen_1_ownership_failed
```

The helper's failure point is after the background launch and PID-file write, after `/proc/$pid/maps` becomes readable, but before window discovery, GDB observer launch or any protected login step.

## Side-effect classification

### FACT

- no login step executed;
- no protected credential variables were injected into the client launch;
- no movement or gameplay/economic action occurred;
- generation-1 structural observer was not armed;
- generation 2 was not attempted;
- cleanup stopped generation slots but returned non-zero before complete task/X11 cleanup, so task-owned run #12 residue may remain and must be inspected/recovered only under exact ownership fences.

## UNKNOWN

The current evidence does not distinguish among:

1. PID-file PID is a transient `setsid`/wrapper PID while the marked client lives under a child PID;
2. the client immediately execs/forks into a different PID/executable while retaining or dropping task markers;
3. expected executable identity differs because of launch/proxy behavior;
4. the client remains at the PID but one Track/Task/Role marker is missing.

No one of these is assumed.

## Next discriminator

Perform read-only inspection of exact run `31885192604` residue before any new runtime launch:

- recorded `client-gen-1.pid` and liveness;
- recorded PID `/proc/<pid>/exe`, environment ownership markers and parent/child relationships when present;
- bounded `/proc` scan for exact Task + `client-gen-1` role marker, recording PID/exe/PPID only;
- sanitized tail of task-owned `generation-1/client.log`;
- Xvfb/relay state and X11 residue for cleanup planning.

Do not access credentials and do not start/stop/signal any process during the diagnostic.
