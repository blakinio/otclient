# OTCLIENT-TIBIA-RE — live Synology runner deployment attempt

Date: 2026-08-13
Repository: `blakinio/otclient`
Owner lane: PR #280 / `ci/dedicated-ot-runners`

## Objective

Deploy the reviewed dedicated OTClient runner stack on the Synology Docker host so PR #48 can perform the official-client login/world-entry experiment on `synology-otclient-01` instead of any historical Oteryn runtime.

## Attempt

A one-time infrastructure-only bridge workflow was added at:

```text
.github/workflows/otclient-runner-synology-migrate.yml
```

Commit:

```text
19b567e993bd72432f75572a0be3f214e4db787d
```

The workflow deliberately does **not** run Tibia or any live reverse-engineering experiment on the historical runner. Its only purpose is to use a previously task-proven Synology Docker-socket runner as a migration control plane to build/recreate the dedicated `otclient-runner` service from `infra/ot-runners/**`.

It is fail-closed around credentials: token values are never printed or committed. It searches only existing Synology runner configuration, validates a candidate credential against the repository runner-registration endpoint, persists the target `.env` only on the NAS with mode `0600`, deploys only `otclient-runner`, and requires GitHub to report exact runner `synology-otclient-01` online with labels:

```text
self-hosted,Linux,X64,otclient,synology,tibia-re
```

Migration workflow run:

```yaml
run: 31686590850
job: 94403975354
head: 19b567e993bd72432f75572a0be3f214e4db787d
selector: [self-hosted, oteryn-staging]
status_after_two_bounded_observations: queued
```

Per anti-stall policy the same pending state was not polled further.

## Independent self-hosted availability evidence

PR #281 already contains a deliberately broad temporary probe using:

```yaml
runs-on: self-hosted
```

Its latest probe run is also still queued:

```yaml
run: 31643425060
head: 91ef11ee8ad02df8c60f9c4f17b1e1ec3d3c6c0e
status: queued
created_at: 2026-08-12T21:38:10Z
```

Therefore this is not merely a wrong `oteryn-staging` label. The live GitHub evidence shows that `blakinio/otclient` currently has no available self-hosted runner capable of accepting even an unqualified `self-hosted` job.

## Canonical consumer state

PR #48 canonical bootstrap remains queued awaiting the dedicated OTClient runner:

```yaml
run: 31679097113
job: 94380204633
workflow: OTClient Tibia RE runner bootstrap
selector: [self-hosted, otclient, synology]
status: queued
```

No login/world-entry experiment was moved back to Oteryn. No proprietary client binary or credentials were persisted in Git.

## Classification

PROVEN:
- reviewed OTClient runner image/Compose build validation already passes in PR #280;
- the canonical PR #48 bootstrap is ready to consume the dedicated runner;
- a repository-owned migration workflow was created and dispatched;
- both the specific migration selector and the broad historical PR #281 `self-hosted` probe have no available runner at the observed time.

DERIVED:
- deployment cannot be driven through GitHub Actions until at least one existing self-hosted Synology runner is online, or an independent authorized NAS/SSH execution channel becomes available.

UNKNOWN:
- why all repository self-hosted runners are currently offline/unregistered;
- whether the Synology Docker host itself is powered on and reachable;
- whether `/volume1/docker/ot-runners/.env` already exists on the NAS.

BLOCKER:
- no live execution channel currently reaches the Synology Docker host: no repository self-hosted runner accepts jobs, the current ChatGPT environment exposes no SSH/Synology connector, and the GitHub integration cannot administer repository runners/secrets (`403`).

NEXT_ACTION:
- restore any authorized execution channel to the Synology host (prefer bringing the existing repository runner online or direct NAS/SSH access), then execute the already-reviewed PR #280 stack; once `synology-otclient-01` is online, immediately reconcile PR #48 bootstrap and continue structural login/world-entry proof on that runner.
