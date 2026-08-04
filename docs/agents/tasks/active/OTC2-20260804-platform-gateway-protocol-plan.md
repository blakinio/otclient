---
task_id: OTC2-20260804-platform-gateway-protocol-plan
coordination_id: OTS-20260804-native-protocol-selection
status: active
agent: "platform gateway protocol architecture owner"
project_lane: otclient-v2
track: greenfield-rust
branch: docs/OTC2-20260804-platform-gateway-protocol-plan
base_branch: main
created: 2026-08-04T16:01:00+02:00
updated: 2026-08-04T16:01:00+02:00
risk: medium
related_prs: []
depends_on:
  - completed OTC2-20260804-dual-protocol-architecture
owned_paths:
  - docs/agents/tasks/active/OTC2-20260804-platform-gateway-protocol-plan.md
  - oteryn-client/AGENTS.md
  - oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md
  - oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md
  - docs/agents/CROSS_REPO_CONTRACTS.md
  - oteryn-client/docs/agents/prompts/OTC2_TOKIO_TRANSPORT_AGENT.md
  - oteryn-client/docs/agents/prompts/OTS_NATIVE_PROTOCOL_CONTRACT_AGENT.md
modules_touched:
  - game entry architecture
  - protocol selection
  - Oteryn Identity and Game Gateway correspondence
shared_path_lease:
  - oteryn-client/AGENTS.md
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

- [ ] Oteryn Platform and Game Gateway are explicit mandatory participants in native protocol selection.
- [ ] Login API `protocol_version` is distinguished from the selected gameplay adapter/profile.
- [ ] Existing Identity, ticket and Gateway behavior is reused rather than duplicated in the Rust client.
- [ ] The execution sequence includes Platform/Gateway capability production before Otheryn native protocol consumption.
- [ ] Package A Tokio remains independently launchable now.
- [ ] A three-repository contract task is independently launchable now without implementing speculative wire bytes.
- [ ] Two complete reusable prompts are stored under `oteryn-client/docs/agents/prompts/`.
- [ ] Documentation validation, exact-head CI, review and merge pass.

# Proven baseline

- Oteryn Platform already owns reusable credentials, browser OAuth/PKCE, MFA policy, one-time Game Login Ticket issuance and World Registry.
- The separately deployable Go Oteryn Game Gateway owns ticket redeem, login context, character/world routing and Game Session orchestration.
- The current Gateway protocol v1 does not yet advertise a native Oteryn gameplay adapter/profile; this remains coordinated future work.
- The Rust client must not create another login server, embed Oteryn password authentication, bypass Gateway or infer protocol selection from failed gameplay bytes.

# Context checkpoint

```yaml
phase: documentation-update
status: active
next_action: Update the owned architecture, cross-repository registry and launchable agent prompts, then open the documentation PR and validate its exact head.
```
