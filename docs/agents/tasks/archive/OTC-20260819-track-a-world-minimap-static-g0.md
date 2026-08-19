---
task_id: OTC-20260819-track-a-world-minimap-static-g0
status: completed
agent: null
session_role: released
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: closed
execution_mode: github_only
execution_class: github_hosted
source_branch: research/OTC-20260819-track-a-world-minimap-static-g0
source_pr: 545
source_head: 55034d31a3cfd55c597f463c97ebf97065192c8b
source_terminal_state: closed_superseded_unmerged
promotion_decision: ACCEPT_WITH_EDITS
promotion_pr: 551
promotion_head: a86713c0f79190710cd437ed3b550ccaf7652436
promotion_merge: 6071b237d70a11ab10e5050cc23730162b0e7e0b
promotion_ci_run: 32223365501
promotion_ci_result: success
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
ownership_released: true
audit_result: PASS_AFTER_EDIT
source_coordinator_review: 4969045959
promotion_review: 4969069217
open_material_findings: 0
e2e_result: NOT_APPLICABLE
---

# Terminal result

The bounded `TIBIA-RE-WORLD-MINIMAP` G0 static package is terminally promoted and closed.

Source Draft #545 was independently audited, classified `ACCEPT_WITH_EDITS`, and closed unmerged as superseded after corrected promotion #551 merged.

## Accepted evidence

Independent inspection of producer artifact `9345368809` reproduced its GitHub digest exactly:

```text
artifact sha256: c3c32ad9ce527e5ff7d469ae41914f3802fb55d465a993c8dbb32be2840e9755
files: fence.txt, minimap-qmeta.txt, minimap-strings.txt
packed sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size: 52109920
CURRENT_PACKAGE_FENCE=PASS
RAW_CLIENT_RETAINED=false
```

The fingerprint is exact for the public Linux package fetched by producer run `32194443653`; it is not proof of the bytes used by a currently installed/canonical runtime.

Accepted static coverage consequence:

```text
F11 Minimap controller / visible area / floor state: NOT_STARTED -> PARTIAL
F12 Minimap markers:                              NOT_STARTED -> PARTIAL
F13 World<->screen coordinate transforms:         PARTIAL -> PARTIAL
F08 server-delivered extent/control:              BLOCKED unchanged
F10 worldmap patch causal propagation:            BLOCKED unchanged
```

PR #536's shared matrix/checklist paths were not modified. The delta is task-local until incorporated by its owner.

## Material audit finding and correction

`WM-MINIMAP-AUD-001` — MEDIUM, high confidence.

The source producer's relative-jump-table heuristic did not prove its emitted per-method `target=... direct=true` values. The raw retained artifact shows unrelated metaobjects receiving identical reported destinations, falsifying exact per-method binding.

The corrected promotion rejects those per-method target addresses and retains only evidence that survived independent falsification:

- exact public-package fingerprint;
- Qt class/method ownership;
- QMeta/static-metacall identity;
- minimap controller/visible-area/tile/render-info surfaces;
- marker action/controller/storage/overlay/render-info/protobuf/disk surfaces;
- world-map camera/viewport transform method-name surfaces;
- conservative F11/F12/F13 classifications.

No formula, object field layout, live semantic transition, server-delivery effect or runtime-stability claim is promoted.

## Validation

Source exact head `55034d31a3cfd55c597f463c97ebf97065192c8b`:

```text
Track A agent runtime governance 32194785639 = SUCCESS
CI 32194785866 = SUCCESS
source changed paths = exactly 3
source review threads = 0
fresh coordinator review = 4969045959
```

Corrected promotion exact head `a86713c0f79190710cd437ed3b550ccaf7652436`:

```text
CI 32223365501 = SUCCESS
changed paths = exactly 4 promotion-owned documentation/evidence/archive paths
promotion review = 4969069217
open material findings = 0
```

Promotion PR #551 squash-merged as:

```text
6071b237d70a11ab10e5050cc23730162b0e7e0b
```

Source PR #545 is closed unmerged as superseded.

E2E: `NOT_APPLICABLE` because this is static GitHub-hosted evidence with `runtime_access: none`.

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

These are future separately admitted work. They do not reopen this G0 task.

## Closeout

```yaml
closeout:
  implementation_complete: true
  complete_feature_or_declared_partial: true
  outcome_verified: true
  audit:
    result: PASS_AFTER_EDIT
    findings_open_material: 0
  e2e:
    result: NOT_APPLICABLE
    reason: static GitHub-hosted reverse-engineering package with runtime_access none
  final_ci:
    head: a86713c0f79190710cd437ed3b550ccaf7652436
    result: PASS
    run: 32223365501
  pull_requests:
    source: blakinio/otclient#545 closed_superseded_unmerged
    promotion: blakinio/otclient#551 merged as 6071b237d70a11ab10e5050cc23730162b0e7e0b
    unresolved_review_threads: 0
  task_archived_or_terminal: true
  ownership_released: true
```

No runtime, login, secret, gameplay or client mutation authority is retained by this task.