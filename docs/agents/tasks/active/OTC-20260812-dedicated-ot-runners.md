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
- docs/agents/tasks/active/OTC-20260812-dedicated-ot-runners.md

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
- [x] No Docker socket or privileged mode is introduced.
- [x] `docker compose config` and both Docker build targets pass on a real Docker engine for exact implementation head `e97cf8be1b2a8c63cecc39e07d0347830b874d5f`.
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

The temporary validation workflow is evidence scaffolding only and should be removed before final PR closeout; run `31679256871` remains the supporting exact-implementation evidence after removal.

Target-NAS registration proof is still required because GitHub repository runner inventory cannot be read by the current integration (`403 Resource not accessible by integration`).

## Durable state

PROVEN:
- all programme code/state being consolidated is in `blakinio/otclient` branches/PRs;
- the runner stack is repository-scoped and independent of Oteryn Platform/Freqtrade infrastructure;
- the declarative OTClient runner has a Tibia-RE-specific image target and label;
- the OTClient Tibia-RE image and Compose configuration build/validate successfully on a real Docker engine;
- PR #48 has a consumer migration path that does not require Docker or an Oteryn container.

DERIVED:
- after Synology rebuild/recreate, new official-client experiments can execute directly inside `synology-otclient-01` and keep durable runtime state in the runner work volume.

UNKNOWN:
- whether the target NAS has deployed the updated PR #280 stack;
- whether the target runner currently has the new `tibia-re` label;
- whether OTS remains available after redeploy.

WAITING_ON:
- authorized deployment/recreate of the updated stack on the Synology Docker host;
- runner acceptance proof from PR #48.

BLOCKER:
- final deployment to the Synology Docker host cannot be performed through the currently available GitHub connector; no authorized NAS/SSH execution tool is available in this session.

next_action: remove temporary validation workflow, then deploy/recreate the PR #280 stack on Synology and prove PR #48 run 31679097113 or a fresh exact-head equivalent is accepted by `synology-otclient-01`
