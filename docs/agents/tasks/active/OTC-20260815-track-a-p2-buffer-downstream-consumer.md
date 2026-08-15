---
task_id: OTC-20260815-track-a-p2-buffer-downstream-consumer
status: active
agent: ChatGPT
session_id: chatgpt-p2-downstream-researcher-20260815-2140
session_role: researcher
session_rotation_count: 1
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: runtime-research
phase: p2-buffer-downstream-consumer
branch: research/OTC-20260815-track-a-p2-buffer-downstream-consumer
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-buffer-downstream-consumer
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: null
created: 2026-08-15T21:40:00+02:00
updated: 2026-08-15T21:40:00+02:00
lease_expires_at: 2026-08-15T22:25:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-buffer-downstream-consumer.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-buffer-downstream-consumer/**
  - .github/workflows/tibia-official-client-re-p2-buffer-downstream-consumer.yml
  - .github/scripts/tibia-official-client-re-p2-buffer-downstream-consumer.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
  - coordinator PR #300 ACCEPT_WITH_EDITS promotion of closed-unmerged PR #308 as pinned evidence only
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
execution_reason: exact-build static ELF/disassembly discriminator from promoted retained QBuffer-backed QDataStream boundary
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
implementation_authorized: true
invocation_started_at: 2026-08-15T21:40:00+02:00
last_progress_at: 2026-08-15T21:40:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: initial-downstream-inventory
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
active_operation: recover the first exact downstream consumer/transform after the promoted persistent QBuffer-backed byte container using type-anchored static evidence
next_action: inventory exact TProtocolWriter and retained-intermediate callable slots plus bounded construction/use references, then isolate the first function that reads/exposes/transforms retained byte-container state; produce a semantic result without using generic census or historical final-socket evidence
---

# Objective

Start from the coordinator-promoted P2 boundary:

```text
TProtocolClientMessageProcessor
  -> retained intermediate AP 0x2f69e30 / RTTI 0x3080748
  -> retained TProtocolWriter AP 0x2f69dd0 / RTTI 0x3080728
  -> retained helper 0x1960340 / TIODeviceWriter AP 0x2f69d48
  -> retained QDataStream serialization
  -> persistent QBuffer-backed QIODevice byte container
```

Recover the **first exact downstream consumer or transform** of that retained byte-container state toward framing/final binary egress. Distinguish concrete data flow from lifecycle adjacency.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Pinned promoted facts

- helper `0x1960340` binds supplied QIODevice shared pair to QDataStream and retains device at `+0x8/+0x10`, stream at `+0x18/+0x20`;
- persistent QBuffer pair is passed to that helper and helper is retained at `TProtocolWriter+0x18/+0x20`;
- retained writer is retained by intermediate, which is retained by `TProtocolClientMessageProcessor`;
- serializer slots `0xc10960` and `0xc20290` use the retained QDataStream;
- local QBuffer slot `0xc20c70` proves QBuffer-backed serialization/exposure;
- only local object lifecycle order is proven.

# Acceptance boundary

A positive downstream claim requires exact type/member provenance plus a concrete read/call/data-flow edge from the retained QBuffer/helper/writer state into the candidate transform/consumer. A symbol-name hit, generic Qt/QBuffer census, vtable adjacency, unrelated local QBuffer use, or a historical final-socket observation is insufficient.

Classify separately:

```yaml
first_downstream_consumer: PROVEN | CANDIDATE | UNKNOWN
protocol_stage_order: PROVEN_PARTIAL | UNKNOWN
framing: PROVEN | CANDIDATE | UNKNOWN
sequence: PROVEN | CANDIDATE | UNKNOWN
compression: PROVEN | CANDIDATE | UNKNOWN
encryption: PROVEN | CANDIDATE | UNKNOWN
final_binary_egress: PROVEN | CANDIDATE | UNKNOWN
```

# Forbidden shortcuts

Do not use:
- generic QIODevice/QBuffer/QByteArray callsite census as proof;
- vtable adjacency as temporal order;
- historical final-socket run `31825417040` as proof;
- stale/superseded sink models;
- unproven direct DualConnection writer ownership;
- live traffic, credentials, login, attach, gameplay or account state.

Static exact-build analysis only. Track B is out of scope. Research stays Draft-only; coordinator PR #300 owns promotion.
