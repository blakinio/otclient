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
related_pr: 790
created: 2026-08-29T08:08:53+02:00
updated: 2026-08-29T08:39:21+02:00
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
local_model_execution_performed: true
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
updated_at: 2026-08-29T08:39:21+02:00
head: pending-qwen-bounded-profile-commit
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
pr: 790
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
  - focused harness suite is 22 of 22 PASS after adding explicit Ollama num_ctx 4096 and num_predict 256 bounds
  - an unbounded diagnostic run reproduced correct Qwen quality but exposed context 262144, about 44 GB residency and 66 percent CPU / 34 percent GPU spill, so its performance metrics are superseded
  - bounded Qwen exact profile qwen3-vl:4b-instruct-q4_K_M digest ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b ran at context 4096, 3527545978 bytes resident and 3527545978 bytes VRAM, 100 percent GPU
  - bounded Qwen login classification is LOGIN_SCREEN 3 of 3 with expected-text recall 1.0
  - bounded Qwen black no-text negative control has zero non-empty visible-text outputs in 3 of 3 and zero false IN_GAME_VISUAL in 3 of 3
  - bounded Qwen warm API p50 is 0.7998541 seconds and interpolated p95 is 1.14383672 seconds; cold total 5.2685395 seconds and cold load 3.8546923 seconds
  - all bounded Qwen hard gates pass and explicit unload leaves both Ollama and Docker Model Runner resident sets empty
  - OvisOCR2 retains exact-text recall 1.0 but false text on 3 of 3 black controls under both tested prompt profiles
  - Ovis2.5-2B remains UNSUPPORTED_BACKEND on the current Windows AMD exact-profile path
derived:
  - Qwen3-VL Q4_K_M num_ctx4096 num_predict256 is the leading viable local profile for representative Track B screenshot evaluation
  - no formal primary or OCR fallback can be selected from synthetic smoke alone because selection_quality remains false and representative Track B frames are absent
unknown:
  - Qwen and OvisOCR2 behavior on accepted secret-safe real Tibia frames from Track B
  - project-specific P7 structural-only versus structural-plus-VisualEvidence research-value result
  - whether Track B has produced a screenshot handoff after coordination comment 5460730478
conflicts: []
first_failure:
  marker: QWEN_UNBOUNDED_CONTEXT_RESOURCE_SPILL
  evidence: pre-unload ollama ps on the first warm suite showed context 262144, about 44 GB residency and CPU/GPU spill; harness now bounds num_ctx 4096 and bounded rerun is clean
rejected_hypotheses:
  - default Ollama model context is an acceptable benchmark resource profile
  - Qwen shares OvisOCR2 black-negative hallucination behavior on the tested synthetic control
  - a synthetic smoke result is sufficient to declare a benchmark winner
changed_paths:
  - tools/tibia-re-vision-benchmark/vision_benchmark.py
  - tools/tibia-re-vision-benchmark/tests/test_ollama_adapter.py
  - tools/tibia-re-vision-benchmark/run_qwen_synthetic_suite.py
  - docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-unbounded-context-diagnostic.json
  - docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-synthetic-suite.json
  - docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md
  - docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark-execution.md
validation:
  - command: python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -v
    result: PASS
    evidence: 22 tests passed including explicit num_ctx and num_predict request assertions
  - command: bounded Qwen synthetic login plus black-negative suite, three trials each
    result: PASS
    evidence: DOMAIN_STATUS=PASS_PROFILE; LOGIN_SCREEN 3 of 3, text recall 1.0, black false text 0 of 3, false IN_GAME_VISUAL 0 of 3, hard gates eligible true
  - command: Ollama API ps before explicit unload
    result: PASS
    evidence: exact digest, context 4096, resident size and size_vram both 3527545978 bytes
  - command: ollama stop plus ollama ps and docker model ps
    result: PASS
    evidence: both local model resident sets empty after bounded suite
blockers: []
next_action: revalidate PR 284 live Track B state and screenshot-handoff availability; if no accepted secret-safe frames exist, persist PARTIAL/INCONCLUSIVE terminal benchmark decision rather than extrapolating from synthetic smoke
```

## Recovery checkpoint

```yaml
status: active
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
head: pending-qwen-bounded-profile-commit
worktree: C:/Users/barte/otclient-vision-benchmark
active_operation: P1 deterministic harness followed by P2 bounded real-model smoke
operation_started_at: null
external_run_ids: []
last_verified_state: bounded Qwen num_ctx4096 profile passes login and black-negative smoke with zero hallucinated black text, 100 percent GPU 3.527 GB residency, explicit unload clean; Ovis statuses unchanged
resume_condition: current task branch still owns the declared paths and Ollama residency is empty or exact target only
failure_handling: if a model/backend pull or inference fails, persist the typed failure and do not switch to cloud or a different undeclared provider
next_action: revalidate Track B PR 284 and consume only an accepted secret-safe screenshot handoff; otherwise terminalize benchmark PARTIAL and research value INCONCLUSIVE
```
