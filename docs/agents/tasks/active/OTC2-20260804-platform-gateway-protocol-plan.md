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
updated: 2026-08-04T16:18:00+02:00
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
- [ ] Documentation validation, exact-head CI, review, merge, archive and lease release pass.

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

Current PR #263 changes exactly six documentation/task/prompt paths. It changes no Rust source, Cargo manifest/lockfile, workflow, packet layout, authentication runtime, Platform/Gateway runtime, Otheryn runtime, asset or production state.

# Validation plan

- verify every relative link and referenced repository path;
- review complete changed-file list and diff;
- check current-versus-target statements against named Platform/Gateway contract evidence;
- check package dependencies and launchability claims for contradictions;
- run exact-head repository CI;
- perform fresh independent documentation/security review;
- require zero unresolved review threads before merge.

# Context checkpoint

```yaml
phase: exact-head-validation
status: validating
pull_request: 263
exact_head_before_checkpoint: 9edb31f2b7c71ea3f4c9194a71872c8444f669f3
next_action: Validate the final documentation head, update the PR description with exact evidence, mark ready, merge after required checks, then archive the task and release leases.
```
