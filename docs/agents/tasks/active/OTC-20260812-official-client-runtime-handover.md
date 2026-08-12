---
task_id: OTC-20260812-official-client-runtime-handover
status: ready
branch: docs/OTC-20260812-official-client-runtime-handover
base_branch: main
created: 2026-08-12
updated: 2026-08-12
related_pr: ""
owned_paths:
  - docs/agents/tasks/active/OTC-20260812-official-client-runtime-handover.md
required_reads:
  - AGENTS.md
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md
search_first:
  - PR #48 and current Oteryn-Platform Tibia analysis branch before any runtime continuation
optional_reads: []
---

# OTC-20260812 — official Tibia client runtime handover

## Purpose

Preserve the verified official-client login/world-entry investigation so a later `blakinio/otclient` worker does not need chat history and does not repeat disproven approaches.

This is a **cross-repository evidence handover**, not authority to mutate the separately owned Oteryn runtime. The directly related OTClient execution task is `OTC-20260727-tibia-linux-runner-analysis`, draft PR #48 on `ci/OTC-20260727-tibia-linux-runner-analysis`.

## Scope and safety boundary

- Target repository for this handover: `blakinio/otclient`.
- Source runtime investigation: `blakinio/Oteryn-Platform`, branch `ops/oteryn-tibia-client-analysis-20260811`, draft PR #1006.
- Oteryn owned runtime: `oteryn-tibia-client-analysis` on `oteryn-synology-staging`.
- OTClient work must treat that Oteryn container/state as read-only evidence unless separately authorized by the Oteryn task ownership model.
- Never expose or persist Tibia credentials, account data, character names, session material, authenticated screenshots, proprietary client binaries, or extracted proprietary assets.
- Do not touch canonical `oteryn-staging` Compose services.

## PROVEN — official client and decoded Worldmap boundary

Official Linux client evidence:

- version `15.32.df7b29`;
- executable `/data/client-15.32.df7b29/bin/client`;
- size `51,965,216` bytes;
- SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

Decoded Worldmap boundary already established and should not be rediscovered without contradictory evidence:

- `handleFullMapMessage` -> `0xcec8d0`;
- `handleFieldDataMessage` -> `0xcd3190`;
- Create -> `0xcecc70`;
- Change -> `0xcecf40`;
- Delete -> `0xcd4e20`;
- shared ordered map routine -> `0x19a8a80`;
- Coordinate protobuf schema: `x=1:uint32`, `y=2:uint32`, `z=3:uint32`;
- the common routine preserves protobuf repeated-field order while iterating field contents;
- per-content processing selects the nested payload through helper `0x1ab4e50`, with `0x314b480` remaining the high-confidence AppearanceInstance default-instance candidate, before runtime map-content builder `0xceca50`.

Final runtime acceptance is still missing: one live decoded sample normalized to `(x,y,z) -> ordered contents -> appearance/type IDs`.

## PROVEN — tunnel and credential boundary

The original kernel/TUN approach was not viable on the Synology environment. The successful network path is userspace WARP:

`wgcf -> wireproxy SOCKS5 127.0.0.1:25344 -> proxychains4 -> Tibia client`

Verified outcomes:

- Cloudflare trace returned `warp=on`;
- direct and tunneled egress differed in the proving runs;
- Tibia client traffic was confined to the local SOCKS path rather than a direct remote TCP socket;
- canonical staging inventory remained unchanged in the bounded runs.

During early Oteryn runs the repository Actions secrets were absent/empty and login correctly failed closed before entry. In later runs the test email/password were injected by GitHub Actions and appeared only as masked values (`***`) in job environment output. No secret value was persisted to Git.

## PROVEN — account login reaches Select Character

The official client can be launched under Xvfb and the account credentials are accepted far enough to reach the `Select Character` dialog.

Relevant verified runs:

- `31612091815` / job `94165700952` — reached character selection; click/activation attempt eventually returned to account login.
- `31612594076` / job `94167418903` — reached character selection; anchored row/OK attempt returned to account login.
- `31613139300` / job `94169246915` — row visual selection changed, but activation returned to account login.
- `31614553971` / job `94173984093` — corrected geometry selected the actual first visible row and visibly changed selection; activation still returned to account login.
- `31615871684` / job `94178400132` — selected-row Return activation also failed in the world-entry step.

