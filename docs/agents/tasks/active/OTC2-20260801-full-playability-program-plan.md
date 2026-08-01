---
task_id: OTC2-20260801-full-playability-program-plan
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: full-playability-program
phase: validation
branch: docs/OTC2-20260801-full-playability-program-plan
base_branch: main
created: 2026-08-01T15:38:00+02:00
updated: 2026-08-01T16:55:00+02:00
last_verified_commit: "f8e15c5a1aed6a01a52904da8cb8b1b93e595a99"
required_base_commit: "02c7ac4b1d5bf1d37c20694bad45e830e430e822"
risk: high
related_pr: 135
depends_on:
  - merged W7 technical-login runtime and lifecycle archive
  - merged post-W7 remediations R1/R2/R4/R3
  - closure audit PR #133 merge 958881038ca5a5bc2f25a878a898ab5446d5e5c4
  - closure audit archive PR #134 merge 7596a792fbf747609a65e9fc35678b800b2d56e2
  - secret-owner completion PR #136 merge 78567eaefb1f6a827ffa1bff3be6d4aa370ba858
  - secret-owner archive PR #137 merge 02c7ac4b1d5bf1d37c20694bad45e830e430e822
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P0_DISCOVERY.md
  - oteryn-client/docs/agents/prompts/PLAYABILITY_COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_CANARY_CAPABILITY_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_LEGACY_PARITY_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_ASSET_PIPELINE_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_UX_INPUT_AUDIO_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_RELEASE_E2E_AGENT.md
shared_path_lease: []
modules_touched: []
crates_touched: []
features_touched:
  - definition of functional playability and parity
  - architecture handoff for future workers
  - multi-wave dependency and parallelism model
  - first bounded parallel discovery wave
contracts_produced:
  - full-playability programme charter
  - capability status vocabulary and parity matrix
  - first discovery-wave ownership and prompts
contracts_consumed:
  - normative Rust client architecture
  - W7 technical-login architecture and merged implementation
  - post-W7 audit and accepted remediations
  - prompting standard and context handoff
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: chat-github-connector
execution_reason: live repository inspection and a bounded documentation/prompt package without checkout-based implementation
context_pressure: high
context_growth: stable
context_score: 12
estimate_confidence: high
decomposition_decision: discovery_first
decomposition_reason: full client parity is too broad to authorize safely until independent protocol, legacy-behaviour, asset, UX and release evidence is normalized into one capability matrix
validation_level: focused
heavy_validation_runs: 1
session_rotation_count: 0
---

# Goal

Turn the owner's broad objective—an Oteryn Rust client that is fully playable with user-visible capability parity to the original Tibia client for features supported by the project-owned Oteryn/Canary target—into a durable, architecture-compliant multi-agent programme.

The planning package defines measurable milestones, current capability status, missing contract producers, serialization boundaries, safe parallel work, exact first-wave outputs and ready-to-paste worker prompts. It does not authorize gameplay implementation.

# Product interpretation

- Target server ecosystem: project-owned Oteryn Platform, Gateway and Canary compatibility; not official Tibia service compatibility.
- Target client: original Rust implementation under `oteryn-client/`; legacy C++/Lua/OTUI remains read-only behavioural evidence.
- Initial production platform: Windows desktop.
- Parity means functional user capability for supported Oteryn/Canary features, not copying proprietary assets, branding, code or exact visual presentation.
- Official or third-party assets may not enter Git without explicit rights. Local import and redistribution are separate contracts.

# Launch gate

The post-remediation audit, its archive and the audited secret-owner follow-up are merged. No P0 worker may start until:

1. audit PR #133, audit archive PR #134, secret-owner PR #136 and archive PR #137 remain merged on the exact base;
2. this planning PR and its separate lifecycle archive are merged;
3. a fresh coordinator preflight confirms no active task/PR/path conflict;
4. each worker creates one task, one branch and one draft PR with exclusive owned paths.

# Acceptance

