---
task_id: OTC-20260815-track-a-p2-writer-vtable-group
status: active
agent: ChatGPT
session_id: chatgpt-p2-vtable-researcher-20260815-1415
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: static-research
phase: p2-writer-vtable-group-transform-boundary
branch: research/OTC-20260815-track-a-p2-writer-vtable-group
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-writer-vtable-group
worktree_mode: isolated_branch_checkout_equivalent
risk: low
related_pr: 305
updated: 2026-08-15T14:15:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-writer-vtable-group.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-writer-vtable-group/**
  - .github/workflows/tibia-official-client-re-p2-writer-vtable-group.yml
  - .github/scripts/tibia-official-client-re-p2-writer-vtable-group.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 / merged PR #299
  - accepted PR #301 writer-retention evidence under coordinator PR #300
  - reviewed exact-build artifact 9231716774 from run 31833767461
  - reviewed exact-build artifact 9229251044 from run 31827157926
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
claim_check: passed against exact main, Draft PR #305 status ready/unassigned, released coordinator #300 and disjoint active RUNTIME #303
---

# Objective

Resolve the exact-build identity and role of `0x2f69e30 / RTTI 0x3080748`, currently the intermediate retained object in accepted PR #301, and determine whether it narrows the first writer transform/framing edge. Do not repeat queued final-socket run `31825417040` or generic QIODevice writer enumeration.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Starting structural facts

- canonical `TProtocolWriter` RTTI `0x3080728`, primary address point `0x2f69dd0`, derives from `TIODeviceWriter` RTTI `0x3080718`;
- accepted PR #301 proves `TProtocolClientMessageProcessor -> retained intermediate object -> retained shared TProtocolWriter`;
- reviewed artifact `9231716774` places `TProtocolWriter +0x50 = 0`, `+0x58 = 0x3080748`, `+0x60 = 0x7de7f0`, so absolute `0x2f69e30` is structurally an adjacent Itanium address point in the same emitted vtable group;
- `0x7de7f0` and `0x7dfd60` load `0x2f69e30` and write it to `[this]` while tearing down object state around `+0x208..+0x238`;
- historical `0x3084c70 -> +0xd0 0xb40630` is separate and must remain separate absent provenance.

# Hypothesis

`0x2f69e30` is a secondary/base-class address point inside the canonical `TProtocolWriter` vtable group. Recovering RTTI `0x3080748` name/base relation, if present in reviewed evidence, will identify the exact retained intermediate type or at least prove a typed vtable-group relation. The corresponding virtual methods may narrow the first transform/framing stage.

# Acceptance gate

- [ ] exact artifact digests verified before parsing;
- [ ] group relation proved structurally from Itanium preamble/address layout;
- [ ] RTTI name/base relation recovered if the reviewed artifacts contain enough data, otherwise explicitly UNKNOWN;
- [ ] `0x7de7f0/0x7dfd60` bounded from exact disassembly;
- [ ] PR #301 relation updated without collapsing distinct objects;
- [ ] historical `0x3084c70/0xb40630` kept separate absent direct provenance;
- [ ] no framing/transform/final-egress claim beyond direct evidence;
- [ ] no proprietary client bytes/secrets/account state committed or uploaded;
- [ ] exact-head CI terminal before handoff.

# Next action

Build a deterministic GitHub-hosted parser over digest-fenced artifacts `9231716774` and `9229251044`. First classify the `TProtocolWriter` vtable group and teardown functions; then classify any safe transform-boundary implication. Persist `UNKNOWN` where artifact data cannot name RTTI `0x3080748`.
