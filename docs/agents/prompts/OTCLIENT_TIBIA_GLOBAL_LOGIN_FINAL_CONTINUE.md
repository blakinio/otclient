# OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE

```yaml
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
repository: blakinio/otclient
entry_task: OTC-20260828-current-login-field6-runtime
```

## ROLE

You are the autonomous coordinator finishing the Tibia Global login objective across Track A field6 evidence and then Track B PR #284. GitHub live state is the source of truth. Do not restart completed work and do not trust checkpoint SHA/PR/runtime state without fresh readback.

## Mandatory startup

Read current trusted `main`, repository `AGENTS.md`, `docs/agents/AGENTS.md`, `EXECUTION_PROTOCOL.md`, `ANTI_STALL_AND_EXECUTION_BUDGET.md`, `TIBIA_RESEARCH_TRACKS.md`, the hybrid routing and independent-ephemeral contracts, then the active field6 task and its newest evidence.

Required checkpoint evidence:
`docs/agents/evidence/OTC-20260828-current-login-field6-runtime/20260830-v4-preauth-failure-official-launcher-seed.md`

Expected repair branch if still live:
`fix/OTC-20260830-field6-official-launcher-seed`

Checkpoint base was `main@18ff83053f5c5d85c9bce6debab0f7fef6b79ecd`; re-resolve because main may have advanced.
## Current proven floor — do not redo V4

V4 is terminal archival evidence:

- trigger comment `5467500633`;
- run `33300352335`, job `99227195253`, attempt `1`;
- exact runner `molehill-otclient-v4-01` and label `field6-v4-5467500633`;
- independent provenance and trusted-main gates passed;
- package step failed with `FETCH_FAILED:curl_22` after WARP PASS;
- authorization, credential exposure and login capture were skipped;
- `physical_action_count=0`, `login_submit_count=0`, `FIELD6_VALUE=UNKNOWN`;
- runner deregistered and V4 guest was destroyed.

Never rerun V4, never reuse comment `5467500633`, and never treat GitHub UI rerun as a permitted new generation.

Root cause is proven: direct custom curl requests for manifest-listed client binaries receive Cloudflare managed challenge HTTP 403, while current manifest/version remain valid. Do not repair this by bypassing Cloudflare or by retrying the same downloader.

## Official-launcher seed fact

Molehill-PC already had the official Linux Tibia launcher. In a throwaway isolated Linux guest, without credentials/login, the launcher successfully installed exact client `15.32.75d4a0`.

Exact installed `bin/client`: size `52105824`, SHA256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.
Frozen local seed on Molehill-PC:

`C:\OTClientV4\tibia-15.32.75d4a0-official-launcher-seed.tar.gz`

Seed size `412272538`, SHA256 `64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016`. It contains the launcher-installed package plus embedded package/asset manifests. Proprietary bytes must not be committed or uploaded to GitHub.

## Phase 1 — finish repository-only seed repair

Current causal RED test is `.github/scripts/test_track_a_current_client_package_seed.py`; expected starting failure is `FIELD6_SEED_RED: materialize_seed missing`.

Use TDD. Finish the fixture first, then implement the smallest safe seed consumer. Required behavior:

1. accept only a host-provisioned local seed, never a repo/download URL fallback;
2. verify exact seed size/SHA before extraction;
3. reject symlinks, hardlinks, devices, absolute paths, `..`, duplicates and extraction escapes;
4. never execute seed content during acquisition/verification;
5. parse embedded `package.json`, `package.json.version`, `assets.json`, `assets.json.sha256`;
6. require exact version `15.32.75d4a0` and asset-manifest hash agreement;
7. re-hash/re-size every package and asset `localfile` against its manifest `unpackedhash/unpackedsize`;
8. re-prove exact `bin/client` fence before authorization/credentials/login;
9. preserve cleanup and secret-env exclusion.

Design the V5 host handoff fail-closed: copy the frozen seed into the fresh guest before runner registration, bind its path/size/SHA to root-owned provenance, then disable/remove host integration. Do not expose the Windows filesystem to the GitHub job.
Update acquisition/workflow/security/admission contracts for a **fresh V5 generation** only after seed GREEN. Do not let the unmerged repair branch authorize its own V5 runtime. Require focused tests, Track A governance, fresh independent audit, exact-head required CI, zero material findings/threads, clean restack and merge to trusted `main` before runtime admission.

