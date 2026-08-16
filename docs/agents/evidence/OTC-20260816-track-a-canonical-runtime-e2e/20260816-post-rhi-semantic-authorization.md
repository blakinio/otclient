# Post-RHI X11 window-state semantic authorization checkpoint

## Trusted base

`main@b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4`

The base was re-read immediately before this checkpoint and is unchanged from the task admission base.

## Pre-runtime hosted gates

Exact pre-authorization head: `40ab1f9fd23e51d1b331c551fed6c5c7348f3f51`.

- hosted transformer preflight: workflow run `31972122188`, job `95226051394` = `SUCCESS`;
- Track A runtime governance: run `31972122158`, both fresh-admission and deterministic-policy jobs = `SUCCESS`;
- repository CI: run `31972122304`, `CI / Required` job `95226208461` = `SUCCESS`;
- physical post-RHI job: `SKIPPED` in every pre-authorization generation;
- actionlint/yamllint: `SUCCESS` on the PR-marker gated workflow;
- immutable source harness blob: `1616edcc982be50ef2c95b8077160ec8fe9291fe`;
- exact official-client fence: SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`, size `51965216`.

## Authorized semantic scope

The PR body now contains `POST_RHI_PHYSICAL_EXECUTION_ENABLED=true`. This checkpoint commit intentionally creates exactly one `pull_request/synchronize` generation in which the physical job may run.

The physical job must:

1. wait for the hosted transformer preflight in the same workflow generation;
2. re-run deterministic Track A admission on the exact semantic head immediately before the runtime boundary;
3. refuse if the PR base SHA is not exactly `b9260379bebfba8e0e8d8a45c63e24ea65b9c6e4`;
4. use only the task-owned `ephemeral_isolated` namespace;
5. launch the exact fenced client once, with no credentials/login/gameplay and no client backend forcing;
6. bind contained `LIBGL_DRIVERS_PATH` only to Xvfb;
7. collect X11 map-state tree, bounded task-owned thread wait channels, and the broader redacted post-RHI log discriminator;
8. clean up completely;
9. stop after the first valid semantic classification; no retry is authorized.

Canonical lease/registration/session state remains out of scope. A successful isolated discriminator does not itself authorize canonical bootstrap.
