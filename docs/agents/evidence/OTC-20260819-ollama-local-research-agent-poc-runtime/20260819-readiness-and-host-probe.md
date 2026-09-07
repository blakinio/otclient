# TIBIA-RE Ollama local research-agent PoC — readiness and host evidence

```yaml
evidence_version: 1
invocation_date: 2026-08-19
repository: blakinio/otclient
trusted_base_sha: c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd
prompt_contract_version: 1.1.0
result: PARTIAL
poc_technical_result: FAIL
research_value_verdict: INCONCLUSIVE
first_blocker: CONTROL_CENTER_EXECUTABLE_OBSERVATION_PATH_NOT_READY
runtime_access: none
credentials_accessed: false
client_input_sent: false
client_process_control: false
client_attach_or_injection: false
login_performed: false
gameplay_action_performed: false
```

## Directly verified repository state

- `main` advanced during the invocation from `fdabf235ed4438bd7c376932ed876bd0bbef019a` to `3cb5d52c06b03f5db496d71e9b6945dbf9d3b0bd` for Surveyor v2 prompt/documentation and then to `c9156e72aa3c647054ff9dfc5ffed00e43a7e9cd` for prompt-publication lifecycle archival. Neither newer commit adds the executable collector, Control Center core or official mutation adapter.
- PR #605 is still Draft/Open and documentation/contracts-only. Its phase order still puts executable Control Center implementation after its independent-audit gate.
- PR #592 is still Draft/Open. Its branch contains a Surveyor implementation and historical/current-session evidence, but open Draft content is not trusted-base executable authority for this PoC.
- PR #610 is still Draft/Open and owns current canonical-runtime adoption/reconciliation. This invocation did not inspect or mutate that owned official-client runtime surface.
- `docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md` on trusted base is `status: design_baseline`.
- the stable `tools/tibia_runtime_bridge` documents a read-only API and a reusable profile only for the superseded `e6c244...` exact-client fence; it does not provide a stable current-fence action API.
- trusted-base coverage registry inspection produced zero matches for promoted action gates `A2`, `A3` or `A4`.

## Hard readiness gate

```yaml
normalized_observation_executable: false
bounded_action_policy_executable: false
dispatch_preflight_executable: false
evidence_store_executable: false
runtime_identity_fencing_executable: true
stop_cancellation_semantics_executable: true
chosen_experiment_supported: false
```

The first false prerequisite is executable normalized observation. The canonical prompt requires fail-closed `PARTIAL` rather than implementing a replacement Control Center inside this task.

## Molehill-PC and local Ollama

Remote Desktop Commander directly identified `Molehill-PC` as an online authorized device at the beginning of the invocation.

Direct local API/CLI probes returned:

```yaml
ollama_version: 0.32.14
endpoint_version: 0.32.14
endpoint: http://127.0.0.1:11434
gpt_oss_20b:
  installed: true
  digest: 17052f91a42e97930aa6e28a6c6c06a983e6a58dbb00434885a0cf5313e376f7
  reported_context_length: 131072
  parameter_size: 20.9B
  quantization: MXFP4
qwen3_5_9b:
  installed: true
  digest: 6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7
  reported_context_length: 262144
```

A bounded `gpt-oss:20b` generation command was attempted. The remote command channel did not return a response within its 60-second tool window; subsequent Remote Desktop Commander calls to Molehill-PC also timed out. No model response was observed. Therefore:

```text
OLLAMA_INFERENCE_RESULT=NOT_ESTABLISHED
```

This is not classified as a model failure. The earlier hard readiness failure already forbids progressing into proposal/action execution, so no retry was performed.

## Molehill-PC to Synology boundary

A bounded HTTPS probe from Molehill-PC to the trusted-base KasmVNC observer locator returned HTTP `200`, with approximately `0.015 s` connect time and `0.662 s` total time. This proves only current network reachability of that endpoint.

The current trusted-base KasmVNC access contract specifies Remote Desktop Commander device `Synology` as the physical-runtime discovery path. An explicit device ping reported that device offline during this invocation. Therefore:

```yaml
synology_network_reachability: PROVEN_FOR_OBSERVER_ENDPOINT
approved_runtime_discovery_transport: NOT_PROVEN
current_track_a_runtime_identity: UNKNOWN_NOT_OBSERVED
current_track_a_admission: NOT_EVALUATED_RUNTIME_ACCESS_NONE
```

No undocumented SSH fallback or credential-based access was used.

## Safety result

This invocation remained repository/environment discovery only with `runtime_access:none`. It did not cross PR #610 runtime ownership, did not touch the official client, and did not expose arbitrary shell, SSH, credentials, login, process control or gameplay capability to the local model.
