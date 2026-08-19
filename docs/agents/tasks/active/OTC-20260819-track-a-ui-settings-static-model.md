---
task_id: OTC-20260819-track-a-ui-settings-static-model
project_lane: otclient
programme: OTCLIENT-TIBIA-RE
alias: TIBIA-RE-UI-SETTINGS
track_id: official-client-re
subject: official native Linux Tibia client only
status: validating
phase: coordinator-accept-with-edits
task_kind: discovery
implementation_authorized: false
run_scope: single_task
researcher_delivery: draft_pr_only
promotion_authority: coordinator_only
base_main: be07623155ac81fa69d618cf277232f6825a7d9e
branch: docs/OTC-20260819-track-a-ui-settings-static-model
session_role: coordinator
execution_mode: chat_github
execution_reason: source research is complete; independent coordinator audit accepted the bounded slice with one repaired fullscreen-evidence classification and is freezing the final head for exact-head validation
context_pressure: medium
context_growth: stable
estimate_confidence: high
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
physical_e2e_required: false
source_pr: 544
source_researcher_head: 7861752c312f77fad0cde28c44c8745aa2806909
coordinator_review: 4969134238
coordinator_decision: ACCEPT_WITH_EDITS
open_material_findings_after_repair: 0
---

# OTC-20260819 Track A UI/settings coordinator checkpoint

## Accepted delivery

`TIBIA-RE-UI-SETTINGS` has a bounded current-build evidence slice suitable for coordinator promotion. It includes:

1. dedicated current-public-package static model evidence for H07-H14;
2. exact static `clientoptions.json` xrefs and used `QSettings` callsites;
3. lower-priority current-build refresh signals for selected H02/H04/H05/H06/H15/H18 surfaces;
4. one causal reversible Master Volume persistence experiment in a task-owned `ephemeral_isolated` runtime;
5. negative-control/harness evidence from earlier fullscreen attempts.

The researcher has dropped runtime authority. No further physical operation belongs to this closeout.

## Exact current-build fence

```yaml
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
elf_build_id: d803d9695868713ef6ab0c3cf65f91212c9c6a62
packed_sha256: 1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
```

## FACT — static evidence

The source exact-head static package establishes dedicated current-build class/model/controller surfaces for H07-H13, `TClientOptions`, `EClientOption`, one `clientoptions.json` literal with 38 decoded executable references, four used `QSettings` read/write/group PLT targets and 51 direct callsites.

This is dedicated evidence beyond broad capability-name presence but does not by itself establish setting-specific runtime semantics.

## FACT — independently verified Master Volume persistence

The coordinator independently re-read primary Remote Desktop Commander command/result history from the authorized Synology device rather than relying only on researcher prose.

That history proves the task-owned isolated exact client, shared GUI-input lock, baseline `clientoptions.json`, committed semantic JSON change:

```text
options.soundMasterVolume:    100 -> 43
options.soundMasterVolumeOld: 100 -> 43
```

survival of both values through a clean same-HOME restart, inverse UI commit restoring both fields to `100`, a second clean restart with both fields still `100`, and terminal cleanup with zero task-marker processes/root/display residue. No login or credentials were used.

The researcher also recorded matching temporary visual UI readbacks (100→43→restart 43→rollback 100→restart 100); because those temporary images were deleted, the coordinator retains the pixel-level UI text as source observation rather than independent artifact evidence. The durable semantic JSON/restart/rollback chain is independently verified.

## Material audit correction

`UISET-AUD-001` — MEDIUM / high confidence.

The prior source overclaimed `Alt+Return` fullscreen persistence as `DISPROVEN`. Inspection of the pinned experiment code shows v2 verified an immediate window-size change, but v5/v6 removed that effect check and only scanned candidate files after sending the key.

Accepted terminal classification:

```yaml
fullscreen_persistence_discriminator: INCONCLUSIVE
alt_return_sent: true
non_cache_candidate_file_delta_observed: false
fullscreen_effect_proven: false
fullscreen_persistence_disproven: false
```

The corrected durable evidence file removes the semantic disproof claim. Open material findings after repair: `0`.

## Coverage disposition

Against PR #536's status definitions, this task supports the following **task-local** delta only:

```text
H07 NOT_STARTED -> PARTIAL
H08 NOT_STARTED -> PARTIAL
H09 NOT_STARTED -> PARTIAL
H10 NOT_STARTED -> PARTIAL
H11 NOT_STARTED -> PARTIAL  (runtime strengthened by Master Volume)
H12 NOT_STARTED -> PARTIAL
H13 NOT_STARTED -> PARTIAL
H14 NOT_STARTED -> PARTIAL  (runtime strengthened by persistence/restart/rollback)
```

No H07-H14 row is `DONE`. PR #536 shared matrix/checklist paths remain untouched.

## Remaining UNKNOWN

- complete H10/H12/H13 setting-specific runtime semantics;
- all per-setting persistence sinks and Apply/OK timing;
- character-specific/global option partition;
- profile/migration versioning semantics;
- user-visible `QSettings` versus `clientoptions.json` relationship;
- fullscreen persistence semantics;
- complete H11 audio/music/ambient configuration semantics beyond the proven Master Volume path.

## Source validation before coordinator edit

Researcher head `7861752c312f77fad0cde28c44c8745aa2806909` passed:

```text
Track A agent runtime governance 32223847502 = SUCCESS
Track A UI/settings static model 32223847653 = SUCCESS
CI 32223847815 = SUCCESS
changed files = exactly 7 task-owned paths
review threads = 0
```

The coordinator edit changes only the task record and `runtime-settings-persistence.md` classification/evidence wording. Final exact-head checks must now run on the new frozen head.

## Durable evidence

- `.github/workflows/track-a-ui-settings-static-model.yml`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/current-build-static-model.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h07-h09-actionbar-hotkey-multiaction.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/persistence-xrefs.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/h01-h06-h15-h19-static-refresh.md`
- `docs/agents/evidence/OTC-20260819-track-a-ui-settings-static-model/runtime-settings-persistence.md`

## Next action

Freeze the resulting exact PR head; verify emitted Track A/static-model/CI checks and zero review threads. If all gates remain green, coordinator marks #544 Ready and squash-merges the accepted corrected slice. Then archive this task, release ownership and persist terminal source/merge evidence in a lifecycle-only closeout PR.