---
task_id: OTC-20260829-tibia-re-vision-benchmark
status: completed
agent: ChatGPT
project_lane: otclient
lane: P0-DESIGN
track_id: official-client-re
task_kind: documentation
phase: archived
branch: docs/OTC-20260829-tibia-re-local-vision-model-benchmark
base_branch: main
base_sha: 4c751870b5dcd51d5b984b78a4f06625306be961
related_pr: "787"
created: 2026-08-29T07:37:00+02:00
updated: 2026-08-29T08:03:37+02:00
completed: 2026-08-29T08:03:37+02:00
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
molehill_accessed: true
molehill_access_scope: closeout_validation_and_benchmark_readiness_preflight_only
synology_accessed: false
owned_paths: []
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
    - benchmark architecture and persistence plan
  objective: Persist a restart-safe programme for selecting the best local vision/OCR model for official-client reverse engineering on the owner's verified PC, without making visual evidence structural authority or creating a parallel Track A/Control Center plane.
  baseline_version: no prior dedicated vision benchmark prompt
  eval_suite: manual scenario matrix in this task record
  rollback_version: revert this documentation PR
---

# TIBIA RE local vision-model benchmark prompt persistence

## Objective

Persist the architecture, benchmark contract and alias for a future local-PC evaluation of vision/OCR models used only as research evidence around the official Linux Tibia client.

The implementation change is documentation/prompting only. Fresh closeout validation in the current owner invocation used the existing Molehill-PC repository worktree plus local hardware/Ollama readiness inspection, but executed no model inference, accessed no Synology or official-client runtime, captured no client screen, accessed no credential, performed no login, sent no GUI input, attached to no official-client process, mutated no Track A state and performed no gameplay action.

## Verified live-state basis

- Task branch was created from trusted `main@4c751870b5dcd51d5b984b78a4f06625306be961`.
- No existing PR matched `TIBIA-RE-VISION`, `VISION-MODEL-BENCHMARK`, Ovis/OCR or Qwen vision benchmark ownership.
- Draft PR #615 is the closest overlap. Its unmerged harness remains discovery input only and none of its owned paths are changed here.
- Track A hybrid routing keeps the physical official-client runtime on Synology and routes deterministic/disposable analysis away from the scarce physical runtime.
- Control Center Adapter v1 already defines passive capture/snapshot/event responsibilities; this design consumes those semantics rather than inventing a second control plane.
- Current `gameWindowState` qualification provides the preferred future four-state benchmark sequence `LOGIN_SCREEN -> CHARACTER_SELECT -> WORLD -> WORLD_EXIT` when current admission and secret-safe captures permit it.

## Persisted design decision

Use a model-agnostic `VisualEvidence` layer. Candidate models run locally on the verified owner PC against frozen secret-safe Tibia inputs. Output remains `visual_only` and `structural_authority: false`; visual evidence cannot satisfy Track A R/A promotion gates by itself.

Initial candidates are hypotheses to revalidate at execution time:

1. `Qwen/Qwen3-VL-4B-Instruct` — whole-screen/UI-semantic hypothesis.
2. `ATH-MaaS/Ovis2.5-2B` — lightweight general-vision challenger.
3. `ATH-MaaS/OvisOCR2` — specialized exact-text/OCR challenger.
4. Optional second pass only after first-pass completion: `Qwen/Qwen3-VL-4B-Thinking` and a proven memory-safe quantized `ATH-MaaS/Ovis2.5-9B` profile.

No winner is claimed by this persistence task.

## Benchmark contract

Weighted score:

- 30% semantic UI / before-after correctness;
- 25% negative-control and hallucination resistance;
- 20% critical-text exact-match OCR;
- 10% repeatability/determinism;
- 10% latency;
- 5% peak VRAM/RAM efficiency.

Hard gates override weighted score:

- schema-valid output: 100%;
- secret leakage/persistence: 0;
- false visual `IN_GAME` on login/character-selection hard-gate cases: 0;
- model runtime/action authority: 0;
- model-authored executable action parameters: 0;
- at most one resident or actively inferencing local model at a time;
- no silent cloud/API/provider fallback;
- complete scored-trial model/backend/prompt/input provenance.

