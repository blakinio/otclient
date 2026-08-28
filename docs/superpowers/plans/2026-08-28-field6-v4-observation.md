# Field6 V4 Observation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the consumed V3 field6 trigger with a fail-closed V4 generation, admit exactly one fresh scalar-only login observation, and promote only the proven sanitized `uint32` result.

**Architecture:** Keep the existing exact-current package materializer, secret wrapper, GDB-as-parent observer, artifact schema, and 18-minute job deadline unchanged. The static generation PR changes only the exact trigger generation and its contract; the later docs-only admission changes runtime authority only after the generation is trusted on `main`; the one live run must still fail closed before login if package/fence verification changes.

**Tech Stack:** GitHub Actions YAML, Python contract tests, Bash runtime helpers, Track A repository governance, official native Linux Tibia exact-current fence.

**Spec:** `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`

## Global Constraints

- Exact-current locator until freshly reverified: version `15.32.75d4a0`, size `52105824`, unpacked SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`, packed `bin/client` SHA-256 `075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f`.
- Observer remains GDB as parent, never attach; producer offset remains `0xe25620`; capture source is only `uint32(edx)`.
- V1/V2/V3 triggers are consumed and may never be replayed; V4 requires exact body `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true` only after a separately merged docs-only V4 admission.
- Live V4 admission is `ephemeral_isolated`, `physical_action_budget: 1`, `physical_action_count: 0`, `relogin_allowed: false`, `restart_allowed: false`, `character_selection_allowed: false`, `gameplay_allowed: false`, `network_payload_capture_allowed: false`.
- No credentials, session material, packet payloads, process environment, unrelated registers, stack bytes, or raw memory may be retained or uploaded.
- Full official package verification, task-owned WARP/SOCKS routing, non-execution during preflight, atomic publication, and cancellation-safe cleanup remain mandatory.
- Do not increase the live job timeout unless a new measured failure proves the bounded parallel materializer still cannot meet the existing 18-minute deadline.

---

### Task 1: Freeze V4 trigger generation with RED → GREEN

**Files:**
- Modify: `.github/scripts/test_track_a_current_login_field6_runtime.py`
- Modify: `.github/workflows/track-a-current-login-field6-runtime.yml`
- Modify: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`

**Interfaces:**
- Consumes: existing V3 exact-body gate and static-safe `runtime_access: none` task state.
- Produces: trusted-main workflow that accepts only `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true` and still requires a separately live-authorized task record.

- [ ] **Step 1: Write the failing V4 contract**

Change the workflow needle in `.github/scripts/test_track_a_current_login_field6_runtime.py` from:

```python
"AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 once=true",
```

to:

```python
"AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true",
```

and add an explicit consumed-generation rejection after `workflow = need(...)`:

```python
if "AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V3 once=true" in workflow:
    raise SystemExit("FIELD6_RUNTIME_CONTRACT_RED: consumed V3 trigger must not remain executable")
```

Do not modify the workflow in this RED commit.

- [ ] **Step 2: Run hosted RED and verify causal failure**

Use the existing pull-request workflow `Track A current login field6 runtime observation` on the exact RED head.

Expected first relevant failure:

```text
FIELD6_RUNTIME_CONTRACT_RED: .github/workflows/track-a-current-login-field6-runtime.yml missing ['AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true']
```

The live observation job must remain skipped on the PR event; Track A governance and unrelated CI may remain green.

- [ ] **Step 3: Implement the minimal V4 generation**

In `.github/workflows/track-a-current-login-field6-runtime.yml`, replace both executable V3 literals with V4:

```yaml
github.event.comment.body == 'AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true'
```

and:

```bash
grep -Fq 'AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true' "$task"
```

Do not alter secrets, materialization order/gates, artifact schema, producer offset, runtime helper, upload retention, runner selection, or `timeout-minutes: 18`.

- [ ] **Step 4: Run focused/component GREEN**

Require exact-head success for:

```text
Track A current login field6 runtime observation / Current login field6 runtime contract
Track A current client package materializer contract
Track A agent runtime governance
CI / Required
```

Inspect the changed filenames and prove no Track B or unrelated Track A runtime files entered the diff.

- [ ] **Step 5: Independent exact-head review and merge**

Request fresh Codex/validator review on the final exact head, resolve every material finding, clean-restack onto fresh `main`, rerun affected exact-head checks, and squash merge. No V4 owner trigger may exist before this merge.

---

### Task 2: Create a separate docs-only V4 live admission

