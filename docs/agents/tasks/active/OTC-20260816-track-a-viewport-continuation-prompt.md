---
task_id: OTC-20260816-track-a-viewport-continuation-prompt
status: validating
project_lane: otclient
track_id: official-client-re
task_kind: documentation
phase: validate
branch: docs/OTC-20260816-track-a-viewport-continuation-prompt
base_branch: main
base_head: 19556a5bca362dede3f9c2608902eda6e358b2bc
pull_request: 363
policy_version: 2
prompting_standard_version: 2.1
execution_mode: chat_github_connector
run_scope: single_task
continuation_policy: stop_at_task_boundary
task_completion_policy: finalize_archive_and_continue
implementation_authorized: false
owned_paths:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_VIEWPORT_CONTINUATION.md
  - docs/agents/tasks/active/OTC-20260816-track-a-viewport-continuation-prompt.md
  - docs/agents/tasks/archive/OTC-20260816-track-a-viewport-continuation-prompt.md
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - PR #325 official-client viewport feasibility research checkpoint
depends_on:
  - PR #325 for the persisted viewport feasibility report/evidence; prompt remains usable read-only against #325 if it has not merged yet
blocks: []
---

# Objective

Persist one ready-to-paste continuation prompt for the official-client worldmap viewport investigation, including the owner's stricter execution routing and GUI-session reuse constraint, so a fresh worker can continue without chat history.

# Durable owner constraint

```yaml
static_execution: github_hosted_first
gui_host: synology_only
gui_session_policy: reuse_existing_logged_in_session_only
create_new_desktop: forbidden
create_new_x11_display: forbidden
create_new_vnc_or_novnc_desktop: forbidden
create_parallel_logged_in_tibia_session: forbidden
change_desktop_version_or_configuration: forbidden
when_safe_reuse_is_unavailable: waiting_or_blocked
```

Interpretation:

- Static/artifact/binary analysis runs on GitHub-hosted Actions by default.
- Synology is reserved for genuinely GUI/runtime-dependent work.
- If GUI is required, use the already existing logged-in Track A desktop/session when current ownership/admission permits.
- Do not create another desktop/session/display/VNC environment and do not re-login from zero merely because reuse is inconvenient.
- Do not steal another active agent's runtime ownership; Gate A / required rebind / Gate B / uniqueness and the current supervisor contract still apply.
- If the existing GUI session cannot be safely reused, the runtime step is WAITING/BLOCKED rather than a bootstrap/new-desktop task.

# Research state carried into the prompt

The continuation prompt preserves the following bounded state from the viewport investigation:

```yaml
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
static_run: 31892019505
static_artifact: 9248797952
static_artifact_digest: sha256:04835ab0bac7ffc43e161e8b2118c90a3d2197f7011385a6758cd7706c93a584
map_capture_lead: PIE+0x19a8ea3
historical_reversible_run: 31806312967
historical_reversible_job: 94785974126
historical_reversible_artifact: 9221332209
baseline_geometry_claim: DERIVED_18_x_14
larger_viewport_claim: DERIVED_HIGH_CONFIDENCE_FEASIBILITY_NOT_IMPLEMENTED
```

Named exact-binary surfaces carried forward:

```text
TWorldMapExtent
TWorldMapSubfieldExtent
TWorldMapStorage
TWorldMapViewport
TWorldMapCamera
TWorldmapProtocolMessageHandler
TWorldMapRenderProvider
TWorldMapPicker
onCameraViewportChanged
TMapScaleFactor / MapScaleFactor
TWorldMapExtentX
```

# Bounded next task encoded in prompt

The worker must remain static-first and recover:

1. xrefs/typeinfo/vtables/constructors for extent/subfield extent/viewport;
2. candidate dimension fields/default writes and all material readers/writers;
3. dependency flow through storage, protocol handler, renderer, camera and picker;
4. fixed arrays, allocation sizes, loop bounds, parser assumptions, clipping/culling and coordinate limits;
5. a durable patch/dependency graph with PROVEN / DERIVED / UNKNOWN / CONFLICT classifications;
6. one final static disposition: `STATIC_PATCH_GRAPH_READY`, `MORE_STATIC_RE_NEEDED`, `RUNTIME_DISCRIMINATOR_REQUIRED` or `BLOCKED`.

No client-byte mutation or live runtime is authorized by this prompt's initial phase.

# Related PR state

- PR #325 contains the viewport feasibility report/evidence and had exact-head required CI success before this handoff was created, but its final merge state must be re-read by the next worker.
- A manual merge attempt returned branch-protection status `Required status check "CI / Required" is expected` despite the successful run; do not bypass protections. Re-read live state rather than treating this transient closeout condition as research evidence.

# Acceptance

- Prompt exists at `docs/agents/prompts/OTCLIENT_TIBIA_RE_VIEWPORT_CONTINUATION.md`.
- It is self-contained enough for a fresh worker while requiring live-state revalidation.
- It records the exact client fence and known viewport evidence without upgrading inference to fact.
- It makes GitHub-hosted static execution the default.
- It encodes Synology GUI reuse-only behavior and explicitly forbids creation/reconfiguration of a replacement desktop/session.
- It preserves Track A ownership/admission rules and does not authorize runtime mutation.
- It does not use owner-funded Codex/OpenAI API quota or owner-owned AI credentials/tokens.
- Final CI/PR closeout must pass before this documentation task is completed.

# Fresh audit

Exact PR #363 two-file diff was re-read against trusted-base Track A governance and the canonical wrapper.

```yaml
audit:
  result: PASS
  material_findings_open: 0
  prompt_expands_runtime_authority: false
  static_github_hosted_first: true
  gui_synology_only: true
  existing_gui_session_reuse_only: true
  new_gui_session_forbidden: true
  desktop_reconfiguration_forbidden: true
  gate_a_rebind_gate_b_preserved: true
  owner_funded_ai_used: false
  proprietary_or_secret_material_added: false
```

The owner GUI rule is stricter than the general runtime model and therefore narrows this viewport task. It does not grant permission to seize or reuse an active session without current ownership/admission.

# Validation checkpoint

```yaml
focused_review:
  prompt_self_contained: true
  owner_gui_constraint_recorded: true
  exact_client_fence_recorded: true
  runtime_mutation_authorized: false
  owner_funded_ai_used: false
fresh_audit: PASS
exact_head_ci: pending
pr_terminal: pending
```

# Next action

Mark PR #363 ready for review, run required exact-head CI, then merge/archive through normal repository protection if all checks remain green.