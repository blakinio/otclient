# ADR-0002: Persistent Track A viewer and same-task controller handoff

- Status: proposed
- Date: 2026-08-18
- Task/PR: `OTC-20260818-track-a-persistent-viewer-handoff` / `#541`
- Extends: `ADR-0001-track-a-canonical-live-runtime.md`
- Authority note: this decision is not live-operation authority until independently reviewed and merged.

## Context

Track A already targets one persistent canonical official-client runtime with disposable controller sessions. Two operational gaps repeatedly caused recovery work:

1. a replacement agent could hold the same task and face a fresh active controller lease whose `controller_session` belonged to the previous disposable worker; there was no narrow same-task transfer primitive, so historical session identifiers leaked into continuation procedures;
2. remote-view health was coupled to ad-hoc noVNC/X11 presentation plumbing. A black browser canvas could coexist with a healthy exact client and viewable X11 window.

The failure is concrete. In native-login PR #528 run/job `32147631742 / 95745198909`, the updater started websockify on runner port `6082` and then attempted to publish a relay on host `192.168.1.2:6082`; Docker correctly failed with `address already in use`. Earlier gen16 evidence separately proved a healthy client on `DISPLAY=:99`, raw-XRes PID ownership of the expected `1920x1080` window, a working RFB listener and working WebSocket while the host `6082 -> runner 6081` presentation mapping was wrong.

A controller session and a browser presentation endpoint are therefore not runtime identity.

## Decision

### 1. Keep three identities separate

Track A uses these distinct identities:

```text
runtime identity
  = runtime_id + boot identity + PID + process start ticks
    + exact executable fence + DISPLAY + raw-XRes-owned XID

controller identity
  = task_id + current disposable session_id + current capability
    + current lease generation

viewer identity
  = immutable runtime identity + viewer instance
    + RFB/backend/public presentation topology
```

Controller `session_id`, lease generation and registration generation MUST NOT be part of the viewer's immutable runtime binding.

### 2. Same-task controller handoff is a narrow authority transition

A replacement worker may transfer an **active, fresh lease for the same task only** when all of these are true:

- repository/session recovery preflight has established that replacing the prior worker is safe;
- the authoritative lease is active and unexpired;
- the lease's `controller_task` equals the replacement task;
- the caller holds the current capability token;
- the caller supplies the exact expected lease generation observed immediately before handoff;
- the new session id differs from the currently registered controller session;
- the new capability is written to a distinct mode-0600 task-local token slot before the lease record is committed;
- the canonical `coordination.lock` remains held for the complete transfer;
- the lease generation increments;
- the capability rotates;
- the previous token is invalid immediately after commit even if unlinking the stale token file later fails.

A handoff MUST NOT:

- cross task ids;
- transfer an expired lease;
- infer ownership from task/PR prose;
- bypass a different task's live controller;
- reuse the old session id merely to make validation pass;
- leave the lease generation unchanged.

An expired lease continues to use the existing stale-takeover path with its explicit reason. A different-task conflict remains a hard refusal.

After same-task handoff, an unchanged registered runtime normally has an older `lease_generation`. The existing reviewed generation-rebind transition MUST then re-prove the exact runtime and bind registration to the new controller generation before Gate B can pass.

### 3. High-level resume owns session-id discovery

The supported continuation entry point is:

```text
tibia-official-client-re-canonical-live-resume.py
```

On GitHub Actions it derives the replacement `session_id` from the current run/attempt/job rather than accepting a historical value from a handoff document. Outside GitHub Actions an explicit new session id is required.

For a fresh active same-task controller, replacement is never silent. The caller must explicitly select same-task replacement and provide a reason after the repository recovery/ownership preflight. The helper then:

```text
fresh/released lease
  -> acquire

active same task + same session
  -> renew

active same task + replacement authorized
  -> same-task handoff
  -> generation increment + capability rotation

registration generation mismatch
  -> canonical rebind

unchanged exact runtime
  -> Gate B

registration absent
  -> report canonical_bootstrap as the next transition
     without launching a client
```

`release` discovers the current authoritative session from lease state and releases controller authority while preserving the runtime.

### 4. Viewer is a persistent programme presentation resource

The browser viewer uses a fixed layered topology:

```text
canonical X11 DISPLAY
  -> x11vnc view-only RFB 127.0.0.1:5901
  -> websockify/noVNC runner backend 0.0.0.0:6081
  -> existing host presentation mapping
  -> http://synology:6082/
```

