# TIBIA RE Vision Benchmark Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and execute a fail-closed local vision benchmark harness on Molehill-PC, measure first-pass model compatibility on frozen secret-safe inputs, and evaluate whether VisualEvidence can materially help the Track B Global Login investigation without becoming protocol or runtime authority.

**Architecture:** A small Python-stdlib harness owns strict VisualEvidence validation, hard-gate scoring, local-residency checks, provenance, and Ollama loopback inference. Synthetic PNG fixtures prove the harness and real-model smoke path; Track B remains a separate producer of secret-safe Linux-container keyframes for project-specific P3-P7 evaluation. Unsupported model backends are recorded as typed results rather than replaced with cloud providers.

**Tech Stack:** Python 3.12 stdlib, unittest, Ollama loopback API 0.32.14, PowerShell/.NET only for deterministic local synthetic PNG generation, Git/GitHub for durable evidence.

**Spec:** `docs/superpowers/specs/2026-08-29-tibia-re-vision-benchmark-design.md`

## Global Constraints

- All model inference is local on the verified Molehill-PC; no cloud/API/provider fallback.
- At most one local model may be resident or actively inferencing at a time; `ollama ps`/`/api/ps` is canonical for Ollama.
- Visual output is always `visual_only: true` and `structural_authority: false`; `IN_GAME_VISUAL` never becomes canonical `IN_GAME`.
- No credentials, 2FA, session/auth tokens, login, GUI input, gameplay, process attach/control, network mutation, or Track A/Track B runtime takeover.
- Track B screenshots are consumed only through a secret-safe handoff; the current Track B no-retry blocker remains unchanged.
- Synthetic fixtures prove harness/model smoke only and cannot support a production winner claim.

---

### Task 1: Deterministic VisualEvidence core

**Files:**
- Create: `tools/tibia-re-vision-benchmark/vision_benchmark.py`
- Create: `tools/tibia-re-vision-benchmark/tests/test_vision_benchmark.py`

**Interfaces:**
- Produces: `validate_visual_evidence(payload) -> list[str]`, `evaluate_hard_gates(trials) -> dict`, `score_profile(metrics) -> float`, `admit_residency(resident_models, target) -> tuple[bool,str]`, `sha256_file(path) -> str`.

- [ ] **Step 1: Write failing unittest cases** for schema validity, forced `visual_only`, forced non-authority, false `IN_GAME_VISUAL` hard gates, missing provenance, empty/exact/different/multiple residency, and weighted score calculation.
- [ ] **Step 2: Run** `python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -v` **and verify RED** because `vision_benchmark` does not exist.
- [ ] **Step 3: Implement minimal stdlib core** with explicit enums/required keys and hard-gate precedence; do not repair malformed model JSON.
- [ ] **Step 4: Re-run the focused unittest suite and require GREEN.**
- [ ] **Step 5: Commit** core + tests + current task/plan checkpoint.

### Task 2: Local Ollama adapter and synthetic fixture

**Files:**
- Modify: `tools/tibia-re-vision-benchmark/vision_benchmark.py`
- Create: `tools/tibia-re-vision-benchmark/tests/test_ollama_adapter.py`
- Create: `tools/tibia-re-vision-benchmark/make_synthetic_fixture.ps1`
- Create: `tools/tibia-re-vision-benchmark/fixtures/synthetic-login-smoke.png`
- Create: `tools/tibia-re-vision-benchmark/fixtures/synthetic-login-smoke.json`

**Interfaces:**
- Produces: `query_ollama_ps(endpoint)`, `run_ollama_trial(endpoint, model, image_path, prompt, keep_alive='0s')`, deterministic fixture manifest with expected `LOGIN_SCREEN` and visible synthetic text.

