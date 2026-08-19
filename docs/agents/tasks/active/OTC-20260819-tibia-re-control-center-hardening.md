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
base_sha: 3e3b3a731cb21d775ae686c65991e90969bb86fb
owned_paths:
  - docs/agents/programs/TIBIA_RE_CONTROL_CENTER_E2E.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_MVP.md
  - docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_INDEPENDENT_AUDIT.md
  - docs/agents/tasks/active/OTC-20260819-tibia-re-control-center-hardening.md
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - canonical Track A lease/registration/Gate A/rebind/Gate B/whole-lifetime supervisor
  - tools/tibia_runtime_bridge/**
  - PR #592 Surveyor only after an accepted exact producer state
depends_on:
  - merged Control Center design PR #600
  - merged audit-prompt PR #602
blocks:
  - Package A Control Center implementation until P1 audit gaps are closed
external_repositories:
  - blakinio/Oteryn-v2 read-only architecture dependency
---

# TIBIA RE Control Center architecture hardening

## Objective

Harden the merged Control Center architecture, adapter contract and implementation/audit prompts against the independent-audit findings before Package A implementation begins.

## Required closures

- atomic final-dispatch authority/cancellation fence;
- linearizable STOP ALL semantics;
- idempotency/replay/duplicate-request handling;
- explicit in-flight/ambiguous action lifecycle and restart recovery;
- enforceable conservative side-effect accounting;
- typed deterministic scenario/predicate semantics;
- multi-source causal event ordering without false total-order claims;
- construction-time secret rejection and screenshot quarantine;
- browser/CLI single-backend semantics and bounded API rules;
- Surveyor schema pinning;
- Oteryn v2 ADR-0007 integration without a second E2E authority;
- field-level differential comparison semantics;
- Package A fake-adapter acceptance with zero Track A runtime access.

## Safety

Documentation/contracts only. No Track A runtime observation or mutation, no client launch/control, no credentials, login or gameplay, and no writes to `blakinio/Oteryn-v2`.

## Validation target

The hardened documents must make all 18 published falsification cases deterministic and fail closed, and a fresh competent agent must be able to implement Package A solely from Git without inventing concurrency, idempotency, budget, privacy, event-ordering or restart semantics.

## Current checkpoint

Branch created from `3e3b3a731cb21d775ae686c65991e90969bb86fb`. Next action: publish the draft PR and harden the architecture/contracts/prompts.