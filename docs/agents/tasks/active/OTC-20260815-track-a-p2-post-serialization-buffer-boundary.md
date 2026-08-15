---
task_id: OTC-20260815-track-a-p2-post-serialization-buffer-boundary
status: waiting
agent: unassigned
session_id: null
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
updated: 2026-08-15T21:19:00+02:00
lease_released_at: 2026-08-15T21:19:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-post-serialization-buffer-boundary.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-post-serialization-buffer-boundary/**
  - .github/workflows/tibia-official-client-re-p2-post-serialization-buffer-boundary.yml
  - .github/scripts/tibia-official-client-re-p2-post-serialization-buffer-boundary.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
  - coordinator PR #300 promoted #306 serialization evidence as pinned unmerged dependency only
blocks:
  - hardened semantic run 31903490468 on code-bearing head 34f73b0c48198ba452caa505b4c0f3ae7e5b61d7 remained in_progress after the two ordinary observations allowed for this exact head
  - repository CI run 31903493799 on the same code-bearing head remained in_progress after its two ordinary observations; terminal-CI exception is not yet eligible until semantic/non-CI acceptance is confirmed
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
last_progress_at: 2026-08-15T21:17:00+02:00
code_bearing_head: 34f73b0c48198ba452caa505b4c0f3ae7e5b61d7
supporting_semantic_run: 31903141897
supporting_semantic_run_state: success
supporting_semantic_run_job: 95056868281
supporting_semantic_artifact: 9251635451
supporting_semantic_artifact_digest: sha256:118810016d53f5bc234f6216b1d2f45876422041d7539b32a942a285317c6c32
supporting_semantic_result: BUFFER_DATAFLOW_PROVEN
hardened_semantic_run: 31903490468
hardened_semantic_run_state_at_release: in_progress
exact_head_ci_run: 31903493799
exact_head_ci_state_at_release: in_progress
ci_checks_for_current_head: 2
ci_check_generation: persistent-writer-buffer-provenance-hardening
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 1
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
next_action: in a fresh researcher rotation inspect hardened run 31903490468 exactly once after terminal; if SUCCESS download its sanitized artifact and require BUFFER_DATAFLOW_PROVEN plus persistent_tprotocolwriter_qbuffer_binding=PROVEN, otherwise inspect the first actionable error; then persist final evidence, require exact final-head repository CI and release Draft as ready for coordinator review
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

# Current evidence

Supporting exact-client run `31903141897` / job `95056868281` on head `5d7f4bb1aadc782f9bc69b1e292577d88fe0c4a2` completed `SUCCESS`. Artifact `9251635451`, digest `sha256:118810016d53f5bc234f6216b1d2f45876422041d7539b32a942a285317c6c32`, contains only `result.json`, `result.txt`, `evidence.txt` and `validation.log`; semantic result is `BUFFER_DATAFLOW_PROVEN`.

That run directly proves helper `0x1960340` installs TIODeviceWriter AP `0x2f69d48`, copies the supplied QIODevice shared pair to helper `+0x8/+0x10`, calls `QDataStream(QIODevice*)` with the supplied device object, retains the stream at helper `+0x18/+0x20`, and sets byte order. `0xc20c70` constructs a QBuffer, passes its shared pair to the helper, serializes through helper `+0x18`, and later calls `QBuffer::buffer()`.

Fresh audit strengthened the reproducer on head `34f73b0c48198ba452caa505b4c0f3ae7e5b61d7`. The positive verdict now additionally requires exact persistent setup bytes and disassembly proving:

```text
[rbp-0x40/-0x38] QBuffer shared pair
  -> saved pair pointer at rbp-0x1a0
  -> helper 0x1960340
  -> TIODeviceWriter helper object
  -> TProtocolWriter+0x18/+0x20
  -> intermediate retained writer
  -> TProtocolClientMessageProcessor retained intermediate
```

The hardened checker also separates `object_lifecycle_order` from `protocol_stage_order`: QBuffer/QDataStream binding construction-before-use can be proven, while overall protocol-stage order remains UNKNOWN. Protocol framing, sequence, compression, encryption, final binary egress and causal harness remain UNKNOWN.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Required discriminator / acceptance boundary

- [x] exact client SHA/size verified by supporting executing job;
- [x] promoted retained intermediate/writer/serializer facts independently revalidated;
- [x] QDataStream sink object/member provenance recovered;
- [x] QBuffer/byte-container object/member provenance recovered;
- [x] common QBuffer/QDataStream data-flow relationship classified from exact evidence;
- [x] local lifecycle order derived from direct construction/use data flow, not vtable adjacency;
- [x] framing distinguished from container management and remains UNKNOWN;
- [x] sequence/compression/encryption/final egress remain UNKNOWN;
- [x] negative controls encoded;
- [x] execution success and semantic outcome are separate outputs;
- [x] no proprietary client bytes, credentials, account state or secret payloads are committed/uploaded;
- [ ] hardened run confirms persistent retained-writer QBuffer provenance on exact code-bearing head;
- [ ] final evidence is persisted in task namespace;
- [ ] exact final-head repository CI terminal green before Draft handoff;
- [ ] task released as `ready` for coordinator review rather than merged.

# Negative controls / forbidden shortcuts

Do not use vtable adjacency, generic QIODevice/QBuffer/QByteArray census, generic Qt/QMeta census, final-socket run `31825417040`, superseded `0xb5b880/0xb46bd0/0xc33259`, stale writer RTTI `0x3080700`, or unproven direct DualConnection writer ownership as proof.

# Side-effect budget

Static exact-build analysis only. No client launch, process attach, login, credential access, live packet replay, movement, gameplay, account state or runtime mutation is authorized.
