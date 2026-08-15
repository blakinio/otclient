---
task_id: OTC-20260815-track-a-p2-post-serialization-buffer-boundary
status: active
agent: ChatGPT
session_id: chatgpt-p2-buffer-researcher-20260815-2107
session_role: researcher
session_rotation_count: 1
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
updated: 2026-08-15T21:07:00+02:00
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
execution_reason: exact-build static ELF/disassembly discriminator on owned P2 paths; no runtime needed
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
implementation_authorized: true
invocation_started_at: 2026-08-15T21:07:00+02:00
last_progress_at: 2026-08-15T21:07:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: buffer-dataflow-discovery
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
next_action: implement and execute one exact-client static reproducer that independently revalidates the promoted QDataStream serializer facts and proves or boundedly rejects shared QDataStream/QBuffer/byte-container state through concrete data provenance
---

# Objective

Determine the next concrete representation/data-flow boundary after the coordinator-promoted QDataStream serialization facts for the exact official native Linux Tibia client:

```text
TProtocolClientMessageProcessor
  -> retained intermediate AP 0x2f69e30 / RTTI 0x3080748
  -> retained TProtocolWriter AP 0x2f69dd0 / RTTI 0x3080728
  -> QDataStream serialization at 0xc10960 and 0xc20290
```

Research output remains Draft-only. Promotion authority is coordinator PR #300.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Promoted starting facts to revalidate

- `+0x10 -> 0xc10960` uses intermediate member `+0x18` and serializes a message-derived value through `QDataStream::operator<<(signed char)`;
- `+0x18 -> 0xc20290` uses the same retained writer branch and serializes structured fields through QDataStream insertion;
- `+0x20 -> 0xc20c70` constructs `QBuffer`;
- relation/order between serializer and QBuffer is UNKNOWN;
- final egress, framing, sequence, compression and encryption remain UNKNOWN.

# Required discriminator

1. Revalidate exact client identity, intermediate/writer RTTI/address points, retention setup and serializer slots from the exact ELF.
2. Recover concrete QDataStream sink object/member provenance in `0xc10960` / `0xc20290`.
3. Recover QBuffer/byte-container construction/use provenance in `0xc20c70` and directly related calls.
4. Classify common versus split state only from exact member stores/loads, constructor args, QDataStream device binding or direct control/data flow.
5. Claim temporal order only from actual control/data flow, never vtable adjacency.
6. Distinguish QBuffer/container management from protocol framing.
7. Preserve UNKNOWN for sequence/compression/encryption/final egress unless directly proven.
8. Emit machine-readable result plus sanitized bounded disassembly/provenance evidence; workflow success and semantic outcome remain separate.

# Allowed semantic outcomes

- `BUFFER_DATAFLOW_PROVEN`
- `SERIALIZATION_TARGET_PROVEN_BUFFER_ORDER_UNKNOWN`
- `BUFFER_INDEPENDENT_OR_SPLIT`
- `FRAMING_EDGE_PROVEN`
- `INCONCLUSIVE`

# Negative controls / forbidden shortcuts

Do not use vtable adjacency, generic QIODevice/QBuffer/QByteArray census, generic Qt/QMeta census, final-socket run `31825417040`, superseded `0xb5b880/0xb46bd0/0xc33259`, stale writer RTTI `0x3080700`, or unproven direct DualConnection writer ownership as proof.

# Acceptance gate

- [ ] exact client SHA/size verified by executing job;
- [ ] promoted retained intermediate/writer/serializer facts independently revalidated;
- [ ] QDataStream sink object/member provenance recovered;
- [ ] QBuffer/byte-container object/member provenance recovered;
- [ ] common or split data-flow relationship classified from exact evidence;
- [ ] temporal order claimed only if direct control/data-flow evidence supports it;
- [ ] framing distinguished from container management;
- [ ] sequence/compression/encryption/final egress remain UNKNOWN unless directly proven;
- [ ] negative controls enforced;
- [ ] execution success and semantic outcome separate;
- [ ] no proprietary client bytes, credentials, account state or secret payloads committed/uploaded;
- [ ] exact-head repository CI terminal before Draft handoff;
- [ ] task released as `ready` for coordinator review rather than merged.

# Side-effect budget

Static exact-build analysis only. No client launch, process attach, login, credential access, live packet replay, movement, gameplay, account state or runtime mutation is authorized.
