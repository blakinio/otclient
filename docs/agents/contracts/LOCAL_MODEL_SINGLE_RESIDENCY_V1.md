# Local Model Single-Residency Contract v1

```yaml
contract_id: LOCAL-MODEL-SINGLE-RESIDENCY-V1
version: 1.0
status: normative
scope: repository-local model execution
runtime_authority: none
```

## Purpose

Bound local CPU/RAM/VRAM pressure and prevent competing model sessions from saturating the same physical host or GPU pool. This is a resource-safety contract, not a model-quality or authority contract.

## Invariant

For one physical host/shared GPU pool:

```text
resident_or_inferencing_local_models <= 1
```

Workers may perform non-model preparation in parallel. Actual local model residency/inference is serialized.

## Preflight

Before every local inference session:1. resolve the exact target model/tag/digest when available;
2. query the provider's current resident-model state;
3. continue only if the resident set is empty or contains exactly the target model;
4. refuse when a different model is resident, more than one model is resident, or state cannot be established.

For Ollama, `ollama ps` or `/api/ps` is the canonical local residency observation. Provider errors/timeouts are `UNKNOWN` and fail closed.

## Model switching

Switching models is always sequential:

```text
finish/cancel model A
-> request unload model A
-> verify model A is no longer resident
-> load/invoke model B
```

Do not overlap warm-up, inference or keep-alive windows for two models. Multi-model benchmarks, ensembles, audits and voting must use the same sequence.

## Session lifecycle

- use bounded keep-alive; default implementations should prefer short residency;
- session exit requests deterministic/best-effort unload;
- if unload cannot be verified, do not load a different model on that host/GPU pool;
- task closeout/handoff records any unresolved resident model and attempts to release task-loaded models when practical.
## Failure behavior

The following are fail-closed for starting a new/different model:

- multiple resident models;
- unexpected resident model;
- provider residency query unavailable/ambiguous;
- previous model unload not verified.

Do not solve resource contention by interfering with unrelated tasks or weakening another task's ownership. Record the blocker instead.

## Authority boundary

This contract controls resource residency only. It does not authorize credentials, paid model quota, shell/process control beyond the task-owned model session, official-client access, Track A mutation, merge, promotion, or acceptance of model output. Existing repository AI funding/credential rules and task-specific safety gates remain authoritative.

## Acceptance tests

Implementations that manage local models should prove at minimum:

1. empty resident set admits target;
2. exact target alone admits reuse;
3. different resident model refuses;
4. multiple resident models refuse;
5. residency-query failure refuses;
6. model switch unloads/verifies A before invoking B;
7. session exit requests unload;
8. bounded keep-alive is enforced.

PR #615 contains an experimental compatible `MAX_ONE_LOADED_MODEL` implementation; that blocked PoC is not promoted by this contract.
