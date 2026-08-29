# TIBIA RE Local Vision Model Benchmark — Design

## Status and scope

This design defines a future local vision/OCR research layer for the official Linux Tibia reverse-engineering programme in `blakinio/otclient`.

It does **not** make OCR or a VLM part of the authoritative Agent Game API. Structural Track A evidence remains the source of truth for read/action promotion. Visual model output is auxiliary research evidence only.

The intended first execution topology is:

```text
Synology / canonical Track A
  official Linux Tibia client
  passive approved screenshot/keyframe capture
          |
          v
approved secret-safe evidence transport
          |
          v
owner PC / Molehill-PC
  local vision benchmark harness
  exactly one resident/inferencing model
          |
          v
strict VisualEvidence JSON
          |
          v
causal correlation / research evaluation
```

The future worker must revalidate the actual host, GPU, RAM, OS/backend, model availability, current Track A contracts and executable Control Center state. Remembered hardware/runtime facts are discovery input only.

## Problem

The official-client RE programme already collects structural evidence from Qt/runtime objects, protocol paths, memory and controlled experiments. Human-visible UI changes are useful ground truth during discovery, but manually inspecting screenshots does not scale and timestamp-only visual interpretation is inconsistent.

A local vision model can provide a machine-readable observation stream for questions such as:

- which client screen is visible;
- which UI panel appeared or disappeared;
- what exact short text is visible;
- what changed between a before/after pair;
- when a visible event occurred relative to structural traces.

The model must not become runtime authority, action authority, a credential handler or a substitute for structural evidence.

## Existing repository boundaries to reuse

The design reuses rather than replaces:

- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md` for physical-runtime versus deterministic-analysis routing;
- `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md` for causal evidence, negative controls and structural promotion gates;
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md` for passive `snapshot`, `capture_start`, `capture_stop` and `SCREEN` event semantics;
- the root `AGENTS.md` local-model rule: at most one resident or actively inferencing local model at a time;
- the existing local Ollama PoC prompt and, if it later reaches trusted `main`, its executable lifecycle helpers. Open Draft PR #615 is discovery input only and must not be copied or treated as trusted executable capability.

## Approaches considered

### A. OvisOCR2-only

Run `ATH-MaaS/OvisOCR2` on screenshots/ROIs and use OCR text as the visual signal.

Advantages:

- small model and low resource pressure;
- strong fit for exact text extraction;
- easy to score with exact-match/CER/WER.

Limitations:

- weak architectural fit for whole-screen semantic questions;
- does not directly solve before/after UI understanding;
- risks optimizing the research layer around text while many useful Tibia visual events are layout/state changes.

### B. One general VLM only

Choose one whole-screen VLM, initially `Qwen/Qwen3-VL-4B-Instruct`, and use it for screen classification, OCR and UI-delta extraction.

Advantages:

- one model lifecycle;
- simple integration;
- whole-screen semantic capability.

Limitations:

- selection would be based on prior expectations rather than project-specific evidence;
- a general VLM may lose exact small-text OCR to a specialized model;
- no principled way to determine whether another small model is better on the owner's hardware/backend.

### C. Model-agnostic benchmark and role selection — chosen

Define one strict `VisualEvidence` contract, benchmark multiple local models sequentially on frozen Tibia-specific inputs, and select a primary model plus an optional specialized fallback only if measured evidence supports it.

Advantages:

- project-specific, repeatable model selection;
- separates whole-screen semantics from exact OCR quality;
- allows `NO_WINNER` when no model satisfies hard gates;
- model/backend changes do not alter Track A authority;
- supports future replacement without redesigning the evidence plane.

Cost:

- requires a small benchmark/evaluation layer before integration.

This is the selected design.

## Candidate set

Initial first-pass candidates, subject to live availability/backend verification:

1. `Qwen/Qwen3-VL-4B-Instruct` — primary whole-screen/UI-semantic hypothesis.
2. `ATH-MaaS/Ovis2.5-2B` — lightweight general-vision challenger.
3. `ATH-MaaS/OvisOCR2` — specialized text/OCR challenger.

Optional second-pass candidates only after first-pass completion:

