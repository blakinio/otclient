---
task_id: OTC-20260903-be4f48-prelogin-sequence-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260903-be4f48-prelogin-sequence-promotion
base_branch: main
base_main: 05a0befa9670b164e5d88046584899ae3aaebb29
created: 2026-09-03T17:28:00+02:00
risk: high
execution_class: github_hosted
execution_mode: chat_github
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
physical_e2e_required: false
implementation_authorized: false
owned_paths:
  - docs/agents/evidence/OTC-20260903-be4f48-prelogin-sequence-promotion/**
  - docs/agents/tasks/active/OTC-20260903-be4f48-prelogin-sequence-promotion.md
modules_touched: []
reuses:
  - source Draft PR #865 exact-current static evidence at 8d6c752cd3d009a78b5deddb650c752c95156298
  - exact-current writer run 32998976901 at 3d87d729b73f868aefe1662c72af666a4921b1d8
blocks:
  - Track B PR #284 next material outbound hypothesis
---

# Objective

Promote only independently verified exact-current source facts for Linux Tibia `15.32.be4f48` (`52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`) from source Draft PR #865 and the already-existing exact-current writer evidence. Preserve the fail-closed SOURCE_BLOCKER result. Do not promote the source analyzer/workflow and do not mutate Track B PR #284.

# Acceptance

1. Preserve exact source PR/head/run/job/artifact identities and result digests.
2. Promote `GameclientMessageLogin.field6` as structurally PRESENT and sourced from producer input `edx`, while keeping its exact value/semantic name UNKNOWN.
3. Promote the exact-current `TProtocolMessageQueue::sendLogin` QMeta target and unique adapter edge only; do not infer causal pre-login ordering from an xref.
4. Record that the current connection peer does not map to `TGameClient` QMeta and that the bounded pre-success send sequence remains UNKNOWN.
5. Record the independent exact-current writer boundary: current sendLogin QMeta/first direct edge/adapter FDE/adapter indirect calls are proven, but the final writer contract remains UNKNOWN.
6. Explicitly keep Track B payload mutation and any new official-service E2E unauthorized from this result.
7. Exact-head required promotion CI/governance and full diff review must pass before merge; the source evidence already carries exact-head self-hosted boundary run `33756449971=SUCCESS`.
8. After merge, close source PR #865 unmerged as consumed and archive this promotion task in a separate narrow lifecycle PR.

# Source evidence

```text
source PR             #865
source head           8d6c752cd3d009a78b5deddb650c752c95156298
source workflow       33756449924 = SUCCESS
source job            100651924970 = SUCCESS
source CI             33756450210 = SUCCESS
source governance     33756449991 = SUCCESS
source boundary       33756449971 = SUCCESS
source artifact       9893838828
artifact sha256       20043e76288cf7377c480015a1c2726fb76f39fd1366e43faae445c3bfd87cee
result.json sha256    c44a1cdd3f20a84da4ca3c8ec6970a0dc86ef46c89ee8cd348db7d46729a2d37

writer run             32998976901 = SUCCESS
writer head            3d87d729b73f868aefe1662c72af666a4921b1d8
writer artifact        9886703883
writer artifact sha256 84e88080ea862d2faf82fc169dde5f908fc5fd7a856585e434523795481fc4fa
writer result sha256   296f5a915d15f9383fc3f1c7809eb5c6934a3deb24a9e2b9cd1808b660c40f14
```

# Promotion validation history

Initial promotion head `5e2878502292b0344d4a84959b53b903acc83e50` had main CI `33773362539=SUCCESS` and fresh admission behavior audit SUCCESS, but deterministic governance job `100708897807` failed before merge because this static/no-runtime coordinator task omitted the mandatory Track A admission metadata fields. The fix is metadata-only: all runtime authority fields are now explicitly `NOT_APPLICABLE` under `runtime_access: none`. No promoted evidence or decision changed.

# Decision

`terminal_result=SOURCE_BLOCKER`.

`GameclientMessageLogin.field6` is present in the exact-current producer and is written from the producer input `edx`, but the value remains UNKNOWN. The exact-current `sendLogin` QMeta entry uniquely tail-transfers to adapter `0xbd3050`; however, the current connection block peer target `0xd052a0` has no `TGameClient` QMeta candidate and bounded root reachability remains `UNKNOWN_PEER_QMETA_IDENTITY`. Therefore causal sender-side ordering is not proven.

The independent exact-current writer run proves current `sendLogin` QMeta, the first direct edge, the adapter FDE and adapter indirect calls, but classifies `final_writer_contract=UNKNOWN`. No source-only evidence currently proves a safe Track B wire-value mutation.

# Track B consequence

PR #284 remains unchanged. Do not add a guessed Field6 constant, do not infer a pre-login message order from the adapter xref, and do not spend another official-service E2E on this evidence cut.

```text
PRE_LOGIN_SEQUENCE_COMPLETE=false
PRE_LOGIN_MESSAGE_ORDER=UNKNOWN
PRE_LOGIN_REQUIRED_MESSAGE_MISSING_IN_OTCLIENT=UNKNOWN
FIELD6_VALUE=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
terminal_result=SOURCE_BLOCKER
```

next_action: require exact-head promotion checks and review, squash-merge the clean docs-only promotion, close source PR #865 unmerged as consumed, then archive this promotion lifecycle. Do not relaunch the #865 analyzer without a new concrete failing discriminator.
