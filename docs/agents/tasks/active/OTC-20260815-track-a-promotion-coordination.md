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
updated: 2026-08-15T12:59:38+02:00
risk: medium
related_pr: 300
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
  - docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/**
  - docs/agents/reports/OTCLIENT-20260815-track-a-promotion-coordination.md
  - docs/agents/tasks/archive/OTC-20260814-official-client-capability-experiment-sweep.md
modules_touched:
  - agent-coordination
reuses:
  - docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
depends_on: []
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
execution_reason: repository coordination, PR/evidence review, bounded integration and task dispatch are supported by the connected GitHub interface; owner-funded Codex is not authorized
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: controlled
decomposition_decision: phased
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
invocation_started_at: 2026-08-15T12:48:00+02:00
last_progress_at: 2026-08-15T12:59:38+02:00
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

Keep canonical Track A (`official-client-re`) true and reproducible while reviewing/promoting bounded researcher evidence, integrating only accepted slices and keeping non-overlapping Draft-only research lanes moving. Track B remains outside mutation authority.

# Coordinator live-state contract

```yaml
TASK_ID: OTC-20260815-track-a-promotion-coordination
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
PROJECT_LANE: otclient
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: docs/OTC-20260815-track-a-promotion-coordination
WORKTREE: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
WORKTREE_MODE: isolated GitHub branch checkout equivalent; no shared local worktree is used
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
  - docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/**
  - docs/agents/reports/OTCLIENT-20260815-track-a-promotion-coordination.md
  - docs/agents/tasks/archive/OTC-20260814-official-client-capability-experiment-sweep.md
```

This session resumed the same coordinator task after the prior coordinator session exceeded the mandatory 15-minute no-progress budget. Before takeover, live GitHub state proved that `main` remained `8fca1c3...`, coordinator PR #300 remained exactly at `d4a6ac10782ffacf36bf6d915cc97b3ffaf76e82`, and subsequent repository writes were on the separately owned P0/RUNTIME research branches rather than the coordinator branch. No research branch/worktree is shared by this session.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Current programme state

## FACT

- PR #299 is merged and explicitly leaves P2 open.
- PR #289 is closed/unmerged after `REJECT/SUPERSEDE`; its broad ownership is released while bounded positive and negative evidence is retained.
- Exact-build structural reversible world transition from run `31806312967` / job `94785974126` is retained as bounded FACT evidence; standalone player-position member and A3/A4 remain unproven.
- PR #283 is accepted for a bounded read-only bridge implementation; P1 is not complete.
- PR #279 is `ACCEPT_WITH_EDITS`: fail-closed reconstruction tooling accepted; task lifecycle/current-main integration still needs repair.
- PR #295 remains `RETURN_FOR_EVIDENCE/EDITS`: four unresolved material review threads and a Track B ownership collision remain.
- PR #292 is Track B and outside Track A mutation authority.
- PR #296 is closed as superseded after its valid archive lifecycle correction was integrated as a bounded coordinator slice.
- PR #281 is now closed unmerged and no longer an active Track A blocker.
- Draft research contracts exist on disjoint branches/paths: #301 P2-NETWORK, #302 P0-STATE, #303 RUNTIME, #304 COVERAGE-AUDIT. P1 remains assigned to existing #283 rather than duplicated.
- #302 is actively researched on its own branch; its passive `TPlayerData` probe is read-only and current runtime result is not yet promotable.
- #303 is actively researched on its own branch with an isolated runtime namespace and restart/relogin reacquisition acceptance gate.

## P2 canonical boundary

```yaml
proven:
  - TGameserverTCPConnection ownership/QMeta/RTTI for the exact build
  - concrete QTcpSocket member construction at receiver +0x10
  - TProtocolWriter : TIODeviceWriter RTTI relationship
disproven_or_superseded:
  - prior clientMessageReadyToProcess -> owner+0x88 -> 0xb5b880 gameplay endpoint model
  - 0xb46bd0 as binary Tibia gameplay-frame sink
  - raw 0xc33259 QIODevice candidate from the successful-but-semantic-failure binary-sink workflow
unknown:
  - TGameserverDualConnection ownership/reference path into the actual writer object
  - serialization/framing order
  - compression/encryption/sequence transformation boundary
  - final binary socket/QIODevice egress
  - causal local/custom harness proof
```

## Reconciliation findings prepared in this session

### PR #277

Provisional disposition: `REJECT/SUPERSEDE` as an active continuation handover. Its task still directs continuation through historical Oteryn repository/runtime state, which current `TIBIA_RESEARCH_TRACKS.md` explicitly forbids for Track A. Preserve any unique historical negative run references before terminal closure; do not reactivate its Oteryn continuation instructions.

### PR #290

Provisional disposition: `ACCEPT_WITH_EDITS` for the bounded historical login/session-recovery procedure and corrected evidence vocabulary. It correctly separates Track A/Track B, labels the historical login procedure `REVALIDATION_REQUIRED`, and confines OCR to character-selection bootstrap rather than world semantics. Its `next_action` and older static message-path leads must be reconciled with later #289/#300 evidence and active runtime task #303 before promotion.

### PR #280

Provisional Track A disposition: `REJECT/SUPERSEDE AS TRACK-A DEPENDENCY`. Exact head `eda8714...` fails repository CI at `actionlint`; its migration workflow still depends on historical `oteryn-staging`, which current Track A isolation forbids. Later exact-build Track A evidence already proves `synology-otclient-01` can execute Track A jobs, so the old no-runner blocker is superseded. Any independently useful cross-repository runner-stack design belongs to infrastructure ownership and must not be silently closed or promoted by Track A beyond this dependency disposition.

# Acceptance inventory

- [x] Current `main` exact SHA refetched and fenced before mutation.
- [x] Current parallel-research, experiment, prompting, trust, execution-budget, Track A/B and closeout contracts read from `main`.
- [x] Dedicated coordinator task/branch/isolated checkout-equivalent recovered without sharing a researcher branch/worktree.
- [x] High-impact #289/#283/#279/#295/#296 evidence and ownership conflicts independently reconciled.
- [x] Stale broad #289 ownership released without losing verified positive/negative evidence.
- [x] READY P2/P0/RUNTIME/COVERAGE research lanes have concrete task/branch/isolated-checkout/owned-path/dependency contracts and no unresolved path overlap; P1 remains on #283.
- [ ] Final #277/#280/#290 dispositions and terminal PR states reconciled.
- [ ] Accepted #279/#283 slices integrated only after exact current-main/diff/lifecycle gates.
- [ ] Draft #301/#302/#303/#304 evidence reviewed and assigned explicit coordinator dispositions.
- [ ] Quantitative P2/P1/P0/runtime/action/protocol/QMeta/P0-coverage state reconciled to item-level canonical evidence.
- [ ] Coordinator exact-head validation, PR hygiene, durable handover and ownership release terminal before completion.

# Execution-budget checkpoint

```yaml
invocation_started_at: 2026-08-15T12:48:00+02:00
last_progress_at: 2026-08-15T12:59:38+02:00
entry_task: OTC-20260815-track-a-promotion-coordination
ordinary_ci_checks: 0
terminal_ci_checks: 0
repair_cycles: 0
context_reconstruction_attempts: 1
stall_warnings: 0
```

# Next action

Terminally reconcile the stale historical Track A PRs (#277/#290 and the Track-A dependency status of #280) while preserving unique evidence, then review active Draft #301-#304 as their exact heads become reviewable; do not poll unchanged CI and do not mutate researcher-owned paths.
