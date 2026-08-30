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

- [x] **Step 1: Write the failing contract**

The contract requires `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true` and rejects consumed V3/V4 literals in both workflow and active task.

- [x] **Step 2: Run the contract through PR CI and verify causal RED**

Verified RED:

```text
head=8c262e0d509af1927380cf36b9179ee9950c507d
run=33305488409
contract_job=99241188716
fresh_audit_job=99241188630
live_job=99241189199
live_job_conclusion=skipped
FIELD6_RUNTIME_CONTRACT_RED: .github/workflows/track-a-current-login-field6-runtime.yml missing ['AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true']
```

No self-hosted runner, secrets, official client, login, or physical action executed.

- [x] **Step 3: Commit RED separately**

RED commit: `8c262e0d509af1927380cf36b9179ee9950c507d` (`test(track-a): require V5 field6 generation`). Draft PR #812 preserved the causal RED before GREEN.

---

### Task 2: Rotate only the static generation to V5

**Files:**
- Modify: `.github/workflows/track-a-current-login-field6-runtime.yml`
- Modify: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`
- Modify: `docs/superpowers/plans/2026-08-30-field6-v5-generation.md`

**Interfaces:**
- Consumes: Task 1 V5 contract.
- Produces: trusted static V5 generation with no live authority and historical V4 revocation through current-main task/workflow text.

- [x] **Step 1: Change only the two executable generation literals in the workflow**

The issue-comment condition and trusted-main task grep now require V5. Runner labels, runner name, guest name, provenance schema, secret ordering, helper, acquisition path, scalar observer, artifact schema, and cleanup remain unchanged and inert in this static phase.

- [x] **Step 2: Recast the active task as static V5 generation**

The active task is `runtime_access: none`, `mutation_authorized: false`, `credentials_allowed: false`, `login_allowed: false`, `physical_action_budget: 0`, and `physical_action_count: 0`. It contains V5 current-generation text and deliberately omits exact consumed V4 text.

- [x] **Step 3: Mark this plan's RED/GREEN evidence with exact run/job IDs**

GREEN implementation head before final plan checkpoint:

```text
head=7da456ce23377b69ad536a71452e905bddb901ac
field6_run=33305748938
runtime_contract_job=99241902604 SUCCESS
fresh_static_audit_job=99241902561 SUCCESS
physical_live_job=99241902984 SKIPPED
package_run=33305748946
package_job=99241902518 SUCCESS
governance_run=33305748935
self_hosted_boundary_run=33305748930
ci_run=33305749033
ci_required_job=99241973216 SUCCESS
yamllint=SUCCESS
actionlint=SUCCESS
```

The first GREEN candidate `54e3f5c6d4b9da06ac2911163fa816fe991cac04` had correct runtime/package/governance/boundary behavior but CI found exactly one formatting defect: missing final newline in `track-a-current-login-field6-runtime.yml`. Commit `7da456ce23377b69ad536a71452e905bddb901ac` fixed only that EOF defect; exact-head CI then passed.

- [x] **Step 4: Commit GREEN**

GREEN implementation is present on PR #812; the final plan checkpoint commit itself must receive fresh exact-head CI before merge.

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

- [x] **Step 1: Require hosted field6 runtime contract GREEN**

Verified on `7da456ce...`: runtime contract SUCCESS, fresh static audit SUCCESS, physical live job SKIPPED.

- [x] **Step 2: Require package materializer contract GREEN**

Verified on `7da456ce...`: package materializer contract SUCCESS; serial production/default acquisition and 45-minute live ceiling remain covered.

- [x] **Step 3: Require governance/self-hosted-boundary/CI GREEN**

Verified on `7da456ce...`: Track A governance SUCCESS, self-hosted PR boundary SUCCESS, yamllint SUCCESS, actionlint SUCCESS, and `CI / Required` SUCCESS.

- [ ] **Step 4: Fresh diff/review/main readback**

Must be repeated on the exact plan-checkpoint head created by this file update. Confirm only intended generation/test/task/plan files changed, unresolved review threads/reviews are zero, and protected `main` has no material overlapping drift.

- [ ] **Step 5: Merge with expected-head guard**

Squash-merge only the exact verified final head and read back the resulting `main` SHA. Verify trusted `main` contains V5 current-generation text and omits exact V4 current-generation text from the active workflow/task.

---

### Task 4: Stop at the external V5 routing/admission gate

**Files:**
- No code write until fresh physical successor prerequisites are directly proven.

**Interfaces:**
- Consumes: merged static V5 generation.
- Produces: an explicit, non-ambiguous next boundary for the same field6 task.

- [ ] **Step 1: Check the authorized `Molehill-PC` control channel**

At the latest readback Molehill-PC is online. This must be reconfirmed after static V5 merge before physical preparation.

- [ ] **Step 2: Destroy only the tainted exact `OTClientV4Clean` target after proving ownership, then create a brand-new successor guest from the pinned Canonical rootfs and re-prove automount/interop/socket/prior-state isolation**

Do not reuse the diagnostic V4 guest.

- [ ] **Step 3: Only after fresh guest provenance exists, create a separate V5 independent-routing/admission change**

That later change must rotate the independent one-time label, guest/runner identifiers, helper/acquisition allowlists, security/admission audit expectations, and grant at most one login scalar observation. It must be TDD-reviewed separately and merged to trusted `main` before any V5 trigger is posted.

- [ ] **Step 4: Never post a V5 trigger until the new trusted-main routing/admission and exact queued-job uniqueness are both proven**

If a later V5 physical login submit occurs without scalar proof, identical replay remains forbidden.
