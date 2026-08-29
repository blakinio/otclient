# Track A Independent Clean Physical Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Safely execute the already-admitted one-shot V4 field6 observation on a fresh physical Linux guest outside the Synology trust boundary without weakening canonical Track A routing.

**Architecture:** First merge a governance-only execution-class/contract PR with `runtime_access:none`; unmerged governance never self-authorizes its consumer. Then restack the V4 consumer on that trusted base, route its one live job to a comment-ID-derived one-time label, and add exact independent-runner provenance plus V4-only system-toolroot gates. Finally provision a fresh WSL2 Ubuntu guest on `Molehill-PC`, queue the exact owner-triggered job while no matching runner exists, register one `--ephemeral --no-default-labels` runner for that label, collect scalar-only evidence, and destroy the guest.

**Tech Stack:** GitHub Actions, Python 3 deterministic validators, Bash V4 helper, GitHub self-hosted Actions runner, WSL2, Ubuntu 24.04 Noble, PowerShell control plane.

**Spec:** `docs/superpowers/specs/2026-08-29-track-a-independent-clean-physical-runtime-design.md`

## Global Constraints

- `blakinio/otclient` is the only writable repository; protected `main` is the source of truth.
- Synology is forbidden for V4 credentials because run `33261106292` / job `99123092884` proved historical runner host Docker-socket RW.
- Canonical bootstrap/reuse/rebind/recovery and retained Kasm state remain `synology_physical_runtime` only.
- New fallback class is exactly `independent_ephemeral_physical_runtime` and initially has one consumer: V4 field6.
- V4 retains `physical_e2e_required: true`, `runtime_access: ephemeral_isolated`, one login submit maximum, and no relogin/restart/character/world/gameplay/network-payload capture.
- GDB remains the parent process and retained live evidence is only sanitized `uint32(edx)` at `PIE+0xe25620`.
- No runner-registration token, Tibia credential, session token, raw packet, process environment, raw memory, or proprietary official-client binary is committed or persisted as evidence.
- Do not post `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true` until both repository PRs are merged and host provenance/queued-job uniqueness are proven.

---

### Task 1: Merge the independent execution-class governance boundary

**Files:**
- Create: `docs/agents/contracts/TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V1.md`
- Create: `.github/scripts/test_track_a_independent_ephemeral_physical_runtime_contract.py`
- Create: `.github/workflows/track-a-independent-ephemeral-physical-runtime-contract.yml`
- Create: `docs/agents/tasks/active/OTC-20260829-field6-independent-clean-runner.md`
- Modify: `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`
- Already created: design spec and this plan.

**Interfaces:**
- Consumes: merged `TRACK_A_SELF_HOSTED_SECRET_RUNNER_V1.md` and terminal Synology-disqualification evidence.
- Produces: trusted definition of `independent_ephemeral_physical_runtime`; no runtime permission by itself.

- [ ] **Step 1: Write the governance RED validator**

The validator must require the routing document to name the new class and a dedicated contract to exist. It must also reject any contract text that permits canonical access classes or omits `physical_e2e_required: true`, `runtime_access: ephemeral_isolated`, independent-host provenance, one-job ephemeral lifecycle, and no-host-socket requirements.

- [ ] **Step 2: Run RED against current `main`**

Run:
```bash
python3 .github/scripts/test_track_a_independent_ephemeral_physical_runtime_contract.py
```
Expected first failure: routing/contract lacks `independent_ephemeral_physical_runtime`; no runtime operation is performed.

- [ ] **Step 3: Add the minimal normative routing change**

Add the third class to the routing enum and a dedicated section that says:
```text
independent_ephemeral_physical_runtime = security fallback for task-owned ephemeral physical Linux work only
canonical_* runtime_access => synology_physical_runtime only
```
The fallback must require durable Synology disqualification plus its own merged task-specific contract.

- [ ] **Step 4: Add the independent-runtime contract**

Freeze exact requirements: physically separate host, hash-verified fresh Linux guest, no prior repo state, no host mounts/interop/Docker socket, `--ephemeral --disableupdate --no-default-labels`, comment-ID-derived one-time label, queue-before-online, exact queued-job uniqueness, root-owned provenance, and guest destruction after the job.

- [ ] **Step 5: Add hosted contract workflow and task record**

The PR workflow runs only on GitHub-hosted Ubuntu and executes the validator + Track A governance + `git diff --check`. Task metadata remains `runtime_access:none`, `mutation_authorized:false`, credentials/login false, physical action budget/count `0/0`.

- [ ] **Step 6: Run GREEN and exact-head CI**

Run locally where available, then require GitHub-hosted contract workflow, Track A governance, reusable self-hosted boundary, and `CI / Required` all GREEN. Physical jobs must be absent/skipped.

