# Final Wave 3 Vision P2 live E2E

Observed on 2026-09-03 after central client-fence reconciliation and fresh Surveyor run `33718302097` / artifact `9879312832`.

- Audited Wave 2 head: `9db0ae43ab5b0ce6b0c9504eec723087f13d5271`.
- Wave 3 restack head before evidence checkpoint: `b3186d06dafffe28d6796cf1f12e0c0fe7fd6ca9`.
- Surveyor identity: client PID `28379`, start ticks `36180734`, XID `31457303`, boot-id SHA-256 `a6b053cc7bf4d6fffa302419b4a1d6fe5ae336c6de92abefeae27e8aa61c624a`.
- Exact current fence: `15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- KasmVNC: `Connected (encrypted)`, `view_only=true`, remote framebuffer `3440x1229`.
- Exact model: `qwen3-vl:4b-instruct-q4_K_M` at digest `ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b`; model slot was empty before and after accepted inference.

The first capture attempt was discarded as `NON_EVIDENCE_CONSUMER_STARTUP_FAILURE`: the Python consumer lacked `PYTHONPATH`, exited before reading the frame, Qwen/reconciliation did not run, and no raw frame was persisted. The isolated harness environment was corrected without product/repository changes.

The accepted evidence-bearing run captured one encrypted view-only framebuffer image in memory, decoded it to RGB in memory, and passed it through the production trusted full-frame mask before persistence. The only persisted image is the secret-safe masked PNG `b73b2b2c6626a91f03744b76f9ba59761c5122f047cfacd4c755bb15467393bc.png`, `762x272`, 683 bytes; every RGB byte is zero. Raw frame persistence is false.
Recovered durable `VISION_RECONCILED` event from the task-owned SQLite store:

```yaml
screen_class: UNKNOWN
reconciliation_state: UNKNOWN
runtime_state: UNKNOWN
runtime_current: false
runtime_evidence_refs: []
visual_evidence_refs:
  - capture:b73b2b2c6626a91f03744b76f9ba59761c5122f047cfacd4c755bb15467393bc
model_profile_id: ollama:qwen3-vl:4b-instruct-q4_K_M@sha256:ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
physical_effect: false
physical_action_count: 0
```

The runtime admission provenance remains the frozen fresh Surveyor observation (`observed_at_epoch_ms=1788412746000`); it was not rewritten to pretend current semantic runtime evidence. No reviewed runtime signal was manufactured, so `runtime_current=false` is the required fail-closed result.

No credentials, login/relogin, character selection, gameplay, GUI input, anti-idle input, process control, process-memory access, packet capture, client mutation or semantic promotion occurred. Cleanup verified resident models `[]`, stopped the exact task-owned Ollama and headless Kasm viewer processes, and left the Ollama loopback API down.

Classification: `PASS_EXPECTED_UNKNOWN_RUNTIME_NOT_CURRENT`. The required physical Vision P2 capture -> exact Qwen -> `reconcile_vision()` evidence is complete.