No run above proves an authenticated game-world session.

## Failure history — what failed and why

### 1. Kernel WARP / `/dev/net/tun`

**Failure:** initial WARP installation/activation attempts could not establish a usable kernel tunnel. The host did not expose `/dev/net/tun`; the analysis container was initially unprivileged; host-level TUN remained unavailable even after bounded probes.

**Why it failed:** the Synology/Docker execution environment did not provide the required kernel TUN device/capability path.

**Resolution:** abandon repeated kernel-TUN retries and use userspace WireGuard/WARP (`wgcf` + `wireproxy`) instead. That path was later proven.

### 2. GitHub-hosted fallback download

The related OTClient task PR #48 tested GitHub-hosted `ubuntu-24.04` as a separate no-OCR path.

**Failure:** the official Linux launcher archive request to `static.tibia.com/download/tibia.x64.tar.gz` returned HTTP 403, including through verified WARP. Run references retained in the PR #48 task record include `31617541307` and `31617769586`.

**Why it failed:** the public hosted-runner request shape/environment was rejected by the official distribution endpoint; changing egress to WARP did not solve the 403.

**Conclusion:** do not repeatedly brute-force hosted-runner download attempts or weaken transport/egress safety. A trusted self-hosted runtime with already materialized official client remains the practical path.

### 3. Actions secrets initially unavailable in Oteryn workflow

**Failure:** early WARP runs resolved `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` to empty values and correctly skipped login.

**Why it failed:** those secret names were not available to the particular workflow execution at that time.

**Resolution:** later workflow runs show both values injected and GitHub-masked; this blocker is no longer the explanation for the current world-entry failure.

### 4. Wrong character-row geometry

**Failure:** several early attempts used derived/fixed row positions. One stabilized attempt clicked around `y=235`.

**Why it failed:** a later geometry-only diagnostic proved the first real row text cluster was around `y=196`, so `y=235` could select the wrong list area even though the dialog reacted visually.

Evidence: diagnostic run `31614383785`, job `94173414953`, reported `GEOMETRY_FIRST_ROW_Y=196` with a 3-token cluster while never emitting the character name.

**Resolution:** derive the row from OCR geometry only; do not print arbitrary OCR text. Corrected execution used approximately `x=292,y=193` and produced `CHARACTER_ROW_VISUAL_CHANGE=true`.

### 5. Correct row selection still does not enter the world

**Failure:** after correcting the row, run `31614553971` selected `x=292,y=193`, visibly changed the row state, then clicked the anchored OK button. Safe snapshots at 1, 5 and 15 seconds still classified the final state as returned to Account Login.

**Why this matters:** it disproves the hypothesis that the entire remaining problem was simply clicking the wrong row.

Subsequent exact-row activation variants (including double-click / Return-based activation) also failed; run `31615871684` job `94178400132` specifically failed in `Login account and activate selected character with Return`.

### 6. Proxy/WARP configuration is not the current leading cause

Diagnostic run `31613249273`, job `94169615390`, proved:

- `strict_chain`, `proxy_dns`, `quiet_mode` enabled;
- exactly one proxy entry;
- type `socks5`;
- local endpoint on port `25344`;
- Cloudflare trace `warp=on`;
- owned analysis container still running;
- canonical staging inventory unchanged.

The same diagnostic found only two client log lines containing `failed`; both categorized as Vulkan-related, not network/TCP/DNS/TLS failures.

**Conclusion:** do not fall back to direct household/public egress and do not treat the proxy as disproven. The verified tunnel remains mandatory.

### 7. Vulkan initialization remains a candidate, not a proven root cause

Safe diagnostics observed client `failed` markers associated with Vulkan initialization. The live Oteryn branch later advanced to commit `04ae356ffe4769b49e28058880088c6533d256af` (`ci: test Tibia world entry with software Vulkan`).

**UNKNOWN:** this handover did not verify the final outcome of that software-Vulkan experiment. Do not claim Vulkan is the root cause until the corresponding run/result is inspected.

## Rejected / superseded hypotheses