## Phase 2 — fresh V5 scalar observation

Only after the seed repair is trusted on `main`:

- create a new V5 admission/trigger generation; do not mutate/reuse V4;
- provision a fresh `OTClientV5Clean`-equivalent guest from the pinned rootfs according to the then-current merged contract;
- stage and hash-verify the local seed before runner registration;
- prove no host mounts/interop/Docker/Podman/prior runner/repo/task state;
- queue before runner-online and use a new comment-derived one-time label;
- exactly one login submit maximum;
- no relog/restart/character selection/world entry/gameplay/network payload capture;
- GDB remains the parent and retained process evidence is only sanitized `uint32(edx)` at the exact producer;
- destroy runner/guest after every terminal result.

If V5 proves field6, promote only sanitized scalar/provenance through a separate repository-only PR and merge it to trusted `main`. If login submit occurs but scalar is not proven, do not retry identically.

## Phase 3 — Track B #284

Only after field6 promotion reaches trusted `main`, re-resolve PR #284 and its exact current task/head. Reconstruct/restack on fresh main rather than carrying stale history. Insert exact field6 in the typed login wire between fields 5 and 7, prove a materially changed outbound request RED→GREEN, then use one legal official-service E2E per new evidence-derived delta.
Track B historical blocker token `BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE` is orientation only; live repository evidence wins. Terminal success requires real structural proof, including `TIBIA_GLOBAL_LAB_GAME_START_PROVEN=true` and preferably `TIBIA_GLOBAL_LAB_IN_GAME_PROVEN=true`. Never call static green tests alone a successful Global login.

## Same-window Vision policy

After any independently legal, materially changed Track B E2E, apply Vision in the **same invocation** when accepted secret-safe keyframes exist. **do not ask the owner to open a second chat/window**. Use `tools/tibia-re-vision-benchmark` from fresh trusted main.

Vision is `visual_only` with `structural_authority:false`. Never trigger or repeat an official-service E2E merely to obtain screenshots. Vision cannot authorize protocol mutation, login acceptance, GAME_START or IN_GAME conclusions.

If no accepted keyframes exist, record `VISION_POST_E2E=SKIPPED_NO_ACCEPTED_KEYFRAMES` and continue structural Track B work. If accepted keyframes exist, record `VISION_POST_E2E=RUN_QWEN` and run the bounded local Qwen profile according to current trusted benchmark policy. If the local model host is unavailable, record `VISION_POST_E2E=BLOCKED_LOCAL_MODEL_HOST_UNAVAILABLE`; do not repeat login/E2E and continue structural Track B work where possible.

Reject/quarantine any frame with possible credentials, 2FA, session/auth tokens, cookies or secret-bearing overlays. Do not persist chain-of-thought or secret-bearing visual material.

## Authority and stop conditions

- GitHub live state and trusted-base contracts override this checkpoint.
- `blakinio/otclient` is the only repository for these tracks.
- Synology remains forbidden for secret-bearing field6 V4/V5 unless a later trusted-main security decision explicitly changes that fact.
- No credentials/session/cookies/raw packet/raw memory/proprietary client package in Git or GitHub artifacts.
- No identical secret-bearing retry without a material evidence-derived change.
- Use Codex/Spark when useful for multi-file implementation/test loops, but independently verify outputs.
- Continue until DONE, a genuine authority/safety/external blocker, anti-stall budget stop, or unsafe context/tool limit. A checkpoint/commit/PR/merge alone is not a stop condition.
## Final response contract

Report only fresh verified state:

```text
STATUS=DONE|BLOCKED|WAITING|ROTATE
TRACK_A_FIELD6=<uint32>|UNKNOWN
PHYSICAL_ACTION_COUNT=<n>
SEED_REPAIR=<state/head/PR>
V5_RUN=<run/job or none>
TRACK_B_PR284=<state/head/merge>
GAME_START=<true|false|unknown>
IN_GAME=<true|false|unknown>
VISION_POST_E2E=<required enum>
BLOCKER=<none or exact blocker>
NEXT_ACTION=<one concrete action or none>
```

Evidence before claims. Persist every material checkpoint in Git before rotation.