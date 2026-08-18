# ADR-0002: Persistent KasmVNC desktop and same-task controller handoff

- Status: proposed
- Date: 2026-08-18
- Task/PR: `OTC-20260818-track-a-persistent-viewer-handoff` / `#541`
- Extends: `ADR-0001-track-a-canonical-live-runtime.md`
- Supersedes in this PR: the proposed `x11vnc -> websockify -> noVNC` persistent-viewer design
- Authority note: this unmerged ADR does not expand live official-client authority.

## Context

Track A needs two kinds of continuity that must not be confused:

1. the exact official-client runtime may survive replacement agent/controller sessions;
2. the human observer needs one stable desktop URL that survives replacement agent/controller sessions.

The prior proposal still used noVNC and therefore did not satisfy the owner's requirement for a genuinely different, persistent desktop technology. Historical failures also showed that a browser presentation chain could be broken while the underlying X11/client state remained healthy.

## Decision

### 1. Controller session remains disposable

Controller authority is still `task_id + current session_id + capability + lease generation`. Same-task handoff rotates the capability and advances generation. A replacement agent does not reuse an old `session_id` merely to pass validation.

The existing raw-XRes reuse/Gate-B work in PR #541 remains valid and is retained for canonical official-client identity when a registered client exists.

### 2. KasmVNC becomes the persistent browser desktop

The Track A user-facing desktop provider is KasmVNC, hosted as a task-owned persistent Docker container on Synology:

```text
browser
  -> https://192.168.1.2:6901/
  -> KasmVNC integrated HTTPS/WebSocket service
  -> persistent Kasm desktop DISPLAY=:1
```

Deployment identity:

```yaml
container: otclient-track-a-kasmvnc
runtime_namespace: track-a-kasmvnc-desktop
host_port: 6901
container_port: 6901
internal_display: ':1'
restart_policy: unless-stopped
```

The Kasm desktop is not created per ChatGPT/GitHub Actions session. Its container and URL survive the deployment job and later controller turnover.

### 3. noVNC is not part of the new path

The new Kasm desktop MUST NOT use:

```text
Xvfb -> x11vnc -> websockify -> noVNC
```

as its browser presentation implementation.

PR #528 may temporarily retain its legacy observer `DISPLAY=:99` / `http://192.168.1.2:6083/` while its own task still owns that surface. That observer is historical/legacy task state and must not be presented as the new Track A desktop.

### 4. Desktop deployment is isolated from official-client execution

A desktop-only Kasm deployment is an `ephemeral_isolated` runtime operation. It is allowed to create only its declared container/state/port and must not touch another task's official-client process/session/display/lease/registration.

Because PR #528 currently owns the native-login official-client surface, PR #541 may deploy KasmVNC now but MUST NOT start an additional official Tibia client inside it yet.

After #528 releases or explicitly reconciles official-client ownership, the official native Linux client launch/bootstrap path should be migrated to run inside the persistent Kasm desktop. At that point current canonical admission, registration and Gate B must describe the exact client actually running there.

### 5. Failure domains stay separate

Kasm desktop health is not official-client health. A broken Kasm endpoint does not authorize a Tibia client restart, and a Tibia client failure does not authorize broad Kasm/Docker cleanup.

Kasm health is proven from exact container ownership, running state, restart policy, port mapping and the real HTTPS application response.

### 6. Secret boundary

Desktop deployment never reads or passes Tibia account/auth/session secrets. The Kasm browser credential is a separate LAN desktop credential and grants no Tibia authority.

## Consequences

- The human observer gets a genuinely different technology from noVNC.
- One stable endpoint can survive replacement agents and GitHub Actions jobs.
- `session_id` remains a controller-authority property, not GUI identity.
- Kasm desktop deployment can proceed without creating a conflicting second official-client session.
- The official client migration becomes a clear later integration step rather than being silently mixed into viewer installation.
- The retained noVNC observer on `6083` is explicitly legacy and can be retired by its owner after migration.

## Acceptance

Before claiming the desktop deployed, physical Synology evidence must show:

1. the exact task-owned Kasm container is running;
2. `restart=unless-stopped`;
3. host `192.168.1.2:6901` reaches the Kasm HTTPS application;
4. the container survives the deploy job;
5. PR #528 `:99/6083` remains untouched;
6. the deploy path accessed no Tibia secrets and launched no official client.

Before claiming the full Track A runtime migration complete, a later serialized E2E must additionally prove the official client runs inside this persistent Kasm desktop and remains correctly registered/controlled across a replacement controller handoff without creating a second official-client session.
