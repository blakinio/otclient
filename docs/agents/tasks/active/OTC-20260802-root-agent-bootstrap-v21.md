---
task_id: OTC-20260802-root-agent-bootstrap-v21
status: implementing
agent: "GPT-5.6 Thinking"
track: agent-governance
workstream: root-agent-bootstrap
parallel_wave: GOVERNANCE-V21
parallel_lane: ROOT-BOOTSTRAP
parallel_lane_state: implementing
coordinator_task: none
branch: docs/root-agent-bootstrap-v21-20260802
base_branch: main
created: 2026-08-02T08:57:00+02:00
updated: 2026-08-02T08:57:00+02:00
last_verified_commit: "74c1ce1c837fc8945888168c6f6f2caf6e87e286"
required_base_commit: ""
risk: low
related_pr: ""
depends_on: []
integration_after: []
owned_paths:
  - AGENTS.override.md
  - docs/agents/tasks/active/OTC-20260802-root-agent-bootstrap-v21.md
shared_path_lease: []
contract_role: bootstrap
contracts_produced:
  - mandatory root Codex bootstrap v2.1
contracts_consumed:
  - delivery completeness and closeout v2.1
  - autonomous programme continuation v2.1
crates_touched: []
features_touched: []
contracts_touched:
  - agent startup and short-command routing
modules_touched:
  - agent-governance
reuses:
  - existing task lifecycle and CI gates
public_interfaces: []
cross_repo_tasks:
  - CAN-20260802-root-agent-bootstrap-v21
  - FTAI-20260802-root-agent-bootstrap-v21
  - OTERYN-20260802-root-agent-bootstrap-v21
  - OTH-20260802-root-agent-bootstrap-v21
performance_evidence:
  - documentation-only
security_evidence:
  - repository allowlist, client, protocol, asset and production restrictions remain authoritative
---

# Root agent bootstrap v2.1

## Goal

Add an automatically loaded root bootstrap that forces every Codex agent to read the complete OTClient governance stack and makes the short autonomous command sufficient.

## Acceptance

- [x] Add root `AGENTS.override.md` without weakening client, protocol, asset or repository safety.
- [x] Require root/nested instructions, delivery closeout and autonomous continuation contracts.
- [x] Define the short Polish autonomous command as authorization for the durable foreground loop.
- [x] Preserve complete vertical-slice, independent audit, real E2E, exact-head CI, terminal PR and archive requirements.
- [ ] Pass required CI.
- [ ] Merge and archive.
