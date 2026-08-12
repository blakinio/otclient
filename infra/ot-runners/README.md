# Dedicated OT runners

This Compose project runs two isolated repository-level GitHub Actions runners on the same Docker host:

- `otclient-runner` -> `blakinio/otclient`, labels `self-hosted`, `Linux`, `X64`, `otclient`, `ot`, `synology`;
- `ots-runner` -> `blakinio/Otheryn`, labels `self-hosted`, `Linux`, `X64`, `ots`, `otheryn`, `ot`, `synology`.

It is independent of the Freqtrade, Oteryn Platform and existing `oteryn-staging` runner stacks. No Docker socket is mounted by default.

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

## Workflow selectors

OTClient jobs intended for this runner should use:

```yaml
runs-on: [self-hosted, Linux, X64, otclient, synology]
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

The stack does not mount `/var/run/docker.sock`, does not run privileged, drops Linux capabilities and enables `no-new-privileges`. If a future workflow genuinely requires Docker builds, add that capability as a separate reviewed change rather than broadening these runners by default.

The state volumes contain GitHub runner registration state and the work volumes can contain repository material and job leftovers. Treat both as private NAS data.
