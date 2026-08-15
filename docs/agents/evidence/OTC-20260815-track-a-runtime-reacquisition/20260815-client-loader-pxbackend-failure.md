# Track A RUNTIME exact client loader dependency failure

Task: `OTC-20260815-track-a-runtime-reacquisition`
Draft PR: `#303`
Execution head: `527369447672a355b6fc0a3f8a4f9c2b39f33b67`
Run: `31885896845`
Job: `95015034558`
Runner: `synology-otclient-01`, id `21`
Conclusion: `FAILURE`
Artifact: `track-a-runtime-reacquisition-31885896845`
Artifact id: `9247260124`
Artifact ZIP SHA-256: `4d62e9ed8e7dc12600db4b24f5881a210216dc18963ace8a162ef07d8f810edc`

## FACT — infrastructure and materialization gates passed

The run passed the structural effective-helper materializer, exact failed-run residue recovery, bootstrap and cross-step persistence before generation 1. Therefore the previously proven runner selector, source-state, upstream WARP, task-local relay, XKB/Xvfb and workflow-step persistence repairs remained effective.

The protected login step was **skipped** because `Prepare generation 1` failed first. Generation 2 was not entered.

## FACT — sanitized artifact proves exact loader failure

The sanitized `gen1-client.log` contains only proxychains initialization followed by the dynamic loader failure:

```text
[proxychains] config file found: /home/runner/_work/_otclient_tibia_re_state/tasks/OTC-20260815-track-a-runtime-reacquisition/runs/31885896845/proxychains.conf
[proxychains] DLL init: proxychains-ng 4.17
[proxychains] DLL init: proxychains-ng 4.17
client: error while loading shared libraries: libpxbackend-1.0.so: cannot open shared object file: No such file or directory
```

The artifact also contains an empty `gen1-map-records.tsv`, consistent with the client failing before any structural world signal.

`workflow-terminal.txt` confirms the exact run/head/client fence and current-run ownership mode:

```text
workflow_status=failure
workflow_run_id=31885896845
workflow_head=527369447672a355b6fc0a3f8a4f9c2b39f33b67
runner=synology-otclient-01
expected_client_sha256=e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
expected_client_size=51965216
current_run_ownership=true
```

## Side-effect classification

### FACT

- no protected login step ran;
- no credential values were injected into a login action;
- no movement or gameplay/economic action occurred;
- no structural world records were produced;
- the failure is a missing dynamic-loader search path for `libpxbackend-1.0.so`, not a direct-position or world-state semantic result.

The job payload reports final cleanup `FAILURE`; the exact historical cleanup stderr is not inferred here. A separate read-only diagnostic is tasked with establishing current residue state before any recovery mutation.

## Current discriminator

Read-only run `31886223175` / job `95015803600` at diagnostic head `5b213ca776cbf55a235742f8a799000d41e4dc02` is locating the exact `libpxbackend-1.0.so*` file under the proven source state and inspecting run `31885896845` residue without starting, stopping or signalling runtime processes.

The next runtime repair must use the diagnostic's exact library location; do not guess or install/download a replacement dependency.
