---
task_id: OTC-20260817-track-a-worldmap-server-delivery-extent
status: investigating
agent: ChatGPT
project_lane: otclient
lane: official-client-re
track: official-client-re
task_kind: discovery
phase: server-delivery-static-analysis
branch: research/OTC-20260817-track-a-worldmap-server-delivery-extent
base_branch: main
base_sha: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
created: 2026-08-17T12:45:00+02:00
updated: 2026-08-17T12:45:00+02:00
risk: medium
related_pr: pending
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-server-delivery-extent.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-extent.md
modules_touched:
  - agent-evidence
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_WORLDMAP_MUTATION_DESIGN.md
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
  - docs/agents/reports/OTCLIENT-20260817-worldmap-mutation-design.md
  - merged PRs #367, #437, #446, #452, #462
policy_version: 2
prompting_standard_version: 2.1
execution_mode: github-only
execution_reason: Static/evidence analysis and durable documentation do not require owner-funded AI or physical runtime access.
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_continue
user_communication: low_noise
context_pressure: high
context_growth: stable
context_score: 10
estimate_confidence: medium
decomposition_decision: phased
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
client_byte_mutation_authorized: false
owner_funded_ai_api_authorized: false
---

# Objective

Resolve the server-delivered worldmap extent acceptance added by prompt contract v1.1.0 without repeating completed worldmap mutation design and without entering physical runtime. Determine from exact-client/canonical evidence how normal gameplay map data is delivered, what larger/full-floor/multi-floor/whole-map claims are directly supportable, and what remains `UNKNOWN`. Produce the smallest separately-authorized runtime discriminator only where static evidence cannot decide semantics.

# Authority and boundaries

Trusted base is `main@f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b` plus current repository governance. This task is GitHub-hosted/static only.

Forbidden in this task:

- official-client byte mutation;
- physical/canonical runtime access, login, relogin or gameplay;
- Synology as static-analysis fallback;
- owner-funded Codex/OpenAI API/paid AI quota;
- raw official-client binary promotion into Git;
- treating third-party OTClient behavior as proof of official-server behavior.

# Live-state preflight

- `main` exact head at claim: `f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b` (merged PR #472, prompt v1.1.0).
- PR #471 merged the durable alias/handover; #472 merged the server-delivered-map-extent acceptance extension.
- Prior mutation-design task #452/#453 is terminal and must not be recreated.
- Prior physical startup-canary #462/#466 is terminal; it proved patched-copy startup only and did not establish IN_GAME semantics or causal worldmap object propagation.
- No open PR matching `worldmap extent` and no existing `worldmap-server` branch was found at claim time.

# Acceptance inventory

Persist direct-evidence classifications for:

```text
SERVER_MAP_DELIVERY_MODEL=CLIENT_DRIVEN|SERVER_DRIVEN|NEGOTIATED|FIXED_PROTOCOL|UNKNOWN
SERVER_LARGER_RECTANGLE_SUPPORTED=true|false|UNKNOWN
SERVER_FULL_FLOOR_DELIVERY_SUPPORTED=true|false|UNKNOWN
SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED=true|false|UNKNOWN
SERVER_WHOLE_MAP_DELIVERY_SUPPORTED=true|false|UNKNOWN
MAX_SERVER_DELIVERABLE_EXTENT=<proven bound or UNKNOWN>
```

Also:

- [ ] Separate client Storage capacity, render/viewport extent and server-delivered protocol extent.
- [ ] Trace exact-client `FullMap`/map-description and directional/floor-change delivery surfaces as far as available canonical evidence permits.
- [ ] Determine whether any exact official-client path negotiates/requests aware range or width/height.
- [ ] Search bounded parser/network evidence for width/height, strip/floor counts, coordinate or length ceilings.
- [ ] Record bounded negative evidence rather than global impossibility claims.
- [ ] Design one separately-authorized runtime discriminator if static evidence cannot distinguish server transmission from client-local storage/render growth.
- [ ] Fresh independent documentation/evidence audit with zero material findings or an explicit blocker.
- [ ] Exact-head changed-file audit, required CI, review hygiene and terminal task lifecycle.

# Current evidence boundary

## PROVEN

- Exact official Linux client fence remains version `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` in the accepted worldmap static/design records.
- Accepted client-local geometry chain starts from packed `18/14` and propagates through the exact worldmap protocol handler to Storage; Viewport/RenderProvider/Picker are separate downstream dependencies.
- Previous physical `[19,14]` canary proved only patched-copy startup in a no-login lifecycle; no accepted worldmap object instance was present in that startup census.

## UNKNOWN

- Whether the server map-delivery model is client-driven, server-driven, negotiated or fixed-protocol.
- Whether increasing the client-local pair causes additional authoritative tiles to arrive.
- Larger rectangle/full-floor/multi-floor/whole-map delivery support and any maximum extent.
- Any parser/network ceiling not already proven by exact-client evidence.

# Checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-17T12:45:00+02:00
base_main: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
branch: research/OTC-20260817-track-a-worldmap-server-delivery-extent
status: investigating
phase: server-delivery-static-analysis
runtime_access: none
last_completed_step: live-state resolution and task claim
validation_level: focused
heavy_validation_runs: 0
session_rotation_count: 0
blockers: []
next_action: Inspect canonical exact-client worldmap/protocol evidence and existing static artifacts for FullMap/map-description/directional/floor-change delivery and any aware-range negotiation; if insufficient, prepare the smallest GitHub-hosted deterministic evidence producer.
```