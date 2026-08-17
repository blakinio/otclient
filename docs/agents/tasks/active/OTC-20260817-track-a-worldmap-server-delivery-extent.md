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
updated: 2026-08-17T12:51:28+02:00
risk: medium
related_pr: 473
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-worldmap-server-delivery-extent.md
  - docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/
  - docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-extent.md
  - .github/workflows/track-a-worldmap-server-delivery-static.yml
modules_touched:
  - agent-evidence
  - github-actions-temporary
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
invocation_started_at: 2026-08-17T12:45:00+02:00
last_progress_at: 2026-08-17T12:51:28+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
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
- Draft PR #473 is the sole current task PR.

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
- [ ] Trace exact-client `FullMap`/map-description and directional/floor-change delivery surfaces as far as canonical evidence permits.
- [ ] Determine whether any exact official-client path negotiates/requests aware range or width/height.
- [ ] Search bounded parser/network evidence for width/height, strip/floor counts, coordinate or length ceilings.
- [ ] Record bounded negative evidence rather than global impossibility claims.
- [ ] Design one separately-authorized runtime discriminator if static evidence cannot distinguish server transmission from client-local storage/render growth.
- [ ] Fresh independent documentation/evidence audit with zero material findings or an explicit blocker.
- [ ] Exact-head changed-file audit, required CI, review hygiene and terminal task lifecycle.

# Evidence checkpoint

## PROVEN

- Exact official Linux client fence: version `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Accepted client-local geometry chain starts from packed `18/14` and propagates through exact `TWorldmapProtocolMessageHandler` to Storage; Viewport/RenderProvider/Picker are separate downstream dependencies.
- Previous physical `[19,14]` canary proved patched-copy startup only; no accepted worldmap object instance was present in its no-login startup census.
- Historical exact-client protocol inventory run `31651220862`, job `94295767215`, recovered 349 generated message names total: 160 client->server and 189 server->client. Its deliberately filtered 98-name output includes `GameserverMessageFullMap`, `GameserverMessageFieldData`, map mutations and movement messages, but the job did not print the other 251 names.

## BOUNDED NEGATIVE / GAP

- The filtered output contains no visible client->server map-range/extent negotiation message, but this is not yet an admissible absence claim because 251 message names were not printed.
- Accepted second-pack worldmap evidence records `network_payload_extent_ceiling=NOT_RECOVERED` and `complete_handler_master_pair_writer_census=UNKNOWN`.

## UNKNOWN

- Server delivery model (`CLIENT_DRIVEN|SERVER_DRIVEN|NEGOTIATED|FIXED_PROTOCOL|UNKNOWN`).
- Whether changing the client-local 18/14 pair causes additional authoritative tiles to arrive.
- Larger rectangle/full-floor/multi-floor/whole-map delivery support and any maximum extent.
- Any exact parser/network ceiling not yet recovered.

# Producer decision

Existing retained evidence is insufficient to classify negotiation because the only complete protocol-symbol run printed a filtered subset. Under `GITHUB_ONLY_EXECUTION.md`, one minimal temporary branch-only workflow is justified. It will fetch the exact SHA-fenced public Linux client through the already-proven hosted WARP method, produce a complete generated-message census plus bounded map/range/extent string evidence, and retain only text evidence. It must be removed before terminal merge.

# Checkpoint

```yaml
checkpoint_version: 2
updated_at: 2026-08-17T12:51:28+02:00
base_main: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
branch: research/OTC-20260817-track-a-worldmap-server-delivery-extent
pr: 473
status: investigating
phase: server-delivery-static-analysis
runtime_access: none
last_completed_step: confirmed the 349-message protocol census and isolated its 98-name filtered-output gap
validation_level: focused
heavy_validation_runs: 0
session_rotation_count: 0
blockers: []
next_action: Add and run the minimal temporary GitHub-hosted exact-client census workflow, then classify its direct evidence before any deeper producer is considered.
```