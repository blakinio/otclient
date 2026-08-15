# Track A RUNTIME generation-1 client role/PID diagnostic

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Diagnostic head: `c632cb8f519c78f85e4209a0ef3c8484f2193ef2`
Run: `31885303986`
Job: `95013631491`
Runner: `synology-otclient-01`, id `21`
Conclusion: `SUCCESS`
Artifact id: `9247096332`
Artifact ZIP SHA-256: `662666569978e2e230f973c08e63f5e502a5a07faa61febc04a62a196eda2ddd`

## Scope

The diagnostic was read-only. It inspected only the exact failed run `31885192604` task namespace and bounded `/proc` metadata. It did not start, stop or signal any process and did not access credential values.

## FACT

The helper-recorded generation-1 PID was:

```text
recorded_client_pid=24109
recorded_client_alive=false
```

At diagnostic time there were zero current task processes with the `client-gen-1` role:

```text
exact_client_role_matches=0
recorded_pid_children=0
```

The only surviving exact-task process was the task-local SOCKS relay:

```text
exact_task_processes=1
task_process pid=23997 ppid=1 client_role=false exe=/usr/bin/python3.12
socks-relay_pid=23997
socks-relay_alive=true
socks-relay_task_owned=true
task_socks_port_listening=true
```

The Xvfb from run #12 was already dead and left no active X11 lock/socket:

```text
xvfb_pid=24032
xvfb_alive=false
x11_lock_exists=false
x11_socket_exists=false
```

The sanitized task-owned client log contains only:

```text
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
```

No login step had executed in run #12 and no protected credential variables were injected into the client launch.

## Classification

### FACT

- trusting the immediate background `$!` as the long-lived authoritative client PID is not sufficient for the lifecycle used by the repaired workflow;
- the diagnostic cannot prove whether the recorded PID was a transient `setsid` process or the client itself before it exited, because it was already dead when inspected;
- no marked client process survived for later inspection;
- there is no evidence of login, movement or gameplay/economic side effects.

### INFERENCE

The next launch should not weaken `role_owned`. Instead it should assign the canonical PID only after discovering exactly one process that simultaneously satisfies:

1. Track marker;
2. Task marker;
3. **current workflow run marker**;
4. exact role marker (`client-gen-N` / `observer-gen-N`);
5. exact expected executable.

This handles a transient launcher PID without accepting foreign/stale processes. The same discovery should be used for GDB because it is also launched through the persistent lifecycle wrapper.

### RECOMMENDATION

Add `OTCLIENT_TIBIA_RE_RUN_ID=$GITHUB_RUN_ID` to every task-owned persistent child, require it inside ownership checks, and discover client/GDB PIDs from `/proc` by exact markers + executable before writing canonical PID files. Recover the surviving run-12 relay only under exact existing task/role ownership before the next bootstrap.
