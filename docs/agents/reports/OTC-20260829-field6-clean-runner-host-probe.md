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

## Terminal physical result

Trusted-main workflow run `33261106292`, job `99123092884`, head `6ea7b6291f6606d04f980dd758b91aa451fc867f`, event `workflow_dispatch`, completed success. Sanitized output:

```text
TRACK_A_FIELD6_HOST_PROBE_ADMISSION=PASS
RUNNER_PROBE_DOCKER_CLI=true
RUNNER_PROBE_DOCKER_SOCKET=true
RUNNER_PROBE_DOCKER_SOCKET_RW=true
RUNNER_PROBE_DOCKER_SERVER=true
RUNNER_PROBE_SUDO_DOCKER=false
RUNNER_PROBE_INSIDE_CONTAINER=true
RUNNER_PROBE_REMOTE_CONTROL_MATCH_COUNT=0
TRACK_A_FIELD6_HOST_PROBE_MUTATION=false
TRACK_A_FIELD6_HOST_PROBE_SECRETS=false
TRACK_A_FIELD6_HOST_PROBE=PASS
```

## Security classification

The historical repository runner had read/write access to the host Docker socket. Repository PR-controlled code therefore had a path to host-equivalent Docker mutation; historical contamination cannot be bounded to runner `_work` or container state. A fresh runner container on this same unverified host is **not** clean secret provenance. The exact V4 trigger remains forbidden and `FIELD6_VALUE=UNKNOWN`; V4 `physical_action_count` remains `0`.

The count of remote-control-name matches was zero; this does not prove absence of host persistence because names are neither exhaustive nor an integrity mechanism.
