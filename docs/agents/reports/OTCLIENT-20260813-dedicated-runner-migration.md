# OTCLIENT-TIBIA-RE dedicated runner migration

## Purpose

Record the active migration of the official Linux Tibia reverse-engineering programme from historical Oteryn-owned execution to the dedicated `blakinio/otclient` self-hosted runner.

## Canonical target

```yaml
repository: blakinio/otclient
runner_name: synology-otclient-01
migration_selector: [self-hosted, otclient, synology]
post_deploy_selector: [self-hosted, Linux, X64, otclient, tibia-re, synology]
persistent_state: /home/runner/_work/_otclient_tibia_re_state
runner_infra_pr: 280
runtime_pr: 48
```

New live programme work must not use `oteryn-staging`, `oteryn-synology-staging`, `oteryn-tibia-client-analysis` or `/var/lib/oteryn-staging-state/**` as active execution/state dependencies.

## Runtime consumer change — PROVEN in repository

PR #48 commit:

```text
eb5e3a0151014f07f8c0b66ecf32f2686a418179
ci(otclient-tibia-re): move bootstrap to dedicated OTClient runner
```

The bootstrap workflow now:

- schedules on `[self-hosted, otclient, synology]`;
- verifies repository `blakinio/otclient` and runner name `synology-otclient-01`;
- initializes persistent state under `/home/runner/_work/_otclient_tibia_re_state`;
- does not require Docker, a Docker socket, or an Oteryn-owned container;
- fails if `/var/lib/oteryn-staging-state/tibia-linux-analysis` exists as an active dependency.

## Dedicated runner image — PROVEN buildable

PR #280 provides the `otclient-tibia-re` image target and adds label `tibia-re` to `otclient-runner` while keeping the OTS runner on the lightweight `base` target.

Exact Docker validation:

```yaml
implementation_head: e97cf8be1b2a8c63cecc39e07d0347830b874d5f
workflow_run: 31679256871
job: 94380701487
conclusion: success
```

The validation passed:

```text
shell/Compose validation
base target Docker build
otclient-tibia-re target Docker build
GDB/Xvfb/proxychains/xdotool/Vulkan availability
Python elftools/yaml imports
```

The temporary validation workflow was removed afterward; the run above remains the exact implementation evidence.

## Live runner acceptance — WAITING

Canonical bootstrap run:

```yaml
run: 31679097113
job: 94380204633
head: eb5e3a0151014f07f8c0b66ecf32f2686a418179
status: queued
```

At this checkpoint the bootstrap job has not been assigned to a runner. This does **not** prove the dedicated runner is absent; it proves only that no matching runner accepted the job yet.

The GitHub integration available to the current worker cannot list repository runners (`403 Resource not accessible by integration`), so runner registration/online state cannot be independently queried through the connector.

## Required host deployment

The updated PR #280 stack must be built/recreated on the Synology Docker host. The current worker has no authorized SSH/NAS execution tool, so this host mutation cannot be performed from the current tool environment.

After deployment, the acceptance proof is:

```text
1. synology-otclient-01 registers to blakinio/otclient with labels otclient,ot,synology,tibia-re;
2. PR #48 bootstrap job starts on that exact runner;
3. OTCLIENT_DEDICATED_RUNNER_VERIFIED=true;
4. OTCLIENT_TIBIA_RE_PERSISTENT_STATE_READY=true;
5. OTCLIENT_TIBIA_RE_OTERYN_RUNTIME_DEPENDENCY=false;
6. persistent state remains available to the next dedicated-runner job.
```

## Owner persistence directive

Every material programme finding, experiment result, failure, blocker, artifact reference and next action must be persisted or indexed in `blakinio/otclient` before return/rotation. External repositories/runtimes are not durable active programme state.

## Next action

Deploy/recreate PR #280's updated `otclient-runner` on Synology, then reconcile run `31679097113` once. If it remains queued after confirmed runner registration, inspect the runner label set and repository registration before changing selectors.
