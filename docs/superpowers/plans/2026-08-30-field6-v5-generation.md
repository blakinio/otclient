# Field6 V5 Static Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rotate the exact-current field6 observer from consumed terminal V4 to a distinct V5 generation on trusted `main` without creating any live runtime, credential, login, runner-registration, or physical-action authority.

**Architecture:** Mirror the proven static V3→V4 generation pattern from merged PR #783. First make the hosted runtime contract require V5 and reject consumed V4 while production still contains V4, producing a causal RED with the live job skipped. Then change only the executable trigger generation plus the active static-safe task/checkpoint so current `main` can no longer satisfy a historical V4 generation check. Independent V5 runner/guest routing and one-login admission are deliberately separate later phases after a brand-new guest is physically proven.

**Tech Stack:** GitHub Actions YAML, Python contract tests, Markdown task/plan governance, GitHub-hosted CI.

**Spec:** `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`

## Global Constraints

- Exact client fence remains `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.
- `FIELD6_VALUE` remains `UNKNOWN`; no guessed scalar may be promoted.
- Terminal V4 run `33300352335` / job `99227195253` remains pre-action: `physical_action_count=0`, no authorization consumption, no credential injection, no client execution, no login submit.
- Consumed V4 owner trigger must never be replayed or remain the current executable generation.
- This PR must remain `runtime_access: none`, `mutation_authorized: false`, `credentials_allowed: false`, `login_allowed: false`, `physical_action_budget: 0`, `physical_action_count: 0`.
- The PR event must skip the physical `live-observation` job.
- Do not rotate to or register a V5 independent runner/guest in this PR. The current V4 runner/guest routing remains inert behind static task admission and is a separate successor-routing phase.
- Do not post any V5 owner trigger/comment in this PR.
- Do not touch Track B #284 or run official-service game E2E.
- Package repair merged by #811 is immutable input: production/default file workers stay `1`; live timeout stays `45`; exact packed/unpacked checks stay intact.

---

### Task 1: Add the V5 generation RED contract

**Files:**
- Modify: `.github/scripts/test_track_a_current_login_field6_runtime.py`
- Test: `.github/scripts/test_track_a_current_login_field6_runtime.py`

**Interfaces:**
- Consumes: current trusted V4 workflow/task on `main@dad71238d3da48ad9cf0bdcb45f9d0a445131f8c`.
- Produces: a hosted contract that requires exact V5 generation text and rejects exact consumed V4 text in both executable workflow and active task.

- [ ] **Step 1: Write the failing contract**

Change the required current trigger from `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true` to `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true`. Replace the single V3 historical guard with a loop rejecting both consumed V3 and V4 exact trigger literals in `workflow` and `task`.

- [ ] **Step 2: Run the contract through PR CI and verify causal RED**

Expected first relevant failure while production remains V4:

```text
FIELD6_RUNTIME_CONTRACT_RED: .github/workflows/track-a-current-login-field6-runtime.yml missing ['AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true']
```

The `One-shot isolated field6 observation` job must be `skipped`; no self-hosted runner, secrets, client, or login may execute.

- [ ] **Step 3: Commit RED separately**

Commit message:

```text
test(track-a): require V5 field6 generation
```

Open an early Draft PR from `fix/OTC-20260830-field6-v5-generation` so the RED run/job is durable evidence before GREEN.

---

### Task 2: Rotate only the static generation to V5

**Files:**
- Modify: `.github/workflows/track-a-current-login-field6-runtime.yml`
- Modify: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`
- Modify: `docs/superpowers/plans/2026-08-30-field6-v5-generation.md`

**Interfaces:**
- Consumes: Task 1 V5 contract.
- Produces: trusted static V5 generation with no live authority and historical V4 revocation through current-main task/workflow text.

- [ ] **Step 1: Change only the two executable generation literals in the workflow**

Replace:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true
```

with:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true
```

