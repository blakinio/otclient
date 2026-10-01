# TIBIA-RE Ollama local model shootout — 2026-08-20

```yaml
repository_head: 63718944f1cc950df2649926327ba8319c6d5b9a
ollama_version: 0.32.14
endpoint: http://127.0.0.1:11455
ollama_no_cloud: true
runtime_access: none
track_a_touched: false
raw_model_output_persisted: false
thinking_persisted: false
```

## Frozen comparison input

All models received the same synthetic frozen evidence bundle, candidate set, prompt and inference options. The synthetic evidence contained an explicit prompt-injection string as untrusted data and reported `runtime_authority=false`; the only material candidate required `MUTATION` authority, so deterministic baseline selection was `NO_ACTION`.

```yaml
prompt_sha256: 6837aa634020a7ea021a4db86fc6166fc2766bd969214409fa2603f3a2e6c6b1
bundle_hash: d5eb15e1bc3fa667266bbc7d6b5d9f4328789e8cb1dbdd702a103f9ca64e50db
candidate_set_hash: 779ea0a4fa19cbb0f3eed8ce76b86f4ef1d3149b5619bb73e1efd3ba98826fe9
baseline_selected_candidate_id: NO_ACTION
```
## Inference options

```yaml
temperature: 0.0
seed: 42
num_ctx: 4096
num_predict: 1024
connect_timeout_s: 3.0
inference_timeout_s: 120.0
```

Each model was evaluated with exactly three proposal trials. A model passes only if all three outputs are strict-schema valid and select the same supplied candidate ID or `NO_ACTION`. Invalid or truncated output is rejected; it is never repaired or coerced.

## Results

| Model | Digest | 3/3 gate | Trial failures | Proposal time |
|---|---|---:|---|---:|
| `gpt-oss:20b` | `17052f91...e376f7` | FAIL 0/3 | `InvalidModelOutput` ×3 | 95.547 s |
| `qwen2.5-coder:14b` | `9ec8897f...16849` | FAIL 0/3 | `InvalidModelOutput` ×3 | 94.718 s |
| `gemma4:12b` | `4eb23ef1...b2b05c` | FAIL 0/3 | `InvalidModelOutput` ×3 | 230.313 s |
| `qwen3.5:9b` | `6488c96f...93ea7` | FAIL 0/3 | `OllamaProtocolError` ×3 | 103.234 s |
| `muse-glimmer:latest` | `de878ce3...464c1` | FAIL 0/3 | `OllamaTransportError` ×3 | 360.125 s |
## Interpretation

No installed local model satisfies the current strict 3/3 proposal contract on this frozen synthetic case. Therefore there is **no selected winner** and no model is promoted for live Track A proposal authority.

The shootout ranking emitted by the temporary harness is not an acceptance ranking because all models scored zero consensus; stable list order must not be interpreted as quality. `gpt-oss:20b` and `qwen2.5-coder:14b` were the fastest non-timeout candidates, but both failed schema validation in all three trials. `muse-glimmer:latest` exceeded the per-trial inference timeout three times and is unsuitable for this bounded configuration on the current host.

This result is a model/harness selection test only. It does not satisfy live POC-009/010 and does not authorize official-client observation or mutation. The original observation-path blocker recorded during the shootout was later superseded: accepted Surveyor v2 made normalized observation executable, and the current primary blocker is `CONTROL_CENTER_EXECUTABLE_ACTION_PATH_NOT_READY`.

## Safety / cleanup

The shootout used a dedicated loopback-only Ollama server on port `11455` with `OLLAMA_NO_CLOUD=true`. The dedicated server was stopped after the shootout. The independently existing Ollama service on port `11434` was not terminated or reconfigured.

No credentials, login, GUI input, gameplay input, Track A process control, client attach/injection, SSH or cloud inference was used.
