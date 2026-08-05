---
task_id: OTC2-20260805-native-protocol-single-version-completion
coordination_id: OTS-20260804-native-protocol-selection
status: active
agent: ChatGPT
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
branch: agents/ots-native-selection-rust-correction-20260804
base_branch: main
created: 2026-08-05T13:08:00+02:00
updated: 2026-08-05T14:29:00+02:00
risk: high
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
execution_mode: github-only
implementation_authorized: true
production_activation_authorized: false
related_pr: 273
owned_paths:
  - oteryn-client/docs/agents/tasks/active/OTC2-20260805-native-protocol-single-version-completion.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
shared_path_lease: []
modules_touched:
  - native-protocol-correspondence
cross_repo_tasks:
  - blakinio/Oteryn-Platform#540
  - blakinio/Otheryn#365
required_reads:
  - AGENTS.md
  - AGENTS.override.md
  - oteryn-client/AGENTS.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
  - oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md
  - oteryn-client/docs/architecture/PLATFORM_GATEWAY_GAME_ENTRY.md
  - oteryn-client/docs/architecture/DUAL_PROTOCOL_EXECUTION_PLAN.md
search_first:
  - exact merged Platform correction and Otheryn correspondence commits
  - active Rust tasks, protocol-canary ownership and shared-path leases
optional_reads: []
---

# OTC2-20260805-native-protocol-single-version-completion

## Goal

Adopt the corrected Platform and Otheryn correspondence for exactly `family = oteryn`, `native_protocol_version = 1`, no native profile dimension, then implement the independent Rust `protocol-oteryn` adapter and automatic family selection using the existing Tokio transport.

## Acceptance criteria

- [x] Correspondence pins exact merged Platform and Otheryn commits plus corrected schema digest.
- [x] Correspondence contains no native profile field/value/catalogue/factory/selection and preserves independent `protocol-canary`.
- [ ] Correspondence exact-head CI and independent audit pass and merge after Otheryn correspondence.
- [ ] A later runtime branch implements `protocol-oteryn`, TLS/ALPN, BE32/protobuf, bounded queues/cancellation, semantic commands, authoritative events, snapshot/delta/resync and immutable adapter binding.
- [ ] Production `Auto` validates Gateway authority and never falls back after redeem/selection/credential handoff.
- [ ] Rust workspace, architecture, supply-chain, parser/fuzz, session fencing and exact Canary regression pass.
- [ ] Runtime exact-head CI, audits, merge, archive and ownership release complete.

## Ownership

```yaml
owned_paths:
  - oteryn-client/docs/agents/tasks/active/OTC2-20260805-native-protocol-single-version-completion.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
shared_path_lease: []
modules:
  - native-protocol-correspondence
dependencies:
  - blakinio/Oteryn-Platform#540 merged as c0b8703d326a04b43ae8e06f6192b0cb91c859b7
  - blakinio/Otheryn#365 merged as 92bd106a92a8c3622de85099e2152db5b8cf2bde
blockers: []
cross_repository_tasks:
  - OTERYN-20260805-native-protocol-single-version-completion
  - OTH-20260805-native-protocol-single-version-completion
```

## Context checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-05T14:29:00+02:00
head: 8fd6353f25521d142a15599a24c143a9de617248
branch: agents/ots-native-selection-rust-correction-20260804
pr: 273
status: active
context_routes:
  - architecture
  - auth-identity
  - canary-integration
  - security
  - testing
owned_paths:
  - oteryn-client/docs/agents/tasks/active/OTC2-20260805-native-protocol-single-version-completion.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
proven:
  - Platform correction merged as c0b8703d326a04b43ae8e06f6192b0cb91c859b7.
  - Otheryn correspondence merged as 92bd106a92a8c3622de85099e2152db5b8cf2bde.
  - Canonical schema SHA-256 is 9c67f19525400fb9890d2a3541ceb6d02eb955061540ad39ca1c1d891c06eba9.
  - Active Canary work owns only protocol-canary and Canary-specific evidence/tests; shared_path_lease is empty.
  - protocol-oteryn remains an independent target path and is not currently owned.
  - Existing Tokio transport remains protocol-neutral and is the required transport runtime.
  - Production activation is not authorized.
derived:
  - Rust correspondence can now complete and merge before any runtime implementation begins.
unknown: []
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - Add a native profile enum, catalogue, factory, map or force-profile mode.
  - Translate native semantics through protocol-canary.
  - Switch adapters after ticket redeem or session failure.
changed_paths:
  - oteryn-client/docs/agents/tasks/active/OTC2-20260805-native-protocol-single-version-completion.md
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
validation:
  - command: immutable cross-repository provenance verification
    result: PASS
    evidence: exact merged Platform and Otheryn revisions are pinned with schema digest
blockers: []
next_action: Run correspondence exact-head CI and five independent audits, then merge PR #273.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: OTS-20260805T1429+0200-rust-correspondence
  session_started_at: 2026-08-05T14:29:00+02:00
  checkpointed_at: 2026-08-05T14:29:00+02:00
  last_progress_at: 2026-08-05T14:29:00+02:00
  phase: validate-rust-correspondence
  exact_head: 8fd6353f25521d142a15599a24c143a9de617248
  pull_request: 273
  active_operation: exact-head-ci-and-audits
  external_run_ids: []
  operation_started_at: 2026-08-05T14:29:00+02:00
  wait_deadline_at: null
  check_generation: exact-head
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: correspondence exact-head CI and independent audits pass
  next_action: Merge PR #273 and create a separate runtime implementation branch from the resulting main head.
```