- **Need to decode encrypted TCP first** — rejected as unnecessary; the decoded protobuf/Worldmap boundary is already statically proven and is lower risk.
- **Kernel WARP is required** — rejected; userspace WARP is proven and carries actual Tibia client traffic.
- **Credentials are the current blocker** — rejected for the later runs; account login reaches Select Character with masked secret injection.
- **Wrong row is the whole problem** — rejected; corrected real-row geometry still returns to account login.
- **Proxy/WARP is obviously broken** — rejected by live WARP trace, local SOCKS configuration and TCP-confinement evidence.
- **A window/pixel change is sufficient success evidence** — rejected by policy; only a semantic in-world/runtime event or decoded Worldmap event should prove world entry.

## UNKNOWN

- Exact reason the official client returns from selected character activation to Account Login.
- Whether software Vulkan eliminates the return-to-login behavior.
- Whether another account/security/setup condition is involved; no recovery/security material may be created or changed without an explicit authority path.
- A live decoded FullMap/FieldData sample has not been captured.
- A character has not been proven online and left idle.

## Recommended continuation

1. Inspect the live Oteryn branch/run state after head `04ae356ffe4769b49e28058880088c6533d256af`, especially the software-Vulkan experiment; do not infer its result from the commit name.
2. Preserve userspace WARP and secret boundaries exactly.
3. Reuse the corrected first-row geometry approach rather than fixed `y=235` logic.
4. Instrument/observe a semantic world-entry event at or before the already proven Worldmap boundary; do not accept a UI-only change as success.
5. If world entry succeeds, leave the character idle/online and immediately capture one bounded decoded map sample.
6. For work executed from `blakinio/otclient`, coordinate with PR #48 rather than creating another competing runtime implementation; do not mutate the Oteryn-owned runtime from an OTClient task.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-12T16:51:00Z
head: UNKNOWN
branch: docs/OTC-20260812-official-client-runtime-handover
pr: none
status: ready
context_routes:
  - docs/agents/CONTEXT_HANDOFF.md
  - docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md
owned_paths:
  - docs/agents/tasks/active/OTC-20260812-official-client-runtime-handover.md
proven:
  - Official client 15.32.df7b29 identity and decoded Worldmap handler/common routine addresses are preserved above.
  - Userspace WARP through local SOCKS 127.0.0.1:25344 is proven and actual Tibia traffic was confined to the tunnel in the proving runs.
  - Account authentication reaches Select Character with later masked Actions-secret injection.
  - Geometry diagnostic found the first real character-row cluster near y=196; corrected selection near y=193 visibly selected it.
  - Corrected row selection and multiple activation variants still returned to Account Login; no game-world session is proven.
  - Diagnostic run 31613249273 found the retained proxy configuration valid and the only failed log categories were Vulkan-related.
derived:
  - Character-row misclick was a real earlier defect but is not the complete explanation for the remaining world-entry failure.
  - Current investigation should prioritize semantic world-entry failure / renderer-runtime causes without weakening WARP or credential boundaries.
unknown:
  - Outcome of the later software-Vulkan experiment at current Oteryn head 04ae356ffe4769b49e28058880088c6533d256af.
  - Exact reason for return to Account Login after selected-character activation.
  - Live decoded map sample and proven online character session.
conflicts: []
first_failure:
  marker: selected character activation returns to Account Login instead of producing a semantic in-world state
  evidence: runs 31614553971 and 31615871684
rejected_hypotheses:
  - Wrong fixed row geometry was the sole cause: corrected actual-row selection still failed.
  - Proxy/WARP was the cause: userspace WARP and local SOCKS configuration are proven.
  - Credentials were unavailable in all runs: later runs injected both values as GitHub-masked secrets and reached Select Character.
changed_paths:
  - docs/agents/tasks/active/OTC-20260812-official-client-runtime-handover.md
validation:
  - command: GitHub live-state inspection of Oteryn runs 31613249273, 31614383785, 31614553971, 31615871684 and PR #48 durable task record
    result: PASS
    evidence: exact run/job metadata and safe logs inspected; no secret values reproduced
blockers: []
next_action: Inspect the completed software-Vulkan/world-entry run(s) after Oteryn head 04ae356ffe4769b49e28058880088c6533d256af and continue from the first semantic failure without repeating rejected approaches.
```
