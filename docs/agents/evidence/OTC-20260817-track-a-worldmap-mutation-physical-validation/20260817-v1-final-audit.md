# Track A worldmap mutation physical v1 — final audit

Task: `OTC-20260817-track-a-worldmap-mutation-physical-validation`  
PR: #462  
Audited run: `32017654044`  
Audited physical job: `95350515419`

## Audit question

Did the physical v1 run execute exactly the merged mutation-design `[19,14]` canary on a task-owned copy, observe only the authorized patched PID, preserve the original source, and classify the absence of worldmap objects without overclaiming causal/semantic validation?

## Audit results

| Check | Result |
|---|---|
| fresh Track A admission before mutation | PASS |
| exact current-main fence | PASS (`1eb4a8edecba3966aa1e6155e241b404eb4d30cb`) |
| exact source fence | PASS |
| PT_LOAD-derived target offset | PASS (`0x1cdd958`) |
| mutation candidate | PASS (`[19,14]`) |
| immutable `[8,6]` guard preserved | PASS by helper postimage/full-diff contract |
| whole-file changed byte count | PASS (`1`) |
| canonical source patched in-place | NO |
| patched-copy SHA differs from exact source | PASS (`7c8d936f...`) |
| patched process live identity | PASS (PID `18401`) |
| process-memory access | READ-ONLY, task-owned PID only |
| memory writes | NONE |
| second patch site | NONE |
| credentials/login/gameplay | NONE |
| exact Handler vptr found in bounded startup census | NO |
| exact Storage vptr found in bounded startup census | NO |
| other accepted worldmap vptr instances found | NO |
| patched process remained alive through t35 | PASS |
| original exact source rehash after run | PASS |
| patched copy/task state removal | PASS |
| cleanup | PASS |

## Negative-result scope

The observer searched writable anonymous/special mappings only. At t35 that bounded search covered `109` ranges / `522559488` bytes and returned zero exact matches for Handler, Storage, Viewport, RenderProvider, Picker and Camera vptr values.

This supports only:

`NO_ACCEPTED_WORLDMAP_VPTR_INSTANCE_OBSERVED_IN_BOUNDED_WRITABLE_NO_LOGIN_STARTUP_CENSUS`

It does not support global absence of those object types and does not falsify the accepted static graph. Because the lifecycle did not authenticate or enter a game session, the Handler constructor and Storage slot12 causal path were not physically observed.

## Findings

No material finding invalidates v1.

`WM-V1-AUD-001` — **INFORMATIONAL boundary**: the memory census did not include arbitrary non-writable or file-backed mappings. That is appropriate for the object-instance hypothesis, but the durable evidence must retain the word **bounded** and must not claim global absence. The v1 evidence does so.

`WM-V1-AUD-002` — **INFORMATIONAL lifecycle**: a live `IN_GAME` follow-up cannot be inferred or authorized from this task. Current canonical RUNTIME ownership must independently establish that a legal current lifecycle exists; a new login/bootstrap solely for worldmap validation remains forbidden unless a future separately authorized programme decision explicitly changes that rule.

## Disposition

```yaml
material_findings_open: 0
v1_physical_execution: PASS
offline_patch_execution: PROVEN
patched_client_startup: PROVEN
bounded_startup_worldmap_instances: NOT_OBSERVED
CAUSAL_PROPAGATION_PROVEN: false
SEMANTICALLY_VALIDATED: false
STARTUP_BOUNDARY_PROVEN: true
additional_v1_launch_required: false
additional_v1_launch_authorized: false
next_dependency: CANONICAL_RUNTIME_LEGAL_IN_GAME_LIFECYCLE_INVENTORY
```

The one-shot v1 workflow and patch helpers must be removed before terminal merge. The task can close v1 cleanly even if no legal `IN_GAME` lifecycle exists; in that case semantic validation remains explicitly blocked rather than fabricated.