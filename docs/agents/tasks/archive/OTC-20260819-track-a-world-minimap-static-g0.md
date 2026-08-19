---
task_id: OTC-20260819-track-a-world-minimap-static-g0
status: completed_static_scope
agent: null
session_role: released_after_promotion
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: coordinator-promotion
execution_mode: github_only
execution_class: github_hosted
source_branch: research/OTC-20260819-track-a-world-minimap-static-g0
source_pr: 545
source_head: 55034d31a3cfd55c597f463c97ebf97065192c8b
promotion_decision: ACCEPT_WITH_EDITS
promotion_pr: pending
promotion_merge: pending
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
client_byte_mutation_authorized: false
physical_e2e_required: false
ownership_release_state: release_effective_on_promotion_merge
audit_result: ACCEPT_WITH_EDITS
coordinator_review: 4969045959
open_material_findings_after_repair: 0
---

# Terminal static-scope result

The bounded `TIBIA-RE-WORLD-MINIMAP` G0 source Draft produced a valid dedicated current-public-package static package for F11/F12/F13, but its per-method target-address claims did not survive independent falsification.

## Accepted result

Exact producer artifact:

```text
run/job: 32194443653 / 95895463554
artifact: 9345368809
artifact sha256: c3c32ad9ce527e5ff7d469ae41914f3802fb55d465a993c8dbb32be2840e9755
packed sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size: 52109920
raw client retained: false
```

Independent artifact inspection confirmed exactly three compact text files and reproduced the artifact digest.

Accepted coverage delta:

```text
F11 NOT_STARTED -> PARTIAL
F12 NOT_STARTED -> PARTIAL
F13 PARTIAL -> PARTIAL
F08 BLOCKED unchanged
F10 BLOCKED unchanged
```

The shared PR #536 coverage matrix remains untouched; the delta is task-local until incorporated by its owner.

## Coordinator audit finding

`WM-MINIMAP-AUD-001` — MEDIUM / high confidence.

The source producer's relative-jump-table heuristic cannot prove its emitted per-method `target=... direct=true` values. Unrelated metaobjects receive identical target destinations in the retained artifact, directly falsifying exact per-method binding.

Disposition: fixed in coordinator promotion by retaining only:

- exact package fingerprint;
- Qt class/method ownership;
- QMeta/static-metacall identity;
- minimap/marker/action/protobuf/disk strings;
- conservative F11/F12/F13 status.

Per-method native target addresses from the producer are rejected and must not be reused as facts.

## Validation

Source exact head `55034d31a3cfd55c597f463c97ebf97065192c8b`:

```text
Track A agent runtime governance 32194785639 = SUCCESS
CI 32194785866 = SUCCESS
source changed paths = exactly 3
source review threads = 0
fresh coordinator review = 4969045959
```

Promotion exact-head CI and merge evidence are intentionally pending until the corrected promotion PR exists.

E2E: `NOT_APPLICABLE` because the task is static GitHub-hosted reverse-engineering with `runtime_access: none`.

## Remaining gaps

```yaml
minimap_layer_representation: UNKNOWN
minimap_visible_area_layout: UNKNOWN
minimap_tile_cache_boundary_semantics: UNKNOWN
marker_protobuf_schema: UNKNOWN
marker_coordinate_encoding: UNKNOWN
marker_persistence_transaction_semantics: UNKNOWN
world_screen_transform_formulas: UNKNOWN
world_screen_round_trip: UNKNOWN
live_minimap_semantics: UNKNOWN
server_delivered_extent_causality: BLOCKED_PR_475
worldmap_patch_causality: BLOCKED_PR_475
```

These do not reopen the bounded G0 static task; they are future separately admitted work.

## Ownership release

The source Draft remains unmerged. Its task/evidence/report paths are superseded by the corrected coordinator promotion. Ownership release becomes effective when that promotion merges; source PR #545 must then be closed unmerged as superseded.