# OTCLIENT-TIBIA-RE canonical repository/runtime wrapper

```yaml
prompt_contract_version: 1.2.0
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
track_a_runtime_agent_admission_version: 1
```

## Resolution contract

Load and obey `docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md` in full. This wrapper is an additive runtime/ownership override for the current programme consolidation. If the base prompt names an old runner/container/repository as a historical lead, this wrapper determines where **new active work** runs.

The owner command is:

```text
Uruchom OTCLIENT-TIBIA-RE autonomicznie.
```

Do not require a task named `docs/agents/tasks/active/OTCLIENT-TIBIA-RE.md`, a branch named `agent/otclient-tibia-re`, or a dedicated `workflow_dispatch` operation merely to resolve the alias.

## Mandatory Track A runtime admission

Before a Track A worker claims, resumes, observes, creates, reuses, controls, or mutates an official-client runtime, it MUST read and apply:

```text
docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
```

The worker must classify `runtime_access` as exactly one of:

```text
none
read_only
ephemeral_isolated
canonical_reuse_or_mutation
canonical_bootstrap
canonical_rebind
canonical_recovery
```

At task claim/resume/checkpoint, persist the complete admission record required by that contract; static/no-runtime work records `runtime_access: none`. Re-evaluate and re-persist admission before the first runtime-related operation and after any material authority/identity change.

`read_only` live observation additionally requires a freshly proven non-conflicting target/namespace/ownership boundary and `target_uniqueness: PROVEN`; otherwise refuse live observation and continue only `none` static/artifact work.

For ordinary canonical reuse/mutation, `mutation_authorized: true` is legal only after current Gate A passes, any required generation rebind passes, Gate B passes on the one authoritative registration, and the mutation remains inside the final PR #321 cancellation-safe whole-lifetime supervisor. Missing registration does not fall through to reuse and requires the separate bootstrap transition. Registration/lease-generation mismatch with unchanged runtime identity does not fall through to reuse and requires the dedicated reviewed rebind transition. A stale registered PID/start pair with one fully proven current same-fence singleton target routes only to reviewed `canonical_recovery`, never rebind. Manual editing of `runtime-registration.json` is never a substitute.

Until direct current evidence proves otherwise, preserve exactly:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Historical `:98`, reachable `6082`, an old PID/session, a task/PR statement, or standalone lease validation is discovery evidence only and never current mutation authority. `UNKNOWN`, `REQUIRED_NOT_PROVEN`, `REQUIRED_UNAVAILABLE`, or `REQUIRED_UNIMPLEMENTED` on a required admission gate means refuse that mutation and continue only unrelated safe work.

Task-owned ephemeral runtimes remain allowed only inside a freshly proven unique namespace. A unique X11 display does not create a second Global session or canonical authority. Do not mutate or live-observe PR #303-owned runtime surfaces, or Track B state, through this wrapper.

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

## Mandatory repository persistence

All material work performed for this programme must be persisted in `blakinio/otclient` during the same bounded worker session or before rotation/return.

This includes, where applicable:

```text
- discoveries and disproven hypotheses;
- experiment contracts and results;
- run/job/artifact identifiers;
- binary versions/hashes and resolver outputs;
- code, scripts, tools and tests;
- workflow/runtime changes;
- protocol/action/state catalogues;
- OTBM findings and mappings;
- capability matrix changes;
- runner/runtime state and recovery procedures;
- blockers, UNKNOWN/CONFLICT classifications;
- handovers, checkpoints and exactly one executable next_action.
```

Do not leave material continuation state only in chat, local scratch space, a transient runner filesystem, an external repository, or an unreferenced Actions log/artifact. Large binary/log/trace artifacts may remain outside Git when repository policy requires it, but their provenance, semantic result, exact run/job/artifact ID and continuation consequence must be indexed from `blakinio/otclient`.

Do not create new active durable programme state in another repository. External repositories may be read for evidence only unless the owner separately authorizes a different exact write target.

Before returning `ROTATE`, `WAITING`, `BLOCKED` or `DONE`, verify that every material fact needed by a fresh agent is recoverable from `blakinio/otclient` plus explicitly referenced evidence.

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
