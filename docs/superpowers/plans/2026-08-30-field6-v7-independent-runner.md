# Field6 V7 Independent Runner + Local X11 Admission Plan

**Goal:** Admit exactly one fresh V7 one-shot field6 observation only after proving a same-boot local X11 socket namespace that cannot regress to the WSLg read-only mount.

**Trusted base:** `main@0c7abfdbeace981e50375d7a322c414936718945`.

## Proven host prerequisite

- `OTClientV7Clean` freshly imported from Canonical rootfs SHA256 `915b4be62933475c3fb5f5031aa2e159294db95fb32aaa9e8b317aadcb6c065d`.
- automount/interop disabled; empty `/mnt/c` removed; no Docker/Podman sockets; no prior repo/runner state.
- WSLg `/tmp/.X11-unix` read-only mount removed while a host-control keeper preserves the same V7 boot.
- local `/tmp/.X11-unix` is `root:root 1777`, not a mountpoint, backed by V7 root ext4.
- secret-free Xvfb `:177` as `runner` created `/tmp/.X11-unix/X177` and cleaned it completely.
- Actions runner `2.337.0` archive SHA256 `70920811a4f8ad4328818682bca5c6469c1c942fab52448868071d0063816613`, unconfigured.
- exact official-launcher seed `/opt/otclient-v7-seed/seed.tar.gz`, size `412272538`, SHA256 `64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016`, directory/file `0555/0444`, runner-read verified.

## Authority

PR #758 comment `5469433732` is V7 admission only. Executable `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V7 once=true` remains unposted.

## Task 1 — TDD RED

- [x] Security contract expects V7 runner/guest/label/admission/seed and new independent-runtime contract v4.
- [x] Contract requires same-boot local X11 directory mode `1777`, `mountpoint=false`, secret-free Xvfb proof, and X11 verification before authorization/secrets.
- [ ] Open Draft PR and prove hosted causal RED with physical job SKIPPED.

## Task 2 — GREEN routing/admission

- [ ] Create contract v4 with same-boot local X11 boundary.
- [ ] Rotate workflow/helper/acquisition/audit physical identity V6 -> V7 and bind X11 proof into provenance schema v4.
- [ ] Workflow independently re-proves local X11 namespace and performs secret-free Xvfb probe before authorization/secrets.
- [ ] Live task uses one-login budget, V7 admission comment, exact guest/runner/seed/X11 fields.
- [ ] Exact-head runtime/security/audit/package/governance/boundary/CI GREEN; physical job SKIPPED; merge expected-head.

## Task 3 — one-shot V7

- [ ] Post exactly one V7 trigger after trusted-main readback.
- [ ] Queue uniqueness -> schema-v4 provenance -> ephemeral runner -> final queue gate.
- [ ] Start listener while keeper holds boot, then retire keeper only after runner listener owns the distro lifetime.
- [ ] Execute one bounded capture; never rerun V7; destroy guest after terminal outcome.
- [ ] If scalar proven, promote sanitized field6 and continue Track B/global-login closeout.