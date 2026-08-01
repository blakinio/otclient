---
task_id: OTC-20260802-delivery-closeout-v21
status: validating
agent: "GPT-5.6 Thinking"
track: agent-governance
workstream: delivery-completeness-closeout
parallel_wave: GOVERNANCE-V21
parallel_lane: DELIVERY-CLOSEOUT
parallel_lane_state: validating
coordinator_task: none
branch: docs/agent-closeout-vertical-slice-v21-20260802
base_branch: main
created: 2026-08-02T00:14:00+02:00
updated: 2026-08-02T00:24:00+02:00
last_verified_commit: "05911d1530883c76b5351e6b38282f6e97167f57"
required_base_commit: "99ebed0914e296268d32642000af6d71664cadd9"
risk: low
related_pr: "#164"
depends_on: []
integration_after: []
owned_paths:
  - docs/agents/AGENTS.md
  - docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md
  - docs/agents/tasks/active/OTC-20260802-delivery-closeout-v21.md
shared_path_lease: []
contract_role: producer
contracts_produced:
  - delivery completeness and closeout v2.1
contracts_consumed:
  - autonomous programme continuation v2
crates_touched: []
features_touched: []
contracts_touched:
  - agent delivery and closeout governance
modules_touched:
  - agent-governance
reuses:
  - existing task lifecycle and CI gates
public_interfaces: []
cross_repo_tasks:
  - blakinio/canary#1054
  - blakinio/freqtrade#989
  - blakinio/Oteryn-Platform#445
  - blakinio/Otheryn#301
performance_evidence:
  - documentation-only
security_evidence:
  - trust boundaries and existing client/protocol safety remain authoritative
---

# Delivery completeness and closeout v2.1

## Goal

Require complete client/backend or producer/consumer delivery, independent audit, real E2E, exact-head validation and terminal PR hygiene before substantial work is completed.

## Acceptance

- [x] Add and route the normative closeout contract.
- [x] Prevent backend-only completion claims where client/frontend consumers are required.
- [x] Require prompt eval discipline and trust boundaries.
- [x] Require audit, E2E and terminal related PRs.
- [ ] Pass required CI.
- [ ] Merge and archive.
