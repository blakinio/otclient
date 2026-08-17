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
updated: 2026-08-17T13:02:22+02:00
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
last_progress_at: 2026-08-17T13:02:22+02:00
ci_checks_for_current_head: 0
ci_check_generation: evidence-production
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
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
- [x] Separate client Storage capacity, render/viewport extent and server-delivered protocol extent in the evidence model.
- [x] Recover complete exact generated-message directionality for `FullMap`, field, directional row/column and floor-change families.
- [ ] Determine whether any exact official-client path negotiates/requests aware range or width/height, including generic outbound message fields.
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
- Historical exact-client protocol inventory run `31651220862`, job `94295767215`, recovered 349 generated message names total: 160 client->server and 189 server->client.
- New exact-client run `32022209943`, job `95364071999`, completed successfully and persisted the complete 349-name census in artifact `9285763750` (`worldmap-server-delivery-static-32022209943`).
- Complete outbound name-level census has no `aware|range|extent|viewport|fullmap|fielddata|width|height` generated message name.
- Complete inbound census directly contains `GameserverMessageFullMap`, `GameserverMessageFieldData`, `GameserverMessageLeftColumn`, `GameserverMessageRightColumn`, `GameserverMessageTopRow`, `GameserverMessageBottomRow`, `GameserverMessageTopFloor` and `GameserverMessageBottomFloor`.
- Exact binary strings additionally contain protocol concepts `Extent`, `MapFieldData`, `ColumnData`, `RowData`, `AdditionalRowsTop`, `AdditionalRowsBottom`, `Columns`, and `Rows`.
- Durable census evidence: `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-complete-message-census.md`.

## FAILED PRODUCER ATTEMPTS — DIAGNOSED, NOT RETRIED IDENTICALLY

- Descriptor run `32022548050`, job `95365067677`, head `888630af1de1d05be1f131df428360c9b4d215ba`: failed with `descriptor_file_count=0` / `no target protocol descriptors recovered`. Static inspection found a producer bug: it treated `FileDescriptorProto` field 6 as `message_type`; the correct field is 4.
- Descriptor run `32022815851`, job `95365868589`, head `57b3068a16fe4d0ee9255fe20bbed4a17f272b9f`: after correcting field 4, it still returned `descriptor_file_count=0`, proving the strict file-descriptor start heuristic remained invalid for this exact generated layout.
- No failed producer was rerun identically. The current repair abandons the file-start heuristic and anchors directly on exact `DescriptorProto` message-name encodings, while preserving bounded neighborhoods even on assertion failure.

## BOUNDED NEGATIVE / GAP

- Absence of a named outbound extent/range message is direct only at generated-message-name level. Generic messages (`ClientDetails`, `Login`, `SecondaryLogin`, `EnterWorld`, `SetClientOptions`) may still carry a negotiation field until their exact descriptors/handlers are bounded.
- Accepted second-pack worldmap evidence records `network_payload_extent_ceiling=NOT_RECOVERED` and `complete_handler_master_pair_writer_census=UNKNOWN`.

## UNKNOWN

- Server delivery model (`CLIENT_DRIVEN|SERVER_DRIVEN|NEGOTIATED|FIXED_PROTOCOL|UNKNOWN`).
- Whether changing the client-local 18/14 pair causes additional authoritative tiles to arrive.
- Larger rectangle/full-floor/multi-floor/whole-map delivery support and any maximum extent.
- Any exact parser/network ceiling not yet recovered.

# Current producer

Temporary branch-only workflow head `ae5778d1f8b0e79b77bfa68c14692a3d599b25c5`, run `32022973229`, performs targeted exact `DescriptorProto` recovery from message-name anchors and uploads bounded text neighborhoods with `if: always()`. It does not execute the client and does not upload proprietary client bytes. The temporary workflow must be removed before terminal merge.

# Checkpoint

```yaml
checkpoint_version: 3
updated_at: 2026-08-17T13:02:22+02:00
base_main: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
branch: research/OTC-20260817-track-a-worldmap-server-delivery-extent
pr: 473
status: investigating
phase: server-delivery-static-analysis
runtime_access: none
last_completed_step: complete exact message census persisted; first two descriptor-probe failures isolated to producer heuristics with distinct repairs
validation_level: focused
heavy_validation_runs: 0
session_rotation_count: 0
blockers: []
next_action: Inspect the text artifact from targeted descriptor run 32022973229; classify exact generic outbound and map-message fields if recovered, otherwise preserve the bounded negative result and stop producer escalation at the three-repair ceiling.
```