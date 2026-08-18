# Track A Controller Handoff and Persistent KasmVNC Desktop Contract v3

```yaml
track_a_controller_handoff_and_viewer_version: 3
track_id: official-client-re
repository: blakinio/otclient
runtime_platform: official_native_linux_only
browser_desktop_provider: KasmVNC
public_frontend: DSM_reverse_proxy
status: proposed_until_PR_541_merge
```

This contract extends, and never weakens, `TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`, `TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md` and ADR-0001. Until PR #541 is reviewed and merged, repository changes here do not expand live official-client authority.

## Canonical viewer decision

Track A has one canonical browser desktop architecture:

```text
browser
  -> HTTPS synology:6902
  -> DSM Reverse Proxy + WebSocket + Authorization forwarding
  -> HTTPS 127.0.0.1:6901
  -> stock KasmVNC integrated HTTPS/WebSocket server
  -> persistent Kasm desktop DISPLAY=:1
```

Agents MUST NOT provision, restore, recommend, or treat `x11vnc`, standalone `websockify`, or noVNC as the Track A viewer. References to historical VNC/noVNC endpoints are legacy evidence only, not current viewer authority. Do not infer that a historical `:98`, `:99`, `6082`, or `6083` endpoint is the current desktop.

The legacy PR #528 observer `DISPLAY=:99` / `http://192.168.1.2:6083/` may exist until its owning task removes it, but it is explicitly non-canonical and must not be reused or mutated by unrelated workers. The replacement viewer is KasmVNC, not a new noVNC instance.

## Purpose and identities

The GUI desktop is a durable programme resource instead of an artifact of one agent/job. A replacement agent gets a fresh controller session/capability while reusing the same KasmVNC desktop/container and browser endpoint.

Keep identities separate:

```text
runtime    = exact registered official client identity when one exists
controller = task + current disposable session + capability + lease generation
desktop    = task-owned KasmVNC container + internal display + loopback backend
frontend   = DSM reverse-proxy rule + stable HTTPS hostname + WebSocket/Auth forwarding
```

A historical agent `session_id` is never desktop identity. Controller release/replacement is not desktop teardown.

## Mandatory controller replacement

The supported canonical controller entry point remains:

```text
python3 .github/scripts/tibia-official-client-re-canonical-live-resume.py resume --task-id <task>
```

For an active fresh lease owned by the same task but a prior agent session, replacement is explicit and requires a reason:

```text
python3 .github/scripts/tibia-official-client-re-canonical-live-resume.py \
  resume --task-id <same-task> --replace-active-same-task \
  --reason '<verified recovery reason>'
```

The handoff must fail closed: same task only, current capability required, exact expected generation required, capability rotated, generation incremented, old capability invalidated at commit, and canonical coordination serialization preserved. Expired leases use the reviewed stale-takeover path. Different-task ownership remains a refusal.

When canonical official-client registration survives across controller generations, reviewed generation rebind and Gate B remain mandatory. The default reuse/Gate-B window proof is raw XRes, not `xdotool --pid`.

## Fixed KasmVNC deployment identity

```yaml
container: otclient-track-a-kasmvnc
image: kasmweb/ubuntu-noble-desktop:1.17.0
runtime_namespace: track-a-kasmvnc-desktop
backend_host: 127.0.0.1
backend_port: 6901
container_port: 6901
internal_display: ':1'
restart_policy: unless-stopped
state_directory: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260818-track-a-persistent-viewer-handoff/kasmvnc
public_url: https://synology:6902/
```

`6901` is a loopback backend only. The supported operator endpoint is `https://synology:6902/`.

The self-hosted Actions runner is itself containerized. Therefore `127.0.0.1` inside `otclient-synology-runner` is NOT Synology/Docker-host loopback. Agents validating the backend from Actions must use a host-network probe (or another explicitly proven Docker-host namespace path) rather than interpreting runner-container `curl https://127.0.0.1:6901` failure as backend failure.

## DSM Reverse Proxy contract

Operator-owned DSM configuration is:

```text
SOURCE:
  protocol: HTTPS
  host: synology
  port: 6902

DESTINATION:
  protocol: HTTPS
  host: 127.0.0.1
  port: 6901

CUSTOM HEADERS:
  Upgrade: $http_upgrade
  Connection: $connection_upgrade
  Authorization: $http_authorization
```

`Authorization: $http_authorization` is required. Physical testing proved that DSM could reach KasmVNC and return its `401 Websockify` challenge while authenticated requests still remained `401` until the incoming Authorization header was explicitly forwarded. After adding this header, the operator confirmed the browser login works.

Repository automation must not silently mutate DSM global Reverse Proxy configuration. If DSM returns `502`, distinguish DSM upstream connectivity from Kasm backend health. If unauthenticated DSM returns Kasm's `401` but correct credentials through DSM still return `401`, verify Authorization forwarding before rotating credentials or recreating Kasm.

## Secret boundary and operator credential

Kasm browser authentication is independent of Tibia authentication. The username is `kasm_user`. The password is generated once into the task-private state file `browser-password`, mode `0600`, and reused with the persistent container. Never commit, print, upload, or place its value in CI logs.

The runner is containerized; the task-private state file is inside `otclient-synology-runner`, not necessarily directly visible at the same path in a DSM host shell. If the owner needs the credential, direct them to read that exact private file locally from the runner container. Never expose the value through public CI.

The Kasm deployment must never read or receive `TIBIA_TEST_EMAIL`, `TIBIA_TEST_PASSWORD`, canonical lease capability, or Tibia auth/session material. Kasm metadata/state must not contain Tibia credentials, cookies, session keys, packet payloads or account identifiers.

## Isolated deployment boundary

Kasm desktop bootstrap is permitted as `runtime_access: ephemeral_isolated` only when admission verifies the unique container, state directory and backend port. It may create/restart only the exact task-owned Kasm container, bind only host loopback `127.0.0.1:6901`, and must fail closed on conflicting ownership. It must not mutate the canonical official-client lease merely to create the desktop, must not start a second official client, and must not touch legacy #528 runtime except optional read-only reachability checks.

Deploying the desktop does not authorize launching Tibia inside it. Migration of the official client into Kasm requires separately admitted current runtime ownership and must preserve the one-official-client invariant.

## Health and physical E2E

Desktop backend, DSM presentation, and official-client runtime health are separate facts. Presentation failure never authorizes restarting/logging out the official client.

Before claiming Kasm backend deployed, physical evidence must prove:

1. `otclient-track-a-kasmvnc` running on the Docker daemon used by `synology-otclient-01`;
2. exact task/runtime/role labels;
3. `restart=unless-stopped`;
4. stock Kasm `Xvnc` and `DISPLAY=:1` with the expected X11 socket;
5. Synology/Docker-host `https://127.0.0.1:6901/` responds as Kasm HTTPS;
6. publication remains loopback-only;
7. persistent container identity survives agent/job turnover;
8. no PR #528 mutation, no Tibia secret access, and no second official client launch.

Before claiming browser presentation available, additionally prove:

1. authenticated `https://synology:6902/` returns the real Kasm application, not DSM 404/502;
2. backend Kasm WebSocket upgrade succeeds;
3. DSM-forwarded WebSocket upgrade succeeds;
4. operator can obtain the real persistent Kasm desktop;
5. an independent post-deploy job re-proves persistence after the deploy job exits.

Repository controller-handoff and raw-XRes tests remain separately required. Exact-head required CI, independent audit, review-thread cleanup, governance closeout, task archival and ownership release remain mandatory before DONE/merge according to repository governance.
