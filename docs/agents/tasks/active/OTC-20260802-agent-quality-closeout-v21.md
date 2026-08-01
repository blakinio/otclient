---
task_id: OTC-20260802-agent-quality-closeout-v21
status: validating
agent: "GPT-5.6 Thinking"
track: agent-governance
workstream: quality-closeout-v21
parallel_wave: GOVERNANCE-V21
parallel_lane: QUALITY-CLOSEOUT
parallel_lane_state: validating
coordinator_task: none
branch: docs/agent-quality-closeout-v21-20260802
base_branch: main
created: 2026-08-02T00:20:00+02:00
updated: 2026-08-02T00:24:00+02:00
last_verified_commit: "78edb2f12d5346ae6e9c7f5981fc4bcd997e18ec"
required_base_commit: "f4eb8eef601a90a9f660672911f3e914f5ffae94"
risk: low
related_pr: "#162"
depends_on: []
integration_after: []
owned_paths:
  - docs/agents/AGENT_QUALITY_AND_CLOSEOUT.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/tasks/active/OTC-20260802-agent-quality-closeout-v21.md
shared_path_lease: []
contract_role: producer
contracts_produced:
  - agent quality and closeout contract v2.1
contracts_consumed:
  - autonomous programme continuation v2
crates_touched: []
features_touched: []
contracts_touched:
  - prompting, quality, validation, and lifecycle governance
modules_touched:
  - agent-governance
reuses:
  - existing checkpoint and archive lifecycle
public_interfaces: []
cross_repo_tasks:
  - blakinio/canary#1053
  - blakinio/freqtrade#988
  - blakinio/Oteryn-Platform#443
  - blakinio/Otheryn#299
performance_evidence:
  - documentation-only
security_evidence:
  - existing client, protocol, asset, upstream, Canary, and production boundaries remain unchanged
---

# OTC-20260802 — Agent quality and closeout v2.1

## Goal

Make outcome-based evals, trust boundaries, full-stack vertical slices, independent audit, real E2E, exact-final-head CI, related-PR cleanup, and terminal task archival mandatory for substantial agent work.

## Acceptance

- [x] Add the normative v2.1 contract.
- [x] Make the prompting handover require it.
- [x] Cover all agreed quality and closeout gates.
- [ ] Pass exact-head CI.
- [ ] Merge and archive.

## Context checkpoint

```yaml
checkpoint_version: 1
policy_version: 2
updated_at: 2026-08-02T00:24:00+02:00
head: 78edb2f12d5346ae6e9c7f5981fc4bcd997e18ec
branch: docs/agent-quality-closeout-v21-20260802
pr: 162
status: validating
phase: validate
session_id: chat-20260802-quality-v21
session_role: coordinator
execution_mode: chat
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
owned_paths:
  - docs/agents/AGENT_QUALITY_AND_CLOSEOUT.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/tasks/active/OTC-20260802-agent-quality-closeout-v21.md
proven:
  - The v2.1 contract exists and is mandatory in the handover.
  - PR 162 owns the governance contract, handover integration, and task record.
derived:
  - Future substantial work must pass the integrated quality and closeout gate.
unknown:
  - Exact-head CI result after this PR binding update.
conflicts: []
changed_paths:
  - docs/agents/AGENT_QUALITY_AND_CLOSEOUT.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/tasks/active/OTC-20260802-agent-quality-closeout-v21.md
validation: []
blockers: []
next_action: verify exact-head CI for PR 162, then complete merge and archive gates
```
