# Field6 V6 Independent Runner Admission Plan

**Goal:** Route static V6 to a brand-new `OTClientV6Clean` / `molehill-otclient-v6-01` one-job runner and eliminate V5 provenance/seed readability failures before one bounded login scalar observation.

**Trusted base:** `main@8442ead31bd448becc01082d34cbe2212f36a58d`.

## Proven physical prerequisite

- fresh WSL2 guest `OTClientV6Clean` imported from Canonical rootfs SHA256 `915b4be62933475c3fb5f5031aa2e159294db95fb32aaa9e8b317aadcb6c065d`;
- automount/interop disabled, no `/mnt/c`, no Docker/Podman sockets, no prior repo/runner state;
- toolroot installed; Actions runner `2.337.0` archive SHA256 `70920811a4f8ad4328818682bca5c6469c1c942fab52448868071d0063816613`; runner remains unconfigured;
- exact official-launcher seed SHA256 `64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016`, size `412272538`;
- seed parent directory `root:root 0555`, seed file `root:root 0444`; direct `sha256sum` as user `runner` PASS.

## Authority

PR #758 comment `5469210031` is V6 admission only. Exact executable trigger remains `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V6 once=true` and is unposted.

## Readability contract v3

V6 must use:

- provenance file `/etc/otclient-field6-runner-provenance`: `root:root 0644`;
- seed directory `/opt/otclient-v6-seed`: `root:root 0555`;
- seed file `/opt/otclient-v6-seed/seed.tar.gz`: `root:root 0444`;
- all three runner-readable and none runner-writable.

### Task 1 ? TDD RED

- [x] Security contract expects V6 runner/guest/label/admission/seed path and new independent-runtime contract v3.
- [x] Security contract rejects current V5 physical runner/guest/label and requires exact readability-mode markers.
- [x] Draft PR #816 hosted RED head `fbfa35ce78b347f3a9a64e0857d59fd9d458961f`: run `33316729039`, runtime job `99271430782` FAILURE on missing `field6-v6-*`, fresh audit `99271430912` FAILURE, physical job `99271431442` SKIPPED.

### Task 2 ? GREEN routing/admission

- [x] Create `TRACK_A_INDEPENDENT_EPHEMERAL_PHYSICAL_RUNTIME_V3.md` with exact readability modes.
- [x] Rotate workflow env/label/schema/seed path and executable physical identity V5 -> V6 while keeping current generation V6 trigger unchanged.
- [x] Rotate helper and package-acquisition runner/seed allowlists V5 -> V6.
- [x] Update independent admission audit to V6 and contract v3.
- [x] Change active task to `independent_ephemeral_physical_runtime`, one-login budget, admission source `PR_758_COMMENT_5469210031`, exact V6 guest/runner/seed/modes.
- [x] Candidate `32aafc5c2b084a2198c38db192d3eb8375270751` exact-head hosted runtime/security/admission/package/governance/boundary/CI GREEN; physical job `99272181229` SKIPPED. Final docs-only exact-head repeat and merge remain.

### Task 3 ? one-shot V6

- [ ] Post exactly one V6 trigger only after trusted-main routing readback.
- [ ] Prove exactly one attempt-1 queued job for `field6-v6-<comment_id>` before runner configuration.
- [ ] Create root-owned schema-v3 provenance mode `0644`; verify read as `runner` before registration.
- [ ] Register exact ephemeral/no-default-label runner via masked `ACTIONS_RUNNER_INPUT_TOKEN`; start one job.
- [ ] Destroy V6 guest after terminal outcome regardless of result; never rerun V6.
- [ ] If scalar proven, promote sanitized scalar to trusted main and continue Track B/global-login closeout.

Local candidate falsification: runtime/security/seed contracts PASS; full independent admission audit PASS; Bash syntax PASS; git diff --check PASS. Hosted GREEN remains required before merge.
