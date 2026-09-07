# Dedicated OT runners

This Compose project runs isolated repository-level GitHub Actions runners on the same Synology Docker host:

- `otclient-runner` -> `blakinio/otclient`, labels `self-hosted`, `Linux`, `X64`, `otclient`, `ot`, `synology`, `tibia-re`;
- `ots-runner` -> `blakinio/Otheryn`, labels `self-hosted`, `Linux`, `X64`, `ots`, `otheryn`, `ot`, `synology`.

It is independent of the Freqtrade, Oteryn Platform and historical `oteryn-staging` runner stacks. No Docker socket is mounted and neither runner is privileged.

The OTClient image uses the `otclient-tibia-re` Docker build target. It bakes in the Linux/X11/Vulkan/GDB/Qt/proxychains/pyelftools dependencies already exercised by the official Tibia analysis workflows, so runtime jobs can execute directly in the repository runner without `sudo`, Docker-in-Docker or an Oteryn-owned container.

## Canonical OTCLIENT-TIBIA-RE runtime

The durable programme is owned by `blakinio/otclient`. New live `OTCLIENT-TIBIA-RE` experiments must run on the dedicated OTClient runner, not on `oteryn-staging`.

After the updated runner image is deployed, the preferred selector is:

```yaml
runs-on: [self-hosted, Linux, X64, otclient, tibia-re, synology]
```

During the migration/bootstrap itself, `[self-hosted, otclient, synology]` is accepted so the currently registered dedicated runner can prove its identity before the new `tibia-re` label is present.

Persistent programme state lives outside a repository checkout but inside the OTClient runner work volume:

```text
/home/runner/_work/_otclient_tibia_re_state
```

That path is backed by `otclient_runner_work`. It is the canonical location for task-owned runtime/cache/checkpoint material that must survive individual jobs and runner-container recreation. Do not use `/var/lib/oteryn-staging-state/**` for new OTClient work.

External Oteryn repositories/runtimes may be consulted only as read-only historical evidence unless the owner separately authorizes work there.

## Authentication

The Compose project expects `GITHUB_RUNNER_PAT` to be supplied only through a local `.env` file on the NAS. Use a repository-scoped GitHub credential authorized for runner registration for both target repositories. Do not commit the populated `.env` file.

At startup the entrypoint exchanges this credential for GitHub's short-lived runner registration token. At shutdown it attempts the equivalent remove-token flow.

## Synology deployment

Use a dedicated directory rather than an existing runner directory:

```sh
mkdir -p /volume1/docker/ot-runners
cd /volume1/docker/ot-runners
```

Copy `Dockerfile`, `entrypoint.sh`, `compose.yaml`, `.env.example` and this README into that directory. Then create the local environment file:

```sh
cp .env.example .env
chmod 600 .env
vi .env
```

Set `GITHUB_RUNNER_PAT`. Runner names can stay at their defaults unless those names already exist in GitHub.

Validate and start:

```sh
docker compose config
docker compose build --pull
docker compose up -d
docker compose ps
docker compose logs --tail=100 otclient-runner
docker compose logs --tail=100 ots-runner
```

Both logs must complete registration and show that the runner is listening for jobs. In GitHub, each target repository's Actions / Runners page must show the matching runner as available.

For the OTClient runner additionally verify the baked Tibia-RE tools:

```sh
docker compose exec otclient-runner bash -lc 'command -v gdb; command -v Xvfb; command -v proxychains4; command -v xdotool; python3 -c "import elftools,yaml"'
```

## Workflow selectors

General OTClient jobs intended for this runner should use:

```yaml
runs-on: [self-hosted, Linux, X64, otclient, synology]
```

Official-client/Tibia-RE jobs should use the stricter post-deploy selector:

```yaml
runs-on: [self-hosted, Linux, X64, otclient, tibia-re, synology]
```

Otheryn/OTS jobs intended for its runner should use:

```yaml
runs-on: [self-hosted, Linux, X64, ots, synology]
```

Do not use only `self-hosted` for dedicated jobs because that could schedule them on unrelated self-hosted runners.

## Operations

Restart one runner without affecting the other:

```sh
docker compose restart otclient-runner
# or
docker compose restart ots-runner
```

The runner is registered with `--disableupdate`. Update the pinned runner image deliberately by changing the digest in `Dockerfile`, reviewing the upstream runner release, rebuilding and recreating the services.

Stop the stack with:

```sh
docker compose down
```

Do not add `-v` unless the state and work volumes are intentionally being deleted.

## Security boundary

The stack does not mount `/var/run/docker.sock` and does not run privileged. It drops the default Linux capability set, adds back only `CHOWN`, `SETUID` and `SETGID` so the root bootstrap can initialize named-volume ownership and then immediately drops to the unprivileged `runner` user, and enables `no-new-privileges`.

The OTClient/Tibia-RE dependencies are installed into the image at build time. Runtime jobs do not require privilege escalation. If a future workflow genuinely requires host Docker access, add that capability as a separate reviewed change rather than broadening these runners by default.

The state volumes contain GitHub runner registration state and the work volumes can contain repository material and job leftovers. Treat both as private NAS data.
