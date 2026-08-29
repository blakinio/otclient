---
task_id: OTC-20260829-tibia-re-vision-benchmark-execution
status: implementing
agent: ChatGPT
session_id: chatgpt-20260829-vision-benchmark-execution
session_role: implementer
project_lane: otclient
lane: P0-DESIGN
track_id: official-client-re
task_kind: implementation
phase: implement
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
base_branch: main
base_sha: f208a20cb4517e8b57bef91983337145d379267c
created: 2026-08-29T08:08:53+02:00
updated: 2026-08-29T08:08:53+02:00
risk: high
execution_mode: local_owner_pc
execution_reason: deterministic harness plus local real-model benchmark on verified Molehill-PC
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: one shared harness and sequential one-model benchmark with Track B screenshot handoff as the final project-specific evidence dependency
validation_level: focused
heavy_validation_runs: 0
repair_cycles_for_current_gate: 0
runtime_access: none
execution_host: Molehill-PC
local_model_authorized: true
owner_funded_ai_api_authorized: false
cloud_model_authorized: false
credentials_allowed: false
login_allowed: false
gui_input_authorized: false
process_control_authorized: false
gameplay_allowed: false
track_b_runtime_ownership: false
owned_paths:
  - tools/tibia-re-vision-benchmark/**
  - docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/**
  - docs/agents/reports/OTCLIENT-20260829-tibia-re-vision-benchmark-execution.md
  - docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md
  - docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark-execution.md
reuses:
  - docs/agents/prompts/TIBIA_RE_VISION_BENCHMARK.md
  - docs/superpowers/specs/2026-08-29-tibia-re-vision-benchmark-design.md
  - docs/agents/contracts/LOCAL_MODEL_SINGLE_RESIDENCY_V1.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
cross_track_dependencies:
  - Track B PR 284 comment 5460730478 requests a future secret-safe Linux/Xvfb screenshot handoff without triggering a retry or transferring ownership
---

# Goal

Execute the repository-owned local vision benchmark programme on the verified Molehill-PC, prove the deterministic harness and first-pass local model compatibility, and measure Track B Global Login research value only when secret-safe Linux-container keyframes are available.

# P0 verified state

```yaml
trusted_main: f208a20cb4517e8b57bef91983337145d379267c
execution_host: MOLEHILL-PC
os: Windows
cpu: AMD Ryzen 7 9800X3D
gpu: AMD Radeon RX 9070 XT
dedicated_vram_bytes_vulkan_heap: 17095983104
system_ram_bytes: 68719476736
gpu_driver_vulkan: 26.7.1
ollama_version: 0.32.14
ollama_resident_models_at_preflight: 0
windows_python: 3.12.0
windows_torch: not_installed
windows_transformers: not_installed
wsl_rocm: not_installed
runtime_access: none
synology_accessed: false
official_client_accessed: false
credentials_accessed: false
track_b_current_blocker: BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE
track_b_screenshot_request_comment: 5460730478
```

# Scope decision

P1/P2 and backend compatibility work are READY offline. P3-P7 project-specific selection/research-value evidence requires an accepted secret-safe Linux-container screenshot dataset. Synthetic fixtures are smoke-only and cannot produce a production winner claim.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-29T08:08:53+02:00
head: pending-initial-task-plan-commit
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
pr: none
status: implementing
context_routes:
  - local-model-benchmark
  - official-client-research-design
  - track-b-read-only-coordination
owned_paths:
  - tools/tibia-re-vision-benchmark/**
  - docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/**
  - docs/agents/reports/OTCLIENT-20260829-tibia-re-vision-benchmark-execution.md
  - docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md
  - docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark-execution.md
proven:
  - exact trusted main includes merged and archived TIBIA-RE-VISION-BENCHMARK programme
  - Molehill-PC host/GPU/RAM/Ollama profile verified in current invocation
  - Ollama resident set is empty at P0 preflight
  - no trusted-main executable vision benchmark harness exists; blocked PR 615 remains discovery input only
  - Track B remains blocked from another official-service E2E and received only a no-retry secret-safe screenshot coordination request
derived:
  - deterministic harness plus synthetic real-model smoke can proceed without Track A or Track B runtime ownership
unknown:
  - Qwen3-VL exact local profile smoke outcome
  - Ovis2.5-2B local backend compatibility on this Windows/AMD host
  - OvisOCR2 local backend compatibility on this Windows/AMD host
  - Track B project-specific P3-P7 research-value result until screenshot handoff exists
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - existing trusted-main executable vision harness can be reused
changed_paths:
  - docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md
  - docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark-execution.md
validation:
  - command: ollama ps
    result: PASS
    evidence: empty resident model set at current P0 preflight
  - command: environment capability inventory
    result: PASS
    evidence: host/GPU/RAM/Ollama/Python state recorded above
blockers: []
next_action: write the Task 1 RED tests for VisualEvidence schema, hard gates, scoring and single-model residency, then run them and require the expected import failure
```

## Recovery checkpoint

```yaml
status: active
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
head: pending-initial-task-plan-commit
worktree: C:/Users/barte/otclient-vision-benchmark
active_operation: P1 deterministic harness followed by P2 bounded real-model smoke
operation_started_at: null
external_run_ids: []
last_verified_state: Ollama resident set empty; no model inference started; no official-client or Track B runtime accessed
resume_condition: current task branch still owns the declared paths and Ollama residency is empty or exact target only
failure_handling: if a model/backend pull or inference fails, persist the typed failure and do not switch to cloud or a different undeclared provider
next_action: continue from Task 1 RED tests; before each real model verify residency and after each model verify unload
```
