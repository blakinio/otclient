# 2026-08-29 independent post-implementation audit ? TIBIA RE Vision Benchmark

```yaml
audited_head: 7621916c76c19aa0951384538a8387c02cafcd04
base_main: f208a20cb4517e8b57bef91983337145d379267c
validator_role: fresh_coordinator_validator
trust_worker_summary: false
result: PASS_BOUNDED
material_findings_open: 0
benchmark_result_confirmed: PARTIAL
primary_model_confirmed: null
ocr_fallback_model_confirmed: null
research_value_verdict_confirmed: INCONCLUSIVE
```

## Scope reviewed

The validator re-read the task acceptance boundary, complete changed-path inventory, benchmark core/adapters/runners/tests, frozen manifests, primary Qwen/Ovis evidence, terminal report, live Track B boundary and current local model residency. It did not treat the implementer completion narrative as proof.

Exact changed paths are confined to the declared benchmark tool, evidence, report, task and plan roots. `git diff --check origin/main...HEAD` passed. The final audited implementation had no repository writes outside `blakinio/otclient`, no Synology/official-client runtime effects, no credentials/login/gameplay/process authority and no cloud inference.

## Findings and disposition

### VISION-EXEC-AUD-001 ? empty evidence could vacuously pass hard gates ? resolved

`evaluate_hard_gates([])` originally inherited Python `all([]) == True`. TDD now requires an empty trial set to be ineligible with `failure_reasons: [no_trials]`.

### VISION-EXEC-AUD-002 ? caller-declared capture hash was not byte-bound ? resolved

The Ollama adapter originally accepted a syntactically valid caller SHA without checking the image bytes. TDD now proves a mismatch is rejected before `/api/chat`; `run_ollama_trial()` recomputes SHA-256 and fails closed.

### VISION-EXEC-AUD-003 ? Qwen warm runner cleanup was not self-contained ? resolved

The warm suite previously relied on an external shell unload after keeping the model warm. The runner now performs exact-target-only release through Ollama `keep_alive: 0`, verifies `/api/ps` empty, records the normal-path unload result and registers best-effort exit cleanup without touching a different resident model. The final real suite proves empty residency after explicit unload.

### VISION-EXEC-AUD-004 ? Ovis input safety/hash checks used Python `assert` ? resolved

The Ovis runner no longer relies on assertions that disappear under `python -O`. Both Qwen and Ovis use shared `validate_input_manifest()`, which enforces `secret_safe: true` and exact image-byte SHA binding.

### VISION-EXEC-AUD-005 ? Qwen profile digest was supplied but not independently bound ? resolved

The harness now queries local Ollama `/api/tags`, requires one exact installed model identity and validates the 64-hex digest before inference. The final real suite used digest `ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b`.

### VISION-EXEC-AUD-006 ? repeatability count could be reduced below contract ? resolved

Both real-model runners now require integer `trials >= 3`; zero/two/bool values are tested fail-closed.

### VISION-EXEC-AUD-007 ? fixture generator did not reproduce frozen scored bytes ? resolved

Two fresh generator runs produced the same SHA `cc485d0af96acc4a6d464783819477194c8604267871baa1303855ed0041a782`, but not the scored fixture SHA `2dea29719c3e6f7c84c40717ead27bd56cfaacb69b06c4f19f0975b231bc47a6`. The helper was removed instead of falsely claiming reproducibility. The committed PNG plus manifest SHA remain immutable benchmark input.

## Independent verification

- `python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -v`: **34/34 PASS**.
- `python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md --require-checkpoint`: **PASS**.
- `git diff --check origin/main...HEAD`: **PASS**.
- Frozen login/black fixture SHA recomputation: **PASS**.
- Final Qwen evidence assertions: **PASS** ? 6 requests, login 3/3, text recall 1.0, black false text 0/3, false in-game 0/3, hard gates eligible, explicit unload empty.
- OvisOCR2 evidence assertions: **PASS** ? revision fixed, recall 1.0, black false text 3/3 in each prompt profile, selection-quality false.
- Ovis2.5 backend classification assertion: **PASS** ? `UNSUPPORTED_BACKEND` for the current host/profile.
- Quick diff secret scan for private-key/test-credential/session-value patterns: no match.
- `ollama ps` and `docker model ps`: empty.

One audit assertion command initially used the wrong JSON key (`profiles` instead of `candidates`) and raised `KeyError`; the command was corrected and the complete evidence assertion set then passed. This was a validator-command defect, not a product/evidence finding.

## Verdict

The implemented harness and measured evidence support only `PARTIAL`. Qwen is the leading candidate for the future representative Track B benchmark, but synthetic smoke cannot promote it to `primary_model`. OvisOCR2 is not promoted as fallback because the repeated black negative-control failure is preserved. Ovis2.5 remains host/profile unsupported. No current evidence establishes project-specific P7 acceleration, so `research_value_verdict: INCONCLUSIVE` is correct.

The remaining non-implementation gate after this audit is final exact-head repository CI/governance and PR/review closeout. The missing Track B screenshot dataset is not repaired or weakened; it remains the explicit reason the benchmark result is `PARTIAL`, not a reason to run a forbidden identical E2E.
