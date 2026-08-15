---
task_id: OTC-20260815-track-a-p2-writer-ownership
status: active
agent: ChatGPT
session_id: chatgpt-p2-researcher-20260815-1344
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: runtime-research
phase: p2-writer-ownership
branch: research/OTC-20260815-track-a-p2-writer-ownership
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-writer-ownership
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 301
updated: 2026-08-15T13:44:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-writer-ownership.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-writer-ownership/**
  - .github/workflows/tibia-official-client-re-p2-writer-ownership.yml
  - .github/scripts/tibia-official-client-re-p2-writer-ownership.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 / merged PR #299
  - coordinator PR #300 for promotion authority
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
claim_check: passed against main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45, open Draft PR #301 head 29ca506501efc716330a80ab2b96eaf9bbe3d4d5, status ready/unassigned and released coordinator task #300
---

# Objective

Resolve the next concrete P2 edge for the exact official native Linux Tibia client without repeating a queued or disproven experiment: recover the concrete ownership/construction/virtual-dispatch path from the already-proven `TGameserverDualConnection` into the actual `TProtocolWriter` / `TIODeviceWriter` writer object.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

Every build-specific result fails closed unless this exact identity is verified.

# Canonical starting facts

- merged #299 places `TGameserverDualConnection` on the corrected outbound ownership chain;
- `TProtocolWriter : TIODeviceWriter` exact-build RTTI relationship is accepted;
- `TGameserverTCPConnection` and its concrete `QTcpSocket*` member at receiver `+0x10` are accepted;
- `0xb46bd0` is not the binary gameplay sink;
- `0xc33259` is not a network/gameplay binary sink;
- the old `owner+0x88 -> 0xb5b880` gameplay endpoint model is superseded.

# Bounded historical exact-build leads — revalidation inputs only

- queue/network handoff evidence proves `clientMessageReadyToProcess` reaches the containing network owner virtual slot `+0x90`, with the queue at owner `+0x88` and QTcpSocket construction in the same owner setup path;
- relocation-aware writer census found a structurally plausible table/address point `0x3084c70` with `+0xd0 -> 0xb40630`; `0xb40630` performs virtual pre/post hooks around a concrete `QIODevice::write(QByteArray const&)` call;
- the class/object provenance of `0x3084c70` and its intersection with the canonical game-session/network-owner graph remain UNKNOWN;
- a historical nested allocation vtable `0x2f69168` is not the containing-owner primary vtable.

These leads cannot override merged #299 and are not semantic proof by themselves.

# Do not repeat

```text
DISPROVEN/SUPERSEDED:
- owner +0x88 -> 0xb5b880 as gameplay endpoint
- generic QIODevice::write callsite enumeration as semantic proof
- 0xb46bd0 as binary gameplay-frame sink
- 0xc33259 as network/gameplay binary sink

ACTIVE NONCANONICAL QUEUE:
- run 31825417040 final-socket-write resolution; do not dispatch a conceptual duplicate
```

# Hypothesis

A concrete retained field, constructor path, factory, or virtual dispatch reachable from the proven `TGameserverDualConnection` ownership graph identifies an actual `TProtocolWriter`/`TIODeviceWriter` instance or subobject and discriminates the next outbound transformation edge.

Competing outcomes:

1. direct writer ownership/reference proven;
2. writer indirectly owned by another retained object;
3. current graph lead does not reach the RTTI-proven writer and is disproven;
4. evidence insufficient and remains UNKNOWN.

# Planned discriminator

Build one exact-SHA static reproducer that does **not** enumerate generic QIODevice callsites as proof. It will:

1. resolve current accepted type identities/RTTI/vtables from exact strings + Itanium structures/relocations rather than trusting stale raw offsets;
2. recover `TGameserverDualConnection` constructor/vptr provenance and retained object/member writes;
3. recover `TProtocolWriter` / `TIODeviceWriter` vtable/address-point provenance and constructor/factory references;
4. test whether any concrete retained field/store/call path intersects those two graphs;
5. separately classify the historical `0x3084c70 -> 0xb40630` writer family as intersecting, unrelated, or unresolved;
6. require a negative control showing that old `0xb46bd0` / `0xb5b880` evidence does not satisfy the provenance gate;
7. report execution success separately from semantic result.

If the exact binary execution environment is unavailable, persist a precise WAITING blocker rather than weakening the semantic gate.

# Acceptance gate

- [ ] exact client identity hard-fenced;
- [ ] current-main #299 facts used;
- [ ] concrete constructor/member/reference/virtual-dispatch evidence ties `TGameserverDualConnection` to writer type, or a bounded negative result disproves the hypothesis;
- [ ] relocation/RTTI/vtable candidates validated as Itanium structures;
- [ ] negative control rejects generic writer/address coincidence;
- [ ] execution success separate from semantic result;
- [ ] framing/encryption/final egress remain UNKNOWN unless directly discriminated;
- [ ] no credentials/proprietary binary bytes/secret-bearing payloads/account state persisted;
- [ ] exact-head repository CI terminal before Draft handoff.

# Side-effect budget

Static exact-build analysis only unless a later read-only live discriminator becomes materially necessary. No gameplay action, login, currency, market, trade, forge or irreversible effect is authorized by this task.

# Deliverable

Draft PR #301 only. Produce a bounded task-scoped reproducer/evidence report and then release the task for coordinator review; do not promote canonical claims from this branch.
