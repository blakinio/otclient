---
task_id: OTC2-20260804-platform-gateway-protocol-plan
coordination_id: OTS-20260804-native-protocol-selection
status: validating
agent: "platform gateway protocol architecture owner"
project_lane: otclient-v2
track: greenfield-rust
branch: docs/OTC2-20260804-platform-gateway-protocol-plan
base_branch: main
created: 2026-08-04T16:01:00+02:00
updated: 2026-08-04T16:24:00+02:00
risk: medium
related_prs: [263]
depends_on:
  - completed OTC2-20260804-dual-protocol-architecture
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-platform-gateway-protocol-plan.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md
  - oteryn-client/docs/architecture/PLATFORM_GATEWAY_GAME_ENTRY.md
  - oteryn-client/docs/agents/prompts/OTC2_TOKIO_TRANSPORT_AGENT.md
  - oteryn-client/docs/agents/prompts/OTS_NATIVE_PROTOCOL_CONTRACT_AGENT.md
modules_touched:
  - game entry architecture
  - protocol selection
  - Oteryn Identity and Game Gateway correspondence
shared_path_lease:
  - oteryn-client/docs/architecture/**
  - docs/agents/CROSS_REPO_CONTRACTS.md
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
execution_mode: github-only
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
user_communication: terminal_only
---

# Goal

Correct the dual-protocol roadmap so it explicitly reuses the already delivered Oteryn Platform native-auth chain: Oteryn Identity OAuth Authorization Code + PKCE, one-time Game Login Ticket issuance, Game Gateway login orchestration, World Registry routing and Game Session issuance. Define the three-repository responsibility split and save only the agent prompts that are safe to launch now.

# Acceptance criteria

- [x] Oteryn Platform and Game Gateway are explicit mandatory participants in native protocol selection.
- [x] Login API `protocol_version` is distinguished from the selected gameplay adapter/profile.
- [x] Existing Identity, ticket and Gateway behavior is reused rather than duplicated in the Rust client.
- [x] The execution sequence includes Platform/Gateway capability production before Otheryn native protocol consumption.
- [x] Package A Tokio remains independently launchable now.
- [x] A three-repository contract task is independently launchable now without implementing speculative wire bytes.
- [x] Two complete reusable prompts are stored under `oteryn-client/docs/agents/prompts/`.
- [ ] Current merge-ref revalidation passes, PR merges, task archives and leases release.

# Proven baseline

- Oteryn Platform already owns reusable credentials, browser OAuth/PKCE, MFA policy, one-time Game Login Ticket issuance and World Registry.
- The separately deployable Go Oteryn Game Gateway owns ticket redeem, login context, character/world routing and Game Session orchestration.
- The current Gateway protocol v1 does not yet advertise a native Oteryn gameplay adapter/profile; this remains coordinated future work.
- Gateway API `protocol_version`, Game Session contract version and gameplay adapter/profile are separate concepts.
- The Rust client must not create another login server, embed Oteryn password authentication, bypass Gateway or infer protocol selection from failed gameplay bytes.

# Delivered documentation

- `oteryn-client/docs/architecture/PLATFORM_GATEWAY_GAME_ENTRY.md` defines the component names, responsibility split, existing implementation truth, three-repository participation and mandatory rollout sequence.
- `oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md` now defines Packages A through G and marks only Package A and Package B launchable now.
- `docs/agents/CROSS_REPO_CONTRACTS.md` registers `OTS-20260804-native-protocol-selection` and distinguishes Gateway API v1 from gameplay protocol versions.
- `oteryn-client/docs/agents/prompts/OTC2_TOKIO_TRANSPORT_AGENT.md` is the launchable client-only implementation prompt.
- `oteryn-client/docs/agents/prompts/OTS_NATIVE_PROTOCOL_CONTRACT_AGENT.md` is the launchable three-repository contract-only prompt.

# Scope audit

PR #263 changes exactly six documentation/task/prompt paths. It changes no Rust source, Cargo manifest/lockfile, workflow, packet layout, authentication runtime, Platform/Gateway runtime, Otheryn runtime, asset or production state.

# Validation

Exact product head before this merge-ref checkpoint: `7a434338a00152e63393fa5167c83d854f41bcce`.

- repository CI run `30917797793`: PASS;
- required job `92020788439`: PASS;
- Rust Client run `30917797133`: PASS;
- Windows formatting, strict Clippy, workspace tests and architecture policy: PASS;
- supply-chain check: PASS;
- exact changed paths: six expected files;
- branch before checkpoint: 7 commits ahead, 0 behind;
- full path/role/version/downgrade/current-versus-target review: PASS;
- material findings: 0;
- unresolved review threads: 0;
- E2E: `NOT_APPLICABLE` — documentation only.

GitHub recalculated the synthetic PR merge ref after ready-for-review transition and temporarily reported required status `CI / Required` as expected even though the exact product head passed. This checkpoint creates one final synchronize generation. Do not change PR metadata or branch content again before merge.

# Context checkpoint

```yaml
phase: merge-ref-revalidation
status: validating
pull_request: 263
previous_validated_head: 7a434338a00152e63393fa5167c83d854f41bcce
repository_ci_run: 30917797793
rust_client_run: 30917797133
next_action: Observe the synchronize-generation checks on the resulting head and merge PR #263 without further metadata or content changes only when required checks are green, mergeability is true and review threads remain zero.
```