- [ ] **Step 7: Clean-restack, review full diff, squash-merge**

Restack to exactly one logical commit on fresh `main`; confirm no PR #801 paths overlap; merge only with zero material review findings/threads.

---

### Task 2: Re-route V4 to the independent one-time runner

**Files:**
- Modify: `.github/workflows/track-a-current-login-field6-runtime.yml`
- Modify: `.github/scripts/test_track_a_current_login_field6_security_contract.py`
- Modify: `.github/scripts/audit_track_a_current_login_field6_admission.py`
- Modify: `.github/scripts/track_a_current_login_field6_runtime.sh`
- Modify: `.github/scripts/test_track_a_current_login_field6_runtime.py`
- Modify: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`
- Create: sanitized field6 independent-runner admission report if needed.

**Interfaces:**
- Consumes: Task 1 merged execution class + contract.
- Produces: trusted-main V4 workflow that can only schedule the independent one-time label and can use system toolroot only after exact provenance.

- [ ] **Step 1: Write consumer RED tests before changing workflow/helper**

Tests must require:
```text
execution_class: independent_ephemeral_physical_runtime
persistent_session_role: none
RUNNER_NAME == molehill-otclient-v4-01
runs-on label == field6-v4-${{ github.event.comment.id }}
TRACK_A_FIELD6_SYSTEM_TOOLROOT=1 only after provenance validation
```
They must reject `[otclient, synology]`, generic `self-hosted/Linux/X64` labels, static shared labels, and system-toolroot use on any other runner.

- [ ] **Step 2: Run RED**

Expected failure must point to the old Synology selector/execution class; live PR job stays skipped.

- [ ] **Step 3: Change task routing and workflow selector**

Restack task metadata on fresh post-Task-1 `main`, keep physical budget/count `1/0`, and route live job to the single dynamic label `field6-v4-${{ github.event.comment.id }}`. Preserve exact V4 owner trigger, PR #758 target, `GITHUB_RUN_ATTEMPT == 1`, package-before-auth ordering, and secret-only capture step.

- [ ] **Step 4: Add provenance validation before secrets**

Validate `/etc/otclient-field6-runner-provenance` as root-owned, not runner-writable, schema-valid, exact guest/name/rootfs/one-time-label bound, with no-automount/no-interop/no-Docker-socket assertions. Fail before package execution, authorization consumption, or secret exposure on any mismatch.

- [ ] **Step 5: Add V4-only system-toolroot mode**

`resolve_toolroot()` may return `/` only when `TRACK_A_FIELD6_SYSTEM_TOOLROOT=1`, `RUNNER_NAME=molehill-otclient-v4-01`, and the independent provenance gate has already passed. Reuse existing `toolroot_ok` requirements so missing Xvfb/xdotool/gdb/XKB/swrast/proxychains fails closed. Existing Synology lookup remains unchanged.

- [ ] **Step 6: GREEN validation and independent audit**

Require field6 runtime contract, security contract, fresh independent V4 admission audit, materializer contract, Track A governance, reusable self-hosted boundary, and `CI / Required` GREEN on exact head; physical PR job skipped.

- [ ] **Step 7: Clean-restack and squash-merge**

Exactly one logical consumer commit on current `main`, no Kasm/Track B paths, zero unresolved material findings.

---

### Task 3: Provision and attest `OTClientV4Clean` without credentials

**Files outside Git:**
- Canonical rootfs cache under `%TEMP%/otclient-v4-clean/`
- New WSL distribution storage only for `OTClientV4Clean`
- Guest provenance: `/etc/otclient-field6-runner-provenance`
- Actions runner install directory owned by Linux `runner` user.

**Interfaces:**
- Consumes: Task 2 merged trusted-main workflow.
- Produces: offline clean guest ready to register for one exact label; no GitHub runner registered yet.

- [ ] **Step 1: Verify Canonical rootfs before import**

Fetch matching Canonical `SHA256SUMS` and `noble-server-cloudimg-amd64-root.tar.xz`; compute SHA256 locally and require exact equality before `wsl --import`.

- [ ] **Step 2: Import unique WSL2 guest**

Require `OTClientV4Clean` absent, create a new storage directory, and run `wsl --import OTClientV4Clean <storage> <rootfs> --version 2`. Do not modify existing `Ubuntu`, `Ubuntu-24.04`, or `docker-desktop` distributions.

- [ ] **Step 3: Disable host integration and restart guest**

Write `/etc/wsl.conf` with automount disabled and interop disabled/Windows PATH disabled, terminate only `OTClientV4Clean`, restart it, and prove `/mnt/c` absent plus Windows executable invocation unavailable.

- [ ] **Step 4: Install exact runtime prerequisites and unprivileged runner user**

Install package set needed by current V4 helper (`gdb`, `xvfb`, `xdotool`, `proxychains4`, Mesa/X11/GTK libraries, Python, curl/git/procps/iproute2/lsof/netcat/socat). Prove system `toolroot_ok` inputs exist. Create `runner` user; no sudo is required by the job.

- [ ] **Step 5: Prove clean guest before any registration**

Require no `/var/run/docker.sock`, no Podman socket, no repository checkout, no `_work`, no runner `.credentials/.runner`, no retained task state, no host mounts, and no secret-named environment variables/files.

- [ ] **Step 6: Prepare public Actions runner software without configuring it**

Download the current GitHub Actions runner release and verify its published checksum. Do not request a registration token yet; do not start `run.sh`.

- [ ] **Step 7: Write root-owned provenance marker**

Record only sanitized facts: schema, rootfs URL/SHA256, WSL guest, WSL version, runner name, clean generation nonce, automount/interop disabled, Docker socket absent. The one-time label is added only after the V4 comment ID exists. Owner `root:root`; mode read-only to runner.

---

### Task 4: Queue and execute exactly one V4 job

**Files:** no repository changes before trigger; runtime evidence becomes a later repository-only promotion PR.

**Interfaces:**
- Consumes: merged Task 2 workflow + clean offline Task 3 guest + owner admission comment `5457904227`.
- Produces: exactly one terminal V4 run and, only on success, one sanitized scalar artifact.

- [ ] **Step 1: Fresh-check main and runtime ownership**

Confirm no conflicting active mutation task, field6 physical action count still `0`, V1/V2/V3 triggers revoked, `FIELD6_VALUE=UNKNOWN`, and no runner with the future one-time label exists.

- [ ] **Step 2: Post exactly one V4 trigger**

Add one new top-level owner comment on merged PR #758 whose body is exactly:
```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true
```
Record the returned numeric comment ID. Do not post a second comment.

- [ ] **Step 3: Prove exact queued-job uniqueness before runner registration**

Find the resulting attempt-1 workflow run/job and require it queued for exactly `field6-v4-<comment_id>`. Enumerate queued self-hosted jobs and fail closed if any other job requests that label.

- [ ] **Step 4: Bind provenance to the exact label**

As guest root, append only the exact `field6-v4-<comment_id>` value to the provenance record, fsync it, and restore non-runner-writable mode. Re-run all clean-guest assertions.

- [ ] **Step 5: Register the runner without exposing registration credential**

Obtain a short-lived repository registration token through the Windows control plane and pipe it into the guest process; never print it or place it in argv/log/files. Configure exact name with `--ephemeral --disableupdate --no-default-labels --labels field6-v4-<comment_id>`.

- [ ] **Step 6: Start runner and verify it accepts only the exact job**

Start `run.sh`, observe GitHub job assignment metadata, and abort/destroy guest if assigned run/job differs from the exact queued V4 identifiers. The runner receives only one job by ephemeral registration.

- [ ] **Step 7: Consume V4 result once**

Inspect only redacted logs and the sanitized artifact. Success requires `login_submit_count=1`, `FIELD6_VALUE_PROVEN=true`, integer field6, and every forbidden action/retention boolean false. If the one login occurred but scalar is unproven, do not retry V4 identically.

- [ ] **Step 8: Destroy guest after terminal result**

Wait for runner deregistration/exit, terminate and `wsl --unregister OTClientV4Clean`, verify distro absent, and remove disposable runner/work directories. Retain only public rootfs hash cache if useful.

---

### Task 5: Promote sanitized Track A evidence

**Files:**
- Modify: `docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md`
- Create: `docs/agents/evidence/OTC-20260828-current-login-field6-runtime/<v4-terminal>.md`
- Create/update: compact report consumed by Track B.

- [ ] **Step 1: Create repository-only evidence PR from fresh main**

Set field6 task `runtime_access:none`, mutation/credentials/login false, physical action count to the actual terminal count, and archive the V4 trigger/run as consumed.

- [ ] **Step 2: Persist only sanitized scalar/provenance**

Record run/job/head, exact official-client fence, producer offset/source, scalar, login submit count, forbidden-action booleans, runner/rootfs sanitized provenance, and guest-destroyed proof. Never commit the raw artifact if it contains fields outside the reviewed scalar-only schema.

- [ ] **Step 3: Exact-head validation, clean-restack, squash-merge**

Track A governance + relevant evidence validators + CI GREEN, zero material findings/threads. After merge, Track B may consume the scalar from trusted `main`.