---
task_id: OTC-20260815-track-a-p2-post-serialization-buffer-boundary
status: active
agent: ChatGPT
session_id: chatgpt-p2-buffer-researcher-20260815-2115
session_role: researcher
session_rotation_count: 2
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
updated: 2026-08-15T21:15:00+02:00
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
invocation_started_at: 2026-08-15T21:15:00+02:00
last_progress_at: 2026-08-15T21:15:00+02:00
code_bearing_head: 5d7f4bb1aadc782f9bc69b1e292577d88fe0c4a2
semantic_run: 31903141897
semantic_run_state: success
semantic_run_job: 95056868281
semantic_artifact: 9251635451
semantic_artifact_digest: sha256:118810016d53f5bc234f6216b1d2f45876422041d7539b32a942a285317c6c32
semantic_result: BUFFER_DATAFLOW_PROVEN
ci_checks_for_current_head: 0
ci_check_generation: persistent-writer-buffer-provenance-hardening
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
next_action: harden the successful reproducer so BUFFER_DATAFLOW_PROVEN additionally requires exact persistent writer setup provenance QBuffer shared pair -> helper 0x1960340 -> TIODeviceWriter -> TProtocolWriter+0x18, rerun exactly once, persist sanitized evidence, require exact-head repository CI, then release Draft as ready for coordinator review
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

# Current implementation checkpoint

Exact-client run `31903141897` / job `95056868281` on code-bearing head `5d7f4bb1aadc782f9bc69b1e292577d88fe0c4a2` completed `SUCCESS`. Artifact `9251635451`, digest `sha256:118810016d53f5bc234f6216b1d2f45876422041d7539b32a942a285317c6c32`, contains only `result.json`, `result.txt`, `evidence.txt` and `validation.log`. Its semantic result is `BUFFER_DATAFLOW_PROVEN`.

Direct exact disassembly proves helper `0x1960340` installs AP `0x2f69d48`, copies the supplied QIODevice shared pair to helper `+0x8/+0x10`, constructs `QDataStream(QIODevice*)` from that supplied device, stores the QDataStream shared pair at helper `+0x18/+0x20`, and sets byte order. In `0xc20c70`, a QBuffer shared pair is passed directly to that helper before the helper's QDataStream `+0x18` is used for serialization; `QBuffer::buffer()` later exposes the resulting byte container.

Fresh review found one hardening requirement before handoff: the positive verdict must also require the persistent setup path that constructs the retained TProtocolWriter branch, namely QBuffer shared pair -> `0x1960340` -> TIODeviceWriter helper object -> `TProtocolWriter+0x18`. This is a proof-strengthening repair, not a changed semantic hypothesis. Protocol framing, sequence, compression, encryption and final binary egress remain UNKNOWN.

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
- relation/order between serializer and QBuffer was previously UNKNOWN;
- final egress, framing, sequence, compression and encryption remain UNKNOWN.

# Required discriminator

1. Revalidate exact client identity, intermediate/writer RTTI/address points, retention setup and serializer slots from the exact ELF.
2. Recover concrete QDataStream sink object/member provenance in `0xc10960` / `0xc20290`.
3. Recover QBuffer/byte-container construction/use provenance in `0xc20c70` and directly related calls.
4. Require the persistent TProtocolWriter setup to prove the same QBuffer-backed helper object is retained at writer `+0x18`.
5. Classify common versus split state only from exact member stores/loads, constructor args, QDataStream device binding or direct control/data flow.
6. Claim lifecycle order only from actual construction/use flow, never vtable adjacency; keep overall protocol-stage order UNKNOWN.
7. Distinguish QBuffer/container management from protocol framing.
8. Preserve UNKNOWN for sequence/compression/encryption/final egress unless directly proven.
9. Emit machine-readable result plus sanitized bounded disassembly/provenance evidence; workflow success and semantic outcome remain separate.

# Allowed semantic outcomes

- `BUFFER_DATAFLOW_PROVEN`
- `SERIALIZATION_TARGET_PROVEN_BUFFER_ORDER_UNKNOWN`
- `BUFFER_INDEPENDENT_OR_SPLIT`
- `FRAMING_EDGE_PROVEN`
- `INCONCLUSIVE`

# Negative controls / forbidden shortcuts

Do not use vtable adjacency, generic QIODevice/QBuffer/QByteArray census, generic Qt/QMeta census, final-socket run `31825417040`, superseded `0xb5b880/0xb46bd0/0xc33259`, stale writer RTTI `0x3080700`, or unproven direct DualConnection writer ownership as proof.

# Acceptance gate

- [x] exact client SHA/size verified by executing job;
- [x] promoted retained intermediate/writer/serializer facts independently revalidated;
- [x] QDataStream sink object/member provenance recovered;
- [x] QBuffer/byte-container object/member provenance recovered;
- [x] common QBuffer/QDataStream data-flow relationship classified from exact evidence;
- [x] local lifecycle order claimed only from direct construction/use data flow;
- [x] framing distinguished from container management and remains UNKNOWN;
- [x] sequence/compression/encryption/final egress remain UNKNOWN;
- [x] negative controls encoded in reproducer;
- [x] execution success and semantic outcome are separate outputs;
- [x] no proprietary client bytes, credentials, account state or secret payloads are committed/uploaded;
- [ ] persistent retained-writer setup provenance is a required positive gate in the final reproducer;
- [ ] exact-head repository CI terminal before Draft handoff;
- [ ] task released as `ready` for coordinator review rather than merged.

# Side-effect budget

Static exact-build analysis only. No client launch, process attach, login, credential access, live packet replay, movement, gameplay, account state or runtime mutation is authorized.
