# Restack + native pre-secret source checkpoint — 2026-08-17

## Verified repository state

- PR: `#475`
- branch: `runtime/OTC-20260817-track-a-worldmap-server-delivery-causal-validation`
- pre-change head: `91759e0a8d9db1c2a736c88f7e48d2bb5a3ffc59`
- trusted-base main at restack: `c1adcf491580e28d40f215356a9e559af2ccadc4`
- restack tree was based on current `main` and overlaid only declared task-owned paths.
- PR #475 was re-read after restack and reported `base_sha=c1adcf491580e28d40f215356a9e559af2ccadc4`, `head_sha=91759e0a8d9db1c2a736c88f7e48d2bb5a3ffc59`, `draft=true`, `mergeable=true`.
- No official client was launched and no protected credential was used during the restack.

## Re-admission state before any new physical runtime

```yaml
track_id: official-client-re
runtime_access: ephemeral_isolated
runtime_owner_task: OTC-20260817-track-a-worldmap-server-delivery-causal-validation
runtime_namespace: worldmap-causal-baseline-ephemeral-v1
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
```

`target_uniqueness` is deliberately reset to `UNKNOWN` because trusted-base governance changed across the restack and the admission contract requires re-evaluation. The next physical action is therefore an `inventory_only` run on `synology-otclient-01`; that run must execute no client and use no credential. It must prove both:

1. zero processes carrying the task-owned ephemeral namespace marker; and
2. zero local official-client candidates under the current exact-client fence.

A client launch remains forbidden until that inventory result is persisted.

## Native pre-secret source repair

The task-owned baseline helper is changed so the safety contract is native to `.github/scripts/track-a-worldmap-causal-ephemeral-baseline.sh` rather than being supplied only by a later transformer.

Required source ordering:

```text
no credential-bearing helper environment
-> exact task-owned bootstrap/observer
-> raw-XRes-owned 1020x650 UI identity
-> harmless email editability probe
-> harmless password editability probe
-> both fields cleared
-> protected FIFO created + PRESECRET_READY
-> credential handoff
-> login submission
-> aggregate post-login transition
-> localized character-row interaction
-> structural FullMap/map-description proof
-> WARP/SOCKS confinement
-> reversible Right/Left stimulus
-> exact cleanup/source rehash
```

Legacy OCR/tesseract anchors are forbidden in the native helper.

The workflow is split into explicit manual physical modes:

```text
inventory_only
presecret_only
baseline_login
```

`pull_request` execution performs only deterministic hosted static checks. A protected GitHub secret reference exists only in the `baseline_login` handoff step, which occurs after the pre-secret helper has already produced both editability PASS markers and the protected FIFO ready marker.

## Budget

```yaml
baseline_ephemeral_login_max: 1
baseline_ephemeral_login_consumed: 0
patched_ephemeral_login_max: 1
patched_ephemeral_login_consumed: 0
simultaneous_logged_in_sessions_max: 1
```

No login budget is consumed by restack, static composition, `inventory_only`, or a successful `presecret_only` run stopped before credential handoff.