**Files:**
- Modify: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`

**Interfaces:**
- Consumes: merged V4 workflow generation and fresh live ownership preflight.
- Produces: exactly one `ephemeral_isolated` account-login scalar observation budget with no reusable trigger authority.

- [ ] **Step 1: Reconstruct fresh runtime ownership from `main`**

Confirm all separate Track A recovery/mutation tasks are either `runtime_access: none` or non-conflicting and that no pending field6 trigger exists. Re-read the exact current fence constants from trusted `main`; do not infer them from this plan.

- [ ] **Step 2: Persist the docs-only admission**

Change the field6 task to the established isolated admission shape:

```yaml
status: validating
phase: live_admission
execution_class: self_hosted
execution_mode: github_actions_ephemeral_isolated
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260828-current-login-field6-runtime
runtime_namespace: field6-runtime-ephemeral-OTC-20260828-v4
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: PROVEN
mutation_authorized: true
credentials_allowed: true
login_allowed: true
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: true
process_control_authorized: true
network_payload_capture_allowed: false
physical_action_budget: 1
physical_action_count: 0
```

Record the current owner instruction as the authority basis and state that execution still requires a new distinct exact V4 trigger after merge. The admission PR itself must contain documentation only and cannot execute a live login.

- [ ] **Step 3: Validate, review, clean-restack, and merge**

Require Track A governance, field6 static contract, CI, exact changed filenames, independent review, zero unresolved threads, and fresh-main restack. Merge only after all gates pass.

---

### Task 3: Execute exactly one V4 observation and classify the terminal result

**Files:**
- No repository mutation before the live run.
- Later evidence update: `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/**`
- Later task update: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`

**Interfaces:**
- Consumes: merged V4 generation + merged docs-only V4 admission + distinct repository-owner trigger.
- Produces: one terminal sanitized scalar artifact or a fail-closed pre-action/runtime blocker with exact physical action count.

- [ ] **Step 1: Post exactly one new V4 trigger**

After revalidating fresh `main` and admission, create one repository-owner comment on merged PR #758 with exact body:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true
```

Never rerun V1/V2/V3 or replay this V4 comment.

- [ ] **Step 2: Inspect the resulting workflow once to terminal state**

The required ordered gates remain:

```text
trusted-main admission
→ full exact-current package materialization through task-owned WARP
→ one-shot authorization consumption
→ protected credential wrapper
→ GDB-parent producer breakpoint
→ scalar-only validation
→ sanitized artifact upload
→ package cleanup
```

If package or exact client fence changes, classify fail-closed and do not submit login. If a later gate fails after the one physical submit, preserve `physical_action_count=1` and do not relog/restart.

- [ ] **Step 3: Accept scalar evidence only on the strict terminal schema**

Success requires the sanitized output to prove:

```text
TRACK_A_FIELD6_RUNTIME_CAPTURED=true
FIELD6_VALUE=<uint32>
FIELD6_VALUE_PROVEN=true
login_submit_count=1
character_selection_performed=false
world_entry_performed=false
gameplay_performed=false
network_payload_capture_performed=false
credentials_retained=false
packet_payloads_retained=false
process_environment_retained=false
raw_memory_retained=false
```

Any missing or contradictory field is not success.

---

### Task 4: Promote terminal V4 evidence before any Track B consumption

**Files:**
- Create/modify: `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/<v4-terminal-evidence>.md`
- Modify: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`

**Interfaces:**
- Consumes: exact V4 terminal run/job/artifact evidence.
- Produces: trusted-main scalar evidence that Track B may consume, or a durable blocker that forbids guessing/retry.

- [ ] **Step 1: Write only sanitized evidence**

Persist run/job IDs, exact tested main, exact client fence, producer offset, proven scalar, action counts, and all negative-retention/safety booleans. Never copy credentials, session material, packet payloads, stack bytes, raw registers other than the scalar source, process environment, or proprietary client/package bytes.

- [ ] **Step 2: Disarm V4 authority**

Return the task to `runtime_access: none`, `mutation_authorized: false`, credentials/login false, `physical_action_budget: 0`, and preserve the terminal `physical_action_count`. Mark the V4 trigger consumed and non-replayable.

- [ ] **Step 3: Exact-head review and promotion**

Use a repository-only evidence PR with exact-head governance/CI and independent review. Only after squash merge to fresh `main` may Track B read `FIELD6_VALUE`.

- [ ] **Step 4: Reassess before Track B**

If `FIELD6_VALUE_PROVEN=true`, close the field6 producer phase and create a separate Track B implementation plan from then-current PR #284 intended diff. If V4 failed before scalar proof, derive the next materially different hypothesis from the terminal evidence; never retry an identical login or guess field6.
