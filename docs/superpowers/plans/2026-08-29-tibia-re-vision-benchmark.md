# TIBIA RE Vision Benchmark Persistence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist a repository-owned, restart-safe local vision/OCR benchmark programme and short alias for official-client reverse engineering without changing Track A runtime authority.

**Architecture:** Keep this PR documentation-only. Store the model-agnostic architecture in a design spec, the executable owner-facing coordinator contract in `docs/agents/prompts/`, the short alias beside it, and durable task state under `docs/agents/tasks/active/`. Future runtime/model implementation is explicitly deferred to a later task resolved from the canonical prompt and current trusted `main`.

**Tech Stack:** Markdown/YAML contracts, existing `blakinio/otclient` prompting and Track A governance.

**Spec:** `docs/superpowers/specs/2026-08-29-tibia-re-vision-benchmark-design.md`

## Global Constraints

- Repository writes are limited to `blakinio/otclient`.
- This persistence task has `runtime_access: none` and performs no local model inference, Molehill/Synology access, screen capture, login, credentials, GUI input, gameplay, process control or Track A mutation.
- Visual model output remains `visual_only` and cannot satisfy structural Track A R/A evidence gates by itself.
- At most one local model may be resident or actively inferencing at a time in the future benchmark.
- No cloud/API fallback is authorized by this programme alias.
- Draft PR #615 remains discovery input only until its code reaches trusted `main`; do not copy or depend on unmerged executable code.
- Documentation-only runtime E2E is `NOT_APPLICABLE` with an explicit reason; exact changed paths, prompt content, PR hygiene and exact-head repository CI remain required.

---

### Task 1: Persist architecture and task ownership

**Files:**
- Create: `docs/superpowers/specs/2026-08-29-tibia-re-vision-benchmark-design.md`
- Create: `docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark.md`

**Interfaces:**
- Consumes: current `AGENTS.md`, `PROMPTING_STANDARD.md`, `PROMPT_EVAL_STANDARD.md`, Track A hybrid-routing/experiment contracts, Control Center Adapter v1, current active tasks and open PRs.
- Produces: stable architecture, five-path ownership declaration, initial candidate set, benchmark metrics/hard gates and durable checkpoint.

- [ ] **Step 1: Revalidate trusted base and overlap**

Verify current `main` SHA, search open/closed PRs for vision/OCR/Ovis/Qwen benchmark ownership, inspect active Track A tasks, and record the closest reusable work without taking its paths.

Expected: no existing dedicated vision benchmark owner; any Draft-only implementation is classified as discovery input.

- [ ] **Step 2: Create the bounded task record**

Record `runtime_access: none`, zero runtime/model/credential effects, exactly five owned documentation paths, current base SHA, prompt contract v1.0.0, reuse list, acceptance inventory and one `next_action`.

Expected: a fresh agent can identify scope/ownership without chat history.

- [ ] **Step 3: Persist the design spec**

Document approaches considered, chosen model-agnostic design, `VisualEvidence` contract, candidate set, datasets, scoring/hard gates, privacy boundary, one-model lifecycle, causal-correlation use and `NO_WINNER` outcome.

Expected: the spec never declares a benchmark winner or gives visual evidence structural authority.

- [ ] **Step 4: Self-review the spec**

Check for placeholders, contradictions, implicit runtime authority, cloud fallback, unversioned model-output schema, missing negative controls and accidental dependence on PR #615.

Expected: zero material findings remain before prompt persistence.

- [ ] **Step 5: Commit**

Commit the task/spec as documentation changes using Conventional Commits.

---

### Task 2: Persist canonical programme prompt and alias

**Files:**
- Create: `docs/agents/prompts/TIBIA_RE_VISION_BENCHMARK.md`
- Create: `docs/agents/prompts/TIBIA_RE_VISION_BENCHMARK_ALIAS.md`

**Interfaces:**
- Consumes: design spec and current Prompting Standard 2.1.
- Produces: alias `TIBIA-RE-VISION-BENCHMARK` and a self-contained coordinator prompt that resolves current repository/runtime/model state before future work.

