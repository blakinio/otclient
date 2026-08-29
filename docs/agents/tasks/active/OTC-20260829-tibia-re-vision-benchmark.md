---
task_id: OTC-20260829-tibia-re-vision-benchmark
status: implementing
agent: ChatGPT
project_lane: otclient
lane: P0-DESIGN
track_id: official-client-re
task_kind: documentation
phase: prompt-and-design-persistence
branch: docs/OTC-20260829-tibia-re-local-vision-model-benchmark
base_branch: main
base_sha: 4c751870b5dcd51d5b984b78a4f06625306be961
created: 2026-08-29T07:37:00+02:00
updated: 2026-08-29T07:37:00+02:00
risk: medium
execution_mode: chat_github
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: medium
decomposition_decision: single
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gui_input_authorized: false
process_control_authorized: false
gameplay_allowed: false
local_model_execution_performed: false
molehill_accessed: false
synology_accessed: false
owned_paths:
  - docs/agents/prompts/TIBIA_RE_VISION_BENCHMARK.md
  - docs/agents/prompts/TIBIA_RE_VISION_BENCHMARK_ALIAS.md
  - docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark.md
  - docs/superpowers/specs/2026-08-29-tibia-re-vision-benchmark-design.md
  - docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark.md
modules_touched:
  - agent-prompting
  - official-client-research-design
reuses:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPT_EVAL_STANDARD.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
  - docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md
  - docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md
  - docs/agents/prompts/TIBIA_RE_OLLAMA_LOCAL_RESEARCH_AGENT_POC.md
  - open PR #615 only as non-authoritative discovery input for local-model lifecycle reuse
  - docs/agents/tasks/active/OTC-20260828-game-window-state-qualification.md as the preferred future screen-state benchmark when current live state permits
depends_on: []
blocks: []
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
  completion_claim: internal_only
prompt_contract:
  version: 1.0.0
  changed_surfaces:
    - new repository-owned local vision benchmark coordinator prompt
    - short owner invocation alias
    - benchmark architecture and future implementation plan
  objective: Persist a restart-safe programme for selecting the best local vision/OCR model for official-client reverse engineering on the owner's verified PC, without making visual evidence structural authority or creating a parallel Track A/Control Center plane.
  baseline_version: no prior dedicated vision benchmark prompt
  eval_suite: manual scenario matrix in this task record
  rollback_version: revert this documentation PR
---

# TIBIA RE local vision-model benchmark prompt persistence

## Objective

Persist the architecture, benchmark contract and alias for a future local-PC evaluation of vision/OCR models used only as research evidence around the official Linux Tibia client.

This task is documentation/prompting only. It does not execute any model, access Molehill-PC or Synology, capture a client screen, inspect credentials, perform login, send GUI input, attach to the official client, mutate Track A state, or run gameplay actions.

## Live-state findings used by this design

- Trusted base at task creation: `main@4c751870b5dcd51d5b984b78a4f06625306be961`.
- No existing PR matched `TIBIA-RE-VISION`, `VISION-MODEL-BENCHMARK`, Ovis/OCR or Qwen vision benchmark ownership.
- Draft PR #615 is the closest overlap. It implements a bounded local Ollama PoC harness but is blocked and remains unmerged. It is discovery input only; this task must not copy unmerged code or take its owned paths.
- Current Track A hybrid routing keeps the physical official-client runtime on Synology and routes deterministic/disposable analysis away from the scarce physical runtime.
- Control Center Adapter v1 already defines passive capture/snapshot/event semantics; the vision layer should consume those semantics rather than define a second control plane.
- Current `gameWindowState` qualification already defines a high-value future four-state sequence: `LOGIN_SCREEN -> CHARACTER_SELECT -> WORLD -> WORLD_EXIT`. This is the preferred first screen-state benchmark when secret-safe captures/current runtime admission are available.

## Design decision

Create a model-agnostic `VisualEvidence` research layer. Local models run on the verified owner PC and consume only approved secret-safe screenshots/keyframes/ROIs. Their outputs remain `visual_only` evidence and never satisfy Track A structural read/action gates by themselves.

Initial candidate set, to be revalidated at execution time rather than treated as permanent availability:

1. `Qwen/Qwen3-VL-4B-Instruct` — primary whole-screen/UI-semantic hypothesis.
2. `ATH-MaaS/Ovis2.5-2B` — lightweight whole-screen/UI-semantic challenger.
3. `ATH-MaaS/OvisOCR2` — specialized exact-text/OCR challenger.
4. Optional second-pass challengers only after the first three finish: `Qwen/Qwen3-VL-4B-Thinking` and a memory-safe quantized `ATH-MaaS/Ovis2.5-9B` if current backend support and resource limits are proven.

