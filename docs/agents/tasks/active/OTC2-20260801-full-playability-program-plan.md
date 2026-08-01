---
task_id: OTC2-20260801-full-playability-program-plan
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: full-playability-program
phase: design
branch: docs/OTC2-20260801-full-playability-program-plan
base_branch: main
created: 2026-08-01T15:38:00+02:00
updated: 2026-08-01T15:38:00+02:00
last_verified_commit: "67a6c9d726f7e70977803b028270475570210db0"
required_base_commit: "67a6c9d726f7e70977803b028270475570210db0"
risk: high
related_pr: null
depends_on:
  - merged W7 technical-login runtime and lifecycle archive
  - merged post-W7 remediations R1/R2/R4/R3
  - closure audit task OTC2-20260801-post-remediation-closure-audit before worker launch
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
heavy_validation_runs: 0
session_rotation_count: 0
---

# Goal

Turn the owner's broad objective—an Oteryn Rust client that is fully playable with user-visible capability parity to the original Tibia client for features supported by the project-owned Oteryn/Canary target—into a durable, architecture-compliant multi-agent programme.

The planning package must define measurable milestones, current capability status, missing contract producers, serialization boundaries, safe parallel work, exact first-wave outputs and ready-to-paste worker prompts. It does not authorize gameplay implementation.

# Product interpretation

- Target server ecosystem: project-owned Oteryn Platform, Gateway and Canary compatibility; not official Tibia service compatibility.
- Target client: original Rust implementation under `oteryn-client/`; legacy C++/Lua/OTUI remains read-only behavioural evidence.
- Initial production platform: Windows desktop.
- Parity means functional user capability for supported Oteryn/Canary features, not copying proprietary assets, branding, code or exact visual presentation.
- Official or third-party assets may not enter Git without explicit rights. Local import and redistribution are separate contracts.

# Launch gate

The programme documents may be reviewed while PR #133 performs the independent post-remediation closure audit. No P0 worker may start until:

1. the closure audit and its lifecycle archive are merged;
2. this planning PR and its separate lifecycle archive are merged;
3. a fresh coordinator preflight confirms no active task/PR/path conflict;
4. each worker creates one task, one branch and one draft PR with exclusive owned paths.

# Acceptance

- [ ] `PROGRAM_CHARTER.md` defines scope, exclusions, evidence vocabulary and measurable milestones from technical login to production parity.
- [ ] `ARCHITECTURE_HANDOFF.md` gives future agents one compact normative map of crate ownership, dependency direction, trust boundaries and non-negotiable invariants.
- [ ] `CAPABILITY_MATRIX.md` records current proven/partial/absent/unknown state and the next owning producer for every major gameplay/product capability.
- [ ] `DEPENDENCY_AND_PARALLELISM.md` defines sole contract producers, shared-path leases, merge order, barrier rules and safe concurrent workstreams.
- [ ] `WAVE_P0_DISCOVERY.md` authorizes only independent discovery packages and one aggregation barrier; no implementation.
- [ ] Every prompt follows `PROMPTING_STANDARD.md`, including role/phase, live state, objective, scope, reads/ownership, policy v2, execution, validation, durable state, stop conditions and compact final response.
- [ ] Existing W1-W7 prompts are not relaunched.
- [ ] No Rust source, manifest, lockfile, workflow, architecture checker, legacy runtime path, producer repository or PR #23-owned shared file is changed.
- [ ] Exact changed-path review and required repository CI pass on the final head.

# Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T15:38:00+02:00
head: 67a6c9d726f7e70977803b028270475570210db0
branch: docs/OTC2-20260801-full-playability-program-plan
pr: none
status: active
phase: design
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
  - Current main is 67a6c9d726f7e70977803b028270475570210db0.
  - W7 provides a synthetic technical-login composition but no minimum playable gameplay slice.
  - R1, R2, R4 and R3 remediations are merged and archived.
  - PR #133 independently audits remediation closure and owns only its audit task/report paths.
  - Open PRs #23, #48 and #97 do not own the proposed playability planning paths.
  - Prompting Standard requires bounded task shapes, staged validation and durable checkpoints.
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
  marker: none
  evidence: planning package not yet written
rejected_hypotheses:
  - Launch all gameplay agents immediately: rejected because shared domain/protocol/UI contracts and parity acceptance are not yet normalized.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-full-playability-program-plan.md
validation: []
blockers:
  - P0 worker launch waits for PR #133 and its archive plus this plan/archive.
next_action: Write the normative programme charter, architecture handoff, capability matrix, parallelism plan and bounded P0 prompts.
```
