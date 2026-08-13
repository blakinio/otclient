# OTCLIENT-TIBIA-RE canonical repository/runtime wrapper

```yaml
prompt_contract_version: 1.1.0
alias: OTCLIENT-TIBIA-RE
repository: blakinio/otclient
base_prompt: docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
canonical_runner_name: synology-otclient-01
canonical_runner_selector:
  - self-hosted
  - otclient
  - synology
canonical_state_dir: /home/runner/_work/_otclient_tibia_re_state
policy_version: 2
prompting_standard_version: 2.1
```

## Resolution contract

Load and obey `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md` in full. This wrapper is an additive runtime/ownership override for the current programme consolidation. If the base prompt names an old runner/container/repository as a historical lead, this wrapper determines where **new active work** runs.

The owner command is:

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
```

Do not require a task named `docs/agents/tasks/active/OTCLIENT-TIBIA-RE.md`, a branch named `agent/otclient-tibia-re`, or a dedicated `workflow_dispatch` operation merely to resolve the alias.

## Canonical ownership

All new programme coordination, durable state, tooling, reports, workflows and implementation belong in:

```text
blakinio/otclient
```

Current implementation lanes to discover and reuse rather than duplicate:

```text
PR #48  official-client runtime/login/recovery and live experiments
PR #279 fail-closed worldmap/OTBM reconstruction pipeline
PR #280 dedicated OTClient/OTS Synology runner infrastructure
PR #283 stable non-GDB runtime bridge
```

Revalidate their exact heads/states before use. When any lane merges or becomes superseded, continue from current `main` and its durable task records rather than preserving stale PR numbers as authority.

## Canonical runtime

New live `OTCLIENT-TIBIA-RE` experiments must use the dedicated repository runner:

```yaml
runner_name: synology-otclient-01
migration_selector: [self-hosted, otclient, synology]
post_deploy_preferred_selector: [self-hosted, Linux, X64, otclient, tibia-re, synology]
persistent_state: /home/runner/_work/_otclient_tibia_re_state
```

The broader migration selector is allowed while PR #280 is being redeployed and the `tibia-re` label may not yet be present. Once the updated runner image is proven deployed, prefer the stricter selector.

Do not schedule new programme experiments on:

```text
oteryn-staging
oteryn-synology-staging
oteryn-tibia-client-analysis
/var/lib/oteryn-staging-state/**
```

Those names may remain in historical evidence. They are not active runtime dependencies for the canonical programme.

The dedicated OTClient runner executes the client/tools directly. Do not require Docker-in-Docker or a host Docker socket for normal RE experiments. PR #280 owns the image dependencies and runner lifecycle; PR #48 owns live runtime experiments.

If the dedicated runner is temporarily unavailable, persist `WAITING` for runner-dependent experiments and continue other independent READY repository work such as static analysis, bridge/tooling, OTBM pipeline work, evidence normalization or update-resilience work. Do not silently fall back to an Oteryn runner.

## External evidence migration

`blakinio/Oteryn-Platform` is read-only historical evidence for this programme. Do not mutate it from an OTClient task unless the owner separately authorizes that exact repository write.

Use the repository-owned consolidated evidence first:

```text
docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
```

Only fetch the external source again when the consolidated record lacks a material detail or provenance must be reverified.

Historical external runtime addresses/PIDs are evidence tied to their exact binary/process and must never be reused as current runtime values. Static offsets/signatures may be leads only after current binary SHA verification.

## Durable-state precedence

For continuation, resolve state in this order:

1. root/nested repository governance;
2. live `main`, PRs, checks and ownership;
3. current active task checkpoints in `blakinio/otclient`;
4. this canonical wrapper and the base programme prompt;
5. repository-owned consolidated evidence/report files;
6. external Oteryn reports as read-only historical evidence;
7. chat history.

No material continuation fact may remain only in chat.

## Current migration acceptance

Before treating the runtime migration as complete, prove all of the following:

```text
- PR #280 exact runner image/Compose validation passes;
- updated Synology OTClient runner is deployed and registered;
- PR #48 job is accepted by synology-otclient-01;
- persistent OTClient state path is writable;
- no active experiment uses oteryn-staging state/runner/container;
- current official-client version/SHA is reverified;
- live structural IN_GAME recovery resumes from OTClient-owned runtime.
```

Until then, classify the runner migration accurately as `WAITING` or `VALIDATING`, not `DONE`.

## Owner-funded AI restriction

Do not use the owner's Codex quota, OpenAI API quota, paid AI review quota, personal access tokens, private model/API credentials or other owner-funded AI allowance unless the owner separately and explicitly authorizes that exact use for this task.

Availability is not authorization.

## Continuation

After this wrapper is resolved, execute the base programme autonomously from the latest durable `next_action`. A workflow completion, commit, PR, logout, disconnect, failed hypothesis or worker rotation is not by itself a programme stop condition.
