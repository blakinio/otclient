---
task_id: OTC-20260815-track-a-p2-post-serialization-buffer-boundary
status: active
agent: ChatGPT
session_id: chatgpt-p2-buffer-researcher-20260815-2128
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
updated: 2026-08-15T21:28:00+02:00
lease_expires_at: 2026-08-15T22:13:00+02:00
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
execution_reason: final artifact classification and Draft handoff after hardened exact-build static ELF proof
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
implementation_authorized: true
invocation_started_at: 2026-08-15T21:28:00+02:00
last_progress_at: 2026-08-15T21:28:00+02:00
code_bearing_head: 34f73b0c48198ba452caa505b4c0f3ae7e5b61d7
supporting_semantic_run: 31903141897
supporting_semantic_run_state: success
supporting_semantic_run_job: 95056868281
supporting_semantic_artifact: 9251635451
supporting_semantic_artifact_digest: sha256:118810016d53f5bc234f6216b1d2f45876422041d7539b32a942a285317c6c32
supporting_semantic_result: BUFFER_DATAFLOW_PROVEN
hardened_semantic_run: 31903490468
hardened_semantic_run_state: success
exact_head_ci_run: 31903493799
exact_head_ci_state: success
ci_checks_for_current_head: 0
ci_check_generation: final-handoff-docs
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
active_operation: download and classify hardened semantic artifact, persist final bounded evidence, then release Draft ready for coordinator review
next_action: inspect artifact from hardened run 31903490468 and require BUFFER_DATAFLOW_PROVEN plus persistent_tprotocolwriter_qbuffer_binding=PROVEN; persist exact evidence and UNKNOWN boundaries; then perform final docs-only handoff with exact-head CI semantics recorded
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

# Accepted supporting evidence

Supporting run `31903141897` / job `95056868281` on head `5d7f4bb1aadc782f9bc69b1e292577d88fe0c4a2` completed `SUCCESS` with semantic result `BUFFER_DATAFLOW_PROVEN`. It proves QBuffer construction, QBuffer-as-QIODevice binding into helper `0x1960340`, retained QDataStream state and local serialization, but the strengthened persistent writer provenance still required an exact checker gate.

# Hardened gate now terminal

Hardened semantic run `31903490468` on exact code-bearing head `34f73b0c48198ba452caa505b4c0f3ae7e5b61d7` is terminal `SUCCESS`. Repository CI run `31903493799` on the same code-bearing head is terminal `SUCCESS`. The final worker rotation must inspect the sanitized artifact rather than infer semantics from run conclusion.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
runner: synology-otclient-01
```

# Required final acceptance

- hardened artifact semantic result is `BUFFER_DATAFLOW_PROVEN`;
- hardened artifact explicitly marks `persistent_tprotocolwriter_qbuffer_binding=PROVEN`;
- exact client SHA/size and promoted writer/intermediate anchors remain pinned;
- local object lifecycle order may be promoted only where directly proved;
- overall protocol-stage order, framing, sequence, compression, encryption, final egress and causal harness remain UNKNOWN unless separately proven;
- no proprietary client bytes, credentials, account state or secret payloads are persisted;
- final evidence saved under task-owned evidence path;
- Draft released `ready` for coordinator review, not merged.
