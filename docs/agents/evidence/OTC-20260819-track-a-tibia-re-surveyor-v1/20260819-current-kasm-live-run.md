# TIBIA-RE Surveyor v1 — current KasmVNC run

## Verified runtime result

```yaml
executed_remote_head: 577fc48e123974adca68e06dea48d59aa4d1a127
runtime_container: otclient-track-a-kasmvnc
display: ':1'
runtime_access: READ_ONLY_ADMITTED
target_uniqueness: PROVEN
candidate_process_count: 1
client_pid: 11365
client_process_start_ticks: 74970818
client_size: 52109920
client_sha256: ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
exact_current_fence_match: true
window_identity_class: CHARACTER_CONTEXT
canonical_registration_present: false
canonical_lease_generation: 16
canonical_lease_expired: true
keepalive_due: true
keepalive_result: KEEPALIVE_SKIPPED_UNAUTHORIZED
keyboard_mouse_input_sent_by_surveyor: false
anti_idle_semantic_evidence: false
heartbeat_present_after_run: false
gui_input_lock_present_after_run: false
```

A clean detached worktree fetched from the exact remote head ran `python3 -m unittest discover -s tests/tools/tibia_re_surveyor -v`: 13 tests passed. `git diff --check` also passed.

The current-session Surveyor run produced exactly 169 canonical rows: 14 DONE, 95 PARTIAL, 56 NOT_STARTED and 4 BLOCKED. It indexed evidence for 88 rows; 64 rows had at least one indexed evidence file containing the exact current-client SHA; the summed per-row evidence-file mention count was 272. These are indexing facts only and do not promote semantic status.

The first priority ordering from the canonical dependency matrix was `A15 C10 F08 F10 A16 B04 C21 H07 H14 H21`.

## Generated host outputs

```text
agent_bundle.json  12307 bytes  sha256 ee3b8ef505f78434368e85fb175de2629efab4624f89a9cb35dc8262784154a5
coverage.json      112314 bytes sha256 2fba73f307544c313ab797772a0c1ccd5fff903ae98ccd4c7a0a3d4df1fb3759
summary.md         2616 bytes   sha256 7b81c57afffccffdf976425fbbdfe7b2f89ae07507f71f1478e5fb50512f62ba
```

The outputs are retained on the Synology host under the task-owned Surveyor live-run directory. A strict privacy/secret-pattern scan returned PASS. The raw character-window title is not retained; only `CHARACTER_CONTEXT` is persisted.

## Anti-idle result

The owner requested an approximately ten-minute in-place turn policy. The harness implements the existing shared eight-minute trigger / ten-minute inactivity target and shared GUI lock/heartbeat contract, but current trusted control-plane state does not permit input: canonical registration is absent and the remaining generation-16 lease is expired.

The due keepalive therefore returned `KEEPALIVE_SKIPPED_UNAUTHORIZED` before the input transport path. A post-run check found both shared heartbeat and GUI-lock files absent. A real rotation on this session is therefore `NOT_PROVEN`; the positive path remains synthetic-test-only until a valid current canonical mutation admission exists.

```text
SURVEYOR_CURRENT_SESSION_READ_ONLY_E2E=PASS
SURVEYOR_CANONICAL_169_ROW_PARSE=PASS
SURVEYOR_EVIDENCE_INDEX=PASS
SURVEYOR_KEEPALIVE_FAIL_CLOSED=PASS
SURVEYOR_REAL_ROTATION=NOT_PROVEN_BLOCKED_BY_CURRENT_ADMISSION
```
