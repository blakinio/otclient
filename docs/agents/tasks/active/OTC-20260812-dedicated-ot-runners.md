# OTC-20260812-dedicated-ot-runners

status: waiting
branch: ci/dedicated-ot-runners
base: main
pr: 280
feature_scope: infrastructure
completion_claim: internal_only

## Objective

Provide dedicated Synology-hosted GitHub Actions runners for OTClient and OTS work, with the OTClient runner also being the canonical execution environment for `OTCLIENT-TIBIA-RE` so new official-client experiments no longer depend on Freqtrade, Oteryn Platform or `oteryn-staging` runners/containers.

## Ownership

owned_paths:
- infra/ot-runners/**
- .github/workflows/otclient-runner-synology-migrate.yml
- docs/agents/tasks/active/OTC-20260812-dedicated-ot-runners.md
- docs/agents/reports/OTCLIENT-20260813-synology-runner-live-deploy-attempt.md

modules_touched: []
reuses:
- official GitHub Actions runner container image
- PR #48 `OTCLIENT-TIBIA-RE` runtime task as the consumer of the OTClient runner

depends_on: []
blocks:
- migration of new OTCLIENT-TIBIA-RE live execution away from `oteryn-staging` is complete only after the updated OTClient runner image is deployed and accepts a canonical probe
cross_repository_tasks:
- blakinio/Otheryn: runner target only; no repository mutation in this task

## Coordination

- `blakinio/otclient` is the canonical repository for `OTCLIENT-TIBIA-RE` programme state, tools and future live execution.
- PR #48 remains the owner of official-Tibia runtime workflows and targets the dedicated OTClient runner through `[self-hosted, otclient, synology]` during migration and the stricter `tibia-re` label after redeploy.
- Historical Oteryn Platform repositories, reports, runners and containers are read-only evidence only; they are not active execution dependencies.
- `otclient-runner` registers only to `blakinio/otclient`.
- `ots-runner` registers only to `blakinio/Otheryn`.
- No owner-funded AI/Codex/OpenAI quota may be used.
- All material findings/checkpoints for this task are persisted in `blakinio/otclient`; external runtime state is never the only continuation source.

## Runner design

### OTClient

```yaml
service: otclient-runner
repository: blakinio/otclient
runner_name: synology-otclient-01
labels:
  - otclient
  - ot
  - synology
  - tibia-re
build_target: otclient-tibia-re
persistent_work_volume: otclient_runner_work
canonical_tibia_re_state: /home/runner/_work/_otclient_tibia_re_state
```

The `otclient-tibia-re` image target bakes in the Linux/X11/Vulkan/GDB/Qt/proxychains/pyelftools dependencies already exercised by the official-client analysis workflows. Runtime jobs stay unprivileged and do not need `sudo`, Docker-in-Docker or a Docker socket.

### OTS

```yaml
service: ots-runner
repository: blakinio/Otheryn
runner_name: synology-ots-01
labels:
  - ots
  - otheryn
  - ot
  - synology
build_target: base
```

## Acceptance inventory

- [x] One Compose project defines independent OTClient and OTS runner services with separate persistent state/work volumes.
- [x] Each service has a unique runner name and dedicated label set.
- [x] Registration uses a short-lived GitHub runner registration token obtained at container startup from an externally supplied repository credential; no credential is committed.
- [x] The official runner image is pinned by immutable digest.
- [x] The OTClient service has a dedicated Tibia-RE image target rather than broadening the OTS runtime.
- [x] The OTClient image installs the runtime/debug dependencies required by the current official-client programme at image-build time.
- [x] The deployment documentation defines the canonical OTCLIENT-TIBIA-RE runner selector and persistent state path.
- [x] No Docker socket or privileged mode is introduced into the new dedicated runner.
- [x] `docker compose config` and both Docker build targets pass on a real Docker engine for exact implementation head `e97cf8be1b2a8c63cecc39e07d0347830b874d5f`.
- [x] Temporary image-validation workflow was removed after its evidence run.
- [x] Workflow-free repository CI passed on head `5f76d213d859c2a8838ac5b8740865ef6afaf1ab`.
- [x] A bounded one-time Synology migration workflow was created and dispatched from this repository.
- [ ] Updated `otclient-runner` is deployed on Synology and registers `synology-otclient-01` with `tibia-re`.
- [ ] A PR #48 canonical probe is accepted by that runner and proves writable persistent state without touching `/var/lib/oteryn-staging-state/**`.
- [ ] `synology-ots-01` remains available in `blakinio/Otheryn` after the stack update.

## Validation history

Earlier static validation:
- `bash -n` on the original exact `entrypoint.sh`: PASS;
- YAML parse of the original exact `compose.yaml`: PASS;
- official `ghcr.io/actions/actions-runner` image pin verified as runner `2.336.0`, digest `sha256:0cfdcc701ce933c6d243c6b0b2da767366dc9f2e99961d4c3754b0b78084cdda`.

Current migration implementation:
- `Dockerfile` has separate `base` and `otclient-tibia-re` targets;
- `compose.yaml` routes only `otclient-runner` through `otclient-tibia-re` and adds label `tibia-re`;
- `infra/ot-runners/README.md` defines OTClient as the canonical `OTCLIENT-TIBIA-RE` runtime and forbids new `oteryn-staging` state use.

Exact Docker validation:

```yaml
workflow: Validate dedicated OT runners
implementation_head: e97cf8be1b2a8c63cecc39e07d0347830b874d5f
run: 31679256871
job: 94380701487
result: PASS
checks:
  shell_and_compose: PASS
  base_target_build: PASS
  otclient_tibia_re_target_build: PASS
  baked_tool_inspection: PASS
```

The job completed all steps successfully, including `docker compose config`, building `base`, building `otclient-tibia-re`, and verifying GDB/Xvfb/proxychains/xdotool/Vulkan plus Python `elftools`/YAML availability.

The temporary validation workflow was removed after this proof. Workflow-free final code/docs head `5f76d213d859c2a8838ac5b8740865ef6afaf1ab` passed repository CI run `31679760916`, including `CI / Required` job `94383401816`.

## Live deployment attempt — 2026-08-13

A one-time infrastructure-only migration workflow was added on this same task branch in commit:

```text
19b567e993bd72432f75572a0be3f214e4db787d
```

It targets `[self-hosted, oteryn-staging]` only as a migration control plane to reach the Synology Docker socket. It does **not** execute Tibia or any programme experiment there. It deploys only the new OTClient runner stack, keeps token values out of logs/Git, and requires GitHub to report `synology-otclient-01` online with `self-hosted,Linux,X64,otclient,synology,tibia-re` before success.

Exact migration attempt:

```yaml
workflow: One-time Synology OTClient runner migration
run: 31686590850
job: 94403975354
head: 19b567e993bd72432f75572a0be3f214e4db787d
observations: 2
status: queued
conclusion: null
```

Per anti-stall policy no further polling of that unchanged pending state was performed.

Independent broad self-hosted evidence from PR #281 also remains queued:

```yaml
workflow: Self-hosted OTClient Probe
run: 31643425060
head: 91ef11ee8ad02df8c60f9c4f17b1e1ec3d3c6c0e
selector: self-hosted
status: queued
created_at: 2026-08-12T21:38:10Z
```

This proves the deployment failure is not just a wrong `oteryn-staging` label: `blakinio/otclient` currently has no available self-hosted runner capable of accepting even the broad probe.

The canonical PR #48 bootstrap also remains queued:

```yaml
run: 31679097113
job: 94380204633
selector: [self-hosted, otclient, synology]
status: queued
```

Detailed provenance is persisted in `docs/agents/reports/OTCLIENT-20260813-synology-runner-live-deploy-attempt.md`.

## Durable state

PROVEN:
- all programme code/state being consolidated is in `blakinio/otclient` branches/PRs;
- the runner stack is repository-scoped and independent of Oteryn Platform/Freqtrade infrastructure;
- the declarative OTClient runner has a Tibia-RE-specific image target and label;
- the OTClient Tibia-RE image and Compose configuration build/validate successfully on a real Docker engine;
- the temporary validation workflow was removed and workflow-free repository CI is green on the last validated implementation head;
- PR #48 has a consumer migration path that does not require Docker or an Oteryn container;
- the repository-owned migration workflow was actually dispatched;
- no currently available self-hosted runner accepts either the specific migration job or the broad PR #281 probe.

DERIVED:
- after Synology rebuild/recreate, new official-client experiments can execute directly inside `synology-otclient-01` and keep durable runtime state in the runner work volume;
- deployment cannot currently be driven through GitHub Actions until some authorized execution channel to the Synology host is restored.

UNKNOWN:
- whether the Synology Docker host itself is powered on/reachable;
- why all repository self-hosted runners are currently offline/unregistered;
- whether `/volume1/docker/ot-runners/.env` already exists on the NAS;
- whether OTS remains available after eventual redeploy.

WAITING_ON:
- an authorized execution channel to the Synology Docker host: either any existing repository self-hosted runner comes online or direct NAS/SSH execution becomes available;
- deployment/recreate of the reviewed PR #280 stack;
- runner acceptance proof from PR #48.

BLOCKER:
- current ChatGPT environment exposes no SSH/Synology connector;
- GitHub integration cannot administer repository runner inventory/secrets (`403`);
- migration run `31686590850` cannot start because no self-hosted runner is currently available;
- broad PR #281 `runs-on: self-hosted` run `31643425060` is also queued, independently confirming the absence of an available repository self-hosted execution path.

next_action: restore one authorized Synology execution path, execute the already-reviewed PR #280 stack, require `synology-otclient-01` online with `tibia-re`, then immediately reconcile PR #48 bootstrap and continue structural login/world-entry proof on that runner