No model is declared the winner by this documentation task.

## Benchmark score

Weighted score:

- 30% semantic UI / before-after correctness;
- 25% negative-control and hallucination resistance;
- 20% critical-text exact-match OCR;
- 10% repeatability/determinism;
- 10% latency;
- 5% peak VRAM/RAM efficiency.

Hard gates override the weighted score:

- schema-valid output: 100%;
- secret leakage/persistence: 0;
- false `IN_GAME` on login/character-selection benchmark cases: 0;
- model receives no runtime/action authority;
- no model-authored executable action parameters;
- at most one local model resident or actively inferencing at a time;
- no silent cloud/API fallback;
- every result records exact model revision/digest where available, backend, prompt/schema version and input hashes.

## Benchmark phases

1. Host/backend proof and one-model residency.
2. Fixed screen-state classification: login, character selection, world, world exit.
3. Tibia text/ROI exact OCR.
4. Paired before/after UI-delta extraction.
5. Negative controls and hallucination tests.
6. Performance/resource measurements on the same frozen inputs.
7. Causal-correlation usefulness against structural Track A evidence.
8. Deterministic/no-VLM baseline versus VisualEvidence-assisted research decisions.
9. Winner/fallback decision or explicit `NO_WINNER`.

## Manual prompt-eval matrix

This is a static documentation review, not model execution.

| Case | Expected behavior | Result |
|---|---|---|
| Fresh agent is given only alias | Resolve current prompt/task from repository state; do not depend on chat history | PASS |
| User PC hardware differs from remembered profile | Verify live host/GPU/RAM/backend; do not trust remembered hardware | PASS |
| Different local model is already resident | Fail closed, unload/verify according to current policy before switching | PASS |
| Qwen produces best OCR but hallucinates UI changes | Hard/weighted quality metrics decide; do not declare winner from OCR alone | PASS |
| OvisOCR2 reads text well but cannot classify full UI reliably | Permit OCR-specialist fallback role without making it primary | PASS |
| Model labels login screenshot as IN_GAME | Hard-gate failure for that model/configuration | PASS |
| Screenshot may contain credentials/session secrets | Reject/quarantine before model inference or persistence | PASS |
| Open PR #615 contains reusable code | Treat as discovery only until trusted-main merge; do not copy unmerged code | PASS |
| Current Control Center capture is unavailable | Use approved existing secret-safe artifacts/offline dataset or return exact blocker; do not invent a second capture plane | PASS |
| Model proposes gameplay action | Ignore/refuse; vision benchmark has no action authority | PASS |
| Benchmark winner changes under a different backend/quantization | Record configuration-specific result; do not generalize across profiles without compatibility eval | PASS |
| One successful run looks impressive | Require fixed dataset/repeatability and baseline comparison before recommendation | PASS |

Static matrix: **12/12 PASS** by implementer self-review. No claim is made that the future runtime/model benchmark has executed.

## Acceptance inventory

- [ ] Canonical prompt exists and is self-contained.
- [ ] Alias exists and resolves to the canonical prompt.
- [ ] Design spec exists with architecture, evidence boundary and benchmark methodology.
- [ ] Future implementation plan exists and preserves reuse/fail-closed rules.
- [ ] Prompt explicitly preserves `visual_only` non-authoritative evidence semantics.
- [ ] Prompt serializes local model residency/inference and forbids cloud fallback.
- [ ] Prompt contains fixed benchmark metrics, hard gates and a `NO_WINNER` outcome.
- [ ] Prompt reuses current Track A/Control Center contracts rather than creating a second control plane.
- [ ] Full changed-file inventory contains only the five declared documentation paths.
- [ ] Runtime/model E2E is `NOT_APPLICABLE` for this persistence task because it performs no runtime/model execution.
- [ ] Exact-head repository CI and PR hygiene are verified before completion/merge.

## Current checkpoint

```yaml
checkpoint_version: 1
status: implementing
base_sha: 4c751870b5dcd51d5b984b78a4f06625306be961
branch: docs/OTC-20260829-tibia-re-local-vision-model-benchmark
pr: pending
runtime_access: none
local_model_execution_performed: false
molehill_accessed: false
synology_accessed: false
credentials_accessed: false
material_findings_open: 0
next_action: persist canonical prompt, alias, design spec and future implementation plan; open/update Draft PR; verify exact changed paths and prompt-content matrix
```
