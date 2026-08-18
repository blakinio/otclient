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

On Synology, the durable user-facing endpoint should also not depend on exposing a task container's high port directly on the LAN. DSM already provides the stable HTTPS frontend and WebSocket-capable reverse-proxy layer.

## Decision

### 1. Controller session remains disposable

Controller authority is still `task_id + current session_id + capability + lease generation`. Same-task handoff rotates the capability and advances generation. A replacement agent does not reuse an old `session_id` merely to pass validation.

The existing raw-XRes reuse/Gate-B work in PR #541 remains valid and is retained for canonical official-client identity when a registered client exists.

### 2. KasmVNC becomes the persistent browser desktop

The persistent desktop provider is KasmVNC, hosted as a task-owned Docker container on Synology. Its port is a loopback backend; DSM Reverse Proxy is the supported user-facing frontend:

```text
browser
  -> https://<stable-kasm-hostname>:443/
  -> DSM Reverse Proxy + WebSocket forwarding
  -> https://127.0.0.1:6901/
  -> KasmVNC integrated HTTPS/WebSocket service
  -> persistent Kasm desktop DISPLAY=:1
```

Deployment identity:

```yaml
container: otclient-track-a-kasmvnc
runtime_namespace: track-a-kasmvnc-desktop
backend_host: 127.0.0.1
backend_port: 6901
container_port: 6901
internal_display: ':1'
restart_policy: unless-stopped
```

The Kasm desktop is not created per ChatGPT/GitHub Actions session. Its container survives the deployment job and later controller turnover. The DSM hostname remains stable independently of agent/session turnover.

### 3. noVNC is not part of the new path

The new Kasm desktop MUST NOT use:

```text
Xvfb -> x11vnc -> websockify -> noVNC
```

as its browser presentation implementation.

PR #528 may temporarily retain its legacy observer `DISPLAY=:99` / `http://192.168.1.2:6083/` while its own task still owns that surface. That observer is historical/legacy task state and must not be presented as the new Track A desktop.

### 4. DSM Reverse Proxy is the public presentation boundary

Port `6901` is bound only to `127.0.0.1` on Synology. A browser is not expected to reach `192.168.1.2:6901` directly.

The operator configures DSM Reverse Proxy with an HTTPS source hostname on port `443` and destination `HTTPS 127.0.0.1:6901`. WebSocket upgrade forwarding is mandatory. Repository automation deliberately does not edit DSM's global reverse-proxy configuration.

Backend deployment and public presentation are separate health gates:

```text
Kasm backend health  = container + loopback HTTPS
DSM frontend health  = hostname + TLS + reverse proxy + WebSocket + Kasm app
```

A healthy backend is not enough to claim the browser endpoint available.

### 5. Desktop deployment is isolated from official-client execution

A desktop-only Kasm deployment is an `ephemeral_isolated` runtime operation. It is allowed to create only its declared container/state/loopback backend and must not touch another task's official-client process/session/display/lease/registration.

Because PR #528 currently owns the native-login official-client surface, PR #541 may deploy KasmVNC now but MUST NOT start an additional official Tibia client inside it yet.

After #528 releases or explicitly reconciles official-client ownership, the official native Linux client launch/bootstrap path should be migrated to run inside the persistent Kasm desktop. At that point current canonical admission, registration and Gate B must describe the exact client actually running there.

### 6. Failure domains stay separate

Kasm backend health, DSM presentation health and official-client health are independent. A broken Kasm/DSM endpoint does not authorize a Tibia client restart, and a Tibia client failure does not authorize broad Kasm/Docker cleanup.

### 7. Secret boundary

Desktop deployment never reads or passes Tibia account/auth/session secrets. The Kasm browser credential is generated at deployment time and stored only in task-private mode-0600 state. It is never committed as a workflow constant and grants no Tibia authority.

## Consequences

- The human observer gets a genuinely different technology from noVNC.
- DSM provides the stable HTTPS hostname/certificate/WebSocket frontend.
- Kasm's backend port is not intentionally exposed on the LAN.
- `session_id` remains a controller-authority property, not GUI identity.
- Kasm desktop deployment can proceed without creating a conflicting second official-client session.
- The official client migration becomes a clear later integration step rather than being silently mixed into viewer installation.
- The retained noVNC observer on `6083` is explicitly legacy and can be retired by its owner after migration.

## Acceptance

Before claiming the Kasm backend deployed, physical Synology evidence must show:

1. the exact task-owned Kasm container is running;
2. `restart=unless-stopped`;
3. host loopback `127.0.0.1:6901` reaches the Kasm HTTPS application;
4. `6901` is not published as a non-loopback LAN endpoint;
5. the container survives the deploy job;
6. PR #528 `:99/6083` remains untouched;
7. the deploy path accessed no Tibia secrets and launched no official client.

Before claiming the operator browser endpoint available, additionally prove a DSM Reverse Proxy HTTPS hostname with WebSocket forwarding to `https://127.0.0.1:6901`.

Before claiming the full Track A runtime migration complete, a later serialized E2E must additionally prove the official client runs inside this persistent Kasm desktop and remains correctly registered/controlled across a replacement controller handoff without creating a second official-client session.
