# OTC-20260829 field6 clean-runner host probe

## Causal RED

Before implementation:

```text
CLEAN_RUNNER_HOST_PROBE_RED: missing .github/workflows/track-a-field6-clean-runner-host-probe.yml
```

## Scope

The implemented probe is deliberately read-only and credential-free. It cannot be used as cleanliness attestation; it only discovers whether the historical runner can reach a host-control mechanism required for later clean one-job runner provisioning.

The stale 2026-08-16 Xvfb diagnostic authority is revoked in the same reconciliation because its workflow was already removed and cleanup terminal. No official client, login submit, GUI action, packet capture, secret, or physical action is allowed by this probe.

## Pre-restack hosted validation

Exact head `3c754db171492fd6d0ee34d222d9d4498de16260` passed host-probe contract run `33260924525`, governance `33260924519`, reusable self-hosted boundary/audit `33260924524`, and CI `33260924605`. Protected main remained `08c31195fd2f44224badf1b6bdff85192495898b`.

Final one-commit restack and exact-head rerun remain authoritative for merge.
