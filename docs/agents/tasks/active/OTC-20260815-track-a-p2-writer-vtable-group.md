---
task_id: OTC-20260815-track-a-p2-writer-vtable-group
status: ready
agent: unassigned_draft_only_researcher
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
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-writer-vtable-group.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-writer-vtable-group/**
  - .github/workflows/tibia-official-client-re-p2-writer-vtable-group.yml
  - .github/scripts/tibia-official-client-re-p2-writer-vtable-group.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 / merged PR #299
  - coordinator-promoted PR #301 writer-retention slice on coordinator PR #300
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
---

# Objective

Resolve the exact-build identity and role of the `0x2f69e30 / RTTI 0x3080748` address point that PR #301 currently labels as an intermediate retained object, and determine whether it narrows the first writer transform/framing edge. Do not repeat the stale queued final-socket run `31825417040` and do not enumerate generic QIODevice writers as semantic proof.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Canonical starting facts

- `TProtocolWriter` RTTI `0x3080728`, primary address point `0x2f69dd0`, derives from `TIODeviceWriter` RTTI `0x3080718`.
- PR #301 proves `TProtocolClientMessageProcessor -> retained intermediate object -> retained shared TProtocolWriter` and leaves the intermediate object's exact class UNKNOWN.
- In the reviewed RTTI/vtable artifact, `TProtocolWriter +0x50 = 0`, `+0x58 = 0x3080748`, `+0x60 = 0x7de7f0`; absolute address `0x2f69e30` is therefore a structurally adjacent Itanium address point inside the same emitted vtable group.
- Functions `0x7de7f0` and `0x7dfd60` write `0x2f69e30` into `[this]` during teardown-like paths and clean object fields around `+0x208..+0x238`.
- Historical table `0x3084c70 -> +0xd0 0xb40630` is a separate unresolved writer-family lead. It must not be conflated with canonical `TProtocolWriter` without provenance.

# Do not repeat

- queued run `31825417040` final-socket-write census;
- generic `QIODevice::write` enumeration;
- superseded `0xb5b880` gameplay endpoint model;
- disproven `0xb46bd0` binary gameplay sink model.

# Hypothesis

`0x2f69e30` is a secondary/base-class address point belonging to the canonical `TProtocolWriter` vtable group, with RTTI `0x3080748`; exact RTTI name/base relation and the corresponding virtual methods can identify the first concrete writer-stage boundary beyond the broad `TProtocolWriter` owner relation.

Competing outcomes:

1. exact type/subobject identity and relation to `TProtocolWriter` proven;
2. vtable-group relation proven but semantic type name remains unresolved;
3. apparent adjacency is an artifact and is disproven;
4. evidence remains insufficient.

# Acceptance gate

- [ ] exact source artifact digests verified before parsing;
- [ ] `0x2f69e30` classified using Itanium preamble/group structure, not address resemblance;
- [ ] RTTI `0x3080748` name/base relationship recovered if available from reviewed evidence;
- [ ] `0x7de7f0/0x7dfd60` role bounded from exact disassembly;
- [ ] relationship to PR #301 retention fact stated as FACT/INFERENCE/UNKNOWN without collapsing distinct objects;
- [ ] `0x3084c70/0xb40630` kept separate unless direct provenance intersects;
- [ ] framing/transform/final-egress claims remain UNKNOWN unless directly discriminated;
- [ ] no proprietary client bytes, credentials or account state committed/uploaded;
- [ ] exact-head CI terminal before handoff.

# Deliverable

Draft-only evidence/reproducer under the owned paths. Coordinator PR #300 remains promotion authority.
