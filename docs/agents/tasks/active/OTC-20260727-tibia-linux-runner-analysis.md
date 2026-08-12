# OTC-20260727 — Tibia Linux runner analysis

## Status

`implementing` — stale operational task resumed on 2026-08-12 under the owner's current instruction to attempt a real official-client login without OCR and to persist work in `blakinio/otclient`.

This remains a one-off research/validation task. It is not a merge-ready product change and must not commit proprietary CipSoft bytes, credentials, account data, character data, cookies, session material, or private captures.

## Current objective

Run one bounded official Linux Tibia login/world-entry attempt on the Synology self-hosted runner **without OCR/Tesseract**. Use deterministic UI input only for the unavoidable graphical authentication controls and use protocol/runtime evidence, not text recognition, to prove whether game-world entry occurred.

The stronger follow-up target is to prove a decoded Worldmap handler hit after authentication so later work can consume semantic client state instead of image text.

## Ownership and coordination

- Repository: `blakinio/otclient`
- Branch: `ci/OTC-20260727-tibia-linux-runner-analysis`
- PR: `#48` (draft operational PR)
- Runner label: `oteryn-staging`
- Expected runner: `oteryn-synology-staging`
- Owned paths:
  - `.github/workflows/tibia-linux-runner-analysis.yml`
  - `docs/agents/tasks/active/OTC-20260727-tibia-linux-runner-analysis.md`
- Owned persistent host state: `/var/lib/oteryn-staging-state/tibia-linux-analysis`
- Planned owned container: `otclient-tibia-login-analysis`
- Required labels: `com.blakinio.owner=otclient`, `com.blakinio.purpose=tibia-login-no-ocr`, `com.blakinio.task=OTC-20260727-tibia-linux-runner-analysis`

A separate `Oteryn-Platform` Tibia-analysis branch received a fresh commit during this takeover. Its `oteryn-tibia-client-analysis` container/state are therefore treated as concurrently owned and must not be read, restarted, stopped, recreated, written, or otherwise used by this task.

## Proven reusable evidence

Read-only cross-repository durable evidence from `blakinio/Oteryn-Platform@ops/oteryn-tibia-client-analysis-20260811` establishes, for official Linux client `15.32.df7b29`:

- installed client executable size `51,965,216` and SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` at the recorded evidence cut;
- Xvfb launch and graphical Account Login were previously reached;
- a userspace Cloudflare WARP path using `wgcf` + `wireproxy` SOCKS5 was proven with `warp=on`, changed egress, and actual Tibia TCP confined to local SOCKS `127.0.0.1:25344`;
- the exact current-login geometry previously used on a verified `1020x650` client window was email `(535,275)`, password `(535,304)`, Login `(590,388)`, first character-row interior `(400,214)`, and OK `(792,511)`;
- decoded Worldmap handlers were statically identified as FullMap `0xcec8d0`, FieldData `0xcd3190`, Create `0xcecc70`, Change `0xcecf40`, Delete `0xcd4e20`; shared map-data routine `0x19a8a80` preserves repeated field/content order;
- prior Oteryn-Platform runs did **not** prove successful authentication because its `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD` secrets resolved empty at those runs.

These facts are evidence inputs only. This task must independently verify the currently downloaded binary identity, current UI geometry preconditions, tunnel state, actual TCP confinement, secret availability, and runtime result before claiming success.

## Safety boundaries

- Never touch canonical `oteryn-staging` Compose containers, deployment infrastructure, databases, networks, or volumes.
- Never touch the separate active `Oteryn-Platform` Tibia-analysis container/state.
- No blanket Docker cleanup.
- Before every mutation of the owned container, verify all three ownership labels.
- Do not originate the account login from the runner's normal/public household egress. Require changed tunneled egress and `warp=on` first.
- Require the real Tibia process to be confined to the local SOCKS endpoint before credential entry; any direct remote TCP fails closed.
- Credentials may enter only from GitHub Actions repository secrets named `TIBIA_TEST_EMAIL` and `TIBIA_TEST_PASSWORD`. Test only non-emptiness; never print or persist values.
- Unset credential variables immediately after deterministic entry into the login controls.
- Do not use OCR, Tesseract, image-to-text, accessibility scraping of secret fields, or arbitrary screenshot text extraction anywhere in the login/world-entry/proof path.
- Do not upload screenshots from authenticated state. Prefer text-only non-secret runtime markers.
- Do not commit or upload CipSoft binaries/assets/archives.
- Leave the character idle if world entry succeeds; do not perform gameplay movement, combat, chat, inventory, or other world actions in this task.

## Acceptance criteria

1. Exact self-hosted runner and canonical-staging before/after inventory are verified.
2. A separate task-owned container/state is used; active Oteryn-Platform analysis runtime remains untouched.
3. Current official Linux package is materialized in the owned state and its executable identity is recorded as non-proprietary metadata.
4. Userspace tunnel is verified by `warp=on` and changed public egress before credentials are made available to the client process.
5. Actual Tibia TCP is demonstrably confined to the local SOCKS transport before secret entry and remains free of direct remote TCP afterwards.
6. Credential availability is checked fail-closed from GitHub Actions secrets without exposing values.
7. No command invokes `tesseract`, OCR libraries, image-to-text, or secret-bearing screenshot inspection.
8. Login controls and first-character entry are driven deterministically only after exact window-size/geometry preconditions are satisfied.
9. Success is claimed only if a semantic/runtime proof of world entry is observed, preferably a decoded FullMap/FieldData/common-map handler hit in the exact verified client. Pixel change alone is insufficient.
10. If authentication, 2FA, secret availability, protocol/runtime instrumentation, or an external challenge blocks entry, record the exact non-secret blocker and stop without weakening the boundary.

## Validation strategy

- focused: YAML/static review ensuring no OCR/Tesseract command and no secret output;
- runtime: exact runner, owned-container labels, package hash/size, WARP trace, direct-vs-proxied egress, Tibia socket confinement, secret gate;
- E2E: Account Login -> character selection -> world entry on the real official client, with success determined by protocol/runtime evidence;
- after any workflow mutation, inspect the emitted run and the exact-head job result rather than trusting the workflow definition.

## Session checkpoint

```yaml
policy_version: 2
task_kind: e2e
feature_scope: infrastructure
complete_user_facing_feature: false
phase: implement
execution_mode: github_actions
execution_reason: requires the isolated Synology self-hosted runner, Docker, Xvfb, real official client and bounded network/runtime observation
updated_at: 2026-08-12T18:04:00+02:00
status: implementing
session_id: chatgpt-20260812-1802-no-ocr-login
session_role: implementer
session_generation: 2
stale_takeover_count: 1
session_rotation_count: 0
heavy_validation_runs: 0
human_interruptions: 0
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: one sequential real-client login scenario with shared runtime state
branch: ci/OTC-20260727-tibia-linux-runner-analysis
pr: 48
observed_head_before_takeover: 2c41d2110b516a82755b3862c95339fc254a357e
safe_to_resume: true
last_completed_step: stale branch/PR ownership verified; fresh Oteryn-Platform writer detected and excluded from runtime ownership; PR scope updated
next_action: replace the one-off workflow with an isolated no-OCR login probe, then execute and inspect the exact run
```

## Recovery checkpoint

```yaml
recovery_generation: 2
session_id: chatgpt-20260812-1802-no-ocr-login
checkpointed_at: 2026-08-12T18:04:00+02:00
phase: implement
branch: ci/OTC-20260727-tibia-linux-runner-analysis
expected_head_before_checkpoint: 2c41d2110b516a82755b3862c95339fc254a357e
pr: 48
active_operation: prepare isolated no-OCR official-client login workflow
external_run_ids: []
status: ready
safe_to_resume: true
next_action: update `.github/workflows/tibia-linux-runner-analysis.yml` to the bounded no-OCR flow and run it
```