- [ ] **Step 1: Write failing adapter tests** using a local fake HTTP server for `/api/ps` and `/api/chat`; prove loopback-only endpoint rejection, invalid JSON propagation, `keep_alive=0`, and residency refusal.
- [ ] **Step 2: Run focused tests and verify RED.**
- [ ] **Step 3: Implement the minimal loopback-only Ollama adapter** with urllib and base64 image transport; never send a request to a non-loopback endpoint.
- [ ] **Step 4: Generate the deterministic synthetic PNG** with .NET drawing: title `TIBIA VISION SAFE FIXTURE`, state text `ACCOUNT LOGIN`, field labels without credentials, and footer `NO SECRET DATA`.
- [ ] **Step 5: Hash the PNG into the JSON manifest, run all focused tests, and commit.**

### Task 3: Qwen3-VL local real-model smoke

**Files:**
- Create: `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-4b-instruct-smoke.json`
- Modify: `docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md`

**Interfaces:**
- Consumes: exact Ollama residency state and synthetic fixture hash.
- Produces: exact local model profile, load/inference timings, schema result, visible text/state result, and verified unload.

- [ ] **Step 1: Verify `ollama ps` is empty and record Ollama/host/GPU facts.**
- [ ] **Step 2: Resolve/pull only the intended `qwen3-vl:4b-instruct` local profile, record the exact digest, and re-check residency before inference.**
- [ ] **Step 3: Run three identical synthetic-login trials through the harness** with strict JSON output and bounded `keep_alive=0`; persist sanitized results and durations only.
- [ ] **Step 4: Verify `ollama ps` is empty after the profile and classify `PASS_PROFILE`, `FAIL_HARD_GATE`, `INVALID_OUTPUT`, or a typed backend/resource failure.**
- [ ] **Step 5: Run focused tests and commit the Qwen evidence/checkpoint.**

### Task 4: Ovis first-pass backend compatibility

**Files:**
- Create: `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovis-backend-compatibility.json`
- Modify: `docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md`

**Interfaces:**
- Produces one typed result for each `ATH-MaaS/Ovis2.5-2B` and `ATH-MaaS/OvisOCR2`: `PASS_PROFILE`, `UNSUPPORTED_BACKEND`, `RESOURCE_LIMIT`, or `INVALID_OUTPUT`.

- [ ] **Step 1: Verify no model is resident and inspect current Windows/WSL Python, Torch/Transformers, ROCm/CUDA/Vulkan support without installing a cloud inference client.**
- [ ] **Step 2: Revalidate current candidate runtime requirements against the exact local environment.**
- [ ] **Step 3: If a supported local backend exists, create a task-owned virtual environment, pin the required packages, run one then three synthetic trials sequentially, unload/release, and record exact revisions.**
- [ ] **Step 4: If no supported local backend exists, do not emulate a winner on an unrelated provider; persist `UNSUPPORTED_BACKEND` with the exact missing capability.**
- [ ] **Step 5: Run focused tests and commit compatibility evidence.**

### Task 5: Track B research-value boundary and terminal decision

**Files:**
- Create: `docs/agents/reports/OTCLIENT-20260829-tibia-re-vision-benchmark-execution.md`
- Modify: `docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md`

**Interfaces:**
- Consumes: local profile evidence plus a future secret-safe Track B keyframe handoff.
- Produces: `benchmark_result`, `primary_model`, `ocr_fallback_model`, and `research_value_verdict` without protocol-authority promotion.

- [ ] **Step 1: Record the Track B coordination handoff** from PR #284 comment `5460730478` and revalidate that no network retry was triggered for screenshots.
- [ ] **Step 2: If accepted Track B Linux-container keyframes are available, run the same frozen model profile on pre-attempt/first-change/terminal frames and compare structural-only versus structural+VisualEvidence hypothesis ranking.**
- [ ] **Step 3: If keyframes are unavailable, return `PARTIAL` and `INCONCLUSIVE` rather than extrapolating from synthetic smoke; state exactly which P3-P7 measurements remain missing.**
- [ ] **Step 4: Produce the report with exact host/model/dataset hashes, hard gates, latency/repeatability, candidate blockers, Track B impact, and no-authority boundary.**
- [ ] **Step 5: Run full focused validation, `git diff --check`, checkpoint validation, fresh independent audit, exact-head CI, then close/merge/archive according to repository policy.**
