---
task_id: OTC-20260815-track-a-p2-first-transform-boundary
status: ready
agent: unassigned
session_id: null
session_role: researcher
session_rotation_count: 0
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: runtime-research
phase: p2-first-transform-boundary
branch: research/OTC-20260815-track-a-p2-first-transform-boundary
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-first-transform-boundary
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 306
updated: 2026-08-15T17:13:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-first-transform-boundary.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-first-transform-boundary/**
  - .github/workflows/tibia-official-client-re-p2-first-transform-boundary.yml
  - .github/scripts/tibia-official-client-re-p2-first-transform-boundary.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
  - coordinator PR #300 head 5e6457b5afd717e3c92bb06a7219d8246c51f3b2 as pinned unmerged accepted-evidence dependency only
  - accepted #301 writer-retention snapshot under coordinator ownership
  - accepted #305 distinct-intermediate-type snapshot under coordinator ownership
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
context_pressure: medium
context_growth: stable
decomposition_decision: single
implementation_authorized: true
next_action: claim this task in a fresh researcher session, build one exact-client static reproducer that traces the first concrete data-transform call(s) from TProtocolClientMessageProcessor into the retained writer branch, run it on synology-otclient-01, and hand off a Draft-only bounded result with exact-head CI
---

# Objective

Resolve the next highest-information P2 question without duplicating final-socket work: identify the **first concrete serialization/data-transform boundary** on the accepted `TProtocolClientMessageProcessor -> retained writer` branch for the exact official native Linux Tibia client.

Research output remains Draft-only. Promotion authority is coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

Every build-specific result fails closed unless the exact size/SHA pair is reverified in the executing job.

# Pinned starting evidence

The following inputs are accepted by the coordinator but remain on unmerged coordinator PR #300, so consume them as pinned evidence dependencies rather than pretending they are already on `main`:

```text
#301 accepted boundary:
TProtocolClientMessageProcessor
 -> retained intermediate object
 -> retained shared TProtocolWriter

writer_relative_to_DualConnection:
INFERENCE_UPSTREAM_ON_CLIENT_PROCESSOR_BRANCH

direct_DualConnection_writer_member:
NOT_PROVEN

#305 accepted correction:
intermediate vptr 0x2f69e30 = FACT
intermediate typeinfo 0x3080748 = FACT
separate allocated retained object = FACT
simple secondary/base TProtocolWriter interpretation = DISPROVEN
semantic name/base relation of RTTI 0x3080748 = UNKNOWN
```

Canonical current-main #299 facts remain authoritative where applicable. If pinned coordinator evidence conflicts with current main or exact-binary reproduction, record `CONFLICT` and stop promotion of that claim.

# Explicit non-duplication boundary

Do **not** repeat or reinterpret these as this task's discriminator:

```text
- queued/historical final-socket-write run 31825417040;
- generic QIODevice::write callsite enumeration;
- generic Qt connect/QMeta census;
- vtable adjacency alone;
- owner +0x88 -> 0xb5b880 gameplay endpoint model (SUPERSEDED);
- 0xb46bd0 as binary gameplay-frame sink (DISPROVEN/SUPERSEDED);
- 0xc33259 as network/gameplay sink (DISPROVEN/SUPERSEDED);
- stale TProtocolWriter RTTI 0x3080700 (SUPERSEDED).
```

This task stops before proving the final socket/device egress unless the first-transform evidence independently and unambiguously reaches it; it must not dispatch a conceptual duplicate of the final-socket experiment.

# Hypothesis

A concrete call/reference path reachable from the proven `TProtocolClientMessageProcessor` retained-writer branch identifies the first method that changes the representation of an outbound semantic/generated client message into a lower-level byte/container form, or performs the first framing/sequence/compression/encryption transform.

Competing outcomes:

1. **TRANSFORM_EDGE_PROVEN** — one concrete call edge has exact object provenance plus discriminated input/output representation and transform role;
2. **SERIALIZATION_ONLY_PROVEN** — semantic/generated message -> byte/container conversion is proven, but framing/compression/encryption/sequence remain later/UNKNOWN;
3. **LIFECYCLE_ONLY** — reachable methods are construction/teardown/bookkeeping and do not establish a data transform;
4. **BYPASS_OR_SPLIT** — evidence shows materially different outbound branches rather than one retained-writer transform spine;
5. **INCONCLUSIVE** — exact evidence is insufficient and the transform boundary stays UNKNOWN.

# Planned discriminator

Build one exact-SHA static reproducer that works from concrete relocation/constructor/call provenance, not name proximity alone. It should:

1. re-resolve the accepted current-main processor/writer/intermediate identities from exact binary structures and relocations;
2. enumerate concrete call/xref sites that use the retained writer/intermediate object from `TProtocolClientMessageProcessor` construction/processing paths;
3. recover bounded disassembly around those sites and identify argument sources, return/use destinations, concrete virtual-slot targets where resolvable, and representation-changing library/helper calls;
4. classify any observed input/output representation conservatively (`generated semantic object`, `typed message object`, `QByteArray/byte buffer`, `device write`, or `UNKNOWN`) only when exact evidence supports it;
5. determine whether sequence/framing/compression/encryption helpers are before, inside, after, or not evidenced at the first proven boundary;
6. prove a negative control showing that generic QIODevice writes, adjacent vtables, old sink addresses, and teardown-only methods do not satisfy the transform gate;
7. emit machine-readable result plus a compact evidence report with exact binary SHA, tool versions, relevant offsets/addresses, classifications and remaining UNKNOWNs;
8. separate workflow execution success from semantic result.

If static evidence cannot discriminate representation semantics, preserve `UNKNOWN` and recommend one bounded next hypothesis rather than broadening into runtime traffic capture.

# Acceptance gate

- [ ] exact client SHA/size verified by the executing job;
- [ ] current-main #299 facts and pinned coordinator #301/#305 evidence are revalidated rather than blindly assumed;
- [ ] at least one retained-writer call/reference path is concretely tied back to `TProtocolClientMessageProcessor`, or a bounded negative result disproves the hypothesis;
- [ ] any claimed transform/serialization role has exact call/data provenance, not address/name coincidence;
- [ ] input/output representation is classified only where evidenced, with `UNKNOWN` retained elsewhere;
- [ ] framing/sequence/compression/encryption ordering is updated only when directly discriminated;
- [ ] negative controls reject generic QIODevice enumeration, vtable adjacency and superseded sink models;
- [ ] execution success and semantic result are recorded separately;
- [ ] no proprietary client bytes, credentials, account state, private chat or secret-bearing payloads are committed/uploaded;
- [ ] exact-head repository CI is terminal before Draft handoff.

# Side-effect budget

Static exact-build analysis only. No login, process attach, gameplay action, movement, market/trade/forge/currency effect, packet replay against live services, credential access, or runtime mutation is authorized.

# Deliverable

Draft PR only. Persist:

```text
docs/agents/evidence/OTC-20260815-track-a-p2-first-transform-boundary/
.github/scripts/tibia-official-client-re-p2-first-transform-boundary.py
.github/workflows/tibia-official-client-re-p2-first-transform-boundary.yml
```

plus this task record. The researcher must not edit coordinator/canonical knowledge paths or merge/promote its own result.