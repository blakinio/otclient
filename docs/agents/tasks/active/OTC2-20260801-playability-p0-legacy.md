---
task_id: OTC2-20260801-playability-p0-legacy
status: active
agent: "P0 legacy parity worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0-legacy
phase: validation
branch: docs/OTC2-20260801-playability-p0-legacy
base_branch: main
created: 2026-08-01T19:00:00+02:00
updated: 2026-08-01T19:43:00+02:00
last_verified_commit: "36502add612ee3ff4d2a34e4a7bdca132d9e8f28"
required_base_commit: "17f2a4bf86563609e6f9edb4c71ca40fbbda59b2"
risk: medium
related_pr: 141
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-legacy.md
  - oteryn-client/docs/research/playability/p0/legacy-user-workflow-inventory.md
  - oteryn-client/docs/research/playability/p0/parity-scenario-catalogue.md
shared_path_lease: []
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: work
context_pressure: high
decomposition_decision: single
validation_level: focused
---

# Goal

Produce an evidence-backed catalogue of player-visible workflows and functional parity scenarios from the repository legacy client and approved original-client evidence without importing legacy architecture into the Rust design.

# Result

The lane produced:

- `legacy-user-workflow-inventory.md` — launch/auth/selection, visible world, movement, HUD, combat, inventory/containers, chat/NPC, action bars/settings, minimap/audio, relog/recovery, install/update and exact-profile feature-family outcomes;
- `parity-scenario-catalogue.md` — reusable M1-M6 scenarios with start state, actions, observables, negative/recovery variants, evidence classes and cross-lane dependencies.

Legacy module behavior is translated into user outcomes. Lua globals, OTUI widget IDs, module boundaries, password fallback, proprietary assets and automation are explicitly not parity requirements.

# Scope

Read-only inspection of maintained legacy architecture and representative `game_interface`, inventory, console and minimap modules. No legacy/Rust source, assets, binaries, PR #23 path or official service was modified/automated.

# Acceptance

- [x] major player journeys and recovery paths have exact evidence paths;
- [x] scenarios state preconditions, actions and observable outcomes;
- [x] core playability, daily-product and version-specific parity are separated;
- [x] server dependencies, unknowns and intentional non-parity recommendations are explicit;
- [ ] only the three owned paths change;
- [ ] checkpoint validator, independent document review and exact-head required CI pass.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T19:43:00+02:00
head: 36502add612ee3ff4d2a34e4a7bdca132d9e8f28
branch: docs/OTC2-20260801-playability-p0-legacy
pr: 141
status: validating
context_routes:
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/prompts/P0_LEGACY_PARITY_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-legacy.md
  - oteryn-client/docs/research/playability/p0/legacy-user-workflow-inventory.md
  - oteryn-client/docs/research/playability/p0/parity-scenario-catalogue.md
proven:
  - Current restack target main is 9c03a448457b1715818e094fdfdeade4a1450434.
  - Maintained legacy architecture makes the legacy client behavior evidence, never a Rust runtime dependency.
  - game_interface owns observable viewport/panel/focus/geometry/logout lifecycle in the legacy product.
  - inventory exposes equipment slots and combat posture/fight/chase presentation.
  - console distinguishes local/private/channel/NPC/monster communication semantics.
  - minimap follows local position, camera/cross position, floor and persisted map behavior.
  - The reports normalize M1-M6 outcomes, recovery and evidence without copying Lua/OTUI architecture.
derived:
  - Core playability requires M1 entry plus M2 visible world/movement/logout; ordinary hunting/interactions require M3.
  - Daily-product UI/settings/minimap/recovery/install behavior belongs primarily to M4.
  - Version-specific systems remain conditional on PR #140 and product classification.
unknown:
  - Exact release-required workflow/feature set for the chosen Oteryn/Canary profile.
  - Exact producer support and protocol semantics for many M5 feature families.
  - Final intentional non-parity/product UX decisions.
conflicts: []
first_failure:
  marker: none
  evidence: discovery completed without ownership or evidence conflict.
rejected_hypotheses:
  - Treat legacy module boundaries as Rust architecture: rejected because only observable behaviour is evidence.
  - Treat feature presence in legacy modules as selected release scope: rejected pending exact server support and owner classification.
  - Copy password fallback, globals, OTUI layouts or bot/automation behavior: rejected for security, architecture, legal and product reasons.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-legacy.md
  - oteryn-client/docs/research/playability/p0/legacy-user-workflow-inventory.md
  - oteryn-client/docs/research/playability/p0/parity-scenario-catalogue.md
validation:
  - command: live ownership and launch-gate preflight
    result: PASS
    evidence: PR #23 paths are disjoint/read-only and no shared lease exists.
  - command: representative legacy behavior evidence review
    result: PASS
    evidence: maintained architecture plus game_interface, inventory, console and minimap paths support the documented observable seams.
  - command: architecture/legal/unsupported-claims review
    result: PASS
    evidence: reports separate behavior from implementation, conditional server scope from legacy presence and exclude proprietary content/official-service automation.
blockers:
  - Final release-required/deferred scenario classification requires P0 aggregation and owner decisions.
  - Exact-profile scenarios require producer evidence from PR #140.
  - Asset/UI/runtime acceptance depends on PR #142/#143/#144 outputs.
next_action: Run exact-head validation and clean review for PR #141, then merge and archive the legacy discovery lane.
```
