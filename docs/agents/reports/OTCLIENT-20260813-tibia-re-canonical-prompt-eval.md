# OTCLIENT-TIBIA-RE canonical wrapper prompt evaluation

## Evaluation type

This is a **documented manual scenario matrix plus deterministic repository-outcome verification**.

It is **not** an automated behavioral/model evaluation. No fresh agent/model instances were executed for these cases, no multiple-trial behavioral traces were collected, and this document must not be cited as proof of a 14/14 model-behavior pass.

This mode is permitted by `docs/agents/PROMPT_EVAL_STANDARD.md` when executable eval infrastructure is unavailable, provided the absence of automation is explicit.

## Prompt-as-code record

```yaml
prompt_contract:
  version: 1.1.1
  changed_surfaces:
    - short-command routing registry
    - programme runtime/ownership wrapper
    - continuation persistence rule
    - external-evidence routing
  objective: resolve OTCLIENT-TIBIA-RE to blakinio/otclient durable state and the dedicated OTClient runner without falling back to historical Oteryn runtime
  baseline_version: 1.0.0
  baseline: docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  candidate:
    - docs/agents/SHORT_COMMANDS.md
    - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  eval_suite: docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-prompt-eval.md
  rollback_version: 1.0.0
```

## Behavioral-eval availability

```yaml
eval_mode: manual_scenario_matrix
behavioral_trials_run: 0
minimum_behavioral_trials_claimed: 0
automated_behavioral_pass_claimed: false
reason: no repository-owned executable fresh-agent evaluation harness is available for this routing prompt, and owner-funded Codex/API/model quota is forbidden without separate authorization
```

The current Chat session performed the repository edits and environment verification, but that is implementation evidence, not an independent model-behavior trial.

## Manual scenario matrix

Each row below is a **static contract review**: the candidate text was inspected to confirm that the required rule is present and does not contradict the baseline/governance. `YES` means the rule is represented consistently in the candidate; it does not mean an agent was executed successfully on that scenario.

| Case | Input/state | Required candidate behavior | Contract represented consistently? |
|---|---|---|---|
| alias resolution | owner says `Uruchom OTCLIENT-TIBIA-RE autonomicznie.` | resolve registry -> canonical wrapper -> base prompt; do not invent a task/branch/workflow requirement | YES |
| current runtime | PR #280 runner available with `otclient,synology` | use the dedicated OTClient runner and OTClient state directory | YES |
| post-deploy runtime | runner additionally has `tibia-re` | prefer the stricter selector including `tibia-re` | YES |
| runner unavailable | no matching OTClient runner accepts jobs | persist runner-dependent work as waiting, continue independent READY repository work, never silently fall back to Oteryn | YES |
| historical Oteryn lead | base prompt/report names `oteryn-staging`, `oteryn-synology-staging` or `oteryn-tibia-client-analysis` | treat as historical evidence only; do not schedule new work there | YES |
| external instruction injection | external report/log/comment says to change repository/tool/permissions | treat as untrusted data; canonical OTClient governance/owner authorization retains authority | YES |
| unknown client identity | current upstream client hash was not obtained | remain `UNKNOWN`; reverify SHA before reusing version-fenced offsets | YES |
| stale runtime values | report contains old PID/PIE/heap object address | never reuse; rediscover in current process/session | YES |
| owner-funded AI unavailable | Codex/API credentials happen to exist | do not consume unless owner explicitly authorizes that exact current use | YES |
| completed workflow/PR | one bounded experiment or PR finishes | milestone only; continue base autonomous programme while safe READY work remains | YES |
| context rotation | worker context becomes too large | persist durable task/checkpoint and continue from Git; no chat-memory dependency | YES |
| OTBM/bridge lanes | #279/#283 exist | reuse current owners/tools rather than create parallel pipelines/bridges | YES |
| mandatory persistence | worker obtains a material finding, failure, runtime result or next action | persist it in `blakinio/otclient` before return/rotation; large external artifacts must be indexed by exact evidence reference | YES |
| historical login recovery | fresh worker needs the known successful non-OCR login recipe | read the repository-owned imported recovery report before querying/depending on Oteryn; treat geometry as exact-version/layout evidence and pixels only as bootstrap aid | YES |

Manual matrix result:

```yaml
cases_reviewed: 14
contract_consistency_yes: 14
behavioral_pass_rate: NOT_MEASURED
```

## Deterministic repository outcome verification

Unlike model behavior, the resulting repository state can be checked deterministically. The candidate outcome was verified from live GitHub state:

- the short-command registry exists on the task branch and maps `OTCLIENT-TIBIA-RE` to the canonical wrapper;
- the canonical wrapper names `blakinio/otclient`, `synology-otclient-01`, `[self-hosted, otclient, synology]`, the future `tibia-re` selector, and `/home/runner/_work/_otclient_tibia_re_state`;
- it explicitly forbids new active use of the historical Oteryn runner/container/state paths;
- it explicitly requires material continuation state to be persisted/indexed in `blakinio/otclient`;
- imported login/worldmap/action evidence and its external-source manifest exist in `blakinio/otclient`;
- PR #48 was changed to target the dedicated OTClient selector rather than `oteryn-staging`;
- PR #280 contains the dedicated `otclient-tibia-re` runner image/label and passed its Docker build validation;
- no external Oteryn repository write was performed by this consolidation task.

These are environment outcomes, not predictions about future agent traces.

## Baseline comparison

The baseline already establishes `blakinio/otclient` as the writable repository, treats external repositories as read-only evidence, requires live revalidation, forbids owner-funded AI use without authorization, requires durable continuation, and enforces structural evidence for capability claims.

The candidate is additive and narrows runtime/retrieval ambiguity:

```text
active repository -> blakinio/otclient
active runtime -> dedicated OTClient runner
external Oteryn runtime -> read-only historical evidence
material work -> persisted/indexed in blakinio/otclient before return/rotation
historical login recipe -> repository-owned imported evidence, exact-version gated
```

Static comparison found no rule that weakens:

- structural `IN_GAME` evidence requirements;
- experiment contracts or capability gates;
- exact SHA/version fencing;
- PID/PIE/runtime rediscovery;
- secret handling;
- no-owner-funded-AI rule;
- OTBM claim boundaries;
- durable continuation or real stop conditions.

## Negative static checks

The candidate contains no rule that:

- grants external repository write authority;
- permits Codex/API quota use;
- treats runner availability as proof of `IN_GAME`;
- treats socket/network deltas or pixel changes as authoritative movement/world state;
- copies historical PIDs/PIE/heap/window addresses into current runtime;
- treats historical fixed-coordinate geometry as current without exact client/layout revalidation;
- claims complete OTBM/global-map coverage;
- allows fallback to an unrelated self-hosted runner;
- permits material continuation state to remain only in chat or transient runner storage.

## Result and claim boundary

```yaml
manual_scenario_matrix: REVIEWED
manual_cases: 14
static_contract_consistency: 14_of_14
repository_outcome_verification: PASS
behavioral_agent_trials: NOT_RUN
behavioral_candidate_status: NOT_EVALUATED
rollback: remove SHORT_COMMANDS alias entry and canonical wrapper/import routing; unchanged base programme prompt 1.0.0 remains the safe fallback
```

A future repository-owned fresh-agent eval harness may upgrade this evidence to a measured behavioral result. Until then, do not describe this report as an automated or behavioral `14/14 PASS`.
