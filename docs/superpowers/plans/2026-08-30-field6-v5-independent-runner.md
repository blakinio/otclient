# Field6 V5 Independent Runner Admission Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Route the already-static V5 field6 generation to a brand-new independent `OTClientV5Clean` / `molehill-otclient-v5-01` one-job runner and grant exactly one bounded login scalar observation after trusted-main merge.

**Architecture:** Keep generation V5 unchanged, but rotate every physical identity fence from V4 to V5 and restore live task admission only after direct host proof. The PR itself remains unable to execute the physical job because the workflow trigger is an exact issue-comment event; hosted contracts must RED first on missing V5 physical boundaries, then GREEN after workflow/helper/acquisition/audit/task changes. The actual trigger is posted only after this PR is merged, a root-owned provenance record is bound to the trigger-derived label, and exactly one attempt-1 queued job is proven.

**Tech Stack:** GitHub Actions, Python security/audit contracts, Bash runtime helpers, WSL2 Ubuntu 24.04, GitHub Actions runner 2.337.0.

**Spec:** `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`

## Global Constraints

- Trusted base is `main@82bd4ef6d11431a40e47d8eea6fa15f372edcdc4`.
- Exact current client fence remains `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.
- Current generation trigger remains exactly `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true`; do not post it in this PR.
- Owner admission is PR #758 comment `5468621219`: `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5_ADMISSION once=true physical_action_budget=1 no_relogin=true`.
- Fresh host guest is `OTClientV5Clean`; runner is `molehill-otclient-v5-01`; scheduling label is `field6-v5-<comment_id>`.
- Canonical rootfs URL/SHA remain `https://cloud-images.ubuntu.com/releases/noble/release-20260801/ubuntu-24.04-server-cloudimg-amd64-root.tar.xz` / `915b4be62933475c3fb5f5031aa2e159294db95fb32aaa9e8b317aadcb6c065d`.
- Actions runner remains `2.337.0`, SHA256 `70920811a4f8ad4328818682bca5c6469c1c942fab52448868071d0063816613`.
- Direct host proof already established for V5: automount/interop disabled; no `/mnt/c`; no Docker/Podman sockets; no previous repo/runner state; required toolroot installed; runner archive hash correct; runner not configured.
- Synology is forbidden for credential-bearing field6 work.
- One login submit maximum; no relogin/restart/character selection/world entry/gameplay/network payload capture.
- `GITHUB_RUN_ATTEMPT != 1` must fail before authorization/secret/client execution.
- No V4 runner/guest/label may remain as an accepted current physical boundary after merge.

---

### Task 1: TDD RED the V5 physical boundary

**Files:**
- Modify: `.github/scripts/test_track_a_current_login_field6_security_contract.py`
- Modify: `.github/scripts/audit_track_a_current_login_field6_admission.py`

- [ ] Require `molehill-otclient-v5-01`, `OTClientV5Clean`, `field6-v5-{0}`, V5 admission comment `5468621219`, and a V5 independent-runtime contract marker.
- [ ] Reject current V4 physical runner/guest/label strings in executable workflow/helper/acquisition/task admission.
- [ ] Open Draft PR before production rotation and verify hosted field6/security/audit failure is causal while physical live job is SKIPPED.
- [ ] Record exact RED head/run/job IDs.

### Task 2: Implement minimal V5 routing/admission

**Files:**
- Create: `docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V2.md`
- Modify: `.github/scripts/audit_track_a_current_login_field6_admission.py`
- Modify: `.github/scripts/test_track_a_current_login_field6_security_contract.py`
- Modify: `.github/scripts/track_a_current_client_package_acquire.sh`
- Modify: `.github/scripts/track_a_current_login_field6_runtime.sh`
- Modify: `.github/workflows/track-a-current-login-field6-runtime.yml`
- Modify: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`

- [ ] V2 contract binds one-job label `field6-v5-<comment_id>`, exact guest/runner names, no-default-labels, no host sockets/mounts, root-owned provenance, and post-job destruction.
- [ ] Workflow env and live job use exact V5 guest/runner/label; exact V5 trigger remains unchanged; trusted-main task grep requires the V5 admission state.
- [ ] Package acquisition accepts V5 independent runner only when provenance is verified; V4 runner is removed from current acceptance.
- [ ] Runtime helper uses V5 independent runner and system toolroot only with provenance flags; V4 runner is removed from current acceptance.
- [ ] Active task changes to `independent_ephemeral_physical_runtime`, `runtime_access: ephemeral_isolated`, `target_uniqueness: PROVEN`, one-action budget, no relog/restart/character/world/gameplay/payload capture, and exact admission source `PR_758_COMMENT_5468621219`.
- [ ] Full independent admission audit allowlist covers exactly changed V5 routing/admission paths.

### Task 3: Exact-head static verification and merge

- [ ] Field6 runtime/security/full independent audit GREEN; physical live job SKIPPED.
- [ ] Package materializer, Track A governance, self-hosted PR boundary, yamllint/actionlint, and `CI / Required` GREEN.
- [ ] Diff limited to planned paths; zero unresolved review threads/reviews; no material main drift.
- [ ] Mark ready and squash-merge with expected-head guard.
- [ ] Trusted-main readback proves V5 runner/guest/label/admission and no current V4 physical acceptance.

### Task 4: One-shot physical V5 execution

- [ ] While no V5 runner is registered/online, post exactly one trigger comment `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true` on PR #758.
- [ ] Prove exactly one attempt-1 queued job exists and requires only `field6-v5-<comment_id>`; no other queued job requires that label.
- [ ] Create root-owned `/etc/otclient-field6-runner-provenance` in `OTClientV5Clean`, exact schema v1, binding guest/rootfs SHA/runner/one-time label plus fresh generation nonce and all isolation booleans true; mode 0644 or stricter, root:root, not runner-writable.
- [ ] Obtain a short-lived GitHub runner registration token without logging it; configure runner as `--ephemeral --disableupdate --no-default-labels --labels field6-v5-<comment_id>` and exact name `molehill-otclient-v5-01`.
- [ ] Start the one-job runner, observe terminal workflow result, then destroy/unregister `OTClientV5Clean` after evidence retrieval regardless of result.
- [ ] If one login submit occurs without scalar proof, do not replay V5; persist terminal result and require a new justified generation.

### Task 5: Promote proven scalar and unblock Track B

- [ ] If sanitized artifact proves `FIELD6_VALUE=<uint32>`, independently validate schema/client fence/login_submit_count=1/no-world/no-payload/no-retained-secret fields.
- [ ] Create a repository-only promotion PR containing only the sanitized scalar/evidence and update Track B owner contract; no credentials/raw memory/proprietary binary.
- [ ] TDD/CI/review/merge promotion to trusted main.
- [ ] Only after promotion, continue the blocked global-login/Track B implementation and exact official-service game E2E under its own existing safety/admission contract until terminal closeout.
