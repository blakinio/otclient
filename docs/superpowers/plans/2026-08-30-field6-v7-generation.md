# Field6 V7 Generation and X11 Namespace Repair Plan

**Goal:** Revoke terminal V6, rotate the current repository generation to V7, then admit a fresh V7 guest only after eliminating the read-only WSLg `/tmp/.X11-unix` mount from the credential-bearing runtime namespace.

**Trusted base:** `main@5def12f5fbb5f3554b60b894df7257f00dcd39f3`.

## V6 terminal fact

V6 run `33317265138` / job `99272880272` failed at `xvfb_socket_missing` after provenance/admission/seed/auth/WARP PASS but before `start_client` and before `submit_login_once`. Physical/login count remains 0; field6 UNKNOWN; V6 guest destroyed.

## Task 1 ? static V7 generation

- [x] TDD RED requires `AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V7 once=true` and revokes V6 as historical.
- [x] Hosted RED causal: run `33317634698`, runtime `99273879730` FAILURE exactly on missing V7; fresh audit `99273879638` FAILURE; physical `99273880151` SKIPPED.
- [x] Minimal GREEN rotates workflow/task current generation V6 -> V7 and returns task to static-safe `runtime_access:none`, budget 0.
- [x] Exact-head candidate c2fec0fcc0b376695ee2d11de79ee81174ee47ca: field6 33317762701 (runtime 99274221549 SUCCESS, static audit 99274221406 SUCCESS, physical 99274221980 SKIPPED); package 33317762678/99274221335 SUCCESS; governance 33317762681/99274221424+99274221612 SUCCESS; boundary 33317762711/99274221481+99274221547 SUCCESS; CI 33317762813/99274297146 SUCCESS.\r\n- [ ] Final docs-only exact-head readback, Ready, expected-head merge.

## Task 2 ? fresh V7 X11 host prerequisite

- [ ] Import brand-new `OTClientV7Clean` from pinned Canonical rootfs; re-prove isolation/toolroot/runner/seed.
- [ ] Before runner registration, unmount the WSLg read-only `/tmp/.X11-unix` mount inside only this V7 guest, recreate `/tmp/.X11-unix` as local `root:root 1777`, prove it is not a mountpoint and is writable by runner for socket creation.
- [ ] Run secret-free Xvfb probe on a non-task display as runner and prove filesystem socket appears and is cleaned.
- [ ] Separate V7 owner admission and routing contract require local X11 socket dir proof before secrets.

## Task 3 ? one-shot V7

- [ ] Merge V7 routing/admission, post exactly one trigger, prove queue uniqueness, bind provenance, configure ephemeral runner via masked `ACTIONS_RUNNER_INPUT_TOKEN`.
- [ ] Execute one bounded capture; never rerun V7.
- [ ] Destroy V7 guest after terminal outcome.
- [ ] If scalar proven, promote sanitized field6 and continue Track B/global-login closeout.
