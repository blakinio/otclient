---
task_id: OTC-20260818-track-a-full-client-re-coverage-audit
status: investigating
agent: ChatGPT
session_role: auditor
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: audit
phase: synthesis
execution_mode: github_only
branch: docs/OTC-20260818-track-a-full-client-re-coverage-audit
base_branch: main
base_main: a10df477ce88183718ed855386ef96ba25b66320
related_pr: TBD
created: 2026-08-18
risk: low
implementation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
owned_paths:
  - docs/agents/tasks/active/OTC-20260818-track-a-full-client-re-coverage-audit.md
  - docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md
modules_touched:
  - official-client-re-documentation
reuses:
  - docs/agents/reports/OTCLIENT-20260814-official-client-capability-census.md
  - docs/agents/reports/OTCLIENT-20260816-track-a-coverage-audit-refresh.md
  - docs/agents/reports/OTCLIENT-20260818-track-a-s1-unfiltered-static-census.md
  - docs/agents/reports/OTCLIENT-20260818-track-a-s2-player-inbound-static.md
  - docs/agents/reports/OTCLIENT-20260818-track-a-s5-container-inbound-static.md
  - docs/agents/reports/OTCLIENT-20260818-track-a-s6-chat-inbound-static.md
  - docs/agents/reports/OTCLIENT-20260818-track-a-s7-inventory-equipment-static.md
  - docs/agents/reports/OTCLIENT-20260818-track-a-s8-creature-inbound-static.md
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md
depends_on: []
blocks: []
non_overlap:
  - PR #535 S9 action/control owns its own task/evidence/report and is not modified.
  - PR #528 native-login-to-ingame runtime is not observed or mutated.
  - PR #475 worldmap physical runtime is not observed or mutated.
  - PR #302 direct-player-position Draft is not modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one repository-wide coverage synthesis with one canonical report output
validation_level: focused
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
invocation_started_at: 2026-08-18
last_progress_at: 2026-08-18
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Create one canonical, evidence-bounded **FULL CLIENT RE 100%** checklist for the official native Linux Tibia client reverse-engineering programme.

The checklist must cover the whole client rather than only login or worldmap, including gameplay state/actions, inventory/equipment, containers, creatures, chat/social/trade, minimap/worldmap, analyzers, Cyclopedia systems, account/economy UI, network/runtime infrastructure, user options/settings and updater/versioning.

# Status contract

Every subsystem receives exactly one terminal coverage label:

```text
DONE
PARTIAL
NOT_STARTED
BLOCKED
```

Rules:

- `DONE`: the subsystem's declared semantic acceptance is fully proven at the required evidence gate; static name/QMeta presence alone is never enough.
- `PARTIAL`: meaningful dedicated proof exists beyond mere lexical presence, but a semantic/runtime/stability/current-version edge remains.
- `NOT_STARTED`: only broad capability-census/static-presence evidence exists, or no dedicated semantic proof package exists.
- `BLOCKED`: a concrete current dependency prevents the next required proof and is recorded with the exact unblock condition.

The report must not convert `STATIC_PRESENT`, a symbol name, a QMeta method, a generated protobuf name, an old address, or an old runtime observation into semantic completion.

# Acceptance

- [ ] include status criteria and evidence boundary;
- [ ] include exact current trusted `main` snapshot and old exact-client fence caveat;
- [ ] include status counters (`DONE`, `PARTIAL`, `NOT_STARTED`, `BLOCKED`, total);
- [ ] include all base-programme capabilities;
- [ ] include every feature family from the official-client capability census;
- [ ] explicitly include options/settings: graphics, audio, interface, gameplay/control persistence;
- [ ] explicitly include updater/versioning/current-client revalidation;
- [ ] distinguish structural inventory from semantic/runtime proof;
- [ ] record current active/unpromoted S9 as in-flight evidence, not canonical fact;
- [ ] record exact primary evidence/PR/report for each non-`NOT_STARTED` row where practical;
- [ ] record one exact missing step to `DONE` for every row;
- [ ] perform full changed-path and full-diff audit;
- [ ] E2E = `NOT_APPLICABLE` with documentation/audit reason;
- [ ] exact-head repository CI/governance green before completion;
- [ ] zero unresolved review threads/material findings before merge;
- [ ] archive task and release ownership after protected squash merge.

# Current checkpoint

```yaml
status: investigating
last_completed_step: trusted-base governance, current main, open PRs, current S8 and in-flight S9 boundaries inspected
material_findings_open: 0
next_action: write the canonical full-client subsystem matrix from current durable evidence without promoting static presence to semantic DONE
```
