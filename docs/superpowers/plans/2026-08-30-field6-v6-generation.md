# Field6 V6 Static Generation Plan

**Goal:** Revoke terminal pre-action V5 from current trusted-main admission and rotate only the repository generation identifier to V6. This phase grants no live runner, credential, login, client execution, or physical mutation authority.

**Trusted base:** `main@d1ce0ad811cf6a4a5a3466f7e5af045f39acab31`.

## Terminal V5 fact

- trigger comment: `5469017445` (`AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V5 once=true`);
- workflow run: `33314713078`, attempt `1`;
- live job: `99265883209` on `molehill-otclient-v5-01`;
- provenance step failed before checkout because `/etc/otclient-field6-runner-provenance` was `root:root 0600` and therefore not readable by the unprivileged runner user;
- checkout/admission/package/authorization/secret/capture/evidence steps: SKIPPED;
- cleanup step failed only because checkout was skipped and the repository cleanup script was absent; no package acquisition state had been created;
- `physical_action_count=0`, `login_submit_count=0`, `FIELD6_VALUE=UNKNOWN`;
- ephemeral runner removed its `.credentials` and `.runner`, deregistered, and the entire `OTClientV5Clean` WSL guest was destroyed.

## TDD sequence

- [x] RED contract requires current V6 trigger and rejects V5 as historical.
- [x] Verify causal RED while physical live job is SKIPPED: run `33315765050`, runtime job `99268806498` failed on missing V6, physical job `99268807332` SKIPPED.
- [x] Minimal GREEN implemented: workflow current-generation condition V5 -> V6 and active task returned to static-safe `github_hosted` / `runtime_access:none` / budget 0.
- [ ] Preserve V5 physical runner/guest/seed routing inert behind static task; rotate those only in a later fresh V6 routing/admission PR.
- [x] Exact-head candidate `b28599af6f73d024d4d56fcb6486199ca1cb8a07` GREEN: field6 `33315959590`, package `33315959597`, governance `33315959585`, boundary `33315959570`, CI `33315959686`; physical job `99269338963` SKIPPED.
- [ ] Merge with expected-head guard and trusted-main readback.

## Successor rule

After static V6 merge, create a brand-new `OTClientV6Clean` guest from the pinned Canonical rootfs. The next provenance file must be root-owned, non-writable by runner, **and runner-readable** (`0644`), because trusted workflow verification executes as the unprivileged runner account. Only after direct host proof may a separate V6 owner admission/routing PR be considered.
