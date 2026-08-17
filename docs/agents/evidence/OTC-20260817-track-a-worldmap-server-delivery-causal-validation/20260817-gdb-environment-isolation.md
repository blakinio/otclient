# OTC-20260817 — pre-login GDB runtime-environment isolation

```yaml
evidence_date: 2026-08-17
task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
branch_head: d14b3f6449ba45307e0889cb5f52d45a5722bbdd
restacked_main: 7fa86095667dcc71005fbf366921c4cb565ebc3f
run_id: 32027110459
job_id: 95378725544
runner: synology-otclient-01
client_launched: false
process_observed: false
credentials_used: false
result: PASS
```

## Question

Why did the attempt-1 pre-Storage observer exit immediately before login in run `32026662197`?

Historical accepted persistent observer code launched `/work/_otclient_tibia_re_state/toolroot/usr/bin/gdb` with the toolroot runtime library environment. The isolated baseline harness invoked the same executable path without that environment.

## Direct deterministic result

The diagnostic invoked only `gdb --version`; it did not launch or inspect a Tibia process.

Without toolroot runtime libraries:

```text
WORLDMAP_GDB_PLAIN_RC=127
error while loading shared libraries: libpython3.12.so.1.0: cannot open shared object file
```

With:

```text
LD_LIBRARY_PATH=/work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu:/work/_otclient_tibia_re_state/toolroot/lib/x86_64-linux-gnu
PATH=/work/_otclient_tibia_re_state/toolroot/usr/bin:/work/_otclient_tibia_re_state/toolroot/usr/sbin:/usr/bin:/bin
```

result:

```text
WORLDMAP_GDB_TOOLROOT_ENV_RC=0
WORLDMAP_GDB_ENVIRONMENT_ISOLATION=PASS
WORLDMAP_GDB_CLIENT_LAUNCHED=false
WORLDMAP_GDB_PROCESS_OBSERVED=false
WORLDMAP_GDB_CREDENTIALS_USED=false
```

## Classification

```yaml
attempt_1_observer_exit_root_cause: MISSING_TOOLROOT_GDB_RUNTIME_LIBRARY_ENVIRONMENT
libpython3_12_dependency_missing_without_toolroot_ld_library_path: PROVEN
same_gdb_starts_with_toolroot_environment: PROVEN
ptrace_failure_as_attempt_1_root_cause: NOT_REACHED
client_failure_as_attempt_1_root_cause: DISPROVEN_AT_THIS_GATE
repair_input_materially_changed: true
identical_retry: false
```

The next baseline attempt is therefore permitted as the one evidence-based repair for this gate. It must inject the toolroot GDB environment only for the observer process, preserve pre-login attachment proof, and otherwise keep the baseline experiment unchanged.
