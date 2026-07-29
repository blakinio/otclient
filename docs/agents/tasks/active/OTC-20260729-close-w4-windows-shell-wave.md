---
task_id: OTC-20260729-close-w4-windows-shell-wave
status: in_progress
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: coordination
parallel_wave: OTERYN-W4-WINDOWS-SHELL
parallel_lane: W4-C
parallel_lane_state: active
branch: docs/OTC-20260729-close-w4-windows-shell-wave
base_branch: main
created: 2026-07-29T12:38:00+02:00
updated: 2026-07-29T12:38:00+02:00
last_verified_commit: "ab0ac39ca70ccea6d8f7517f4119395de6b17017"
required_base_commit: "ab0ac39ca70ccea6d8f7517f4119395de6b17017"
risk: low
related_pr: pending
depends_on:
  - W4 plan PR #77 and archive PR #78
  - W4 implementation PR #79 and archive PR #80
owned_paths:
  - oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md
  - oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md
  - docs/agents/README.md
  - docs/agents/tasks/active/OTC-20260729-close-w4-windows-shell-wave.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - merged Windows application-shell contract from PR #79
  - merged W4 runtime evidence
crates_touched: []
features_touched: []
contracts_touched:
  - completed W4 status and future launch routing only
modules_touched: []
reuses:
  - archived W4 task records and exact CI evidence
  - merged application-shell public contract
  - W4 runtime evidence blockers
public_interfaces:
  - coordination documentation only
cross_repo_tasks: []
performance_evidence:
  - no runtime, GPU or performance claim
security_evidence:
  - no secrets, assets, captures, dependencies or external-repository writes
---

# Goal

Close `OTERYN-W4-WINDOWS-SHELL` durably, prevent its relaunch, prove every lease is released and leave exactly one next bounded recommendation without implementing or pre-claiming it.

# Acceptance criteria

- [ ] W4 plan and implementation are recorded as merged and archived with exact evidence.
- [ ] No W4 lane remains launchable and no W4 shared-path lease remains active.
- [ ] Current routing no longer instructs agents to launch W4.
- [ ] Open unrelated legacy/operational PRs remain distinguished from Rust ownership.
- [ ] Exactly one next bounded package is recommended from merged evidence.
- [ ] The next package is not implemented, tasked, branched or leased here.
- [ ] Interactive Windows compatibility blockers remain explicit.
- [ ] No Rust source, Cargo, lockfile, dependency policy, CI, architecture, protocol, asset, legacy runtime or external-repository change.
- [ ] Exact-head required CI passes; closure merges and archives separately.

# Confirmed live state

- Current `main`: `ab0ac39ca70ccea6d8f7517f4119395de6b17017`.
- W4 plan/archive: PR #77 merge `7ff7a80df15dd22178c3a1920cc3714216c91ac6`; PR #78 archive `b16e0a8c17cf1ce7b0808ef577cce0d5bc76f0b3`.
- W4 implementation/archive: PR #79 merge `00ad2729aab3696ca4571fd718ef1b350747e3b5`; PR #80 archive `ab0ac39ca70ccea6d8f7517f4119395de6b17017`.
- W4 Cargo/lockfile/dependency-policy/shared-document lease is released.
- Open PRs #23 and #37 remain legacy-only; PR #48 remains isolated operational non-merge work.

# Exactly one next recommendation

Recommend one bounded **renderer surface-ownership evidence/spike** only after a separate fresh plan.

Required envelope:

- consume the merged application-shell window/lifecycle contract without weakening its deterministic close path;
- establish only renderer instance/adapter/device/surface ownership and clear/present lifecycle with original synthetic content;
- fresh primary-source dependency/version/license/MSRV/advisory review before Cargo changes;
- no game rendering, map/entity extraction, textures/assets, shader system, UI, protocol, identity, networking, audio, persistence or extension runtime;
- no global renderer singleton or background scheduler;
- deterministic CPU-side surface state tests and explicit device-loss/zero-size/suspend/shutdown behavior;
- interactive GPU/hardware/driver/performance evidence marked `BLOCKED` unless genuinely observed on a named environment;
- one unique Cargo/lockfile/dependency-policy/shared-document lease after a separate accepted plan.

This recommendation is not an accepted wave and is not pre-claimed.

# Completion

- Final status: in progress
- PR: pending
- Merge commit: pending
- Archived at: pending
