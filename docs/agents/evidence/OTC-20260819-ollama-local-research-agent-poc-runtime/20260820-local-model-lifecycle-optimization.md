# TIBIA-RE Ollama PoC — local model lifecycle optimization

```yaml
revalidated_at: 2026-08-20T12:47:00+02:00
trusted_main: 272ea49f5bf2d8651e22dfa776537e8ea61758e2
runtime_access: none
official_client_touched: false
owner_policy: max_one_loaded_model
```

## Trigger

A live `ollama ps` check showed two models loaded concurrently on Molehill-PC (`qwen2.5-coder:14b` and `qwen3.5:9b`). The owner required that this PoC load at most one model at a time and stop leaving heavy models resident after tests.

Both loaded models were explicitly stopped before further model work. A follow-up `ollama ps` returned an empty model table, proving the local GPU/model slot was released.

## Harness changes

`tools/tibia_re_ollama_poc/client.py` now adds a fail-closed local-model lifecycle boundary:

- `loaded_models()` reads `/api/ps`;
- `assert_single_model_slot(tag)` refuses a generation if any different model is already loaded or more than one model is resident;
- `InferenceOptions.keep_alive_s` defaults to 15 seconds and is bounded to `0..60`;
- every generate request sends the bounded keep-alive value;
- `unload_model(tag)` requests an Ollama unload with `keep_alive=0`;
- `model_session(tag)` guarantees best-effort deterministic unload on session exit after checking the current loaded-model set.
## Validation

```text
python -m unittest discover -s tests/tools/tibia_re_ollama_poc -v
25/25 PASS

python -m compileall -q tools/tibia_re_ollama_poc tests/tools/tibia_re_ollama_poc
PASS

git diff --check
PASS
```

New regression coverage proves:

- concurrent different-model residency is rejected before inference;
- the target model alone is accepted;
- model-session exit invokes unload;
- keep-alive above the bounded limit is rejected;
- generate requests carry the short `15s` keep-alive;
- existing loopback, timeout, digest, strict-output and safety tests remain green.

This optimization changes only Molehill-PC model resource management. It creates no Track A authority and does not change the primary programme blocker `CONTROL_CENTER_EXECUTABLE_ACTION_PATH_NOT_READY`.
## Shared-service root cause and global fix

The duplicate-residency condition recurred after the harness fix because another local adjudicator used the same port `11434`, while the active Ollama service had been started through `ollama app.exe -> ollama.exe serve` instead of the supervisor entrypoint. That bypassed the supervisor's existing `OLLAMA_MAX_LOADED_MODELS=1` setting.

The separate adjudicator process was allowed to finish before service restart. The extra model was stopped and the GPU slot was emptied first.

The supervisor entrypoint `scripts/ollama-server.ps1` was then hardened from indefinite residency (`OLLAMA_KEEP_ALIVE=-1`) to `OLLAMA_KEEP_ALIVE=15s`. User-scoped `OLLAMA_MAX_LOADED_MODELS=1` was also persisted.

Ollama was restarted through the supervisor script. The resulting server log proves:

```text
OLLAMA_MAX_LOADED_MODELS:1
OLLAMA_NUM_PARALLEL:1
OLLAMA_KEEP_ALIVE:15s
OLLAMA_MODELS:<supervisor-managed model store>
```

Post-restart verification:

```text
/api/version = 0.32.14
/api/ps loaded model count = 0
```

This makes the max-one-model rule effective at both harness and shared-server layers without interrupting the unrelated adjudicator while it was still active.