- [ ] **Step 1: Write the canonical prompt**

Include role/phase, repository/live-state preflight, objective, authority/non-goals, trust boundary, feature scope, required reads, local-host proof, candidate revalidation, benchmark phases, `VisualEvidence` schema, privacy/resource policy, fixed metrics/hard gates, research-value A/B comparison, acceptance, closeout and terminal response contract.

Expected: future execution may run local models only after current host/backend/resource proof and may use live Track A capture only after applicable passive/read-only admission; the alias itself grants no login/GUI/gameplay/process authority.

- [ ] **Step 2: Write the alias**

Expose exactly:

```text
Uruchom TIBIA-RE-VISION-BENCHMARK autonomicznie.
Kontynuuj TIBIA-RE-VISION-BENCHMARK autonomicznie.
```

The alias points to the canonical prompt, requires live-state resolution, allows local model benchmarking on the verified owner PC, forbids cloud/API fallback, and preserves one-model residency.

- [ ] **Step 3: Verify alias/canonical version alignment**

Check both files use prompt contract `1.0.0`, `track_id: official-client-re`, autonomous continuation metadata, `runtime_access` classification before any live work and the same programme boundary.

Expected: no stale path/name/version mismatch.

- [ ] **Step 4: Commit**

Commit the canonical prompt and alias as one logical documentation change.

---

### Task 3: Prompt evaluation and durable checkpoint

**Files:**
- Modify: `docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark.md`

**Interfaces:**
- Consumes: prompt, alias and design spec on the exact branch head.
- Produces: documented manual scenario matrix, acceptance results, exact changed-file inventory and next closeout action.

- [ ] **Step 1: Run the manual scenario matrix**

Evaluate at minimum: fresh-alias resolution; changed hardware; occupied model slot; OCR-versus-hallucination trade-off; OCR-specialist fallback; false `IN_GAME_VISUAL`; secret-bearing screenshot; Draft PR dependency; unavailable capture; model action proposal; backend/quantization change; one-run overclaim.

Expected: each case has an explicit expected behaviour and PASS/FAIL; this is labelled static/manual, not automated model evidence.

- [ ] **Step 2: Verify changed paths**

Compare branch to its base and require exactly:

```text
docs/agents/prompts/TIBIA_RE_VISION_BENCHMARK.md
docs/agents/prompts/TIBIA_RE_VISION_BENCHMARK_ALIAS.md
docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark.md
docs/superpowers/specs/2026-08-29-tibia-re-vision-benchmark-design.md
docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark.md
```

Expected: no source, workflow, runtime, secret or shared-index changes.

- [ ] **Step 3: Update checkpoint**

Set prompt/alias/spec/plan acceptance items to PASS only after direct file inspection. Keep runtime/model E2E `NOT_APPLICABLE` with the reason that this task persists documentation only.

- [ ] **Step 4: Commit**

Commit the final documentation checkpoint.

---

### Task 4: PR validation and closeout

**Files:**
- Modify only the task record if validation state changes.

**Interfaces:**
- Consumes: exact final branch head and Draft PR.
- Produces: verified PR/CI/review state and either a terminal merge/archive or one exact waiting/blocker action.

- [ ] **Step 1: Review full PR diff**

Inspect every changed file and confirm the prompt does not weaken Track A authority, privacy, evidence gates, model-slot policy or closeout requirements.

- [ ] **Step 2: Verify repository checks on the exact head**

Observe the aggregate required CI/governance result for the exact final SHA. Do not claim success from an earlier head.

- [ ] **Step 3: Check review hygiene**

Require zero unresolved review threads and disposition any material finding before readiness.

- [ ] **Step 4: Finalize according to repository gates**

If all documentation/prompt acceptance, required audit/review and exact-head CI gates are satisfied, mark ready and squash-merge under current repository policy, then archive/release task ownership. If an independent audit/review required by current governance cannot be obtained in this invocation, leave the PR intentionally Draft/WAITING with one concrete `next_action`; do not fabricate completion.
