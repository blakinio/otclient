# OTC-20260817 — isolated baseline attempt 1

```yaml
evidence_date: 2026-08-17
task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
execution_class: synology_physical_runtime
runtime_access: ephemeral_isolated
namespace: worldmap-causal-baseline-ephemeral-v1
runner: synology-otclient-01
run_id: 32026662197
job_id: 95377398485
head: 68e1bbaa75305c54689b8d7e1d2015a112f55c0c
result: FAILED_BEFORE_CREDENTIAL_USE
login_submitted: false
gameplay_used: false
client_byte_mutation: false
```

## FACT — isolated exact-client runtime reached a verified XRes-owned window

Admission and canonical-idle preflight passed before the task-owned isolated runtime started:

```text
TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true
WORLDMAP_CAUSAL_EPHEMERAL_BASELINE_ADMISSION=PASS
WORLDMAP_BASELINE_CANONICAL_LEASE={generation:8,status:released,controller_task:null,controller_session:null}
WORLDMAP_BASELINE_CANONICAL_REGISTRATION=ABSENT
WORLDMAP_BASELINE_CANONICAL_CONTROLLER_IDLE=PASS
```

The isolated worker then proved:

```text
WORLDMAP_BASELINE_PREEXISTING_NAMESPACE_PROCESS_COUNT=0
TRACK_A_CANONICAL_XRES_ADAPTER=PASS
WORLDMAP_BASELINE_EPHEMERAL_XRES_WORKER=PASS
TRACK_A_CANONICAL_STAGE=warp_egress_probe_pass
TRACK_A_CANONICAL_STAGE=xvfb_pass
TRACK_A_CANONICAL_STAGE=vnc_pass
TRACK_A_CANONICAL_STAGE=client_start
TRACK_A_CANONICAL_STAGE=client_window_wait_pass
WORLDMAP_BASELINE_MANIFEST_FENCE=PASS
WORLDMAP_BASELINE_CLIENT_PID=25587
WORLDMAP_BASELINE_WINDOW_IDENTITY=x11-window:12582929
WORLDMAP_BASELINE_TARGET_UNIQUENESS=PROVEN
```

This directly revalidates the merged #465 raw-XRes XID→PID path in the new task-owned ephemeral namespace. The legacy `client_window_missing` selector failure from canonical attempt 1 did not recur.

## FACT — attempt stopped before any account credential was used

The next gate attempted to arm the pre-Storage GDB observer before login. The observer process exited before the harness could prove attachment:

```text
WORLDMAP_BASELINE_ERROR=gdb_observer_not_alive
```

The harness checks for OCR/login tooling and uses `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` only **after** the observer is proven attached. Therefore this run did not submit login and did not issue gameplay input.

No screenshot, OCR text, coordinate evidence or raw process-memory artifact was uploaded. The privacy-safe artifact step was skipped because the physical step failed.

## FACT — cleanup and source rollback passed

The helper cleanup reported:

```text
WORLDMAP_BASELINE_ORIGINAL_SOURCE_REHASH=PASS
WORLDMAP_BASELINE_CLEANUP=COMPLETE
```

The isolated worker had a unique exact namespace marker before launch; cleanup targets only the observer and that task-owned process group/root. The exact installed source remained at SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

## Repair hypothesis

Historical accepted persistent observer commit `734f845deace5a26efa09b96a168bea0c05272f0` launched the toolroot GDB with a toolroot-aware runtime environment:

```text
HOME=<task home>
DISPLAY=<task display>
PATH=<toolroot usr/bin + usr/sbin + system fallback>
LD_LIBRARY_PATH=<toolroot usr/lib/x86_64-linux-gnu + toolroot lib/x86_64-linux-gnu>
```

Attempt 1 invoked the full toolroot GDB path but did not supply that runtime library environment. This is a concrete, materially changed repair hypothesis; it is not yet promoted to a fact until the repaired observer either attaches or emits a new diagnostic.

The repaired harness must also surface a sanitized pre-login GDB diagnostic when attachment fails, because no credentials exist at that gate and the previous local `gdb.stdout` was deleted during cleanup before it could be inspected.

```yaml
failure_gate: pre_storage_observer_attach
repair_cycle_for_ephemeral_baseline_gate: 1
identical_retry: forbidden
new_hypothesis: toolroot_gdb_runtime_environment_required
baseline_login_budget_consumed: 0
baseline_client_launches_consumed: 1
semantic_worldmap_attempt_consumed: 0
```
