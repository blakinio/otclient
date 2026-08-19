---
task_id: OTC-20260819-tibia-re-control-center-hardening
status: active
agent: ChatGPT
project_lane: otclient
lane: P0-DESIGN-HARDENING
track_id: official-client-re
task_kind: architecture_contract_hardening
risk: medium
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
transaction_authorized: false
initial_base_sha: 3e3b3a731cb21d775ae686c65991e90969bb86fb
implementation_pr: 605
owned_paths:
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
  - docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-hardening.md
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - canonical Track A lease/registration/Gate A/rebind/Gate B/whole-lifetime supervisor
  - tools/tibia_runtime_bridge/**
  - PR #592 Surveyor only after an accepted exact producer state
  - blakinio/Oteryn-v2 docs/architecture/ADR-0007-native-end-to-end-test-platform.md
depends_on:
  - merged Control Center design PR #600
  - merged audit-prompt PR #602
blocks:
  - Package A Control Center implementation until fresh independent re-audit reports no P0/P1 and PACKAGE_A_IMPLEMENTATION_READY=YES
external_repositories:
  - blakinio/Oteryn-v2 read-only architecture dependency
---

# TIBIA RE Control Center architecture hardening

## Objective

Harden the merged Control Center architecture, adapter contract and implementation/audit prompts against the fresh independent-audit findings before Package A implementation begins.

## Material closures implemented in PR #605

- Added normative `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`.
- Replaced advisory preflight authority with a defined final one-shot `commit_dispatch()` boundary.
- Added a fresh unique `backend_epoch` per backend restart plus scoped monotonic `control_generation`.
- Added a tiny local `dispatch_gate` shared by STOP and final dispatch commit; external Track A guard acquisition must occur without holding this local gate.
- Defined continuous official Track A guard ownership across final Track A checks, local durable dispatch commit and physical mutation.
- Added write-ahead `DISPATCH_COMMITTED/POSSIBLY_DISPATCHED` persistence plus storage durability barrier before physical mutation.
- Defined crash-after-commit-before-effect as conservative `AMBIGUOUS` unless authoritative no-effect reconciliation exists.
- Added globally unique `action_id`, normalized request hash, same-ID deduplication and conflicting-body refusal.
- Added explicit action lifecycle and no automatic retry after possible dispatch.
- Added side-effect ledger `limit/reserved/at_risk/committed/uncertain` with at-risk transition in the dispatch-commit transaction.
- Added typed scenario predicates and deterministic UNKNOWN behavior.
- Added pause/resume and backend/control/adapter/runtime/session fencing.
- Added multi-clock Recorder semantics: ingest/source timestamps, clock domain, source sequence/scope and ordering confidence.
- Preserved Track A causal-recorder fields explicitly and prohibited causal promotion from ingestion order alone.
- Added late-event and `ACTIVE -> CLOSING -> FINALIZED` semantics.
- Made construction-time secret exclusion mandatory; export-time redaction is defense in depth only.
- Added screenshot `SAFE/QUARANTINED/REJECTED` design boundary.
- Added metadata-only network capture with no raw fallback.
- Defined one loopback versioned Control API/domain path for browser and CLI with idempotency/bounds/backpressure.
- Split generic semantic capability support from official-only R0-R4/A0-A4 evidence maturity.
- Pinned future Surveyor integration by schema/version/producer commit/interface.
- Reconciled Oteryn v2 adapter with accepted ADR-0007 instead of creating a second Oteryn E2E authority.
- Added field-level semantic comparison classes and explicit coverage-gap outcomes.
- Reordered phases so Scenario Engine, Recorder primitives, durability model and fake adapter precede UI and all real mutation.
- Added the hardened Control Center contracts to `MODULE_CATALOG.md` and recorded the architecture change in `CHANGELOG.md`.
- Updated the now-merged #596 canonical adoption catalogue entry so future agents do not treat it as an active unmerged dependency.

## Falsification baseline

The hardened audit prompt requires 28 explicit race/retry/crash/privacy/cross-repo cases, including:

- authority loss at final commit;
- STOP versus dispatch commit;
- duplicate browser/CLI requests;
- response loss/retry;
- durability barrier failure;
- crash after durable commit before physical effect;
- stale callbacks across backend epoch restart;
- STOP while an action is blocked waiting for Track A guard;
- ambiguous budget consumption;
- multi-clock recorder ordering;
- screenshot/exception secret leakage;
- Surveyor schema drift;
- Oteryn production test-hook leakage.

## Safety

Documentation/contracts only. No Track A runtime observation/mutation, no client launch/control, no credentials, login or gameplay, and no writes to `blakinio/Oteryn-v2`.

## Repository reconciliation

The branch was reconciled with `main@a5cbdf1125887f8e5455dfbed5ee5a8e901f105c` through merge/reconciliation commit `bd498ecd827dbd5e9e32e493169abd41703e4a0e` after #596 and its closeout had landed. No Control Center semantic conflict was found; the design continues to consume then-current trusted-base Track A authority dynamically rather than pin the adoption implementation.

Surveyor #592 was rechecked and remained an open Draft at `90fb32f69173a6e621dfe6bd34c6f2e494076655`; Package C therefore remains schema/producer-pinned and blocked on an accepted exact Surveyor state.

## Validation state

Draft PR #605 exists. Current intended changed-file set is exactly the five Control Center programme/contract/prompt paths, `MODULE_CATALOG.md`, `CHANGELOG.md`, and this task record.

Before readiness:

1. recheck/reconcile any newer `main` movement that can affect the design;
2. inspect the exact final changed-file set and full diff;
3. run repository-required docs/governance checks on the exact final head;
4. perform full self-review;
5. obtain a genuinely fresh independent re-audit of the exact final hardening head; this implementing session cannot self-label its own review independent;
6. only if the independent result has no P0/P1 and `PACKAGE_A_IMPLEMENTATION_READY=YES`, proceed to readiness/merge under repository policy.

## Next action

Revalidate current `main` and exact PR #605 head, run exact-head repository checks, then hand the exact unchanged head to a fresh independent Control Center audit.