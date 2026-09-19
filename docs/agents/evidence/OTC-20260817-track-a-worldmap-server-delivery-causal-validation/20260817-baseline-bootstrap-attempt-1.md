# OTC-20260817 — baseline canonical bootstrap attempt 1

```yaml
evidence_date: 2026-08-17
task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
pr: 475
execution_class: synology_physical_runtime
runner: synology-otclient-01
run_id: 32025398762
job_id: 95373646537
head: 4296c2376fc8585fa62f6edf040ee88db453dbc3
result: FAILED_BEFORE_REGISTRATION
credentials_used: false
login_used: false
gameplay_used: false
client_byte_mutation: false
```

## FACT — physical launch reached exact-client window detection

The admitted transaction acquired fresh canonical lease generation `8`, validated Gate-A lease ownership, started the canonical WARP/SOCKS path successfully, started Xvfb and VNC, and reached `TRACK_A_CANONICAL_STAGE=client_start` followed by `client_window_wait_start`.

The exact failure was:

```text
TRACK_A_CANONICAL_SESSION_ERROR=client_window_missing
TRACK_A_CANONICAL_TRANSITION_ERROR=bootstrap_worker_failed
```

The bootstrap therefore did not publish `runtime-registration.json`. No credentials were supplied and no login or gameplay operation occurred.

## FACT — attempt used the obsolete raw worker composition

The branch workflow passed `.github/scripts/tibia-official-client-re-canonical-live-session.sh` directly to the reviewed transition. That raw source still contains the legacy `xdotool search --onlyvisible --pid ... --name '^Tibia$'` window selector.

Trusted `main` already contains merged PR #465 (`f8e628a255a18ec92839bbb45ef0e3b40bef8605`), whose purpose is to replace exactly that legacy selector in the canonical worker composition with the raw-XRes XID→PID resolver. #465's hosted integration generates the corrected worker with `.github/scripts/tibia-official-client-re-canonical-xres-worker-adapter.py` and rejects any generated worker that still contains the legacy selector.

The failure is therefore classified as an execution-composition defect in this task's first workflow, not as evidence that the exact client failed to create a valid X11 window and not as a worldmap semantic result.

## FACT — rollback was independently verified clean

Post-failure cleanup audit:

```yaml
run_id: 32025665881
job_id: 95374436911
head: 4d011ebef3fe500a125caae7fda287ac8498ff52
result: SUCCESS
lease_generation: 8
lease_status: released
lease_controller_task: null
lease_controller_session: null
canonical_registration: ABSENT
canonical_session_root: ABSENT
task_lease_token: ABSENT
canonical_marked_process_count: 0
rollback: PASS
```

The cleanup audit used a narrow read-only process census restricted to processes explicitly marked `OTCLIENT_TIBIA_RE_TRACK=official-client-re` and `OTCLIENT_TIBIA_RE_CANONICAL_RUNTIME=1`; it found zero survivors.

## Repair classification

```yaml
failure_signature: legacy_window_selector_client_window_missing
identical_retry_authorized: false
new_hypothesis: use trusted-main merged #465 XRes-generated canonical worker
repair_cycle: 1
physical_launch_consumed: 1
semantic_worldmap_attempt_consumed: 0
```

The next physical bootstrap, if executed, must not repeat the raw worker. It must generate and syntax-check the #465 XRes-composed worker and pass that generated worker to the same reviewed cancellation-safe bootstrap transition. This is one evidence-based repair with materially changed input under `ANTI_STALL_AND_EXECUTION_BUDGET.md`; it is not an identical retry.
