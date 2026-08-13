---
task_id: OTC-20260813-tibia-global-login-lab
status: implementing
agent: ChatGPT
project_lane: otclient
lane: otclient
track: legacy-analysis
task_kind: infrastructure
phase: consolidation
branch: feat/OTC-20260813-tibia-global-login-lab
base_branch: main
created: 2026-08-13T09:10:00+02:00
updated: 2026-08-13T09:51:00+02:00
risk: medium
related_pr: 284
owned_paths:
  - tools/tibia-global-login-lab/**
  - .github/workflows/tibia-global-login-lab.yml
  - docs/agents/tasks/active/OTC-20260813-tibia-global-login-lab.md
modules_touched:
  - legacy-analysis
  - github-actions
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
  - PR #48 runtime evidence as migration input only
  - synology-otclient-01 self-hosted runner
cross_repo_tasks: []
execution_mode: github-only
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: true
  completion_claim: internal_only
---

# Goal

Make `blakinio/otclient` the single durable source of truth and execution home for the official-Tibia compatibility investigation, and determine whether this OTClient fork can authenticate to and enter the official Tibia game service using the dedicated `synology-otclient-01` runner.

# Owner durable-state directive

As of 2026-08-13, all material work for this investigation must be persisted in `blakinio/otclient` rather than existing only in chat or another repository. This includes scripts, workflow changes, checkpoints, evidence summaries, failure classification, migration decisions, next actions, and final status. Chat is only an execution/control interface.

Runtime-only proprietary bytes, credentials, cookies, session keys, and other protected material must remain outside Git and are referenced only by non-secret evidence markers.

# Safety and isolation

- Repository writes are confined to `blakinio/otclient` and this task branch unless a later repository-governed closeout explicitly changes that.
- Execution is pinned to the repository's dedicated `synology-otclient-01` runner using labels `otclient` and `synology`.
- The lab owns separate Docker named volumes and a separate container namespace.
- It must not mutate canonical `oteryn-staging` services or depend on their writable state.
- It must not commit proprietary Tibia binaries/assets, credentials, cookies, session keys, private captures, screenshots containing secrets, or generated account data.
- Owner-funded Codex/API/token quota is forbidden unless the owner explicitly authorizes that specific use.
- Existing `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` GitHub Actions secrets may be consumed only by the bounded repository workflow and must never be printed or persisted.
- No OCR/Tesseract is part of the login proof path.

# Consolidation decision

PR #284 is the canonical active implementation for this investigation. PR #48 is migration input/evidence only and must not remain a parallel execution lane once its reusable runtime knowledge has been ported. Its large historical workflow collection is not to be copied wholesale; only evidence-backed components required by the canonical lab are migrated.

Verified reusable components from PR #48:

- exact self-hosted runner routing to `synology-otclient-01`;
- userspace WARP using pinned `wgcf` v2.2.32 and `wireproxy` v1.1.3 with SHA-256 verification;
- changed-egress verification through Cloudflare trace;
- current Tibia 15.32 asset materialization logic;
- bounded non-OCR OTClient login markers and credential redaction requirements;
- current HTTP login identifiers (`clientversion`, `clienttype`, `assetversion`) previously validated against the real login service.

# Acceptance inventory

- [x] Dedicated project root exists under `tools/tibia-global-login-lab/`.
- [x] Dedicated workflow exists and targets the OTClient Synology runner only.
- [x] Bootstrap verifies `RUNNER_NAME=synology-otclient-01` and Docker availability.
- [x] Bootstrap creates/refreshes only lab-owned Docker named volumes and container labels.
- [x] Runner execution emits non-secret proof markers for container/image identity and network isolation.
- [x] Draft PR #284 exists for the canonical lab.
- [ ] Port the proven userspace-WARP egress bootstrap from PR #48 into `tools/tibia-global-login-lab/**`.
- [ ] Route asset retrieval and OTClient runtime traffic through verified changed WARP egress.
- [ ] Re-run the exact-head E2E and classify the first real compatibility failure after infrastructure gates.
- [ ] Prove `HTTP_LOGIN_SUCCESS=true` on the canonical lab or persist the exact non-secret rejection classification.
- [ ] Attempt character handoff and `g_game.loginWorld()` after HTTP success.
- [ ] Prove `GAME_START=true` or persist a concrete compatibility/security boundary.
- [ ] Persist all material evidence and next action in this repository.
- [ ] Make PR #48 intentionally terminal as superseded after migration is complete.
- [ ] Run final exact-head relevant CI/audit and complete repository closeout only after the runtime objective is terminal.

# Current evidence

- PR #284 head before this checkpoint: `728b1ab175e9be0c165d2895f82897a6a68d229d`.
- Run `31677656137`, job `94375680670` executed on runner `synology-otclient-01` and proved the lab bootstrap, named volumes and isolated container.
- The same run failed before login because direct retrieval of `https://static.tibia.com/launcher/assets-current/assets.json` returned HTTP 403 repeatedly.
- This is an infrastructure/egress failure, not evidence of an OTClient game-protocol incompatibility.
- PR #48 contains a previously working userspace-WARP path using pinned `wgcf`/`wireproxy`; that component is now authorized migration input for PR #284.

# Next action

Port the pinned userspace-WARP setup and changed-egress verification into the canonical lab, make asset retrieval and OTClient traffic use that proxy, then run the exact-head E2E on `synology-otclient-01` until `GAME_START=true` or a concrete post-login compatibility boundary is proven.
