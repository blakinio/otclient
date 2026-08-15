---
task_id: OTC-20260815-track-a-p2-writer-vtable-group
status: ready
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
updated: 2026-08-15T14:23:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-writer-vtable-group.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-writer-vtable-group/**
  - .github/workflows/tibia-official-client-re-p2-writer-vtable-group.yml
  - .github/scripts/tibia-official-client-re-p2-writer-vtable-group.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 / merged PR #299
  - accepted PR #301 writer-retention evidence under coordinator PR #300
  - reviewed exact-build artifact 9231716774 from run 31833767461
  - reviewed exact-build artifact 9229609330 from run 31828102313
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
claim_check: passed against exact main, Draft PR #305, released coordinator #300 and disjoint active RUNTIME #303
semantic_result: PROVEN_DISTINCT_ADJACENT_ITANIUM_VTABLE_IDENTITY_NAME_UNKNOWN
proposed_disposition: ACCEPT_WITH_EDITS
successful_run: 31884166982
successful_job: 95010894063
sanitized_result_artifact_id: 9246799418
sanitized_result_artifact_sha256: d0bf06e8c973f351fe96037445de0586f30e5044f5d1a097bfc866b85c0df48f
validated_checkpoint_head: dcf5e1e11d30cd42608c4e071618f521729ee4e0
validated_checkpoint_task_run: 31884286098
validated_checkpoint_pr_ci: 31884288165
stop_reason: bounded vtable-group hypothesis resolved; intermediate object is structurally distinct from canonical TProtocolWriter by typeinfo/object provenance, but semantic RTTI name and transform/framing boundary remain UNKNOWN
---

# Objective

Resolve the exact-build identity and role of `0x2f69e30 / RTTI 0x3080748`, previously the intermediate retained object in accepted PR #301, and determine whether the reviewed evidence narrows the first writer transform/framing edge without repeating final-socket or generic-QIODevice experiments.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Result

```text
P2_VTABLE_GROUP_RESULT=PROVEN_DISTINCT_ADJACENT_ITANIUM_VTABLE_IDENTITY_NAME_UNKNOWN
P2_FIRST_WRITER_TRANSFORM_BOUNDARY=UNKNOWN
```

Successful semantic workflow: run `31884166982`, job `95010894063`, exact executed head `c479f58a1b45d6a4a2d4063d07ea83057532b8f7`.

The workflow SHA-verifies three reviewed exact-build text artifacts before parsing:

```text
9231716774 / d99919403c001fbcc2a959346443c405f8a2234fb81438fbc6a626a1833edb82
9229609330 / bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c
9229251044 / 4b914f65d4a4eb3c91a39ce9918e8e4f865fadcf4853ab4af25ffa5d5f519520
```

# FACT

Canonical `TProtocolWriter` remains RTTI `0x3080728`, primary address point `0x2f69dd0`, base `TIODeviceWriter` RTTI `0x3080718`.

The reviewed vtable window immediately following it resolves to a fresh normal Itanium tuple:

```text
0x2f69e20 = 0
0x2f69e28 = 0x3080748
0x2f69e30 = 0x7de7f0
0x2f69e38 = 0x7dfd60
```

A separate reviewed setup artifact proves a separately allocated `0x250`-byte shared object receives vptr `0x2f69e30` at its actual object start.

Thus the PR #301 intermediate object is structurally sharpened to:

```text
vptr 0x2f69e30
Itanium typeinfo 0x3080748
semantic type name UNKNOWN
separately allocated object
```

# DISPROVEN

The simple hypothesis that `0x2f69e30` should be treated as merely a secondary/base address point of canonical `TProtocolWriter` from table adjacency is rejected:

- its typeinfo differs from canonical `TProtocolWriter` and `TIODeviceWriter` typeinfo;
- a distinct separately allocated object receives this vptr.

# INFERENCE

`0x7de7f0` / `0x7dfd60` are bounded as teardown-like: both install `0x2f69e30`; `0x7de7f0` also releases linked/list state and clears object storage around `+0x208..+0x238`.

No semantic type symbol or writer-transform stage is inferred from that cleanup behavior.

# UNKNOWN

- semantic name for RTTI `0x3080748`;
- inheritance/base relationship of RTTI `0x3080748`;
- first writer transform/framing boundary;
- gameplay framing/serialization order;
- final binary QIODevice/socket egress;
- relationship of historical `0x3084c70 -> +0xd0 -> 0xb40630` to the canonical writer branch.

Historical `0x3084c70` remains separate: reviewed evidence reports RTTI zero, no direct LEA xrefs and `+0xd0 -> 0xb40630`.

# Evidence

- `docs/agents/evidence/OTC-20260815-track-a-p2-writer-vtable-group/20260815-distinct-adjacent-vtable.md`
- `docs/agents/evidence/OTC-20260815-track-a-p2-writer-vtable-group/result.json`
- `.github/scripts/tibia-official-client-re-p2-writer-vtable-group.py`
- `.github/workflows/tibia-official-client-re-p2-writer-vtable-group.yml`

# Validation

Durable checkpoint head `dcf5e1e11d30cd42608c4e071618f521729ee4e0`:

- task-specific run `31884286098` = SUCCESS;
- standard PR CI `31884288165`, including `CI / Required` = SUCCESS;
- changed paths confined to declared task roots;
- review threads = 0.

This final `status: ready` commit changes task handoff bookkeeping only and requires its own exact-head validation before coordinator consumption.

# Proposed disposition

`ACCEPT_WITH_EDITS` as bounded negative/type-structure evidence.

P2 remains incomplete. A later transform-order hypothesis must use actual serialization/data-stream behavior or independently recover RTTI `0x3080748` semantics; vtable adjacency alone is insufficient.

# Handoff

Researcher ownership is released by `status: ready`. Coordinator PR #300 must refetch the exact final #305 head and final-head validation before authoritative promotion. Researcher proposal is not canonical authority.
