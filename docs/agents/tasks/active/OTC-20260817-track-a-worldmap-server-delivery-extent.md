---
task_id: OTC-20260817-track-a-worldmap-server-delivery-extent
status: validating
agent: ChatGPT
project_lane: otclient
lane: official-client-re
track: official-client-re
task_kind: discovery
phase: closeout-audit
branch: research/OTC-20260817-track-a-worldmap-server-delivery-extent
base_branch: main
base_sha: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
created: 2026-08-17T12:45:00+02:00
updated: 2026-08-17T13:08:50+02:00
risk: medium
related_pr: 473
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
estimate_confidence: high
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
last_progress_at: 2026-08-17T13:08:50+02:00
ci_checks_for_current_head: 0
ci_check_generation: closeout-pre-ci
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

- `main` exact head at claim remains current during closeout: `f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b` (merged PR #472, prompt v1.1.0).
- PR #471 merged the durable alias/handover; #472 merged the server-delivered-map-extent acceptance extension.
- Prior mutation-design task #452/#453 is terminal and was not recreated.
- Prior physical startup-canary #462/#466 is terminal; it proved patched-copy startup only and did not establish IN_GAME semantics or causal worldmap object propagation.
- Draft PR #473 is the sole current task PR.

# Direct result

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
SERVER_LARGER_RECTANGLE_SUPPORTED=UNKNOWN
SERVER_FULL_FLOOR_DELIVERY_SUPPORTED=UNKNOWN
SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED=UNKNOWN
SERVER_WHOLE_MAP_DELIVERY_SUPPORTED=UNKNOWN
MAX_SERVER_DELIVERABLE_EXTENT=UNKNOWN
```

These are evidence-bounded results, not missing work disguised as success. Exact generated-message directionality is proven server->client for normal map payload families, but the exact field surface required to distinguish negotiated/client-driven/fixed/server-driven extent control was not recovered through the authorized static surface. The causal distinction is isolated into one separately authorized physical runtime experiment in the final report.

# Acceptance inventory

- [x] Separate client Storage capacity, render/viewport extent and server-delivered protocol extent.
- [x] Recover complete exact generated-message directionality for `FullMap`, field, directional row/column and floor-change families.
- [x] Bound the aware-range/width-height negotiation question: no separately named outbound extent/range message exists in the complete 160-name census; generic outbound fields remain `NOT_RECOVERED`, therefore model remains `UNKNOWN`.
- [x] Search bounded parser/network evidence for width/height, strip/floor counts, coordinate or length ceilings; retain `UNKNOWN` where no exact ceiling was recovered.
- [x] Record bounded negative evidence rather than global impossibility claims.
- [x] Design one separately-authorized causal runtime discriminator that separates authoritative inbound growth from Storage/render/picker growth.
- [ ] Fresh independent documentation/evidence audit with zero material findings or an explicit blocker.
- [ ] Exact-head changed-file audit, required CI, review hygiene and terminal task lifecycle.

# Evidence summary

## PROVEN

- Exact official Linux client fence: version `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Accepted client-local geometry chain starts from packed `18/14` and propagates through exact `TWorldmapProtocolMessageHandler` to Storage; Viewport/RenderProvider/Picker are separate downstream dependencies.
- Historical inventory run `31651220862`, job `94295767215`, recovered 349 generated message names total but emitted only a filtered subset.
- New exact-client run `32022209943`, job `95364071999`, producer head `553e447c0662892b0c1b9cab994c4545d09f22c8`, completed successfully and persisted the complete 349-name census in artifact `9285763750`.
- Complete census: 160 client->server, 189 server->client; no client->server generated name contains `aware|range|extent|viewport|fullmap|fielddata|width|height`.
- Inbound exact names directly include `GameserverMessageFullMap`, `FieldData`, `Left/RightColumn`, `Top/BottomRow`, `Top/BottomFloor` and map mutation messages.
- Final targeted descriptor run `32022973229`, job `95366330613`, producer head `ae5778d1f8b0e79b77bfa68c14692a3d599b25c5`, completed successfully and retained artifact `9286040543`.
- That probe validates exact raw descriptor recovery by proving `Coordinate.x/y/z` are optional `uint32` fields 1/2/3, but does not recover `Extent` or target generic/map message descriptors.
- Retained artifact `9227370490` contains normal strip observations consistent with an 18-wide baseline; it is not an atomic packet trace and does not prove multi-floor bulk delivery.
- Temporary branch-only evidence workflow was removed at commit `174def652ae494f337897d79996ec7c8a47408cf`; final diff contains only durable docs/evidence/task state.

## FAILED PRODUCER ATTEMPTS — DIAGNOSED, NOT RETRIED IDENTICALLY

- Run `32022548050`, job `95365067677`, head `888630af1de1d05be1f131df428360c9b4d215ba`: failed because producer used `FileDescriptorProto` field 6 instead of `message_type` field 4.
- Run `32022815851`, job `95365868589`, head `57b3068a16fe4d0ee9255fe20bbed4a17f272b9f`: corrected field number but strict raw protocol FileDescriptorProto start/layout heuristic still did not match the exact generated layout.
- Run `32022973229` changed hypothesis to targeted `DescriptorProto` anchors, succeeded and closed producer escalation.

## UNKNOWN

- Whether a generic outbound login/client-details/options/enter-world field carries extent negotiation.
- Whether changing the client-local `18/14` pair causes additional authoritative tiles to arrive.
- Larger rectangle/full-floor/multi-floor-bulk/whole-map delivery support and maximum server-deliverable extent.
- Any exact parser/network extent ceiling beyond the bounded evidence already retained.

# Durable outputs

- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-complete-message-census.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-targeted-descriptor-boundary.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-retained-strip-observation.md`
- `docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-extent.md`

# E2E classification

`NOT_APPLICABLE_WITH_REASON`: this task is a static/evidence research slice with `feature_scope.e2e_required=false` and `RUNTIME_ACCESS=none`. Physical causal validation is explicitly a separately authorized follow-on and is not required to close this bounded static task because the contract permits direct `UNKNOWN` classifications when the authorized evidence cannot prove a stronger value.

# Checkpoint

```yaml
checkpoint_version: 4
updated_at: 2026-08-17T13:08:50+02:00
base_main: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
branch: research/OTC-20260817-track-a-worldmap-server-delivery-extent
pr: 473
status: validating
phase: closeout-audit
runtime_access: none
last_completed_step: reconciled final static classifications, removed temporary evidence workflow and entered closeout audit
validation_level: focused
heavy_validation_runs: 0
session_rotation_count: 0
blockers: []
next_action: Perform a fresh independent audit of the current five-file durable diff against prompt v1.1.0 and repository closeout contracts; resolve any findings before exact-head CI/review/merge.
```