- `Qwen/Qwen3-VL-4B-Thinking` for difficult semantic cases;
- memory-safe quantized `ATH-MaaS/Ovis2.5-9B` only if current backend compatibility, quantization provenance and resource limits are proven.

No candidate receives a preferred score because of public benchmark claims. The winner is determined by the frozen Tibia-specific suite.

## VisualEvidence contract

The future implementation should normalize every model output before it reaches the research correlator:

```yaml
schema_version: 1
capture:
  evidence_ref: string
  sha256: string
  source_monotonic_ns: integer | null
model:
  model_id: string
  model_revision_or_digest: string
  backend: string
  backend_version: string
  quantization: string | null
  prompt_version: string
observation:
  screen_class: LOGIN_SCREEN | CHARACTER_SELECT | IN_GAME_VISUAL | WORLD_EXIT | OTHER | UNKNOWN
  visible_text: [string]
  ui_objects: [object]
  appeared: [object]
  disappeared: [object]
  changed: [object]
quality:
  schema_valid: bool
  visual_only: true
  structural_authority: false
  unknown_fields: [string]
```

`IN_GAME_VISUAL` deliberately differs from canonical structural `IN_GAME`. No downstream component may promote it to structural session authority by name conversion or implicit truthiness.

## Input privacy boundary

Before inference, each image must be classified as safe for local model processing and persistence.

Reject/quarantine rather than infer when the frame may contain:

- account credentials;
- 2FA values;
- session/auth tokens;
- secret-bearing console/debug overlays;
- other material classified as secret by current repository rules.

Do not upload screenshots to cloud/API services. Local model inference must remain on the verified owner host unless the owner separately authorizes a different exact service and repository policy permits it.

Private unrelated chat/player data should be cropped, omitted or redacted unless it is deliberately test-generated and necessary for the benchmark.

## Model lifecycle and resource policy

At most one local model may be resident or actively inferencing on the physical host.

For each candidate/configuration:

```text
verify model slot empty or exact target only
-> load target
-> run frozen trials
-> persist sanitized metrics/results
-> unload target
-> verify target released
-> only then proceed to next model
```

Unknown residency or a different resident model fails closed.

No silent model pull, cloud fallback or alternate provider is allowed during a frozen comparison. Any changed model revision, backend, quantization or prompt/schema version defines a new benchmark profile.

## Benchmark datasets

### Dataset A — four-state screen classification

Preferred first ground truth is the current Track A `gameWindowState` qualification sequence when secret-safe captures are available:

```text
LOGIN_SCREEN
CHARACTER_SELECT
WORLD
WORLD_EXIT
```

The visual labels remain independent of the structural labels used for ground truth.

Target: at least 25 accepted keyframes per class for a meaningful first pass when available. A smaller smoke set may validate the harness but cannot select a production recommendation.

### Dataset B — exact Tibia text/ROI

Representative secret-safe ROIs:

- center/system messages;
- container titles;
- NPC/test-generated text;
- battle-list creature names;
- popup title/body;
- explicit no-text negative controls.

Store expected normalized text separately from images and hash both inputs.

### Dataset C — paired UI delta

Frozen before/after pairs for transitions such as:

- container closed -> opened;
- target absent -> selected;
- no popup -> popup;
- NPC dialog absent -> present;
- character selection -> world;
- world -> exit/disconnect screen.

The output is a strict set of appeared/disappeared/changed semantic objects, not free-form prose.

### Dataset D — negative controls

Cases where requested events are absent. A model should return `UNKNOWN`/empty sets rather than inventing text, panels or state transitions.

## Metrics and hard gates

Weighted score:

| Weight | Metric family |
|---:|---|
| 30% | semantic screen/UI and before-after correctness |
| 25% | negative-control / hallucination resistance |
| 20% | critical-text exact-match OCR |
| 10% | repeated-trial stability |
| 10% | warm p50/p95 latency |
| 5% | peak VRAM/RAM efficiency |

Hard gates override weighted score:

