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
updated: 2026-08-15T13:11:22+02:00
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
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
modules_touched:
  - agent-coordination
  - tibia-worldmap-reconstruction
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
last_progress_at: 2026-08-15T13:11:22+02:00
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

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete. Researchers remain Draft-only; this task alone performs campaign-level promotion/integration subject to repository gates. Track B remains outside mutation authority.

# Live-state contract

```yaml
TASK_ID: OTC-20260815-track-a-promotion-coordination
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
PROJECT_LANE: otclient
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: docs/OTC-20260815-track-a-promotion-coordination
WORKTREE: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
```

The session resumed the same coordinator task after the prior session exceeded the mandatory no-progress budget. No researcher branch/worktree is shared. Worldmap integration paths were claimed only after source PR #279 was closed unmerged, releasing its stale ownership.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Promotion ledger

## ACCEPT

- PR #283: bounded read-only runtime bridge implementation only; P1 remains incomplete.
- Exact-build reversible structural world transition retained from run `31806312967` / job `94785974126`; standalone player XYZ and A3/A4 remain unproven.

## ACCEPT_WITH_EDITS

- PR #279: fail-closed worldmap reconstruction tooling. Source PR closed unmerged at `04356aa9c042ce19d9d8431b91f18567e410a5e5`; exact accepted tool/test blobs are being rebuilt on current main. Product/test blob integration commit: `5d99da492c902c5c2391b61fb5373d0acd43aec0`.
- PR #290: bounded historical login/recovery procedure only. Source PR closed; accepted extract persisted as `REVALIDATION_REQUIRED` under coordinator evidence.

## RETURN_FOR_EVIDENCE

- PR #295: map-observation ownership correction; four unresolved material review threads plus Track B ownership collision remain.

## REJECT/SUPERSEDE

- PR #289: broad stale continuation branch; superseded P2 model and unresolved safety findings.
- PR #296: stale lifecycle PR after valid correction was integrated as a bounded coordinator slice.
- PR #277: stale Oteryn-dependent runtime handover; unique negative history preserved under coordinator evidence.
- PR #280: rejected/superseded only as an active Track A dependency. Broader infrastructure PR intentionally remains open under separate ownership.

# P2 canonical boundary

```yaml
proven:
  - TGameserverTCPConnection ownership/QMeta/RTTI for the exact build
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

- #301 / P2-NETWORK: separately owned Draft task for writer ownership; no coordinator mutation of its paths.
- #302 / P0-STATE: active read-only typed `TPlayerData` direct-position research; no direct-position result promoted without runtime evidence.
- #303 / RUNTIME: active isolated restart/relogin/reacquisition validation.
- #304 / COVERAGE-AUDIT: separately owned item-level registry audit.
- #283 / P1-BRIDGE: existing separately owned bridge lane; no duplicate P1 task created.

# Acceptance inventory

- [x] Current main and governance refetched before mutation.
- [x] Dedicated coordinator task/branch/isolated checkout recovered safely.
- [x] Broad stale #289 ownership released with positive/negative evidence preserved.
- [x] Historical #277/#290 reconciled terminally; #280 removed as a Track A dependency without overstepping infrastructure ownership.
- [x] P2/P0/RUNTIME/COVERAGE Draft contracts are disjoint; P1 remains on #283.
- [ ] PR #279 documentation/catalogue/changelog/archive lifecycle integration complete and exact-head validated.
- [ ] PR #283 accepted bridge rebuilt on current main and exact-head validated.
- [ ] Draft #301-#304 reviewed at reviewable heads and assigned explicit dispositions.
- [ ] Quantitative protocol/QMeta/P0 registries reconciled item-by-item.
- [ ] P2/P1/P0/runtime/action final gates satisfied or explicitly left non-complete with evidence.
- [ ] Final audit/E2E/exact-head CI/PR hygiene/task archive/ownership release complete.

# Execution budget

```yaml
invocation_started_at: 2026-08-15T12:48:00+02:00
last_progress_at: 2026-08-15T13:11:22+02:00
ordinary_ci_checks_for_previous_head_1eccec0: 2
ordinary_ci_checks_for_current_head: 0
terminal_ci_checks: 0
repair_cycles: 0
context_reconstruction_attempts: 1
stall_warnings: 0
```

# Next action

Finish PR #279 lifecycle integration: add the accepted source report, merge shared `MODULE_CATALOG.md` and `CHANGELOG.md` narrowly, create terminal archive task evidence, then run exact-head validation before beginning PR #283 integration.
