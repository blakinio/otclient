---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-125938
session_role: coordinator
session_rotation_count: 1
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: promotion-review-integration
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T13:17:04+02:00
risk: medium
related_pr: 300
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
  - docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/**
  - docs/agents/reports/OTCLIENT-20260815-track-a-promotion-coordination.md
  - docs/agents/tasks/archive/OTC-20260814-official-client-capability-experiment-sweep.md
  - tools/tibia_worldmap_reconstruction/**
  - tests/tools/tibia_worldmap_reconstruction/**
  - docs/agents/reports/OTC-20260812-worldmap-reconstruction.md
  - docs/agents/tasks/archive/OTC-20260812-worldmap-reconstruction.md
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
  - docs/agents/tasks/archive/OTC-20260813-tibia-runtime-bridge.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - agent-coordination
  - tibia-worldmap-reconstruction
  - tibia-runtime-bridge
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: controlled
decomposition_decision: phased
invocation_started_at: 2026-08-15T12:48:00+02:00
last_progress_at: 2026-08-15T13:17:04+02:00
ci_checks_for_current_head: 0
ci_check_generation: other
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Researchers remain Draft-only; this task performs campaign-level promotion/integration subject to repository gates. Track B remains outside mutation authority.

# Live-state contract

```yaml
TASK_ID: OTC-20260815-track-a-promotion-coordination
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
PROJECT_LANE: otclient
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: docs/OTC-20260815-track-a-promotion-coordination
WORKTREE: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
```

No researcher branch/worktree is shared. Worldmap paths were claimed only after #279 was closed; bridge paths were claimed only after #283 was closed, releasing their stale source ownership.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Promotion ledger

## ACCEPT

- PR #283: bounded read-only runtime bridge implementation only. Source PR closed unmerged at `d93ccb34f66af7d3198a50a46e706b4f902ae637`; accepted evidence preserved in `accepted-read-only-runtime-bridge.md`. `session-status` remains DERIVED until live structural correlation; P1 is not complete.
- Exact-build reversible structural world transition retained from run `31806312967` / job `94785974126`; standalone player XYZ and A3/A4 remain unproven.

## ACCEPT_WITH_EDITS

- PR #279: fail-closed worldmap reconstruction tooling. Source PR closed unmerged at `04356aa9c042ce19d9d8431b91f18567e410a5e5`; exact product/test blobs rebuilt on current main and documentation/catalogue/changelog reconciled on #300. Real capture/mappings/complete OTBM remain unproven.
- PR #290: bounded historical login/recovery procedure only. Source PR closed; accepted extract persisted as `REVALIDATION_REQUIRED`.

## RETURN_FOR_EVIDENCE

- PR #295: map-observation ownership correction; four unresolved material review threads plus Track B ownership collision remain.

## REJECT/SUPERSEDE

- PR #289: broad stale continuation branch; superseded P2 model and unresolved safety findings.
- PR #296: stale lifecycle PR after valid correction was integrated as a bounded coordinator slice.
- PR #277: stale Oteryn-dependent runtime handover; unique negative history preserved.
- PR #280: rejected/superseded only as an active Track A dependency. Broader infrastructure PR intentionally remains open under separate ownership.

# P2 canonical boundary

```yaml
proven:
  - TGameserverTCPConnection ownership/QMeta/RTTI for exact build
  - concrete QTcpSocket member construction at receiver +0x10
  - TProtocolWriter : TIODeviceWriter RTTI relationship
disproven_or_superseded:
  - clientMessageReadyToProcess -> owner+0x88 -> 0xb5b880 gameplay endpoint model
  - 0xb46bd0 as binary gameplay-frame sink
  - 0xc33259 as network/gameplay binary sink
unknown:
  - TGameserverDualConnection ownership/reference path into actual writer
  - serialization/framing order
  - compression/encryption/sequence transformation boundary
  - final binary socket/QIODevice egress
  - causal local/custom harness proof
```

# Parallel lane state

- #301 / P2-NETWORK: separately owned Draft writer-ownership research.
- #302 / P0-STATE: separately owned typed direct-position research; no result promoted without runtime evidence.
- #303 / RUNTIME: separately owned isolated restart/relogin/reacquisition validation.
- #304 / COVERAGE-AUDIT: separately owned item-level coverage registry audit.
- P1 source #283 is now terminally closed after bounded acceptance; further P1 promotion depends on current P0/RUNTIME live evidence and must not weaken the read-only bridge boundary.

# Integration state

```yaml
worldmap:
  source_pr: 279 closed unmerged
  source_head: 04356aa9c042ce19d9d8431b91f18567e410a5e5
  source_final_ci: 31681889560 success
  current_main_product_test_integration: 5d99da492c902c5c2391b61fb5373d0acd43aec0
  report_lifecycle_reconciled: true
  module_catalog_registered: true
  changelog_registered: true
  integration_ci_run: 31881564952
  integration_ci_state_last_observed: in_progress
bridge:
  source_pr: 283 closed unmerged
  source_head: d93ccb34f66af7d3198a50a46e706b4f902ae637
  validated_code_head: 89e13819e6f53026b831b7e8e4c8fab228d1626c
  source_final_ci: 31680615776 success
  source_head_vs_validated_code: only task Markdown changed
  evidence_extract_preserved: true
  current_main_blob_integration: pending
```

# Acceptance inventory

- [x] Current main and governance refetched before mutation.
- [x] Coordinator branch/worktree ownership recovered safely.
- [x] Historical #277/#290 terminally reconciled; #280 removed as Track A dependency without overstepping infrastructure ownership.
- [x] PR #279 source accepted/closed and bounded product/test/report/catalogue/changelog slice rebuilt on current main.
- [x] PR #283 source accepted/closed with evidence boundary preserved and old path ownership released.
- [ ] PR #283 exact product/test blobs rebuilt on current main and registered in shared catalogue/changelog.
- [ ] Accepted integration slice exact-head CI passes after final bridge/worldmap current-main rebuild.
- [ ] Draft #301-#304 reviewed at reviewable heads and assigned explicit dispositions.
- [ ] Quantitative protocol/QMeta/P0 registries reconciled item-by-item.
- [ ] P2/P1/P0/runtime/action final gates satisfied or explicitly left non-complete with evidence.
- [ ] Final audit/E2E/exact-head CI/PR hygiene/task archive/ownership release complete.

# Execution budget

```yaml
invocation_started_at: 2026-08-15T12:48:00+02:00
last_progress_at: 2026-08-15T13:17:04+02:00
ordinary_ci_checks_for_worldmap_head_2d98321: 1
ordinary_ci_checks_for_current_head: 0
terminal_ci_checks: 0
repair_cycles: 0
context_reconstruction_attempts: 1
stall_warnings: 0
```

# Next action

Rebuild the exact accepted PR #283 product/test blobs on current main from source head `d93ccb34...`, register the reusable bridge in `MODULE_CATALOG.md`/`CHANGELOG.md`, then inspect active Draft #301-#304 outcomes while the combined integration CI progresses.