`6081` is the runner backend. `6082` is the user-facing host endpoint. A workflow MUST NOT bind websockify to `6082` and then attempt to publish another relay on the same host port.

The viewer start/stop transition requires current controller lease authority and executes while holding the canonical coordination lock. Viewer children receive neither the coordination-lock file descriptor nor the lease capability. They run with credential/capability environment variables removed and `x11vnc` is `-viewonly`.

The viewer may survive controller release or controller handoff. Its identity binds to immutable runtime identity, so a lease/rebind generation change alone does not invalidate a healthy viewer.

A client PID/start/executable/display/window change does invalidate the viewer and requires a new viewer binding.

### 5. Raw XRes is the window-ownership authority

For viewer binding and health, the supported authority is:

```text
.github/scripts/tibia-official-client-re-xres-window-owner.py
```

The resolved XID must:

- be `VIEWABLE`;
- have the expected `1920x1080` geometry;
- resolve through raw XRes 1.2 LocalClientPid to the registered exact client PID;
- equal the registration's `x11-window:<xid>` identity.

`xdotool search --pid` is discovery convenience only and MUST NOT override contradictory raw-XRes ownership evidence.

### 6. Public viewer health is proven end to end

A listening process or HTTP 200 on one layer is insufficient.

Every viewer instance serves a non-secret:

```text
/viewer-identity.json
```

containing the immutable runtime binding, viewer instance id and backend port. Health requires all of:

```text
registered runtime identity       PASS
raw-XRes window/PID ownership     PASS
x11vnc RFB banner                 PASS
local :6081 identity              exact match
local /websockify upgrade         HTTP 101
public :6082 identity             exact same match
public /websockify upgrade        HTTP 101
```

The identity request is cache-busted and compared structurally. This prevents a stale or unrelated host presentation service from being reported healthy merely because port `6082` accepts connections.

### 7. Runtime and viewer health are independent

Report independently:

```text
TRACK_A_RUNTIME_HEALTH=PASS|FAIL_<reason>
TRACK_A_VIEWER_HEALTH=PASS|FAIL_<reason>|UNKNOWN
TRACK_A_VIEWER_URL=http://synology:6082/
```

A viewer failure with runtime health `PASS` MUST NOT authorize client restart, logout, login, character selection, process signalling or runtime-registration mutation.

Repair the viewer path only.

A runtime identity failure is not relabelled as a presentation failure.

### 8. Port/ownership failures are fail closed

If `5901`, `6081` or public `6082` is already owned by an unproven process/service, the viewer controller refuses destructive replacement.

It may stop only viewer PIDs recorded in its own mode-restricted state whose process environment proves the expected Track A viewer instance and role.

It never uses broad `pkill`, broad Docker cleanup or unrelated listener replacement.

### 9. Secret boundary

Viewer and controller-continuation tooling never reads Tibia account/password values.

Persistent viewer children must not inherit:

```text
TIBIA_TEST_*
RUNNER_TRACKING_ID
*LEASE_TOKEN*
*CAPABILITY*
```

Viewer state and `/viewer-identity.json` are non-secret and must not contain credentials, account identifiers, session/auth tokens, cookies, packet payloads, framebuffer contents or character-selection secrets.

## Consequences

- Replacement agents get a new disposable session id instead of reusing stale chat/history values.
- A safe same-task handoff invalidates the old capability and deliberately advances generation, preserving the existing rebind/Gate B trust chain.
- The canonical client can survive controller turnover.
- The browser endpoint can survive controller turnover because viewer identity does not include controller-generation metadata.
- Black noVNC is diagnosed as presentation failure when exact runtime/XRes evidence remains healthy.
- `6081`/`6082` roles are unambiguous.
- Physical activation remains serialized and cannot be authorized by this unmerged ADR.

## Validation requirements

Before promotion:

1. deterministic unit tests for handoff refusal/success/token rotation;
2. deterministic tests for session-id derivation and rebind/Gate B routing;
3. deterministic tests proving viewer identity excludes controller generations and strips credentials/capabilities;
4. exact-head repository CI;
5. fresh independent audit of the authority and process-ownership boundaries;
6. physical Synology E2E after ownership is available, proving persistence across replacement jobs and exact public `6082` identity/WebSocket mapping without touching a second logged-in official-client session.

Until item 6 passes, repository implementation may be complete but physical deployment is not.
