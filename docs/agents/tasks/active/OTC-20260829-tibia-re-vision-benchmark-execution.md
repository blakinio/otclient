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
updated: 2026-08-29T08:12:04+02:00
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
updated_at: 2026-08-29T08:12:04+02:00
head: pending-p1-harness-fixture-commit
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
  - P1 deterministic VisualEvidence schema, hard-gate, scoring, file-hash and residency helpers are implemented with 14 focused core tests
  - loopback-only Ollama adapter, strict model JSON handling and secret-input rejection are implemented with five adapter tests
  - focused unittest suite is 19 of 19 PASS
  - deterministic synthetic LOGIN_SCREEN smoke fixture exists, is visually verified secret-safe, and hashes to 2dea29719c3e6f7c84c40717ead27bd56cfaacb69b06c4f19f0975b231bc47a6
  - no model inference, official-client access, Track B runtime access or credential access has occurred
derived:
  - P1 is complete and P2 Qwen3-VL real-model smoke is READY after a fresh residency check
unknown:
  - Qwen3-VL exact local profile smoke outcome
  - Ovis2.5-2B local backend compatibility on this Windows/AMD host
  - OvisOCR2 local backend compatibility on this Windows/AMD host
  - Track B project-specific P3-P7 research-value result until screenshot handoff exists
conflicts: []
first_failure:
  marker: SYNTHETIC_FIXTURE_FONT_CONSTRUCTOR_AMBIGUOUS
  evidence: initial PowerShell New-Object Font three-argument overload was ambiguous; explicit four-argument Font constructor was proven and regenerated fixture hash is recorded
rejected_hypotheses:
  - existing trusted-main executable vision harness can be reused
  - initial synthetic PNG generated after Font constructor errors is usable benchmark input
changed_paths:
  - tools/tibia-re-vision-benchmark/vision_benchmark.py
  - tools/tibia-re-vision-benchmark/tests/test_vision_benchmark.py
  - tools/tibia-re-vision-benchmark/tests/test_ollama_adapter.py
  - tools/tibia-re-vision-benchmark/make_synthetic_fixture.ps1
  - tools/tibia-re-vision-benchmark/fixtures/synthetic-login-smoke.png
  - tools/tibia-re-vision-benchmark/fixtures/synthetic-login-smoke.json
  - docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md
  - docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark-execution.md
validation:
  - command: python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -v
    result: PASS
    evidence: 19 tests passed
  - command: git diff --check
    result: PASS
    evidence: no whitespace errors before P1 checkpoint commit
  - command: synthetic fixture visual inspection and SHA-256
    result: PASS
    evidence: labels only, empty fields, NO SECRET DATA; sha256 2dea29719c3e6f7c84c40717ead27bd56cfaacb69b06c4f19f0975b231bc47a6
blockers: []
next_action: verify Ollama residency is still empty, resolve the exact qwen3-vl:4b-instruct local digest, then run three strict synthetic smoke trials with keep_alive zero and verify unload
```

## Recovery checkpoint

```yaml
status: active
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
head: pending-p1-harness-fixture-commit
worktree: C:/Users/barte/otclient-vision-benchmark
active_operation: P1 deterministic harness followed by P2 bounded real-model smoke
operation_started_at: null
external_run_ids: []
last_verified_state: P1 harness and synthetic secret-safe fixture complete; Ollama resident set was empty at latest preflight; no model inference or official-client/Track B runtime access yet
resume_condition: current task branch still owns the declared paths and Ollama residency is empty or exact target only
failure_handling: if a model/backend pull or inference fails, persist the typed failure and do not switch to cloud or a different undeclared provider
next_action: fresh Ollama residency check, then exact qwen3-vl:4b-instruct resolve/pull and three-trial P2 smoke with deterministic unload
```
