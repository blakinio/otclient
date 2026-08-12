# OTC-20260812-dedicated-ot-runners

status: active
branch: ci/dedicated-ot-runners
base: main
feature_scope: infrastructure
completion_claim: internal_only

## Objective

Provide a dedicated Synology-hosted GitHub Actions runner stack for OTClient and OTS work so these jobs do not consume the Freqtrade or Oteryn Platform runners.

## Ownership

owned_paths:
- infra/ot-runners/**
- docs/agents/tasks/active/OTC-20260812-dedicated-ot-runners.md

modules_touched: []
reuses:
- official GitHub Actions runner container image

depends_on: []
blocks: []
cross_repository_tasks:
- blakinio/Otheryn: runner target only; no repository mutation in this task

## Coordination

- PR #48 remains the owner of its existing official-Tibia runtime workflow paths and `oteryn-staging` execution path.
- This task does not edit `.github/workflows/**` and does not modify the existing `oteryn-staging`, Freqtrade, or Oteryn Platform runner services.
- `otclient-runner` registers only to `blakinio/otclient`.
- `ots-runner` registers only to `blakinio/Otheryn`.
- No owner-funded AI/Codex/OpenAI quota may be used.

## Acceptance inventory

- One Compose project defines two independent runner services with separate persistent state/work volumes.
- Each service has a unique runner name and dedicated label set.
- Registration uses a short-lived GitHub runner registration token obtained at container startup from an externally supplied GitHub PAT; no token is committed.
- The runner image is pinned by immutable digest.
- The deployment documentation includes exact Synology commands, secret handling, update/restart procedure, validation commands, and example `runs-on` selectors.
- Existing runner stacks are not referenced as dependencies and are not mutated.

## Validation

pending

## Durable state

PROVEN:
- `blakinio/otclient` and `blakinio/Otheryn` are accessible user-owned repositories.
- Open PR #48 owns existing `oteryn-staging` runtime work and must remain untouched.

UNKNOWN:
- Exact Synology filesystem location chosen by the owner for the new Compose project.
- Whether a suitable GitHub PAT is already stored on the NAS.

next_action: add and validate the isolated runner stack files
