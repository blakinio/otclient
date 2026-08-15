---
task_id: OTC-20260815-track-a-p2-first-transform-boundary
status: ready
agent: ChatGPT
session_id: chatgpt-p2-transform-researcher-20260815-1724
session_role: researcher
session_rotation_count: 1
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
updated: 2026-08-15T17:40:00+02:00
lease_released_at: 2026-08-15T17:40:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-first-transform-boundary.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-first-transform-boundary/**
  - .github/workflows/tibia-official-client-re-p2-first-transform-boundary.yml
  - .github/scripts/tibia-official-client-re-p2-first-transform-boundary.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
  - coordinator PR #300 accepted #301/#305 evidence as pinned unmerged dependency only
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
invocation_started_at: 2026-08-15T17:24:00+02:00
last_progress_at: 2026-08-15T17:40:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-handoff
terminal_ci_wait_started_at: 2026-08-15T17:40:00+02:00
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 1
stall_warnings: 0
claim_check: task was ready/unassigned, PR #306 remained open Draft/mergeable, main remained 8fca1c3, and no other worker owned this branch during the research session
semantic_run: 31893080162
semantic_job: 95032159933
semantic_head: f471bfc0b67046bdd917ea6e10a2e22af7f8d00f
semantic_artifact: 9249061176
semantic_artifact_digest: sha256:2604ddaddd7381de0797ccfdc1c027ac49f66175485012647a4804a98e100130
semantic_result: SERIALIZATION_ONLY_PROVEN
first_concrete_non_lifecycle_slot: 0xc10960
next_serializer_slot: 0xc20290
adjacent_qbuffer_slot: 0xc20c70
framing_order: UNKNOWN
sequence_order: UNKNOWN
compression_order: UNKNOWN
encryption_order: UNKNOWN
final_binary_egress: UNKNOWN
causal_local_harness: UNKNOWN
last_checkpoint:
  - docs/agents/evidence/OTC-20260815-track-a-p2-first-transform-boundary/RESULT.json
  - docs/agents/evidence/OTC-20260815-track-a-p2-first-transform-boundary/STATUS.json
  - docs/agents/evidence/OTC-20260815-track-a-p2-first-transform-boundary/20260815-first-serialization-boundary.md
next_action: coordinator PR #300 must independently review and either ACCEPT, ACCEPT_WITH_EDITS, RETURN_FOR_EVIDENCE, or REJECT this Draft result; safe promotion is bounded to SERIALIZATION_ONLY_PROVEN and the exact retention/call/data facts, while pipeline ordering, final egress and local harness remain UNKNOWN
---

# Objective

Identify the first concrete serialization/data-transform boundary on the coordinator-accepted `TProtocolClientMessageProcessor -> retained intermediate -> retained shared TProtocolWriter` branch for the exact official native Linux Tibia client.

Research output remains Draft-only. Promotion authority is coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Proven retained branch — FACT

Exact-binary reproduction independently revalidates:

```text
TProtocolClientMessageProcessor
 -> retained intermediate object (vptr 0x2f69e30, typeinfo 0x3080748)
 -> retained shared TProtocolWriter (vtable AP 0x2f69dd0, RTTI 0x3080728)
```

The intermediate is a separate allocated retained object. Direct DualConnection writer ownership remains NOT_PROVEN.

# Semantic result

`SERIALIZATION_ONLY_PROVEN`

The first two intermediate slots are lifecycle-like:

```text
+0x00 -> 0x7de7f0
+0x08 -> 0x7dfd60
```

The first concrete non-lifecycle slot is:

```text
+0x10 -> 0xc10960
```

Exact disassembly proves that this slot:

- reads the retained writer through intermediate member `+0x18`;
- reads a message-derived dispatch value;
- serializes it through `QDataStream::operator<<(signed char)`.

The next serializer slot:

```text
+0x18 -> 0xc20290
```

preserves the argument pointer (`rbx <- rsi`), reads structured fields at argument `+0x30` and `+0x34`, and serializes them with `QDataStream::operator<<(signed short)`.

Adjacent slot:

```text
+0x20 -> 0xc20c70
```

constructs `QBuffer`, but adjacency alone does not establish its temporal order relative to the proven serializers.

# Explicit UNKNOWN boundary

The following remain `UNKNOWN`:

- whether `0xc10960` is temporally first in the complete outbound pipeline;
- QBuffer order relative to serializer calls;
- framing order;
- sequence-number order;
- compression boundary/order;
- encryption boundary/order;
- final binary egress/socket ownership;
- causal local harness.

# Execution provenance

Semantic workflow execution:

- run `31893080162`;
- job `95032159933`;
- head `f471bfc0b67046bdd917ea6e10a2e22af7f8d00f`;
- runner `synology-otclient-01`;
- artifact `9249061176`;
- digest `sha256:2604ddaddd7381de0797ccfdc1c027ac49f66175485012647a4804a98e100130`;
- conclusion `SUCCESS`.

The artifact contains only machine-readable result, validation markers and sanitized text disassembly. No proprietary client bytes were uploaded.

# Explicit non-duplication / negative controls

Not used as proof:

- final-socket run `31825417040`;
- generic QIODevice::write enumeration;
- generic Qt/QMeta census;
- vtable adjacency alone;
- superseded `0xb5b880`, `0xb46bd0`, `0xc33259` sink models;
- stale writer RTTI `0x3080700`.

# Acceptance gate

- [x] exact client SHA/size verified by the executing job;
- [x] current-main / pinned writer-intermediate facts independently revalidated against the exact binary;
- [x] retained-writer call/data path concretely tied through the processor-retained intermediate;
- [x] claimed serialization role has exact call/data provenance;
- [x] input/output representation is conservative and UNKNOWN preserved where necessary;
- [x] framing/sequence/compression/encryption ordering changed only where directly supported — therefore remains UNKNOWN;
- [x] negative controls reject generic QIODevice/vtable/superseded sink models;
- [x] execution success and semantic result recorded separately;
- [x] no proprietary client bytes, credentials, account state or secret payloads committed/uploaded;
- [x] code/workflow head `da94bcb21d82a05f043a4ec8c87816820342090e` passed repository `CI / Required` before the final evidence/handoff commit;
- [ ] final handoff head repository CI and static workflow are pending at commit creation time and must be terminal green before coordinator consumption.

# Side-effect budget

Static exact-build analysis only. No login, process attach, gameplay action, movement, packet replay, credential access, account state or runtime mutation occurred.
