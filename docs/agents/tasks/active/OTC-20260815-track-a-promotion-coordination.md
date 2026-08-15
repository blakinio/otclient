---
task_id: OTC-20260815-track-a-promotion-coordination
status: validating
agent: ChatGPT
session_id: chatgpt-coordinator-20260815-125938
session_role: coordinator
session_rotation_count: 1
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: exact-head-validation-and-handover
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T13:25:01+02:00
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
  - tools/tibia_runtime_bridge/**
  - tests/tools/tibia_runtime_bridge/**
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
last_progress_at: 2026-08-15T13:25:01+02:00
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

Keep canonical Track A (`official-client-re`) true, reproducible and progressively complete while researchers remain Draft-only and the coordinator alone promotes accepted evidence. Track B is outside mutation authority.

# Coordinator live-state contract

```yaml
TASK_ID: OTC-20260815-track-a-promotion-coordination
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
PROJECT_LANE: otclient
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: docs/OTC-20260815-track-a-promotion-coordination
WORKTREE: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
```

This session safely took over the same coordinator task after the prior coordinator exceeded the mandatory no-progress budget. No researcher branch/worktree has been shared.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Coordinator dispositions

## ACCEPT

- PR #283: bounded read-only runtime bridge implementation only. Source PR closed unmerged; accepted exact source blobs rebuilt on #300. P1 remains incomplete because live `session-status`, authoritative player position, restart/relogin stability and write/action APIs are not proven.
- Exact-build reversible structural world transition from run `31806312967` / job `94785974126` as bounded runtime/world-state evidence only; A3/A4 remain unproven.

## ACCEPT_WITH_EDITS

- PR #279: fail-closed worldmap reconstruction tooling. Source PR closed unmerged; accepted tool/test/report blobs rebuilt on #300 with module catalogue and changelog registration. Real capture coverage, appearance mappings and complete OTBM remain unproven.
- PR #290: bounded historical login/recovery procedure preserved as `REVALIDATION_REQUIRED`; stale source PR closed unmerged.

## RETURN_FOR_EVIDENCE

- PR #295: four unresolved material review threads plus Track B ownership collision.
- PR #301: dispatch-only P2 writer-ownership Draft; no researcher evidence or executed hypothesis yet; remains READY/unassigned.
- PR #302: typed read-only direct-position probe exists, but self-hosted run `31880617510` job `95002559098` remains queued; no semantic result.
- PR #303: isolated restart/relogin design exists, but no self-hosted `reacquire` semantic job has executed; serialized behind #302.
- PR #304: dispatch-only item-level coverage Draft; no registries/validator/summary yet; remains READY/unassigned.

## REJECT/SUPERSEDE

- PR #289: stale broad continuation with superseded P2 model and unresolved safety failures.
- PR #296: stale lifecycle draft after accepted correction was integrated.
- PR #277: stale Oteryn-dependent handover; unique negative history preserved before closure.
- PR #280 only as an active Track A dependency; broader infrastructure PR remains intentionally open under separate ownership.

# Canonical P2 boundary

```yaml
proven:
  - TGameserverTCPConnection exact-build ownership/QMeta/RTTI
  - concrete QTcpSocket member construction at receiver +0x10
  - TProtocolWriter : TIODeviceWriter RTTI
disproven_or_superseded:
  - owner+0x88 -> 0xb5b880 gameplay endpoint
  - 0xb46bd0 binary gameplay sink
  - 0xc33259 network/gameplay sink
unknown:
  - TGameserverDualConnection -> actual writer edge
  - serialization/framing order
  - compression/encryption/sequence boundary
  - final binary socket/QIODevice egress
  - causal local/custom harness proof
```

# Integration state

```yaml
worldmap:
  source_pr: 279 closed unmerged
  source_head: 04356aa9c042ce19d9d8431b91f18567e410a5e5
  source_exact_head_ci: 31681889560 success
  current_main_rebuild: present_on_pr_300
  module_catalog: registered
  changelog: registered
bridge:
  source_pr: 283 closed unmerged
  source_head: d93ccb34f66af7d3198a50a46e706b4f902ae637
  validated_code_head: 89e13819e6f53026b831b7e8e4c8fab228d1626c
  source_exact_head_ci: 31680615776 success
  current_main_rebuild: present_on_pr_300
  module_catalog: registered
  changelog: registered
```

# Quantitative checkpoint

```yaml
protocol_identifier_inventory: 349/349 scoped inventory only
protocol_handler_qmeta_records: 47/47 scoped inventory only
legacy_qobject_connect_edges: 40/41
high_information_gameaction_sender_metaobjects: 29/31
direct_qt_connection_semantic_classification: UNKNOWN/2184
generated_message_semantic_classification: UNKNOWN/349
p0_live_read_coverage: UNKNOWN/UNKNOWN
```

No scoped 100% inventory value is global semantic coverage.

# Acceptance inventory

- [x] Current main/governance/ownership preflight completed before mutation.
- [x] Stale broad #289 ownership released with positive and negative evidence preserved.
- [x] #277/#290 terminally reconciled; #280 removed as a Track A dependency without overstepping infrastructure ownership.
- [x] #279 accepted source closed and bounded worldmap implementation rebuilt on current main.
- [x] #283 accepted source closed and bounded read-only bridge implementation rebuilt on current main.
- [x] Active Draft #301-#304 exact heads reviewed and assigned coordinator dispositions.
- [x] P2/P1/P0/RUNTIME/ACTION non-completion boundaries explicitly preserved.
- [ ] Combined coordinator exact-head CI passes on the final checkpoint head.
- [ ] Item-level protocol/QMeta/P0 registries produced and promoted.
- [ ] P2 writer/final-egress, authoritative P0 reads and restart/relogin evidence close their required gates.
- [ ] A3/A4 safe action parity gates close.
- [ ] Final programme audit/E2E/terminal PR/task/archive/ownership release gates close.

# Execution budget checkpoint

```yaml
invocation_started_at: 2026-08-15T12:48:00+02:00
last_progress_at: 2026-08-15T13:25:01+02:00
context_reconstruction_attempts: 1
repair_cycles: 0
stall_warnings: 0
```

# Next action

Run exact-head CI on this combined coordinator checkpoint. If it passes and no new researcher evidence becomes reviewable, checkpoint the coordinator `ready` and rotate: an independent researcher must next claim the already-created P2 task #301 (highest information gain) or coverage task #304; the current coordinator session cannot impersonate those Draft-only researcher roles or spawn a separate worker with the available toolset.
