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
updated: 2026-08-29T08:33:34+02:00
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
updated_at: 2026-08-29T08:33:34+02:00
head: pending-ovis-compatibility-evidence-commit
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
  - deterministic harness test suite is 22 of 22 PASS, including OCR normalization that preserves hallucinated text instead of repairing it
  - Qwen3-VL Q4_K_M synthetic state/OCR smoke remains 3 of 3 PASS with all hard gates green and final Ollama residency empty
  - OvisOCR2 exact revision 1fc9221b7823a371d6e97f92d527cc847e24e107 loads and runs locally through a fingerprinted Transformers CPU profile
  - OvisOCR2 found all five expected synthetic login strings in 3 of 3 trials under both benchmark-safe-v1 and model-card recommended prompt profiles
  - OvisOCR2 emitted non-empty fabricated text on the solid-black no-text control in 3 of 3 trials under both prompt profiles
  - OvisOCR2 recommended-profile p50 latency is 17.4179759 seconds, peak process RSS 2295803904 bytes, selection_quality false
  - Ovis2.5-2B current revision 393c932b2a03e28eb9aaa503e3c4ab3ad384d958 is UNSUPPORTED_BACKEND on this host profile: Docker Model Runner exposes it as vllm while local DMR v1.2.5 reports vllm Not Installed and only supported on Linux, and the current Windows AMD host has no NVIDIA CUDA path
  - no Ovis2.5 inference was performed and no alternative cloud or materially different model profile was substituted
  - final Ollama and Docker Model Runner residency sets are empty
derived:
  - OvisOCR2 is locally executable as a CPU OCR specialist but cannot currently be recommended unqualified because its negative-control hallucination rate is 3 of 3 in both tested prompt profiles
  - Ovis2.5-2B cannot enter P3-P6 on the current Windows AMD backend without a materially different supported local runtime profile
unknown:
  - Qwen negative-control behavior and warm latency on the frozen synthetic suite
  - Qwen and OvisOCR2 behavior on accepted secret-safe real Tibia frames from Track B
  - project-specific P7 research-value result until Track B screenshot handoff exists
conflicts: []
first_failure:
  marker: OVISOCR2_BLACK_NEGATIVE_FALSE_TEXT
  evidence: solid-black image produced non-empty prompt-like fabricated text in 3 of 3 trials for both benchmark-safe and model-card recommended prompt profiles
rejected_hypotheses:
  - the OvisOCR2 negative-control failure is caused only by the benchmark-safe prompt
  - Ovis2.5 prior scratch AttributeError alone proves unsupported backend
  - Docker Model Runner vllm can provide an AMD Windows execution path for exact Ovis2.5-2B
changed_paths:
  - tools/tibia-re-vision-benchmark/vision_benchmark.py
  - tools/tibia-re-vision-benchmark/tests/test_vision_benchmark.py
  - tools/tibia-re-vision-benchmark/run_ovisocr2_cpu_smoke.py
  - docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovisocr2-cpu-smoke.json
  - docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovisocr2-cpu-recommended-prompt-smoke.json
  - docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovis-backend-compatibility.json
  - docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md
  - docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark-execution.md
validation:
  - command: python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -v
    result: PASS
    evidence: 22 tests passed
  - command: OvisOCR2 CPU three-trial synthetic-login plus black-negative suite under benchmark-safe-v1
    result: PASS
    evidence: DOMAIN_STATUS=PASS_PROFILE_WITH_NEGATIVE_CONTROL_FAILURE; text recall 1.0, black false text 3 of 3
  - command: OvisOCR2 CPU three-trial suite under ovisocr2-recommended-v1
    result: PASS
    evidence: DOMAIN_STATUS=PASS_PROFILE_WITH_NEGATIVE_CONTROL_FAILURE; text recall 1.0, black false text 3 of 3, p50 17.4179759 seconds
  - command: docker model status and model search backend classification
    result: PASS
    evidence: DOMAIN_STATUS=UNSUPPORTED_BACKEND; Ovis2.5-2B backend vllm; local DMR vllm Not Installed and only supported on Linux; Windows host GPU is AMD Radeon RX 9070 XT
  - command: ollama ps and docker model ps after Ovis execution
    result: PASS
    evidence: both resident model sets empty
blockers: []
next_action: run a bounded Qwen synthetic-login plus black-negative warm-residency suite, unload and verify empty residency, then consume Track B screenshot handoff if available or close P3-P7 as blocked/inconclusive with exact missing evidence
```

## Recovery checkpoint

```yaml
status: active
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
head: pending-ovis-compatibility-evidence-commit
worktree: C:/Users/barte/otclient-vision-benchmark
active_operation: P1 deterministic harness followed by P2 bounded real-model smoke
operation_started_at: null
external_run_ids: []
last_verified_state: Qwen synthetic smoke PASS; OvisOCR2 CPU exact-text smoke PASS with repeatable black-negative false text; Ovis2.5-2B UNSUPPORTED_BACKEND on current Windows AMD vllm path; all local model residency empty
resume_condition: current task branch still owns the declared paths and Ollama residency is empty or exact target only
failure_handling: if a model/backend pull or inference fails, persist the typed failure and do not switch to cloud or a different undeclared provider
next_action: Qwen warm plus black-negative synthetic suite, deterministic unload, then Track B screenshot handoff check and P7 decision
```
