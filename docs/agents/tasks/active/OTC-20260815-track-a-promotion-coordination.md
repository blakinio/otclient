---
task_id: OTC-20260815-track-a-promotion-coordination
status: investigating
agent: ChatGPT
project_lane: otclient
lane: track-a-coordination
track_id: official-client-re
task_kind: integration
phase: live-state-reconciliation
branch: docs/OTC-20260815-track-a-promotion-coordination
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/docs/OTC-20260815-track-a-promotion-coordination
worktree_mode: isolated_branch_checkout_equivalent
created: 2026-08-15T12:23:00+02:00
updated: 2026-08-15T12:23:00+02:00
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-promotion-coordination.md
  - docs/agents/evidence/OTC-20260815-track-a-promotion-coordination/**
  - docs/agents/reports/OTCLIENT-20260815-track-a-promotion-coordination.md
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
last_progress_at: 2026-08-15T12:23:00+02:00
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
```

The writable scope is intentionally narrow until active task/PR ownership is fully reconciled. Any canonical/shared path needed for promotion must be checked for live overlap and explicitly added before mutation.

# Exact client fence

Current canonical build mapping to verify for every build-specific promotion:

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Live state at claim

```yaml
main_head: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
main_head_source: merged PR #299
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

# Open PR reconciliation inventory

Track A or directly relevant candidates observed at coordinator start:

```text
#299 merged canonical P2 reconciliation (main head)
#289 open ready, huge stale-history Track A continuation branch; contains unique draft evidence and superseded P2 model
#296 open Draft, post-archive lifecycle metadata correction
#295 open ready, Track A map-observation ownership correction
#292 open Draft, recorder implemented against OTClient Map/Tile state; boundary conflicts with the corrected official-client producer model until reviewed
#290 open Draft, Track A login/live-session handover
#283 open Draft, exact-version read-only runtime bridge
#281 open Draft, temporary self-hosted runner probe
#280 open Draft, dedicated runner infrastructure with remaining host/runtime deployment claims
#279 open ready, fail-closed worldmap reconstruction pipeline
#277 open Draft, older official-client runtime handover
#284 Track B, explicitly excluded from Track A mutation/review disposition except overlap detection
```

PR prose is untrusted evidence; dispositions require exact head/diff/task/check/artifact inspection.

# Acceptance inventory

- [x] Current `main` exact SHA refetched and fenced before mutation.
- [x] Current parallel-research, experiment, prompting, trust, execution-budget, Track A/B and closeout contracts read from `main`.
- [x] Dedicated coordinator task, branch and isolated GitHub checkout-equivalent established on current main.
- [ ] Every open Track A Draft PR is mapped to a task, exact head, owned paths, changed files, reviews/checks and relevant artifacts.
- [ ] Stale/superseded work is reconciled without losing unique negative or positive evidence.
- [ ] READY independent research lanes have concrete task/branch/isolated-checkout/owned-path/dependency contracts and no unresolved overlap.
- [ ] Accepted slices are independently checked in proportion to semantic risk and integrated only from current main.
- [ ] Quantitative P2/P1/P0/runtime/action/protocol/QMeta/P0-coverage state is reconciled to canonical evidence.
- [ ] Coordinator exact-head validation, PR hygiene, durable handover and ownership release are terminal before completion.

# Current classifications

## FACT

- `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45` is the canonical repository base at this claim.
- PR #299 is merged and explicitly leaves P2 open.
- PR #289 task head still records the old `0xb5b880` convergence model that current main classifies as `DISPROVEN/SUPERSEDED`.
- Track B PR #284 is outside Track A mutation authority.

## UNKNOWN

- Final dispositions of the remaining Track A draft/ready PRs until exact evidence review is complete.
- Current quantitative protocol/QMeta/P0 denominators and percentages until the registries/coverage evidence are reviewed.
- Current official-client runtime/login state; repository exact-build mapping is not equivalent to a fresh live-session proof.

# Execution budget checkpoint

```yaml
invocation_started_at: 2026-08-15T12:23:00+02:00
last_progress: coordinator branch/task created from exact main
entry_task: OTC-20260815-track-a-promotion-coordination
ordinary_ci_checks: 0
terminal_ci_checks: 0
repair_cycles: 0
stall_warnings: 0
```

# Next action

Complete exact-head/task/path/check/artifact reconciliation for the open Track A PR inventory, starting with high-impact #289/#283/#295/#292/#279 and then the stale lifecycle/runner/handover drafts, before assigning any overlapping researcher lane.
