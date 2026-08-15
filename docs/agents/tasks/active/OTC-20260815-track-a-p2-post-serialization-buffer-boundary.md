---
task_id: OTC-20260815-track-a-p2-post-serialization-buffer-boundary
status: ready
agent: unassigned
session_id: null
session_role: researcher
session_rotation_count: 0
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: runtime-research
phase: p2-post-serialization-buffer-boundary
branch: research/OTC-20260815-track-a-p2-post-serialization-buffer-boundary
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-post-serialization-buffer-boundary
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 308
created: 2026-08-15T17:49:00+02:00
updated: 2026-08-15T17:50:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-post-serialization-buffer-boundary.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-post-serialization-buffer-boundary/**
  - .github/workflows/tibia-official-client-re-p2-post-serialization-buffer-boundary.yml
  - .github/scripts/tibia-official-client-re-p2-post-serialization-buffer-boundary.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
  - coordinator PR #300 promoted #306 serialization evidence as pinned unmerged dependency only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
implementation_authorized: true
next_action: a fresh independent researcher must claim this task, independently revalidate the promoted retained-writer/QDataStream boundary against the exact client, then prove or boundedly reject a concrete data-flow relationship between the serializer state and QBuffer/byte-container state without using vtable adjacency as temporal proof
---

# Objective

Determine the next concrete representation/data-flow boundary after the coordinator-promoted QDataStream serialization facts on the exact official native Linux Tibia client branch:

```text
TProtocolClientMessageProcessor
  -> retained intermediate AP 0x2f69e30 / RTTI 0x3080748
  -> retained TProtocolWriter AP 0x2f69dd0 / RTTI 0x3080728
  -> proven QDataStream serialization at intermediate slots 0xc10960 and 0xc20290
```

The prior source Draft #306 is closed unmerged. Coordinator PR #300 is the canonical promotion authority. The new researcher may use its promoted snapshot only as a pinned dependency and must revalidate load-bearing facts against the exact binary.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Promoted starting FACT

- first two intermediate slots `0x7de7f0`, `0x7dfd60` are lifecycle-like;
- `+0x10 -> 0xc10960` accesses retained writer member `+0x18` and invokes `QDataStream::operator<<(signed char)` on a message-derived value;
- `+0x18 -> 0xc20290` serializes structured fields `+0x30/+0x34` via `QDataStream::operator<<(signed short)`;
- adjacent `+0x20 -> 0xc20c70` constructs `QBuffer`;
- the temporal/data-flow relation between these facts is still `UNKNOWN`.

# Required discriminator

The researcher must trace **actual shared state/data flow**, not table adjacency. At minimum:

1. revalidate the exact retained intermediate/writer setup and serializer slot identities from the exact ELF;
2. recover the exact object/member state used by `0xc10960` / `0xc20290` as the QDataStream sink;
3. recover the exact object/member state created or used by `0xc20c70` and any directly related buffer-owning methods;
4. determine whether both operations can be tied to the same writer/intermediate-owned QIODevice/QBuffer/byte-container object through concrete member stores, loads, constructor arguments, QDataStream device binding, or direct call/data provenance;
5. if a common state is proven, classify the representation boundary conservatively (for example structured fields -> QDataStream -> QBuffer-backed byte container);
6. determine temporal order only from direct control/data flow or call relationships, never from vtable slot order;
7. if framing is observed, distinguish raw serialized payload/container construction from protocol framing and do not call generic length/container management "framing" without exact evidence;
8. preserve `UNKNOWN` for sequence/compression/encryption/final egress unless directly discriminated;
9. emit machine-readable result and sanitized exact disassembly/data-provenance evidence;
10. keep workflow execution success separate from the semantic result.

# Allowed semantic outcomes

- `BUFFER_DATAFLOW_PROVEN`
- `SERIALIZATION_TARGET_PROVEN_BUFFER_ORDER_UNKNOWN`
- `BUFFER_INDEPENDENT_OR_SPLIT`
- `FRAMING_EDGE_PROVEN`
- `INCONCLUSIVE`

Any positive outcome must include exact member/call/data provenance.

# Explicit negative controls / do not duplicate

Do **not** use as proof:

- vtable adjacency (`0xc10960`, `0xc20290`, `0xc20c70`) by itself;
- generic `QIODevice::write` or QBuffer/QByteArray census;
- generic Qt/QMeta census;
- final-socket run `31825417040`;
- superseded sink addresses `0xb5b880`, `0xb46bd0`, `0xc33259`;
- stale writer RTTI `0x3080700`;
- direct DualConnection writer ownership, which remains NOT_PROVEN.

# Acceptance gate

- [ ] exact client SHA/size verified by executing job;
- [ ] promoted retained intermediate/writer/serializer facts independently revalidated;
- [ ] QDataStream sink object/member provenance recovered;
- [ ] QBuffer/byte-container object/member provenance recovered;
- [ ] common or split data-flow relationship classified from exact evidence;
- [ ] temporal order claimed only if direct control/data-flow evidence supports it;
- [ ] framing distinguished from container management;
- [ ] sequence/compression/encryption/final egress stay UNKNOWN unless directly proven;
- [ ] negative controls explicitly enforced;
- [ ] execution success and semantic outcome recorded separately;
- [ ] no proprietary client bytes, credentials, account state or secret payloads committed/uploaded;
- [ ] exact-head repository CI terminal before Draft handoff;
- [ ] researcher releases task as `ready` for coordinator review rather than merging it.

# Side-effect budget

Static exact-build analysis only. No client launch, process attach, login, credential access, live packet replay, movement, gameplay, account state or runtime mutation is authorized.
