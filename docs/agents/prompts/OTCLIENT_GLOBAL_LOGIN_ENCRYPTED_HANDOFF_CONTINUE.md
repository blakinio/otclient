# OTCLIENT-GLOBAL-LOGIN-ENCRYPTED-HANDOFF-CONTINUE

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous implementation + validation + physical E2E continuation.

Continue the existing task `OTC-20260813-tibia-global-login-lab`, branch `feat/OTC-20260813-tibia-global-login-lab`, PR #284. Do not create a new task, branch or PR.

Treat current GitHub `main`, current PR #284 head, current task record and current runtime as source of truth. Do not trust historical PID/SHA/run state from chat.

First read:
- `docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md`
- `docs/agents/evidence/OTC-20260813-tibia-global-login-lab/20260824-molehill-encrypted-handoff.md`
- `.github/scripts/test_track_b_encrypted_handoff.py`
- `.github/workflows/tibia-global-login-encrypted-handoff.yml`
- `.github/track-b-encrypted-handoff/**`

Primary objective: reach and prove real OTClient `GAME_START` / `IN_GAME` against official Tibia Global 15.32 using the existing Track B lane, without exposing credentials/session secrets or uploading proprietary Tibia assets.
Hard boundaries:
- never print, persist plaintext, commit, upload or return `TIBIA_TEST_EMAIL`, `TIBIA_TEST_PASSWORD`, session keys, cookies, device cookies or play-session secrets;
- do not invoke secret-ingress through Remote Desktop Commander;
- do not copy the Molehill private handoff key into GitHub/Actions;
- do not upload proprietary Tibia binaries/assets to GitHub;
- do not weaken TLS/auth/anti-cheat or fabricate server success;
- do not mutate Track A paths or runtimes;
- do not repeat already-falsified hypotheses merely to get another run.

Current proven environment facts:
- Molehill `tibia-kasm` has exact current package `15.32.bf29ac`;
- official client size `52109920`, SHA256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`;
- current `assets.json` SHA256 `d1969b4ba69339fcea5ea52aa1bfe3eaf0b7800226a3635c1e71de87235837f9` and local expected hash match;
- current `catalog-content.json` SHA256 `6156366d9489d20bf2ec330f2365f3b328e36cbd57cdcdeba01706259e83765b`;
- current appearances/staticdata files are present and official launcher logged `InstalledAndUsable` + `Asset loading complete`;
- GitHub-hosted Ubuntu/Windows/macOS all receive HTTP 403 for `assets-current/assets.json`; hosted CDN fetching is a proven environment dead end;
- `tibiaclient-linux-current/package.json` is reachable but contains only binary package files, not gameplay assets;
- `synology-otclient-01` is currently offline; do not treat it as available without revalidation;
- local CMS encryption round-trip using the Molehill public certificate passed synthetically.
Continue autonomously in this order:
1. Revalidate PR #284 head, current `main`, task ownership and changed-path scope. Abort/reconcile if another Track B writer moved the branch.
2. Run the encrypted-handoff contract, shell syntax, YAML parse, `git diff --check`, and repository checkpoint validation. Fix only actual failures.
3. Publish the WIP encrypted-handoff checkpoint to the existing PR #284 branch. Ensure the isolated producer lane does not trigger the old full login-lab by path-filter accident.
4. Execute only the encrypted-handoff producer workflow. It may use GitHub Secrets for HTTP auth, but must upload only encrypted `handoff.cms` with one-day retention and fixed non-secret markers.
5. On Molehill, verify the committed public certificate fingerprint against the task-owned private key/cert material. Download only ciphertext and decrypt locally without printing plaintext values.
6. Stage the already verified current 15.32 asset cache from `tibia-kasm` into the local Track B OTClient runtime. Do not send those assets to GitHub.
7. Consume the decrypted handoff once and perform one bounded OTClient game-login attempt. Capture only sanitized state markers, server opcode class, and byte lengths/transport state.
8. Success requires real `GAME_START` plus authoritative in-game semantic evidence. `BRIDGE_3_OF_3`/object presence alone is not `IN_GAME` authority.
9. If the first game-server result is again structured `0x14`, do not retry the identical packet and do not guess field toggles. Require/consume current-build promoted wire-writer evidence before protocol mutation.
10. On success: update evidence/task, run self-review/required validation, make PR ready only if task acceptance is satisfied, and follow repository closeout policy. If a real blocker remains, persist exact blocker + evidence + next action instead of claiming completion.

Expected reporting style: FACT / INFERENCE / UNKNOWN where useful. Evidence before claims. Do not stop for routine recoverable failures; debug autonomously until success or a genuine authority/safety/external blocker.