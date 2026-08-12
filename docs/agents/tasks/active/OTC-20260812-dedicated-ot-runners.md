# OTC-20260812-dedicated-ot-runners

status: waiting
branch: ci/dedicated-ot-runners
base: main
pr: 280
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
- Registration uses a short-lived GitHub runner registration token obtained at container startup from an externally supplied GitHub credential; no credential is committed.
- The official runner image is pinned by immutable digest.
- The deployment documentation includes exact Synology commands, secret handling, update/restart procedure, validation commands, and example `runs-on` selectors.
- Existing runner stacks are not referenced as dependencies and are not mutated.
- Runtime registration must be proven on the target Synology host before merge readiness.

## Validation

Static validation on PR head before this checkpoint:
- full PR diff reviewed; changed paths are confined to this task record and `infra/ot-runners/**`;
- `bash -n` on the exact `entrypoint.sh` content: PASS;
- YAML parse of the exact `compose.yaml` content with PyYAML: PASS; both services and the intended capability list were resolved;
- official `ghcr.io/actions/actions-runner` image pin verified against GitHub Packages as runner `2.336.0`, digest `sha256:0cfdcc701ce933c6d243c6b0b2da767366dc9f2e99961d4c3754b0b78084cdda`;
- GitHub documentation verifies `--disableupdate` is supported for containerized self-hosted runners and that repository registration/remove tokens are short-lived API tokens;
- GitHub commit combined status for head `403c8275b04fe6083c2782fd14102df7ca427cd7`: no status checks reported.

Unavailable in the current execution environment:
- Docker CLI / `docker compose config`;
- Synology Docker host;
- target-host registration proof for `synology-otclient-01` and `synology-ots-01`.

## Durable state

PROVEN:
- `blakinio/otclient` and `blakinio/Otheryn` are accessible user-owned repositories.
- Open PR #48 owns existing `oteryn-staging` runtime work and remains untouched.
- Draft PR #280 contains the isolated runner stack.
- No `.github/workflows/**`, Freqtrade or Oteryn Platform runner paths are changed by PR #280.

UNKNOWN:
- Whether the target Synology host already contains a suitable GitHub credential for runner registration.
- Runtime outcome until Compose is executed on the Synology host.

WAITING_ON:
- target Synology execution of `docker compose config`, build, startup, log inspection and GitHub runner availability verification.

next_action: deploy `infra/ot-runners` on Synology and verify both repository runners become available before marking PR #280 ready
