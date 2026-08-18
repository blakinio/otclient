---
task_id: OTC-20260818-track-a-full-client-re-coverage-audit
status: blocked
agent: ChatGPT
session_role: auditor
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: audit
phase: refreshed-current-state-independent-audit-required
execution_mode: github_only
branch: docs/OTC-20260818-track-a-full-client-re-coverage-audit
base_branch: main
base_main: ebbb36f50076ff4072c7218e302614c1dfea00b1
related_pr: 536
created: 2026-08-18
updated: 2026-08-18T16:08:00+02:00
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
  - docs/agents/reports/OTCLIENT-20260818-full-client-re-current-refresh.md
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
  - PR #528 current-package/native-login continuation evidence
  - PR #539 S10 retained action-protocol code-window harvest
  - docs/research/native-client/NATIVE_AUTH_SESSION_FLOW.md
  - docs/research/native-client/NATIVE_GAME_LOGIN_CREDENTIAL_PROOF.md
depends_on: []
blocks: []
non_overlap:
  - PR #528 owns current official-client package/runtime/login; this task consumes durable non-secret evidence only and does not observe or mutate its runtime/package.
  - PR #539 owns S10 action-protocol harvesting; this task records only its in-flight frontier and does not promote its result.
  - PR #475 worldmap physical runtime is not observed or mutated.
  - PR #302 direct-player-position Draft is not modified.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one repository-wide coverage synthesis with checklist, matrix and current refresh overlay
validation_level: focused
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
invocation_started_at: 2026-08-18
last_progress_at: 2026-08-18T16:08:00+02:00
ci_checks_for_current_head: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Maintain one evidence-bounded **FULL CLIENT RE 100%** checklist plus a compact matrix for the whole official native Linux Tibia client reverse-engineering programme, and refresh it when live repository evidence materially changes.

# Current status model

```text
DONE
PARTIAL
NOT_STARTED
BLOCKED
```

Static/QMeta/protobuf presence alone is never semantic `DONE`.

# Current refresh result — 2026-08-18 16:08 +02:00

Fresh repository inspection found two material post-matrix facts:

1. PR #528 now retains a read-only current-official package fingerprint:
   - run/job `32140385842 / 95721374178`;
   - packed SHA `1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354`;
   - unpacked SHA `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`;
   - unpacked size `52109920`;
   - canonical on-disk source-package `bin/client` identity remains `UNKNOWN` and must be re-inventoried before updater mutation/current-build RE.
2. PR #539 / S10 is now the active retained-evidence discriminator for the first direct action-layer -> protocol-layer code/dataflow edge, starting with `sendMoveObject`; result remains in progress and is not promoted.

Therefore row `A01` moves from `BLOCKED` to `PARTIAL` and no other row changes status.

Current totals:

```text
TOTAL        169
DONE          10
PARTIAL       65
NOT_STARTED   86
BLOCKED        8
```

Current artifacts:

- canonical base checklist: `docs/agents/reports/OTCLIENT-20260818-full-client-re-100-percent-checklist.md`;
- refreshed matrix: `docs/agents/reports/OTCLIENT-20260818-full-client-re-matrix.md`;
- current delta overlay: `docs/agents/reports/OTCLIENT-20260818-full-client-re-current-refresh.md`.

# Acceptance

- [x] all 169 subsystem IDs represented;
- [x] structural inventory separated from semantic/runtime proof;
- [x] options/settings explicitly represented;
- [x] updater/current-build resilience explicitly represented;
- [x] current `main@ebbb36f50076ff4072c7218e302614c1dfea00b1` rechecked and unchanged;
- [x] #528 current-package evidence incorporated without claiming current on-disk package completion;
- [x] #539/S10 incorporated as in-flight frontier without premature promotion;
- [x] refreshed totals reconcile: `10 + 65 + 86 + 8 = 169`;
- [x] E2E = `NOT_APPLICABLE` because this task changes documentation/coverage state only;
- [ ] exact-head required CI/governance after this refresh commit;
- [ ] fresh independent documentation audit with material findings `0`;
- [ ] zero unresolved review threads/requested changes on final head;
- [ ] Ready -> protected squash merge -> task archive/ownership release.

# Independent-audit blocker

No submitted independent review exists on PR #536. The current worker's self-review cannot satisfy the repository's fresh independent documentation-audit gate; central Spark pre-review remains advisory only.

```yaml
status: blocked
material_findings_open_from_self_audit: 0
blocker: REQUIRED_FRESH_INDEPENDENT_DOCUMENTATION_AUDIT_UNAVAILABLE_IN_CURRENT_SESSION
last_completed_step: current repository state refreshed; A01 promoted BLOCKED->PARTIAL from #528 read-only current-package fingerprint; S10 #539 added as in-flight frontier; matrix totals updated
next_action: a fresh independent auditor validates PR #536 final four-path diff against current main and primary evidence; if material findings are 0 and exact-head checks are green, mark Ready and continue protected squash merge/closeout
```
