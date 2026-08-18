# Track A Controller Handoff and Persistent Viewer Contract v1

```yaml
track_a_controller_handoff_and_viewer_version: 1
track_id: official-client-re
repository: blakinio/otclient
runtime_platform: official_native_linux_only
status: proposed_until_PR_541_merge
```

This contract extends, and never weakens, `TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`, `TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md` and ADR-0001. Until PR #541 is reviewed and merged, it is implementation evidence only and is **not** live runtime authority.

## Purpose

Keep the canonical official-client runtime and browser observer durable across replacement agent sessions without treating a historical agent `session_id` as runtime identity.

The three identities are separate:

```text
runtime    = registration + boot/PID/start/exact-client/display/raw-XRes XID
controller = current task + disposable current session + capability + lease generation
viewer     = immutable runtime binding + viewer instance + presentation topology
```

A controller session may change while the same exact runtime and the same viewer remain alive.

## Mandatory replacement-session sequence

A replacement worker must first perform ordinary repository/session recovery and current Track A admission. It must not copy a historical `session_id` from a handoff document merely to satisfy lease validation.

The supported controller entry point is:

```text
python3 .github/scripts/tibia-official-client-re-canonical-live-resume.py \
  resume \
  --task-id <current task>
```

On GitHub Actions the helper derives a fresh controller session from the current run/attempt/job. Outside GitHub Actions a fresh explicit `--session-id` is required.

If a fresh unexpired controller already belongs to the **same task** but a different prior session, replacement is explicit:

```text
python3 .github/scripts/tibia-official-client-re-canonical-live-resume.py \
  resume \
  --task-id <same task> \
  --replace-active-same-task \
  --reason '<verified recovery reason>'
```

The same-task handoff must:

- discover the previous session from authoritative lease state;
- require the current capability and expected generation;
- refuse another task;
- refuse an expired lease and use normal stale takeover instead;
- rotate the capability;
- increment lease generation;
- invalidate the old capability immediately at state commit;
- keep the canonical coordination lock through the transfer.

A new generation does **not** automatically bless the existing registration. When registration survives from the older generation, `resume.py` must use the promoted generation-rebind transition and then Gate B.

## Canonical reuse and Gate B window authority

For replacement-session reuse, rebind and Gate B, the default probe is:

```text
.github/scripts/tibia-official-client-re-canonical-live-xres-probe.py
```

It must prove the registered X11 window through:

```text
raw X11/XRes
 -> LocalClientPid
 -> exact registered client PID
 -> VIEWABLE 1920x1080 XID
 -> exact registration window_identity
```

The reuse/Gate-B path must not use `xdotool search --pid` as window-ownership authority. `xdotool` may remain a bootstrap/discovery implementation detail until the separate initial-creation worker is migrated, but it cannot override raw-XRes evidence for reuse of an already registered runtime.

The raw-XRes reuse probe also verifies the canonical tracked process group, role markers, secret-free process environments, VNC and WARP listener ownership, and the RFB banner before returning a manifest to the existing transition manager.

## Persistent browser observer

The canonical browser presentation topology is:

```text
registered canonical X11 DISPLAY
 -> x11vnc view-only 127.0.0.1:5901
 -> websockify/noVNC runner backend :6081
 -> existing host presentation layer :6082
 -> http://synology:6082/
```

`6081` and `6082` are different roles. A worker must not bind the runner websockify backend to `6082` and then attempt to publish another host relay on `6082`.

The low-level viewer implementation is:

```text
.github/scripts/tibia-official-client-re-persistent-viewer.py
```

`start` and `stop` are state-changing observer-management operations and are legal only for the current controller after current Gate A/rebind/Gate B authority is already established for the exact registered runtime. The viewer implementation's lease validation is an additional guard, not a substitute for Gate B.

A future higher-level caller may compose `resume -> Gate B -> viewer start`; it must not weaken this ordering.

## Viewer identity and health

Every viewer instance serves a non-secret `viewer-identity.json` that binds the presentation backend to immutable runtime identity. Viewer health requires:

```text
runtime registration binding       PASS
raw-XRes registered XID ownership  PASS
RFB banner                          PASS
local :6081 identity               exact match
local :6081 WebSocket upgrade      HTTP 101
public :6082 identity              exact same match
public :6082 WebSocket upgrade     HTTP 101
```

Runtime health and viewer health are reported independently.

If the exact runtime remains healthy but viewer health fails:

```text
TRACK_A_RUNTIME_HEALTH=PASS
TRACK_A_VIEWER_HEALTH=FAIL_<presentation reason>
```

then the failure authorizes **viewer repair only**. It does not authorize client restart, login/logout, character selection, process signalling or registration mutation.

## Viewer process ownership

The viewer may replace only its own recorded PIDs whose `/proc/<pid>/environ` proves the exact Track A viewer instance and role. Unknown listeners fail closed. Broad `pkill`, broad Docker cleanup, display cleanup and unrelated listener replacement remain forbidden.

The viewer is view-only. Persistent viewer children must not inherit credentials, lease capabilities, `RUNNER_TRACKING_ID` or secret-bearing variables.

## Release

A controller may release authority without destroying the canonical runtime or viewer:

```text
python3 .github/scripts/tibia-official-client-re-canonical-live-resume.py \
  release \
  --task-id <current task>
```

The release helper discovers the current authoritative controller session and current token slot from controller state. A historical `session_id` is not an input.

## Physical validation gate

Repository tests are not physical deployment proof. Before this facility is called deployed, a serialized physical Synology validation must prove on the current admitted exact client that:

1. one controller establishes Gate B;
2. the viewer is healthy through the exact public `:6082` identity and WebSocket path;
3. controller authority is released/replaced without terminating the client/viewer;
4. the replacement controller obtains a fresh session/capability/generation;
5. required rebind + Gate B pass using the raw-XRes probe;
6. the same runtime identity and viewer instance remain healthy after controller replacement;
7. no second official-client login/session is created;
8. no Tibia credential or auth/session secret is accessed by the viewer/handoff test.

If another task owns the required Synology/runtime surface, the physical validation waits. It must never preempt that owner merely to complete this contract.
