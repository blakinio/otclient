# Track A worldmap mutation — physical v1 startup canary

Task: `OTC-20260817-track-a-worldmap-mutation-physical-validation`  
PR: #462  
Physical run: `32017654044`  
Hosted preflight job: `95350458656 = SUCCESS`  
Physical job: `95350515419 = SUCCESS`  
Runner: `synology-otclient-01`

## Physical admission

The accepted run was restacked on exact trusted `main@1eb4a8edecba3966aa1e6155e241b404eb4d30cb`. Immediately before the mutation boundary the same physical job proved:

```text
TRACK_A_AGENT_RUNTIME_CHANGED_TASKS=1
TRACK_A_AGENT_RUNTIME_BRANCH_BOUND_TASKS=1
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
WORLDMAP_RUNTIME_ADMISSION=PASS
WORLDMAP_LIVE_MAIN=1eb4a8edecba3966aa1e6155e241b404eb4d30cb
```

Two earlier generations consumed zero client launches:

- `32017164791`: generated harness lacked `EVENT_BASE_SHA` and refused before sandbox/patch/launch;
- `32017315080`: live-main fence detected main drift and refused before patch/launch.

The accepted run therefore consumed the task's first and only actual v1 patched-client launch.

## Exact patch proof

The exact official source fence passed before the task copy was created:

```text
WINDOW_DIAG_EXACT_SOURCE_FENCE=PASS
```

The fail-closed ELF patch helper then proved:

```text
WORLDMAP_COPY_PATCH=PASS
WORLDMAP_COPY_PATCH_TARGET_VA=0x01cdd958
WORLDMAP_COPY_PATCH_FILE_OFFSET=0x1cdd958
WORLDMAP_COPY_PATCH_CHANGED_BYTE_COUNT=1
WORLDMAP_COPY_PATCH_PATCHED_SHA256=7c8d936fa43e4a026d2a69c32ff30fdea149bb7eff7938c1b1acfc173899b44c
WORLDMAP_PATCHED_SHA256=7c8d936fa43e4a026d2a69c32ff30fdea149bb7eff7938c1b1acfc173899b44c
WORLDMAP_PATCH_FILE_OFFSET=0x1cdd958
WORLDMAP_PATCH_CANDIDATE=19,14
WORLDMAP_PATCH_DIFF_BYTES=1
```

This is the mutation-design canary only:

- source preimage `[18,14,8,6]`;
- patched first pair `[19,14]`;
- immutable trailing guard `[8,6]` unchanged;
- whole-file source-vs-copy difference exactly one byte;
- original exact installed source not modified.

The patched executable was fenced after launch:

```text
WORLDMAP_LIVE_PATCHED_PROCESS_FENCE=PASS
WINDOW_DIAG_CLIENT_PID=18401
WINDOW_DIAG_CLIENT_START=PASS
```

No credentials, login or gameplay were used.

## Bounded read-only memory observation

The patched process had stable PIE load bias:

```text
load_bias=0x55cc8f3ff000
```

The observer was the direct parent of PID `18401` and opened only `/proc/18401/mem` read-only. It scanned writable anonymous/special mappings for the exact runtime vptr values recovered by accepted static evidence.

At t01:

```text
ranges=7
bytes=962560
HANDLER=0 STORAGE=0 VIEWPORT=0 RENDER=0 PICKER=0 CAMERA=0
```

At t05:

```text
ranges=40
bytes=18063360
HANDLER=0 STORAGE=0 VIEWPORT=0 RENDER=0 PICKER=0 CAMERA=0
```

At t15:

```text
ranges=104
bytes=457375744
HANDLER=0 STORAGE=0 VIEWPORT=0 RENDER=0 PICKER=0 CAMERA=0
```

At t35:

```text
ranges=109
bytes=522559488
HANDLER=0 STORAGE=0 VIEWPORT=0 RENDER=0 PICKER=0 CAMERA=0
```

The exact t35 targets were:

```text
Handler  = 0x55cc924861d8
Storage  = 0x55cc9248be70
Viewport = 0x55cc9248b9a8
Render   = 0x55cc9236b258
Picker   = 0x55cc9236a7c8
Camera   = 0x55cc92482968
```

The client remained alive and had a VIEWABLE 1920x1080 X11 resource by t15/t35, so the negative object result is not explained by immediate process failure. The run nevertheless had no authenticated/in-game lifecycle.

The generated classification was:

```text
WORLDMAP_STRUCTURAL_CLASSIFICATION=NO_HANDLER_CANARY_OBSERVED
```

## Interpretation

This is a bounded startup-state negative, not a disproof of the accepted static dependency graph.

What the run proves:

1. the exact `[19,14]` patched-copy construction is physically executable;
2. the patched process starts and remains alive through the bounded no-login startup observation;
3. in that no-login lifecycle, no exact Handler/Storage/Viewport/Render/Picker/Camera vptr instance was found in the bounded writable-memory census;
4. therefore this lifecycle cannot directly test Handler constructor propagation or Storage slot12 propagation;
5. a later causal propagation test requires a lifecycle in which the worldmap object graph is instantiated — expected to be an authenticated/game-session lifecycle, but that must be independently admitted rather than assumed.

This run does **not** prove that no such objects can ever exist, does not prove the final safe worldmap extent, and does not authorize a second patch site or a login.

## Rollback and cleanup

Rollback succeeded after the evidence capture:

```text
WORLDMAP_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_PATCHED_COPY_REMOVED=PASS
WINDOW_DIAG_CLEANUP=COMPLETE
WORLDMAP_GENERATED_SCRIPT_RC=0
WORLDMAP_PHYSICAL_CANARY_V1=PASS_EVIDENCE_CAPTURED
```

The task-owned sandbox was removed and the canonical exact source rehashed to its original exact SHA.

## v1 terminal classification

```yaml
offline_patch_execution: PROVEN
patched_client_startup: PROVEN
patched_copy_identity: PROVEN
original_source_unchanged: PROVEN
rollback: PROVEN
no_login_startup_worldmap_object_graph: NOT_OBSERVED_BOUNDED
handler_canary_19_14: NOT_OBSERVED
storage_canary_19_14: NOT_OBSERVED
CAUSAL_PROPAGATION_PROVEN: false
SEMANTICALLY_VALIDATED: false
STARTUP_BOUNDARY_PROVEN: true
second_patch_site_authorized: false
additional_v1_launch_authorized: false
```

The next legitimate step is not another v1 launch. It is to determine, through the canonical RUNTIME owner, whether a legal current `IN_GAME` lifecycle exists. Only a fresh separately admitted live-session consumer may perform the worldmap causal/semantic follow-up.