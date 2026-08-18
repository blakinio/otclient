# Track A Controller Handoff and Persistent KasmVNC Desktop Contract v2

```yaml
track_a_controller_handoff_and_viewer_version: 2
track_id: official-client-re
repository: blakinio/otclient
runtime_platform: official_native_linux_only
browser_desktop_provider: KasmVNC
public_frontend: DSM_reverse_proxy
status: proposed_until_PR_541_merge
```

This contract extends, and never weakens, `TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`, `TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md` and ADR-0001. Until PR #541 is reviewed and merged, repository changes here do not expand live official-client authority.

## Purpose

Make the GUI desktop a durable programme resource instead of an artifact of one agent/job. A replacement agent gets a fresh controller session and capability while reusing the same KasmVNC desktop/container and browser endpoint.

Keep these identities separate:

```text
runtime    = exact registered official client identity when one exists
controller = task + current disposable session + capability + lease generation
desktop    = task-owned KasmVNC container + internal display + loopback backend
frontend   = DSM reverse-proxy rule + stable HTTPS hostname + WebSocket forwarding
```

A historical agent `session_id` is never desktop identity.

## Mandatory controller replacement

The supported canonical controller entry point remains:

```text
python3 .github/scripts/tibia-official-client-re-canonical-live-resume.py resume --task-id <task>
```

On GitHub Actions it derives a fresh current session from the current run/attempt/job. For an active fresh lease owned by the same task but a prior agent session, replacement is explicit and requires a reason:

```text
python3 .github/scripts/tibia-official-client-re-canonical-live-resume.py \
  resume --task-id <same-task> --replace-active-same-task \
  --reason '<verified recovery reason>'
```

The handoff must remain fail closed: same task only, current capability required, exact expected generation required, capability rotated, generation incremented, old capability invalidated at commit, and canonical coordination serialization preserved. Expired leases use the existing stale-takeover path. Different-task ownership remains a refusal.

When a canonical official-client registration survives across controller generations, the existing reviewed generation-rebind transition and Gate B remain mandatory. The default reuse/Gate-B window proof is the raw-XRes probe, not `xdotool --pid`.

## KasmVNC desktop is the browser presentation authority

The new Track A GUI topology is:

```text
browser
  -> HTTPS synology:6902
  -> DSM Reverse Proxy with WebSocket forwarding
  -> HTTPS 127.0.0.1:6901
  -> KasmVNC integrated web server/WebSocket
  -> task-owned persistent Kasm desktop DISPLAY=:1
```

The task-owned deployment identity is fixed:

```yaml
container: otclient-track-a-kasmvnc
runtime_namespace: track-a-kasmvnc-desktop
backend_host: 127.0.0.1
backend_port: 6901
container_port: 6901
internal_display: ':1'
restart_policy: unless-stopped
state_directory: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260818-track-a-persistent-viewer-handoff/kasmvnc
public_url: https://synology:6902/
```

Port `6901` is a loopback backend, not the supported user-facing LAN endpoint. The supported public/LAN entrypoint for this deployment is DSM Reverse Proxy `https://synology:6902/`. The DSM rule must preserve WebSocket upgrade semantics and forward to `HTTPS 127.0.0.1:6901`.

KasmVNC owns the desktop and browser transport. The new desktop path MUST NOT use `x11vnc`, `websockify` or noVNC as an intermediate presentation chain.

The retained PR #528 observer `DISPLAY=:99` / `http://192.168.1.2:6083/` is legacy task-owned state only. It is not the new Track A desktop and must not be attached to, stopped, replaced or republished by the KasmVNC task.

## Isolated deployment boundary

KasmVNC desktop bootstrap is permitted as `runtime_access: ephemeral_isolated` only when the active task declares and verifies its unique container, state directory and backend port. This desktop-only deployment:

- may create/restart only `otclient-track-a-kasmvnc` whose labels prove exact task ownership;
- may bind only host loopback `127.0.0.1:6901` for the Kasm backend;
- must fail closed when that container name or port is owned by an unrelated process/container;
- must not mutate DSM reverse-proxy configuration automatically from repository code;
- must not access or mutate the canonical lease/registration merely to create the desktop;
- must not launch an official Tibia client while another task owns the official-client runtime surface;
- must not touch PR #528 `:99/6083` except optional non-invasive reachability checks.

DSM Reverse Proxy configuration is an operator-owned presentation step. Repository deployment may verify the loopback backend independently, but public desktop health is not `PASS` until `https://synology:6902/` itself is verified from a real HTTPS/WebSocket client path.

## Persistence across agent turnover

The KasmVNC container uses `restart: unless-stopped` and is deliberately not tied to the lifecycle of a GitHub Actions job or ChatGPT session. A replacement worker must discover/reuse the exact task-owned container rather than creating a new desktop because its own `session_id` changed.

Once the official-client runtime is migrated into Kasm under separately admitted ownership, a controller turnover must preserve the Kasm container and desktop. Controller release is not desktop teardown.

## Official-client migration gate

Deploying the desktop does not authorize launching Tibia inside it. Before the official native Linux client is migrated into the Kasm desktop, the current official-client owner must release or explicitly reconcile its runtime surface and current Track A admission must prove the required client/runtime gates.

The migration must ensure the future canonical registration describes the exact client actually running inside the Kasm desktop. No second official-client login/session may be created merely to populate the new desktop.

## Secret boundary

The Kasm deployment must never read or receive:

```text
TIBIA_TEST_EMAIL
TIBIA_TEST_PASSWORD
canonical lease token/capability
Tibia auth/session material
```

The Kasm browser password is a separate temporary desktop credential. It is generated at deployment time, stored only in the task-private state directory with mode `0600`, and is not committed or printed by CI. It is not Tibia authentication authority.

Kasm container metadata/state must not contain Tibia credentials, cookies, session keys, packet payloads or account identifiers.

## Health and failure semantics

Desktop-backend health, DSM presentation health and official-client runtime health are separate facts.

Backend health is proven by at least:

```text
exact task-owned container labels    PASS
container running                    PASS
restart policy unless-stopped        PASS
host 127.0.0.1:6901 mapping          PASS
HTTPS Kasm web application reachable PASS
```

Public presentation health additionally requires:

```text
DSM https://synology:6902 reachable  PASS
DSM reverse proxy destination        HTTPS 127.0.0.1:6901
WebSocket upgrade through DSM        PASS
Kasm login/application usable        PASS
```

A Kasm/DSM presentation failure does not authorize restart/logout/login of an otherwise healthy official client. Likewise, a client failure does not authorize broad Docker cleanup of the desktop.

## Validation gates

Before calling the Kasm backend deployed, physical Synology evidence must prove:

1. `otclient-track-a-kasmvnc` is running on the Docker daemon used by `synology-otclient-01`;
2. exact task/runtime/role labels match;
3. restart policy is `unless-stopped`;
4. `https://127.0.0.1:6901/` serves the KasmVNC application on Synology host loopback;
5. no non-loopback `6901` publication exists;
6. the container remains alive after the deployment GitHub Actions job exits;
7. PR #528 `:99/6083` is not mutated by the deployment;
8. no Tibia secret is accessed and no official client is launched by the desktop-only deployment.

Before calling the browser desktop available to the operator, additionally prove DSM Reverse Proxy `https://synology:6902/`, including authenticated Kasm content and WebSocket forwarding to `https://127.0.0.1:6901`.

Repository controller-handoff tests remain separately required. Integration of the official client into the Kasm desktop is a later physical gate after runtime ownership is available.
