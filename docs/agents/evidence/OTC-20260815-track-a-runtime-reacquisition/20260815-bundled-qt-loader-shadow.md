# Track A RUNTIME bundled Qt loader precedence failure

Task: `OTC-20260815-track-a-runtime-reacquisition`  
Draft PR: `#303`  
Execution head: `cd39eccbcb57c5ac4abf7bbb89cb89e01caaedba`  
Run: `31887680537`  
Job: `95019260014`  
Runner: `synology-otclient-01`  
Conclusion: `FAILURE`  
Artifact: `track-a-runtime-reacquisition-31887680537`  
Artifact id: `9247723963`  
Artifact ZIP SHA-256: `9abf5de9d5066cf28db6fb036228491cdc00619e39682858c59cc846f51844e9`

## FACT — libpxbackend repair passed

Run #18 passed the exact request/baseline fence, pinned runtime-materializer rehydration, explicit verification of the existing `libpxbackend-1.0.so`, materialization of its exact `libproxy` directory into the client loader path, exact run-16 residue recovery, bootstrap and cross-step relay/Xvfb persistence.

The exact client was verified and discovered as a no-secret `client-gen-1` process:

```text
TRACK_A_EXACT_CLIENT_VERIFIED size=51965216 sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
TRACK_A_CREDENTIAL_ENV_CLEAR role=client-gen-1 pid=27793
TRACK_A_RUNTIME_ROLE_DISCOVERED role=client-gen-1 pid=27793 launcher_pid=27793
```

Therefore the previous `libpxbackend-1.0.so` failure is closed for this materialization generation.

## FACT — official bundled Qt was shadowed by toolroot Qt

`Prepare generation 1` failed only after client launch because no Tibia window appeared. The sanitized artifact `gen1-client.log` explains why: the runtime loader selected toolroot `libQt6Core.so.6`, which does not provide `Qt_6.9`, while the exact official package's dependent Qt libraries are under the copied package's `bin/lib/` directory.

Representative failure:

```text
client: /work/_otclient_tibia_re_state/toolroot/usr/lib/x86_64-linux-gnu/libQt6Core.so.6: version `Qt_6.9' not found
```

The same line is reported against official package libraries such as `bin/lib/libQt6WebEngineQuick.so.6`, `libQt6Quick.so.6`, `libQt6Qml.so.6` and related bundled Qt libraries.

This independently reproduces the already-known Track A boundary: toolroot libraries are support/tool dependencies and must not override the official client's bundled Qt runtime.

## Side-effect boundary

- protected login step was skipped;
- no credential values were supplied to client login;
- no movement or gameplay/economic action occurred;
- no structural map records were produced;
- the result is a loader-order failure, not a gameplay/world-state semantic result.

## Required repair

Keep the proven toolroot and `libproxy` support paths, but place the exact copied package `bin/lib` first in `LD_LIBRARY_PATH` for the official client process. Do not install/download another Qt build and do not weaken the exact client fence.

The next run must also use explicit current-run cleanup/snapshot code rather than executing unevaluated `${{ ... }}` expressions extracted from historical workflow YAML.