The future programme includes host/backend proof, four-state screen classification, exact ROI OCR, paired UI-delta extraction, negative controls, resource/latency measurements, repeated trials, causal-correlation usefulness and deterministic/no-VLM research-value comparison. `NO_WINNER` is a valid terminal benchmark result.

## Manual prompt-eval matrix

This is a static documentation review, not model execution.

| Case | Expected behavior | Result |
|---|---|---|
| Fresh agent receives only alias | Resolve current prompt/task from repository state; do not depend on chat history | PASS |
| Owner PC differs from remembered profile | Verify live host/GPU/RAM/backend; remembered hardware is discovery input only | PASS |
| Different local model is resident | Fail closed; unload/verify before switching according to current policy | PASS |
| General VLM has strong OCR but hallucinates UI changes | Hard/weighted quality metrics decide; OCR alone cannot win | PASS |
| OvisOCR2 reads text well but weakly classifies full UI | Permit measured OCR-specialist role without making it primary | PASS |
| Model labels login/character-selection screenshot as IN_GAME_VISUAL | Hard-gate failure for that profile | PASS |
| Screenshot may contain credentials/session secrets | Reject/quarantine before inference or ordinary persistence | PASS |
| Open PR #615 contains useful code | Treat as discovery only until trusted-main merge; do not copy unmerged code | PASS |
| Current Control Center capture is unavailable | Use approved secret-safe offline evidence or exact blocker; do not create a second capture plane | PASS |
| Model proposes gameplay action | Refuse/ignore; vision benchmark has no action authority | PASS |
| Backend/quantization changes | Treat as a new model profile; require targeted compatibility result | PASS |
| One successful run looks impressive | Require fixed dataset/repeatability/baseline before recommendation | PASS |

Static matrix: **12/12 PASS** by implementer self-review. It is not an automated/model benchmark pass and not an independent audit.

## Direct persistence verification

Direct branch reads verified:

- canonical prompt exists, contract version `1.0.0`, alias `TIBIA-RE-VISION-BENCHMARK`, autonomous continuation metadata and explicit no-cloud/no-runtime-authority boundaries;
- alias exists, contract version `1.0.0`, points to `docs/agents/prompts/TIBIA_RE_VISION_BENCHMARK.md`, exposes start/continue owner commands and preserves local-only/one-model/non-authoritative rules;
- design spec exists and chooses the model-agnostic benchmark after considering OvisOCR2-only and one-general-VLM approaches;
- implementation plan exists and keeps this PR documentation-only while deferring real runtime/model implementation to a future task.

Branch comparison against the base verified exactly five changed files and no source/workflow/runtime/shared-index changes.

## Acceptance inventory

- [x] Canonical prompt exists and is self-contained.
- [x] Alias exists and resolves to the canonical prompt.
- [x] Design spec exists with architecture, evidence boundary and benchmark methodology.
- [x] Persistence/future-work plan exists and preserves reuse/fail-closed rules.
- [x] Prompt explicitly preserves `visual_only` non-authoritative evidence semantics.
- [x] Prompt serializes local model residency/inference and forbids silent cloud/API fallback.
- [x] Prompt contains fixed benchmark metrics, hard gates and a `NO_WINNER` outcome.
- [x] Prompt reuses current Track A/Control Center contracts rather than creating a second control plane.
- [x] Full changed-file inventory contains only the five declared documentation paths.
- [x] Runtime/model E2E is `NOT_APPLICABLE`: this persistence task performs no runtime/model execution.
- [x] Exact-final-head repository CI/review hygiene and fresh independent audit passed before squash merge.

## Fresh independent closeout audit

Fresh coordinator/validator context independently re-read the exact PR diff, prompt, alias, spec, plan, task record, current trusted governance, live PR state and exact-head checks instead of relying on the implementer self-review.

Finding `VISION-DOC-AUD-001` identified that the task checkpoint used the obsolete `checkpoint_version: 2` shape and therefore failed the current deterministic checkpoint validator. The remediation below restores the normative version-1 checkpoint shape without changing programme authority, benchmark acceptance, runtime scope or the four other owned documents.

Audit evidence before this remediation:

- exact pre-remediation head: `5be9e8bf3e7b2ca634ecd48019c2b18b333ce83d`;
- GitHub CI run `33236846075`: PASS;
- Track A governance run `33236844673`: PASS;
- PR #787 had zero comments/review threads and was mergeable;
- `git diff --check origin/main...HEAD`: PASS;
- full changed-file set: exactly the five declared documentation paths;
- direct contract checks for prompt/alias v1.0.0, `visual_only`, `structural_authority: false`, no-cloud, one-model residency and `NO_WINNER`: PASS;
- deterministic checkpoint validator initially failed only on stale checkpoint schema (`VISION-DOC-AUD-001`); after the task-only remediation it passes.

Fresh independent audit result after remediation: **PASS_BOUNDED** (`fresh_coordinator_session`), `VISION-DOC-AUD-001` resolved, material findings open: **0**. Exact-final-head GitHub checks remain a separate closeout gate.

## Terminal closeout

PR #787 final ready head `3b322bda50daf7e23e7640e174a80abf40d2b82e` passed CI run `33237454649` and Track A governance run `33237454525`, remained mergeable with zero review comments/threads, and was squash-merged as `da2b511399c9a8447fdf6422cac6ff12b76085e7`. Fresh independent documentation audit result was `PASS_BOUNDED` with `VISION-DOC-AUD-001` resolved and zero open material findings. Runtime/model E2E is `NOT_APPLICABLE` because this PR persisted documentation/prompting only and performed no model inference or official-client runtime execution.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-29T08:03:37+02:00
head: 3b322bda50daf7e23e7640e174a80abf40d2b82e
branch: main
pr: 787
status: completed
context_routes:
  - agent-prompting
  - official-client-research-design
owned_paths: []
proven:
  - PR 787 exact final ready head 3b322bda50daf7e23e7640e174a80abf40d2b82e passed CI run 33237454649
  - PR 787 exact final ready head passed Track A governance run 33237454525
  - fresh independent documentation audit PASS_BOUNDED with zero open material findings
  - PR 787 squash-merged as da2b511399c9a8447fdf6422cac6ff12b76085e7
  - runtime/model E2E is NOT_APPLICABLE because the merged deliverable is documentation/prompting only
derived: []
unknown:
  - none
conflicts: []
first_failure:
  marker: VISION-DOC-AUD-001
  evidence: stale checkpoint_version 2 shape was repaired before final exact-head validation and merge
rejected_hypotheses:
  - prompt or alias contract mismatch
  - unexpected changed path outside declared documentation scope
changed_paths:
  - docs/agents/tasks/archive/OTC-20260829-tibia-re-vision-benchmark.md
validation:
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark.md --require-checkpoint
    result: PASS
    evidence: final pre-merge task checkpoint validated on 3b322bda50daf7e23e7640e174a80abf40d2b82e
  - command: GitHub CI
    result: PASS
    evidence: run 33237454649 on exact final ready head
  - command: Track A agent runtime governance
    result: PASS
    evidence: run 33237454525 on exact final ready head
  - command: runtime/model E2E
    result: NOT_APPLICABLE
    evidence: merged PR 787 changed documentation/prompting only and executed no model inference or official-client runtime
blockers: []
next_action: after this archive PR merges, start the separately scoped real local vision benchmark execution task from exact current main and keep the Track B secret-safe screenshot handoff as a dependency for project-specific research-value evaluation
```

## Closeout record

```yaml
closeout:
  implementation_complete: true
  vertical_slice_complete: true
  audit:
    result: PASS_BOUNDED
    independent_validator: fresh_coordinator_session
    material_findings_open: 0
  e2e:
    result: NOT_APPLICABLE
    reason: documentation/prompting persistence only; no runtime/model execution in PR 787
  final_ci:
    head: 3b322bda50daf7e23e7640e174a80abf40d2b82e
    result: PASS
    required_checks:
      - CI 33237454649
      - Track A governance 33237454525
  pull_requests:
    vision_programme_787: MERGED
    unresolved_review_threads: 0
  task_status: completed
  task_archived: true
  ownership_released: true
  blocker: none
  next_action: after this archive PR merges, start the separately scoped real local vision benchmark execution task from exact current main and keep the Track B secret-safe screenshot handoff as a dependency for project-specific research-value evaluation
```