- 100% schema-valid benchmark output;
- zero secret leakage/persistence events;
- zero false `IN_GAME_VISUAL` predictions on accepted login-screen or character-selection hard-gate cases;
- zero runtime/action authority exposed to the model;
- zero model-authored executable action parameters;
- one-model residency policy always satisfied;
- no silent cloud/provider fallback;
- complete model/backend/input/prompt provenance for scored trials.

A candidate failing a hard gate cannot be selected as primary regardless of weighted score.

## Repeatability

Use frozen input hashes and frozen prompt/schema versions. Run at least three repeated inference trials per safety-critical case when the model is nondeterministic or when sampling cannot be fully disabled.

Record disagreement rather than majority-repairing malformed or contradictory output.

## Research-value test

Model quality is not the same as RE acceleration.

After visual accuracy testing, compare two research conditions on the same frozen structural evidence:

```text
A: structural evidence only
B: identical structural evidence + normalized VisualEvidence
```

Measure:

- correct hypothesis/candidate ranking;
- false hypothesis count;
- number of bounded experiments needed;
- time/steps to a valid candidate;
- whether VisualEvidence changes the correct decision.

Use a deterministic/no-VLM baseline where practical. One successful case cannot justify a general acceleration claim.

## Causal correlation integration

When a visual event has source timing, preserve it alongside the existing causal recorder rather than rewriting structural events:

```yaml
visual_event_monotonic_ns: integer | null
visual_event_type: string
visual_evidence_ref: string
visual_model_profile: string
```

Correlation may rank candidate handlers/memory objects/messages around a visual event, but timing correlation alone does not promote causality. Current negative-control and restart/rediscovery requirements remain unchanged.

## Failure handling

Return explicit typed outcomes:

```text
PASS_PROFILE
FAIL_HARD_GATE
UNSUPPORTED_BACKEND
RESOURCE_LIMIT
INVALID_OUTPUT
SECRET_INPUT_REJECTED
MODEL_SLOT_NOT_EXCLUSIVE
NO_WINNER
INCONCLUSIVE_RESEARCH_VALUE
```

Do not silently repair invalid JSON with another model. Do not switch to another provider during the same frozen profile.

## Selection outcome

The benchmark may produce:

```yaml
primary_model: <profile id> | null
ocr_fallback_model: <profile id> | null
benchmark_result: WINNER | ROLE_SPLIT | NO_WINNER | PARTIAL
research_value_verdict: SUPPORTED_FOR_TESTED_CASES | NOT_SUPPORTED_FOR_TESTED_CASES | INCONCLUSIVE
```

A role split is valid only when the specialized fallback materially improves a predefined metric and the extra model-switch/load cost is acceptable under the one-model residency rule.

## Expected first hypothesis, not a result

Before project-specific execution, the working hypothesis is:

- `Qwen/Qwen3-VL-4B-Instruct` may be the best primary whole-screen/UI model;
- `ATH-MaaS/OvisOCR2` may be the best exact-text specialist;
- `ATH-MaaS/Ovis2.5-2B` is the lightweight general challenger.

These are hypotheses only. The future benchmark must be allowed to disprove all three.

## Testing layers

1. Schema/unit tests with synthetic fixtures.
2. Deterministic scorer tests, including hard-gate precedence.
3. Model-runner contract tests using fake local model responses.
4. Offline real-model benchmark on secret-safe frozen images on the verified owner PC.
5. Optional read-only Control Center capture integration after current executable/passive prerequisites are proven.
6. Research-value A/B comparison against the same structural evidence bundle.
7. Fresh compatibility evaluation whenever model family, backend, quantization, prompt schema or hardware profile materially changes.

## Non-goals

This design does not:

- make OCR/VLM output authoritative gameplay state;
- create a bot or autonomous gameplay loop;
- grant credentials/login/session authority;
- grant GUI input, process control, attach/injection or network mutation;
- replace Track A, Control Center, Scenario Engine, Safety Controller or evidence store;
- require more than one model in VRAM at once;
- declare a model winner before measurement.

## Approval and future execution

The durable owner alias is `TIBIA-RE-VISION-BENCHMARK`. A future invocation must resolve live repository state first, then execute only the currently safe READY phases. The alias is an owner command to continue the benchmark programme; it never overrides current repository/runtime authority gates.