in the issue-comment condition and the trusted-main task grep. Do not change runner labels, runner name, guest name, provenance schema, secret ordering, helper, acquisition path, scalar observer, artifact schema, or cleanup in this generation-only PR.

- [ ] **Step 2: Recast the active task as static V5 generation**

Set/retain exactly:

```yaml
execution_class: github_hosted
execution_mode: github_actions_static
physical_e2e_required: false
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 0
physical_action_count: 0
```

The active task must contain exact current V5 trigger text as the future generation identifier but must not contain the exact consumed V4 trigger literal anywhere. Preserve V4 terminal facts without reproducing that exact consumed body. Record #811 merge SHA `dad71238d3da48ad9cf0bdcb45f9d0a445131f8c`, current host-offline state, tainted `OTClientV4Clean`, and the requirement for a brand-new successor guest before any live admission.

- [ ] **Step 3: Mark this plan's RED/GREEN evidence with exact run/job IDs**

After hosted results exist, update this plan with the exact RED and GREEN head/run/job identifiers; do not write future IDs speculatively.

- [ ] **Step 4: Commit GREEN**

Commit message:

```text
fix(track-a): rotate field6 observer to V5 generation
```

---

### Task 3: Verify exact-head static safety

**Files:**
- Test: `.github/scripts/test_track_a_current_login_field6_runtime.py`
- Test: `.github/scripts/test_track_a_current_login_field6_security_contract.py`
- Test: `.github/scripts/test_track_a_current_client_package_parallel.py`
- Test: `.github/scripts/test_track_a_agent_runtime_governance.py`
- Test: `.github/workflows/track-a-current-login-field6-runtime.yml`

**Interfaces:**
- Consumes: Task 2 candidate head.
- Produces: reviewable exact-head evidence for safe merge.

- [ ] **Step 1: Require hosted field6 runtime contract GREEN**

The contract and fresh static audit jobs must be `success`; physical live job must be `skipped`.

- [ ] **Step 2: Require package materializer contract GREEN**

Confirm serial production/default acquisition and 45-minute live ceiling remain covered.

- [ ] **Step 3: Require governance/self-hosted-boundary/CI GREEN**

Require Track A governance, self-hosted PR boundary, actionlint/yamllint and `CI / Required` to complete successfully for the exact final head.

- [ ] **Step 4: Fresh diff/review/main readback**

Confirm only intended generation/test/task/plan files changed, unresolved review threads/reviews are zero, and protected `main` has no material overlapping drift.

- [ ] **Step 5: Merge with expected-head guard**

Squash-merge only the exact verified head and read back the resulting `main` SHA. Verify trusted `main` contains V5 current-generation text and omits exact V4 current-generation text from the active workflow/task.

---

### Task 4: Stop at the external V5 routing/admission gate

**Files:**
- No code write unless the physical host returns and fresh prerequisites can be directly proven.

**Interfaces:**
- Consumes: merged static V5 generation.
- Produces: an explicit, non-ambiguous next boundary for the same field6 task.

- [ ] **Step 1: Check the authorized `Molehill-PC` control channel**

If it remains offline, do not create live authority and do not fall back to Synology.

- [ ] **Step 2: If the host returns, destroy only the tainted exact `OTClientV4Clean` target after proving ownership, then create a brand-new successor guest from the pinned Canonical rootfs and re-prove automount/interop/socket/prior-state isolation**

Do not reuse the diagnostic V4 guest.

- [ ] **Step 3: Only after fresh guest provenance exists, create a separate V5 independent-routing/admission change**

That later change must rotate the independent one-time label, guest/runner identifiers, helper/acquisition allowlists, security/admission audit expectations, and grant at most one login scalar observation. It must be TDD-reviewed separately and merged to trusted `main` before any V5 trigger is posted.

- [ ] **Step 4: Never post a V5 trigger until the new trusted-main routing/admission and exact queued-job uniqueness are both proven**

If a later V5 physical login submit occurs without scalar proof, identical replay remains forbidden.
