---
task_id: OTC2-20260801-playability-p0-ux
status: active
agent: "P0 UX input audio worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0-ux
phase: validation
branch: docs/OTC2-20260801-playability-p0-ux
base_branch: main
created: 2026-08-01T19:02:00+02:00
updated: 2026-08-01T19:25:00+02:00
last_verified_commit: "2f1ffc78a681fff5c3ef0f1c6e984de6283faaa7"
required_base_commit: "17f2a4bf86563609e6f9edb4c71ca40fbbda59b2"
risk: medium
related_pr: 143
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-ux.md
  - oteryn-client/docs/research/playability/p0/windows-ux-input-audio-inventory.md
  - oteryn-client/docs/research/playability/p0/ui-feature-decomposition.md
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

Define native Windows presentation, semantic input, audio and accessibility requirements and decompose them into architecture-safe core contracts and independent feature packages.

# Result

The lane produced:

- `windows-ux-input-audio-inventory.md` — observable launch/login/selection/gameplay/panel/error workflows, Windows platform acceptance, normalized input contexts/bindings/capture, audio device/voice requirements, accessibility/localization and evidence ladder;
- `ui-feature-decomposition.md` — candidate sole producers for UI primitives, common view-model/actions, input, platform text/IME, audio and resources, followed by independent auth, HUD, inventory, chat, combat, action-bar, minimap and settings consumers.

The result preserves the current evidence boundary: shell/renderer state and hosted Windows compilation are proven, while real desktop launch, DPI, IME, clipboard, physical input, accessibility bridge, audio device behavior and product UI remain unproven or absent.

# Scope

Read-only investigation of Rust architecture, W4/W5 evidence and representative legacy UI ownership. No code, dependency, proprietary presentation/asset or PR #23 path was changed.

# Acceptance

- [x] login, selection, viewport, HUD, panels, modal/error and settings workflows have observable acceptance;
- [x] UI core, feature UI, input actions and audio intents have explicit ownership seams;
- [x] DPI, IME, focus, clipboard, capture, drag/drop, keyboard navigation and accessibility requirements are named;
- [x] synthetic/headless and interactive Windows evidence are separated;
- [ ] only the three owned paths change and exact-head required validation passes;
- [ ] checkpoint validator and independent review pass.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T19:25:00+02:00
head: 2f1ffc78a681fff5c3ef0f1c6e984de6283faaa7
branch: docs/OTC2-20260801-playability-p0-ux
pr: 143
status: validating
context_routes:
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/prompts/P0_UX_INPUT_AUDIO_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-ux.md
  - oteryn-client/docs/research/playability/p0/windows-ux-input-audio-inventory.md
  - oteryn-client/docs/research/playability/p0/ui-feature-decomposition.md
proven:
  - Current launch base is 17f2a4bf86563609e6f9edb4c71ca40fbbda59b2 and coordinator merge is 21f0725f0beb46775951dd17f2587c67ebcdee12.
  - Current shell owns one Windows event loop and deterministic focus/resize/scale/keyboard/mouse/IME event boundaries.
  - Current renderer owns deterministic surface lifecycle and a constant DX12 clear/present adapter.
  - Hosted Windows CI does not prove visible launch, physical input, DPI/IME, named GPU/driver or performance.
  - Normative architecture requires retained UI primitives, view models/semantic actions, normalized input and explicit audio ownership.
  - Legacy modules are behavioral evidence only and PR #23 paths remain read-only/disjoint.
  - Two reports define observable requirements, sole producers, consumer features, tests and interactive evidence boundaries.
derived:
  - P1 should establish narrow input, UI primitive/common-action and audio contract producers before broad feature screens.
  - Feature UI may proceed independently only after merged producer contracts and bounded synthetic fixtures exist.
  - Text/font/audio resource decisions depend on approved asset evidence from PR #142.
unknown:
  - Final native UI implementation strategy and Windows accessibility bridge.
  - Text shaping/font/localization and audio backend decisions.
  - Final default bindings, release-required feature panels and interactive Windows support matrix.
conflicts: []
first_failure:
  marker: none
  evidence: discovery completed without ownership or architecture conflict.
rejected_hypotheses:
  - Select and implement a UI framework during P0: rejected because this lane is requirements/decomposition only.
  - Copy legacy OTUI/module structure into Rust: rejected because only user-visible behavior is evidence.
  - Let features consume raw OS events or wire messages: rejected by normalized input/action and view-model boundaries.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-ux.md
  - oteryn-client/docs/research/playability/p0/windows-ux-input-audio-inventory.md
  - oteryn-client/docs/research/playability/p0/ui-feature-decomposition.md
validation:
  - command: live ownership and launch-gate preflight
    result: PASS
    evidence: PR #23 is disjoint and read-only; no shared lease exists.
  - command: architecture and current-evidence review
    result: PASS
    evidence: normative architecture, W4 shell, W5 renderer and legacy architecture boundaries were reconciled without strengthening runtime claims.
  - command: producer-consumer and unsupported-claims review
    result: PASS
    evidence: reports assign one producer per shared contract, keep product/library decisions explicit and separate headless from interactive evidence.
blockers:
  - Library, accessibility, shaping/font and audio-backend selections require later bounded producer decisions.
  - Interactive Windows compatibility requires named desktop, display/input/IME/accessibility/audio and GPU evidence.
  - Exact feature set/default bindings depend on PR #140/#141 and product owner classification.
next_action: Run exact-head validation and clean review for PR #143, then merge and archive the UX discovery lane.
```
