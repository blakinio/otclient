---
task_id: OTC-20260815-track-a-promotion-coordination
status: active
agent: ChatGPT
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: promotion-and-dispatch
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T12:37:00+02:00
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
invocation_started_at: 2026-08-15T12:23:00+02:00
last_progress_at: 2026-08-15T12:37:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: other
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# Objective

Keep canonical Track A (`official-client-re`) true and reproducible while reviewing/promoting bounded researcher evidence and preparing non-overlapping draft-only research lanes. Track B is outside mutation authority.

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

The archived lifecycle path was added only after PR #296 was terminally closed as superseded, releasing its ownership. Any further canonical/shared path needed for promotion must be checked for live overlap and explicitly added before mutation.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Live state checkpoint

```yaml
main_head: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
main_head_source: merged PR #299
coordinator_pr: 300
closed_as_superseded:
  - pr: 289
    reason: broad stale Track A continuation; superseded P2 model; failed exact-head CI; unresolved P1 safety findings
  - pr: 296
    reason: accepted lifecycle repair is being integrated as a bounded current-main coordinator slice
track_a_p2_canonical_boundary:
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
stalled_noncanonical_run:
  id: 31825417040
  state_observed: queued
  semantic_rule: do not dispatch a conceptual duplicate merely to bypass the queue
```

# Promotion checkpoint

## FACT

- PR #299 is merged and explicitly leaves P2 open.
- PR #289 is closed, unmerged, after coordinator `REJECT/SUPERSEDE`; its broad ownership is released.
- The exact-build structural reversible world transition from run `31806312967` / job `94785974126` is retained as bounded FACT evidence; direct player-position member and A3/A4 remain unproven.
- PR #283 is accepted for a bounded read-only bridge implementation, not for P1 completion.
- PR #279 is `ACCEPT_WITH_EDITS`: fail-closed tooling accepted, lifecycle checkpoint still needs current-state repair/integration.
- PR #295 is `RETURN_FOR_EVIDENCE/EDITS` due four unresolved material findings and a Track B ownership collision.
- PR #292 is Track B and therefore outside Track A mutation authority.
- PR #296 is closed as superseded after its valid archive lifecycle correction was accepted for current-main integration.

## UNKNOWN

- Final dispositions of #290, #277, #280 and #281 until remaining supersession/current-runtime checks are complete.
- Final item-level protocol/QMeta/P0 coverage; selected census percentages are not global semantic coverage.
- Current official-client runtime/login state at this instant; historical exact-build runtime evidence is not a live-state guarantee.

# Acceptance inventory

- [x] Current `main` exact SHA refetched and fenced before mutation.
- [x] Current parallel-research, experiment, prompting, trust, execution-budget, Track A/B and closeout contracts read from `main`.
- [x] Dedicated coordinator task, branch and isolated GitHub checkout-equivalent established on current main.
- [x] High-impact #289/#283/#279/#295/#296 evidence and ownership conflicts independently reconciled.
- [x] Stale broad #289 ownership released without losing verified positive/negative evidence.
- [ ] Remaining #290/#277/#280/#281 dispositions terminally reconciled.
- [ ] READY independent research lanes have concrete task/branch/isolated-checkout/owned-path/dependency contracts and no unresolved overlap.
- [ ] Accepted slices are integrated only as bounded auditable current-main changes.
- [ ] Quantitative P2/P1/P0/runtime/action/protocol/QMeta/P0-coverage state is reconciled to item-level canonical evidence.
- [ ] Coordinator exact-head validation, PR hygiene, durable handover and ownership release are terminal before completion.

# Execution budget checkpoint

```yaml
invocation_started_at: 2026-08-15T12:23:00+02:00
last_progress: broad stale ownership released; bounded promotion ledger persisted; archive lifecycle path claimed after #296 closure
entry_task: OTC-20260815-track-a-promotion-coordination
ordinary_ci_checks: 0
terminal_ci_checks: 0
repair_cycles: 0
stall_warnings: 0
```

# Next action

Integrate the accepted #296 archive lifecycle correction on this current-main branch, then materialize distinct Draft-only P2-NETWORK, P0-STATE, RUNTIME and COVERAGE-AUDIT task/branch/isolated-checkout contracts from a freshly refetched main; keep P1-BRIDGE assigned to existing PR #283 rather than duplicating it.
