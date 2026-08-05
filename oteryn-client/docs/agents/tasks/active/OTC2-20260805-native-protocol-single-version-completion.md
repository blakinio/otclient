---
task_id: OTC2-20260805-native-protocol-single-version-completion
coordination_id: OTS-20260804-native-protocol-selection
status: waiting
agent: ChatGPT
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
branch: agents/ots-native-selection-rust-correction-20260804
base_branch: main
created: 2026-08-05T13:08:00+02:00
updated: 2026-08-05T13:08:00+02:00
risk: high
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
execution_mode: github-only
implementation_authorized: true
production_activation_authorized: false
related_pr: none
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

- [ ] Correspondence pins exact merged Platform and Otheryn commits plus corrected schema digest.
- [ ] Correspondence contains no native profile field/value/catalogue/factory/selection and preserves independent `protocol-canary`.
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
  - blakinio/Oteryn-Platform#540 merged
  - blakinio/Otheryn#365 merged
blockers:
  - Platform correction and Otheryn correspondence are not yet merged
cross_repository_tasks:
  - OTERYN-20260805-native-protocol-single-version-completion
  - OTH-20260805-native-protocol-single-version-completion
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-05T13:08:00+02:00
head: d1cd2c8502ef3363d1a104f0694fd1c7d15d1b97
branch: agents/ots-native-selection-rust-correction-20260804
pr: none
status: waiting
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
  - Current correspondence still pins superseded profile-oriented Platform and Otheryn revisions.
  - Active Canary work owns only protocol-canary and Canary-specific evidence/tests; shared_path_lease is empty.
  - protocol-oteryn remains an independent target path and is not currently owned.
  - Existing Tokio transport remains protocol-neutral and is the required transport runtime.
  - Production activation is not authorized.
derived:
  - Rust correspondence cannot finalize until both prior mandatory correspondence merges expose immutable commits.
unknown:
  - Exact corrected Platform and Otheryn merge commits and schema SHA-256.
conflicts: []
first_failure:
  marker: none
  evidence: none
rejected_hypotheses:
  - Add a native profile enum, catalogue, factory, map or ForceOteryn(profile).
  - Translate native semantics through protocol-canary.
  - Switch adapters after ticket redeem or session failure.
changed_paths:
  - oteryn-client/docs/agents/tasks/active/OTC2-20260805-native-protocol-single-version-completion.md
validation:
  - command: live ownership, lease and open-PR preflight
    result: PASS
    evidence: protocol-oteryn is free and protocol-canary remains isolated with no shared lease
blockers:
  - Platform PR #540 and Otheryn PR #365 must merge first
next_action: After Platform and Otheryn correspondence merges, update Rust correspondence to both exact commits and corrected schema digest.
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: OTS-20260805T1308+0200-rust-correspondence
  session_started_at: 2026-08-05T13:08:00+02:00
  checkpointed_at: 2026-08-05T13:08:00+02:00
  last_progress_at: 2026-08-05T13:08:00+02:00
  phase: wait-for-platform-and-otheryn-correspondence
  exact_head: d1cd2c8502ef3363d1a104f0694fd1c7d15d1b97
  pull_request: none
  active_operation: none
  external_run_ids: []
  operation_started_at: null
  wait_deadline_at: null
  check_generation: draft
  checks_used: 0
  status: waiting
  safe_to_resume: true
  resume_condition: Platform PR #540 and Otheryn PR #365 are merged
  next_action: Update Rust correspondence to exact merged Platform and Otheryn revisions.
```