- [x] `PROGRAM_CHARTER.md` defines scope, exclusions, evidence vocabulary and measurable milestones from technical login to production parity.
- [x] `ARCHITECTURE_HANDOFF.md` gives future agents one compact normative map of crate ownership, dependency direction, trust boundaries and non-negotiable invariants.
- [x] `CAPABILITY_MATRIX.md` records current proven/partial/absent/unknown state and the next owning producer for every major gameplay/product capability.
- [x] `DEPENDENCY_AND_PARALLELISM.md` defines sole contract producers, shared-path leases, merge order, barrier rules and safe concurrent workstreams.
- [x] `WAVE_P0_DISCOVERY.md` authorizes only independent discovery packages and one aggregation barrier; no implementation.
- [x] Every prompt follows `PROMPTING_STANDARD.md`, including role/phase, live state, objective, scope, reads/ownership, policy v2, execution, validation, durable state, stop conditions and compact final response.
- [x] Existing W1-W7 prompts are not relaunched.
- [x] No Rust source, manifest, lockfile, workflow, architecture checker, legacy runtime path, producer repository or PR #23-owned shared file remains in the diff.
- [x] Exact changed-path review is limited to the twelve declared documentation paths; required repository CI runs on this final checkpoint head.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T16:55:00+02:00
head: f8e15c5a1aed6a01a52904da8cb8b1b93e595a99
branch: docs/OTC2-20260801-full-playability-program-plan
pr: 135
status: validating
phase: validation
context_routes:
  - docs/agents/PROMPTING_STANDARD.md
  - docs/agents/PROMPTING_HANDOVER.md
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/architecture/ARCHITECTURE.md
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
  - oteryn-client/docs/audits/post-w7/main-audit-report.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md
  - oteryn-client/docs/agents/playability/**
  - oteryn-client/docs/agents/prompts/PLAYABILITY_COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_*_AGENT.md
proven:
  - Current main is 02c7ac4b1d5bf1d37c20694bad45e830e430e822.
  - W7 provides a synthetic technical-login composition but no minimum playable gameplay slice.
  - R1, R2, R4 and R3 remediations are merged and archived.
  - Audit PR #133, audit archive PR #134, secret-owner completion PR #136 and archive PR #137 are merged.
  - The plan contains twelve declared documentation paths and no implementation or shared PR #23 path.
  - Every P0 prompt contains the mandatory Prompting Standard sections and explicit implementation prohibition.
derived:
  - The safe next package is a discovery-first programme definition with independent inventories before gameplay implementation.
  - Parallel implementation can begin only after sole public contracts and shared-path leases are explicitly assigned.
unknown:
  - Exact complete Canary post-admission capability surface and sanitized fixture availability.
  - Exact functional parity inventory required by the chosen Oteryn product release.
  - Production asset source, rights and deployment contract.
  - Interactive Windows and real staging acceptance state.
conflicts: []
first_failure:
  marker: resolved-stale-status
  evidence: programme documents and prompts are written; stale audit/residual status and checkpoint schema were normalized to current main.
rejected_hypotheses:
  - Launch all gameplay agents immediately: rejected because shared domain/protocol/UI contracts and parity acceptance are not yet normalized.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/playability/DEPENDENCY_AND_PARALLELISM.md
  - oteryn-client/docs/agents/playability/WAVE_P0_DISCOVERY.md
  - oteryn-client/docs/agents/prompts/PLAYABILITY_COORDINATOR_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_CANARY_CAPABILITY_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_LEGACY_PARITY_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_ASSET_PIPELINE_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_UX_INPUT_AUDIO_AGENT.md
  - oteryn-client/docs/agents/prompts/P0_RELEASE_E2E_AGENT.md
validation:
  - command: programme document and Prompting Standard review
    result: PASS
    evidence: twelve declared documentation paths; implementation remains unauthorized and each worker prompt contains required bounded sections.
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md --require-checkpoint
    result: PASS
    evidence: refresh workflow run 30704758539.
blockers:
  - P0 worker launch waits for this planning PR and its separate lifecycle archive.
next_action: Complete exact-head CI and clean review for PR #135, merge and archive the plan, then run a fresh P0 coordinator launch preflight.
```
