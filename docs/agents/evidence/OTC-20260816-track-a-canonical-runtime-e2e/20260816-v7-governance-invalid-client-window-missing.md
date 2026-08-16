# Track A canonical runtime v7 — governance-invalid fail-closed attempt

## Exact run

- PR: `#405`
- branch: `ci/OTC-20260816-track-a-canonical-runtime-e2e-v7`
- workflow head: `8f560e0d3a87e9f6a6b599bb276b7b25d9588e53`
- workflow run: `31960965493`
- job: `95198777325`
- runner: `synology-otclient-01`
- repository CI: `31960965583` = `SUCCESS`
- Track A governance: `31960965481` = `FAILURE`

## Governance classification

The deterministic admission-policy audit rejected the active task before this attempt could be considered policy-compliant:

```text
Track A runtime admission invalid: bootstrap is not currently implemented/authorized
```

Current governance for `runtime_access: canonical_bootstrap` requires `mutation_authorized: false`; v7 task metadata incorrectly set `mutation_authorized: true` while dispatching the one-shot workflow.

Therefore:

- this run MUST NOT be represented as a governance-compliant canonical bootstrap;
- it MUST NOT authorize a retry or any further physical mutation;
- any observations below are retained only as fail-closed physical evidence from an execution that occurred while the deterministic governance gate was red.

## Physical observations

Before mutation the workflow fenced exact trusted base `main@778e13306d93297025abf8e4e970e91ac9830a36` and proved:

```text
RUNTIME_TRUSTED_WORKER_WAIT_CONTRACT=PASS
RUNTIME_TRUSTED_WORKER_GRAPHICS_CONTRACT=PASS
RUNTIME_SUPPORT_ROOT_PREFLIGHT=PASS
RUNTIME_SYSTEM_XKBCOMP_PREFLIGHT=PASS
```

Pre-admission lease state was released at generation `5`. The workflow then acquired generation `6`:

```text
TRACK_A_CANONICAL_LEASE_ACQUIRE=true
TRACK_A_CANONICAL_LEASE_GENERATION=6
```

The trusted worker progressed through:

```text
TRACK_A_CANONICAL_STAGE=warp_start
TRACK_A_CANONICAL_STAGE=wireproxy_configtest_start
TRACK_A_CANONICAL_STAGE=wireproxy_configtest_pass
TRACK_A_CANONICAL_STAGE=warp_egress_probe_start
TRACK_A_CANONICAL_STAGE=warp_egress_probe_pass
TRACK_A_CANONICAL_STAGE=warp_pass
TRACK_A_CANONICAL_STAGE=xvfb_start
TRACK_A_CANONICAL_STAGE=xvfb_pass
TRACK_A_CANONICAL_STAGE=vnc_start
TRACK_A_CANONICAL_STAGE=vnc_pass
TRACK_A_CANONICAL_STAGE=client_start
TRACK_A_CANONICAL_STAGE=client_window_wait_start
```

After the bounded 30-second wait it failed closed:

```text
TRACK_A_CANONICAL_SESSION_ERROR=client_window_missing
TRACK_A_CANONICAL_TRANSITION_ERROR=bootstrap_worker_failed
```

## Result boundary

- graphics source contract after #402: `PASS`;
- support root/xkbcomp: `PASS`;
- WARP: `PASS`;
- Xvfb: `PASS`;
- VNC: `PASS`;
- exact client start stage: reached;
- visible `^Tibia$` window within bounded wait: not found;
- canonical registration: not published;
- Gate B: not reached;
- credentials/login/gameplay: not used;
- controller lease cleanup: workflow exit trap attempted release; generation advances to `6` and no success claim is made.

## Interpretation

`QT_XCB_GL_INTEGRATION=none` removal alone did not produce a visible Tibia window during this attempt. This does **not** prove that the graphics fix is ineffective in all conditions, nor does it identify the actual runtime GLX/EGL/RHI backend, because the worker does not surface the task-owned `client.log`/`QSG_INFO` output on bootstrap failure.

The next legitimate step is governance-compliant, non-canonical diagnostic/research that obtains bounded `QSG_INFO`/GLX/EGL/backend evidence without canonical mutation, or a governance change/implementation that explicitly authorizes canonical bootstrap. No further canonical bootstrap retry is authorized from this task checkpoint.
