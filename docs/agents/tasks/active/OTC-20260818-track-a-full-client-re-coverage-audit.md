---
task_id: OTC-20260818-track-a-full-client-re-coverage-audit
status: blocked
agent: ChatGPT
session_role: auditor
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: audit
phase: independent-audit-required
execution_mode: github_only
branch: docs/OTC-20260818-track-a-full-client-re-coverage-audit
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
related_pr: 536
created: 2026-08-18
updated: 2026-08-18
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
  - docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md
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
  - docs/agents/reports/OTCLIENT-20260818-track-a-s9-action-control-static-census.md
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md
depends_on: []
blocks: []
non_overlap:
  - promoted S9 is read as current-main evidence; its closed source/promotion paths are not modified.
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
decomposition_reason: one repository-wide coverage synthesis with checklist plus compact matrix projection
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

Create one canonical, evidence-bounded **FULL CLIENT RE 100%** checklist and a compact **coverage matrix** for the official native Linux Tibia client reverse-engineering programme.

The coverage spans the whole client rather than only login or worldmap: gameplay state/actions, inventory/equipment, containers, creatures, chat/social/trade, minimap/worldmap, analyzers, Cyclopedia/progression systems, account/economy UI, network/runtime infrastructure, user options/settings and updater/versioning.

# Status contract

Every subsystem receives exactly one coverage label:

```text
DONE
PARTIAL
NOT_STARTED
BLOCKED
```

- `DONE`: the exact row claim is fully proven at the required evidence gate; static name/QMeta presence alone is never enough.
- `PARTIAL`: meaningful dedicated proof exists beyond lexical presence, but a semantic/runtime/stability/current-version edge remains.
- `NOT_STARTED`: only broad capability-census/static-presence evidence exists, or no dedicated semantic proof package exists; this is not an absence claim.
- `BLOCKED`: a concrete current dependency prevents the next required proof and the report records the unblock route.

# Acceptance

- [x] status criteria and evidence boundary;
- [x] exact current trusted `main` snapshot and old exact-client fence caveat;
- [x] status counters: total `169`, `DONE 10`, `PARTIAL 64`, `NOT_STARTED 86`, `BLOCKED 9`;
- [x] all base-programme capabilities represented;
- [x] capability-census feature families represented;
- [x] options/settings explicitly represented: graphics, audio, interface, gameplay/control and persistence;
- [x] updater/versioning/current-client revalidation explicitly represented;
- [x] structural inventory separated from semantic/runtime proof;
- [x] promoted S9 reconciled from current `main@ebbb36f50076ff4072c7218e302614c1dfea00b1`;
- [x] primary evidence keys/PRs/reports recorded;
- [x] every checklist row has a concrete remaining-step code/path to `DONE`;
- [x] compact matrix provides area counts and a full 169-ID one-hot projection with no status reinterpretation;
- [x] matrix scope table explicitly includes equipment/options/client feature families;
- [x] full changed-path and full-diff self-audit after matrix addition: exactly three declared documentation/task paths; no workflow/runtime/client mutation;
- [x] matrix totals reconcile exactly to checklist totals: `10 + 64 + 86 + 9 = 169`;
- [x] E2E = `NOT_APPLICABLE` with documentation/audit reason;
- [ ] fresh independent documentation audit with material findings `0`;
- [ ] required exact-head checks on the final unchanged head after this checkpoint commit;
- [x] review threads/requested changes at matrix self-audit checkpoint: `0/0`;
- [ ] mark Ready, protected squash merge, task archive and ownership release.

# Matrix projection

Canonical detailed checklist:

`docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md`

Compact dashboard/matrix:

`docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md`

The matrix is deliberately a projection of the checklist, not an independent source of truth. It contains:

```text
Executive status matrix: 8 areas × 4 states
Full ID matrix: all 169 IDs exactly once
Scope matrix: what each area covers
Critical dependency matrix
Completion-condition matrix
```

# Validation checkpoint

The matrix head immediately before this checkpoint-only task update was:

```text
2a2e7d44dc87bc83badb5fde08ce03b3b3a4033e
Track A agent runtime governance 32144075488 = SUCCESS
CI 32144075809 = SUCCESS
main freshness = ebbb36f50076ff4072c7218e302614c1dfea00b1
changed paths = exactly 3 declared files
review threads = 0
```

This checkpoint changes the head; exact-head required checks must be green again before any Ready/merge transition.

# Independent-audit blocker

Repository governance requires a fresh independent documentation audit. The current worker's self-review cannot satisfy that gate, and the standing central Spark pre-review is explicitly advisory and does not replace required independent review. No separate independent auditor/validator with fresh semantic context is available through the current execution surface.

```yaml
status: blocked
material_findings_open_from_self_audit: 0
blocker: REQUIRED_FRESH_INDEPENDENT_DOCUMENTATION_AUDIT_UNAVAILABLE_IN_CURRENT_SESSION
last_completed_step: full-client checklist plus compact matrix persisted; 169 IDs/totals reconciled; final three-path diff self-audited with no unrelated mutation
next_action: a fresh independent auditor validates PR #536 exact final diff against current main and primary evidence; if material findings are 0 and final-head CI is green, mark Ready and continue protected squash merge/closeout
```
