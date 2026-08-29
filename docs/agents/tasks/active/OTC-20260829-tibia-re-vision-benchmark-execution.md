---
task_id: OTC-20260829-tibia-re-vision-benchmark-execution
status: validating
agent: ChatGPT
session_id: chatgpt-20260829-vision-benchmark-execution
session_role: implementer
project_lane: otclient
lane: P0-DESIGN
track_id: official-client-re
task_kind: implementation
phase: validate
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
base_branch: main
base_sha: f208a20cb4517e8b57bef91983337145d379267c
related_pr: 790
created: 2026-08-29T08:08:53+02:00
updated: 2026-08-29T08:41:57+02:00
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


# Terminal benchmark decision

```yaml
benchmark_result: PARTIAL
primary_model: null
leading_profile: ollama:qwen3-vl:4b-instruct-q4_K_M@sha256:ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
ocr_fallback_model: null
research_value_verdict: INCONCLUSIVE
track_b_help_verdict: USEFUL_DIAGNOSTIC_SENSOR_CANDIDATE_NOT_CURRENT_UNBLOCKER
track_b_head_revalidated: 62383aded3acbeb5f405a12fe1f93849cd8e35f9
track_b_current_blocker: BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE
track_b_screenshot_handoff: UNAVAILABLE
representative_selection_dataset: UNAVAILABLE
weighted_selection_score: NOT_COMPUTED
```

The full rationale and measured profile evidence are persisted in `docs/agents/reports/OTCLIENT-20260829-tibia-re-vision-benchmark-execution.md`.

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
updated_at: 2026-08-29T08:41:57+02:00
head: pending-terminal-report-commit
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
pr: 790
status: validating
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
  - bounded Qwen profile passes all synthetic schema, login-state, exact-text, black-negative and residency hard gates
  - bounded Qwen warm API p50 0.7998541 seconds, p95 1.14383672 seconds, context 4096, 3527545978 bytes VRAM, 100 percent GPU
  - OvisOCR2 exact-text recall is 1.0 but black no-text false output is 3 of 3 under each of two prompt profiles
  - Ovis2.5-2B exact current candidate is UNSUPPORTED_BACKEND on current Windows AMD local profile and was not substituted
  - Track B PR 284 live head is 62383aded3acbeb5f405a12fe1f93849cd8e35f9 and its current terminal blocker is BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE
  - PR 284 comment 5460730478 is the latest vision coordination comment and no later accepted screenshot handoff exists
  - Track B branch contains no repo-owned screenshot or keyframe evidence dataset suitable for the benchmark; static product image assets do not qualify
  - no Track B or official-client E2E was triggered for screenshot collection
  - closeout audit rejected the System.Drawing fixture generator as a reproducer because regenerated pixels differed from the already-scored frozen PNG; the generator is removed and the committed PNG plus SHA-256 remain the canonical immutable input
  - final benchmark decision is PARTIAL with primary_model null, ocr_fallback_model null and research_value_verdict INCONCLUSIVE
derived:
  - bounded Qwen is the leading profile to test first when representative Track B screenshots become legally available
  - Vision is likely useful as an additive diagnostic sensor but does not remove the current native outbound-sequence blocker
unknown:
  - representative real Track B state/OCR/delta accuracy
  - measured structural-only versus structural-plus-VisualEvidence hypothesis/E2E/time reduction
conflicts: []
first_failure:
  marker: REPRESENTATIVE_TRACK_B_SCREENSHOT_DATASET_UNAVAILABLE
  evidence: no post-comment handoff and no repo-owned Track B evidence image; current Track B no-retry blocker forbids manufacturing another service run merely for screenshots
rejected_hypotheses:
  - synthetic smoke is sufficient for a formal winner claim
  - Vision can prove or recover the native pre-login outbound sequence
  - OvisOCR2 can be promoted as fallback despite repeatable black-negative hallucination
  - System.Drawing fixture regeneration is bitwise and pixel-identical to the frozen scored fixture
changed_paths:
  - docs/agents/reports/OTCLIENT-20260829-tibia-re-vision-benchmark-execution.md
  - docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md
  - docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark-execution.md
validation:
  - command: python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -v
    result: PASS
    evidence: 32 tests passed on post-remediation worktree
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md --require-checkpoint
    result: PASS
    evidence: current task checkpoint validated
  - command: git diff --check
    result: PASS
    evidence: terminal report worktree has no whitespace errors
  - command: ollama ps plus docker model ps
    result: PASS
    evidence: both resident model sets empty after all real-model trials
  - command: GitHub PR 284 live-state revalidation plus exact current task tail
    result: PASS
    evidence: head 62383aded3acbeb5f405a12fe1f93849cd8e35f9; current blocker BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE
  - command: PR 284 comment and changed-file inventory
    result: PASS
    evidence: vision request comment 5460730478 exists; no subsequent accepted screenshot handoff and no Track B evidence screenshot/keyframe dataset path exists
blockers:
  - repository-mandated fresh independent post-implementation audit is still required before completion/merge; implementer session cannot self-approve material work
next_action: run full focused validation and exact-scope checks on the terminal report head, push it, consume exact-head CI/governance and review hygiene, then stop at REQUIRED_FRESH_INDEPENDENT_POST_IMPLEMENTATION_AUDIT if no separate validator session is available
```

## Recovery checkpoint

```yaml
status: active
branch: feat/OTC-20260829-tibia-re-vision-benchmark-execution
head: pending-terminal-report-commit
worktree: C:/Users/barte/otclient-vision-benchmark
active_operation: P1 deterministic harness followed by P2 bounded real-model smoke
operation_started_at: null
external_run_ids: []
last_verified_state: terminal benchmark PARTIAL/INCONCLUSIVE report prepared; bounded Qwen leading profile; no Track B screenshot handoff; Track B blocker unchanged; all local model residency empty
resume_condition: current task branch still owns the declared paths and Ollama residency is empty or exact target only
failure_handling: if a model/backend pull or inference fails, persist the typed failure and do not switch to cloud or a different undeclared provider
next_action: full final focused validation plus exact-head CI/governance/review checks, then separate fresh audit or explicit audit blocker
```
