---
task_id: OTC-20260815-track-a-p2-post-serialization-buffer-boundary
status: ready
agent: unassigned
session_id: null
session_role: researcher
session_rotation_count: 3
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
updated: 2026-08-15T21:31:00+02:00
lease_released_at: 2026-08-15T21:31:00+02:00
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
execution_reason: hardened static exact-build P2 data-flow proof completed and released for coordinator review
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
implementation_authorized: true
last_progress_at: 2026-08-15T21:31:00+02:00
code_bearing_head: 34f73b0c48198ba452caa505b4c0f3ae7e5b61d7
supporting_semantic_run: 31903141897
supporting_semantic_run_state: success
supporting_semantic_artifact: 9251635451
supporting_semantic_result: BUFFER_DATAFLOW_PROVEN
hardened_semantic_run: 31903490468
hardened_semantic_run_state: success
hardened_semantic_artifact: 9251725866
hardened_semantic_artifact_digest: sha256:f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e
hardened_artifact_digest_rechecked: true
hardened_semantic_result: BUFFER_DATAFLOW_PROVEN
persistent_tprotocolwriter_qbuffer_binding: PROVEN
code_bearing_ci_run: 31903493799
code_bearing_ci_state: success
release_head_ci_state: pending_after_release_commit
ci_checks_for_current_head: 0
ci_check_generation: final-release-head
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
final_evidence: docs/agents/evidence/OTC-20260815-track-a-p2-post-serialization-buffer-boundary/20260815-hardened-persistent-qbuffer-writer.md
promotion_status: DRAFT_NOT_PROMOTED
next_action: coordinator PR #300 must verify exact release-head repository CI terminal green and independently review this evidence; if accepted, promote bounded QBuffer-backed QDataStream retained-writer facts and keep protocol-stage order/framing/sequence/compression/encryption/final egress/harness UNKNOWN
---

# Final research result

`PROMOTION_CANDIDATE / BUFFER_DATAFLOW_PROVEN`

The hardened artifact for run `31903490468` was downloaded and its ZIP SHA-256 independently rechecked against GitHub's artifact digest. `result.txt` and `result.json` explicitly prove:

```text
HELPER_QIODEVICE_QDATASTREAM_BINDING=PROVEN
LOCAL_QBUFFER_BYTEFLOW=PROVEN
PERSISTENT_TPROTOCOLWRITER_QBUFFER_BINDING=PROVEN
COMMON_QBUFFER_QDATASTREAM_BINDING=PROVEN
```

The strengthened validation log proves the persistent chain:

```text
QBuffer shared pair
  -> helper 0x1960340 / TIODeviceWriter
  -> TProtocolWriter+0x18/+0x20
  -> retained intermediate writer
  -> TProtocolClientMessageProcessor retained intermediate
```

and revalidates serializer slots `0xc10960` and `0xc20290` plus local QBuffer slot `0xc20c70`.

The only directly proven ordering claim is object lifecycle: QBuffer/QDataStream binding is constructed before serializer use. The task does not prove overall protocol-stage ordering.

# Explicit UNKNOWN boundary

```yaml
protocol_stage_order: UNKNOWN
protocol_framing: UNKNOWN
sequence: UNKNOWN
compression: UNKNOWN
encryption: UNKNOWN
final_binary_egress: UNKNOWN
causal_local_harness: UNKNOWN
```

No login, attach, live traffic, credentials, gameplay, account state or runtime mutation was used. Research remains Draft-only until coordinator promotion.
