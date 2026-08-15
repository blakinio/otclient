---
task_id: OTC-20260815-track-a-p2-writer-vtable-group
status: validating
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
updated: 2026-08-15T14:20:00+02:00
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

# Successful discriminator

Task-specific workflow:

```text
Track A P2 writer vtable-group identity
run 31884166982
job 95010894063
executed head c479f58a1b45d6a4a2d4063d07ea83057532b8f7
result SUCCESS
```

The workflow independently fetched and SHA-verified all reviewed source artifacts before parsing:

```text
9231716774 / d99919403c001fbcc2a959346443c405f8a2234fb81438fbc6a626a1833edb82
9229609330 / bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c
9229251044 / 4b914f65d4a4eb3c91a39ce9918e8e4f865fadcf4853ab4af25ffa5d5f519520
```

Sanitized result artifact:

```text
id 9246799418
sha256 d0bf06e8c973f351fe96037445de0586f30e5044f5d1a097bfc866b85c0df48f
```

# FACT — distinct typed address point

Canonical `TProtocolWriter` remains:

```text
RTTI 0x3080728
primary address point 0x2f69dd0
offset-to-top 0
base TIODeviceWriter RTTI 0x3080718
```

The reviewed vtable window immediately following it resolves to a fresh normal Itanium tuple:

```text
0x2f69e20 = 0                  # offset-to-top
0x2f69e28 = 0x3080748         # distinct typeinfo
0x2f69e30 = 0x7de7f0          # first virtual target
0x2f69e38 = 0x7dfd60          # second virtual target
```

The setup artifact independently proves a separately allocated `0x250`-byte shared object whose actual object starts at allocation `+0x10` and receives vptr `0x2f69e30`.

Therefore `0x2f69e30` is not merely an address-adjacent scanner artifact.

# DISPROVEN

The simple hypothesis that `0x2f69e30` is just a secondary/base address point of canonical `TProtocolWriter` is rejected for the current evidence model:

- its typeinfo `0x3080748` differs from `TProtocolWriter` RTTI `0x3080728`;
- it also differs from `TIODeviceWriter` RTTI `0x3080718`;
- a distinct separately allocated object receives this vptr.

Do not collapse this object into canonical `TProtocolWriter` based on table adjacency.

# INFERENCE

Functions `0x7de7f0` and `0x7dfd60` are bounded as `TEARDOWN_LIKE`:

- both install `0x2f69e30` into `[this]`;
- `0x7de7f0` additionally releases linked/list state and clears object storage around `+0x208..+0x238`.

This is not a semantic symbol/name or transform-stage claim.

# UNKNOWN

- semantic type name for RTTI `0x3080748`;
- base/inheritance relationship represented by RTTI `0x3080748`;
- first writer transform/framing boundary;
- gameplay framing/serialization order;
- final binary QIODevice/socket egress;
- relationship of historical `0x3084c70 -> +0xd0 -> 0xb40630` family to canonical writer branch.

The historical `0x3084c70` lead remains structurally separate: its reviewed artifact has RTTI zero, no direct LEA xrefs, and `+0xd0 -> 0xb40630`. No provenance intersection is claimed.

# Effect on accepted PR #301

The accepted retention relation remains valid:

```text
TProtocolClientMessageProcessor
 -> retained intermediate object
 -> retained shared TProtocolWriter
```

The intermediate object can now be sharpened to:

```text
vptr 0x2f69e30
Itanium typeinfo 0x3080748
semantic type name UNKNOWN
not collapsible into canonical TProtocolWriter by adjacency
```

# Evidence

- `docs/agents/evidence/OTC-20260815-track-a-p2-writer-vtable-group/20260815-distinct-adjacent-vtable.md`
- `docs/agents/evidence/OTC-20260815-track-a-p2-writer-vtable-group/result.json`
- `.github/scripts/tibia-official-client-re-p2-writer-vtable-group.py`
- `.github/workflows/tibia-official-client-re-p2-writer-vtable-group.yml`

# Acceptance gate

- [x] exact source artifact digests verified before parsing;
- [x] `0x2f69e30` classified from Itanium preamble/address layout rather than resemblance;
- [x] RTTI name/base relation left UNKNOWN because reviewed artifacts do not provide a proven name/relationship;
- [x] `0x7de7f0/0x7dfd60` role bounded without overclaiming;
- [x] relationship to PR #301 sharpened without collapsing distinct objects;
- [x] `0x3084c70/0xb40630` kept separate absent provenance;
- [x] framing/transform/final-egress remain UNKNOWN;
- [x] no proprietary client bytes, credentials or account state committed/uploaded;
- [ ] exact final-head task-specific workflow and standard PR CI terminal after durable evidence checkpoint.

# Proposed researcher disposition

`ACCEPT_WITH_EDITS` as bounded negative/type-structure evidence.

P2 remains incomplete. The next transform-order hypothesis must use actual serialization/data-stream behavior or independently recover the semantic role of RTTI `0x3080748`; vtable adjacency alone is insufficient.

# Next action

Validate the current durable checkpoint head with both the task-specific provenance workflow and standard PR CI. If terminal green, set task status `ready`, validate the final bookkeeping head, and hand the Draft back to coordinator #300 for independent review.
