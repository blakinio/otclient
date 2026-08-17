---
task_id: OTC-20260817-track-a-worldmap-server-delivery-extent
status: validating
agent: ChatGPT
project_lane: otclient
lane: official-client-re
track: official-client-re
task_kind: discovery
phase: final-ci-review
branch: research/OTC-20260817-track-a-worldmap-server-delivery-extent
base_branch: main
base_sha: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
created: 2026-08-17T12:45:00+02:00
updated: 2026-08-17T13:10:25+02:00
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
last_progress_at: 2026-08-17T13:10:25+02:00
ci_checks_for_current_head: 0
ci_check_generation: final-gate
terminal_ci_wait_started_at: 2026-08-17T13:10:25+02:00
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

# Live-state

- Current `main` during final-gate entry remains `f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b`.
- PR #471/#472 are merged predecessor handover/contract changes.
- Prior mutation-design #452/#453 and startup-canary #462/#466 are terminal and were not recreated.
- PR #473 is the sole current task PR.
- Temporary branch-only evidence workflow was removed at commit `174def652ae494f337897d79996ec7c8a47408cf`.

# Direct result

```text
SERVER_MAP_DELIVERY_MODEL=UNKNOWN
SERVER_LARGER_RECTANGLE_SUPPORTED=UNKNOWN
SERVER_FULL_FLOOR_DELIVERY_SUPPORTED=UNKNOWN
SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED=UNKNOWN
SERVER_WHOLE_MAP_DELIVERY_SUPPORTED=UNKNOWN
MAX_SERVER_DELIVERABLE_EXTENT=UNKNOWN
```

These are evidence-bounded values. Exact generated-message directionality is proven server->client for normal map payload families, but the static evidence does not recover the generic outbound field surface required to distinguish negotiated/client-driven/fixed/server-driven extent control. The remaining causal distinction is isolated into one separately authorized physical runtime experiment in the final report.

# Acceptance inventory

- [x] Separate client Storage capacity, render/viewport extent and server-delivered protocol extent.
- [x] Recover complete exact generated-message directionality for `FullMap`, field, directional row/column and floor-change families.
- [x] Bound aware-range/width-height negotiation: no separately named outbound extent/range message in the complete 160-name census; generic outbound fields remain `NOT_RECOVERED`, so the model remains `UNKNOWN`.
- [x] Search bounded parser/network evidence for width/height, strip/floor counts, coordinate or length ceilings; preserve `UNKNOWN` where no exact ceiling was recovered.
- [x] Record bounded negative evidence rather than global impossibility claims.
- [x] Design one separately-authorized causal runtime discriminator that separates authoritative inbound growth from Storage/render/picker growth.
- [x] Fresh independent documentation/evidence audit: `20260817-closeout-audit.md`, `MATERIAL_FINDINGS=0`, `RESOLVED_FINDINGS=1`, `AUDIT_RESULT=PASS`.
- [ ] Exact-head changed-file audit, required CI, review hygiene and terminal task lifecycle.

# Evidence / validation summary

- Exact official Linux client: `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.
- Complete message census: run `32022209943`, job `95364071999`, producer `553e447c0662892b0c1b9cab994c4545d09f22c8`, artifact `9285763750`: 349 generated names, 160 client->server, 189 server->client; inbound exact names include FullMap/FieldData/rows/columns/floors/map mutations; no separately named outbound aware/range/extent/viewport/fullmap/fielddata/width/height message.
- Targeted descriptor boundary: run `32022973229`, job `95366330613`, producer `ae5778d1f8b0e79b77bfa68c14692a3d599b25c5`, artifact `9286040543`: exact `Coordinate.x/y/z` optional `uint32` recovered; target `Extent`/generic outbound/map-delivery descriptors not recovered.
- Descriptor failures `32022548050` and `32022815851` were diagnosed and repaired with changed hypotheses; no identical failure retry.
- Retained artifact `9227370490` is consistent with an 18-wide normal strip baseline but is not an atomic packet trace and does not prove larger/full-floor/multi-floor/whole-map delivery.
- Closeout audit at audited head `5a1f42ebb8b0eac061229f08774f87c16def2511` found zero material findings. Its one stale-checkpoint finding was already resolved by `07c2056129db2fc93dafe3cbd311f3bc3be90f39`.

# Durable outputs

- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-complete-message-census.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-targeted-descriptor-boundary.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-retained-strip-observation.md`
- `docs/agents/evidence/OTC-20260817-track-a-worldmap-server-delivery-extent/20260817-closeout-audit.md`
- `docs/agents/reports/OTCLIENT-20260817-worldmap-server-delivery-extent.md`

# E2E classification

`NOT_APPLICABLE_WITH_REASON`: this task is a static/evidence research slice with `feature_scope.e2e_required=false` and `RUNTIME_ACCESS=none`. Physical causal validation is explicitly a separately authorized follow-on. The contract permits direct `UNKNOWN` classifications when the authorized evidence cannot prove a stronger value, so physical E2E is not a closeout requirement for this bounded static task.

# Checkpoint

```yaml
checkpoint_version: 5
updated_at: 2026-08-17T13:10:25+02:00
base_main: f99ec371bafd0b9dbccb8fd6f4c8a3137e7d963b
branch: research/OTC-20260817-track-a-worldmap-server-delivery-extent
pr: 473
status: validating
phase: final-ci-review
runtime_access: none
last_completed_step: independent closeout audit passed with zero material findings
validation_level: focused
heavy_validation_runs: 0
session_rotation_count: 0
blockers: []
next_action: Verify the exact current head changed-file set, required checks, PR review/threads and mergeability; resolve any final gate before marking PR ready and merging.
```
